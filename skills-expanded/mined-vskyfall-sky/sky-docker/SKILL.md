---
name: sky-docker
description: >-
  Docker ve Compose ustalığı: her dil için çok aşamalı (multi-stage) Dockerfile kalıpları
  (Node, Python/uv, Go, Rust, Java), katman önbelleği ve BuildKit cache mount'ları, küçük ve
  güvenli imajlar (distroless, non-root, .dockerignore), healthcheck, yerel geliştirme için
  docker compose (Postgres, Redis, MinIO, Mailpit, watch), imaj tarama, etiketleme ve kayıt
  defteri, sık hatalar. "Dockerize et", "Dockerfile yaz", "compose", "imaj çok büyük" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Docker

## Altın kurallar

1. **Çok aşamalı** build: derleme araçları son imaja girmez.
2. Önce bağımlılık dosyalarını kopyala, sonra kaynak → bağımlılık katmanı önbellekte kalır.
3. **non-root** kullanıcı, salt gerekli dosyalar, `.dockerignore`.
4. Sırlar imaja gömülmez (`ARG`/`ENV` değil; runtime env veya BuildKit `--secret`).
5. Etiket = git SHA (`latest` dağıtımda kullanılmaz); taban imajı sürümle sabitle.

## .dockerignore

```
.git
node_modules
.next
dist
target
__pycache__
.venv
.env*
*.log
coverage
```

## Python (uv)

```dockerfile
FROM python:3.13-slim AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev --no-install-project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

FROM python:3.13-slim
RUN useradd -r -u 10001 app
WORKDIR /app
COPY --from=build --chown=app /app /app
ENV PATH="/app/.venv/bin:$PATH"
USER app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```
(uv imaj etiketini de belirli bir sürüme sabitle.)

## Go

```dockerfile
FROM golang:1.23 AS build
WORKDIR /src
COPY go.mod go.sum ./
RUN --mount=type=cache,target=/go/pkg/mod go mod download
COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build CGO_ENABLED=0 go build -ldflags="-s -w" -o /out/api ./cmd/api

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=build /out/api /api
EXPOSE 8080
ENTRYPOINT ["/api"]
```

## Node / Next.js

Next için standalone kalıbı `sky-deploy`'da. Genel Node servisi:
```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
RUN corepack enable
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store pnpm install --frozen-lockfile

FROM deps AS build
COPY . .
RUN pnpm build && pnpm prune --prod

FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build --chown=node /app/node_modules ./node_modules
COPY --from=build --chown=node /app/dist ./dist
USER node
CMD ["node", "dist/index.js"]
```

## Rust / Java

- Rust: `cargo-chef` ile bağımlılık katmanı (`chef prepare` → `chef cook --release` → `cargo build --release`), son imaj `distroless/cc`.
- Java: Spring Boot katmanlı jar (`java -Djarmode=tools -jar app.jar extract --layers`) veya `spring-boot:build-image`; `eclipse-temurin:21-jre` son imaj.

## Healthcheck ve sinyaller

- `HEALTHCHECK CMD wget -qO- http://localhost:8080/health || exit 1` (distroless'ta curl/wget yok → orkestratörün sağlık kontrolünü kullan veya uygulamaya `/healthcheck` alt komutu ekle).
- `CMD ["node", "dist/index.js"]` (exec biçimi) → SIGTERM sürece ulaşır; shell biçimi (`CMD node …`) sinyali yutar.
- PID 1 sorunları için `--init` veya `tini`.

## Yerel geliştirme: compose

```yaml
services:
  db:
    image: postgres:16
    environment: { POSTGRES_PASSWORD: dev, POSTGRES_DB: app }
    ports: ["5432:5432"]
    volumes: [pgdata:/var/lib/postgresql/data]
    healthcheck: { test: ["CMD-SHELL", "pg_isready -U postgres"], interval: 5s, retries: 10 }
  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]
  mail:
    image: axllent/mailpit          # gönderilen e-postaları http://localhost:8025'te gör — çok sevilen
    ports: ["1025:1025", "8025:8025"]
  storage:
    image: minio/minio              # S3 uyumlu yerel depolama
    command: server /data --console-address ":9001"
    ports: ["9000:9000", "9001:9001"]
  api:
    build: .
    env_file: .env
    depends_on: { db: { condition: service_healthy } }
    develop:
      watch:
        - { action: sync, path: ./src, target: /app/src }
        - { action: rebuild, path: package.json }
volumes: { pgdata: {} }
```
`docker compose up --watch` ile kaynak değişince otomatik senkron/yeniden build.

## Boyut ve güvenlik

- `docker image ls` / `dive` ile katman analizi; slim/alpine/distroless taban.
- Tarama: `docker scout cves`, Trivy (`trivy image app:sha`) — CI'da yüksek/kritik açıkta başarısız.
- `--platform linux/amd64,linux/arm64` (buildx) Apple Silicon + sunucu uyumu için.

## Sık hatalar

| Belirti | Sebep |
|---|---|
| Her build tüm bağımlılıkları yeniden kuruyor | kaynak kodu bağımlılıktan önce kopyalanmış |
| Konteyner `docker stop`'ta 10 sn bekliyor | shell biçimi CMD, sinyal sürece ulaşmıyor |
| `localhost` ile DB'ye bağlanamıyor | konteyner içinde servis adı kullan (`db:5432`) |
| Apple Silicon'da çalışan imaj sunucuda çöküyor | mimari farkı → buildx çoklu platform |
| İmaj 1GB+ | tek aşama, dev bağımlılıkları, build önbelleği imajda |
