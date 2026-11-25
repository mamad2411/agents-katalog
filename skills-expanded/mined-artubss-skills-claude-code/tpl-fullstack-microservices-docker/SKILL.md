---
name: tpl-fullstack-microservices-docker
description: Template do pack (fullstack/03-microservices-docker.md). Orienta o agente em stacks fullstack e arquitetura ponta a ponta alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: fullstack/03-microservices-docker.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Microservices Architecture (Docker Compose)

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `fullstack/03-microservices-docker.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Orchestration:** Docker Compose v3.9
- **Services:** Node.js 22 + TypeScript per service
- **Queues:** BullMQ + Redis 7
- **API Gateway:** nginx (upstream routing)
- **Database:** PostgreSQL 16 (one per service — DB per service pattern)
- **Auth service:** Shared JWT validation (JWKS endpoint)
- **Tracing:** OpenTelemetry SDK + correlation IDs
- **Testing:** Vitest (unit), Docker Compose (integration)

---

## PROJECT STRUCTURE
```
services/
├── gateway/                     # nginx config + docker
├── auth-service/                # JWT issuance, user identity
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── user-service/                # User profiles, preferences
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── post-service/                # Posts CRUD
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── notification-service/        # Email/push via BullMQ consumer
    ├── src/
    ├── Dockerfile
    └── package.json
shared/
├── types/                       # Shared TypeScript interfaces
└── events/                      # Event schema definitions
docker-compose.yml
docker-compose.override.yml      # Dev overrides (volumes, ports)
docker-compose.prod.yml
.env.example
```

---

## ARCHITECTURE RULES
1. **Database per service** — each service owns its PostgreSQL schema; no shared DB access.
2. **Async events for cross-service side effects** — use BullMQ for email, notifications, analytics; never synchronous HTTP chains.
3. **Correlation ID on every request** — gateway injects `X-Correlation-ID`; all services propagate it in every log and outgoing request.
4. **Services communicate via HTTP or events only** — no shared memory, no shared filesystem mounts.
5. **Health check endpoint required** — every service exposes `GET /health` returning `{ status: 'ok', version, db: 'connected' }`.
6. **Environment parity** — prod uses identical Dockerfile to dev; only env vars differ.
7. **Secrets via environment variables** — never bake secrets into images; use `.env` (dev) or Docker Secrets/Vault (prod).

---

## DOCKER COMPOSE CONFIGURATION

```yaml
# docker-compose.yml
version: '3.9'

x-service-defaults: &service-defaults
  restart: unless-stopped
  networks: [app-net]
  logging:
    driver: json-file
    options: { max-size: "10m", max-file: "3" }

services:
  gateway:
    <<: *service-defaults
    image: nginx:1.25-alpine
    ports: ["80:80"]
    volumes: ["./services/gateway/nginx.conf:/etc/nginx/nginx.conf:ro"]
    depends_on: [auth-service, user-service, post-service]

  auth-service:
    <<: *service-defaults
    build: { context: ./services/auth-service, target: production }
    environment:
      DATABASE_URL: postgres://auth:secret@auth-db:5432/auth
      JWT_SECRET:   ${JWT_SECRET}
      REDIS_URL:    redis://redis:6379
    depends_on: { auth-db: { condition: service_healthy }, redis: { condition: service_healthy } }
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3001/health"]
      interval: 10s
      timeout: 5s
      retries: 3

  auth-db:
    image: postgres:16-alpine
    environment: { POSTGRES_USER: auth, POSTGRES_PASSWORD: secret, POSTGRES_DB: auth }
    volumes: [auth-db-data:/var/lib/postgresql/data]
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U auth"]
      interval: 5s

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
    volumes: [redis-data:/data]

  notification-service:
    <<: *service-defaults
    build: { context: ./services/notification-service, target: production }
    environment:
      REDIS_URL:   redis://redis:6379
      SMTP_HOST:   ${SMTP_HOST}
    depends_on: { redis: { condition: service_healthy } }

networks:
  app-net:

volumes:
  auth-db-data:
  redis-data:
```

---

## CORRELATION ID PROPAGATION

```typescript
// shared/middleware/correlation.ts
import { randomUUID } from 'node:crypto'
import type { Request, Response, NextFunction } from 'express'

export const CORRELATION_HEADER = 'x-correlation-id'

export function correlationMiddleware(req: Request, res: Response, next: NextFunction): void {
  const correlationId = (req.headers[CORRELATION_HEADER] as string) ?? randomUUID()
  req.correlationId = correlationId
  res.setHeader(CORRELATION_HEADER, correlationId)
  next()
}

// Outgoing HTTP call — propagate correlation ID
export function makeRequest(
  url: string,
  init: RequestInit,
  correlationId: string,
): Promise<Response> {
  return fetch(url, {
    ...init,
    headers: { ...init.headers, [CORRELATION_HEADER]: correlationId },
  })
}

declare global { namespace Express { interface Request { correlationId: string } } }
```

---

## BULLMQ EVENT-DRIVEN PATTERN

```typescript
// shared/events/index.ts
export type AppEvent =
  | { type: 'USER_CREATED'; payload: { userId: string; email: string; name: string } }
  | { type: 'POST_PUBLISHED'; payload: { postId: string; authorId: string; title: string } }

// services/user-service/src/producers/user.ts
import { Queue } from 'bullmq'
import Redis     from 'ioredis'
import type { AppEvent } from '../../../shared/events'

const connection = new Redis(process.env.REDIS_URL!, { maxRetriesPerRequest: null })
const eventQueue = new Queue<AppEvent>('app-events', { connection })

export async function emitUserCreated(userId: string, email: string, name: string): Promise<void> {
  await eventQueue.add('USER_CREATED', {
    type: 'USER_CREATED',
    payload: { userId, email, name },
  }, { attempts: 3, backoff: { type: 'exponential', delay: 1000 } })
}

// services/notification-service/src/consumers/events.ts
import { Worker } from 'bullmq'
import Redis      from 'ioredis'
import type { AppEvent } from '../../../shared/events'

const connection = new Redis(process.env.REDIS_URL!, { maxRetriesPerRequest: null })

new Worker<AppEvent>('app-events', async (job) => {
  const { type, payload } = job.data
  if (type === 'USER_CREATED') {
    await sendWelcomeEmail(payload.email, payload.name)
  }
}, { connection, concurrency: 5 })
```

---

## NGINX GATEWAY

```nginx
# services/gateway/nginx.conf
upstream auth    { server auth-service:3001; }
upstream users   { server user-service:3002; }
upstream posts   { server post-service:3003; }

server {
  listen 80;
  add_header X-Request-ID $request_id always;

  location /api/auth/   { proxy_pass http://auth/; proxy_set_header X-Correlation-ID $request_id; }
  location /api/users/  { proxy_pass http://users/; proxy_set_header X-Correlation-ID $request_id; }
  location /api/posts/  { proxy_pass http://posts/; proxy_set_header X-Correlation-ID $request_id; }
  location /health      { return 200 '{"status":"ok"}'; add_header Content-Type application/json; }
}
```

---

## ROUTING TABLE

| Method | Path (gateway) | Target Service | Action |
|--------|---------------|----------------|--------|
| POST | /api/auth/login | auth-service | Issue JWT |
| POST | /api/auth/register | auth-service | Register user |
| GET | /api/users/:id | user-service | Get profile |
| PUT | /api/users/:id | user-service | Update profile |
| GET | /api/posts | post-service | List posts |
| POST | /api/posts | post-service | Create post |
| DELETE | /api/posts/:id | post-service | Delete post |
| GET | /health | nginx local | Gateway health |
| BullMQ | USER_CREATED | notification-service | Send welcome email |
| BullMQ | POST_PUBLISHED | notification-service | Notify followers |

---

## QUALITY GATES
- [ ] `docker compose up --build` — all services healthy
- [ ] All `GET /health` endpoints return `{ status: 'ok' }` with HTTP 200
- [ ] Correlation IDs appear in logs for every request across services
- [ ] BullMQ workers restart automatically on crash (Docker `restart: unless-stopped`)
- [ ] No service accesses another service's PostgreSQL database
- [ ] `docker compose down -v && docker compose up` — clean state works
- [ ] Secrets in `.env.example` marked clearly (never real values committed)
- [ ] `vitest run` passes all unit tests per service

---

## FORBIDDEN
- ❌ Shared database between services — strict DB-per-service
- ❌ Synchronous HTTP chain A→B→C→D — use events for side effects
- ❌ Hardcoded IPs/hostnames — use Docker service names
- ❌ Root user in Dockerfiles — always `USER node` or `USER 1001`
- ❌ `latest` Docker image tags in production compose files — pin versions
- ❌ Missing healthchecks — every service must have one
- ❌ `console.log` without correlation ID context
- ❌ Fire-and-forget BullMQ jobs without error handling / deadletter queue
