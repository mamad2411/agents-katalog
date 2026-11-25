---
name: context-manager
description: Use when the user asks about context organization, CLAUDE.md structure, where to store decisions or learnings, or when context feels bloated or ineffective. Teaches the 7 principles of context engineering and triages knowledge to the right destination automatically.
invoke_when: Use when managing persistent context, structuring CLAUDE.md, organizing .shipworthy/ memory, running /context, or when the user asks how to make Claude remember things across sessions.
---

# Context Manager

## Purpose

Context quality matters more than model capability. This skill teaches Claude HOW to build maximum project understanding by routing knowledge to the right place and following the 7 principles that make context survive across sessions, context compaction, and multiple Claude instances.

## The 7 Principles of Context Engineering

### 1. Prohibitions Beat Descriptions

Rules framed as what NOT to do survive context decay. Descriptive rules drift.

| Wrong | Right |
|-------|-------|
| We use Supabase for our database. | NEVER use Prisma. NEVER use Drizzle. Supabase only. |
| We prefer pino for logging. | NEVER use console.log — pino is already configured. |
| We use Jest for testing. | NEVER use Mocha or Vitest. Jest only. |

### 2. Anchor Rules to File Paths

Verifiable rules reference the actual file tree. Abstract rules drift because Claude has nothing concrete to check against.

| Wrong | Right |
|-------|-------|
| Use Zod for validation. | All validation schemas live in `src/schemas/`. NEVER inline validation. |
| We use Express with a standard structure. | All routes in `src/routes/`. All middleware in `src/middleware/`. All models in `src/models/`. |
| Tests should be nearby. | Tests colocated: `src/foo.ts` has `src/foo.test.ts`. NEVER put tests in a separate `tests/` tree. |

### 3. Negative Examples Anchor Harder

A regression fence of documented past mistakes works better than abstract best practices. Claude avoids repeating documented failures more reliably than it follows aspirational rules.

The regression fence lives at `.shipworthy/regression-fence.md` and is loaded every session as hard constraints. See the Regression Fence section below.

### 4. Constitution vs Working Memory

Two files, two jobs:
- **CLAUDE.md** = Constitution. Stable. Rarely changing. Stack locks, prohibitions, directory structure, non-negotiable rules. Read every session.
- **`.shipworthy/sessions/`** = Working memory. Dynamic. Updated every session. What happened, what's in progress, what's next.

Never mix these concerns. CLAUDE.md should not contain session state. Session files should not contain architectural rules.

### 5. Only Write What Claude Can't Infer

If Claude already does something correctly from reading your existing code, that rule wastes context window space. Ruthlessly prune.

| Wasteful (Claude can see this) | Worth writing (Claude can't infer this) |
|---|---|
| "We use TypeScript" (package.json shows it) | "NEVER use `any` — use `unknown` with type guards" |
| "We use PostgreSQL" (docker-compose shows it) | "NEVER use SQLite, even for tests — always PostgreSQL" |
| "We have a src/ directory" (it exists) | "NEVER create files at project root — everything goes in src/" |

### 6. Ordering is Load-Bearing

Claude reads top-down. What comes first survives longest under context pressure. Put your hardest constraints at the top, conventions at the bottom.

**CLAUDE.md ordering:**
1. Stack locks and prohibitions (NEVER/ALWAYS rules)
2. Directory structure anchored rules
3. Key conventions with file path references
4. How to run things (test, build, deploy)

**Session-start context priority (already enforced by hook):**
1. Architecture spec + Mandatory Rules
2. Regression fence (prohibitions)
3. In-progress plans
4. Previous session
5. Learnings

### 7. Zero Global Bleed

No tone, identity, philosophy, or general coding principles in project scope. That belongs in global Claude settings or auto-memory. The moment you mix concerns, both layers get weaker.

| Project scope (CLAUDE.md / .shipworthy/) | Global scope (Claude auto-memory / settings) |
|---|---|
| "NEVER use Prisma in this project" | "I prefer terse responses with no trailing summaries" |
| "All API routes return JSON with `{data, error}` shape" | "I'm a senior engineer, skip basic explanations" |
| "Run `npm test` before committing" | "Always suggest tests for new code" |

## Context Triage: Where Knowledge Belongs

| Knowledge Type | Destination | Automatic? |
|---|---|---|
| "NEVER do X" anti-patterns | `.shipworthy/regression-fence.md` | Auto via session-start auto-retro |
| Architecture constraints, mandatory rules | `.shipworthy/architecture.md` | Manual (one-time via `architecture-awareness`) |
| Project patterns that work | `.shipworthy/learnings/[topic].md` | Auto via session-start auto-retro |
| Session events (commits, deps, warnings) | `.shipworthy/.session-signals` | Fully automatic (hooks) |
| Task state / handoff notes | `.shipworthy/sessions/[date].md` | Auto at session end |
| Architecture decisions | `.shipworthy/decisions/[NNN].md` | Manual, prompted by skills |
| Repo map / entry points / stack locks | `CLAUDE.md` | Manual (stable, one-time) |
| User preferences (cross-project) | Claude auto-memory (global) | Automatic |

## Regression Fence

The regression fence at `.shipworthy/regression-fence.md` is a first-class Shipworthy concept. It is:
- **Loaded every session** by the session-start hook as hard constraints
- **Auto-populated** from session signals and retrospective corrections
- **Imperative format**: Each entry is an H2 heading starting with NEVER or ALWAYS
- **Anchored to file paths** where possible (principle 2)
- **Capped at 20 entries** — oldest pruned when adding the 21st
- **Dated** — each entry includes the date it was discovered (absolute, YYYY-MM-DD)

Format:
```markdown
# Regression Fence
> Known anti-patterns. Loaded every session as hard constraints. Max 20 entries.

## NEVER use SQLite in this project — PostgreSQL only
Concurrent write failures in the API layer. (2026-03-15)

## NEVER add route handlers outside src/routes/
Route in src/utils/helper.ts broke middleware chain. (2026-03-20)
```

## Context Recovery Protocol

When context is compacted mid-session and you lose awareness of the project state:

1. Read `.shipworthy/INDEX.md` — one-page index of all project memory
2. Read `.shipworthy/regression-fence.md` — anti-patterns to avoid
3. Read `.shipworthy/architecture.md` — constraints and mandatory rules
4. Read relevant `.shipworthy/learnings/` files for the current task
5. Check `.shipworthy/.session-signals` for what happened so far this session

## Multi-Instance Awareness

When multiple Claude instances work on the same project:
- All instances share `.shipworthy/` (it's in the repo)
- Regression fence protects ALL instances from known mistakes
- Session summaries provide handoff between instances
- `.session-signals` is append-only (safe for concurrent writers)
- Each instance should read INDEX.md at start for full awareness

## Rules

1. **Never auto-edit CLAUDE.md** — guide the user, propose changes, but let them own their constitution.
2. **Always use prohibitive format** for regression fence entries — "NEVER X" not "We learned X doesn't work."
3. **Always anchor to file paths** when possible — verifiable > abstract.
4. **Never duplicate** — if a rule exists in architecture.md, don't also put it in the regression fence.
5. **Prune aggressively** — if the code already shows a pattern, the rule wastes context.
