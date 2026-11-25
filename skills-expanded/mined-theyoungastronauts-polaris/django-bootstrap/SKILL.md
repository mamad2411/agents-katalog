---
name: django-bootstrap
description: "Scaffold a Django/DRF project (Docker, split settings, JWT auth, Celery, S3) at a chosen blueprint tier."
disable-model-invocation: true
---

# Django Bootstrap

On-demand command for scaffolding a new Django/DRF project with Docker, PostgreSQL, split settings, and standard conventions. Supports three blueprint tiers for right-sized infrastructure.

## Before You Start

Ask the user for these values (provide defaults where shown):

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{blueprint}` | Blueprint tier: `minimal`, `standard`, or `full` | `standard` |
| `{service_name}` | Top-level directory name | `my_service` |
| `{project-name}` | Docker Compose project name (kebab-case) | `my-service` |
| `{db_name}` | Postgres database name (snake_case) | `my_service` |
| `{host_port}` | Host port for Django (default: `8000`) | `8002` |
| `{project_prefix}` | Short cache key prefix | `myserv` |
| `{heroku-app-name}` | Heroku app name (`full` only, if deploying) | `my-service-prod` |

### Blueprint Tiers

| Tier | Name | Includes | Use when |
|------|------|----------|----------|
| 1 | **minimal** | Django + DRF + Postgres + Docker. LocMem cache, session auth, AllowAny, local file storage, console logging. No Redis, Celery, JWT, custom User, S3, Sentry, email, discord. | Simple APIs, prototypes, no user accounts |
| 2 | **standard** | Minimal + Redis cache + custom User (`access` app) + JWT auth + Sentry. No Celery, S3, email, discord. | Most production apps with auth |
| 3 | **full** | Standard + Celery/Beat + S3/R2 + email + discord + Heroku deployment. | Background tasks, file uploads, notifications |

> **Only generate files and sections marked for your blueprint tier.** Sections are tagged `[ALL]`, `[STANDARD+]`, or `[FULL]`. Generate `[ALL]` always, `[STANDARD+]` for standard and full, `[FULL]` only for full.

> **MANDATORY: This project runs entirely in Docker.**
> Every Docker file below (Dockerfile.dev, docker-compose.yml, Makefile, docker/ scripts) MUST be generated.
> The Makefile is the sole interface — never run `python manage.py` directly on the host.

## Bootstrapping Steps

1. Create `{service_name}/` directory and all subdirectories
2. Generate all files from templates below, replacing placeholders (respecting blueprint tier tags)
3. `cd {service_name} && make build && make up`
4. Standard/full only: `make makemigrations` first — the shipped `access/` app has only `migrations/__init__.py`, and `migrate` fails with `Dependency on app with no migrations: access` without it
5. `make migrate && make createsuperuser`
6. Verify admin at `http://localhost:{host_port}/admin/`

---

## Directory Structure

### `[MINIMAL]` Directory Structure

```
{service_name}/
├── project/
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── environment.py
│   │   ├── security.py
│   │   ├── apps.py
│   │   ├── database.py
│   │   ├── cache.py
│   │   ├── auth.py
│   │   ├── cors.py
│   │   ├── storage.py
│   │   └── logging.py
│   ├── utils/
│   │   └── __init__.py
│   └── templates/
├── docker/
│   ├── entrypoint.sh
│   └── wait-for-it.sh
├── docker-compose.yml
├── Dockerfile.dev
├── Makefile
├── Procfile
├── manage.py
├── requirements.txt
├── .python-version
├── .env.example
├── .gitignore
└── .coveragerc
```

### `[STANDARD]` Directory Structure — adds `access/` app and `sentry.py`

```
{service_name}/
├── project/
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── environment.py
│   │   ├── security.py
│   │   ├── apps.py
│   │   ├── database.py
│   │   ├── cache.py
│   │   ├── auth.py
│   │   ├── cors.py
│   │   ├── storage.py
│   │   ├── logging.py
│   │   └── sentry.py
│   ├── utils/
│   │   └── __init__.py
│   └── templates/
├── access/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── migrations/
│   │   └── __init__.py
│   └── urls.py
├── docker/
│   ├── entrypoint.sh
│   └── wait-for-it.sh
├── docker-compose.yml
├── Dockerfile.dev
├── Makefile
├── Procfile
├── manage.py
├── requirements.txt
├── .python-version
├── .env.example
├── .gitignore
└── .coveragerc
```

### `[FULL]` Directory Structure — adds `worker.py`, `services/`, cloud settings

```
{service_name}/
├── project/
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   ├── worker.py
│   ├── wsgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── environment.py
│   │   ├── security.py
│   │   ├── apps.py
│   │   ├── database.py
│   │   ├── cache.py
│   │   ├── auth.py
│   │   ├── cors.py
│   │   ├── aws.py
│   │   ├── storage.py
│   │   ├── worker.py
│   │   ├── email.py
│   │   ├── logging.py
│   │   └── sentry.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── storage.py
│   │   ├── email.py
│   │   └── discord.py
│   ├── utils/
│   │   └── __init__.py
│   └── templates/
├── access/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── migrations/
│   │   └── __init__.py
│   └── urls.py
├── docker/
│   ├── entrypoint.sh
│   └── wait-for-it.sh
├── docker-compose.yml
├── Dockerfile.dev
├── Makefile
├── Procfile
├── manage.py
├── requirements.txt
├── .python-version
├── .env.example
├── .gitignore
└── .coveragerc
```

---

## File Templates

### manage.py `[ALL]`

```python
#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
```

### project/\_\_init\_\_.py — varies by tier

**`[MINIMAL]` and `[STANDARD]`:** empty file

```python
```

**`[FULL]`:**

```python
from .worker import app as celery_app

__all__ = ("celery_app",)
```

### project/models.py `[ALL]`

```python
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class TypeValidator:
    """Validator to ensure a field value is of a specific type."""

    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __call__(self, value):
        if not isinstance(value, self.expected_type):
            raise ValidationError(
                f"Value must be of type {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )

    def __eq__(self, other):
        return (
            isinstance(other, TypeValidator)
            and self.expected_type == other.expected_type
        )


class AbstractModel(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        validators=[TypeValidator(dict)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_field(cls, field_name):
        return cls._meta.get_field(field_name)

    def silent_save(self, *fields):
        """Update specific fields without triggering updated_at or signals."""
        cls = type(self)
        if hasattr(cls, "_default_manager"):
            cls._default_manager.filter(pk=self.pk).update(
                **{field: getattr(self, field) for field in fields}
            )

    class Meta:
        abstract = True
        ordering = ["-created_at"]
```

### project/worker.py `[FULL]`

```python
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Beat schedule — add periodic tasks here
app.conf.beat_schedule = {}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
```

### project/wsgi.py `[ALL]`

```python
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_wsgi_application()
```

### project/urls.py `[ALL]`

```python
from django.contrib import admin
from django.urls import include, path

# [STANDARD+] auth app (access) — omit this import and the auth include for the
# minimal (no-auth) tier
from access.urls import urlpatterns as auth_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    # API v1
    path("api/v1/auth/", include((auth_urlpatterns, "auth"))),  # [STANDARD+]
]
```

---

## Settings

### project/settings/\_\_init\_\_.py — varies by tier

**`[MINIMAL]`** (9 imports):

```python
# Environment and core settings
from .environment import *  # noqa: F401, F403

# Security, middleware, templates
from .security import *  # noqa: F401, F403

# Installed apps
from .apps import *  # noqa: F401, F403

# Database
from .database import *  # noqa: F401, F403

# Cache
from .cache import *  # noqa: F401, F403

# Authentication and REST framework
from .auth import *  # noqa: F401, F403

# CORS
from .cors import *  # noqa: F401, F403

# Storage
from .storage import *  # noqa: F401, F403

# Logging
from .logging import *  # noqa: F401, F403
```

**`[STANDARD]`** (10 imports — adds sentry):

```python
# Environment and core settings
from .environment import *  # noqa: F401, F403

# Security, middleware, templates
from .security import *  # noqa: F401, F403

# Installed apps
from .apps import *  # noqa: F401, F403

# Database
from .database import *  # noqa: F401, F403

# Cache
from .cache import *  # noqa: F401, F403

# Authentication and REST framework
from .auth import *  # noqa: F401, F403

# CORS
from .cors import *  # noqa: F401, F403

# Storage
from .storage import *  # noqa: F401, F403

# Logging
from .logging import *  # noqa: F401, F403

# Sentry (Error Tracking)
from .sentry import *  # noqa: F401, F403
```

**`[FULL]`** (13 imports — adds aws, worker, email, sentry):

```python
# Environment and core settings
from .environment import *  # noqa: F401, F403

# Security, middleware, templates
from .security import *  # noqa: F401, F403

# Installed apps
from .apps import *  # noqa: F401, F403

# Database
from .database import *  # noqa: F401, F403

# Cache
from .cache import *  # noqa: F401, F403

# Authentication and REST framework
from .auth import *  # noqa: F401, F403

# CORS
from .cors import *  # noqa: F401, F403

# AWS/S3/R2
from .aws import *  # noqa: F401, F403

# Storage
from .storage import *  # noqa: F401, F403

# Celery worker
from .worker import *  # noqa: F401, F403

# Email
from .email import *  # noqa: F401, F403

# Logging
from .logging import *  # noqa: F401, F403

# Sentry (Error Tracking)
from .sentry import *  # noqa: F401, F403
```

### project/settings/environment.py `[ALL]`

```python
import os
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV = environ.Env(
    DEBUG=(bool, False),
)

env_file = BASE_DIR / ".env"
if env_file.exists():
    ENV.read_env(str(env_file))

DEBUG = ENV.bool("DEBUG", default=False)
ENVIRONMENT = ENV.str("ENVIRONMENT", default="development")
VERSION = ENV.str("VERSION", default="0.1.0")

FRONTEND_BASE_URL = ENV.str("FRONTEND_BASE_URL", default="http://localhost:3000")
```

### project/settings/security.py `[ALL]`

```python
from .environment import BASE_DIR, ENV, DEBUG

SECRET_KEY = ENV.str("SECRET_KEY", default="django-insecure-change-me-in-production")

ALLOWED_HOSTS = ENV.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

CSRF_TRUSTED_ORIGINS = ENV.list("CSRF_TRUSTED_ORIGINS", default=["http://localhost:{host_port}"])

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "project" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Production hardening
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

### project/settings/apps.py — varies by tier

**`[MINIMAL]`:**

```python
DJANGO_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "admin_auto_filters",
]

LOCAL_APPS = [
    "project",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Required for django-admin-interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
```

Note: `admin_interface` and `colorfield` must come before `django.contrib.admin`.

**`[STANDARD+]`** (adds simplejwt, token_blacklist, access):

```python
DJANGO_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "admin_auto_filters",
    "storages",
]

LOCAL_APPS = [
    "project",
    "access",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Required for django-admin-interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
```

Note: `admin_interface` and `colorfield` must come before `django.contrib.admin`.

### project/settings/database.py `[ALL]`

```python
import dj_database_url

from .environment import ENV, DEBUG

DATABASE_URL = ENV.str(
    "DATABASE_URL",
    default="postgres://postgres:postgres@db:5432/{db_name}"
)

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
        ssl_require=not DEBUG,
    )
}
```

### project/settings/cache.py — varies by tier

**`[MINIMAL]`** (LocMemCache, database sessions):

```python
CACHE_TIMEOUT_SHORT = 5
CACHE_TIMEOUT_MEDIUM = 30
CACHE_TIMEOUT_DEFAULT = 60
CACHE_TIMEOUT_LONG = 300

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "KEY_PREFIX": "{project_prefix}",
        "VERSION": 1,
        "TIMEOUT": CACHE_TIMEOUT_DEFAULT,
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.db"
```

**`[STANDARD+]`** (Redis, cache sessions):

```python
import ssl

from .environment import ENV

REDIS_URL = ENV.str("REDIS_URL", default="redis://redis:6379/0")

CACHE_TIMEOUT_SHORT = 5
CACHE_TIMEOUT_MEDIUM = 30
CACHE_TIMEOUT_DEFAULT = 60
CACHE_TIMEOUT_LONG = 300

REDIS_SSL = REDIS_URL.startswith("rediss://")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
        "KEY_PREFIX": "{project_prefix}",
        "VERSION": 1,
        "TIMEOUT": CACHE_TIMEOUT_DEFAULT,
        # Heroku Redis (and some managed providers) serve rediss:// with a
        # self-signed cert, so verification is disabled here. This trades away
        # MITM protection and is only acceptable on a trusted private network —
        # prefer ssl.CERT_REQUIRED with the provider's CA bundle where supported.
        **({"OPTIONS": {"ssl_cert_reqs": ssl.CERT_NONE}} if REDIS_SSL else {}),
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

### project/settings/auth.py — varies by tier

**`[MINIMAL]`** (session auth, AllowAny):

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "project.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
}
```

**`[STANDARD+]`** (JWT + session, IsAuthenticated, custom user):

```python
from datetime import timedelta

from .environment import ENV

AUTH_USER_MODEL = "access.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "project.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 20,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        minutes=ENV.int("JWT_ACCESS_TOKEN_LIFETIME_MINUTES", default=480)
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        days=ENV.int("JWT_REFRESH_TOKEN_LIFETIME_DAYS", default=7)
    ),
    # Rotation off: the contract's refresh response is `{access}` only, and the
    # decoupled frontend keeps its original refresh token across calls. Stock
    # TokenRefreshView returns a new `refresh` in the body when rotation is on,
    # which would silently diverge from both. Turn rotation on only if the
    # frontend is updated to persist the rotated refresh token on every call.
    "ROTATE_REFRESH_TOKENS": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    # uuid, not the integer PK — a JWT's claims are base64, not encrypted, so
    # the identity field is client-visible. Keeps the contract's "clients only
    # ever see uuid" true for tokens too, not just URLs and payloads.
    "USER_ID_FIELD": "uuid",
    "USER_ID_CLAIM": "user_id",
}
```

### project/pagination.py `[ALL]`

Custom paginator emitting the canonical contract shape (`{page, count, num_pages, results}`) with `page`/`page_size` query params. Wired in above as `DEFAULT_PAGINATION_CLASS`, so every DRF list endpoint paginates in this shape automatically.

```python
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.page.number,
                "count": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "results": data,
            }
        )
```

### project/settings/cors.py `[ALL]`

```python
from .environment import ENV, DEBUG, FRONTEND_BASE_URL

CORS_ALLOWED_ORIGINS = ENV.list(
    "CORS_ALLOWED_ORIGINS",
    default=[FRONTEND_BASE_URL]
)

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
```

### project/settings/aws.py `[FULL]`

```python
from .environment import ENV

# Cloudflare R2 configuration (S3-compatible)
R2_ACCOUNT_ID = ENV.str("R2_ACCOUNT_ID", default="")
R2_ACCESS_KEY_ID = ENV.str("R2_ACCESS_KEY_ID", default="")
R2_SECRET_ACCESS_KEY = ENV.str("R2_SECRET_ACCESS_KEY", default="")
R2_BUCKET_NAME = ENV.str("R2_BUCKET_NAME", default="")
R2_CUSTOM_DOMAIN = ENV.str("R2_CUSTOM_DOMAIN", default="")

R2_ENDPOINT_URL = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"

# AWS-compatible settings (for django-storages)
AWS_ACCESS_KEY_ID = R2_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = R2_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
AWS_S3_REGION_NAME = "auto"
AWS_S3_ENDPOINT_URL = R2_ENDPOINT_URL
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_DEFAULT_ACL = None
# Public bucket served through R2_CUSTOM_DOMAIN, so object URLs are unsigned —
# this matches querystring_auth=False in the [FULL] STORAGES block. For a
# private bucket, set this True and hand out time-limited links via
# FileService.get_signed_url instead. AWS_QUERYSTRING_EXPIRE applies only when
# signing is on.
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_EXPIRE = 3600

AWS_S3_CUSTOM_DOMAIN = R2_CUSTOM_DOMAIN
USE_R2_STORAGE = ENV.bool("USE_R2_STORAGE", default=False)
```

### project/settings/storage.py — varies by tier

**`[MINIMAL]` and `[STANDARD]`** (local filesystem only):

```python
import os

from .environment import BASE_DIR

TEMP_DIR = os.path.join(BASE_DIR, "tmp")
os.makedirs(TEMP_DIR, exist_ok=True)

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
os.makedirs(MEDIA_ROOT, exist_ok=True)
```

**`[FULL]`** (R2 conditional):

```python
import os

from .environment import BASE_DIR
from .aws import (
    R2_ACCESS_KEY_ID,
    R2_SECRET_ACCESS_KEY,
    R2_BUCKET_NAME,
    R2_ENDPOINT_URL,
    R2_CUSTOM_DOMAIN,
    USE_R2_STORAGE,
)

TEMP_DIR = os.path.join(BASE_DIR, "tmp")
os.makedirs(TEMP_DIR, exist_ok=True)

if USE_R2_STORAGE and R2_ACCESS_KEY_ID:
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": R2_ACCESS_KEY_ID,
                "secret_key": R2_SECRET_ACCESS_KEY,
                "bucket_name": R2_BUCKET_NAME,
                "region_name": "auto",
                "endpoint_url": R2_ENDPOINT_URL,
                "signature_version": "s3v4",
                "default_acl": None,
                "querystring_auth": False,
                "custom_domain": R2_CUSTOM_DOMAIN,
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    MEDIA_URL = f"https://{R2_CUSTOM_DOMAIN}/"
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    os.makedirs(MEDIA_ROOT, exist_ok=True)
```

### project/settings/worker.py `[FULL]`

```python
import ssl

from .environment import ENV
from .cache import REDIS_URL, REDIS_SSL

CELERY_BROKER_URL = ENV.str("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = ENV.str("CELERY_RESULT_BACKEND", default=None)

if REDIS_SSL:
    CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE}
    CELERY_REDIS_BACKEND_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE}

CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"

CELERY_TASK_ANNOTATIONS = {
    "*": {
        "max_retries": 5,
        "retry_backoff": True,
    }
}

CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes

PROCESS_TASKS_ASYNC = ENV.bool("PROCESS_TASKS_ASYNC", default=True)
```

### project/settings/email.py `[FULL]`

```python
from .environment import ENV

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ENV.str("EMAIL_HOST", default="")
EMAIL_PORT = ENV.int("EMAIL_PORT", default=587)
EMAIL_USE_TLS = ENV.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = ENV.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = ENV.str("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = ENV.str("DEFAULT_FROM_EMAIL", default="noreply@example.com")

PASSWORD_RESET_TIMEOUT = 3600
```

### project/settings/logging.py — varies by tier

**`[MINIMAL]` and `[STANDARD]`** (no celery logger):

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
```

**`[FULL]`** (adds celery logger):

```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "celery": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
```

### project/settings/sentry.py — `[STANDARD+]`, varies by tier

**`[STANDARD]`** (Django + Logging integrations only):

```python
import logging
from .environment import ENV, ENVIRONMENT

SENTRY_DSN = ENV.str("SENTRY_DSN", default="")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
        send_default_pii=False,
    )
```

**`[FULL]`** (adds Celery + Redis integrations):

```python
import logging
from .environment import ENV, ENVIRONMENT

SENTRY_DSN = ENV.str("SENTRY_DSN", default="")

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.redis import RedisIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR,
            ),
        ],
        send_default_pii=False,
    )
```

---

## Services `[FULL]`

### project/services/\_\_init\_\_.py

```python
```

### project/services/storage.py

```python
import boto3
from botocore.config import Config
from django.conf import settings


class R2Client:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = boto3.client(
                "s3",
                endpoint_url=settings.R2_ENDPOINT_URL,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
                config=Config(signature_version="s3v4"),
                region_name="auto",
            )
        return cls._client

    @classmethod
    def get_signed_url(cls, key: str, expires_in: int = 3600) -> str:
        client = cls.get_client()
        return client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.R2_BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in,
        )

    @classmethod
    def get_public_url(cls, key: str) -> str:
        return f"https://{settings.R2_CUSTOM_DOMAIN}/{key}"

    @classmethod
    def upload_file(cls, file_data: bytes, key: str, content_type: str = "audio/mpeg"):
        client = cls.get_client()
        client.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=key,
            Body=file_data,
            ContentType=content_type,
        )

    @classmethod
    def delete_file(cls, key: str):
        client = cls.get_client()
        client.delete_object(Bucket=settings.R2_BUCKET_NAME, Key=key)

    @classmethod
    def file_exists(cls, key: str) -> bool:
        client = cls.get_client()
        try:
            client.head_object(Bucket=settings.R2_BUCKET_NAME, Key=key)
            return True
        except client.exceptions.ClientError:
            return False
```

### project/services/email.py

```python
from enum import Enum

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class EmailType(Enum):
    TRANSACTIONAL = "transactional"
    USER_TRIGGERED = "user_triggered"
    MARKETING = "marketing"


class EmailService:
    @classmethod
    def render_template(cls, template_name, context) -> str:
        context.setdefault("frontend_url", settings.FRONTEND_BASE_URL)
        return render_to_string(template_name, context)

    @classmethod
    def should_send(cls, user, email_type: EmailType) -> bool:
        if email_type == EmailType.TRANSACTIONAL:
            return True
        return getattr(user, "email_notifications", True)

    @classmethod
    def send(cls, user, email_type, subject, message, html_message=None) -> bool:
        if not cls.should_send(user, email_type):
            return False
        # fail_silently keeps a delivery failure from raising, but send_mail
        # returns the number of messages actually delivered — return that so the
        # caller can tell a real send from a silently-swallowed failure.
        sent = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=True,
        )
        return sent > 0
```

### project/services/discord.py

```python
import logging
from enum import Enum

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class DiscordColor(Enum):
    GREEN = 0x2ECC71
    BLUE = 0x3498DB
    ORANGE = 0xE67E22
    RED = 0xE74C3C


class DiscordService:
    @classmethod
    def send_embed(cls, webhook_url, title, description, color, fields=None) -> bool:
        if not webhook_url:
            return False
        try:
            embed = {
                "title": title,
                "description": description,
                "color": color.value,
            }
            if fields:
                embed["fields"] = [
                    {"name": k, "value": str(v), "inline": True}
                    for k, v in fields.items()
                ]
            payload = {"embeds": [embed]}
            requests.post(webhook_url, json=payload, timeout=10)
            return True
        except Exception as e:
            logger.warning(f"Discord webhook failed: {e}")
            return False

    @classmethod
    def notify_signup(cls, email, name=None):
        cls.send_embed(
            getattr(settings, "DISCORD_WEBHOOK_SIGNUPS", ""),
            "New Signup",
            f"**{name or email}** just signed up",
            DiscordColor.GREEN,
        )
```

---

## Custom User Model `[STANDARD+]`

### access/models.py

```python
import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )
    # Unique so the contract's email-based login (/api/v1/auth/login/) can
    # resolve a single account. Public identifier stays `uuid`, not the PK.
    email = models.EmailField(unique=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return self.email or self.username
```

### access/admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ["email", "username", "is_active", "is_staff", "date_joined"]
    list_filter = ["is_active", "is_staff", "date_joined"]
    search_fields = ["email", "username"]
    ordering = ["-date_joined"]
```

### access/apps.py

```python
from django.apps import AppConfig


class AccessConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "access"
```

### access/serializers.py

```python
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def tokens_for(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


class UserSerializer(serializers.ModelSerializer):
    # Public identifier is uuid — the integer PK is never exposed.
    class Meta:
        model = User
        fields = ["uuid", "username", "email", "first_name", "last_name"]
        read_only_fields = ["uuid"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = User.objects.filter(email=attrs["email"]).first()
        if user is None or not user.check_password(attrs["password"]):
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        attrs["user"] = user
        return attrs
```

### access/views.py

```python
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
    tokens_for,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"user": UserSerializer(user).data, "tokens": tokens_for(user)},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(tokens_for(serializer.validated_data["user"]))


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
```

### access/urls.py

Ships the contract's auth endpoints. Refresh reuses SimpleJWT's `TokenRefreshView` (returns `{access}`).

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("me/", views.MeView.as_view(), name="me"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
```

---

## Docker (REQUIRED — do not skip)

### docker-compose.yml — varies by tier

**`[MINIMAL]`** (web + db):

```yaml
name: {project-name}

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["/wait-for-it.sh", "db", "--", "/entrypoint.sh"]
    volumes:
      - .:/app
    ports:
      - "{host_port}:8000"
    depends_on:
      - db
    env_file:
      - .env
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}

  db:
    image: postgres:17
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB={db_name}
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

volumes:
  postgres_data:
```

**`[STANDARD]`** (web + db + redis):

```yaml
name: {project-name}

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["/wait-for-it.sh", "db", "--", "/entrypoint.sh"]
    volumes:
      - .:/app
    ports:
      - "{host_port}:8000"
    depends_on:
      - db
      - redis
    env_file:
      - .env
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}

  db:
    image: postgres:17
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB={db_name}
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**`[FULL]`** (web + db + redis + celery + celery-beat):

```yaml
name: {project-name}

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["/wait-for-it.sh", "db", "--", "/entrypoint.sh"]
    volumes:
      - .:/app
    ports:
      - "{host_port}:8000"
    depends_on:
      - db
      - redis
    env_file:
      - .env
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}

  db:
    image: postgres:17
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB={db_name}
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

  celery:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: celery --app=project worker --loglevel=INFO --without-heartbeat --without-gossip --without-mingle
    volumes:
      - .:/app
    depends_on:
      - web
      - redis
    env_file:
      - .env
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}
      - CELERY_BROKER_URL=redis://redis:6379/0

  celery-beat:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: celery --app=project beat --loglevel=INFO
    volumes:
      - .:/app
    depends_on:
      - web
      - redis
    env_file:
      - .env
    environment:
      - DEBUG=True
      - DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}
      - CELERY_BROKER_URL=redis://redis:6379/0

volumes:
  postgres_data:
  redis_data:
```

### Dockerfile.dev `[ALL]`

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY docker/wait-for-it.sh /wait-for-it.sh
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /wait-for-it.sh /entrypoint.sh

COPY . .

EXPOSE 8000

CMD ["/entrypoint.sh"]
```

### docker/entrypoint.sh `[ALL]`

```bash
#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000
```

### docker/wait-for-it.sh `[ALL]`

```bash
#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
```

---

## Makefile (REQUIRED — do not skip) — varies by tier

**`[MINIMAL]` and `[STANDARD]`** (docker + django + test + db + utils):

```makefile
# {project-name} - Makefile
PROJECT_NAME = {project-name}
DOCKER_COMPOSE = docker compose --project-name $(PROJECT_NAME)

# ============================================================================
# Docker
# ============================================================================

.PHONY: build up down restart stop ps logs logs-all bash wipe

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up --detach

down:
	$(DOCKER_COMPOSE) down

restart: down up

stop:
	$(DOCKER_COMPOSE) stop

ps:
	$(DOCKER_COMPOSE) ps

logs:
	$(DOCKER_COMPOSE) logs -f web

logs-all:
	$(DOCKER_COMPOSE) logs -f

bash:
	$(DOCKER_COMPOSE) exec web bash

wipe:
	@echo "WARNING: This will delete all containers and volumes!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) down -v --remove-orphans

# ============================================================================
# Django
# ============================================================================

.PHONY: manage shell migrate makemigrations createsuperuser collectstatic showmigrations

manage:
	$(DOCKER_COMPOSE) exec web python manage.py $(filter-out $@,$(MAKECMDGOALS))

shell:
	$(DOCKER_COMPOSE) exec web python manage.py shell

migrate:
	$(DOCKER_COMPOSE) exec web python manage.py migrate

makemigrations:
	$(DOCKER_COMPOSE) exec web python manage.py makemigrations

createsuperuser:
	$(DOCKER_COMPOSE) exec web python manage.py createsuperuser

collectstatic:
	$(DOCKER_COMPOSE) exec web python manage.py collectstatic --noinput

showmigrations:
	$(DOCKER_COMPOSE) exec web python manage.py showmigrations

# ============================================================================
# Testing
# ============================================================================

.PHONY: test test-cov test-cov-html

test:
	$(DOCKER_COMPOSE) exec web python manage.py test

test-cov:
	$(DOCKER_COMPOSE) exec web coverage run --source='.' manage.py test
	$(DOCKER_COMPOSE) exec web coverage report

test-cov-html:
	$(DOCKER_COMPOSE) exec web coverage run --source='.' manage.py test
	$(DOCKER_COMPOSE) exec web coverage html

# ============================================================================
# Database
# ============================================================================

.PHONY: dbshell dbreset

dbshell:
	$(DOCKER_COMPOSE) exec db psql -U postgres -d {db_name}

dbreset:
	@echo "WARNING: This will delete the database!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) exec db psql -U postgres -c "DROP DATABASE IF EXISTS {db_name};"
	$(DOCKER_COMPOSE) exec db psql -U postgres -c "CREATE DATABASE {db_name};"
	$(DOCKER_COMPOSE) exec web python manage.py migrate

# ============================================================================
# Admin Theme
# ============================================================================

.PHONY: admin_theme_dump admin_theme_load

admin_theme_dump:
	$(DOCKER_COMPOSE) exec web python manage.py dumpdata admin_interface.Theme --indent 2 > admin_theme.json

admin_theme_load:
	$(DOCKER_COMPOSE) exec web python manage.py loaddata admin_theme.json

# ============================================================================
# Utilities
# ============================================================================

.PHONY: lint format clean

lint:
	$(DOCKER_COMPOSE) exec web ruff check .

format:
	$(DOCKER_COMPOSE) exec web ruff format .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Catch-all for manage commands
%:
	@:
```

**`[FULL]`** (adds celery + heroku sections):

```makefile
# {project-name} - Makefile
PROJECT_NAME = {project-name}
DOCKER_COMPOSE = docker compose --project-name $(PROJECT_NAME)

# ============================================================================
# Docker
# ============================================================================

.PHONY: build up down restart stop ps logs logs-all logs-celery logs-beat bash wipe

build:
	$(DOCKER_COMPOSE) build

up:
	$(DOCKER_COMPOSE) up --detach

down:
	$(DOCKER_COMPOSE) down

restart: down up

stop:
	$(DOCKER_COMPOSE) stop

ps:
	$(DOCKER_COMPOSE) ps

logs:
	$(DOCKER_COMPOSE) logs -f web

logs-all:
	$(DOCKER_COMPOSE) logs -f

logs-celery:
	$(DOCKER_COMPOSE) logs -f celery

logs-beat:
	$(DOCKER_COMPOSE) logs -f celery-beat

bash:
	$(DOCKER_COMPOSE) exec web bash

wipe:
	@echo "WARNING: This will delete all containers and volumes!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) down -v --remove-orphans

# ============================================================================
# Django
# ============================================================================

.PHONY: manage shell migrate makemigrations createsuperuser collectstatic showmigrations

manage:
	$(DOCKER_COMPOSE) exec web python manage.py $(filter-out $@,$(MAKECMDGOALS))

shell:
	$(DOCKER_COMPOSE) exec web python manage.py shell

migrate:
	$(DOCKER_COMPOSE) exec web python manage.py migrate

makemigrations:
	$(DOCKER_COMPOSE) exec web python manage.py makemigrations

createsuperuser:
	$(DOCKER_COMPOSE) exec web python manage.py createsuperuser

collectstatic:
	$(DOCKER_COMPOSE) exec web python manage.py collectstatic --noinput

showmigrations:
	$(DOCKER_COMPOSE) exec web python manage.py showmigrations

# ============================================================================
# Celery
# ============================================================================

.PHONY: celery celery-beat celery-purge celery-restart

celery:
	$(DOCKER_COMPOSE) exec celery celery --app=project worker --loglevel=INFO

celery-beat:
	$(DOCKER_COMPOSE) exec celery-beat celery --app=project beat --loglevel=INFO

celery-purge:
	$(DOCKER_COMPOSE) exec celery celery --app=project purge -f

celery-restart:
	$(DOCKER_COMPOSE) restart celery celery-beat

# ============================================================================
# Testing
# ============================================================================

.PHONY: test test-cov test-cov-html

test:
	$(DOCKER_COMPOSE) exec web python manage.py test

test-cov:
	$(DOCKER_COMPOSE) exec web coverage run --source='.' manage.py test
	$(DOCKER_COMPOSE) exec web coverage report

test-cov-html:
	$(DOCKER_COMPOSE) exec web coverage run --source='.' manage.py test
	$(DOCKER_COMPOSE) exec web coverage html

# ============================================================================
# Database
# ============================================================================

.PHONY: dbshell dbreset

dbshell:
	$(DOCKER_COMPOSE) exec db psql -U postgres -d {db_name}

dbreset:
	@echo "WARNING: This will delete the database!"
	@read -p "Are you sure? [y/N] " confirm && [ "$$confirm" = "y" ]
	$(DOCKER_COMPOSE) exec db psql -U postgres -c "DROP DATABASE IF EXISTS {db_name};"
	$(DOCKER_COMPOSE) exec db psql -U postgres -c "CREATE DATABASE {db_name};"
	$(DOCKER_COMPOSE) exec web python manage.py migrate

# ============================================================================
# Admin Theme
# ============================================================================

.PHONY: admin_theme_dump admin_theme_load

admin_theme_dump:
	$(DOCKER_COMPOSE) exec web python manage.py dumpdata admin_interface.Theme --indent 2 > admin_theme.json

admin_theme_load:
	$(DOCKER_COMPOSE) exec web python manage.py loaddata admin_theme.json

# ============================================================================
# Utilities
# ============================================================================

.PHONY: lint format clean

lint:
	$(DOCKER_COMPOSE) exec web ruff check .

format:
	$(DOCKER_COMPOSE) exec web ruff format .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# ============================================================================
# Heroku
# ============================================================================

HEROKU_APP = {heroku-app-name}

.PHONY: heroku-bash heroku-logs heroku-config

heroku-bash:
	heroku run bash -a $(HEROKU_APP)

heroku-logs:
	heroku logs --tail -a $(HEROKU_APP)

heroku-config:
	heroku config -a $(HEROKU_APP)

# ============================================================================
# Stripe (if applicable)
# ============================================================================

.PHONY: stripe_listen ngrok

stripe_listen:
	stripe listen --forward-to localhost:{host_port}/api/v1/payments/webhook/

ngrok:
	ngrok http {host_port}

# Catch-all for manage commands
%:
	@:
```

---

## Deployment

### Procfile — varies by tier

**`[MINIMAL]` and `[STANDARD]`:**

```
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --worker-class gthread
```

**`[FULL]`** (adds worker + beat):

```
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --worker-class gthread
worker: celery --app=project worker --loglevel=INFO --concurrency=2 --without-heartbeat --without-gossip --without-mingle
beat: celery --app=project beat --loglevel=INFO
```

### .python-version `[ALL]`

```
3.12
```

### .github/workflows/deploy-backend.yml `[FULL]`

```yaml
name: Deploy Backend

on:
  push:
    branches: [main]
    paths:
      - '{service_name}/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: akhileshns/heroku-deploy@v3.13.15
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "{heroku-app-name}"
          heroku_email: "{email}"
          appdir: "{service_name}"
```

---

## Config Files

### requirements.txt — varies by tier

**`[MINIMAL]`:**

```
Django>=5.2,<6.0
djangorestframework>=3.16,<4.0
django-cors-headers>=4.4,<5.0
django-environ>=0.11,<1.0
django-admin-interface>=0.28,<1.0
django-admin-autocomplete-filter==0.7.1
dj-database-url>=2.2,<3.0
whitenoise>=6.7,<7.0
gunicorn>=22.0,<23.0
psycopg2-binary>=2.9,<3.0
coverage>=7.6,<8.0
ruff>=0.7,<1.0
```

**`[STANDARD]`** (adds simplejwt, redis, sentry-sdk, storages):

```
Django>=5.2,<6.0
djangorestframework>=3.16,<4.0
djangorestframework-simplejwt>=5.5,<6.0
django-cors-headers>=4.4,<5.0
django-environ>=0.11,<1.0
django-storages[boto3]>=1.14,<2.0
django-admin-interface>=0.28,<1.0
django-admin-autocomplete-filter==0.7.1
dj-database-url>=2.2,<3.0
whitenoise>=6.7,<7.0
gunicorn>=22.0,<23.0
redis>=5.0,<6.0
psycopg2-binary>=2.9,<3.0
sentry-sdk>=2.14,<3.0
coverage>=7.6,<8.0
ruff>=0.7,<1.0
```

**`[FULL]`** (adds celery, boto3, requests):

```
Django>=5.2,<6.0
djangorestframework>=3.16,<4.0
djangorestframework-simplejwt>=5.5,<6.0
django-cors-headers>=4.4,<5.0
django-environ>=0.11,<1.0
django-storages[boto3]>=1.14,<2.0
django-admin-interface>=0.28,<1.0
django-admin-autocomplete-filter==0.7.1
dj-database-url>=2.2,<3.0
whitenoise>=6.7,<7.0
gunicorn>=22.0,<23.0
celery[redis]>=5.4,<6.0
redis>=5.0,<6.0
psycopg2-binary>=2.9,<3.0
boto3>=1.35,<2.0
requests>=2.32,<3.0
sentry-sdk>=2.14,<3.0
coverage>=7.6,<8.0
ruff>=0.7,<1.0
```

### .env.example — varies by tier

**`[MINIMAL]`:**

```bash
# Core
DEBUG=True
ENVIRONMENT=development
SECRET_KEY=django-insecure-change-me-in-production
VERSION=0.1.0

# Database
DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}

# Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:{host_port}
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Frontend
FRONTEND_BASE_URL=http://localhost:3000
```

**`[STANDARD]`** (adds redis, jwt, sentry):

```bash
# Core
DEBUG=True
ENVIRONMENT=development
SECRET_KEY=django-insecure-change-me-in-production
VERSION=0.1.0

# Database & Cache
DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}
REDIS_URL=redis://redis:6379/0

# Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:{host_port}
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Frontend
FRONTEND_BASE_URL=http://localhost:3000

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=480
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Error Tracking
SENTRY_DSN=
```

**`[FULL]`** (adds celery, R2, email):

```bash
# Core
DEBUG=True
ENVIRONMENT=development
SECRET_KEY=django-insecure-change-me-in-production
VERSION=0.1.0

# Database & Cache
DATABASE_URL=postgres://postgres:postgres@db:5432/{db_name}
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0

# Hosts
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:{host_port}
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Frontend
FRONTEND_BASE_URL=http://localhost:3000

# JWT
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=480
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# Storage (Cloudflare R2)
USE_R2_STORAGE=False
R2_ACCOUNT_ID=
R2_ACCESS_KEY_ID=
R2_SECRET_ACCESS_KEY=
R2_BUCKET_NAME=
R2_CUSTOM_DOMAIN=

# Email (Resend SMTP)
EMAIL_HOST=smtp.resend.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=resend
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=noreply@example.com

# Error Tracking
SENTRY_DSN=

# Async Tasks
PROCESS_TASKS_ASYNC=True
```

### .gitignore `[ALL]`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
.eggs/
dist/
build/

# Django
*.log
local_settings.py
db.sqlite3
staticfiles/
media/

# Environment
.env
.venv
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# Testing
.coverage
htmlcov/
.pytest_cache/

# Temp
tmp/
*.tmp

# OS
.DS_Store
Thumbs.db

# Celery
celerybeat-schedule
celerybeat-schedule.db
```

### .coveragerc `[ALL]`

```ini
[run]
source = .
branch = True
omit =
    */migrations/*
    */tests/*
    */test_*.py
    */__pycache__/*
    */venv/*
    manage.py
    */settings/*
    */admin.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
show_missing = True
skip_covered = False

[html]
directory = htmlcov
```

---

## App Structure Convention `[ALL]`

When adding a new app, create this structure:

```
{app_name}/
├── __init__.py
├── admin.py          # ModelAdmin with list_display, list_filter, inlines
├── apps.py           # AppConfig
├── models.py         # Inherit AbstractModel
├── serializers.py    # DRF serializers
├── services.py       # Business logic (NOT in views)
├── tasks.py          # Celery tasks ([FULL] only)
├── urls.py           # Export urlpatterns
├── views.py          # Thin APIViews that call services
├── migrations/
│   └── __init__.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_views.py
```

Then add the app to `LOCAL_APPS` in `project/settings/apps.py`.

### URL export pattern (app/urls.py)

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListView.as_view(), name="list"),
    path("<uuid:uuid>/", views.DetailView.as_view(), name="detail"),
]
```

Then in `project/urls.py`:

```python
from {app}.urls import urlpatterns as {app}_urlpatterns

urlpatterns = [
    # ...
    path("api/v1/{app}/", include(({app}_urlpatterns, "{app}"))),
]
```

### View pattern

```python
from rest_framework.views import APIView
from rest_framework.response import Response

class ListView(APIView):
    def get(self, request):
        items = ItemService().list(request.user)
        return Response(ItemSerializer(items, many=True).data)
```

### Service pattern

```python
class ItemService:
    def __init__(self, ai_service=None):
        self.ai = ai_service  # inject external deps

    def list(self, user):
        return Item.objects.filter(user=user)

    def create(self, user, data):
        return Item.objects.create(user=user, **data)
```

### Celery task pattern `[FULL]`

```python
from celery import shared_task

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def process_item_task(self, item_id: int):
    try:
        item = Item.objects.get(id=item_id)
        ItemService().process(item)
    except Exception as e:
        self.retry(exc=e)
```

---

## Optional: AI Service (Anthropic)

Only generate this section if the user requests AI/LLM integration.

### project/settings/ai.py

```python
from .environment import ENV

ANTHROPIC_API_KEY = ENV.str("ANTHROPIC_API_KEY", default="")
ANTHROPIC_MODEL = ENV.str("ANTHROPIC_MODEL", default="claude-sonnet-5")
ANTHROPIC_MAX_TOKENS = ENV.int("ANTHROPIC_MAX_TOKENS", default=4096)
```

Add to `project/settings/__init__.py`:
```python
# AI
from .ai import *  # noqa: F401, F403
```

### project/services/ai.py

```python
import json
import logging
import re

from django.conf import settings

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._client

    def chat(self, messages, system=None, max_tokens=None, temperature=1.0) -> str:
        response = self.client.messages.create(
            model=settings.ANTHROPIC_MODEL,
            max_tokens=max_tokens or settings.ANTHROPIC_MAX_TOKENS,
            messages=messages,
            system=system or "",
            temperature=temperature,
        )
        return response.content[0].text

    def chat_with_json(self, messages, system=None, **kwargs) -> tuple[str, dict | None]:
        response = self.chat(messages, system=system, **kwargs)
        json_data = self.extract_json(response)
        return response, json_data

    @staticmethod
    def extract_json(text: str) -> dict | None:
        match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1).strip())
            except json.JSONDecodeError:
                pass
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
        return None


_ai_service = None

def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
```

Add `anthropic` to `requirements.txt`.

---

## Optional: Stripe Integration

Only generate this section if the user requests payment processing.

### project/settings/stripe.py

```python
from .environment import ENV

STRIPE_SECRET_KEY = ENV.str("STRIPE_SECRET_KEY", default="")
STRIPE_PUBLISHABLE_KEY = ENV.str("STRIPE_PUBLISHABLE_KEY", default="")
STRIPE_WEBHOOK_SECRET = ENV.str("STRIPE_WEBHOOK_SECRET", default="")
```

Add to `project/settings/__init__.py`:
```python
# Stripe
from .stripe import *  # noqa: F401, F403
```

### Stripe webhook view pattern

```python
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # handle payment...

    return HttpResponse(status=200)
```

Add `stripe` to `requirements.txt`.

---

## Key Patterns Summary

| Pattern | Convention | Tier |
|---------|-----------|------|
| Settings module | Always `project.settings`, never the project name | ALL |
| Settings structure | Modular files in `settings/`, wildcard imports in `__init__.py` | ALL |
| ENV access | `ENV` singleton from `environment.py`, imported by all settings files | ALL |
| Models | Always inherit `AbstractModel` (uuid, metadata, created_at, updated_at) | ALL |
| Views | Thin — delegate to services, return serialized responses | ALL |
| Services | All business logic lives here, external deps injected via `__init__` | ALL |
| URLs | Export urlpatterns from each app, aggregate in `project/urls.py` with `api/v1/` prefix | ALL |
| Apps list | `DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS` | ALL |
| CORS | Allow all in DEBUG, explicit origins in prod | ALL |
| Prod security | SSL redirect, XSS filter, nosniff — only when `not DEBUG` | ALL |
| Admin theme | django-admin-interface, portable via `dumpdata`/`loaddata` | ALL |
| Port mapping | Container always 8000, host port varies per project | ALL |
| All commands | Via Makefile -> `docker compose exec`, never run Python directly | ALL |
| Storage | Conditional R2/local based on `USE_R2_STORAGE` env flag | FULL |
| Redis cache | Redis backend, cache-based sessions | STANDARD+ |
| JWT auth | simplejwt with custom User model | STANDARD+ |
| Sentry | Error tracking with tier-appropriate integrations | STANDARD+ |
| Celery | `PROCESS_TASKS_ASYNC` flag for synchronous testing | FULL |
| Redis SSL | Auto-detect `rediss://` prefix, set `ssl_cert_reqs=CERT_NONE` for Heroku | STANDARD+ |
| Deployment | Heroku with Procfile release phase (migrate + collectstatic) | FULL |

---

## Post-Bootstrap Checklist

### All tiers

1. Create service directory, init git
2. Generate all files from templates above (respecting blueprint tier), replacing placeholders
3. Copy `.env.example` to `.env`
4. Verify Docker files exist: `Dockerfile.dev`, `docker-compose.yml`, `Makefile`, `docker/entrypoint.sh`, `docker/wait-for-it.sh`
5. `make build && make up`
6. `make migrate` (standard/full: run `make makemigrations` first — the shipped `access/` app has no migration files, so `migrate` alone fails with `Dependency on app with no migrations: access`)
7. `make createsuperuser`
8. Verify admin at `http://localhost:{host_port}/admin/`
9. Add first app: `make manage startapp {app_name}`
10. Add app to `LOCAL_APPS` in `settings/apps.py`
11. Create models inheriting `AbstractModel`
12. `make makemigrations && make migrate`

### Standard+ additional steps

13. Verify Redis is running: `make ps` should show the redis container
14. Verify JWT auth works: create a user and obtain tokens via API

### Full additional steps

15. Verify Celery worker is running: `make logs-celery` should show worker ready
16. Verify Celery Beat is running: `make logs-beat` should show beat scheduler started
17. Test a debug task if needed

---

## Upgrading Between Tiers

### Minimal → Standard (add auth + Redis + Sentry)

1. **Install packages**: add `djangorestframework-simplejwt`, `redis`, `sentry-sdk`, `django-storages[boto3]` to `requirements.txt`
2. **Create `access/` app**: copy the `[STANDARD+]` access app files (User model, admin, apps, urls, `migrations/__init__.py`)
3. **Add settings files**: create `settings/sentry.py` from the `[STANDARD]` template
4. **Update existing settings**:
   - `settings/apps.py`: add `rest_framework_simplejwt`, `rest_framework_simplejwt.token_blacklist`, `storages` to `THIRD_PARTY_APPS` and `access` to `LOCAL_APPS`
   - `settings/cache.py`: replace LocMemCache with Redis backend, switch `SESSION_ENGINE` to `django.contrib.sessions.backends.cache`, add `SESSION_CACHE_ALIAS`, add `REDIS_URL`/`REDIS_SSL` config
   - `settings/auth.py`: add `AUTH_USER_MODEL = "access.User"`, add JWT authentication class, switch default permission to `IsAuthenticated`, add `SIMPLE_JWT` config
   - `settings/__init__.py`: add `from .sentry import *`
5. **Update Docker**: add `redis` service to `docker-compose.yml`, add `redis` to web's `depends_on`, add `redis_data` volume
6. **Update `.env`**: add `REDIS_URL`, `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`, `JWT_REFRESH_TOKEN_LIFETIME_DAYS`, `SENTRY_DSN` variables
7. **Run**: `make build && make up && make makemigrations && make migrate`

### Standard → Full (add Celery + cloud services)

1. **Install packages**: add `celery[redis]`, `boto3`, `requests` to `requirements.txt`
2. **Create files**: `project/worker.py`, `settings/aws.py`, `settings/worker.py`, `settings/email.py`, `project/services/__init__.py`, `project/services/storage.py`, `project/services/email.py`, `project/services/discord.py`
3. **Update `project/__init__.py`**: add `from .worker import app as celery_app` and `__all__ = ("celery_app",)`
4. **Update `settings/__init__.py`**: add `from .aws import *`, `from .worker import *`, `from .email import *` imports
5. **Update `settings/storage.py`**: add R2 conditional logic (import from `.aws`, add `if USE_R2_STORAGE and R2_ACCESS_KEY_ID:` block)
6. **Update `settings/sentry.py`**: add `CeleryIntegration` and `RedisIntegration` imports and integrations
7. **Update `settings/logging.py`**: add `"celery"` logger entry
8. **Update Docker**: add `celery`, `celery-beat` services to `docker-compose.yml`
9. **Update Makefile**: add celery section (`celery`, `celery-beat`, `celery-purge`, `celery-restart` targets), add `logs-celery`/`logs-beat` targets, add heroku section
10. **Update Procfile**: add `worker` and `beat` entries
11. **Update `.env`**: add `CELERY_BROKER_URL`, `PROCESS_TASKS_ASYNC`, `USE_R2_STORAGE`, `R2_*`, `EMAIL_*` variables
12. **Run**: `make build && make up`
