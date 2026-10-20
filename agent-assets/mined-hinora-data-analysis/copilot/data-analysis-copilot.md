# data-analysis Development Guidelines

## Required Reading

Before making changes, read the relevant documentation:

- README: `README.md`
- Project structure: `docs/project-structure.md`
- Type generation: `docs/type-generation.md`
- Testing guide: `docs/testing.md`
- Validation reference: `lib/broker/validation.ts`
- API documentation: `docs/api/api.yaml`
- Domain knowledge: `docs/domain-knowledge/**`

## Active Technologies

- **Runtime:** TypeScript 5.x, Node.js 20 LTS (strict mode)
- **Microservices:** Moleculer 0.14.x with auto-generated type-safe service calls
- **ORM:** TypeORM 0.3.x
- **Database:** PostgreSQL 16+ with pgvector extension for vector embeddings; one database per microservice
- **AI:** Ollama (local) / Google Gemini adapters
- **File Parsing:** pdf-parse (PDF text), tabula-js (PDF tables, requires JRE 8+), xlsx/SheetJS (XLSM), papaparse (CSV)
- **Embeddings:** nomic-embed-text (768-dim via Ollama) or text-embedding-004 (Gemini)
- **Frontend:** Next.js / React / React Query
- **Linting:** Biome

## Project Structure

```text
lib/                          # Shared core library (core.lib)
apps/                         # Microservices organized by domain
  domain.analysis/
    microservice.analysis/    # Sessions, conversations, AI chat
  domain.data/
    microservice.data/        # Upload, datasets, metadata, 16+ tools
  domain.example/
    microservice.example/     # Reference microservice
  domain.platform/
    microservice.proxy/       # API gateway (moleculer-web)
frontend/                     # Next.js frontend
docs/                         # Documentation (source of truth)
  api/api.yaml                # OpenAPI 3.0 spec
  domain-knowledge/           # Feature-specific docs with diagrams
specs/                        # Feature specifications and plans
```

## Workflow Checklist

After implementing changes you **must** do these steps:

1. **Backend only:** Add or update tests for every changed action/event — see `docs/testing.md`.
2. Run tests: `npm test` (or `npx jest path/to/file.test.ts` for a single file).
3. Run `npm run lint:fix` in root (biome). Fix issues and re-run.
4. **Backend only:** Run type generation: `npm run generate:types:all`.
5. **Backend only:** If REST endpoint added → update `docs/api/api.yaml` (OpenAPI).
6. **Backend only:** Add/update domain knowledge docs in `docs/domain-knowledge/*.md`.

## Commands

| Command | Description |
|---------|-------------|
| `npm test` | Run all tests |
| `npm run test:coverage` | Run tests with coverage |
| `npx jest path/to/file.test.ts` | Run a single test file |
| `npm run lint` | Check code with Biome |
| `npm run lint:fix` | Auto-fix lint issues |
| `npm run generate:types:all` | Generate types for all microservices |

## Code Style

- **Single object parameter** for functions (exceptions: simple utils, callbacks)
- **Named imports/exports only** — no default exports, no `import *`
- **Alphabetical ordering** of object properties, interface members, enum values
- **Inline objects** when simple (≤4 props), multi-line when complex
- **No `{Type}` in JSDoc** — TypeScript provides types
- **Parallel async** when operations are independent (`Promise.all`)
- **Custom error classes** with context — no plain `throw new Error()`
- **Strict typing** — no `any`, use `unknown` with type guards
- **UPPER_SNAKE_CASE** for constants
- **camelCase** for functions/variables, **PascalCase** for classes/interfaces/enums

## Backend: Moleculer Rules

- **Unique service names** across all microservices — service name = folder name under `services/`
- **camelCase for service folders** (e.g., `sessionData`, not `session-data`)
- Use `defineAction` for actions, `defineEvent` for events
- External actions have `rest: "..."`, internal actions have no `rest` property
- Use `TypedContext<P>` for public endpoints, `AuthenticatedTypedContext<P>` for protected
- Follow RESTful URL conventions (nouns, not verbs)

## Frontend: Next.js Rules

- React Query hooks for data fetching (`useQuery`/`useMutation`)
- Always destructure mutation hooks
- Never use async/await with mutation callbacks
- Functional components only with TypeScript interfaces for props
- Pass IDs as props, fetch data inside components with React Query
- Components: `PascalCase.tsx`, Hooks: `useHookName.ts`, Pages: `page-name.tsx`

## Testing

- Tests against real PostgreSQL (port 5433 via `postgres-test` container)
- Co-located in `__tests__/` directories next to source files
- Use `defineTest()` helper from `core.lib/testing` for declarative action testing
- Mock db module: `jest.mock("../../../db", () => ({ get dataSource() { return testDs; } }))`
- Import action **after** mock registration
