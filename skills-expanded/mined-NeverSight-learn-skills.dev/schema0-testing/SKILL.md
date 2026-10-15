---
name: schema0-testing
description: Testing guide for web and mobile platforms — bun:test, Jest, PGlite, 3-layer validation, and test templates
---

# Testing

**STOP — testing is non-skippable.**

If you believe tests should be skipped, deferred, or substituted with anything else (browser smoke test, manual verification, "I'll add them after deploy", etc.), you MUST stop and ask the user before making any change. Send exactly this message and wait for a reply:

"I'm proposing to skip mandatory tests because [reason]. Approve?"

You may not decide this unilaterally. The decision to skip is the user's, not yours.

A test todo is complete only when you paste the test runner's output showing pass/fail counts. Other states ("deferred", "covered by smoke test", "called out in summary") are not completion.

**Minimum requirement: 3 CRUD tests per entity (create, update, delete via UI).** NEVER gut tests to make them pass — fix the source code instead.

## Shared Infrastructure

| Type   | Location                                 | Runner                               |
| ------ | ---------------------------------------- | ------------------------------------ |
| Web    | `packages/test/web/{entity}.test.tsx`    | bun:test + HappyDOM                  |
| Mobile | `packages/test/mobile/{entity}.test.tsx` | Jest + @testing-library/react-native |

Path aliases are already configured in the test tsconfigs:

- `packages/test/web/tsconfig.json` maps `@/*` → `apps/web/src/*`
- `packages/test/mobile/tsconfig.json` maps `@/*` → `apps/mobile/*`

All tests run against a **real in-process PGlite database** -- no mocks for the DB layer.

| File                | Purpose                                                                        |
| ------------------- | ------------------------------------------------------------------------------ |
| `db.ts`             | PGlite instance, `initializeTestDatabase()`. Reads migrations from `drizzle/`. |
| `drizzle.config.ts` | Generates test migrations from `packages/db/src/schema/`.                      |

### Migration Generation

When schema changes, regenerate test DB migrations:

```bash
schema0 sandbox exec "bun drizzle-kit generate" --cwd packages/test
```

This generates migration files into `packages/test/drizzle/`. **NEVER hand-write migration files.**

## Quick Start Commands

```bash
# Web tests
schema0 sandbox exec "NODE_ENV=test bun test web/{entity}.test.tsx" --cwd packages/test

# Mobile tests
schema0 sandbox exec "NODE_ENV=test NODE_OPTIONS='--experimental-vm-modules' npx jest --config jest.config.js --forceExit mobile/{entity}.test.tsx" --cwd packages/test --timeout 120000
```

## Key Rules

- **ALWAYS prefix test commands with `NODE_ENV=test`**
- Router MUST use `createDb()` -- NOT `fetchCustomResources` (causes ECONNREFUSED)
- Collection `queryFn` must use direct server calls -- NOT HTTP requests
- Collection `id`/`queryKey` must match the test's `invalidateQueries` call
- NEVER use `.toBeInTheDocument()` -- jest-dom is not installed (web tests)
- Mock ordering is critical: `@template/db` and `@template/auth` before router import
- Insert tests require `optimistic: false` to prevent HappyDOM deadlock (web tests)
- Every test MUST call `debugTexts()` as its first action (web tests)
- Every test MUST exercise the full UI chain -- no direct router/collection calls
- NEVER use `e.stopPropagation()` in `onPress` handlers (mobile tests)
- `mockQueryClient` must be created inside `jest.mock` factory (mobile tests)

## References

- `references/web-testing.md` -- Full web test guide (pre-test checklist, infrastructure, mock ordering, 3-layer validation, template, common failures)
- `references/mobile-testing.md` -- Full mobile test guide (Jest setup, differences from web, Alert.alert pattern, template)
