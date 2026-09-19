# Função única para gravar eventos de auditoria.
# Centraliza o log para login, bloqueio, logout e 2FA.

from .models import AuditLog
import logging

logger = logging.getLogger("verbum.audit")


def write_audit_log(
    event,
    request=None,
    user=None,
    email="",
    success=False,
    message="",
):
    ip_address = None
    if request is not None:
        ip_address = request.META.get("REMOTE_ADDR")
        if not email:
            posted_email = request.POST.get("email", "")
            email = posted_email

    if user is not None and not email:
        email = getattr(user, "email", "") or ""

    AuditLog.objects.create(
        event=event,
        user=user,
        email=email,
        ip_address=ip_address,
        success=success,
        message=message,
    )

    # Também escreve no arquivo de log da aplicação, sem senha ou token.
    logger.info(
        "%s success=%s email=%s ip=%s message=%s",
        event,
        success,
        email,
        ip_address,
        message,
    )
