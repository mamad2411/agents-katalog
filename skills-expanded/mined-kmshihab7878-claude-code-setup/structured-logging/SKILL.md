---
name: structured-logging
description: Structured logging patterns with loguru and structlog for Python services, JSON output, correlation IDs, and Loki/Grafana integration
triggers:
  - logging
  - structured logging
  - loguru
  - structlog
  - log format
  - observability logs
---

# Structured Logging

Production logging patterns for Python services. Replace stdlib logging with structured, machine-parseable output that integrates with Grafana Loki.

## Setup: loguru + structlog

```python
# src/coremind/core/logging.py
import structlog
from loguru import logger
import sys
import json

def setup_logging(json_output: bool = True, level: str = "INFO"):
    """Configure structured logging for CoreMind services."""

    # Remove default loguru handler
    logger.remove()

    if json_output:
        # JSON format for production (Loki/ELK ingest)
        logger.add(
            sys.stdout,
            format="{message}",
            level=level,
            serialize=True,
        )
    else:
        # Human-readable for development
        logger.add(
            sys.stdout,
            format="<green>{time:HH:mm:ss}</green> | <level>{level:<8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=level,
            colorize=True,
        )

    # Configure structlog to use loguru as backend
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer() if json_output
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
```

## Correlation IDs

```python
# Middleware for request correlation
import uuid
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

class CorrelationMiddleware:
    async def __call__(self, request, call_next):
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        correlation_id.set(req_id)
        structlog.contextvars.bind_contextvars(correlation_id=req_id)

        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response
```

## Log Levels Guide

- **DEBUG**: Variable values, function entry/exit, SQL queries
- **INFO**: Request handled, task started/completed, state transitions
- **WARNING**: Retry attempts, deprecation usage, approaching limits
- **ERROR**: Failed operations that can be retried or degraded
- **CRITICAL**: Data loss risk, security incidents, unrecoverable failures

## Anti-Patterns

- Never log sensitive data (tokens, passwords, PII)
- Never use f-strings in log messages (use structured fields)
- Never log inside tight loops (use sampling)
- Never suppress exceptions silently

```python
# BAD
logger.info(f"User {user.email} logged in with token {token}")

# GOOD
logger.info("user_login", user_id=user.id, auth_method="oauth")
```
