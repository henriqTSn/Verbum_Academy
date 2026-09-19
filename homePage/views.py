from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from accounts.models import UserProfile
from accounts.views import login_view


def homePage(request):

	if request.method == 'POST':
		# Encaminha o login da home para o login_view (bloqueio, 2FA e logs)
		return login_view(request)

	return render(request, 'login.html')


def register_page(request):
	return redirect('/accounts/register/')
