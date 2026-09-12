from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

	# Significa que cada usuário possui um único UserProfile
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE

	)

	# Aqui é onde o secret TOTP é armazenado 
	# o motivo do blank=True e null=True é que nem todo usuário imediatamente terá 2FA configurado
	totp_secret = models.CharField(
		max_length=255,
		blank=True,
		null=True

	)

	# Por padrão vai estar False e se o usuário ativar o 2FA 
	# o two_factor_enabled manda o usuário para a tela de 2FA
	two_factor_enabled = models.BooleanField(
		default=False
	)

	# Por padrão o valor será igual a 0 e representa as vezes consecutivas de senhas digitadas errada
	failed_login_attempts = models.PositiveIntegerField(
		default=0
	)

	# Até que momento a conta permanecerá bloqueada
	locked_until = models.DateTimeField(
		null=True, 
		blank=True
	)