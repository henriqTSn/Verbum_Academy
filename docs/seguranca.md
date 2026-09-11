# Segurança

## Projeto Integrador - Autenticação, Credenciais e Recuperação de Senha

---

## 1. Proteção das senhas

Uso de `create_user()` e do sistema de hash do Django. A senha não é gravada em texto puro.

---

## 2. Validação das senhas

Validadores nativos do Django em `Verbum/settings.py`.

---

## 3. Tentativas de login

5 tentativas e bloqueio de 5 minutos.

---

## 4. 2FA

TOTP com `pyotp`. Campos `totp_secret` e `two_factor_enabled`.

---

## 5. Sessão e cookie

`@login_required`, sessão de 30 minutos e `SESSION_COOKIE_HTTPONLY = True`.

---

## 6. Logout

`logout()` do Django em `logout_view()`.

---

## 7. Recuperação de senha

Token do `PasswordResetTokenGenerator`, sem gravação no banco.

Expiração: 900 segundos. Uso único. Falha visível no front-end para token inválido.

Logs de evento em `verbum.log`, sem senha, token, uid ou e-mail.

---

## 8. Resumo

| Mecanismo | Implementação |
| --- | --- |
| Validação de senha | Validadores do Django |
| Hash da senha | Sistema de autenticação do Django |
| Tentativas | 5 |
| Bloqueio | 5 minutos |
| 2FA | TOTP / `pyotp` |
| Sessão | 30 minutos + HttpOnly |
| Recuperação | Token temporário + logs |
| Expiração do token | 900 segundos |


---

## 9. Dados pessoais e LGPD

- Cadastro pede só usuário, e-mail e senha (minimização).
- Consentimento gravado com finalidade, data e versão da política (`ConsentRecord`).
- Titular consulta, exporta (JSON) e exclui a conta pelo front-end.
- Exclusão exige e-mail + senha atual.
- Logs de consentimento, acesso, exportação e exclusão **não** gravam senha, token ou segredo TOTP.
- Política pública versionada em `/accounts/politica-privacidade/`.

Documentação: `docs/lgpd.md`.
