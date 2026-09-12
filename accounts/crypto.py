from cryptography.fernet import Fernet
from django.conf import settings


def _get_fernet():

	# Cria uma instância do Fernet usando a chave criptográfica fornecida pelas configurações do projeto.
	return Fernet(settings.VERBUM_ENCRYPTION_KEY)

def encrypt_totp_secret(secret):

	# Criptografa o secret totp antes que seja armazenado
	return _get_fernet().encrypt(secret.encode()).decode()

def decrypt_totp_secret(encrypted_secret):

	return _get_fernet().decrypt(encrypted_secret.encode()).decode()