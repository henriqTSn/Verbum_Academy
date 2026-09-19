# Checklist de Requisitos

## Projeto Integrador - Autenticação, Credenciais e Recuperação de Senha

Este documento apresenta os requisitos implementados no projeto Verbum.

A documentação foi feita com base nas funcionalidades presentes no código. Os testes são realizados através da interface da aplicação (front-end).

---

## 1. Cadastro de usuário

**Status:** Implementado

O sistema possui uma tela de cadastro onde o usuário informa os dados necessários para criar uma conta.

Durante o cadastro, o sistema verifica se a senha e a confirmação de senha são iguais. Caso sejam diferentes, o cadastro não é realizado e uma mensagem de erro é apresentada.

O sistema também verifica se o nome de usuário já está cadastrado. Caso o usuário já exista, o cadastro não é realizado e uma mensagem de erro é apresentada.

Quando os dados estão corretos, o usuário é criado utilizando o método `create_user()` do Django.

A implementação está localizada em `accounts/views.py`, função `register()`.

### Evidências

- `01-cadastro-sucesso.png`
- `02-senhas-diferentes.png`
- `08-usuario-ja-existente.png`

---

## 2. Login

**Status:** Implementado

O sistema possui uma tela de login onde o usuário informa e-mail e senha.

O sistema busca o usuário pelo e-mail sem diferenciar maiúsculas e minúsculas e valida a senha com `authenticate()` do Django.

A implementação está em `accounts/views.py`, função `login_view()`.

### Evidências

- `03-tela-login.png`
- `04-email-invalido.png`
- `05-painel-com-login.png`
- `11-login-esqueci-senha.png`

---

## 3. Proteção contra várias tentativas de login

**Status:** Implementado

São permitidas até 5 tentativas incorretas. Depois disso a conta fica bloqueada por 5 minutos.

Campos no `UserProfile`: `failed_login_attempts` e `locked_until`.

### Evidência

- `09-bloqueio-tentativas.png`

---

## 4. Autenticação em dois fatores (2FA)

**Status:** Implementado

O 2FA usa TOTP com `pyotp`. Campos: `totp_secret` e `two_factor_enabled`.

Funções: `setup_2fa()` e `verify_2fa()`.

### Evidências

- `06-setup2fa-sem-login.png`
- `07-verifica-2fa.png`

---

## 5. Gerenciamento de sessão

**Status:** Implementado

O painel usa `@login_required`. Sessão de 30 minutos, `SESSION_SAVE_EVERY_REQUEST = True` e cookie `HttpOnly`.

### Evidências

- `05-painel-com-login.png`
- `06-setup2fa-sem-login.png`

---

## 6. Logout

**Status:** Implementado

Função `logout_view()` em `accounts/views.py`, usando `logout()` do Django.

---

## 7. Validação de senha

**Status:** Implementado

Validadores nativos do Django configurados em `Verbum/settings.py`.

### Evidência

- `10-teste_validacao_senha.png`

---

## 8. Recuperação de senha

**Status:** Implementado

Redefinição por token temporário. Classes `PasswordResetRequestView` e `PasswordResetConfirmView` em `accounts/views.py`.

`PASSWORD_RESET_TIMEOUT = 900` (15 minutos).

Logs de solicitação, sucesso e token inválido, sem gravar senha ou token.

Detalhamento em `docs/recuperacao-senha.md`.

### Evidências

- `11-login-esqueci-senha.png`
- `12-form-recuperacao.png`
- `13-email-enviado.png`
- `14-email-console.png`
- `15-nova-senha.png`
- `16-reset-sucesso.png`
- `17-token-reutilizado.png`
- `18-token-invalido.png`
- `19-log-solicitacao.png`
- `20-log-sucesso.png`
- `21-log-falha-token.png`

---

## 9. Resumo

| Requisito | Status |
| --- | --- |
| Cadastro de usuário | Implementado |
| Login | Implementado |
| Proteção contra tentativas excessivas | Implementado |
| Autenticação em dois fatores | Implementado |
| Gerenciamento de sessão | Implementado |
| Logout | Implementado |
| Validação de senha | Implementado |
| Recuperação de senha | Implementado |

---

## 10. Forma de comprovação

As evidências estão em `docs/evidencias`. Os testes foram feitos pelo front-end.


## 11. Auditoria e Logs

**Status:** Implementado

Eventos gravados em `verbum.log` pela função `audit_log()` em `accounts/views.py`.
Nenhum registro contém senha, token, código 2FA, secret TOTP ou hash.
A tela `/accounts/auditoria/` é somente leitura (item 5.3).

| Requisito | Status | Evidência |
|---|---|---|
| 5.1 Logs de autenticação registrados | Implementado | `34-2fa-sucesso.png`, `35-logout.png`, `docs/auditoria-logs.md` |
| 5.2 Logs de falhas e 2FA registrados | Implementado | `33-2fa-falha.png`, `32-conta-bloqueada.png` |
| 5.3 Proteção contra alteração dos logs | Implementado | tela somente leitura, arquivo em modo append, sem edição |
| 5.4 Exemplo de análise de logs apresentado | Implementado | seção 5.4 de `docs/auditoria-logs.md` + `36-tela-auditoria.png` |
