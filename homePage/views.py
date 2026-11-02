from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accounts.models import UserProfile
from accounts.views import login_view

from .vocabulario import PALAVRAS, CHUNKS

def homePage(request):

	if request.method == 'POST':
		# Encaminha o login da home para o login_view (bloqueio, 2FA e logs)
		return login_view(request)

	return render(request, 'login.html')


def register_page(request):
	return redirect('/accounts/register/')


@login_required
def vocabulario(request):
	pesquisa = request.GET.get("q","").strip().casefold()
	categoria = request.GET.get("categoria", "").strip()

	categorias = sorted({
		palavra["category"]
		for palavra in PALAVRAS
	})

	palavras_filtradas = [
		palavra
		for palavra in PALAVRAS
		if(
			not pesquisa
			or pesquisa in palavra["word"].casefold()
			or pesquisa in palavra["translation"].casefold()
		)
			and(
				not categoria
				or palavra["category"] == categoria
			)
	]

	return render(
		request,
		"vocabulario.html",
		{
			"palavras": palavras_filtradas,
			"categorias": categorias,
			"pesquisa": request.GET.get("q", ""),
			"categoria_selecionada": categoria,
		},
	)



@login_required
def chunks(request):

    pesquisa = request.GET.get("q", "").strip().casefold()
    categoria = request.GET.get("categoria", "").strip()
    categorias = sorted({
        chunk["category"]
        for chunk in CHUNKS
    })

    chunks_filtrados = [
        chunk
        for chunk in CHUNKS

        if (

            not pesquisa
            or pesquisa in chunk["word"].casefold()
            or pesquisa in chunk["translation"].casefold()
        )

        and (
            not categoria
            or chunk["category"] == categoria
        )
    ]
    return render(
        request,
        "chunks.html",
        {
            "chunks": chunks_filtrados,
            "categorias": categorias,
            "pesquisa": request.GET.get("q", ""),
            "categoria_selecionada": categoria,
        },
    )
