# Como implementar a etapa 3 no código

A documentação em `lgpd.md` descreve o sistema **depois** destas alterações.
Sem o código e sem os prints do front-end a rubrica aplica −50% (projeto não testável) e −50% (documentação sem lastro).

Façam **um commit por bloco**, com mensagem clara (ex.: `feat: modelo ConsentRecord`, `feat: painel LGPD`). Isso evita o desconto de commits não temporais.

---

## 1. Modelo — acrescentar em `accounts/models.py`

```python
from django.utils import timezone


class ConsentRecord(models.Model):
    """Registro append-only de consentimento (art. 8º da LGPD)."""

    PURPOSE_DEFAULT = (
        "Prestação do serviço Verbum: criação e gestão da conta, "
        "autenticação, recuperação de senha e acompanhamento do aprendizado."
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="consents",
    )
    purpose = models.TextField()
    granted = models.BooleanField(default=True)
    granted_at = models.DateTimeField(default=timezone.now)
    revoked_at = models.DateTimeField(null=True, blank=True)
    policy_version = models.CharField(max_length=16)
    source = models.CharField(max_length=32, default="register")

    class Meta:
        ordering = ["-granted_at"]

    def __str__(self):
        status = "concedido" if self.granted else "revogado"
        return f"{self.user_id} {status} v{self.policy_version}"
```

No `UserProfile`, o `on_delete=models.CASCADE` já remove o perfil quando o `User` é excluído.

Rodar:

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

---

## 2. Views — acrescentar em `accounts/views.py`

Importe no topo (além do que já existe):

```python
import json
import logging

from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import UserProfile, ConsentRecord

logger = logging.getLogger("accounts")

POLICY_VERSION = "1.0"
POLICY_PURPOSE = ConsentRecord.PURPOSE_DEFAULT
```

Cadastro: **só criar o usuário se `request.POST.get("consent")` vier marcado**. Depois do `create_user` / `UserProfile`:

```python
ConsentRecord.objects.create(
    user=user,
    purpose=POLICY_PURPOSE,
    granted=True,
    policy_version=POLICY_VERSION,
    source="register",
)
logger.info("consent_granted user_id=%s version=%s source=register", user.id, POLICY_VERSION)
```

Se o checkbox não vier:

```python
messages.error(request, "É necessário aceitar a Política de Privacidade para criar a conta.")
```

Views novas:

```python
def politica_privacidade(request):
    return render(request, "accounts/politica_privacidade.html", {
        "policy_version": POLICY_VERSION,
    })


def _dados_titular(user):
    """Monta o dicionário exportável. Sem senha e sem TOTP."""
    consents = [
        {
            "purpose": c.purpose,
            "granted": c.granted,
            "granted_at": c.granted_at.isoformat(),
            "revoked_at": c.revoked_at.isoformat() if c.revoked_at else None,
            "policy_version": c.policy_version,
            "source": c.source,
        }
        for c in user.consents.all()
    ]
    profile = getattr(user, "userprofile", None)
    return {
        "username": user.username,
        "email": user.email,
        "date_joined": user.date_joined.isoformat(),
        "last_login": user.last_login.isoformat() if user.last_login else None,
        "two_factor_enabled": bool(profile and profile.two_factor_enabled),
        "consents": consents,
    }


@login_required
def privacidade(request):
    logger.info("data_access user_id=%s", request.user.id)
    vigente = request.user.consents.filter(granted=True).first()
    return render(request, "accounts/privacidade.html", {
        "dados": _dados_titular(request.user),
        "consentimento_vigente": vigente,
        "historico": request.user.consents.all(),
        "policy_version": POLICY_VERSION,
    })


@login_required
def exportar_dados(request):
    logger.info("data_export user_id=%s", request.user.id)
    payload = json.dumps(_dados_titular(request.user), ensure_ascii=False, indent=2)
    response = HttpResponse(payload, content_type="application/json; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="verbum-dados.json"'
    return response


@login_required
@require_http_methods(["GET", "POST"])
def revogar_consentimento(request):
    if request.method == "POST":
        acao = request.POST.get("acao")
        if acao == "revogar":
            vigente = request.user.consents.filter(granted=True).first()
            if vigente:
                vigente.granted = False
                vigente.revoked_at = timezone.now()
                vigente.save(update_fields=["granted", "revoked_at"])
                logger.info(
                    "consent_revoked user_id=%s version=%s",
                    request.user.id,
                    vigente.policy_version,
                )
                messages.warning(
                    request,
                    "Consentimento revogado. Sem este aceite o serviço de conta não pode continuar. "
                    "Você pode excluir a conta agora.",
                )
        elif acao == "renovar":
            ConsentRecord.objects.create(
                user=request.user,
                purpose=POLICY_PURPOSE,
                granted=True,
                policy_version=POLICY_VERSION,
                source="privacidade",
            )
            logger.info(
                "consent_granted user_id=%s version=%s source=privacidade",
                request.user.id,
                POLICY_VERSION,
            )
            messages.success(request, "Consentimento registrado novamente.")
        return redirect("privacidade")
    return redirect("privacidade")


@login_required
@require_http_methods(["GET", "POST"])
def excluir_conta(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        senha = request.POST.get("password") or ""
        if email.lower() != request.user.email.lower():
            messages.error(request, "O e-mail informado não confere.")
            return render(request, "accounts/excluir_conta.html")
        if not authenticate(username=request.user.username, password=senha):
            logger.warning("account_delete_failed user_id=%s reason=bad_password", request.user.id)
            messages.error(request, "Senha incorreta. A conta não foi excluída.")
            return render(request, "accounts/excluir_conta.html")

        user = request.user
        logger.warning("account_deleted user_id=%s", user.id)
        logout(request)
        user.delete()
        messages.success(request, "Conta e dados pessoais excluídos.")
        return redirect("login")
    return render(request, "accounts/excluir_conta.html")
```

Observação: o login do Verbum usa e-mail. Se `authenticate` no projeto de vocês exige o username interno, mantenham o mesmo padrão já usado em `login_view`.

---

## 3. Rotas — `accounts/urls.py`

```python
path("politica-privacidade/", views.politica_privacidade, name="politica_privacidade"),
path("privacidade/", views.privacidade, name="privacidade"),
path("privacidade/exportar/", views.exportar_dados, name="exportar_dados"),
path("privacidade/consentimento/", views.revogar_consentimento, name="revogar_consentimento"),
path("privacidade/excluir/", views.excluir_conta, name="excluir_conta"),
```

---

## 4. Templates

### 4.1 Checkbox em `templates/register.html`

Colocar **antes** do botão de enviar, desmarcado:

```html
<p>
  <label>
    <input type="checkbox" name="consent" value="1">
    Li e aceito a
    <a href="{% url 'politica_privacidade' %}" target="_blank" rel="noopener">
      Política de Privacidade v1.0
    </a>
    para a finalidade de prestação do serviço Verbum
    (conta, autenticação e aprendizado).
  </label>
</p>
```

### 4.2 Link no painel (`templates/painel.html`)

```html
<p><a href="{% url 'privacidade' %}">Privacidade e meus dados (LGPD)</a></p>
```

### 4.3 `templates/accounts/politica_privacidade.html`

Usar o texto de `docs/politica-privacidade.md` (versão 1.0 visível no topo).

### 4.4 `templates/accounts/privacidade.html`

Mostrar `dados.username`, `dados.email`, `dados.date_joined`, `dados.two_factor_enabled`,
finalidade / data / versão do consentimento vigente, histórico,
botões: Exportar, Revogar, Renovar, Excluir conta.

### 4.5 `templates/accounts/excluir_conta.html`

Formulário POST com CSRF, campo e-mail, campo senha e texto:

> Esta ação apaga a conta e os dados pessoais. Não pode ser desfeita.

---

## 5. Comentários obrigatórios

A rubrica pede código comentado, principalmente em segurança e credenciais.
Comentem:

- por que o JSON **não** exporta `password` nem `totp_secret`;
- por que a exclusão exige senha (evita CSRF + sessão roubada sem o segredo);
- por que o checkbox nasce desmarcado (consentimento livre, art. 8º);
- por que o log não grava token/senha.

---

## 6. Release e Kanban

1. Commitar código + `docs/lgpd.md` + prints.
2. Criar tag `v1.3.0` (ou o número que o grupo usar) com notas: *Etapa 3 — Conformidade com a LGPD (itens 4.1 a 4.11)*.
3. Atualizar o quadro Kanban (há desconto de 20% se não existir).
4. Entregar o link do repositório **e** o link da release na pasta acadêmica, individualmente.

---

## 7. O que não inventar na hora da defesa

- Não digam que usam Argon2 se o Django padrão do projeto ainda estiver em PBKDF2. Confiram `PASSWORD_HASHERS` em `settings.py` e documentem o hasher real.
- Não digam que há HTTPS de produção se o teste for em `http://127.0.0.1:8000/`. HTTPS é a seção 3 da rubrica, não a 4.
- Consentimento essencial + execução de contrato podem coexistir. Se perguntarem “por que consentimento se já há contrato?”, respondam: *a rubrica exige o registro do art. 8º; usamos o aceite para a finalidade declarada e a execução do serviço para a operação da conta.*
