import asyncio
from celery import Celery
from celery.schedules import crontab

from config import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    REDIS_PASSWORD,
    TIMEZONE
)

# ==============================================
# CONFIGURAÇÃO DO CELERY
# ==============================================
redis_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}" if REDIS_PASSWORD else f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

app = Celery(
    "larizinhastore",
    broker=redis_url,
    backend=redis_url
)

app.conf.timezone = TIMEZONE
app.conf.enable_utc = True

# ==============================================
# AGENDAMENTO DE TAREFAS PERIÓDICAS (BEAT)
# ==============================================
app.conf.beat_schedule = {
    # Verifica e expira PIX vencidos a cada minuto
    "check-expired-pix-every-minute": {
        "task": "check_expired_pix",
        "schedule": crontab(minute="*"),
    },
    # Consulta gateway para confirmar pagamentos a cada 30 segundos
    "check-pending-pix-every-30-seconds": {
        "task": "check_pending_pix",
        "schedule": 30.0,
    },
    # Envia alertas de reabastecimento a cada 5 minutos
    "send-alerts-every-5-minutes": {
        "task": "send_alerts",
        "schedule": crontab(minute="*/5"),
    },
    # Atualiza rankings a cada 10 minutos
    "update-rankings-every-10-minutes": {
        "task": "update_rankings",
        "schedule": crontab(minute="*/10"),
    },
}

# ==============================================
# TAREFAS
# ==============================================

@app.task(name="check_expired_pix")
def check_expired_pix():
    """
    Marca como expirados os pagamentos PIX cuja data de expiração passou.
    """
    async def _run():
        from services.payment_gateway import expire_pending_payments
        await expire_pending_payments()
    asyncio.run(_run())


@app.task(name="check_pending_pix")
def check_pending_pix():
    """
    Consulta o gateway para verificar pagamentos PIX pendentes.
    """
    async def _run():
        from services.payment_gateway import verify_pending_payments
        await verify_pending_payments()
    asyncio.run(_run())


@app.task(name="send_alerts")
def send_alerts():
    """
    Envia alertas de reabastecimento para usuários com alertas ativos.
    """
    async def _run():
        from services.alert_service import send_stock_alerts
        await send_stock_alerts()
    asyncio.run(_run())


@app.task(name="update_rankings")
def update_rankings():
    """
    Recalcula os rankings de produtos, usuários e recargas.
    """
    async def _run():
        from services.ranking_service import refresh_rankings
        await refresh_rankings()
    asyncio.run(_run())


@app.task(name="broadcast_message")
def broadcast_message(user_ids: list, text: str):
    """
    Envia mensagem em massa para uma lista de IDs de usuários.
    """
    async def _run():
        from services.notifier import send_broadcast
        await send_broadcast(user_ids, text)
    asyncio.run(_run())
