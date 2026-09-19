from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.conf import settings
from .models import UserProfile, ConsentRecord
from django.contrib.auth import views as auth_views
from accounts.crypto import encrypt_totp_secret, decrypt_totp_secret
import pyotp
import logging

logger = logging.getLogger(__name__)

# Máximo de tentativas
MAX_LOGIN_ATTEMPTS = 5

# Duração do bloqueio
LOCKOUT_DURATION = timedelta(minutes=5)


def _client_ip(request):
	# IP do cliente para o registro de auditoria
	return request.META.get('REMOTE_ADDR', '-')


def audit_log(request, event, success, message, user=None, email=None):
	# Grava evento crítico em verbum.log.
	# Não registra senha, token, código 2FA, secret TOTP ou hash.
	if user is not None:
		user_id = getattr(user, 'id', '-')
		email = email or getattr(user, 'email', '-')
	else:
		user_id = '-'
		email = email or '-'

	logger.info(
		'event=%s success=%s user_id=%s email=%s ip=%s message=%s',
		event,
		str(success).lower(),
		user_id,
		email,
		_client_ip(request),
		message,
	)


def register(request):

	if request.method == 'POST':

		username = request.POST.get('username')
		email = request.POST.get('email')
		password = request.POST.get('password')
		password_confirmation = request.POST.get('password_confirmation')

		# Se a senha e a confirmação forem diferentes, o cadastro não segue
		if password != password_confirmation:
			return render(
				request,
				'register.html',
				{'error': 'As senhas não coincidem.'}
			)

		# Impede cadastro com nome de usuário que já existe
		if User.objects.filter(username=username).exists():
			return render(
				request,
				'register.html',
				{'error': 'Este nome de usuário já está cadastrado.'}
			)

		# Aplica os validadores de senha configurados no settings.py
		try:
			validate_password(password)
		except ValidationError as e:
			return render(
				request,
				'register.html',
				{'error': ' '.join(e.messages)}
			)

		# Sem o aceite da política o cadastro não é criado (consentimento livre, art. 8º)
		if not request.POST.get('consent'):
			return render(
				request,
				'register.html',
				{'error': 'É necessário aceitar a Política de Privacidade para criar a conta.'}
			)

		# A senha não é gravada em texto puro; o Django aplica o hash
		user = User.objects.create_user(
			username=username,
			email=email,
			password=password
		)

		UserProfile.objects.create(user=user)

		# Registra finalidade, data (auto) e versão da política
		ConsentRecord.objects.create(
			user=user,
			purpose=ConsentRecord.PURPOSE_DEFAULT,
			granted=True,
			policy_version="1.0",
			source="register",
		)
		logger.info("Consentimento registrado no cadastro.")

		return render(
			request,
			'register.html',
			{'success': 'Usuário cadastrado com sucesso!'}
		)

	return render(request, 'register.html')


def login_view(request):

	# A tela de login está na home. Esta rota não renderiza /accounts/login/
	if request.method != 'POST':
		return redirect('/')

	# Primeiramente nós pegamos os dados inseridos pelo usuário sendo eles email e senha
	email = request.POST.get('email')
	password = request.POST.get('password')

	# Aqui o código ignora se o email foi escrito com letras maiúsculas ou minúsculas com o iexact
	try:
		user = User.objects.get(email__iexact=email)
	except User.DoesNotExist:
		user = None

	if user is not None:

		# CORREÇÃO DO ERRO 500: antes o código fazia "profile = user.userprofile",
		# que quebra (lança exceção e gera 500) se esse usuário não tiver um
		# UserProfile associado — o que acontece com contas criadas fora do
		# fluxo de registro do site (ex: pelo Django Admin ou createsuperuser).
		# get_or_create busca o perfil e, se não existir, cria um automaticamente
		# na hora, então o login nunca mais quebra por causa disso.
		profile, _ = UserProfile.objects.get_or_create(user=user)

		# Verifica se a conta está temporariamente bloqueada
		if profile.locked_until is not None:

			if timezone.now() < profile.locked_until:
				# Auditoria: tentativa enquanto a conta ainda está bloqueada
				audit_log(
					request,
					event='ACCOUNT_LOCKED',
					success=False,
					message='Conta bloqueada por excesso de tentativas.',
					user=user,
					email=user.email,
				)
				messages.error(request, 'Conta temporariamente bloqueada. Tente novamente mais tarde.')
				return redirect('/')

			# Se o período de bloqueio terminou, a conta é liberada
			profile.locked_until = None
			profile.failed_login_attempts = 0
			profile.save(
				update_fields=['locked_until', 'failed_login_attempts']
			)

		# Aqui verifica a senha e se estiver correta o authenticate_user será um usuário e se estiver errada será none
		authenticated_user = authenticate(
			request,
			username=user.username,
			password=password
		)

		# Essa parte é a que cria a sessão de autenticação do usuário e redireciona o usuário para a página painel após o login.
		if authenticated_user is not None:

			# A senha está correta, então zeramos as tentativas anteriores
			profile.failed_login_attempts = 0
			profile.locked_until = None
			profile.save(
				update_fields=['failed_login_attempts', 'locked_until']
			)

			# Auditoria: autenticação primária concluída (ainda pode faltar o 2FA)
			audit_log(
				request,
				event='LOGIN_SUCCESS',
				success=True,
				message='Autenticação primária concluída com sucesso.',
				user=authenticated_user,
				email=authenticated_user.email,
			)

			# Se o usuário possui 2FA ativado, ainda não fazemos o login
			if profile.two_factor_enabled:

				# Guardamos temporariamente o ID do usuário na sessão
				request.session['pending_2fa_user_id'] = authenticated_user.id

				# Enviamos o usuário para a tela de validação do 2FA
				return redirect('verify_2fa')

			# Se o 2FA não estiver ativado, o login continua normalmente
			auth_login(request, authenticated_user)
			return redirect('painel')

		else:

			# A senha informada está incorreta
			profile.failed_login_attempts += 1

			# Se atingir o limite, a conta é bloqueada temporariamente
			if profile.failed_login_attempts >= MAX_LOGIN_ATTEMPTS:

				profile.locked_until = timezone.now() + LOCKOUT_DURATION
				profile.save(
					update_fields=['failed_login_attempts', 'locked_until']
				)
				# Auditoria: senha errada e limite de tentativas atingido
				audit_log(
					request,
					event='LOGIN_FAILURE',
					success=False,
					message='Falha na autenticação primária.',
					user=user,
					email=user.email,
				)
				audit_log(
					request,
					event='ACCOUNT_LOCKED',
					success=False,
					message='Conta bloqueada por excesso de tentativas.',
					user=user,
					email=user.email,
				)
				messages.error(request, 'Conta temporariamente bloqueada. Tente novamente mais tarde.')
				return redirect('/')

			profile.save(
				update_fields=['failed_login_attempts']
			)
			# Auditoria: senha errada, ainda sem bloqueio
			audit_log(
				request,
				event='LOGIN_FAILURE',
				success=False,
				message='Falha na autenticação primária.',
				user=user,
				email=user.email,
			)

	else:
		# Auditoria: e-mail inexistente (mesma mensagem da senha errada)
		audit_log(
			request,
			event='LOGIN_FAILURE',
			success=False,
			message='Falha na autenticação primária.',
			email=email or '-',
		)

	messages.error(request, 'Email ou senha inválidos.')
	return redirect('/')


# tela de perfil do usuario
@login_required(login_url="homePage")
def perfil(request):
    return render(request, "accounts/user.html")


# Diferente das outras funções não coloquei o @login_required aqui pois o usuário ainda não é considerado autenticado pelo Django
def verify_2fa(request):

	# Aqui pegamos o ID do usuário que passou pela primeira etapa do login que está armazenado em pending_2fa_user_id
	user_id = request.session.get('pending_2fa_user_id')

	# Se não tem usuário aguardando o 2FA, volta para a home
	if not user_id:
		return redirect('/')

	try:
		user = User.objects.get(id=user_id)
	except User.DoesNotExist:
		request.session.pop('pending_2fa_user_id', None)
		return redirect('/')

	# CORREÇÃO: mesma troca do login_view. "user.userprofile" direto quebraria
	# com 500 se esse usuário não tivesse UserProfile; get_or_create é seguro.
	profile, _ = UserProfile.objects.get_or_create(user=user)

	if request.method == 'POST':

		codigo = request.POST.get('codigo', '').strip()
		secret = decrypt_totp_secret(profile.totp_secret)
		totp = pyotp.TOTP(secret)

		if totp.verify(codigo):

			# O segundo fator foi validado
			auth_login(request, user)

			# Auditoria: TOTP válido. O código digitado NÃO entra no log.
			audit_log(
				request,
				event='2FA_SUCCESS',
				success=True,
				message='Validação de 2FA concluída com sucesso.',
				user=user,
				email=user.email,
			)

			# Remove o estado temporário da sessão
			request.session.pop('pending_2fa_user_id', None)
			return redirect('painel')

		# Auditoria: TOTP inválido. O código digitado NÃO entra no log.
		audit_log(
			request,
			event='2FA_FAILURE',
			success=False,
			message='Falha na validação de 2FA.',
			user=user,
			email=user.email,
		)
		return render(
			request,
			'verify_2fa.html',
			{'error': 'Código 2FA inválido.'}
		)

	return render(request, 'verify_2fa.html')


# Somente um usuário autenticado pode acessar essa página painel.
@login_required
def painel(request):
	return render(request, 'painel.html')


# Somente um usuário autenticado pode acessar essa página setup2fa.
@login_required
def setup_2fa(request):

	# CORREÇÃO: mesma troca das outras funções. Como aqui é
	# "request.user.userprofile", o mesmo risco de 500 existe caso o usuário
	# logado não tenha UserProfile. get_or_create resolve isso.
	profile, _ = UserProfile.objects.get_or_create(user=request.user)

	# Se o usuário não tiver um secret TOTP a condicional é True, cria um secret aleatório encripta ele e salva no banco.
	# Se o usuário já tiver 2fa a variável secret é descriptografada
	if not profile.totp_secret:
		secret = pyotp.random_base32()
		profile.totp_secret = encrypt_totp_secret(secret)
		profile.save()
	else:
		secret = decrypt_totp_secret(profile.totp_secret)

	totp = pyotp.TOTP(secret)

	# Se o usuário enviar o formulário nós entramos nesta parte POST /accounts/setup2fa/
	if 
