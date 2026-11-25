---
name: stack-architect
description: Choose the exact right tech stack before building any software — frontend, backend, database, cache, ORM, auth, hosting, deployment, CI/CD, backups, monitoring, security, email, payments, storage and every supporting service. Use this skill whenever the user is starting a new project, says "I want to build...", asks "what should I use for...", "which framework/database/hosting", "best stack for X", compares technologies (Next.js vs TanStack Start, Postgres vs MongoDB, VPS vs Vercel), plans architecture, prepares to scaffold a repo, or is about to write the first line of code for a website, web app, SaaS, mobile app, desktop app, API, bot, CLI, data pipeline, AI/LLM app, game, IoT or embedded system — even if they never say the word "stack".
---

# Stack Architect

Pick the right stack *before* any code exists, explain why, and hand over a decision record the user can build from. A wrong early choice (database, auth, hosting) is the most expensive mistake in software, so this step deserves care.

## Core philosophy (apply to every decision)

1. **Boring by default, novel on purpose.** Choose proven, well-documented tools. Pick something new only when it solves a real problem the boring option can't.
2. **Fit the project, not the hype.** A landing page and a multi-tenant SaaS need different stacks. Classify first, then choose.
3. **One language where possible.** TypeScript end-to-end (or Python end-to-end) cuts context switching, shares types, and halves hiring/learning cost.
4. **Postgres unless proven otherwise.** It covers relational data, JSON, full-text search, vectors (pgvector), queues and time series (TimescaleDB) well enough for most apps.
5. **Speed comes from locality.** Database next to the app server, server near users, indexes, then caching. Network hops kill latency more than engine choice.
6. **Match operations to the team.** Self-hosting is cheap in money and expensive in attention. Solo devs with no ops time should lean managed; people who enjoy ops can self-host.
7. **No premature scale.** No microservices, Kubernetes, Kafka or multi-region until a measured need exists. A monolith on one good server handles far more than people think.
8. **Data safety is non-negotiable.** Every stack decision includes backups (tested restores), secrets handling and auth that isn't hand-rolled crypto.
9. **Reversibility matters.** Prefer choices that are easy to leave (standard SQL, S3-compatible storage, Docker, open protocols) over deep vendor lock-in, unless the lock-in buys a lot.
10. **Verify freshness.** Tech moves fast. Before finalizing, check current versions and maturity (see "Freshness check").

## Workflow

### Step 1 — Load the house defaults

Read `references/00-house-defaults.md` first. It holds the owner's preferred stack per project type. These win over generic recommendations unless the project's requirements clearly rule them out — and if they do, say so explicitly.

### Step 2 — Gather requirements (ask only what's missing)

Infer whatever the conversation already answers. Ask at most 3–5 questions per round, the ones that would actually change the stack. Key dimensions:

| Dimension | Why it changes the stack |
|---|---|
| What it is and who uses it (public, customers, internal staff) | Archetype, SEO, auth model |
| Login? Roles? Organizations/teams (multi-tenant)? | Auth provider, data model, row-level security |
| Data shape (relational, documents, time series, files, vectors, graphs) | Database family |
| Expected scale (users, requests/sec, data size) in year 1 | Hosting tier, caching, pooling |
| Realtime needs (chat, live dashboards, collaboration) | WebSockets/SSE, Durable Objects, Phoenix |
| SEO / public content | SSR/SSG vs SPA |
| Platforms (web, iOS, Android, desktop, offline) | Mobile/desktop frameworks, sync |
| Team skills and size | Language, framework |
| Budget and ops appetite | Managed vs self-hosted |
| Compliance, data residency, on-prem requirements | Region, cloud, self-hosting |
| Timeline (hackathon vs long-lived product) | Speed vs robustness trade-off |
| Integrations (payments, email, maps, AI, existing company systems) | Supporting services |

If the user wants speed ("just pick"), skip questions and state the assumptions you made.

### Step 3 — Classify the project

Match it to one or more archetypes in `references/01-project-types.md`. Many projects are hybrids (e.g., SaaS + marketing site + mobile app); handle each part and how they share auth, API and data.

### Step 4 — Decide layer by layer

For each layer, read only the reference files needed:

| Layer | Reference |
|---|---|
| Frontend frameworks, UI, state, forms | `references/02-frontend.md` |
| Backend languages, frameworks, API styles | `references/03-backend.md` |
| Databases, ORMs, cache, search, vectors, queues | `references/04-data-layer.md` |
| Authentication and authorization | `references/05-auth.md` |
| Hosting, deployment, CI/CD, IaC, domains/CDN | `references/06-deployment.md` |
| Backups, disaster recovery | `references/07-backups-dr.md` |
| Monitoring, logging, security hardening | `references/08-observability-security.md` |
| Mobile, desktop, extensions, CLI | `references/09-mobile-desktop-other.md` |
| Data engineering, analytics, ML, LLM/AI apps | `references/10-data-ai.md` |
| Realtime, collaboration, messaging | `references/11-realtime.md` |
| Payments, email, storage, CMS, search, maps, i18n | `references/12-supporting-services.md` |
| Scaling path, performance, cost | `references/13-scaling-cost.md` |
| Common mistakes to avoid | `references/14-anti-patterns.md` |

For every choice, have a one-line reason and a named alternative ("use X because...; switch to Y if..."). This makes the decision reviewable.

### Step 5 — Freshness check

Before presenting, verify anything version- or maturity-sensitive: new frameworks, recently released majors, deprecated libraries, pricing changes, acquisitions. Use web search if available, or run `scripts/check_versions.sh <npm-packages...>` / `pip index versions <pkg>`. If you can't verify, flag the item as "verify before use". The reference files carry a "last reviewed" date; treat anything older than ~6 months as needing a check.

### Step 6 — Output the Stack Decision Record

Use the template in `assets/stack-decision-record.md`. Always include:
- Project summary and assumptions
- The full stack table (every layer, including "none needed" where applicable)
- Why each choice, and the alternative
- Architecture sketch (text or Mermaid)
- Folder structure
- Environment variables / secrets list
- Backup and disaster-recovery plan
- Security checklist
- Cost estimate (rough monthly)
- Scaling path (what changes at 10x and 100x)
- Risks and open questions
- First-week build plan

Keep it proportional: a landing page gets a short record; a SaaS gets the full one.

### Step 7 — Scaffold (only if asked)

If the user wants to start building, generate the init commands, config files (Dockerfile, docker-compose, Caddyfile, CI workflow, .env.example, backup script) and folder structure for the chosen stack. Use official CLIs (`npm create ...`, `uv init`, etc.) over hand-written boilerplate when they exist.

## Decision shortcuts (when you need a fast answer)

- Static marketing/landing/blog/docs → Astro (or Next.js if it'll grow into an app) on Cloudflare.
- Web app with login → TanStack Start or Next.js + Postgres + Drizzle + Better Auth; self-hosted on a VPS behind Cloudflare, or managed on Vercel/Railway.
- API only → Hono (TS) or FastAPI (Python) + Postgres.
- Mobile → Expo (React Native) sharing a TypeScript API.
- Desktop → Tauri (Electron only if you need Node APIs or Chromium consistency).
- Data/ML → Python, Polars/DuckDB, FastAPI for serving, Postgres/ClickHouse for storage.
- LLM app → TypeScript or Python with the provider SDK directly, Postgres + pgvector, streaming UI.
- Realtime collab → Yjs + a sync provider (Liveblocks, Durable Objects, Hocuspocus).
- CLI → Go or Rust for distributed binaries; Python (Typer) or Node for internal tools.
- Embedded → C/C++ or Rust on ESP-IDF/Zephyr; MQTT to a Postgres/Timescale backend.

These are starting points; the reference files hold the nuance.

## Tone

Be decisive. Give one recommendation per layer, not a menu, then the main alternative. Explain trade-offs in plain language. When the user's own assumption is right, say so; when it's wrong, say why and what to do instead.
