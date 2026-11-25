---
name: global-error-registry
description: >
  Design, install, migrate, validate, audit, and document a hexagonal
  application-global error registry with stable numeric error codes, structured
  matchers, ports/adapters, and UI-neutral domain models. AUTO-RUN the global
  workflow global-error-registry when the user asks for a global error registry,
  error-code allocation, migrate getErrorInfo/dashboard-error-screen, audit
  unregistered errors, or runs /global-error-registry or
  /workflow global-error-registry. Use for ErrorRegistry, ErrorCode, matchers,
  NormalizedApplicationError, and dashboard error presentation adapters.
---

# Global Error Registry

## Auto-run (do not only summarize)

When the user wants **implementation, migration, audit, validation, or docs** for
an application-global error registry (not a pure explanation), **immediately**
launch the workflow tool:

```text
name: global-error-registry
args: {
  "command": "full",
  "root": "",
  "dry_run": false,
  "auto_implement": true,
  "focus": "apps/web/src/components/layouts/dashboard-error-screen.tsx",
  "report_dir": "docs/errors",
  "report_slug": ""
}
agent_budget: 64
```

| User intent | `command` |
|-------------|-----------|
| Full XBP-style migrate | `full` (default) |
| Discover layout / propose package path | `init` |
| Inventory only | `inspect` |
| Add one error definition | `register` |
| Move existing message matching into registry | `migrate` |
| Static validation of registry | `validate` |
| Find unregistered / ad hoc error UI | `audit` |
| Run tests + typecheck | `test` |
| Generate docs / error-code table | `docs` |

- Inventory / no edits → `"dry_run": true` or `command: inspect` / `audit`
- Human gate before broad edits → `"auto_implement": false`
- Focus path → `"focus"` or `"root"` (e.g. `apps/web`)

Tell the user the run is in `/workflows`. On completion report:

1. Files created / changed  
2. Error codes added  
3. Behavior preserved (especially dashboard actions)  
4. Tests run (or why not)  
5. Remaining migration candidates  
6. Compatibility risks  

## Hard invariants

1. **Registry resolves meaning; UI renders.** Domain package has **zero** React, TanStack Router, HeroUI, Tailwind, or browser API imports.
2. **Codes are stable compile-time constants** — never allocate dynamically at runtime; never silently renumber.
3. **Matchers are structured** — no new ad hoc `lower.includes(...)` chains in UI after migration.
4. **Precedence is explicit** (not registration order alone). See [references/architecture.md](references/architecture.md).
5. **Redact secrets** — never put tokens, cookies, Authorization headers, credentialed URLs, or request bodies in user messages or diagnostics payloads.
6. **Preserve dashboard behavior** unless the user explicitly asks to change UX.
7. **Inspect the repo first** — package manager, path aliases, test runner, existing error conventions.
8. **Small reviewable steps** — no uncontrolled repo-wide rewrite.

## Primary XBP target

When working in the XBP monorepo, start with:

```text
apps/web/src/components/layouts/dashboard-error-screen.tsx
```

`getErrorInfo(error)` is message-string matching. **Do not** only move that
function. Design a proper registry + migrate definitions. Full migration notes:
[references/xbp-dashboard-migration.md](references/xbp-dashboard-migration.md).

Architecture detail (domain models, ports, code allocation, API):
[references/architecture.md](references/architecture.md).

## Hexagonal layout (preferred)

```text
domain (package, no UI)
  types: ErrorCode, ApplicationErrorDefinition, ErrorMatcher, NormalizedApplicationError
  ports: ErrorNormalizer, ErrorRegistryPort, DiagnosticReporter, ErrorPresentationAdapter
  registry: createErrorRegistry, applicationErrorRegistry, validate()
  definitions: github-*, rate-limit-*, network-*, timeout-*, not-found-*, unknown-*

adapters (may live next to consumers)
  normalize: Error / fetch / Octokit / TanStack Query / string / unknown
  presentation: dashboard → title, description, icon token, action
  diagnostics: recordClientDiagnosticError enrichment (code + key)
  router: thin ErrorComponentProps bridge only

UI (apps/web)
  DashboardErrorScreen — resolve → present → buttons / router / modals
```

Prefer existing monorepo conventions for package location:

| Layout signal | Prefer |
|---------------|--------|
| `apps/web/packages/*` workspace | `apps/web/packages/error-registry` or similar |
| root `packages/*` | `packages/error-registry` |
| Single app, no packages | `src/lib/errors/` domain folder with clear boundary |

Propose the path in **init** before writing files when location is unclear →
pause / await_user.

## Matcher precedence (must implement)

Higher wins; first match at a tier wins within that tier:

1. Exact registered **error code** on the normalized error  
2. Exact **provider + HTTP status**  
3. Exact **error name**  
4. Specific **message-regex** / multi-token message patterns (e.g. Linear rate limit)  
5. Generic **message-contains**  
6. Generic **HTTP status** only  
7. Generic **network / timeout** classes  
8. **Unknown** fallback (always registered)

`validate()` must flag: duplicate codes/keys, unreachable matchers, missing
unknown fallback, invalid `ErrorCode` shape, unsafe `exposeDetails` defaults.

## Error code allocation

HTTP-associated:

```text
{status}{index:02d}
```

Examples: `40100`, `40101`, `40300`, `40400`, `42900`, `50000`.

Non-HTTP reserved namespace (e.g. `9xxxx` or repo-existing convention) for pure
client/network/unknown if no status applies. **Inspect first** — if the repo
already has a convention, preserve it.

Allocator rules:

- Deterministic next free index per status namespace  
- Never reuse  
- Duplicate code/key/semantic → fail validate  
- Rename display text **keeps** code  
- Code change requires explicit migration entry  

## Registry API (target shape)

```ts
createErrorRegistry(defs): ErrorRegistry
applicationErrorRegistry // app singleton

registry.register(def)
registry.getByCode(code)
registry.getByKey(key)
registry.resolve(error): ResolvedApplicationError
registry.list()
registry.validate(): RegistryValidationResult
```

Core must support **new instances** for tests, not only a singleton.

## Dashboard migration checklist

After migrate, `DashboardErrorScreen` should:

1. `applicationErrorRegistry.resolve(error)`  
2. Presentation adapter → title/description/icon/action  
3. Keep buttons, Link, router.invalidate, GitHub modal, org warnings  
4. Preserve `cleanErrorMessage`  
5. Preserve diagnostics (with **code + key** fields)  
6. Preserve self-approve PR, Linear rate limit detail bounding  
7. **No** long `if (lower.includes(...))` chain  

## Diagnostics

Every report should include when available:

- code, key, httpStatus, provider, category, severity, retryable  
- route/path, requestId  
- safe normalized message  

Never: access tokens, cookies, Authorization, signed secret URLs, installation
secrets, arbitrary bodies.

## Workflow commands

Global workflow: `~/.grok/workflows/global-error-registry.rhai`

```text
/workflow global-error-registry
/workflow global-error-registry command=init
/workflow global-error-registry command=inspect
/workflow global-error-registry command=register
/workflow global-error-registry command=migrate
/workflow global-error-registry command=validate
/workflow global-error-registry command=audit
/workflow global-error-registry command=test
/workflow global-error-registry command=docs
/workflow global-error-registry command=full dry_run=true
```

## Manual skill-only mode

If the user says “explain only” / “don’t edit”:

1. Read focus files and inventory error handling  
2. Propose package path, code namespaces, definition list  
3. Do **not** launch implement phases  

## Stop conditions (must pause)

- Conflicting registry definitions or ambiguous precedence  
- Unclear package location / multiple monorepo apps without `root`/`focus`  
- Migration would change observable user-facing copy/actions without approval  
- Tests cannot run and user required proof  
- Sensitive data handling uncertain  

## Final report template

```markdown
## Global error registry report
- Command:
- Files created:
- Files changed:
- Error codes added:
- Behavior preserved:
- Tests executed / not executed:
- Remaining migration candidates:
- Compatibility risks:
```
