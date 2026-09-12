# Testes da Aplicação

## Projeto Integrador - Autenticação, Credenciais e Recuperação de Senha

Os testes foram realizados pelo front-end. Evidências em `docs/evidencias/`.

---

## 1. Verificação do ambiente

Comando: `python manage.py check`

Houve o aviso `models.W042` no `UserProfile`. A aplicação executa normalmente.

**Resultado: Aprovado com aviso.**

---

## 2. Inicialização

`python manage.py runserver` em `http://127.0.0.1:8000/`

**Resultado: Aprovado.**

---

## 3. Tela de login

Rota `/accounts/login/`. Campos de e-mail e senha, botão Entrar, cadastro e link “Esqueci minha senha”.

**Evidências:** `03-tela-login.png`, `11-login-esqueci-senha.png`

**Resultado: Aprovado.**

---

## 4. Cadastro válido

Mensagem: `Usuário cadastrado com sucesso!`

**Evidência:** `01-cadastro-sucesso.png`

**Resultado: Aprovado.**

---

## 5. Senhas diferentes

Mensagem: `As senhas não coincidem.`

**Evidência:** `02-senhas-diferentes.png`

**Resultado: Aprovado.**

---

## 6. E-mail inválido

Envio bloqueado sem `@`.

**Evidência:** `04-email-invalido.png`

**Resultado: Aprovado.**

---

## 7. Usuário já existente

Cadastro duplicado recusado.

**Evidência:** `08-usuario-ja-existente.png`

**Resultado: Aprovado.**

---

## 8. Validação de senha

Senha fraca rejeitada pelos validadores do Django.

**Evidência:** `10-teste_validacao_senha.png`

**Resultado: Aprovado.**

---

## 9. Login válido

Acesso ao painel após credenciais corretas.

**Evidência:** `05-painel-com-login.png`

**Resultado: Aprovado.**

---

## 10. Rota protegida

`/accounts/setup2fa/` sem login redireciona.

**Evidência:** `06-setup2fa-sem-login.png`

**Resultado: Aprovado.**

---

## 11. 2FA

Após a senha, a aplicação exigiu o código TOTP.

**Evidência:** `07-verifica-2fa.png`

**Resultado: Aprovado.**

---

## 12. Bloqueio por tentativas

Cinco senhas erradas geraram bloqueio de 5 minutos.

**Evidência:** `09-bloqueio-tentativas.png`

**Resultado: Aprovado.**

---

## 13. Sessão

Painel só com autenticação. Sessão de 30 minutos e cookie HttpOnly.

**Evidências:** `05-painel-com-login.png`, `06-setup2fa-sem-login.png`

**Resultado: Aprovado.**

---

## 14. Logout

Sessão encerrada e retorno ao login.

**Resultado: Aprovado.**

---

## 15. Recuperação — solicitação

Fluxo “Esqueci minha senha” até a tela de e-mail enviado.

**Evidências:** `11-login-esqueci-senha.png`, `12-form-recuperacao.png`, `13-email-enviado.png`

**Resultado: Aprovado.**

---

## 16. Link no console

O servidor exibiu o e-mail com o link de redefinição.

**Evidência:** `14-email-console.png`

**Resultado: Aprovado.**

---

## 17. Redefinição válida

Nova senha aceita e processo concluído.

**Evidências:** `15-nova-senha.png`, `16-reset-sucesso.png`

**Resultado: Aprovado.**

---

## 18. Token reutilizado

O mesmo link foi recusado depois do uso.

**Evidência:** `17-token-reutilizado.png`

**Resultado: Aprovado.**

---

## 19. Token inválido

Link adulterado recusado no front-end.

**Evidência:** `18-token-invalido.png`

**Resultado: Aprovado.**

---

## 20. Logs

Registros de solicitação, sucesso e falha, sem senha ou token.

**Evidências:** `19-log-solicitacao.png`, `20-log-sucesso.png`, `21-log-falha-token.png`

**Resultado: Aprovado.**

---

## 21. Criptografia do segredo TOTP

Após a configuração do 2FA, foi verificado no banco de dados que o campo `totp_secret` estava armazenado como um token Fernet, e não em texto puro.

A verificação foi realizada pelo shell do Django.

Resultado obtido:

`2FA ativo: True`

`Tamanho: 140`

`Fernet: True`

**Resultado: Aprovado.**

---

## 22. Descriptografia do segredo TOTP

Foi verificado que a aplicação consegue descriptografar o segredo TOTP armazenado no banco utilizando a chave criptográfica no ambiente.

A verificação foi realizada sem exibir o segredo original.

Resultado obtido:

`Descriptografia realizada: True`

`Tamanho do segredo: 32`

**Resultado: Aprovado.**

---

## 23. Fluxo completo do 2FA com segredo criptografado

Foi realizado o fluxo completo de autenticação utilizando 2FA após a implementação da criptografia do `totp_secret`.

O teste consistiu em:

1. Configuração do 2FA para o usuário.
2. Cadastro do segredo no aplicativo autenticador.
3. Logout.
4. Novo login com e-mail e senha.
5. Solicitação do código TOTP.
6. Validação do código.
7. Acesso ao painel.

O fluxo foi concluído com sucesso.

**Resultado: Aprovado.**

---

## 24. Resumo

| Teste | Funcionalidade | Evidência | Resultado |
| --- | --- | --- | --- |
| 01 | Ambiente Django | — | Aprovado com aviso |
| 02 | Inicialização | — | Aprovado |
| 03 | Tela de login | 03 e 11 | Aprovado |
| 04 | Cadastro | 01 | Aprovado |
| 05 | Confirmação de senha | 02 | Aprovado |
| 06 | E-mail inválido | 04 | Aprovado |
| 07 | Usuário existente | 08 | Aprovado |
| 08 | Política de senha | 10 | Aprovado |
| 09 | Login válido | 05 | Aprovado |
| 10 | Rota protegida | 06 | Aprovado |
| 11 | 2FA | 07 | Aprovado |
| 12 | Bloqueio | 09 | Aprovado |
| 13 | Sessão | 05 e 06 | Aprovado |
| 14 | Logout | — | Aprovado |
| 15 | Pedido de recuperação | 11, 12 e 13 | Aprovado |
| 16 | Link no console | 14 | Aprovado |
| 17 | Redefinição válida | 15 e 16 | Aprovado |
| 18 | Token reutilizado | 17 | Aprovado |
| 19 | Token inválido | 18 | Aprovado |
| 20 | Logs | 19, 20 e 21 | Aprovado |
| 21 | Criptografia do segredo TOTP | - | Aprovado |
| 22 | Descriptografia do segredo TOTP | - | Aprovado |
| 23 | Fluxo completo do 2FA criptografado | - | Aprovado |

---

## 25. Observações

Os testes foram feitos pelo front-end. O aviso `models.W042` não impede a avaliação funcional.
