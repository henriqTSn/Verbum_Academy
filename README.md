# Verbum Academy

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

Implementado nesta entrega (Lei nº 13.709/2018, itens 4.1 a 4.11):

- Inventário de dados pessoais com finalidade e base legal
- Minimização (cadastro sem CPF, telefone ou dado sensível)
- Consentimento explícito, com finalidade, data e versão da política
- Revogação do consentimento
- Consulta dos dados do titular
- Exportação em JSON
- Exclusão da conta e dos dados pessoais

Documentação: `docs/lgpd.md`  
Política versionada: `docs/politica-privacidade.md`

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
- Documentação da etapa 3: docs/lgpd.md
- Quadro Kanban: https://github.com/users/sarahmazoni/projects/1

## Status

Projeto em desenvolvimento.
