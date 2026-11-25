---
name: search-first
description: Research-before-coding workflow. Search for existing tools, libraries, and patterns before writing custom code.
---

# Search First — Research Before You Code

Systematizes the "search for existing solutions before implementing" workflow.

## When to Activate

- Starting a new feature that likely has existing solutions
- Adding a dependency or integration
- Before creating a new utility, helper, or abstraction
- When about to write code for a common problem

## Workflow

```
┌─────────────────────────────────────────────┐
│  1. NEED ANALYSIS                           │
│     Define what functionality is needed      │
│     Identify language/framework constraints  │
├─────────────────────────────────────────────┤
│  2. PARALLEL SEARCH                         │
│     ┌──────────┐ ┌──────────┐ ┌──────────┐  │
│     │  go pkg  │ │  npm     │ │  GitHub / │  │
│     │  search  │ │  search  │ │  Web      │  │
│     └──────────┘ └──────────┘ └──────────┘  │
├─────────────────────────────────────────────┤
│  3. EVALUATE                                │
│     Score candidates (functionality, maint, │
│     community, docs, license, deps)         │
├─────────────────────────────────────────────┤
│  4. DECIDE                                  │
│     ┌─────────┐  ┌──────────┐  ┌─────────┐  │
│     │  Adopt  │  │  Extend  │  │  Build   │  │
│     │ as-is   │  │  /Wrap   │  │  Custom  │  │
│     └─────────┘  └──────────┘  └─────────┘  │
├─────────────────────────────────────────────┤
│  5. IMPLEMENT                               │
│     Install package / Write minimal custom  │
│     code informed by research               │
└─────────────────────────────────────────────┘
```

## Decision Matrix

| Signal | Action |
|--------|--------|
| Exact match, well-maintained, MIT/Apache | **Adopt** — install and use directly |
| Partial match, good foundation | **Extend** — install + write thin wrapper |
| Multiple weak matches | **Compose** — combine 2-3 small packages |
| Nothing suitable found | **Build** — write custom, but informed by research |

## Quick Search Checklist

Before writing a utility or adding functionality:

1. Is this a common problem? → Search pkg.go.dev / npm
2. Is there an MCP tool for this? → Check configured MCP servers
3. Does the codebase already solve this? → `grep_search` and `find_by_name`
4. Is there a well-known library? → Search GitHub / web

## Search Shortcuts by Category

### Go Ecosystem
- HTTP framework → `gin-gonic/gin` (already used)
- ORM → `gorm.io/gorm` (already used)
- JWT → `golang-jwt/jwt`
- Validation → `go-playground/validator`
- Config → `spf13/viper`, `kelseyhightower/envconfig`
- Logging → `uber-go/zap`, `rs/zerolog`
- Testing → `stretchr/testify`, `DATA-DOG/go-sqlmock`
- Migration → `golang-migrate/migrate`
- Task queue → `hibiken/asynq`
- Cron → `robfig/cron`

### TypeScript/React Ecosystem
- HTTP client → `ky`, `axios`
- Validation → `zod`
- State management → `zustand`, `jotai`
- Date handling → `date-fns`, `dayjs`
- Animation → `framer-motion`
- Charts → `recharts`, `visx`
- Icons → `lucide-react` (already used)
- Forms → `react-hook-form`
- Table → `@tanstack/react-table`
- Virtual list → `@tanstack/react-virtual`

### Infrastructure
- Reverse proxy → `nginx`, `caddy`
- Process manager → `air` (Go hot reload)
- CI → GitHub Actions
- Container registry → `ghcr.io`

## Examples

### Example 1: "Add price fetching"
```
Need: Fetch cryptocurrency prices from an external API
Search: Go "cryptocurrency price API client"
Found: coingecko-api (score: 7/10), direct HTTP (score: 9/10)
Action: BUILD — simple HTTP client with the asset's API
Result: Thin wrapper around net/http, no heavy dependency
```

### Example 2: "Add structured logging"
```
Need: JSON structured logging with levels
Search: Go "structured logging"
Found: zerolog (9/10), zap (9/10), slog (8/10 — stdlib)
Action: ADOPT — use slog (stdlib, zero dependencies)
Result: Zero external dependency, production-ready
```

### Example 3: "Add form validation"
```
Need: Client-side form validation with TypeScript types
Search: npm "react form validation typescript"
Found: react-hook-form + zod (9/10)
Action: ADOPT — install both, use zod for schema + react-hook-form for UI
Result: Battle-tested solution, great TypeScript support
```

## Anti-Patterns

- **Jumping to code**: Writing a utility without checking if one exists
- **NIH syndrome**: Rejecting good libraries because "we can build it ourselves"
- **Over-customizing**: Wrapping a library so heavily it loses its benefits
- **Dependency bloat**: Installing a massive package for one small feature
- **Ignoring stdlib**: Go's standard library and Node.js built-ins cover many cases

---

**Remember**: The best code is the code you don't write. Research first, build only what's truly custom to your domain.
