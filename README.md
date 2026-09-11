# Verbum Labs

## Plataforma de Aprendizagem de Idiomas

O **Verbum** é uma plataforma web de aprendizagem de idiomas baseada em vocabulário de alta frequência, gramática, expressões frequentes e acompanhamento individual do progresso do estudante.

## Objetivo

O projeto tem como objetivo disponibilizar uma plataforma que organize o aprendizado de idiomas de forma estruturada, permitindo que o usuário acompanhe seu desenvolvimento em diferentes áreas do idioma estudado.

## Funcionalidades

Implementadas nesta entrega:
- Cadastro e autenticação de usuários
- Autenticação em dois fatores (2FA)
- Recuperação de senha por token temporário (expiração 15 min, uso único e logs)


## Stack Tecnológico

### Backend

- Python
- Django

### Banco de Dados

- SQLite 

### Frontend

- HTML
- CSS
- JavaScript

### Arquitetura

O sistema utiliza a arquitetura MVT (Model-View-Template) disponibilizada pelo framework Django.

## Segurança

Implementados nesta entrega:
- Hash e salt das senhas (Django)
- 2FA (TOTP)
- Controle e expiração de sessões
- Proteção contra tentativas excessivas de autenticação
- Recuperação de senha por token HMAC temporário
- Logs de solicitação, sucesso e falha da recuperação (sem senha/token)

## Privacidade e LGPD

O sistema será desenvolvido considerando princípios de proteção de dados pessoais, permitindo ao usuário:

- Consultar seus dados
- Solicitar a exportação de seus dados
- Excluir sua conta
- Gerenciar seu consentimento

Os registros de consentimento considerarão informações como finalidade, data e versão do consentimento.

## Como executar

    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver

A aplicação estará disponível em http://127.0.0.1:8000/.

## Estrutura do Projeto

    Verbum/
    ├── accounts/
    ├── homePage/
    ├── templates/
    ├── docs/
    ├── Verbum/
    ├── manage.py
    ├── requirements.txt
    ├── README.md
    ├── LICENSE
    └── .gitignore

## Documentação

Os documentos de requisitos e escopo fornecidos para o Projeto Integrador estão disponíveis na pasta docs.

## Equipe

- Sarah
- Henrique
- Gabriel

## Entrega Atual
- Release: https://github.com/sarahmazoni/Verbum/releases/tag/v1.2.0
- Documentação da etapa 2: docs/recuperacao-senha.md
- Quadro Kanban: https://github.com/users/sarahmazoni/projects/1

## Status

Projeto em desenvolvimento.
