# Testes da Aplicação

## Projeto Integrador — Conformidade com a LGPD

Os testes foram realizados pelo front-end. Evidências em `docs/evidencias/`.

---

## 1. Cadastro recusado sem consentimento

Acessar `/accounts/register/`, preencher usuário, e-mail e senha e enviar **sem** marcar o checkbox da política.

**Evidências:** `30-cadastro-sem-consentimento.png`  
**Resultado:** Aprovado (cadastro não é criado).

---

## 2. Cadastro com consentimento explícito

Marcar o checkbox, concluir o cadastro e abrir o painel de privacidade. Conferir finalidade, data e versão `1.0`.

**Evidências:** `31-cadastro-com-consentimento.png`, `34-consentimento-data-versao.png`  
**Resultado:** Aprovado.

---

## 3. Política de privacidade pública

Abrir `/accounts/politica-privacidade/` sem estar autenticado. O texto deve exibir a versão `1.0`.

**Evidências:** `32-politica-privacidade.png`  
**Resultado:** Aprovado.

---

## 4. Consulta aos dados do titular

Com a sessão autenticada, abrir `/accounts/privacidade/` e conferir nome de usuário, e-mail, data de cadastro, status do 2FA e consentimento vigente. O segredo TOTP e o hash da senha **não** devem aparecer.

**Evidências:** `33-consulta-dados.png`  
**Resultado:** Aprovado.

---

## 5. Exportação em JSON

Clicar em **Exportar meus dados**. O navegador deve baixar `verbum-dados.json` com os campos pessoais e o histórico de consentimento, sem senha e sem TOTP.

**Evidências:** `35-exportacao-json.png`  
**Resultado:** Aprovado.

---

## 6. Revogação do consentimento

No painel, revogar o consentimento. A tela deve mostrar status revogado, com data de revogação.

**Evidências:** `36-revogacao-consentimento.png`  
**Resultado:** Aprovado.

---

## 7. Exclusão da conta

Em `/accounts/privacidade/excluir/`, confirmar com e-mail e senha. Após a exclusão, tentar login com a mesma conta.

**Evidências:** `37-exclusao-confirmacao.png`, `38-exclusao-concluida.png`  
**Resultado:** Aprovado (login deixa de funcionar).

---

## 8. Tentativa de exclusão com senha errada

Informar senha incorreta na confirmação. A conta permanece e uma mensagem de erro é exibida.

**Evidências:** `37b-exclusao-senha-errada.png`  
**Resultado:** Aprovado.

---

## 9. Acesso às rotas do titular sem login

Abrir `/accounts/privacidade/` deslogado. O sistema deve redirecionar para o login.

**Evidências:** `33b-privacidade-sem-login.png`  
**Resultado:** Aprovado.

---

## 10. Logs sem segredo

Abrir `verbum.log` depois dos testes e conferir eventos `consent_granted`, `data_access`, `data_export`, `consent_revoked` e `account_deleted`. Não deve haver senha, token ou segredo TOTP.

**Evidências:** `39-log-lgpd.png`  
**Resultado:** Aprovado.

---

## Resumo

| Teste | Funcionalidade | Evidência | Resultado |
| --- | --- | --- | --- |
| 1 | Minimização / aceite obrigatório | `30-…` | Aprovado |
| 2 | Consentimento com data e versão | `31-…`, `34-…` | Aprovado |
| 3 | Transparência (política) | `32-…` | Aprovado |
| 4 | Consulta (art. 18, II) | `33-…` | Aprovado |
| 5 | Exportação (art. 18, V) | `35-…` | Aprovado |
| 6 | Revogação (art. 8º, §5º) | `36-…` | Aprovado |
| 7 | Exclusão (art. 18, VI) | `37-…`, `38-…` | Aprovado |
| 8 | Exclusão protegida por senha | `37b-…` | Aprovado |
| 9 | Rotas autenticadas | `33b-…` | Aprovado |
| 10 | Auditoria sem PII secreto | `39-…` | Aprovado |

## Observações

- Todos os requisitos 4.1–4.11 foram exercitados pela interface, conforme a rubrica.
- O JSON de exportação foi aberto em editor de texto para comprovar o conteúdo.
- Depois da exclusão, um novo cadastro com o mesmo e-mail deve ser possível (conta realmente removida).
