---
name: consult-scars
preamble-tier: 1
version: 1.0.0
description: |
  Scar-tissue retrieval. Loads relevant past lessons from ~/.claude/lessons/
  before producing any architectural plan, so you don't repeat mistakes that
  already cost time/money. Use this skill at the START of any task involving:
  authentication, JWT, OAuth, RBAC, sessions, multi-tenancy, permissions,
  caching (any layer), cache invalidation, TTLs, database migrations, schema
  changes, ORM upgrades, indexes, distributed locking, payment flows, refunds,
  webhook handling, queue processing, retry logic, error recovery, rate
  limiting, deploys, infrastructure changes, API contract design, response
  wrappers, response formats, frontend-backend type contracts, NestJS modules,
  NestJS DI, Prisma client setup, Next.js layouts, Server Components, seed
  data, demo data, fake data generation. Triggers on prompts containing
  "design", "refactor", "migrate", "introduce", "implement", "build",
  "set up", "fix", "upgrade", "add caching", "add auth", "ship", "deploy",
  "schema change", "data model", "memory system", "agent architecture",
  "tune Claude", "context optimization", "improve Claude" or any combination
  of action verbs with the topics above. ALSO use when user asks to plan,
  spec, or architect anything non-trivial. The cost of skipping this skill
  is repeating a known-broken pattern; the cost of running it is ~30 seconds
  and ~500 tokens.
---

# Consult Scars — load lessons before you plan

You are about to design, refactor, migrate, or introduce something. Before
producing any plan or writing any code, run this protocol.

## Step 1 — Identify domains touched

List the domains your task touches. Use the lesson library structure:

- `agent-architecture` — memory, context, tooling for AI agents
- `agent-tuning` — Claude Code config, output styles, plugins
- `api-design` — API contracts, response wrappers, naming
- `auth` — JWT, OAuth, sessions, RBAC, multi-tenancy
- `caching` — cache layers, TTLs, invalidation
- `data-modeling` — schemas, seeds, soft-delete, time-series
- `external-apis` — rate limits, headers, auth, retries, pricing
- `migrations` — schema changes, downtime, rollback
- `nestjs` — NestJS-specific gotchas
- `nextjs` — Next.js / React-specific gotchas
- `prisma` — Prisma ORM specifics

A task can touch multiple domains. List all of them.

## Step 2 — Load every relevant domain file

For each domain identified, read `~/.claude/lessons/<domain>.md`.

Use the Read tool. Skim every entry — they're short. Pay attention to:

- The `Tags` field — does this lesson actually apply to your specific case?
- The `Severity` field — high-severity lessons get more weight in your plan.
- The `Never do again` field — that's the actionable rule.
- ARCHIVED entries — the body still has value as historical context but the
  rule no longer applies.

If no lesson file exists for a domain, that's fine — note it in your plan
("no scar tissue logged for X — proceeding without precedent").

## Step 3 — Cross-check your proposed approach

For each lesson loaded, ask:

- Am I about to repeat this mistake?
- Does my proposed approach explicitly avoid the failure mode?
- Is there a lesson that suggests a better approach than the one I had in mind?

If yes to any: revise your plan BEFORE presenting it.

## Step 4 — Surface lessons in your output

When you present the plan, name the lessons that informed it. Format:

> Plan: <approach summary>
>
> Lessons consulted:
>
> - **L-NESTJS-001** — avoiding ESM/CJS conflict by inlining types instead of importing from shared workspace package
> - **L-API-001** — typing the wrapper, not the inner data, in the new endpoint client
>
> Domains with no logged scars: `caching` (no `~/.claude/lessons/caching.md` yet)

This makes the lesson library's contribution visible to the user — they
can audit whether you're actually using it, and they can request specific
lessons not be applied if context has changed.

## Step 5 — Write a new lesson if something burns during the work

If during execution something breaks, surprises you, or reveals a non-
obvious gotcha:

1. Stop and write the lesson IMMEDIATELY (not later).
2. Use the format in `~/.claude/lessons/README.md`.
3. Get the next stable ID by reading the domain file's existing lesson
   IDs and incrementing.
4. Anchor the lesson to a commit SHA, PR #, or short diff.
5. Resume the task.

After-the-fact lessons lose 60% of their specificity. Write while it stings.

## Step 6 — When NOT to write a lesson

- Project-specific gotchas that don't generalize → put in
  `<project>/memory/feedback_*.md` instead.
- Personal preferences without an underlying failure mode → put in
  `~/.claude/memory/_global/MEMORY.md`.
- General software-engineering principles you'd find in any architecture
  textbook → leave them out of the lessons library.

The lessons library should grow because of pain, not because of theory.

## When this skill ITSELF is wrong

If the user explicitly says "skip scar tissue, just do it" — comply. The
skill's forcing function is for default behavior, not absolute mandate.
The user is in control.
