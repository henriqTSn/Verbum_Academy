# Verbum — Requisitos Funcionais e Não Funcionais

**Projeto:** Verbum — Plataforma de aprendizagem de idiomas  
**Versão do documento:** 1.1  
**Release de referência:** v1.1.0 (Autenticação e Gestão de Credenciais)  
**Stack:** Python, Django (MVT), SQLite, HTML/CSS/JavaScript  
**Equipe:** Sarah, Henrique, Gabriel  

Este documento descreve o que o sistema deve fazer (requisitos funcionais) e as restrições de qualidade, segurança e conformidade (requisitos não funcionais).  
Ele complementa o checklist de evidências da etapa atual (`docs/requisitos.md`) e o enunciado do Projeto Integrador de Políticas de Segurança da Informação.

---

## 1. Visão do produto

O **Verbum** é uma plataforma web de aprendizagem de idiomas baseada em:

- vocabulário de alta frequência;
- gramática;
- chunks e expressões frequentes;
- acompanhamento individual do progresso.

Nesta etapa do Projeto Integrador, o núcleo entregue é o **sistema seguro de autenticação e gestão de credenciais**, em conformidade com a LGPD (Lei nº 13.709/2018). As funcionalidades de estudo (vocabulário, expressões, histórico) estão no escopo do produto, mas ainda não implementadas.

### Objetivo desta entrega

Disponibilizar cadastro, login, 2FA, controle de sessão e proteção de credenciais, com documentação técnica, testes e evidências, de forma que as próximas etapas (recuperação de senha, LGPD operacional, auditoria e conteúdo pedagógico) possam ser acrescentadas sem redesenhar a base.

---

## 2. Atores

| Ator | Descrição |
|---|---|
| Visitante | Pessoa sem conta. Pode acessar telas públicas (login e cadastro). |
| Estudante | Usuário autenticado. Destinatário das funcionalidades de aprendizado e dos direitos de titular. |
| Titular de dados | O próprio estudante, no exercício dos direitos da LGPD. |
| Sistema | Processos automáticos (validação, bloqueio, expiração de sessão, geração de TOTP). |
| Administrador (futuro) | Gestão de conteúdo e auditoria. Fora do escopo da v1.1.0. |

---

## 3. Convenções

Cada requisito possui:

- **ID** estável (RF-xx ou RNF-xx);
- **Prioridade:** Must / Should / Could (MoSCoW);
- **Status:** Implementado | Parcial | Planejado;
- **Origem:** produto, PI (Projeto Integrador) ou ambos.

Prioridade **Must** nesta fase = exigido pelo enunciado do PI ou já entregue na v1.1.0.

---

## 4. Requisitos funcionais

### 4.1 Conta e autenticação

#### RF-01 — Cadastro de usuário
**Prioridade:** Must · **Status:** Implementado · **Origem:** Produto + PI

O sistema deve permitir que o visitante crie uma conta informando nome de usuário, e-mail, senha e confirmação de senha.

**Critérios de aceite**

- O cadastro só é concluído se senha e confirmação forem iguais.
- O sistema rejeita nome de usuário já existente, com mensagem clara.
- O usuário é criado com `create_user()` do Django (senha nunca persistida em texto claro).
- Em sucesso, o sistema informa que o cadastro foi realizado.

**Implementação atual:** `accounts/views.py` → `register()`  
**Evidências:** `01-cadastro-sucesso.png`, `02-senhas-diferentes.png`, `08-usuario-ja-existente.png`

#### RF-02 — Validação de senha no cadastro
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 1.1–1.4

A senha deve passar pelos validadores configurados no Django:

- similaridade com atributos do usuário;
- comprimento mínimo;
- senhas comuns;
- senha somente numérica.

**Evidência:** `10-teste_validacao_senha.png`

#### RF-03 — Login com e-mail e senha
**Prioridade:** Must · **Status:** Implementado · **Origem:** Produto + PI

O estudante deve autenticar-se com e-mail e senha.

**Critérios de aceite**

- A busca pelo e-mail não diferencia maiúsculas de minúsculas.
- Credenciais inválidas geram mensagem genérica (“e-mail ou senha inválidos”), sem revelar qual campo falhou.
- Formato de e-mail inválido é rejeitado na interface.

**Implementação:** `accounts/views.py` → `login_view()`  
**Evidências:** `03-tela-login.png`, `04-email-invalido.png`, `05-painel-com-login.png`

#### RF-04 — Proteção contra tentativas excessivas
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 1.11

Após **5** tentativas de senha incorreta, a conta deve ser bloqueada por **5 minutos**.

**Critérios de aceite**

- Durante o bloqueio, novas tentativas são recusadas com mensagem de bloqueio temporário.
- Após o período, o contador é reiniciado.
- O controle usa `failed_login_attempts` e `locked_until` em `UserProfile`.

**Evidência:** `09-bloqueio-tentativas.png`

#### RF-05 — Autenticação em dois fatores (TOTP)
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 1.5–1.6

O estudante deve poder configurar 2FA baseado em TOTP (`pyotp`) e, quando ativo, o login só se conclui após o código válido.

**Critérios de aceite**

- Configuração do 2FA exige sessão autenticada.
- Campos `totp_secret` e `two_factor_enabled` no `UserProfile`.
- Senha correta com 2FA ativo redireciona para a tela de verificação.
- Código inválido impede o acesso.

**Implementação:** `setup_2fa()`, `verify_2fa()`  
**Evidências:** `06-setup2fa-sem-login.png`, `07-verifica-2fa.png`

#### RF-06 — Sessão autenticada
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 1.9

Páginas restritas (painel, setup de 2FA) só são acessíveis com sessão válida.

**Critérios de aceite**

- Rotas protegidas usam `@login_required`.
- Duração da sessão: 30 minutos.
- `SESSION_SAVE_EVERY_REQUEST = True` (renovação enquanto houver uso).
- Cookie de sessão `HttpOnly`.

#### RF-07 — Logout
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 1.10

O estudante deve encerrar a sessão. Após o logout, o painel deixa de ser acessível e o usuário retorna à tela de login.

**Implementação:** `logout_view()`

#### RF-08 — Recuperação e alteração de senha
**Prioridade:** Must (PI) · **Status:** Planejado · **Origem:** PI seção 2

O sistema deve permitir redefinir senha por token temporário.

**Critérios de aceite (próxima etapa)**

- Token criptograficamente seguro, com expiração.
- Token invalidado após o uso.
- Token expirado ou reutilizado falha de forma segura.
- Solicitação, sucesso e falha registrados em log de auditoria.

#### RF-09 — Gerenciamento de perfil
**Prioridade:** Should · **Status:** Planejado · **Origem:** Produto

O estudante autenticado deve consultar e atualizar dados básicos do perfil (nome de exibição, e-mail, preferências), respeitando RF-21 a RF-24.

---

### 4.2 Aprendizagem (escopo do produto)

Estes requisitos descrevem o produto Verbum. Não fazem parte da pontuação obrigatória da etapa de credenciais, mas devem constar no documento de visão.

#### RF-10 — Seleção do idioma estudado
**Prioridade:** Must (produto) · **Status:** Planejado

O estudante deve escolher o idioma-alvo. Na primeira versão pedagógica, o idioma disponível é **inglês**.

#### RF-11 — Vocabulário de alta frequência
**Prioridade:** Must (produto) · **Status:** Planejado

O sistema deve apresentar listas de vocabulário ordenadas por frequência de uso, com significado, exemplo e marcação de progresso (visto / em revisão / dominado).

#### RF-12 — Chunks e expressões frequentes
**Prioridade:** Must (produto) · **Status:** Planejado

O sistema deve disponibilitar expressões e chunks recorrentes, separados do vocabulário isolado, para estudo contextual.

#### RF-13 — Gramática estruturada
**Prioridade:** Should · **Status:** Planejado

O sistema deve organizar tópicos gramaticais associados ao nível e ao vocabulário já estudado.

#### RF-14 — Histórico de estudos
**Prioridade:** Must (produto) · **Status:** Planejado

O estudante deve visualizar o histórico de sessões, itens estudados e evolução ao longo do tempo.

#### RF-15 — Painel do estudante
**Prioridade:** Should · **Status:** Parcial (tela existe após login)

Após autenticar-se, o estudante acessa um painel. Na v1.1.0 o painel comprova a sessão; nas próximas versões deve resumir idioma, progresso e atalhos de estudo.

---

### 4.3 Privacidade e direitos do titular (LGPD)

#### RF-20 — Inventário e finalidade dos dados
**Prioridade:** Must · **Status:** Planejado (documentação) / Parcial (coleta atual mínima)

O sistema deve listar cada dado pessoal coletado e associá-lo a uma finalidade.

**Inventário mínimo da v1.1.0**

| Dado | Finalidade | Base |
|---|---|---|
| Nome de usuário | Identificação da conta | Execução do serviço |
| E-mail | Login e comunicações da conta | Execução do serviço |
| Hash da senha + salt | Autenticação | Execução do serviço / segurança |
| Segredo TOTP (quando habilitado) | Segundo fator | Segurança da conta |
| Contadores de bloqueio | Proteção contra força bruta | Legítimo interesse / segurança |
| Dados de sessão | Manter o acesso autenticado | Execução do serviço |

Não devem ser coletados dados desnecessários ao serviço (minimização).

#### RF-21 — Consentimento
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 4.4–4.7

O titular deve registrar consentimento explícito, associado à finalidade, com data e versão do texto. Deve poder revogar o consentimento.

#### RF-22 — Consulta aos dados
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 4.8

O titular autenticado deve consultar os dados pessoais armazenados sobre si.

#### RF-23 — Exportação dos dados
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 4.9

O titular deve exportar seus dados em formato estruturado e de uso comum (ex.: JSON).

#### RF-24 — Exclusão de conta e dados
**Prioridade:** Must · **Status:** Implementado · **Origem:** PI 4.10

O titular deve solicitar a exclusão da conta e dos dados pessoais, observando eventuais retenções legais mínimas de logs de segurança.

#### RF-25 — Auditoria de eventos de segurança
**Prioridade:** Must · **Status:** Planejado · **Origem:** PI 5.1–5.4

O sistema deve registrar, no mínimo:

- tentativas de autenticação (sucesso e falha);
- ativação/verificação de 2FA;
- bloqueio por tentativas;
- logout;
- (futuro) solicitação e conclusão de recuperação de senha;
- (futuro) consulta, exportação e exclusão de dados.

Os logs não devem ser alteráveis pela aplicação de uso comum e devem permitir análise posterior.

---

## 5. Requisitos não funcionais

### 5.1 Segurança (RNF-S)

#### RNF-S01 — Armazenamento de senha
**Prioridade:** Must · **Status:** Implementado (hasher padrão do Django) / Planejado (Argon2 explícito)

Senhas devem ser persistidas apenas como hash com salt único por usuário. Algoritmos aceitos pelo PI: Argon2, bcrypt ou PBKDF2.

**Estado atual:** o Django `create_user()` aplica hash + salt do hasher configurado (PBKDF2 por padrão).  
**Próximo passo documentado no README:** migrar/explicitar Argon2 e justificar parâmetros de custo (iterações, memória, paralelismo).

#### RNF-S02 — Autenticação multifator
**Prioridade:** Must · **Status:** Implementado

O segundo fator é TOTP, validado somente após a autenticação primária bem-sucedida.

#### RNF-S03 — Política de sessão
**Prioridade:** Must · **Status:** Implementado

- Expiração: 30 minutos de inatividade controlada pela configuração de sessão.
- Invalidação imediata no logout.
- Cookie `HttpOnly`.
- Em produção: cookie `Secure` e `SameSite` adequados (planejado com HTTPS).

#### RNF-S04 — Resistência a força bruta
**Prioridade:** Must · **Status:** Implementado

Limite de 5 tentativas e bloqueio de 5 minutos por conta. Mensagens de erro não devem permitir enumeração trivial de usuários além do que o cadastro já expõe.

#### RNF-S05 — Comunicação em trânsito
**Prioridade:** Must (produção) · **Status:** Planejado · **Origem:** PI 3.1–3.3

Em ambiente de produção a aplicação deve ser servida exclusivamente via TLS/HTTPS. Conexões HTTP devem ser redirecionadas ou bloqueadas. O ambiente local de desenvolvimento (http://127.0.0.1:8000/) é aceito para testes da etapa atual.

#### RNF-S06 — Dados sensíveis em repouso
**Prioridade:** Must · **Status:** Parcial · **Origem:** PI 3.4–3.6

- Senhas: hash + salt (atendido).
- Segredo TOTP e demais segredos: devem ser protegidos (criptografia em repouso ou cofre de chaves) na evolução do projeto.
- Chaves e `SECRET_KEY` do Django não devem ser versionadas. Usar variáveis de ambiente.

#### RNF-S07 — Proteção das rotas
**Prioridade:** Must · **Status:** Implementado

Recursos autenticados exigem sessão. Tentativa de acesso direto redireciona ao login.

#### RNF-S08 — Integridade dos logs
**Prioridade:** Must · **Status:** Planejado

Logs de segurança devem ter proteção contra alteração casual (permissões de arquivo, append-only ou destino separado do banco da aplicação).

#### RNF-S09 — Cabeçalhos e práticas web
**Prioridade:** Should · **Status:** Planejado

Em produção: CSRF do Django habilitado (padrão), `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, e headers básicos (`X-Content-Type-Options`, `X-Frame-Options`).

---

### 5.2 Privacidade e conformidade (RNF-P)

#### RNF-P01 — Conformidade com a LGPD
**Prioridade:** Must · **Status:** Parcial (princípios adotados; telas de titular planejadas)

O tratamento deve observar finalidade, adequação, necessidade, transparência, segurança e prevenção. Direitos de acesso, exportação, eliminação e revogação de consentimento são RF-21 a RF-24.

#### RNF-P02 — Minimização
**Prioridade:** Must · **Status:** Parcial

Coletar apenas username, e-mail e credenciais necessárias à autenticação nesta etapa. Não solicitar CPF, telefone, foto ou dados sensíveis sem finalidade explícita.

#### RNF-P03 — Transparência
**Prioridade:** Should · **Status:** Planejado

Textos de política de privacidade e de consentimento versionados, acessíveis antes do cadastro.

---

### 5.3 Usabilidade (RNF-U)

#### RNF-U01 — Feedback imediato
**Prioridade:** Must · **Status:** Implementado (fluxos de auth)

Mensagens de sucesso e erro visíveis na interface (senhas diferentes, usuário existente, bloqueio, cadastro ok).

#### RNF-U02 — Interface responsiva
**Prioridade:** Should · **Status:** Parcial

Telas de login/cadastro utilizam HTML/CSS/Bootstrap e devem permanecer utilizáveis em desktop e largura de tablet/celular.

#### RNF-U03 — Idioma da interface
**Prioridade:** Should · **Status:** Implementado nas telas atuais

A interface da etapa atual está em português brasileiro. O conteúdo pedagógico futuro (inglês) é o objeto de estudo, não o idioma da UI.

#### RNF-U04 — Tempo para concluir login
**Prioridade:** Could · **Status:** Não medido

Fluxo e-mail + senha (sem 2FA) deve ser concluído em poucos segundos em ambiente local, sem etapas ocultas.

---

### 5.4 Confiabilidade e disponibilidade (RNF-C)

#### RNF-C01 — Inicialização verificável
**Prioridade:** Must · **Status:** Implementado

`python manage.py check` e `runserver` devem subir a aplicação. Aviso `models.W042` (PK automática do `UserProfile`) é conhecido e não bloqueia a execução; deve ser corrigido em refatoração.

#### RNF-C02 — Persistência
**Prioridade:** Must · **Status:** Implementado

Contas, perfil e flags de 2FA/bloqueio persistem no SQLite após restart do processo.

#### RNF-C03 — Recuperação de falha de autenticação
**Prioridade:** Must · **Status:** Implementado

Falha de senha, 2FA ou bloqueio não derruba o processo; o usuário permanece na interface com mensagem.

---

### 5.5 Desempenho (RNF-D)

#### RNF-D01 — Ambiente acadêmico
**Prioridade:** Should · **Status:** Adequado ao escopo

SQLite e servidor de desenvolvimento Django são aceitáveis para a disciplina. Não há meta de usuários concorrentes nesta fase.

#### RNF-D02 — Custo do hash
**Prioridade:** Must (quando Argon2/parametrização forem formalizados)

Parâmetros de hash devem ser altos o suficiente para retardar força bruta e baixos o suficiente para o cadastro/login permanecerem interativos em máquina comum de laboratório. A escolha deve ser justificada em `docs/seguranca.md`.

---

### 5.6 Manutenibilidade e documentação (RNF-M)

#### RNF-M01 — Arquitetura MVT
**Prioridade:** Must · **Status:** Implementado

Separação em `accounts/`, `homePage/`, `templates/`, `Verbum/settings.py`.

#### RNF-M02 — Documentação viva
**Prioridade:** Must · **Status:** Em evolução

A pasta `docs/` deve conter, no mínimo:

| Arquivo | Papel |
|---|---|
| `requisitos-funcionais-e-nao-funcionais.md` | Este documento (RF/RNF e status) |
| `requisitos.md` | Checklist + evidências da etapa de autenticação |
| `implementacao.md` | Como o código realiza cada fluxo |
| `seguranca.md` | Mecanismos e justificativas |
| `testes.md` | Casos de teste e resultados |
| PDFs do PI | Enunciado e rubrica |

#### RNF-M03 — Rastreabilidade código ↔ requisito
**Prioridade:** Should · **Status:** Atendido para auth

Cada RF implementado aponta view/model/settings e evidência de tela.

#### RNF-M04 — Reprodução do ambiente
**Prioridade:** Must · **Status:** Implementado

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Aplicação em `http://127.0.0.1:8000/`.

---

### 5.7 Portabilidade e ambiente (RNF-E)

#### RNF-E01 — Multiplataforma de desenvolvimento
**Prioridade:** Should · **Status:** Implementado

O projeto deve rodar em ambientes com Python 3 e dependências do `requirements.txt` (Windows, Linux ou macOS).

#### RNF-E02 — Segredos fora do repositório
**Prioridade:** Must (produção) · **Status:** Planejado

`SECRET_KEY`, chaves de criptografia e credenciais de e-mail (recuperação de senha) em variáveis de ambiente, nunca commitadas.

---

## 6. Fora de escopo (v1.1.0)

- Aplicativo nativo mobile.
- Login social (Google, GitHub etc.).
- Múltiplos idiomas de estudo além do inglês (produto futuro).
- Correção automática por IA / speech recognition.
- Painel administrativo completo.
- Implantação pública com domínio e certificado (pode ser evidência futura de TLS).

---

## 7. Rastreabilidade com a rubrica do Projeto Integrador

| Item da rubrica | Requisitos | Situação na v1.1.0 |
|---|---|---|
| 1.1–1.4 Hash + salt | RNF-S01, RF-01 | Atendido via hasher Django; explicitar Argon2 + custo |
| 1.5–1.6 2FA | RF-05, RNF-S02 | Implementado |
| 1.7–1.8 Fluxo e evidências | RNF-M02, `testes.md` | Documentado |
| 1.9–1.10 Sessão e logout | RF-06, RF-07, RNF-S03 | Implementado |
| 1.11 Força bruta | RF-04, RNF-S04 | Implementado |
| 2.x Recuperação de senha | RF-08 | Planejado |
| 3.x TLS e crypto em repouso | RNF-S05, RNF-S06 | Planejado / parcial |
| 4.x LGPD | RF-20–RF-24, RNF-P01–P03 | Inventário iniciado; telas planejadas |
| 5.x Auditoria | RF-25, RNF-S08 | Planejado |
| 6.x Documentação técnico-científica | este doc + `implementacao.md` + `seguranca.md` | Em evolução |

---

## 8. Regras de negócio resumidas

1. Uma conta = um `User` Django + um `UserProfile`.
2. Login identifica o usuário pelo e-mail (case-insensitive).
3. 2FA é opcional até o estudante configurá-lo; depois torna-se obrigatório no login.
4. Bloqueio por tentativas é temporário e automático.
5. Senha nunca é exibida, logada ou persistida em claro.
6. Dados pedagógicos futuros pertencem ao titular e entram no pacote de exportação/exclusão.

---

## 9. Como manter este documento

- Ao implementar um RF/RNF, mude só o **Status** e acrescente evidência/arquivo.
- Não apague IDs. Se um requisito for abandonado, marque **Cancelado** e justifique.
- O checklist com prints continua em `docs/requisitos.md` (é a prova da etapa, não a especificação do produto).
- Decisões de segurança (algoritmo de hash, tempo de sessão, política de token) devem ser espelhadas em `docs/seguranca.md`.
