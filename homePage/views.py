from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from accounts.models import UserProfile


def homePage(request):

	if request.method == 'POST':

		email = request.POST.get('email')
		password = request.POST.get('password')

		try:
			user = User.objects.get(email__iexact=email)
		except User.DoesNotExist:
			user = None

		if user is not None:

			profile, _ = UserProfile.objects.get_or_create(user=user)
			authenticated_user = authenticate(
				request,
				username=user.username,
				password=password
			)

			if authenticated_user is not None:

				if profile.two_factor_enabled:
					request.session['pending_2fa_user_id'] = authenticated_user.id
					return redirect('verify_2fa')

				auth_login(request, authenticated_user)
				return redirect('painel')

		messages.error(request, 'Email ou senha inválidos.')
		return redirect('/')

	return render(request, 'login.html')


def register_page(request):
	return redirect('/accounts/register/')
