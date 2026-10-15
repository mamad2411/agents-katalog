---
name: simplicity-guide
description: Reference for choosing the simplest stack that meets a stated requirement. Use during the salvage architecture interview to frame each technical fork and record a rationale. Covers data store, frontend, realtime, auth, jobs, and deploy.
---

# Simplicity Guide

The spine of opinions behind salvage. For every technical choice, start at the
lowest rung of its ladder and climb ONLY when a written requirement forces it.

## The ladders

Each fork has a reference file under `references/`, structured identically:
one `## rung` section per rung, each with **Use when**, **Climb when**, **Cost**,
and a **Rationale template**.

- Data store → `references/data-store.md` (flat files → SQLite → Postgres)
- Frontend → `references/frontend.md` (server-rendered → HTMX → SPA)
- Realtime → `references/realtime.md` (manual refresh → polling → SSE → websockets)
- Auth → `references/auth.md` (framework sessions → library → third-party)
- Jobs → `references/jobs.md` (inline → cron → queue)
- Deploy → `references/deploy.md` (one box → containers → orchestration)

## How to consult during the interview

For each relevant fork:
1. Open the matching reference.
2. Find the lowest rung whose **Use when** the project satisfies.
3. Check the **Climb when** — climb one rung only if a *stated* requirement
   matches it. Never climb "to be safe."
4. Weigh **Cost** against the developer's maintenance ceiling (from Stage 1).
5. Record the decision in `tech-stack.md` by filling the rung's **Rationale
   template**, citing the rung (e.g. `data-store.md#sqlite`).
