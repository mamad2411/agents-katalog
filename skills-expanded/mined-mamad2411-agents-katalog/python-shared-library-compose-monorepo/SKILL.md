---
name: python-shared-library-compose-monorepo
description: Structure a shared Python library for multiple FastAPI microservices in a Docker Compose monorepo, with pip-installable common package, per-service pyproject.toml, and Dockerfile layer caching
version: 2
created: 2026-05-15
updated: 2026-05-15
---
## When to Use
When building a multi-service Docker Compose environment where multiple Python FastAPI services share common code (models, config, telemetry, HTTP clients). Use this pattern to avoid duplicating code across services while keeping Docker layer caching efficient.

## Procedure

### 1. Create a shared library package

Structure:
```
common/
  pyproject.toml
  src/
    x402_common/
      __init__.py
      config.py
      http.py
      logging.py
      mock_base.py
      models.py
      telemetry.py
```

`common/pyproject.toml` — declare all shared dependencies here:
```toml
[project]
name = "x402-common"
version = "0.1.0"
dependencies = [
    "fastapi>=0.111",
    "uvicorn>=0.29",
    "pydantic>=2.7",
    "pydantic-settings>=2.2",
    "httpx>=0.27",
    "structlog>=24.1",
    "opentelemetry-api>=1.25",
    "opentelemetry-sdk>=1.25",
    "opentelemetry-instrumentation-fastapi>=0.45b0",
    "opentelemetry-instrumentation-httpx>=0.45b0",
    "opentelemetry-exporter-otlp>=1.25",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

`common/src/x402_common/__init__.py` — re-export for convenience:
```python
from x402_common.mock_base import create_app
from x402_common.config import ServiceConfig
from x402_common.telemetry import instrument
```

### 2. Create reusable common modules

**config.py** — Pydantic Settings with env var prefix:
```python
from pydantic_settings import BaseSettings

class ServiceConfig(BaseSettings):
    service_name: str = "unknown"
    log_level: str = "INFO"
    seller_url: str = ""
    gateway_url: str = ""
    # ... other service URLs

    model_config = {"env_prefix": "X402_"}
```

**mock_base.py** — FastAPI app factory:
```python
from fastapi import FastAPI

def create_app(title: str, version: str = "0.1.0") -> FastAPI:
    app = FastAPI(title=title, version=version, docs_url="/api/docs")
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    return app
```

**http.py** — HTTP client factory:
```python
from httpx import AsyncClient

def make_client(base_url: str) -> AsyncClient:
    return AsyncClient(base_url=base_url, timeout=10.0)
```

**telemetry.py** — OpenTelemetry instrumentation:
```python
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor as _HTTPXInstrumentor

def instrument(app):
    FastAPIInstrumentor.instrument_app(app)
    _HTTPXInstrumentor().instrument()  # Note: instantiate the class first
```

### 3. Create per-service packages

Each service has its own `pyproject.toml` that depends on the shared library:
```toml
[project]
name = "x402-seller"
version = "0.1.0"
dependencies = ["x402-common"]

[tool.setuptools.packages.find]
where = ["."]
include = ["src*"]
```

Service main.py uses shared code:
```python
from x402_common import create_app, ServiceConfig, instrument
from x402_common.models import Invoice
from x402_common.http import make_client

app = create_app("seller-api", "0.1.0")
instrument(app)
config = ServiceConfig()
client = make_client(config.gateway_url)
```

### 4. Write service Dockerfiles with layer caching

```dockerfile
FROM python:3.12-slim
WORKDIR /app

# Install common library first (layer cached unless common/ changes)
COPY common/pyproject.toml /app/common/
COPY common/src/ /app/common/src/
RUN pip install --no-cache-dir /app/common/.

# Install service (layer cached unless service/ changes)
COPY services/seller/pyproject.toml .
COPY services/seller/src/ src/
RUN pip install --no-cache-dir -e .

EXPOSE 8000
CMD ["uvicorn", "src.seller.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Key optimization**: Common library is installed first as a separate Docker layer. If only a service changes, the common library layer is cached. Rebuilds are fast.

### 5. Docker Compose build context

All services share the project root as build context:
```yaml
seller:
  build:
    context: .
    dockerfile: services/seller/Dockerfile
  environment:
    - X402_SERVICE_NAME=seller
    - X402_GATEWAY_URL=http://toxiproxy:18000
```

The `context: .` (project root) is essential because the Dockerfile references both `common/` and `services/seller/`.

### 6. Test runner Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /app
RUN pip install --no-cache-dir pytest httpx pytest-asyncio
COPY common/ /app/common/
RUN pip install --no-cache-dir /app/common/.
CMD ["sleep", "infinity"]
```

## Pitfalls
- **OpenTelemetry HTTPXInstrumentor**: Call `HTTPXClientInstrumentor().instrument()` (instantiate the class first). Calling `HTTPXClientInstrumentor.instrument()` directly raises TypeError in newer versions.
- **Docker build context must be project root**: `context: .` not `context: ./services/seller/` because the Dockerfile copies from `common/` AND `services/seller/`.
- **Shared library version**: Pin or at least set `dependencies = ["x402-common"]` in service pyproject.toml so pip resolves the local package.
- **Pydantic Settings env prefix**: All config vars use `X402_` prefix (e.g., `X402_SELLER_URL`, `X402_GATEWAY_URL`). Docker Compose env vars must match.
- **`docker cp src/. container:/dest/` copies directory CONTENTS** (flattened), not the directory itself. So `docker cp my-poc/. container:/workspace/` puts files at `/workspace/docker-compose.yml`, NOT `/workspace/my-poc/docker-compose.yml`. Account for this flattening when using DinD setups.
- **Don't include `version` key** in docker-compose.yml — it's obsolete in Compose v2+ and causes deprecation warnings.
- **`[tool.setuptools.packages.find]` is required** in service pyproject.toml — without `include = ["src*"]`, setuptools won't find `src/buyer/` as a package and imports will fail at runtime with ModuleNotFoundError.
## Verification
1. `docker compose build <service>` — both common and service layers build
2. `docker compose build <service>` again — common layer is cached if unchanged
3. Service starts with `uvicorn` and responds on `/health`
4. Service can import from `x402_common` at runtime