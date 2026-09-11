# Trechos para colar nos arquivos que já existem

Não substituam os arquivos inteiros. Só acrescentem.

---

## `docs/README.md` — incluir na tabela “Leia nesta ordem”

```markdown
| [lgpd.md](lgpd.md) | Etapa 3: inventário, consentimento e direitos do titular (itens 4.1 a 4.11) |
| [politica-privacidade.md](politica-privacidade.md) | Texto versionado da política (v1.0) |
| [lgpd-testes.md](lgpd-testes.md) | Casos de teste do front-end da etapa 3 |
| [requisitos-lgpd.md](requisitos-lgpd.md) | Checklist 4.1–4.11 + prints |
```

Trocar o parágrafo de status:

```markdown
A etapa atual cobre autenticação, recuperação de senha e conformidade com a LGPD
(itens 4.1 a 4.11 do checklist). HTTPS de produção permanece na seção 3 da rubrica.
```

---

## `README.md` da raiz — bloco “Privacidade e LGPD”

```markdown
## Privacidade e LGPD

Implementado nesta entrega (Lei nº 13.709/2018, itens 4.1 a 4.11):

- Inventário de dados pessoais com finalidade e base legal
- Minimização (cadastro sem CPF, telefone ou dado sensível)
- Consentimento explícito, com finalidade, data e versão da política
- Revogação do consentimento
- Consulta dos dados do titular
- Exportação em JSON
- Exclusão da conta e dos dados pessoais

Documentação: `docs/lgpd.md`  
Política versionada: `docs/politica-privacidade.md`
```

Atualizar “Entrega Atual” para a release nova (ex.: `v1.3.0`) e o link do Kanban.

---

## `docs/requisitos-funcionais-e-nao-funcionais.md`

Mudar o status de RF-21 a RF-24 e RNF-P01/P03 de **Planejado** para **Implementado**.
Apontar as rotas `/accounts/privacidade/`, exportar e excluir.

---

## Resumo científico (200–300 palavras) — item 7.5 da rubrica

Usar ou adaptar:

O crescimento dos serviços digitais ampliou o tratamento de dados pessoais e tornou a
autenticação insegura uma das principais causas de incidente. Este trabalho apresenta o
Verbum, plataforma acadêmica de aprendizagem de idiomas cujo núcleo de segurança
combina gestão de credenciais e conformidade com a Lei nº 13.709/2018 (LGPD).

A solução foi implementada em Django (arquitetura MVT) com SQLite. As senhas são
persistidas apenas como hash com salt, com validadores de complexidade. O login admite
segundo fator TOTP, sessão com expiração de 30 minutos e cookie HttpOnly, além de
bloqueio temporário após tentativas excessivas. A recuperação de senha usa token HMAC
de uso único e validade de 15 minutos, com registro de solicitação, sucesso e falha sem
expor o segredo.

A conformidade com a LGPD apoia-se em minimização (coleta restrita a usuário, e-mail e
credenciais), finalidade declarada e consentimento explícito versionado (art. 8º). O
titular consulta seus dados, exporta um JSON estruturado e exclui a conta pelo
front-end, com auditoria desses eventos. Não há tratamento de dados sensíveis do art. 11
nem compartilhamento com terceiros nesta versão.

O conjunto atende aos itens 4.1 a 4.11 da rubrica do Projeto Integrador e materializa
os princípios de finalidade, necessidade, transparência, segurança e responsabilização
previstos no art. 6º da LGPD.
