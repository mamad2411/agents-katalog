---
name: data-layer-handbook
description: Prisma vs Drizzle and SQL in Next.js - when to choose relations migrations serverless drivers and pairing with database-schema-agent
tags:
  - database
  - drizzle
  - prisma
  - nextjs
version: 1.0.0
category: development
outcomes:
  - Decision matrix Prisma Drizzle raw SQL for greenfield vs legacy constraints
  - Serverless and edge driver constraints connection pooling server vs edge split
  - Pointer to database-schema-agent for Prisma deep schema work
stack:
  - next
  - prisma
  - drizzle-orm
  - typescript
last_reviewed: 2026-05-19
risk_level: low
tools_allowed: read-only
requires_user_approval: false
compatibility:
  - generic-markdown
  - skills-sh
  - cursor
  - claude-code
  - antigravity
  - codex
  - github-copilot
  - windsurf
  - gemini-cli
  - cline
  - amp
  - opencode
  - roo
  - goose
  - kilo
  - kiro-cli
  - droid
  - openclaw
  - trae
references:
  - references/stack-nextjs.md
  - references/skill-safety.md
  - references/data-layer-choice.md
---

# Instructions

## When to Use

- Use when choosing Prisma vs Drizzle vs SQL for Next.
- Prefer `database-schema-agent` after ORM choice for Prisma schema work.
- Prefer `auth-handbook` if the question is sessions, not storage.

Pick a **data layer** for **Next.js** when Prisma is not assumed.

1. **Prisma:** best when team wants **migrations**, **studio**, rich **relation** API, and mostly **Node** runtime. Use **`database-schema-agent`** for schema design and audits.
2. **Drizzle:** strong when you want **SQL-first**, lighter runtime, **edge**-friendly drivers with explicit SQL; migrations via `drizzle-kit` - verify driver supports your DB (Postgres, SQLite, etc.).
3. **Raw SQL / Kysely:** acceptable for reporting or tight performance paths - isolate in repository modules; parameterize queries (**no string concat** for user input).
4. **Serverless pooling:** avoid unbounded `new Client()` per request; use **connection pooler** (PgBouncer, Neon, Supavisor, etc.) - name pattern, not vendor mandate.
5. **Edge:** Prisma often needs **Data Proxy** or separate Node path; Drizzle edge drivers still have SQL dialect limits - align with **`edge-runtime-handbook`**.
6. **Transactions:** boundary at use-case level; retry idempotency for user-facing writes documented in **`api-handbook`**.
## Outcomes

- One-page matrix: team skill, edge need, reporting, → recommended tool.
- “If you already have X in repo, default to X” rule.

## Output Rules

No schema dumps; link to existing `schema.prisma` or `drizzle/` folder if present.

## Scope and boundaries

- **In scope:** ORM/SQL choice, pooling, edge constraints.
- **Out of scope:** distributed saga orchestration, data warehouse ETL.

## Safety

- read-only; flag SQL injection if user shows string-built queries.

## Troubleshooting

- **Too many connections:** missing pooler or Prisma `connection_limit` in serverless.
- **Type drift:** generate types from DB (`drizzle-kit pull`) vs hand models - pick one source of truth.

## Related skills

- [`database-schema-agent`](../database-schema-agent/SKILL.md) - Prisma schema design after ORM choice
- [`next-server-patterns`](../next-server-patterns/SKILL.md) - where queries run
- [`secure-dependencies`](../secure-dependencies/SKILL.md) - driver and ORM supply chain

**GitHub:** https://github.com/bh611627/skillcodex/tree/main/skills/data-layer-handbook/SKILL.md  
**npm:** https://www.npmjs.com/package/@skillcodex/skills
