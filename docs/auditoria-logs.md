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

O sistema já possui configuração de logging em `Verbum/settings.py`.

- destino: arquivo `verbum.log` na raiz do projeto
- origem: logger do app `accounts`
- nível: INFO
- o arquivo é escrito pela aplicação, em modo de acréscimo

Eventos já registrados em etapas anteriores (sem senha, token ou secret TOTP):

- solicitação de recuperação de senha
- falha de token inválido ou expirado
- sucesso da recuperação de senha
- consulta, exportação, revogação e exclusão de dados pessoais

Eventos desta etapa (autenticação, bloqueio, logout e 2FA) seguem a especificação de `docs/auditoria-eventos.md` e serão gravados no mesmo arquivo `verbum.log`, sem criar tabela no banco.

## Eventos desta etapa

| Evento | Item | Situação |
|---|---|---|
| LOGIN_SUCCESS | 5.1 | Especificado |
| LOGIN_FAILURE | 5.2 | Especificado |
| ACCOUNT_LOCKED | 5.2 | Especificado |
| LOGOUT | 5.1 | Especificado |
| 2FA_SUCCESS | 5.2 | Especificado |
| 2FA_FAILURE | 5.2 | Especificado |

Nenhum desses registros guarda senha, token de recuperação, código 2FA, secret TOTP ou hash da senha.

## Proteção contra alteração (5.3)

Justificativa técnica da proteção atual:

1. O log não é editável pela interface do aluno.
2. A gravação ocorre só pela aplicação, via `logging` do Django.
3. O arquivo `verbum.log` não é servido como página pública.
4. Não há tela para alterar ou apagar linha de log.
5. O conteúdo não inclui segredo que, se vazado, permita recriar a senha ou o 2FA.

Assim, um usuário comum não consegue falsificar o histórico pela aplicação.

## Evidências pelo front-end

Os testes desta etapa devem ser feitos pela interface, não só pelo terminal:

1. senha incorreta
2. conta bloqueada após 5 tentativas
3. senha correta e 2FA incorreto
4. senha correta e 2FA correto
5. logout

Os prints entram em `docs/evidencias/` depois que o registro desses eventos estiver ativo no `verbum.log`.

## Exemplo de análise de logs (5.4)

Formato esperado no `verbum.log`:

```text
INFO LOGIN_FAILURE email=aluno@email.com
INFO LOGIN_FAILURE email=aluno@email.com
INFO ACCOUNT_LOCKED email=aluno@email.com
INFO 2FA_FAILURE email=aluno@email.com
INFO 2FA_SUCCESS email=aluno@email.com
INFO LOGOUT email=aluno@email.com

## Implementação

Função `audit_log()` em `accounts/views.py`.
Chamada em `login_view()`, `verify_2fa()` e `logout_view()`.
A home encaminha o POST do login para `login_view()`.
Consulta: `GET /accounts/auditoria/` (sem POST, sem apagar, sem editar).

## Evidências de front-end

- `33-2fa-falha.png` — código 2FA inválido
- `34-2fa-sucesso.png` — painel após 2FA válido
- `35-logout.png` — sessão encerrada
- `36-tela-auditoria.png` — consulta somente leitura do log
- `32-conta-bloqueada.png` — bloqueio após 5 tentativas

## Exemplo de análise (5.4)

Trecho esperado no `verbum.log` após os testes no front-end:

```text
event=LOGIN_FAILURE success=false email=marciamazoni@gmail.com message=Falha na autenticação primária.
event=ACCOUNT_LOCKED success=false email=marciamazoni@gmail.com message=Conta bloqueada por excesso de tentativas.
event=LOGIN_SUCCESS success=true email=marciamazoni@gmail.com message=Autenticação primária concluída com sucesso.
event=2FA_FAILURE success=false email=marciamazoni@gmail.com message=Falha na validação de 2FA.
event=2FA_SUCCESS success=true email=marciamazoni@gmail.com message=Validação de 2FA concluída com sucesso.
event=LOGOUT success=true email=marciamazoni@gmail.com message=Sessão encerrada pelo usuário.
