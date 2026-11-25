# Agent Guidelines

## Code Style

- Use `const` and arrow function syntax (no `function` keyword)
- Use double quotes for strings
- Format with Prettier before committing (`npm run format`)

## Setup

Fastify + TypeScript API with PostgreSQL. Database managed via Docker Compose. Uses Kysely for queries, Zod for validation.

**Key Files:**

- `src/index.ts` - Server entry point
- `src/routes/` - Route definitions (thin layer, delegates to controllers)
- `src/controllers/` - Request handlers with business logic coordination
- `src/repositories/` - Repository pattern for data access (one per table)
- `src/services/` - Business logic services (e.g., shipment.service.ts)
- `src/clients/` - External API clients (implement abstract.client.ts interface)
- `src/config/database.ts` - Kysely database instance
- `src/db/migrations/` - Database migrations
- `src/db/seeds/` - Database seeds

**Local Development:**

- Requires ngrok for webhook testing (Late Logistics callbacks)
- Configure ngrok authtoken once for persistent URLs
- Set `WEBHOOK_BASE_URL` in `.env` to your ngrok URL

**Important:** After any significant change or refactor, check if this file needs updates. Keep it concise.
