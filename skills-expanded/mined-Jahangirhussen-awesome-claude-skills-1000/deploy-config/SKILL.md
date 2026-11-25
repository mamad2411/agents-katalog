---
name: deploy-config
description: >
  Trigger when the user wants to configure deployment for their app — Vercel, Railway, Fly.io, Docker, or CI/CD pipelines. Also trigger for environment variable management, health checks, Docker Compose setup, GitHub Actions workflows, or production readiness reviews.
source:
  repository: armaneker/claude-code-skills
  original_path: saas-builder-kit/skills/deploy-config
  original_name: deploy-config
status: canonical
---
# Deploy Config

You are an expert in cloud deployment and DevOps. Generate production-ready deployment configuration for the user's target platform — not just docs summaries but actual working config files.

## Workflow

1. **Identify the target platform(s):**
   - **Vercel** — best for Next.js; zero-config for most setups
   - **Railway** — best for full-stack apps with databases, background workers
   - **Fly.io** — best for long-running servers, websockets, global edge
   - **Docker / Docker Compose** — best for self-hosting, VPS, or custom infra
   - **Multiple** — e.g. frontend on Vercel + backend on Railway

2. **Identify the app type:** Next.js, Express API, full-stack monorepo, etc.

3. **Identify what's needed:**
   - CI/CD pipeline (GitHub Actions)
   - Environment variable management
   - Health check endpoints
   - Database migrations on deploy
   - Secrets management

---

## Vercel

### `vercel.json`
```json
{
  "framework": "nextjs",
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm ci",
  "env": {
    "NODE_ENV": "production"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ],
  "rewrites": [
    { "source": "/health", "destination": "/api/health" }
  ]
}
```

### GitHub Actions for Vercel (`/.github/workflows/deploy.yml`)
```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: ${{ github.ref == 'refs/heads/main' && '--prod' || '' }}
```

---

## Railway

### `railway.toml`
```toml
[build]
builder = "NIXPACKS"
buildCommand = "npm ci && npm run build"

[deploy]
startCommand = "npm start"
healthcheckPath = "/api/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[[services]]
name = "web"
```

### Procfile (alternative)
```
web: node dist/server.js
worker: node dist/worker.js
release: npx prisma migrate deploy
```

The `release` process runs before deploy — use it for DB migrations.

---

## Fly.io

### `fly.toml`
```toml
app = "your-app-name"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "production"
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 1

  [[http_service.checks]]
    grace_period = "10s"
    interval = "30s"
    method = "GET"
    path = "/api/health"
    timeout = "5s"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
```

### Deploy command
```bash
flyctl deploy --remote-only
```

### Secrets management
```bash
flyctl secrets set DATABASE_URL="postgres://..." STRIPE_SECRET_KEY="sk_live_..."
flyctl secrets list
```

---

## Docker

### `Dockerfile` (Node.js multi-stage)
```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && cp -r node_modules prod_node_modules
RUN npm ci

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Runtime
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

# Non-root user
RUN addgroup --system --gid 1001 nodejs && adduser --system --uid 1001 appuser

COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=deps /app/prod_node_modules ./node_modules
COPY package.json ./

USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD wget -qO- http://localhost:8080/api/health || exit 1

CMD ["node", "dist/server.js"]
```

### `.dockerignore`
```
node_modules
.next
dist
.env*
.git
*.log
coverage
```

### `docker-compose.yml` (local dev + staging)
```yaml
version: '3.9'

services:
  app:
    build:
      context: .
      target: runner
    ports:
      - "3000:8080"
    environment:
      - DATABASE_URL=postgres://postgres:password@db:5432/myapp
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

---

## Health Check Endpoint (Always Add)

```typescript
// app/api/health/route.ts (Next.js) or src/routes/health.ts (Express)
export async function GET() {
  // Optional: check DB connection
  try {
    await db.$queryRaw`SELECT 1`;
  } catch {
    return Response.json({ status: 'unhealthy', db: 'down' }, { status: 503 });
  }

  return Response.json({
    status: 'healthy',
    version: process.env.npm_package_version,
    uptime: process.uptime(),
  });
}
```

---

## Database Migration on Deploy

### Prisma
```bash
# In package.json scripts
"migrate:deploy": "prisma migrate deploy"

# In Procfile / Railway / Dockerfile CMD
release: npm run migrate:deploy
```

### Drizzle
```bash
"migrate:deploy": "drizzle-kit migrate"
```

**Never run `db push` in production** — always use `migrate deploy` which applies committed migrations only.

---

## GitHub Actions — Full CI Pipeline

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm test
        env:
          DATABASE_URL: postgres://postgres:test@localhost:5432/testdb

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      # Add your platform-specific deploy step here
```

---

## Environment Variable Checklist

Generate a `.env.example` file with all required vars (no values):

```bash
# App
NODE_ENV=
APP_URL=
PORT=

# Database
DATABASE_URL=

# Auth
AUTH_SECRET=
GITHUB_ID=
GITHUB_SECRET=

# Stripe
STRIPE_SECRET_KEY=
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=

# Email
RESEND_API_KEY=
```

## Common Pitfalls — Avoid These

- **Not running migrations before starting the app** — use `release` commands or init containers
- **Storing secrets in Dockerfile or docker-compose.yml** — use platform secret managers
- **Running containers as root** — always use a non-root user in production Dockerfiles
- **No health check endpoint** — load balancers and orchestrators need `/health` to route traffic correctly
- **`npm install` in production Dockerfile** — use `npm ci` for reproducible installs
- **Large Docker images** — multi-stage builds; never copy `node_modules` from dev stage to prod
- **Missing `.dockerignore`** — `node_modules` and `.git` can add hundreds of MB to build context
- **Hardcoding `NODE_ENV=development`** — always set explicitly in platform env vars
