from django.db import migrations
from django.conf import settings
from cryptography.fernet import Fernet

def encrypt_existing_totp_secrets(apps, schema_editor):

	UserProfile = apps.get_model('accounts', 'UserProfile')

	cipher = Fernet(settings.VERBUM_ENCRYPTION_KEY)

	# Essa parte o código seleciona os usuários que possuem totp
	profiles = UserProfile.objects.exclude(totp_secret__isnull=True)

	for profile in profiles:

		# Aqui o código pega o secret em texto puro e transforma em ciphertext usando a chave Fernet do ambiente
		profile.totp_secret = cipher.encrypt(profile.totp_secret.encode()).decode()

		# Por último salva
		profile.save(update_fields=['totp_secret'])

class Migration(migrations.Migration):

	dependencies = [('accounts', '0003_alter_userprofile_totp_secret'),]

	operations = [migrations.RunPython(encrypt_existing_totp_secrets, reverse_code=migrations.RunPython.noop),]