# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Development
pnpm dev              # API + Web simultaneously
pnpm dev:api          # API only (gateway + all services via serverless-offline)
pnpm dev:web          # Web only (Next.js on :3000 with Turbopack)
pnpm dev:desktop      # Electron desktop app
pnpm dev:mobile       # Expo mobile app

# Build / Quality
pnpm build            # Build all (via Turbo)
pnpm lint             # Lint all (via Turbo)
pnpm typecheck        # Type-check all (via Turbo)
pnpm format           # Format all (Biome)
pnpm check            # Biome check (lint + format)

# Tests (Vitest — @scaffold/api e @scaffold/desktop)
pnpm test                                    # Run all tests
pnpm --filter @scaffold/api test                  # API tests only
pnpm --filter @scaffold/desktop test                  # App tests only
pnpm --filter @scaffold/api test:watch            # Watch mode
pnpm --filter @scaffold/api exec vitest run path  # Single test file

# Targeting a specific workspace
pnpm --filter @scaffold/web <script>
pnpm --filter @scaffold/api <script>
```

## Architecture

Monorepo TypeScript (pnpm workspaces + Turbo) with quatro apps:

### `apps/api/` — Serverless Microservices (AWS Lambda)

Cada microservice vive em `apps/api/services/<name>/` com seu proprio `serverless.ts` e port. Core libs compartilhados em `apps/api/core/`:

- **`core/apis/`** (`scaffold.core.apis`) — Tipos de response (`Success`, `Created`, `NoContent`, `NotValid`, `NotFound`, etc.), middleware (`json-serializer`, `error-handler`), tipo `JsonProxyEvent`
- **`core/aws/`** (`scaffold.core.aws`) — `createApiHandler` (wrapper Lambda que parseia body, injeta auth, serializa response) e `createServerlessConfig` (factory de config Serverless Framework)
- **`core/errors/`** (`scaffold.core.errors`) — `DomainError` com kinds (`NOT_FOUND`, `VALIDATION`, `CONFLICT`, etc.) e `createDomainError`
- **`gateway/`** — Express proxy local (:8080) que roteia para cada service por prefix (ex: `/health` -> `:3005`)

**Padrao para novo service:**
1. Criar `apps/api/services/<name>/` com `package.json` (deps: `scaffold.core.apis`, `scaffold.core.aws`, `scaffold.core.errors`), `serverless.ts` (usando `createServerlessConfig`), e handlers em `handlers/http/<action>/handler.ts`
2. Handler retorna `ApiResponse` (Success, Created, etc.) — nunca retorna raw HTTP
3. Registrar rota no gateway (`apps/api/gateway/server.ts`) com port do service
4. O port do service e definido em `serverless.ts` via `custom.serverless-offline.httpPort`

### `apps/web/` — Next.js 15 (App Router, React 19, Tailwind CSS 4)

Roda em `:3000`, faz proxy de `/api/*` para o gateway (`:8080`) via `next.config.ts` rewrites.

### `apps/desktop/` — Electron + React + Tailwind + ShadcnUI

Desktop app com Vite + `vite-plugin-electron/simple`. React 18, Tailwind CSS 3, ShadcnUI (style: new-york). Testes com Vitest + Happy DOM + Testing Library. Estrutura: `electron/` (main + preload) e `src/` (React renderer). Path alias `@/` aponta para `src/`. Build desktop via `pnpm --filter @scaffold/desktop build:desktop`.

### `apps/mobile/` — Expo (React Native, NativeWind)

App mobile com Expo Router e Tailwind via NativeWind.

### `packages/typescript-config/` — Configs TS compartilhados

## Code Style (Biome)

- 2 spaces, 80 chars, single quotes, sem semicolons, sem trailing commas
- `useConst`, `noVar` em TypeScript
- `noCommonJs` (exceto configs: babel, metro, tailwind, serverless)
- `noExplicitAny`: warn
- Imports organizados automaticamente via Biome assist

## Conventions

- **Commits**: Conventional Commits (enforced via commitlint + Husky)
- **Node**: >=22 (`.nvmrc`: 22.19.0)
- **Package manager**: pnpm 10.33.0
- **Workspace packages API**: nomeados como `scaffold.core.<module>` ou `scaffold.service.<name>`
- **Linguagem do app**: pt-BR (metadata, UI)
