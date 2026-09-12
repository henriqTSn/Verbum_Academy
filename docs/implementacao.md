# Documentação da Implementação

## Projeto Integrador - Autenticação, Credenciais e Recuperação de Senha

Este documento relaciona cada funcionalidade aos arquivos do código.

---

## 1. Cadastro

Função `register()` em `accounts/views.py`. Criação com `create_user()`.

---

## 2. Login

Função `login_view()` em `accounts/views.py`. Busca por e-mail (`iexact`) e `authenticate()`.

---

## 3. Tentativas de login

`MAX_LOGIN_ATTEMPTS = 5` e bloqueio de 5 minutos. Campos `failed_login_attempts` e `locked_until`.

---

## 4. 2FA

Biblioteca `pyotp`. Funções `setup_2fa()` e `verify_2fa()`.

---

## 5. Sessão

`@login_required`, `SESSION_COOKIE_AGE = 1800`, `SESSION_SAVE_EVERY_REQUEST = True`, `SESSION_COOKIE_HTTPONLY = True`.

---

## 6. Logout

Função `logout_view()`.

---

## 7. Validação de senha

Validadores configurados em `Verbum/settings.py`.

---

## 8. Recuperação de senha

Classes em `accounts/views.py`:

- `PasswordResetRequestView`
- `PasswordResetConfirmView`

Rotas em `accounts/urls.py`. Timeout: `PASSWORD_RESET_TIMEOUT = 900`.

Em desenvolvimento, o link é emitido pelo backend de e-mail de console.

---

## 9. Criptografia de dados sensíveis

O campo `totp_secret` do modelo `UserProfile` é criptografado antes de ser armazenado no banco de dados.

A lógica de criptografia está separada em `accounts/crypto.py`, utilizando a biblioteca `cryptography` e o esquema Fernet.

As funções utilizdas são:


-`encrypt_totp_secret()` - criptografa o segredo TOTP antes do armazenamento.

-`decrypt_totp_secret()` - descriptografa o segredo quando necessário para validar o 2FA.


A chave utilizada pelo Fernet é obtida por meio da variável de ambiente `VERBUM_ENCRYPTION_KEY`.

O fluxo de configuração e validação do 2FA utiliza essas funções em `setup_2fa()` e `verify_2fa()`, respectivamente.

Também foi criada uma migration para criptografar os segredos TOTP que já existiam no banco antes da alteração da implementação.

---

## 10. Estrutura

- `accounts/views.py` — cadastro, login, 2FA, logout e recuperação
- `accounts/models.py` — `UserProfile`
- `acounts/crypto.py` — funções de criptografia e descriptografia dos segredos TOTP
- `accounts/urls.py` — rotas, inclusive `password-reset`
- `Verbum/settings.py` — sessão, validadores, timeout e log

---

## 11. Considerações

A comprovação é feita pelos testes de front-end e pelas evidências em `docs/evidencias/`.

---

## 11. Conformidade com a LGPD

Mapeamento do código dos direitos do titular (itens 4.1 a 4.11).

| Elemento | Local |
| --- | --- |
| ConsentRecord (finalidade, data, versão, revogação) | `accounts/models.py` |
| Cadastro com checkbox de consentimento | `accounts/views.py` → `register()` |
| Consulta dos dados | `accounts/views.py` → `privacidade()` |
| Exportação JSON | `accounts/views.py` → `exportar_dados()` |
| Revogar / renovar consentimento | `accounts/views.py` → `revogar_consentimento()` |
| Exclusão da conta | `accounts/views.py` → `excluir_conta()` |
| Política versionada v1.0 | `templates/accounts/politica_privacidade.html` |

Rotas:

- `/accounts/politica-privacidade/`
- `/accounts/privacidade/`
- `/accounts/privacidade/exportar/`
- `/accounts/privacidade/consentimento/`
- `/accounts/privacidade/excluir/`

O JSON de exportação e os logs **não** incluem senha, salt, token nem segredo TOTP.

Detalhamento: `docs/lgpd.md`. Testes: `docs/lgpd-testes.md`.
