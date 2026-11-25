---
name: mvp
description: "Ship a working MVP as fast as possible. Ruthless scope, aggressive defaults, skip non-essential gates. For speed-first projects where 'done' beats 'perfect'."
---

<!-- Delete when: native Claude Code MVP mode with automatic scope-cutting and parallelization planning is available -->

# MVP Skill

Ship a working MVP fast. Cut everything that isn't core. Assume defaults. Ship ugly. Fix later.

## When to Use
- User runs `/mvp` with an idea or description
- Speed > thoroughness
- Ship working prototype first, harden later

---

## Quick Start

1. **60-second intake**: Ask max 3 blocking questions. Assume everything else.
   
   Safe assumptions:
   - Auth: email/password (simplest)
   - DB: SQLite local, Postgres hosted
   - Styling: Tailwind (fastest)
   - Testing: smoke tests only
   - Deploy: Vercel for frontend, Railway for backend

2. **Ruthless scope**: For every feature: "Does product BREAK without this?"
   - YES → MVP v1
   - NO → v2 backlog

3. **One-liner spec**: "A user can [core action]" — nothing more.

4. **Break into parallel tasks**:
   - Foundation (setup, schema, auth)
   - Parallel streams (features 2–4 in parallel)
   - Integration (wire + smoke test + deploy)

5. **Non-negotiable even in MVP**:
   - No hardcoded secrets
   - Run `npm audit` / `pip-audit` before shipping
   - All work committed
   - Lint + basic test pass

---

## After MVP Ships

Before real users:

- Run `/security-audit` on auth + API
- Run `/supply-chain` on dependencies
- Run `/quality-gate` full checks
- Migrate smoke tests to real coverage
- Design review if going public

Then promote to production mode.
