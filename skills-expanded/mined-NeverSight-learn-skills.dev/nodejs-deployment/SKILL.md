---
name: nodejs-deployment
description: "Despliegue y operaciones de aplicaciones Node.js. Cubre Docker multi-stage, PM2, CI/CD con GitHub Actions, logging con pino, OpenTelemetry tracing, health checks, graceful shutdown, y gestión de secretos. Actívala al preparar una app para producción, configurar CI/CD, o monitorear servicios."
disable-model-invocation: true
---

# Node.js Deployment & Operations

Guía de despliegue y operaciones para Node.js. Enfoque en producción: contenedores, logging, monitoreo, graceful shutdown.

---

## Docker — Multi-stage build

```dockerfile
# Dockerfile.prod
# Stage 1: Build
FROM node:24-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
# Si usas TS, compilar aquí
COPY tsconfig.json ./
COPY src/ src/
RUN npx tsgo --outDir dist

# Stage 2: Production
FROM node:24-alpine AS production
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
USER app

COPY --from=build /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
COPY package.json ./

ENV NODE_ENV=production
ENV PORT=3000
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"]
```

### Docker Compose dev + DB

```yaml
# docker-compose.yml
services:
  app:
    build: .
    ports:
      - "3000:3000"
    env_file: .env
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./src:/app/src  # Hot reload en dev

  postgres:
    image: postgres:18-alpine
    environment:
      POSTGRES_DB: miapp
      POSTGRES_USER: app_user
      POSTGRES_PASSWORD: dev_pass
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app_user -d miapp"]
      interval: 5s
```

---

## PM2 — Process Manager

```bash
npm install -g pm2

# Arrancar con PM2
pm2 start dist/index.js --name miapp-api -i max
# -i max: tantos workers como CPUs

# Config desde archivo
# ecosystem.config.cjs
module.exports = {
  apps: [{
    name: 'miapp-api',
    script: './dist/index.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: { NODE_ENV: 'production', PORT: 3000 },
    max_memory_restart: '512M',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    error_file: '/var/log/miapp/error.log',
    out_file: '/var/log/miapp/out.log',
  }],
};

# pm2 start ecosystem.config.cjs
# pm2 save      # Guarda para auto-restart al reiniciar el SO
# pm2 startup   # Configura auto-start en systemd
```

---

## Logging — Pino

```typescript
import pino from 'pino';

const logger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  transport: process.env.NODE_ENV !== 'production'
    ? { target: 'pino-pretty', options: { colorize: true } }
    : undefined,
  // En producción: JSON a stdout para ELK/Datadog
  redact: ['req.headers.authorization', 'req.headers.cookie'],
  serializers: {
    req: (req) => ({
      method: req.method,
      url: req.url,
      headers: { 'x-request-id': req.headers['x-request-id'] },
    }),
    res: (res) => ({ statusCode: res.statusCode }),
  },
});

// Uso estructurado (nunca interpolación)
logger.info({ orderId, customerId }, 'Order created');
logger.error({ err, orderId }, 'Failed to create order');

// Child logger con contexto
const orderLogger = logger.child({ module: 'orders' });
orderLogger.info('Processing batch');

// Request logging (Express)
import pinoHttp from 'pino-http';
app.use(pinoHttp({ logger }));
```

---

## Graceful Shutdown

```typescript
import { createTerminus } from '@godaddy/terminus';

function beforeShutdown() {
  logger.info('Server shutting down...');
  return new Promise(resolve => setTimeout(resolve, 5000)); // 5s grace
}

function onSignal() {
  logger.info('Signal received, draining connections...');
  // Cerrar pool de DB, conexiones Redis, etc.
}

function onShutdown() {
  logger.info('Cleanup complete, process exiting');
}

createTerminus(server, {
  signal: 'SIGTERM',
  timeout: 10_000,          // Máximo 10s para shutdown
  healthChecks: {
    '/health': () => ({ status: 'ok' }),
    '/health/ready': async () => {
      await db.$queryRaw`SELECT 1`; // Verify DB connection
      return { status: 'ok', db: 'connected' };
    },
  },
  beforeShutdown,
  onSignal,
  onShutdown,
  logger: (msg, err) => logger.error({ err }, msg),
});
```

---

## Health Checks

```typescript
// Liveness: ¿el proceso está vivo?
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', uptime: process.uptime() });
});

// Readiness: ¿puedo recibir tráfico?
app.get('/health/ready', async (_req, res) => {
  try {
    await db.$queryRaw`SELECT 1`;
    await redis.ping();
    res.json({ status: 'ok', db: 'connected', redis: 'connected' });
  } catch {
    res.status(503).json({ status: 'degraded' });
  }
});
```

---

## CI/CD — GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:18-alpine
        env:
          POSTGRES_DB: test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports: [5432:5432]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '24' }
      - run: npm ci
      - run: npm run typecheck
      - run: npm run lint
      - run: npm test -- --coverage
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t ghcr.io/mi-org/miapp:${{ github.sha }} -f Dockerfile.prod .
      - name: Push to registry
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker push ghcr.io/mi-org/miapp:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # SSH o kubectl o actualizar service
          echo "Deploying ${{ github.sha }}"
```

---

## OpenTelemetry Tracing

```typescript
import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http';
import { ExpressInstrumentation } from '@opentelemetry/instrumentation-express';
import { PgInstrumentation } from '@opentelemetry/instrumentation-pg';

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
    new PgInstrumentation(),
  ],
});

sdk.start();

// Al shutdown:
process.on('SIGTERM', async () => {
  await sdk.shutdown();
  process.exit(0);
});
```

---

## Checklist de deployment

- [ ] Docker multi-stage build (separar build de runtime)
- [ ] PM2 con `-i max` para multi-core en servidor único
- [ ] Health checks `/health` (liveness) y `/health/ready` (readiness)
- [ ] Graceful shutdown: drenar conexiones, cerrar DB pool, timeout máximo
- [ ] Pino logger configurado (pretty en dev, JSON en prod)
- [ ] CI/CD: typecheck → lint → test → build Docker → deploy
- [ ] Secrets: variables de entorno, nunca en código ni Dockerfile
- [ ] Node.js corriendo como usuario no-root
- [ ] `NODE_ENV=production` en producción
- [ ] OpenTelemetry tracing para requests y DB queries
- [ ] `npm ci` en CI (no `npm install` — respeta lockfile)
