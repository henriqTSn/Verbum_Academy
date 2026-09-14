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
				messages.error(request, 'Conta temporariamente bloqueada. Tente novamente mais tarde.')
				return redirect('/')

			profile.save(
				update_fields=['failed_login_attempts']
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

			# Remove o estado temporário da sessão
			request.session.pop('pending_2fa_user_id', None)
			return redirect('painel')

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
	if request.method == 'POST':

		# Aqui pegamos o código digitado pelo usuário
		codigo = request.POST.get('codigo', '').strip()

		# Faz a verificação do código, se for True entra nessa condicional, habilita 2FA e salva.
		if totp.verify(codigo):
			profile.two_factor_enabled = True
			profile.save()
			messages.success(
				request,
				'Autenticação em dois fatores ativada com sucesso!'
			)
			return redirect('painel')

		messages.error(
			request,
			'Código inválido. Tente novamente.'
		)

	provisioning_uri = totp.provisioning_uri(
		name=request.user.email,
		issuer_name='Verbum'
	)

	return render(
		request,
		'accounts/setup_2fa.html',
		{
			'secret': secret,
			'provisioning_uri': provisioning_uri,
		}
	)


def logout_view(request):

	# Encerra a sessão do usuário
	logout(request)
	return redirect('/')


class PasswordResetRequestView(auth_views.PasswordResetView):

	def form_valid(self, form):

		# Aqui faz um registro de solicitação de recuperação de senha recebida, e nenhum token ou link é armazenado no log
		logger.info('Solicitação de recuperação de senha recebida.')
		return super().form_valid(form)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):

	# Assim que o usuário enviar a solicitação, o django verifica o token de recuperação
	def dispatch(self, request, *args, **kwargs):

		response = super().dispatch(request, *args, **kwargs)

		# Se o django identificar que o link contém um token inválido ou expirado, registra a tentativa
		if getattr(response, 'context_data', {}).get('validlink') is False:
			logger.warning('Tentativa de recuperação de senha com token inválido ou expirado.')

		return response

	# Assim que o usuário digitar duas senhas iguais no link contendo o token o django chama esse método
	def form_valid(self, form):

		# Faz o registro de que a recuperação de senha foi concluida mas não adiciona nenhuma senha ou token
		logger.info('Recuperação de senha concluída com sucesso.')
		return super().form_valid(form)


def politica_privacidade(request):

	# Texto público e versionado da política. Não exige login.
	return render(
		request,
		'accounts/politica_privacidade.html',
		{'policy_version': '1.0'},
	)


@login_required
def privacidade(request):

	# Consulta dos dados do titular autenticado (item 4.8)
	logger.info("Titular consultou os dados pessoais.")
	ultimo = request.user.consents.first()
	return render(
		request,
		'accounts/privacidade.html',
		{'ultimo_consentimento': ultimo},
	)


@login_required
def exportar_dados(request):

	# Exportação em JSON sem senha, salt ou segredo TOTP (item 4.9)
	ultimo = request.user.consents.first()
	payload = {
		'username': request.user.username,
		'email': request.user.email,
		'date_joined': request.user.date_joined.isoformat(),
		'consentimento': None if ultimo is None else {
			'finalidade': ultimo.purpose,
			'concedido': ultimo.granted,
			'data': ultimo.granted_at.isoformat(),
			'revogado_em': None if ultimo.revoked_at is None else ultimo.revoked_at.isoformat(),
			'versao_politica': ultimo.policy_version,
		},
	}
	logger.info("Titular exportou os dados pessoais.")
	response = JsonResponse(payload, json_dumps_params={'ensure_ascii': False, 'indent': 2})
	response['Content-Disposition'] = 'attachment; filename="meus-dados-verbum.json"'
	return response


@login_required
def revogar_consentimento(request):

	# Revoga ou renova o consentimento (item 4.6)
	if request.method != 'POST':
		return redirect('privacidade')

	ultimo = request.user.consents.first()
	if ultimo is not None and ultimo.granted:
		ultimo.granted = False
		ultimo.revoked_at = timezone.now()
		ultimo.save(update_fields=['granted', 'revoked_at'])
		logger.info("Titular revogou o consentimento.")
		messages.success(request, 'Consentimento revogado.')
	else:
		ConsentRecord.objects.create(
			user=request.user,
			purpose=ConsentRecord.PURPOSE_DEFAULT,
			granted=True,
			policy_version='1.0',
			source='privacidade',
		)
		logger.info("Titular renovou o consentimento.")
		messages.success(request, 'Consentimento renovado (política v1.0).')

	return redirect('privacidade')


@login_required
def excluir_conta(request):

	# Exclusão da conta com confirmação de e-mail e senha (item 4.10)
	if request.method != 'POST':
		return redirect('privacidade')

	email = request.POST.get('email', '')
	password = request.POST.get('password', '')

	if email.lower() != request.user.email.lower():
		messages.error(request, 'O e-mail informado não confere.')
		return redirect('privacidade')

	if authenticate(request, username=request.user.username, password=password) is None:
		messages.error(request, 'Senha incorreta. A conta não foi excluída.')
		return redirect('privacidade')

	logger.info("Titular solicitou exclusão da conta.")
	user = request.user
	logout(request)
	user.delete()
	return render(request, 'accounts/conta_excluida.html')
