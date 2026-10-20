---
name: task-queue-celery
description: |
  Celery task queue patterns for background jobs, scheduled tasks, and async processing.
  Apply when implementing email sending, payment processing, file generation, scheduled jobs,
  or any operation that should not block the HTTP response.
---

# Task Queue — Celery Patterns

## Celery Configuration
```python
# config/celery.py
from celery import Celery
from celery.schedules import crontab

app = Celery('myapp')
app.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_CONFIG = {
    'broker_url': settings.REDIS_URL,
    'result_backend': settings.REDIS_URL,
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json'],
    'timezone': 'Asia/Tashkent',
    'task_track_started': True,
    'task_acks_late': True,           # ACK after completion, not on receipt
    'worker_prefetch_multiplier': 1,  # One task at a time per worker slot
    'task_reject_on_worker_lost': True,

    # Routing to different queues
    'task_routes': {
        'apps.notifications.tasks.*': {'queue': 'notifications'},
        'apps.payments.tasks.*': {'queue': 'payments'},
        'apps.reports.tasks.*': {'queue': 'reports'},
    },

    # Scheduled tasks
    'beat_schedule': {
        'daily-sales-report': {
            'task': 'apps.reports.tasks.generate_daily_sales_report',
            'schedule': crontab(hour=23, minute=0),
        },
        'cleanup-expired-sessions': {
            'task': 'apps.users.tasks.cleanup_expired_sessions',
            'schedule': crontab(hour=3, minute=0),
        },
    }
}
```

## Task Patterns
```python
from celery import shared_task, Task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# Basic task with retry
@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_order_confirmation(self, order_id: str):
    try:
        order = Order.objects.select_related('user').get(id=order_id)
        send_email(
            to=order.user.email,
            subject=f"Order #{order.id[:8]} confirmed",
            template='emails/order_confirmation.html',
            context={'order': order},
        )
        logger.info("order_confirmation_sent", order_id=order_id, user_id=order.user_id)
    except Order.DoesNotExist:
        logger.error("order_not_found", order_id=order_id)
        # Don't retry — order won't appear later
    except EmailError as exc:
        logger.warning("email_send_failed", order_id=order_id, attempt=self.request.retries)
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 30)

# Long-running task with progress tracking
@shared_task(bind=True)
def generate_report(self, report_type: str, date_range: dict):
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': 100})
    
    data = collect_report_data(report_type, date_range)
    self.update_state(state='PROGRESS', meta={'current': 50, 'total': 100})
    
    file_url = export_to_excel(data)
    self.update_state(state='PROGRESS', meta={'current': 90, 'total': 100})
    
    notify_report_ready.delay(report_type, file_url)
    return {'url': file_url, 'total': len(data)}

# Chain tasks
from celery import chain
result = chain(
    validate_payment.s(payment_id),
    process_order.s(),
    send_confirmation.s(),
    notify_warehouse.s(),
)()
```

## Docker Compose for Celery
```yaml
celery-worker:
  build: { context: ./backend }
  command: celery -A config worker -Q default,notifications -l info -c 4
  env_file: .env
  depends_on: [redis, db]

celery-payments:
  build: { context: ./backend }
  command: celery -A config worker -Q payments -l info -c 2
  env_file: .env

celery-beat:
  build: { context: ./backend }
  command: celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
  env_file: .env

flower:
  image: mher/flower
  command: celery --broker=${REDIS_URL} flower --port=5555
  ports: ["5555:5555"]
```
