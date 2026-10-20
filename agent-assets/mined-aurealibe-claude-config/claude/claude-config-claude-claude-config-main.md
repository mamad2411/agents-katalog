# AUREA Developer Guidelines

## Project Overview

**AUREA** Claude Code stack (Next.js 16 + Go).

- **Frontend**: Next.js 16 (App Router), TypeScript, TailwindCSS, React Query, Shadcn UI
- **Backend**: Go (Golang), Fiber, Clean Architecture
- **Database**: Supabase (PostgreSQL), Redis
- **Infrastructure**: Docker

### Supabase Project IDs

- **Dev**: `dev_project_id`
- **Prod**: `prod_project_id`

---

## Fundamental Development Principles

### 1. Database Interaction via MCP Supabase (PRIORITY)

**All database interactions MUST use MCP Supabase servers:**

- **Read/Write**: Use `mcp__supabase-dev__execute_sql` or `mcp__supabase-prod__execute_sql`
- **Migrations**: Use `mcp__supabase-dev__apply_migration` or `mcp__supabase-prod__apply_migration`
- **Inspection**: Use MCP commands `list_tables`, `list_extensions`, `list_migrations`
- **NEVER**: Direct connections, psql, or other SQL clients

### 2. Maximum Reuse of Existing Code

**GOLDEN RULE**: Before creating anything new, ALWAYS:

1. Search for existing functionality in the project
2. Review components/functions in the same directory
3. Follow patterns established in similar files
4. Reuse and adapt instead of recreating

**Practical examples**:
- Creating a UI component → check `frontend/src/components/`
- Adding a hook → check `frontend/src/hooks/`
- Adding a backend service → check `backend/internal/application/usecases/`
- Adding a repository → check `backend/internal/domain/repositories/`

### 3. Dynamic & Modular Code

- All code must be fully dynamic and modular
- **NO hardcoded** parameters, thresholds, URLs, paths, or credentials
- Load all values from configuration files (`.env` for secrets, `app.yaml` for config)
- Business logic must adapt automatically to configuration changes

### 4. Clean Code & Maintenance

- **NEVER** leave unused code - ask for user approval before deletion
- **DRY Principle** - duplication is a liability
- **Concurrency**: Use goroutines (Go) or async functions (TypeScript) where beneficial, but preserve logical flow

### 5. API & Error Handling

- **ALWAYS** handle all error cases in API responses
- Never return 500 unless it's a genuine internal server error
- **NEVER** simplify external API calls without understanding their constraints (Stripe, Google, etc.)
- Never expose internal errors in API responses

### 6. Up-to-Date Information & Documentation

**ALWAYS use current information for libraries, APIs, and best practices.**

#### Priority Order for Documentation:

1. **MCP Context7** (`mcp__plugin_context7_context7__resolve-library-id` + `mcp__plugin_context7_context7__query-docs`)
   - Use FIRST for any library documentation (React, Next.js, Supabase, Fiber, etc.)
   - Provides indexed, structured documentation
   - Example: Before using a React Query pattern, query Context7 for latest API

2. **WebSearch** (`WebSearch` tool)
   - Use when Context7 doesn't have the library
   - Use for latest best practices and patterns (add "2024 2025" to queries)
   - Use for error messages and troubleshooting
   - Use for external API documentation (Stripe, Google, etc.)

3. **WebFetch** (`WebFetch` tool)
   - Use to fetch specific documentation pages found via WebSearch
   - Use for official API documentation URLs

#### When to Search for Documentation:

- **Before using any library feature** you're not 100% certain about
- **When implementing a new pattern** (auth, caching, state management, etc.)
- **When encountering an error** from an external library
- **When integrating external APIs** (always check current API version)
- **When the codebase pattern seems outdated** compared to current best practices

#### Examples:

```
# Check React Query v5 patterns
mcp__plugin_context7_context7__resolve-library-id(libraryName="tanstack-query")
mcp__plugin_context7_context7__query-docs(libraryId="/tanstack/query", query="useMutation optimistic updates")

# Check latest Supabase RLS patterns
WebSearch(query="Supabase RLS policies best practices 2025 2026")

# Check Fiber middleware patterns
mcp__plugin_context7_context7__query-docs(libraryId="/gofiber/fiber", query="middleware authentication JWT")
```

**NEVER assume library APIs haven't changed. Always verify.**

### 7. Internationalization

- **ALWAYS** use `next-intl` for all user-facing text
- Define messages in `frontend/messages/{language}.json`
- **NEVER** hardcode user-facing strings
- Write code in English first, then translate

### 8. Context Propagation (Go)

- **ALWAYS** use `context.Context` as first parameter for I/O operations
- Applies to: repository methods, use case Execute methods, service methods
- **NEVER** use `context.Background()` except at application entry point

### 9. UI Design Quality (Frontend)

Pour toute création de composant UI significatif (pages, modals, forms, dashboards, cards), utilise le skill `frontend-design:frontend-design` pour garantir un design distinctif et production-ready.

### 10. Workflow Modification - CRITICAL RULE

**BEFORE editing any files, you MUST Read at least 3 files** that will help you to understand how to make a coherent and consistent codebase.

**Types of files you MUST read:**

1. **Similar files**: Read files that do similar functionality to understand patterns and conventions
2. **Imported dependencies**: Read the definition/implementation of any imports you're not 100% sure how to use correctly - understand their API, types, and usage patterns

**Steps to follow:**

1. Read at least 3 relevant existing files (similar functionality + imported dependencies)
2. Understand the patterns, conventions, and API usage
3. Only then proceed with creating/editing files

### 11. Frontend Styling Guidelines

- **Mobile-first approach** with TailwindCSS
- Use Shadcn/UI components from `src/components/ui/`
- Custom components in `src/components/nowts/`

#### Styling Preferences

- Use the shared typography components in `@/components/nowts/typography.tsx` for paragraphs and headings (instead of creating custom `p`, `h1`, `h2`, etc.)
- For spacing, prefer utility layouts like `flex flex-col gap-4` for vertical spacing and `flex gap-4` for horizontal spacing (instead of `space-y-4`)
- Prefer the card or item or container (`@/components/ui/card.tsx`, `@/components/ui/item.tsx`) for styled wrappers rather than adding custom styles directly to `<div>` elements

#### Visual / Colors

- Never use emojis (no emoji characters).
- Use ONLY - icons from our icon library instead of emojis (e.g., Lucide) 
- VISUAL / COLORS : Avoid “default LLM aesthetics”: no purple/violet/pink gradients by default, no aurora/sunset/cyber gradients, no heavy glow/glassmorphism.
- Default to solid neutral backgrounds + one accent.
- Colors/gradients only from brand palette tokens; if tokens aren't provided, don't invent colors (stick to neutral).

#### Copywriting / Punctuation

- **NEVER use em-dashes (`—`)** anywhere: not in i18n messages (`frontend/messages/*.json`), not in user-facing copy, not in code comments, not in JSX text. Em-dashes are a classic "LLM-written" tell and break a human tone.
- Replace `—` with a period (`.`) for sentence breaks, a comma (`,`) for continuation, a colon (`:`) to introduce a clause, or parentheses `()` for asides.
- Same rule for en-dashes (`–`) in prose. Hyphens (`-`) are fine for compound words, ranges, and technical identifiers.

### 12. Quality-First Recommendations (CRITICAL)

**Do not default to the simplest / cheapest / "small-project" option when recommending a plan or a code modification.** This is production software, not a prototype. The **recommended** choice must reflect genuine technical judgment, balancing:

- **Elegance**: clean, idiomatic, well-architected code
- **Long-term maintainability**: low technical debt, clear boundaries, testable
- **Reasonable scalability**: fits the current scale and foreseeable growth without requiring a rewrite

A lean / simple solution IS the right call in some cases (small isolated scope, throwaway logic, clear YAGNI), but only as the outcome of an **explicit arbitration**, not a reflex. When the trade-off is genuinely unclear, lean toward the more robust and maintainable option.

**Forbidden defaults**: reflexively picking the shortest path; proposing "quick wins" that create future debt without flagging the trade-off; optimizing the *recommended* option for token cost or implementation speed.

**When presenting multiple options**, the option tagged **"Recommended"** MUST:

1. Score highest on (elegance + maintainability + scalability) among the options.
2. Include a one-sentence justification of WHY each alternative is NOT the recommendation (what it sacrifices: robustness, scale ceiling, testability, isolation).
3. If it is also the simplest to implement, explicitly state "simplicity is a genuine technical fit here because X" rather than leaving it implicit.

A more economical variant CAN be offered as an **alternative**, with the trade-offs spelled out so the user can choose knowingly.

---

## Core Architecture

### Frontend (Next.js 16)

- **Pattern**: Hybrid Server/Client Components
  - **Server Components** (default): Layouts, initial data fetching, static UI
  - **Client Components** (`'use client'`): Interactivity, state, hooks, providers
- **I18n**: MUST use `next-intl`
- **Styling**: Tailwind CSS + Shadcn UI

### Backend (Go Clean Architecture)

**4 Layers - Strict Separation**:

1. **Domain** (`internal/domain`): Entities, Value Objects, Repository Interfaces. NO external deps.
2. **Application** (`internal/application`): Use Cases, DTOs, Ports. Orchestrates logic.
3. **Infrastructure** (`internal/infrastructure`): Repository implementations, external services (DB, AI, Auth).
4. **Presentation** (`internal/presentation`): HTTP Handlers (Fiber), Middleware.

### Database & Environment

- **Parameterized Queries**: All database operations MUST use parameterized queries
- **Supabase Remote ONLY**: Never use local Supabase
- **Docker**: NEVER restart manually during dev - use `air` for auto-reload
- **Configuration**: `.env` for secrets, `app.yaml` for application config

### Logging Strategy

- **Dev**: Verbose (Info level) with full data structures
- **Prod**: Clean (Info/Warn/Error)
- **Retries**: NEVER log `ERROR` on retryable failures - use `Warn`. An `Error` should mean a final, unrecoverable failure (the one that reaches your error tracker, e.g. Sentry).

#### Structured logging only (Go)

- **NEVER use the stdlib `log` package** (`log.Printf`, etc.) in application code. Use the injected structured logger everywhere.
- **Every log call MUST attach context via `WithField` / `WithFields` / `WithError`.** With logrus, extra positional args are silently dropped or concatenated into the message, not parsed as key-value pairs.
- **Field names in `snake_case`** (`user_id`, `task_id`, `retry_count`).
- **No `fmt.Sprintf` / `Errorf` inside log messages** - pass the values as fields instead.
- No emojis or bracket prefixes (`[CRAWLER]`) in log messages.

```go
// FORBIDDEN: positional args, stdlib log, string concat, Sprintf
logger.Error("Failed to process", "user_id", userID)
log.Printf("Task %s failed: %v", taskID, err)
logger.Info(fmt.Sprintf("Processing %d items", count))

// REQUIRED: structured fields + WithError
logger.WithField("user_id", userID).Error("failed to process")
logger.WithFields(map[string]interface{}{
    "user_id": userID,
    "task_id": taskID,
}).WithError(err).Warn("failed to check rate limit")
```

### Security

- **Secrets**: NEVER commit `.env`
- **Auth**: JWT in `httpOnly` cookies, backend validates tokens

---

## Development Process

### Before Implementation

1. Understand the full context of the request
2. Identify affected components and services
3. Evaluate dependencies and side effects
4. Plan all steps using TodoWrite

### Ask Clarifying Questions

If not clearly defined, clarify:
- Where should the new code be placed?
- What level of input validation is expected?
- What error scenarios should be handled?
- Are there performance or scalability constraints?

### Validation with User

**Approval required at key checkpoints**:
1. Before starting major work
2. After preparing implementation plan
3. If architectural decisions are needed

---

## Naming Conventions

- **Go structs**: PascalCase
- **JS/TS**: camelCase for variables, PascalCase for components
- **Files**: kebab-case for frontend, snake_case for backend

---

## Linting (Go)

**Run the linter BEFORE any Go build or commit:**

```bash
cd backend && golangci-lint run ./...
```

Fix all reported issues before proceeding. Common patterns:

- `defer x.Close()` → `defer func() { _ = x.Close() }()`
- Unchecked error return → `_ = x.Method(...)` or handle it with `if err := ...; err != nil`
- `if x != nil && len(x) > 0` → `if len(x) > 0` (nil slice length is zero in Go)
- Error strings must be lowercase: `fmt.Errorf("failed to ...")`, not `"Failed to ..."`
- Never leave unused functions / variables in the codebase

---

## Testing (CRITICAL)

**Every significant change MUST include unit tests, regardless of layer.** Run tests before any build or commit; zero regressions allowed.

### Common rules (backend AND frontend)

- **Mandatory** for any new logic with non-trivial branches or state: backend usecases / services / repository methods; frontend components with conditional rendering, hooks, and utility/parsing functions.
- **Colocated**: test files live next to the source (`*_test.go` for Go, `*.test.ts` / `*.test.tsx` for TS/TSX).
- **Coverage**: at minimum the happy path + the main error / edge cases.
- **Zero regressions**: ALL existing tests MUST pass. If a change legitimately breaks a test, update the test in the same change. NEVER skip / disable tests just to make a build pass.

```bash
cd backend && go test ./...
cd frontend && npm run test:run
```

### Backend (Go)

- Framework: `testing` + `github.com/stretchr/testify` (`assert` / `require`).
- Mocks: hand-written function-pointer mocks (no code generation); shared setup in `*_test_helpers_test.go`.
- Use an `env` struct helper to wire dependencies for each test (happy-path + error-case tests).

### Frontend (Vitest + Testing Library)

- Framework: `vitest` (jsdom) + `@testing-library/react` + `@testing-library/jest-dom` matchers.
- Prefer `vi.mock(modulePath, factory)` for module-level deps (contexts, hooks, navigation); keep mocks shallow.
- Mock the i18n layer, e.g. `vi.mock('next-intl', () => ({ useTranslations: () => (k: string) => k }))`.
- No real network in unit tests: mock the API module instead.

---

## Process & Resource Hygiene

Long sessions and subagents leak background processes if you are not careful. Follow these rules so nothing leaks:

- **Prefer self-exiting commands for verification** (they terminate on their own): `go build ./...`, `go vet ./...`, `go test ./...`, `golangci-lint run ./...`, `npm run build`, `npm run test:run`.
- **NEVER use watch / dev mode for a one-off check**: not `npm run test` (watch), not `npm run dev`, not `go run cmd/main.go`, not `air` / `vite`, just to "see if it compiles". Use the self-exiting variant instead.
- **To verify against a running app, reuse the running stack**: discover its port with `lsof -iTCP -sTCP:LISTEN -P -n` and hit it, rather than spawning a parallel server.
- **Never start servers with raw `&`, `nohup`, or a detached background run** - they escape cleanup and leak past your turn. If you must start something long-running, stop it before you finish.
- **Build-storm hygiene**: do not fan out many concurrent heavy builds; prefer one `go build ./...` over many per-package invocations; never disable the Go build cache.

---

## Common Commands

```bash
# Setup
npm run setup:all

# Start Dev (Docker + Backend + Redis)
npm run dev

# Backend only
cd backend
go run cmd/main.go
go test ./...             # ALWAYS run - zero regressions
golangci-lint run ./...  # ALWAYS run before build/commit

# Frontend only
cd frontend
npm run dev
npm run test:run          # ALWAYS run - zero regressions
npm run build             # type-check + production build
```
