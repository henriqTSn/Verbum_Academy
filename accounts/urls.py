from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', views.login_view, name='login'),
	path('painel/', views.painel, name='painel'),
	path('setup2fa/', views.setup_2fa, name='setup_2fa'),
	path('verify-2fa/', views.verify_2fa, name='verify_2fa'),
	path('logout/', views.logout_view, name='logout'),
	path('password-reset/', views.PasswordResetRequestView.as_view(template_name='password_reset_form.html'), name='password_reset'),
	path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
	path('password-reset-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
	path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
	path('politica-privacidade/', views.politica_privacidade, name='politica_privacidade'),
	path('privacidade/', views.privacidade, name='privacidade'),
	path('privacidade/exportar/', views.exportar_dados, name='exportar_dados'),
	path('privacidade/consentimento/', views.revogar_consentimento, name='revogar_consentimento'),
	path('privacidade/excluir/', views.excluir_conta, name='excluir_conta'),
]
