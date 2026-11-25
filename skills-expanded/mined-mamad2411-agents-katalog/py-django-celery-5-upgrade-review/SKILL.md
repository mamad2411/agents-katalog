---
name: py-django-celery-5-upgrade-review
description: Use this skill when reviewing upgrades to Celery 5.x, especially Celery 4-to-5 migration, current 5.6 compatibility, Python support, broker changes, and worker behavior.
---

# py-django-celery-5-upgrade-review

## Purpose

Use this skill when reviewing upgrades to Celery 5.x, especially Celery 4-to-5 migration, current 5.6 compatibility, Python support, broker changes, and worker behavior.

## Use When

- The task involves Django and Celery 5.x.
- The project includes `celery.py`, `CELERY_` settings, `tasks.py`, workers, beat, brokers, or result backends.

## Do Not Use When

- The task is only about Django request/response behavior without Celery.
- The task is only about Redis, RabbitMQ, or SQS administration unrelated to Celery.
- The project targets an incompatible Celery major version without explicit migration work.

## Process

1. Identify the Django settings module and project layout.
2. Inspect relevant settings, Celery app setup, task definitions, and command history.
3. Run included read-only scanners when available and relevant.
4. Apply this skill's workflow and checklist.
5. Prefer small, safe changes with explicit validation steps.
6. Escalate destructive queue, worker, or broker operations for confirmation.
