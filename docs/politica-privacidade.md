# Política de Privacidade — Verbum

**Versão:** 1.0  
**Vigência:** setembro de 2026  
**Controlador:** equipe acadêmica do projeto Verbum (Sarah, Henrique, Gabriel)

Esta política explica quais dados pessoais o Verbum trata, para quê, com qual base legal e quais direitos o titular pode exercer.  
O texto é o mesmo exibido em `/accounts/politica-privacidade/`. A versão (`1.0`) é gravada no registro de consentimento.

---

## 1. Quem somos

O Verbum é uma plataforma web de aprendizagem de idiomas (vocabulário de alta frequência, gramática e expressões), desenvolvida como Projeto Integrador de Políticas de Segurança da Informação.

## 2. Quais dados coletamos

| Dado | Por que pedimos |
| --- | --- |
| Nome de usuário | Identificar sua conta |
| E-mail | Login, recuperação de senha e avisos da conta |
| Senha | Autenticação (armazenada só como hash com salt; nunca em texto claro) |
| Segredo de 2FA | Apenas se você ativar o segundo fator |
| Registros de consentimento | Comprovar finalidade, data e versão do aceite (art. 8º da LGPD) |
| Logs de segurança | Investigar falhas de autenticação e o exercício dos seus direitos |

Não pedimos CPF, telefone, endereço, foto, biometria nem dados sensíveis.

## 3. Finalidade

Prestação do serviço Verbum: criação e gestão da conta, autenticação, recuperação de senha e acompanhamento do aprendizado.

Não vendemos dados. Não fazemos publicidade comportamental. Não compartilhamos dados com terceiros nesta versão.

## 4. Bases legais (art. 7º da LGPD)

- consentimento do titular (inciso I), registrado no cadastro e no painel de privacidade;
- execução de contrato / prestação do serviço (inciso V);
- legítimo interesse para segurança da conta e logs de auditoria (inciso IX), sem prejudicar direitos e liberdades.

## 5. Como exercitar seus direitos (art. 18)

Com a conta autenticada, em **Privacidade**:

- consultar os dados que mantemos sobre você;
- exportar esses dados em JSON;
- revogar o consentimento;
- excluir a conta e os dados pessoais.

O atendimento é imediato pelo próprio sistema.

## 6. Retenção

Os dados da conta permanecem enquanto a conta existir. Ao excluir a conta, o usuário e o perfil são removidos do banco. Logs de segurança podem ser conservados sem senha, token ou segredo TOTP, para auditoria acadêmica e investigação de incidente.

## 7. Segurança

- hash e salt das senhas pelo Django;
- 2FA opcional (TOTP);
- sessão com expiração e cookie HttpOnly;
- bloqueio temporário após tentativas excessivas de login;
- token de recuperação com validade de 15 minutos e uso único;
- logs sem senha e sem token.

## 8. Alterações desta política

Se o texto mudar, a versão será incrementada (1.1, 1.2, …) e um novo aceite será pedido.

## 9. Contato

Dúvidas sobre esta política: canal acadêmico da equipe Verbum, informado no repositório do projeto.
