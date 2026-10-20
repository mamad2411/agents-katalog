# AGENTS.md: Coding Agent Guide for turbo-payload

## Project Overview

Monorepo: **Next.js + Payload CMS** (web), **Bun server** (API), **React Native/Expo** (mobile).

- **Package manager**: `bun` (v1.3.9): use `bun` for all commands, NOT npm/yarn/pnpm
- **Task runner**: Turborepo (`turbo.json` at root)
- **Workspace roots**: `apps/*`, `packages/*`, `tooling/*`

## Build / Lint / Test Commands

| Task                   | Command                                                              |
| ---------------------- | -------------------------------------------------------------------- |
| Lint (check)           | `bun x biome lint .` or `bun run lint`                               |
| Lint (auto-fix)        | `bun x biome check --write .` or `bun run lint:fix`                  |
| Format (check)         | `bun x biome format .` or `bun run format`                           |
| Format (fix)           | `bun x biome format --write .` or `bun run format:fix`               |
| Typecheck (all)        | `bun run typecheck`                                                  |
| Typecheck (single app) | `bun --filter @news-spend-media/cms typecheck`                       |
| Build (CMS)            | `bun run build` (root) or `bun --filter @news-spend-media/cms build` |
| Dev (CMS)              | `bun run dev` or `bun --filter @news-spend-media/cms dev`            |
| Dev (Server)           | `bun --filter @news-spend-media/server dev`                          |
| Test (all packages)    | `bun run test` (turbo)                                               |
| Test (API)             | `cd packages/api && bun test`                                        |
| Test (API, watch)      | `cd packages/api && bun test --watch`                                |
| Test (API, single file)| `cd packages/api && bun test path/to/file.test.ts`                   |
| Test (Native)          | `cd apps/native && bun run test`                                     |
| Test (Native, watch)   | `cd apps/native && bun run test:watch`                               |
| Generate Payload types | `cd apps/cms && bun run generate:types`                              |
| DB push                | `cd packages/db && bun run db:push`                                  |
| DB migrate             | `cd packages/db && bun run db:migrate`                               |
| DB studio              | `cd packages/db && bun run db:studio`                                |

Run `bun x biome check --write` before committing. Pre-commit hooks (lefthook) enforce this.

## Linting & Formatting (Biome)

This project uses **Biome** for linting and formatting, not ESLint/Prettier.

Config files: `biome.jsonc` at repo root.

## TypeScript Config

All packages extend `@news-spend-media/config/tsconfig.base.json`:

- `strict: true`, `strictNullChecks: true`
- `target: "ESNext"`, `module: "ESNext"`, `moduleResolution: "bundler"`
- `verbatimModuleSyntax: true`: use `import type` for type-only imports
- `noUncheckedIndexedAccess: true`: array/object access returns `T | undefined`
- `noFallthroughCasesInSwitch: true`
- `isolatedModules: true`

CMS tsconfig uses `~/*` path alias → `./src/*`.

## Code Style Guidelines

### Imports

- Use `import type` for type-only imports (enforced by `verbatimModuleSyntax`)
- Prefer named exports; avoid default exports where possible
- Use specific imports, not namespace imports (`import * as X`)
- Workspace packages use `workspace:*` in package.json

### Types & Safety

- Prefer `unknown` over `any` when type is genuinely unknown
- Use `as const` for immutable literal values
- Leverage TypeScript narrowing over type assertions
- Never use `as any`, `@ts-ignore`, `@ts-expect-error` to suppress errors

### JavaScript/TypeScript

- `const` by default; `let` only when reassignment needed; never `var`
- Arrow functions for callbacks and short functions
- `for...of` loops over `.forEach()` and indexed `for`
- Optional chaining (`?.`) and nullish coalescing (`??`)
- Template literals over string concatenation
- Destructuring for object/array assignments

### Async

- Always `await` promises in async functions
- `async/await` over `.then()` chains
- Use try-catch for error handling in async code
- Never use async functions as Promise executors

### React

- Function components, not class components
- Hooks at top level only, never conditional
- Complete dependency arrays for hooks
- `key` prop on iterables (prefer unique IDs over array indices)
- Semantic HTML + ARIA for accessibility
- React 19: use `ref` as prop (not `React.forwardRef`)

### Error Handling

- Remove `console.log`/`debugger`/`alert` from production code
- Throw `Error` objects with descriptive messages
- Early returns over nested conditionals for error cases
- Don't catch errors just to rethrow them

### API Layer (orpc)

- Procedures: `publicProcedure`, `protectedProcedure`, `protectedNoGuestProcedure`, `rateLimitedPublicProcedure`
- Validation: Zod schemas
- Context: `packages/api/src/context.ts`

#### Testing routers

Test procedures directly (no HTTP), per the [oRPC testing guide](https://v2.orpc.dev/docs/advanced/testing-and-mocking).
Helpers live in `packages/api/src/test-utils.ts`; put the test next to the
router as `<router>.test.ts`.

```ts
const payload = createFakePayload({ collections: { users: [{ id: "user-1" }] } });
const ctx = mockContext({ user: { id: "user-1", isAnonymous: false } as never, payload });

await call(myRouter.get, { id: "x" }, { context: ctx });     // one procedure
const client = createTestClient(myRouter, ctx);              // whole router
const error = await expectError(client.get({ id: "nope" })); // assert a rejection
```

`createFakePayload` is an in-memory Payload: seeded collections, real `where`
filtering, sort and pagination, plus `payload.docs(slug)` and `payload.calls`
for assertions. Middleware runs for real, so auth and rate limiting are
testable; a schema failure surfaces as `BAD_REQUEST` / "Input validation failed".

### Payload CMS

- Collections/fields/hooks in `packages/payload/src/`
- Components in `packages/payload/src/components/`
- Use `cn()` utility (clsx + tailwind-merge) for class merging

## Project Structure

```
apps/
  cms/          # Next.js + Payload admin + frontend
  server/       # Bun HTTP server (orpc API, auth, health)
  native/       # React Native / Expo mobile app
packages/
  api/          # orpc router, procedures, middlewares (bun:test tests here)
  auth/         # Better Auth config
  config/       # Shared tsconfig bases
  db/           # Drizzle ORM schema + migrations
  env/          # Environment variable validation (@t3-oss/env-nextjs)
  logger/       # Logging utilities
  mail/         # Email sending
  payload/      # Payload CMS config, collections, fields, blocks, hooks
  payload-cpanel-storage/  # Custom Payload storage adapter
  transactional/  # Email templates (react-email)
  utils/        # Shared utilities
tooling/
  tailwind/     # Shared Tailwind config
```

## Key Libraries & Frameworks

| Library             | Purpose                         |
| ------------------- | ------------------------------- |
| Payload CMS v3      | Headless CMS, admin panel       |
| Next.js 15          | CMS frontend (React 19)         |
| orpc                | Type-safe API layer (tRPC-like) |
| Zod v4              | Schema validation               |
| Drizzle ORM         | Database (PostgreSQL)           |
| Better Auth         | Authentication                  |
| Tailwind CSS        | Styling                         |
| React Native / Expo | Mobile app                      |
| Jest                | Native unit testing             |
| bun:test            | API unit testing                |
| Turborepo           | Monorepo task orchestration     |
| Sentry              | Error tracking                  |

## Git Hooks (Lefthook)

Pre-commit: runs `bun x biome check --write` on staged files, auto-stages fixes.

## What Biome Won't Catch

1. Business logic correctness
2. Meaningful naming and self-documentation
3. Architecture decisions (component structure, data flow)
4. Edge cases and boundary conditions
5. UX/accessibility beyond linting rules
6. Performance implications of algorithmic choices

## Agent skills

### Issue tracker

Issues, specs, and tickets live as GitHub issues (via the `gh` CLI). See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Multi-context: `CONTEXT-MAP.md` at the root points at per-context `CONTEXT.md` files (`apps/cms`, `apps/server`, `apps/native`), with `docs/adr/` at the root for system-wide decisions. See `docs/agents/domain.md`.
