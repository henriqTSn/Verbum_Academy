# Checklist de Requisitos — Conformidade com a LGPD

## Projeto Integrador — Etapa 3

Este documento apresenta os requisitos 4.1 a 4.11 implementados no Verbum.
A documentação foi feita com base nas funcionalidades presentes no código.
Os testes são realizados através da interface da aplicação (front-end).

Detalhamento técnico: `docs/lgpd.md`.  
Roteiro de testes: `docs/lgpd-testes.md`.  
Política versionada: `docs/politica-privacidade.md`.

---

## 4.1 Listagem dos dados pessoais

**Status:** Implementado

O sistema coleta apenas: nome de usuário, e-mail, hash da senha, dados opcionais de 2FA, controles de bloqueio, sessão e registros de consentimento.

**Evidências:** `33-consulta-dados.png`

---

## 4.2 Finalidade de cada dado

**Status:** Implementado

Cada campo está associado a uma finalidade e a uma base legal do art. 7º na tabela de inventário de `docs/lgpd.md`.

**Evidências:** `33-consulta-dados.png`, `34-consentimento-data-versao.png`

---

## 4.3 Minimização

**Status:** Implementado

O cadastro não pede CPF, telefone, foto nem dado sensível. Sem o aceite da política a conta não é criada.

**Evidências:** `30-cadastro-sem-consentimento.png`, `31-cadastro-com-consentimento.png`

---

## 4.4 Registro explícito de consentimento

**Status:** Implementado

Checkbox desmarcado por padrão no cadastro. Persistência em `ConsentRecord`.

**Evidências:** `31-cadastro-com-consentimento.png`

---

## 4.5 Consentimento associado à finalidade

**Status:** Implementado

O campo `purpose` grava a finalidade da prestação do serviço Verbum.

**Evidências:** `34-consentimento-data-versao.png`

---

## 4.6 Revogação

**Status:** Implementado

O titular revoga o consentimento em `/accounts/privacidade/consentimento/`.

**Evidências:** `36-revogacao-consentimento.png`

---

## 4.7 Data e versão

**Status:** Implementado

`granted_at` + `policy_version` (`1.0`) visíveis na tela e no JSON exportado.

**Evidências:** `34-consentimento-data-versao.png`, `35-exportacao-json.png`

---

## 4.8 Consulta

**Status:** Implementado

Painel autenticado em `/accounts/privacidade/`. Sem hash de senha e sem segredo TOTP.

**Evidências:** `33-consulta-dados.png`, `33b-privacidade-sem-login.png`

---

## 4.9 Exportação

**Status:** Implementado

Download de `verbum-dados.json` (formato estruturado e de uso comum).

**Evidências:** `35-exportacao-json.png`

---

## 4.10 Exclusão

**Status:** Implementado

Exclusão da conta com confirmação de e-mail e senha. Login posterior falha.

**Evidências:** `37-exclusao-confirmacao.png`, `38-exclusao-concluida.png`

---

## 4.11 Fluxo documentado

**Status:** Implementado

Fluxo descrito em `docs/lgpd.md` (seção 8) e exercitado pelos testes acima.

---

## Resumo

| Requisito | Status |
| --- | --- |
| 4.1 Inventário | Implementado |
| 4.2 Finalidade | Implementado |
| 4.3 Minimização | Implementado |
| 4.4 Consentimento explícito | Implementado |
| 4.5 Finalidade no aceite | Implementado |
| 4.6 Revogação | Implementado |
| 4.7 Data e versão | Implementado |
| 4.8 Consulta | Implementado |
| 4.9 Exportação | Implementado |
| 4.10 Exclusão | Implementado |
| 4.11 Fluxo documentado | Implementado |
