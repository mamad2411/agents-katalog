---
name: mapping-codebase
description: Produce a curated CONTEXT.md map of an unfamiliar or large codebase covering entry points, architecture, modules, domain terms, commands, and landmines. Use when starting work on an unfamiliar codebase, joining a project, before a cross-cutting refactor, or when a previous session got confused about where things live. Skip for codebases under ~30 source files where direct reading is faster.
---

# Mapping Codebase

Context degradation is the primary failure mode of AI coding. The fix is not to dump more files into context — it is to produce a small, curated artifact that gives a navigation layer over the actual code. This skill produces that artifact.

The output is a map, not a re-export. The minimum information needed to reason about *where* things live and *what they're called*, so the actual code can be read on demand.

The map is not the territory. Make the map small enough to be useful — under 300 lines, pointing to detail rather than reproducing it.

## Process

1. **Check for an existing map.** Look for `CLAUDE.md`, `CONTEXT.md`, `docs/ARCHITECTURE.md`, then `README.md`. If a recent map exists, ask the user if it's still accurate. If refreshing, read the existing map first and use it as scaffolding — don't rebuild.
2. **Survey the codebase.** Get raw signals before opening source files: top-level layout, build/config files present, file counts by extension, comment-tag density (TODO/FIXME/HACK/XXX), source files over ~300 lines, test directory layout, generated/vendored locations.
3. **Identify entry points and architecture.** An entry point is where execution starts: `main()`, HTTP server bind, CLI dispatcher, job worker, Lambda handler. Most codebases have 1–5; if you find 10+ you're listing files. State the architecture in one or two sentences. If you can't, read more before continuing.
4. **Identify modules.** List the 5–15 that carry weight. Aggregate trivial groupings. Module boundaries follow shared state and crossed interfaces, not directory depth — a `lib/` folder is not a module; `services/auth/` may be one or three.
5. **Identify domain terms.** Capture 5–20 product-specific terms whose meaning is not self-evident. Term as it appears in code, one-line definition, canonical location. If a term is used heavily but you can't define it, ask the user.
6. **Identify commands.** Find install/run/build/test/lint/typecheck/format commands from `package.json`, `Makefile`, `pyproject.toml`, etc. Verify they run before recording. Mark broken ones `BROKEN — <reason>`.
7. **Identify landmines.** Things that will trip up future changes. Be specific — path, nature, recommended caution.
8. **Write `CONTEXT.md`** at the project root using the template below. Keep total under 300 lines; if a section grows past ~30 lines, push to `docs/architecture/<area>.md` and link.
9. **Confirm with user.** Ask: "Anything wrong or missing?" and "Should this stay as standalone CONTEXT.md, or merge key parts into CLAUDE.md?" If merging, follow the rules below.

## Rules

- **Curate, don't re-export.** A map listing every directory adds nothing over `tree`. Pick the 10 of 200 directories that actually matter, and say why.
- **Find entry points before mapping structure.** If you can't say what the code *does* at runtime, mapping its structure produces a static-analysis report, not a useful map.
- **Distrust README.** READMEs go stale faster than any other doc. Verify any claim against actual code before recording it.
- **Ask one history question.** "Why is this code shaped this way?" often surfaces a constraint (a customer integration, a regulatory rule, a deprecated migration) that no code reading reveals.
- **Be specific on landmines.** "Some legacy code" is useless. "`src/billing/legacy_invoice.ts` predates current schema, used by ~5 customers, no tests; modify only with characterization tests in place" is useful.
- **No code changes in this skill.** It reads only.

## Output Format

Write `CONTEXT.md` at the project root with this structure. Fill in only sections with real content; delete empty headings rather than leaving TODO stubs.

```
# Project Context

**Last mapped:** YYYY-MM-DD

## What this project is

Two to four sentences. What does this software do, for whom, and what is its dominant constraint? A reader who has never seen the code should be able to summarize the project's purpose.

Avoid marketing language. Avoid implementation language. Aim for: "Multi-tenant SaaS billing engine that accepts usage events from customer systems, runs nightly invoice generation, and exposes a customer-facing portal. Strict tenant isolation is the dominant constraint."

## Architecture in one paragraph

Pattern, tech, key data flow.

Example: "Next.js 14 app router. React Server Components for pages; route handlers under `app/api/` for the public API. PostgreSQL via Drizzle ORM. Background jobs run via Inngest. Auth via Clerk; multi-tenancy enforced by middleware that injects `org_id` into every database query."

## Entry points

| Entry point | Path | Triggered by | Purpose |
|---|---|---|---|
| HTTP API | `src/app/api/` | HTTP request | Public REST API |
| Background jobs | `src/jobs/` | Inngest schedule | Nightly invoicing |

## Modules

| Module | Path | Responsibility | Public interface | Depends on |
|---|---|---|---|---|
| Billing | `src/billing/` | Invoice generation and prorations | `generateInvoice()`, `prorate()` | DB, Domain |
| Domain | `src/domain/` | Core entities and business rules | Entity classes | (leaf) |

If more than 15 rows, you're listing files. Group.

## Data model summary

5–10 most important entities and their relationships, in plain language. Not the full schema.

- **Organization**: tenant boundary; every other entity references one
- **Customer**: belongs to an Organization; has many Subscriptions
- **Invoice**: monthly billing artifact, generated by the billing engine

Full schema: `<path/to/schema>`.

## Domain terms

Only terms that are non-obvious or differ from common usage.

| Term | Meaning | Defined in |
|---|---|---|
| Org | Short for Organization; tenant boundary | `src/domain/org.ts` |
| Proration | Adjustment for mid-cycle plan change | `src/billing/proration.ts` |

## Commands

| Action | Command |
|---|---|
| Install | `pnpm install` |
| Test | `pnpm test` |
| Lint | `pnpm lint` |
| Type check | `pnpm typecheck` |
| Build | `pnpm build` |

Mark broken commands `BROKEN — <reason>`.

## Testing approach

One paragraph on how tests are organized. Example: "Unit tests sit next to source as `*.test.ts`. Integration tests in `tests/integration/` require a running Postgres (started by `pnpm db:test:up`)."

## Landmines

- `src/billing/legacy_invoice.ts` — predates current schema, no tests. Modify only with characterization tests in place.
- `src/utils/dates.ts` — three date-formatting functions with subtly different timezone behavior. Pick deliberately.
- Generated code in `src/generated/` — do not hand-edit; regenerate via `pnpm codegen`.

## Conventions

Project-specific rules not enforced by tooling.

- All DB queries go through `src/db/` — no direct ORM use from controllers.
- Server-only modules suffixed `.server.ts`; never imported by client code.

## History notes

Non-obvious context surfaced from the user. Omit if none.

- Billing engine rewritten Q3 2025; old engine still runs for ~5 grandfathered customers.

## Open questions

Unresolved items. Omit if none.
```

## CLAUDE.md vs CONTEXT.md

`CLAUDE.md` loads on every session. Every byte taxes every future interaction. `CONTEXT.md` is read on demand. Keep `CLAUDE.md` under ~200 lines.

**Goes in CLAUDE.md** (needed every interaction):
- Architecture in one paragraph
- Build/test/lint/typecheck commands
- Top 3–5 landmines
- Hard rules (phrased positively — "use X" not "never use Y")
- Pointer: "For full context see CONTEXT.md"

**Stays in CONTEXT.md** (needed only when working in a specific area):
- Full module table
- Full domain term glossary
- Detailed landmines
- History notes
- Conventions
- Open questions

Never duplicate content between the two. Duplication guarantees drift.

## Post-output instruction

After saving the map, state:

> Map saved at `<path>`. Want me to extract the high-leverage subset into CLAUDE.md so it loads on every session? I'd recommend the architecture paragraph, commands, top 3 landmines, and any hard rules — about 50 lines.
