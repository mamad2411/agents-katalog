---
name: docker-dev-setup
description: Docker Compose and local dev setup for this project (Postgres 17 + Redis 8, dev:setup script). Use when configuring docker-compose.yml, .env.example, package.json dev scripts, or bootstrapping the local development environment.
---

# Docker Dev Setup

## docker-compose.yml

```yaml
services:
  postgres:
    image: postgres:17-alpine
    ports:
      - '5432:5432'
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:8-alpine
    ports:
      - '6379:6379'

volumes:
  postgres_data:
```

## .env.example

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/todo_dev"
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=todo_dev
REDIS_URL="redis://localhost:6379"
```

## dev:setup Script (`package.json`)

```json
"scripts": {
  "dev": "next dev",
  "dev:setup": "docker compose up -d && node scripts/wait-for-db.mjs && pnpm prisma migrate dev && pnpm next dev"
}
```

## wait-for-db.mjs (scripts/)

```js
import { execSync } from 'child_process'

const maxAttempts = 30
let attempt = 0

while (attempt < maxAttempts) {
  try {
    execSync('docker compose exec postgres pg_isready -U postgres', { stdio: 'ignore' })
    console.log('Postgres ready')
    process.exit(0)
  } catch {
    attempt++
    console.log(`Waiting for Postgres... (${attempt}/${maxAttempts})`)
    await new Promise(r => setTimeout(r, 1000))
  }
}

console.error('Postgres did not become ready in time')
process.exit(1)
```

## Rules

- App container is **not** in Docker — `next dev` runs on the host
- Never commit `.env` — only `.env.example`
- Port conflicts: ensure 5432 and 6379 are free before starting
- Redis is session-only for this prototype; no caching logic required
