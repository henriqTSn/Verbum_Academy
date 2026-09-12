# Conformidade com a LGPD

## Projeto Integrador — Etapa 3

**Projeto:** Verbum — Plataforma de aprendizagem de idiomas  
**Lei de referência:** Lei nº 13.709/2018 (LGPD)  
**Itens da rubrica:** 4.1 a 4.11  
**Release prevista:** v1.3.0  

Este documento descreve o inventário de dados pessoais, as bases legais, o registro de consentimento e os direitos do titular implementados no Verbum.  
Os testes desta etapa são feitos pelo front-end. As capturas ficam em `docs/evidencias/`.

---

## 1. Objetivo

Atender aos princípios da LGPD (finalidade, adequação, necessidade, transparência, segurança e prevenção) e aos direitos do titular previstos no art. 18:

- confirmação e acesso (consulta);
- portabilidade (exportação em JSON);
- eliminação (exclusão da conta e dos dados pessoais);
- revogação do consentimento.

O tratamento de dados no Verbum existe para prestar o serviço de conta e aprendizagem. Não há venda de dados, perfilamento comercial nem compartilhamento com terceiros nesta versão.

---

## 2. Onde está no código

| Elemento | Local |
| --- | --- |
| Modelo de perfil e consentimento | `accounts/models.py` (`UserProfile`, `ConsentRecord`) |
| Consulta, exportação, exclusão e consentimento | `accounts/views.py` |
| Rotas do titular | `accounts/urls.py` |
| Política de privacidade (texto versionado) | `templates/accounts/politica_privacidade.html` e `docs/politica-privacidade.md` |
| Cadastro com aceite | `templates/register.html` |
| Painel de privacidade | `templates/accounts/privacidade.html` |
| Logs de direitos do titular | logger `accounts` em `verbum.log` (`Verbum/settings.py`) |

Rotas:

- `/accounts/register/` — cadastro com consentimento explícito
- `/accounts/privacidade/` — consulta dos dados e gestão do consentimento
- `/accounts/privacidade/exportar/` — download JSON
- `/accounts/privacidade/excluir/` — exclusão da conta
- `/accounts/privacidade/consentimento/` — revogar ou renovar consentimento
- `/accounts/politica-privacidade/` — texto público da política (versão vigente)

---

## 3. Papéis no tratamento (art. 5º)

| Papel | Quem |
| --- | --- |
| Titular | Estudante cadastrado |
| Controlador | Equipe Verbum (Sarah, Henrique, Gabriel) — projeto acadêmico |
| Operador | Não há operador externo nesta versão (hospedagem local / ambiente de avaliação) |
| Encarregado (DPO) | Contato acadêmico do grupo: ver política de privacidade |

Não há transferência internacional de dados nesta entrega. O banco é SQLite local.

---

## 4. Inventário de dados pessoais (itens 4.1 e 4.2)

Cada dado coletado possui finalidade e base legal. Nada fora desta tabela é pedido no cadastro.

| Dado | Origem | Finalidade | Base legal (art. 7º) | Retenção |
| --- | --- | --- | --- | --- |
| Nome de usuário (`User.username`) | Cadastro | Identificar a conta e o perfil de estudo | Execução de contrato / prestação do serviço (inciso V) + consentimento (inciso I) | Até exclusão da conta |
| E-mail (`User.email`) | Cadastro | Login, recuperação de senha e avisos da conta | Incisos V e I | Até exclusão da conta |
| Hash da senha + salt (`User.password`) | Cadastro / redefinição | Autenticar o titular | Inciso V + segurança da conta | Até exclusão da conta |
| Segredo TOTP (`UserProfile.totp_secret`) | Setup 2FA (opcional) | Segundo fator de autenticação | Legítimo interesse / segurança (inciso IX) + inciso V | Até desativar 2FA ou excluir a conta |
| Flag 2FA (`two_factor_enabled`) | Setup 2FA | Controlar o fluxo de login | Segurança da conta | Até exclusão |
| Contador de falhas e `locked_until` | Login | Bloquear força bruta | Legítimo interesse / segurança (inciso IX) | Rotacionado a cada bloqueio; apagado com a conta |
| Dados de sessão (cookie HttpOnly) | Login | Manter o acesso autenticado | Inciso V | 30 minutos de inatividade |
| Consentimento (`ConsentRecord`) | Cadastro / painel | Provar finalidade, data e versão do aceite | Art. 8º (prova do consentimento) | Até exclusão; logs de auditoria podem permanecer sem PII |
| Logs de segurança (sem senha/token) | Autenticação e direitos do titular | Auditoria e investigação de incidente | Legítimo interesse / segurança (inciso IX) e art. 46 | Prazo acadêmico da disciplina; sem senha, token ou segredo TOTP |

Dados **não coletados** (minimização — item 4.3):

- CPF, RG, CNH, passaporte
- telefone, endereço, CEP, geolocalização
- data de nascimento, foto, biometria
- dados sensíveis do art. 11 (saúde, religião, opinião política, etc.)
- dados de menores com tratamento específico (o serviço não é dirigido a crianças)

A senha em texto claro nunca é persistida. O token de recuperação não é gravado em log.

---

## 5. Minimização (item 4.3)

O formulário de cadastro pede apenas:

1. nome de usuário;
2. e-mail;
3. senha e confirmação;
4. aceite da política de privacidade (obrigatório para criar a conta).

Justificativa: sem esses quatro elementos não é possível criar uma conta autenticável, comunicar a recuperação de senha e registrar o consentimento exigido pelo art. 8º. Qualquer campo adicional seria desnecessário nesta etapa.

---

## 6. Consentimento (itens 4.4 a 4.7)

### 6.1 Registro explícito (4.4)

No cadastro há um checkbox **desmarcado por padrão**. O texto ao lado do checkbox informa a finalidade e aponta para a política versionada. Sem o aceite, o cadastro é recusado.

O registro é gravado em `ConsentRecord`:

| Campo | Função |
| --- | --- |
| `user` | Titular |
| `purpose` | Finalidade declarada |
| `granted` | `True` no aceite; `False` na revogação |
| `granted_at` | Data e hora do aceite |
| `revoked_at` | Data e hora da revogação (se houver) |
| `policy_version` | Versão do texto aceito (ex.: `1.0`) |
| `source` | Origem (`register` ou `privacidade`) |

### 6.2 Finalidade associada (4.5)

Texto gravado no aceite vigente (`POLICY_VERSION = "1.0"`):

> Prestação do serviço Verbum: criação e gestão da conta, autenticação, recuperação de senha e acompanhamento do aprendizado. Os dados não são vendidos nem compartilhados com terceiros.

### 6.3 Revogação (4.6)

No painel `/accounts/privacidade/` o titular pode revogar o consentimento. A revogação:

- marca `granted = False` e preenche `revoked_at`;
- registra o evento em log;
- informa que, sem o consentimento essencial ao serviço, a conta será encerrada;
- oferece a exclusão imediata da conta.

O consentimento pode ser renovado na mesma tela, gerando um novo registro (histórico append-only: o registro antigo não é apagado).

### 6.4 Data e versão (4.7)

Cada registro guarda `granted_at` (timezone-aware) e `policy_version`. Se a política mudar, a versão incrementa e o titular precisa aceitar o novo texto.

---

## 7. Direitos do titular (itens 4.8 a 4.10)

Todas as telas abaixo exigem sessão autenticada (`@login_required`), salvo a política pública.

### 7.1 Consulta (4.8) — art. 18, II

`/accounts/privacidade/` mostra, em texto claro (exceto segredos):

- nome de usuário e e-mail;
- data de cadastro (`date_joined`);
- se o 2FA está ativo (não exibe o segredo TOTP);
- consentimento vigente (finalidade, data, versão, status);
- histórico resumido de consentimentos.

### 7.2 Exportação (4.9) — art. 18, V

`/accounts/privacidade/exportar/` gera um arquivo `verbum-dados.json` com `Content-Disposition: attachment`.

O JSON contém os dados do titular em formato estruturado e de uso comum. **Não inclui**:

- hash da senha;
- salt;
- segredo TOTP;
- tokens de recuperação;
- cookie de sessão.

### 7.3 Exclusão (4.10) — art. 18, VI

`/accounts/privacidade/excluir/` pede confirmação (e-mail digitado de novo + senha atual).

Efeitos:

1. log de `account_deleted` **sem** gravar a senha;
2. exclusão do `User` (CASCADE remove `UserProfile` e `ConsentRecord`);
3. invalidação da sessão (`logout`);
4. redirecionamento para a tela de login com mensagem de conta excluída.

Retenção residual: linhas de `verbum.log` anteriores à exclusão podem permanecer para auditoria de segurança, sem a senha e sem o token. Não há backup externo nesta versão acadêmica.

---

## 8. Fluxo de atendimento aos direitos (item 4.11)

```
Visitante
    │
    ▼
Cadastro ── checkbox desmarcado ── recusa se não aceitar
    │ aceite + versão 1.0
    ▼
ConsentRecord (granted=True, data, finalidade, versão)
    │
    ▼
Estudante autenticado
    │
    ├── Consultar  → GET /accounts/privacidade/
    ├── Exportar   → GET /accounts/privacidade/exportar/  → JSON
    ├── Revogar    → POST /accounts/privacidade/consentimento/
    └── Excluir    → POST /accounts/privacidade/excluir/  → User.delete() + logout
```

Prazo: o atendimento é **imediato** e self-service (não depende de ticket). Isso atende o art. 18 com margem em relação ao prazo legal de 15 dias.

---

## 9. Auditoria dos direitos do titular

| Evento | Nível | Mensagem (sem segredo) |
| --- | --- | --- |
| Aceite no cadastro | INFO | `consent_granted user_id=… version=1.0 source=register` |
| Consulta | INFO | `data_access user_id=…` |
| Exportação | INFO | `data_export user_id=…` |
| Revogação | INFO | `consent_revoked user_id=… version=1.0` |
| Renovação | INFO | `consent_granted user_id=… version=1.0 source=privacidade` |
| Exclusão | WARNING | `account_deleted user_id=…` |
| Tentativa de exclusão com senha errada | WARNING | `account_delete_failed user_id=… reason=bad_password` |

Os logs usam o handler de arquivo definido em `Verbum/settings.py`. A aplicação comum não oferece tela para editar `verbum.log`.

---

## 10. Princípios da LGPD aplicados

| Princípio (art. 6º) | Como o Verbum aplica |
| --- | --- |
| Finalidade | Cada campo do inventário tem uso declarado |
| Adequação | Dados usados só para conta, autenticação e estudo |
| Necessidade (minimização) | Cadastro sem CPF, telefone, foto ou dado sensível |
| Livre acesso | Tela de consulta autenticada |
| Qualidade dos dados | Titular vê e pode excluir a conta; e-mail é o identificador de login |
| Transparência | Política pública versionada + texto no checkbox |
| Segurança | Hash+salt, 2FA, sessão HttpOnly, token de reset com expiração |
| Prevenção | Bloqueio de força bruta, logs sem segredo, CSRF do Django |
| Não discriminação | Nenhum tratamento de dado sensível do art. 11 |
| Responsabilização | Este documento, o código comentado e os logs |

---

## 11. Checklist da rubrica (seção 4)

| Nº | Requisito | Status | Comprovação |
| --- | --- | --- | --- |
| 4.1 | Listagem completa dos dados pessoais coletados | Implementado | Seção 4 deste arquivo + tela de consulta |
| 4.2 | Associação de cada dado a uma finalidade | Implementado | Tabela da seção 4 |
| 4.3 | Evidência de minimização de dados | Implementado | Formulário de cadastro + seção 5 |
| 4.4 | Registro explícito de consentimento | Implementado | Checkbox + `ConsentRecord` |
| 4.5 | Consentimento associado à finalidade | Implementado | Campo `purpose` |
| 4.6 | Possibilidade de revogação do consentimento | Implementado | Painel de privacidade |
| 4.7 | Registro de data e versão do consentimento | Implementado | `granted_at` + `policy_version` |
| 4.8 | Funcionalidade de consulta aos dados do titular | Implementado | `/accounts/privacidade/` |
| 4.9 | Funcionalidade de exportação dos dados | Implementado | JSON em `/accounts/privacidade/exportar/` |
| 4.10 | Funcionalidade de exclusão dos dados pessoais | Implementado | `/accounts/privacidade/excluir/` |
| 4.11 | Fluxo de atendimento aos direitos documentado | Implementado | Seção 8 + `docs/lgpd-testes.md` |

---

## 12. Evidências

Capturas esperadas em `docs/evidencias/` (nomes sugeridos):

| Arquivo | O que mostra |
| --- | --- |
| `30-cadastro-sem-consentimento.png` | Cadastro recusado sem checkbox |
| `31-cadastro-com-consentimento.png` | Cadastro aceito com política versão 1.0 |
| `32-politica-privacidade.png` | Texto público da política |
| `33-consulta-dados.png` | Painel com os dados do titular |
| `34-consentimento-data-versao.png` | Finalidade, data e versão na tela |
| `35-exportacao-json.png` | Download / conteúdo do JSON |
| `36-revogacao-consentimento.png` | Consentimento revogado |
| `37-exclusao-confirmacao.png` | Tela de confirmação da exclusão |
| `38-exclusao-concluida.png` | Conta removida; login da mesma conta falha |
| `39-log-lgpd.png` | Trecho de `verbum.log` com eventos da etapa |

O roteiro passo a passo está em `docs/lgpd-testes.md`.

---

## 13. Limitações desta entrega (transparência acadêmica)

- Ambiente de avaliação em `DEBUG = True` e SQLite. HTTPS de produção é item da seção 3 da rubrica (criptografia), tratado em documento próprio.
- Não há operador contratado nem transferência internacional.
- Não há módulo de incidentes com notificação à ANPD (fora do checklist 4.1–4.11).
- Logs de arquivo local não são append-only em hardware dedicado; a proteção é a ausência de interface de edição e o fato de a aplicação não reescrever o arquivo.

---

## 14. Referências

- BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD).
- ANPD. Guia orientativo de boas práticas. Tratamento de dados pessoais.
- ANPD. Guia de segurança da informação para agentes de tratamento de pequeno porte.
- Django Software Foundation. *User authentication* e *Password management*. Documentação oficial.
- ISO/IEC 27001 / 27701 — gestão de segurança da informação e privacidade (fundamentação da análise de riscos do projeto).
