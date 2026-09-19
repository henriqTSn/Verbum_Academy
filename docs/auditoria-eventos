# Especificação dos logs de auditoria

Etapa do Projeto Integrador: Auditoria e Logs (itens 5.1 a 5.4 / 4.5).

Este arquivo define o que o sistema deve gravar. A implementação vem no passo seguinte.

## Eventos obrigatórios

| Evento | Quando gravar | Sucesso | Item |
|---|---|---|---|
| LOGIN_SUCCESS | Senha correta na autenticação primária | sim | 5.1 |
| LOGIN_FAILURE | Senha incorreta ou falha na autenticação primária | não | 5.2 |
| ACCOUNT_LOCKED | Conta bloqueada após 5 tentativas | não | 5.2 |
| LOGOUT | Usuário encerra a sessão | sim | 5.1 |
| 2FA_SUCCESS | Código TOTP válido | sim | 5.2 |
| 2FA_FAILURE | Código TOTP inválido ou ausente | não | 5.2 |

## Campos de cada registro

- created_at
- event
- user_id (quando existir usuário)
- email
- ip_address
- success
- message

## Mensagens padrão

- LOGIN_SUCCESS: Autenticação primária concluída com sucesso.
- LOGIN_FAILURE: Falha na autenticação primária.
- ACCOUNT_LOCKED: Conta bloqueada por excesso de tentativas.
- LOGOUT: Sessão encerrada pelo usuário.
- 2FA_SUCCESS: Validação de 2FA concluída com sucesso.
- 2FA_FAILURE: Falha na validação de 2FA.

## Proibido gravar

- senha
- token de recuperação
- código 2FA digitado
- secret TOTP
- hash da senha
