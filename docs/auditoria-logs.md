# Auditoria e Logs

Etapa do Projeto Integrador — itens 5.1 a 5.4 do checklist e item 4.5 do enunciado.

Este documento descreve como o Verbum registra eventos críticos de segurança, como o log é protegido e como ele pode ser analisado.

A lista oficial dos eventos está em `docs/auditoria-eventos.md`.

## Objetivo

Atender ao requisito de registro e proteção de eventos críticos de segurança:

- logs de autenticação (5.1)
- logs de falhas e 2FA (5.2)
- proteção contra alteração dos logs (5.3)
- exemplo de análise de logs (5.4)

## Onde o log é gravado

A configuração está em `Verbum/settings.py`.

- destino: arquivo `verbum.log` na raiz do projeto
- origem: logger do app `accounts`
- nível: INFO
- o arquivo é escrito pela aplicação, em modo append (`mode='a'`)

Eventos já registrados em etapas anteriores (sem senha, token ou secret TOTP):

- solicitação de recuperação de senha
- falha de token inválido ou expirado
- sucesso da recuperação de senha
- consulta, exportação, revogação e exclusão de dados pessoais

Eventos desta etapa (autenticação, bloqueio, logout e 2FA) são gravados no mesmo `verbum.log`, sem criar tabela no banco.

## Implementação

Função `audit_log()` em `accounts/views.py`.

Chamada em:

- `login_view()` — `LOGIN_SUCCESS`, `LOGIN_FAILURE`, `ACCOUNT_LOCKED`
- `verify_2fa()` — `2FA_SUCCESS`, `2FA_FAILURE`
- `logout_view()` — `LOGOUT` (antes de encerrar a sessão)

A home encaminha o POST do login para `login_view()`.
Consulta somente leitura: `GET /accounts/auditoria/` (sem POST, sem editar, sem apagar).

## Eventos desta etapa

| Evento | Item | Situação |
|---|---|---|
| LOGIN_SUCCESS | 5.1 | Implementado |
| LOGIN_FAILURE | 5.2 | Implementado |
| ACCOUNT_LOCKED | 5.2 | Implementado |
| LOGOUT | 5.1 | Implementado |
| 2FA_SUCCESS | 5.2 | Implementado |
| 2FA_FAILURE | 5.2 | Implementado |

Nenhum desses registros guarda senha, token de recuperação, código 2FA, secret TOTP ou hash da senha.

## Proteção contra alteração (5.3)

1. O log não é editável pela interface do aluno.
2. A gravação ocorre só pela aplicação, via `logging` do Django, em modo append.
3. O arquivo `verbum.log` não é servido como página pública.
4. A tela `/accounts/auditoria/` apenas consulta as últimas linhas.
5. Não há tela para alterar ou apagar linha de log.
6. O conteúdo não inclui segredo que, se vazado, permita recriar a senha ou o 2FA.

Assim, um usuário comum não consegue falsificar o histórico pela aplicação.

## Evidências pelo front-end

- `33-2fa-falha.png` — código 2FA inválido
- `34-2fa-sucesso.png` — painel após 2FA válido
- `35-logout.png` — sessão encerrada
- `36-tela-auditoria.png` — consulta somente leitura do log
- `32-conta-bloqueada.png` — bloqueio após 5 tentativas

## Exemplo de análise de logs (5.4)

Trecho esperado no `verbum.log` após os testes no front-end:

```text
event=LOGIN_FAILURE success=false email=marciamazoni@gmail.com message=Falha na autenticação primária.
event=ACCOUNT_LOCKED success=false email=marciamazoni@gmail.com message=Conta bloqueada por excesso de tentativas.
event=LOGIN_SUCCESS success=true email=marciamazoni@gmail.com message=Autenticação primária concluída com sucesso.
event=2FA_FAILURE success=false email=marciamazoni@gmail.com message=Falha na validação de 2FA.
event=2FA_SUCCESS success=true email=marciamazoni@gmail.com message=Validação de 2FA concluída com sucesso.
event=LOGOUT success=true email=marciamazoni@gmail.com message=Sessão encerrada pelo usuário.
