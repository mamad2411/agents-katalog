---
name: enterprise-stack-review
description: "Tech stack decision phase for the enterprise pipeline. Auto-detects which technology domains need decisions (runtime, framework, database, auth, etc.), presents options with decision matrices, and locks choices into stack-decisions.json for downstream consumption by enterprise-plan. Incumbent bias for existing projects. Only triggers on FULL path. Use between enterprise-brainstorm and enterprise-plan."
---

# Enterprise Stack Review

## Global Precheck

Before reading further, writing artifacts, delegating, or changing files, run:

```bash
enterprise-precheck --skill enterprise-stack-review
```

If it exits non-zero, stop and report stderr verbatim. Do not hand-craft packet files or evidence markers to bypass it.

### LEARNED BEHAVIORS

See `.codex/enterprise-state/repo-best-practices.json` — apply with `DOMAIN_TAG=STACK_REVIEW`, `STAGE=stack-review`.



You are a technology evaluator. You take the Technical Design Document from `enterprise-brainstorm` and the stack profile from `enterprise-discover`, determine which technology decisions are needed, present options, and lock decisions before planning begins.

**Input:** TDD at `docs/designs/YYYY-MM-DD-<slug>-tdd.md` + `.codex/enterprise-state/stack-profile.json`
**Output:** `.codex/enterprise-state/stack-decisions.json` + `docs/designs/YYYY-MM-DD-<slug>-stack.md`

```
/enterprise-stack-review docs/designs/2026-03-09-sync-alerts-tdd.md
/enterprise-stack-review   (auto-detects most recent TDD)
```

---

## WHEN THIS RUNS

- **FULL path only.** QUICK and STANDARD skip this phase entirely.
- **After BRAINSTORM, before PLAN.** The TDD defines what needs to be built. This phase decides what to build it WITH.
- **Auto-skip on existing projects** if all required domains are already resolved in stack-profile.json. Announce the skip:
  ```
  STACK REVIEW — SKIPPED
  All required technology domains already resolved in stack-profile.json.
  Existing stack covers: [list domains]
  Proceeding to PLAN.
  ```

---

## THREE PHASES

```
DETECT     (auto)       — scan TDD + stack-profile, classify domains needed
EVALUATE   (with user)  — present options per domain, user picks
LOCK       (auto)       — produce stack-decisions.json + audit doc
```

One touchpoint with the user: the EVALUATE phase where they choose technologies. DETECT and LOCK are autonomous.

---

## PHASE 1: DETECT

Goal: Determine which technology decision domains this feature requires. Don't ask the user what domains to evaluate — figure it out from the TDD and current stack.

### Step 1: Read Inputs

1. **Read the TDD** — understand what capabilities the feature needs (real-time? payments? file uploads? new UI? new API?)
2. **Read stack-profile.json** — understand what technologies are already in use
3. **Read stack-traps.json** — understand known pitfalls with current stack

### Step 2: Classify the Project

| Classification | Criteria | Behavior |
|---------------|----------|----------|
| **Greenfield** | No stack-profile.json OR profile has <3 resolved domains | All 18 domains evaluated |
| **Existing + New Domain** | stack-profile.json exists, but TDD requires capabilities not covered | Only unresolved domains evaluated |
| **Existing + Explicit Review** | User passed `--review-stack` flag or said "review our tech choices" | All domains re-evaluated (incumbent pre-selected) |
| **Fully Resolved** | All domains the TDD needs are already in stack-profile.json | Auto-skip with announcement |

### Step 3: Scan for Templates

Check these locations for reusable project templates (in order):

1. `.codex/templates/` (project-local)
2. `~/.codex/templates/` (user-global)
3. `~/claude-harness/templates/` (harness distribution)
4. `~/Projects/` (sibling projects as reference)
5. Current project root (for `.codex-template.json`)

**Template metadata format** (`.codex-template.json`):
```json
{
  "name": "express-api-starter",
  "stack": {
    "runtime": "node",
    "framework": "express",
    "database": "postgresql",
    "orm": "raw-sql",
    "testing": "jest"
  },
  "description": "Express API with PostgreSQL and Jest"
}
```

If a matching template is found, pre-populate decisions from it. User still confirms.

### Step 4: Map Required Domains

Scan the TDD for capability signals and map to decision domains:

| TDD Signal | Domain(s) Triggered |
|-----------|-------------------|
| New tables, schema changes | database, orm |
| New API endpoints | framework, runtime |
| New UI pages/components | ui_components, state_management |
| Authentication/authorization | auth |
| WebSocket, SSE, polling | real_time |
| Payment processing, billing | payments |
| File upload/download, S3 | file_storage |
| Email sending, notifications | email |
| Full-text search, filtering | search |
| Performance requirements | caching, monitoring |
| Background jobs, queues | queues |
| Docker, hosting, CI | deployment, ci_cd |
| Test strategy mentions | testing |

### Step 5: Present Required Domains

```
STACK REVIEW — DETECT
═════════════════════

Project classification: [greenfield / existing+new / explicit review]
Stack profile: [found at path / not found]
Template match: [template name / none]

Domains requiring decisions:
  [x] framework      — TDD requires new API endpoints
  [x] real_time      — TDD specifies WebSocket for live updates
  [x] ui_components  — TDD includes new dashboard page

Already resolved (from stack-profile.json):
  [=] runtime        — node (locked)
  [=] database       — postgresql (locked)
  [=] testing        — jest (locked)

Not needed for this feature:
  [ ] payments, file_storage, email, search

Add or remove any domains? (Enter to proceed)
```

**Wait for user confirmation.** They can add domains they want reviewed or skip ones they consider decided.

---

## PHASE 2: EVALUATE

Goal: For each open domain, present 2-4 options with a structured decision matrix. Recommend one. User picks.

### The 18 Decision Domains

| # | Domain | Key Question |
|---|--------|-------------|
| 1 | **runtime** | What language/runtime? (Node, Deno, Bun, Python, Go, Rust) |
| 2 | **framework** | What web framework? (Express, Fastify, Hono, Next.js, Django, Gin) |
| 3 | **database** | What primary database? (PostgreSQL, MySQL, SQLite, MongoDB, DynamoDB) |
| 4 | **orm** | How to talk to the DB? (Raw SQL, Knex, Prisma, Drizzle, TypeORM, Sequelize) |
| 5 | **auth** | How to authenticate? (JWT, session, OAuth, Passport, Clerk, Auth0) |
| 6 | **state_management** | Frontend state? (React hooks, Zustand, Redux, Jotai, TanStack Query) |
| 7 | **ui_components** | Component library? (shadcn/ui, MUI, Ant Design, Radix, custom) |
| 8 | **deployment** | Where to host? (Render, Vercel, AWS, Railway, Fly.io, self-hosted) |
| 9 | **testing** | Test framework? (Jest, Vitest, Playwright, Cypress, pytest) |
| 10 | **ci_cd** | CI/CD pipeline? (GitHub Actions, GitLab CI, CircleCI, Jenkins) |
| 11 | **real_time** | Real-time strategy? (WebSocket, SSE, polling, Socket.io, Pusher) |
| 12 | **payments** | Payment processor? (Stripe, PayPal, Square, Shopify Payments) |
| 13 | **file_storage** | File storage? (S3, R2, local disk, GCS, Azure Blob) |
| 14 | **email** | Email provider? (SendGrid, Postmark, SES, Resend, Mailgun) |
| 15 | **search** | Search engine? (PostgreSQL FTS, Elasticsearch, Meilisearch, Algolia, Typesense) |
| 16 | **monitoring** | Observability? (Sentry, Datadog, New Relic, Grafana, custom logging) |
| 17 | **caching** | Cache layer? (Redis, Memcached, in-memory, CDN, none) |
| 18 | **queues** | Job queue? (BullMQ, pg-boss, SQS, RabbitMQ, custom pg queue) |

### Decision Matrix Format

For each open domain, present:

```
DOMAIN: [name]
═════════════

Current: [incumbent technology, if any] ← PRE-SELECTED (change only with strong reason)

| Criterion        | [Option A]  | [Option B]  | [Option C]  |
|-----------------|-------------|-------------|-------------|
| Fit for task    | [1-5]       | [1-5]       | [1-5]       |
| Maturity        | [1-5]       | [1-5]       | [1-5]       |
| Learning curve  | [1-5]       | [1-5]       | [1-5]       |
| Integration     | [1-5]       | [1-5]       | [1-5]       |
| Cost            | [free/paid] | [free/paid] | [free/paid] |
| Migration path  | [easy/med/hard] | [easy/med/hard] | [easy/med/hard] |

Recommendation: [Option X] — [1 sentence why]
Incumbent bias: [STAY / SWITCH — reason]

Your choice? ([A]/B/C or keep current)
```

### Evaluation Rules

1. **Incumbent bias is STRONG.** For existing projects, the current technology is pre-selected. Present it as the default. The user must explicitly choose to switch. Switching requires a compelling reason documented in the audit trail.

2. **2-4 options per domain.** Not 1 (no choice) and not 10 (decision paralysis). Pick the most relevant options for the project context.

3. **Score objectively.** Fit = how well it solves THIS specific need. Maturity = production-readiness. Learning curve = team ramp-up time. Integration = how well it works with the rest of the stack. Don't inflate scores for technologies you "like."

4. **Cost matters.** Free tier limits, per-seat pricing, usage-based billing. Flag anything that gets expensive at scale.

5. **Migration path matters.** How hard is it to switch away later? Vendor lock-in is a real cost. Prefer technologies with standard interfaces.

6. **Present all domains together**, not one at a time. Let the user see the full picture before deciding. Group related domains (e.g., database + ORM, framework + deployment).

### Batch Presentation

```
STACK REVIEW — EVALUATE
════════════════════════

Here are the technology decisions needed for [feature name].
Existing choices are pre-selected (marked ←). Override only if you have a strong reason.

[Domain 1 matrix]
[Domain 2 matrix]
[Domain 3 matrix]

Summary of recommendations:
  framework:     Express ← (incumbent, fits well)
  real_time:     Socket.io (best integration with Express)
  ui_components: shadcn/ui (matches existing Tailwind setup)

Confirm these choices, or tell me what to change.
```

**Wait for user to confirm or adjust.**

---

## PHASE 3: LOCK

Goal: Produce machine-readable and human-readable artifacts recording the decisions.

### Step 1: Write stack-decisions.json

Save to `.codex/enterprise-state/stack-decisions.json`:

```json
{
  "slug": "<slug>",
  "created": "YYYY-MM-DDTHH:mm:ss.sssZ",
  "classification": "greenfield | existing_new_domain | explicit_review | fully_resolved",
  "template_used": null,
  "domains_evaluated": ["framework", "real_time", "ui_components"],
  "domains_skipped": ["payments", "file_storage"],
  "domains_inherited": ["runtime", "database", "testing"],
  "decisions": {
    "runtime": {
      "choice": "node",
      "version": "20.x",
      "source": "inherited",
      "reason": "Existing project runtime"
    },
    "framework": {
      "choice": "express",
      "version": "4.18",
      "source": "incumbent",
      "reason": "Existing framework, no reason to switch",
      "alternatives_considered": ["fastify", "hono"],
      "incumbent_override": false
    },
    "real_time": {
      "choice": "socket.io",
      "version": "4.x",
      "source": "new_decision",
      "reason": "Best Express integration, team familiarity",
      "alternatives_considered": ["ws", "sse"],
      "incumbent_override": false,
      "packages_to_install": ["socket.io", "socket.io-client"]
    }
  },
  "constraints": [
    "Must run on Render (no WebSocket sticky sessions without pro plan)",
    "PostgreSQL 15 — no extensions beyond pg_trgm"
  ],
  "locked": true,
  "locked_by": "enterprise-stack-review",
  "locked_at": "YYYY-MM-DDTHH:mm:ss.sssZ"
}
```

### Step 2: Write Stack Audit Document

Save to `docs/designs/YYYY-MM-DD-<slug>-stack.md`:

```markdown
# Stack Decisions: [Feature Name]
**Date:** YYYY-MM-DD | **Classification:** [type]
**TDD:** docs/designs/YYYY-MM-DD-<slug>-tdd.md

## Decisions

### [Domain Name]
**Choice:** [technology] [version]
**Source:** [inherited / incumbent / new_decision]
**Reason:** [why this was chosen]
**Alternatives considered:** [list with brief rejection reasons]

[Repeat for each domain]

## Constraints
- [constraint 1]
- [constraint 2]

## Template
[Template used, or "No template — decisions made from scratch"]
```

### Step 3: Update Pipeline State

Update `.codex/enterprise-state/<slug>.json`:
```json
{
  "stages": {
    "stack_review": { "status": "complete", "completed_at": "..." }
  }
}
```

### Step 4: Announce Completion

```
STACK REVIEW — COMPLETE
═══════════════════════

Decisions locked for [N] domains:
  [domain]: [choice] ([source])
  [domain]: [choice] ([source])
  ...

Artifacts:
  Machine-readable: .codex/enterprise-state/stack-decisions.json
  Audit trail:      docs/designs/YYYY-MM-DD-<slug>-stack.md

Technology choices are now locked. enterprise-plan will use these decisions.
Proceeding to PLAN.
```

---

## SKIP LOGIC

### Auto-Skip Conditions (all must be true)

1. Path is NOT `--review-stack`
2. `stack-profile.json` exists
3. Every domain the TDD requires is already resolved in stack-profile.json
4. No new capability domains detected in the TDD

When auto-skipping:
1. Still create `stack-decisions.json` with all `source: "inherited"` entries
2. Mark `stack_review` stage as `skipped` (not `complete`)
3. Announce the skip with the list of inherited decisions
4. Proceed directly to PLAN

### Force Review

User can force a full review even on existing projects:
```
/enterprise --full --review-stack
```

This re-evaluates all domains with incumbent pre-selected but changeable.

---

## ARTIFACT VALIDATION

| This Skill | Required Upstream | Produces |
|-----------|-------------------|----------|
| enterprise-stack-review | TDD at `docs/designs/*-tdd.md` | `stack-decisions.json` + `docs/designs/*-stack.md` |

**Missing TDD:** `BLOCKED: enterprise-stack-review requires a TDD. Run /enterprise-brainstorm first.` STOP.

---

## QUALITY GATE

Before locking, verify:

| Check | Pass If |
|-------|---------|
| Every required domain has a decision | Zero unresolved domains |
| Every decision has a reason | No empty `reason` fields |
| Every non-inherited decision has alternatives | `alternatives_considered` is non-empty |
| JSON is valid | `JSON.parse()` succeeds |
| Audit doc matches JSON | Domain count and choices match |
| No banned words in reasons | Zero instances of "probably", "maybe", "might" |

---

## ANTI-PATTERNS

| Don't | Do Instead |
|-------|-----------|
| Evaluate all 18 domains on an existing project | Only evaluate domains the TDD actually needs |
| Auto-pick technologies without user input | Present options, let user decide |
| Switch incumbents without strong justification | Pre-select incumbent, require explicit override |
| Present 10 options per domain | 2-4 focused options based on project context |
| Skip this phase "because we already know" | The audit trail is the point — even confirming incumbents is valuable |
| Evaluate technologies you haven't used | Score based on documented capabilities, not assumptions |
| Recommend bleeding-edge for production | Maturity score exists for a reason |
