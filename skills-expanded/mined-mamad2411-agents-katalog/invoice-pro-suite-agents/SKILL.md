# AGENTS.md

Guidance for agents working in this repository. Keep changes focused, verify with build/lint after edits, and prefer the smallest fix that restores the intended behavior.

## At a Glance

This is a React 18 + TypeScript + Vite application for Circle Pair and Circle Phone service/sales workflows. The UI is local-state-driven, while persistence now lives in PostgreSQL via Vercel Edge API routes and Neon.

## How The App Runs

### Local Development

Use Node 24.

```bash
nvm use v24
npm run dev
```

`npm run dev` launches two local processes:

- Vite frontend on `http://localhost:8081`
- Custom API proxy on `http://localhost:3000`

The proxy server is `scripts/dev-server.ts`. It loads handlers from `api/` and forwards non-API traffic to Vite. During local development, the frontend should point `VITE_API_URL` to `http://localhost:3000`.

Useful local commands:

- `npm run dev:frontend` for Vite only
- `npm run dev:api` for the API proxy only
- `npm run build` for production bundle validation
- `npm run lint` for static checks
- `npm run test` for the Vitest suite

### Vercel Deployment

`vercel.json` builds with `npm run build`, publishes `dist`, and rewrites `/api/*` to the Edge handlers in `api/`.

Important Vercel constraints:

- API files under `api/` run as Edge Functions.
- Do not rely on Node-only modules at the top level of Edge handlers.
- Use Neon-compatible queries and `sql.query(...)` when you need placeholder parameters.
- Keep route imports extension-safe for the Vercel TypeScript/Esm build.

Production behavior should be same-origin for the frontend and API. No separate API host is required in Vercel.

## Database Migration

The project uses PostgreSQL, typically Neon in production and optionally local PostgreSQL in development.

Environment files are loaded in this order for migration scripts:

1. `.env`
2. `.env.local` overrides `.env` when present

Primary migration command:

```bash
npm run migrate
```

That script:

- reads `DATABASE_URL`
- connects with `pg`
- runs `schema.sql`
- creates the full database structure for users, Circle Pair, Circle Phone, trade-ins, service history, and company profiles

If you need to migrate exported browser data into PostgreSQL, use:

```bash
npm run migrate:localstorage
```

That script expects a `localStorage-export.json` file and moves the exported app data into the database.

Local example connection string:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/circlephone_db
```

For Neon, set `DATABASE_URL` to the provided Neon connection string in both local env and Vercel environment variables.

## Project Flow

### Main Routes

`src/App.tsx` wires these screens:

- `/` Dashboard
- `/invoice/new` Circle Pair invoice editor
- `/invoice/:id` Circle Pair invoice editor for existing records
- `/phone/new` Circle Phone editor
- `/phone/:id` Circle Phone editor for existing records
- `/settings` Company and app settings

### Data Flow

1. The page loads data through `src/lib/storage-api.ts`.
2. The storage layer maps app models to API payloads and back.
3. API calls go to `src/lib/api-client.ts`, which chooses the correct base URL.
4. The API handlers under `api/` read and write PostgreSQL.
5. The UI updates after mutations by reloading the relevant collection.

### Domain Split

- Circle Pair covers service invoices, items, signatures, and service history.
- Circle Phone covers sales invoices and trade-in data.
- Users are shared across both flows and are used for customer lookup/stats.

### Business Rules To Preserve

- Invoice numbers use the project-specific formatted sequence.
- Totals are rounded to integers.
- Tax is applied after discounts.
- Trade-in data must be persisted and rehydrated for Circle Phone.
- Signatures and warranty notes must survive save/reload.
- Print and preview output should remain invoice-focused.

## Code Areas To Touch Carefully

- `src/lib/storage-api.ts` for persistence mapping
- `src/lib/api-client.ts` for API base URL behavior
- `api/*.ts` for Vercel Edge handlers
- `src/components/InvoicePreview.tsx` for printable output
- `src/pages/PhoneEditor.tsx` and `src/pages/InvoiceEditor.tsx` for form behavior
- `schema.sql` and migration scripts for database structure

## Testing And Validation

After any non-trivial change, validate with:

```bash
npm run build
```

If the change touches API or persistence logic, also validate the relevant workflow in the browser or against the local API proxy.

## Existing Conventions

- Use `@` as the alias for `./src`
- Preserve shadcn/ui components under `src/components/ui/`
- Avoid rewriting unrelated code or formatting large files unnecessarily
- Prefer data mapping fixes over UI workarounds when persistence breaks
