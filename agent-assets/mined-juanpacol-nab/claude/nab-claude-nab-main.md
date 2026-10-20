# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Nab — plataforma de automatización de búsqueda de empleo con IA (agrega vacantes, genera CVs/cartas personalizados, permite aplicar con swipe, dashboard de seguimiento, monetización por créditos vía Stripe). Monorepo Turborepo + pnpm, TypeScript en todo el stack.

```
apps/
  web/       Next.js 15 (App Router) — landing + dashboard
  api/       NestJS — REST + WebSocket, produce jobs a las colas
  workers/   NestJS standalone — consume colas BullMQ (ingesta, IA, embeddings, email)
  mobile/    Expo/React Native (Expo Router) — feed swipe, coach, tracking, push
packages/
  ui/        Design system (Button/Card/Badge/StatusPill, cva + Tailwind)
  database/  Prisma schema + cliente + seeds (Postgres 16 + pgvector)
  shared/    Zod schemas, tipos, constantes compartidas (incluye QUEUE_NAMES, CREDIT_COSTS)
  config/    tsconfig / eslint / tailwind compartidos
```

## Commands

```bash
pnpm install                        # instalar todo el monorepo
pnpm docker:dev                     # levanta Postgres/Redis/MinIO/Mailpit (docker-compose.dev.yml)
pnpm db:generate && pnpm db:migrate && pnpm db:seed   # cliente Prisma + migraciones + datos demo
pnpm dev                            # todas las apps en watch mode (turbo)

pnpm build / pnpm lint / pnpm typecheck / pnpm test   # en todo el monorepo (turbo run <task>)
pnpm --filter @nab/api <script>     # limitar a un paquete (@nab/api, @nab/workers, web, @nab/mobile, @nab/database, @nab/shared, @nab/ui)
```

**Tests** son Vitest, sin archivo de config (usa las convenciones por defecto `*.spec.ts`). Para correr un solo archivo o un solo test:
```bash
pnpm --filter @nab/api exec vitest run src/modules/billing/credits.service.spec.ts
pnpm --filter @nab/api exec vitest run -t "nombre del test"
pnpm --filter @nab/workers exec vitest run src/adapters/adapters.spec.ts
```
Solo `@nab/api` y `@nab/workers` tienen tests; `web` y `@nab/mobile` no (sin infra de test configurada). Los tests mockean Prisma con un cliente fake hecho a mano (`vi.fn()` sobre un `Map` en memoria, no una DB real) — ver cualquier `*.service.spec.ts` como plantilla.

**Prisma**: `pnpm db:migrate` corre `prisma migrate deploy` (producción); `pnpm --filter @nab/database migrate:dev` para crear una migración nueva en desarrollo. `pnpm --filter @nab/database studio` abre Prisma Studio.

**Docker Compose completo** (todas las apps + infra, para probar el stack como en producción): `pnpm docker:up` (`docker-compose.yml`). Para producción real: `docker-compose.prod.yml` (sin `web`, que va a Vercel; usa imágenes de GHCR en vez de `build:`).

## Architecture

### Flujo de datos y colas

`apps/api` es el único punto de entrada HTTP/WebSocket para los clientes (web/mobile). No corre workers de BullMQ, solo **produce** jobs (`apps/api/src/queues/`, vía `@nestjs/bullmq` `BullModule.registerQueue`). `apps/workers` es un proceso NestJS standalone separado que **consume** esas colas (`apps/workers/src/processors/*.ts`) y no expone HTTP de negocio (sí un health-server HTTP mínimo, ver más abajo).

Colas (`QUEUE_NAMES` en `packages/shared/src/constants.ts`): `job-ingest`, `embeddings`, `ai-generation`, `email`. Todos los productores (api y workers) configuran `defaultJobOptions` con `attempts: 3` + backoff exponencial + límites de retención (`removeOnComplete`/`removeOnFail`) — importante porque en el despliegue gratuito Redis vive en Upstash con cuota de comandos/memoria limitada.

### Créditos (lógica de dinero — el código más sensible del repo)

`CreditLedger` es la fuente de verdad (append-only, `@@unique([userId, reason, refId])` para idempotencia ante reintentos de webhooks de Stripe); `User.creditsRemaining` es un caché denormalizado que se actualiza en la misma operación que el asiento del ledger. Ver `apps/api/src/modules/billing/credits.service.ts`:
- `consume()`/`grant()` abren su propia transacción.
- `consumeWithClient(tx, ...)` existe para que **otro servicio** (ej. `ApplicationsService.apply()`) pueda cobrar crédito dentro de SU PROPIA transacción, para que "marcar la Application como enviada" y "cobrar el crédito" confirmen o reviertan juntos.
- El chequeo de saldo va DENTRO del `UPDATE` (`user.updateMany({ where: { creditsRemaining: { gte: amount } } })`), no en un `SELECT` previo separado — así Postgres serializa gastos concurrentes del mismo usuario sin dejar el saldo negativo.

Cualquier flujo nuevo que cobre créditos debe seguir este patrón (transacción compartida con `consumeWithClient`, nunca upsert-de-negocio-luego-cobro-aparte).

### Modo mock explícito (nunca silencioso)

`apps/api/src/config/env.validation.ts` y `apps/workers/src/env.validation.ts` validan el entorno al arrancar (Zod) y **fallan rápido** en producción si faltan secretos — no hay fallbacks hardcodeados. Los mocks de IA (`AiService` en api, `apps/workers/src/ai.ts`), embeddings (`apps/workers/src/embeddings.ts`) e ingesta (`apps/workers/src/adapters/`) solo se activan si falta la clave real **y** se declaró explícitamente `AI_MOCK=true` / `INGEST_MOCK=true`; sin el flag, el arranque en producción falla con un mensaje claro en vez de correr en modo demo sin avisar. En desarrollo, sin clave, corren en mock automáticamente.

### Ingesta de vacantes

`apps/workers/src/adapters/index.ts` → `buildAdapters()` arma la lista de adapters según qué env vars estén presentes (`GREENHOUSE_BOARDS`, `LEVER_BOARDS`, `ADZUNA_APP_ID`+`ADZUNA_APP_KEY`, `JSEARCH_RAPIDAPI_KEY`); si no hay ninguna, cae a `MockAdapter`. Cada adapter implementa `JobAdapter.fetchJobs()` y **nunca lanza** (captura sus propios errores y devuelve `[]`, con `AbortSignal.timeout(10_000)` en cada fetch). `ingest.processor.ts` hace upsert por `@@unique([source, externalId])` (idempotente) y desactiva (`isActive: false`) vacantes no vistas en la corrida solo para las fuentes que sí devolvieron resultados esa vez, para que un adapter caído no desactive todo su catálogo.

### IA (Claude)

`AiService` (api) y `apps/workers/src/ai.ts` son paralelos e independientes (no comparten código, cada proceso instancia su propio cliente `Anthropic` con `timeout: 60_000, maxRetries: 2`). Modelos configurables vía `AI_MODEL_FAST`/`AI_MODEL_GENERATION` (default `claude-haiku-4-5` / `claude-sonnet-5`). Generación de CV usa un segundo paso de verificación (`verifyResume`) que le pide a Claude marcar bullets no respaldados por el perfil real y los elimina — patrón anti-alucinación, no confiar ciegamente en la primera respuesta para contenido que se presenta como hechos del usuario.

`ChatService` (api) implementa tool-use de Claude para el chat de soporte/coach — el bucle de ejecución de herramientas vive ahí, `AiService.chatComplete()` es solo la primitiva de bajo nivel (una llamada, devuelve texto + tool_uses).

### Storage

`StorageService` (api) usa un cliente `@aws-sdk/client-s3` genérico (`S3_ENDPOINT`/`S3_REGION`/`S3_FORCE_PATH_STYLE`/`S3_ACCESS_KEY`/`S3_SECRET_KEY`/`S3_BUCKET`) — el mismo código sirve para MinIO (dev), Cloudflare R2 o Supabase Storage (prod) sin cambios, solo variando env vars.

### Realtime

`RealtimeGateway` (api, namespace `/realtime`) autentica el socket con el mismo JWT que la API REST y une a cada cliente a una sala privada `user:{userId}`. Web y mobile comparten el mismo gateway (`apps/mobile/src/lib/socket.ts` usa `socket.io-client`).

### Auth

JWT access + refresh con rotación (el refresh viejo se invalida al usarse, hasheado en DB). Ver `apps/api/src/modules/auth/token.service.ts`.

### Despliegue

Dos rutas documentadas en `docs/DEPLOY.md`:
- **Ruta A (gratis)**: Vercel (web) + Supabase (Postgres+Storage) + Upstash (Redis) + Render free tier (api + workers). `render.yaml` es el Blueprint. Render free solo permite "web services" (no workers dedicados) y duerme sin tráfico HTTP — por eso `apps/workers/src/health-server.ts` expone un HTTP mínimo (puerto 4100) solo para que un ping externo lo mantenga despierto; no sirve tráfico de negocio.
- **Ruta B (VPS, ~€6/mes)**: todo el backend en Docker Compose propio + Caddy (TLS automático), `docker-compose.prod.yml`, CD vía GHCR + `scripts/deploy.sh`.

Gotchas de Docker ya resueltos (ver comentarios en los Dockerfiles si reaparece algo similar): Next.js standalone necesita `ENV HOSTNAME="0.0.0.0"` explícito o se bindea a la IP del contenedor; healthchecks con `wget http://localhost:PORT` pueden fallar por resolver `::1` antes que `0.0.0.0` (usar `127.0.0.1` explícito); el stage `runner` de los Dockerfiles necesita `package.json`/`pnpm-workspace.yaml`/`pnpm-lock.yaml` copiados para que corepack resuelva la versión de pnpm pineada; las dependencias directas de cada app viven como symlinks en `apps/<app>/node_modules` además del `node_modules` raíz (pnpm workspaces) — hay que copiar ambos en el stage final.
