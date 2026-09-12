# Segurança

## Projeto Integrador - Autenticação, Credenciais e Recuperação de Senha

---

## 1. Proteção das senhas

Uso de `create_user()` e do sistema de hash do Django. A senha não é gravada em texto puro.

---

## 2. Validação das senhas

Validadores nativos do Django em `Verbum/settings.py`.

---

## 3. Tentativas de login

5 tentativas e bloqueio de 5 minutos.

---

## 4. 2FA

TOTP com `pyotp`. Campos `totp_secret` e `two_factor_enabled`.

---

## 5. Sessão e cookie

`@login_required`, sessão de 30 minutos e `SESSION_COOKIE_HTTPONLY = True`.

---

## 6. Logout

`logout()` do Django em `logout_view()`.

---

## 7. Recuperação de senha

Token do `PasswordResetTokenGenerator`, sem gravação no banco.

Expiração: 900 segundos. Uso único. Falha visível no front-end para token inválido.

Logs de evento em `verbum.log`, sem senha, token, uid ou e-mail.

---

## 8. Criptografia de dados sensíveis

O segredo utilizado pelo TOTP do 2FA é criptografado antes de ser armazenado no banco de dados.

A aplicação utiliza o Fernet, disponibilizado pela biblioteca `cryptography`, para proteger o campo `totp_secret` do modelo `UserProfile`.

O segredo é criptografado pela função `encrypt_totp_secret()` e descriptografado pela função `decrypt_totp_secret()`, ambas implementadas em `accounts/crypto.py`.

Dessa forma, o segredo TOTP não é armazenado em texto puro no banco de dados.


---

## 9. Algoritmo criptográfico

A proteção dos segredos TOTP utiliza o esquema Fernet da biblioteca `cryptography`.

O Fernet fornece confidencialidade e integridade aos dados criptografados, utilizando AES-128-CBC para a criptografia e HMAC-SHA256 para autenticação e verificação de integridade.

A aplicação utiliza a implementação padrão da biblioteca, evitando a implementação manual dos mecanismos criptográficos.

---

## 10. Proteção da chave criptográfica

A chave utilizada pelo Fernet é fornecida por meio da variável de ambiente `VERBUM_ENCRYPTION_KEY`.

A chave não é armazenada no código-fonte nem no banco de dados e não deve ser versionada no Git.

Durante o desenvolvimento, a configuração sensível é mantida fora dos arquivos versionados. Em ambiente de produção, a chave deverá ser configurada como segredo do ambiente de hospedagem.

A aplicação não gera uma nova chave a cada execução. A mesma chave deve ser preservada enquanto existirem dados criptografados que dependam dela.

---

## 11. Justificativa técnica

A criptografia dos segredos TOTP foi adotada para reduzir o impacto de um eventual acesso não autorizado ao banco de dados.

Mesmo que um terceiro obtenha acesso aos dados armazenados, o segredo TOTP não estará disponível diretamente em texto puro.

A utilização do Fernet fornece criptografia e autenticação dos dados por meio de uma biblioteca especializada, reduzindo os riscos associados à implementação manual de algoritmos criptográficos.

A chave criptográfica é mantida separada dos dados protegidos e fora do código-fonte, sendo fornecida à aplicação por variável de ambiente.

A perda da chave impossibilita a descriptografia dos dados protegidos por ela. Por esse motivo, em ambiente de produção, a chave deverá possuir armazenamento seguro, controle de acesso e procedimento adequado de backup e rotação.

---

## 12. Resumo

| Mecanismo | Implementação |
| --- | --- |
| Validação de senha | Validadores do Django |
| Hash da senha | Sistema de autenticação do Django |
| Tentativas | 5 |
| Bloqueio | 5 minutos |
| 2FA | TOTP / `pyotp` |
| Sessão | 30 minutos + HttpOnly |
| Recuperação | Token temporário + logs |
| Expiração do token | 900 segundos |
| Criptografia em repouso | Fernet para segredos TOTP |
| Algoritmo criptográfico | Fernet / AES-128-CBC + HMAC-SHA256 |
| Proteção da chave | Variável de ambiente |


---

## 9. Dados pessoais e LGPD

- Cadastro pede só usuário, e-mail e senha (minimização).
- Consentimento gravado com finalidade, data e versão da política (`ConsentRecord`).
- Titular consulta, exporta (JSON) e exclui a conta pelo front-end.
- Exclusão exige e-mail + senha atual.
- Logs de consentimento, acesso, exportação e exclusão **não** gravam senha, token ou segredo TOTP.
- Política pública versionada em `/accounts/politica-privacidade/`.

Documentação: `docs/lgpd.md`.
