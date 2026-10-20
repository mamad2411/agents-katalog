# AGENTS.md — `@t/config`

## What this owns

All environment-variable parsing, validation, and typed access for the monorepo.
Single source of truth for every config namespace: `system`, `auth`, `db`, `redis`,
`analytics`, `posthog`, `stripe`, `revenueCat`, `apple`, `appStore`, `android`,
`website`, `client`.

## Layout

```
packages/config/
  entities/
    ports/      ConfigRepository.ts            — abstract port
    schemas/    SystemConfigSchema.ts          — per-namespace Zod schemas (16 files)
                ConfigValuesSchema.ts          — full union schema
    types/      Environment.ts, etc.
  infrastructure/
    ConfigRepositoryImpl.ts                    — reads process.env; throws at boot
    __tests__/  ConfigRepositoryImpl.test.ts
  dependency-injection/
    registerConfigRepoDI.ts                    — registers CONFIG token
  index.ts
```

## DI registrar

C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\config\dependency-injection\registerConfigRepoDI.ts

```ts
registerConfigRepo(container: Container, options?: ConfigRepositoryOptions): void
```

`ConfigRepositoryOptions.schema` lets consumers narrow to a per-app schema
(e.g., `WebConfigValuesSchema`) so mobile/web don't fail on API-only env vars.

Token key: `dependencyKeys.global.CONFIG` (`"config"`).
Must be the **first** `register*` call in every composition root — all other registrars
take `config` as an option.

## Consumers

- `apps/api` — full `ConfigValuesSchema` (all namespaces)
- `apps/website` — `WebConfigValuesSchema` (system + auth + analytics + website)
- `apps/web` — `WebClientConfigSchema` (client-side subset)
- `apps/mobile` — `MobileConfigValuesSchema`

## Conventions

- **Hard-fail on missing required vars.** `ConfigRepositoryImpl` calls
  `this._schema.parse(raw)` in the constructor. Any missing required field throws a
  `ZodError` at boot — the process exits before serving traffic. This is intentional.
- **No NoOp fallback for required vars.** Do not add `.optional()` or `.default()`
  to silence a missing required var. Add an explicit feature-flag field with a
  boolean opt-out instead.
- **Schema-scoped validation.** Pass a narrower schema via `options.schema` to
  skip namespaces the app doesn't need — not to suppress validation errors.
- **No raw `process.env` reads outside this package.** All config access goes through
  `ConfigRepository`; app code never reads `process.env` directly.
- `ConfigRepositoryImpl` is the only implementation. Test doubles mock the port.

## Links

- Config architecture: docs/architecture/platform/config.md
- Root conventions: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md
- DI token registry: C:\Users\jager\OneDrive\Documents\GitHub\template-repo\packages\dependency-injection\src\entities\dependencyKeys.ts
