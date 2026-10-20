---
name: feature-delivery
description: End-to-end feature delivery orchestration for the main Claude session. Invoked when the goal is to build something completely — from idea to shipped. Triggers include "build X end to end", "deliver a feature", "deliver an app", "deliver a platform", "take this from idea to shipped", "run the whole team on this", "full delivery", "ship this", or "/deliver".
---

# Feature Delivery Skill

Full-stack delivery playbook for the main Claude Code session. Sequences the specialist agents — brainstorm → architecture → data → plan the build → track & coordinate → build → finish — scaling the process to the real size of the goal. Small goals skip phases; large goals run them all. Note the order: the design is decided first, the `lead-engineer` turns it into a technical implementation plan, and only then does the `project-manager` transcribe that plan into tracked issues — the tracking follows the technical plan, never precedes it.

Apply `principles-dry-kiss`: phases are tools, not ceremony. Do only the phases that the goal actually needs.

## Dispatch constraint (read this first)

**Only the main Claude Code session can dispatch specialist agents.** Subagents cannot spawn other subagents — the harness blocks agent nesting. When running inside a subagent this skill produces a plan only; the main session executes the dispatch loop.

## Phase order

### Phase 0 — Frame

Invoke `superpowers:brainstorming` to turn the raw goal into a concrete spec. Output a spec document at `docs/superpowers/specs/<feature-name>.md` covering: problem statement, user/system outcomes, scope boundaries (in/out), and open questions.

Skip if the goal is already fully specified with acceptance criteria.

### Phase 1 — Architecture

Invoke the `systems-architect` agent (via the `architecture` skill) to:
- Define service and bounded-context boundaries
- Produce a C4 container diagram
- Enumerate NFRs (scalability, availability, latency, cost, security)
- Select technology with explicit tradeoff tables
- Write ADRs for every significant decision at `docs/adr/NNNN-title.md`

For anything handling auth, money, PII, multi-tenant data, or untrusted input, pull in `security-architect` here to threat-model (`threat-modeling`) so security requirements seed the plan. Skip for self-contained utilities where one process/service is the obvious answer. Do not produce ADRs for decisions that are not load-bearing.

### Phase 2 — Data

Invoke the `data-architect` agent (via the `data-modeling` skill) to:
- Choose stores per workload (relational, columnar, document, key-value, vector, time-series)
- Design schemas, indexes, and constraints aligned to DDD aggregate boundaries
- Plan retention tiers (hot/warm/cold) when data volume or cost warrants it
- Model vector embeddings and retrieval pipeline if semantic search is needed
- Write a migration plan

Skip for features with no persistence layer, or where the existing schema is unchanged.

### Phase 3 — Plan the build

Invoke the `lead-engineer` agent (via `superpowers:writing-plans`) to turn the decided design + data model + threat model into one coherent implementation plan: an ordered, dependency-aware sequence of small, revertible, PR-sized tasks, each with its file-level approach, integration points, and the test cases (from `test-design`) it must satisfy. This is the **technical** plan — build order, integration seams, file contention — authored by the agent with the depth to make those calls.

Output: an implementation plan at `docs/superpowers/plans/<feature-name>.md`. This is the input Phase 4 transcribes into tracked issues. Skip only for a trivial single-task change where the order is obvious.

### Phase 4 — Track & coordinate

Invoke the `project-manager` agent (via the `project-management` skill) to represent the lead-engineer's implementation plan in the tracker and own the live state:
- Confirm done criteria
- Transcribe each plan task → a GitHub issue (carrying the plan's acceptance criteria + owner) and each plan section → an epic/milestone
- Mirror the plan's dependencies as `blockedBy` links
- Produce a sequenced delivery roadmap (wave 0, wave 1, …) and the durable progress ledger

The PM **represents and tracks** the plan — it does not re-decide the task granularity or author the sequencing (those are the lead-engineer's). Output: a GitHub issue list + local tracking doc. This becomes the execution contract for Phase 5.

### Phase 5 — Build loop

**Before dispatching any specialist, seed the stack profile.** If the project's stack differs from the plugin defaults (TanStack Start, Go/Node/Rust, AWS/CF/Hetzner, shadcn/Base UI), run `/init-stack` (or write `.ai/stack-profile.md` directly per the `stack-profile` skill) so every dispatched specialist reads the same stack. A default-stack project can skip this. Discipline (TDD/DDD/pragmatic-SOLID/DRY-KISS, ports-and-adapters, test tiers, naming) is invariant either way.

Execute the `project-management` dispatch loop — follow the `git-workflow` skill for PR sizing (small cohesive PRs, default per-issue, group trivial siblings, split big ones; squash-merge off main):

For each ready issue (wave order, blockers closed):

1. **Implement** — dispatch the assigned specialist via `superpowers:subagent-driven-development`. **Specify the model explicitly** per the `project-management` → "Model selection (required at dispatch)" rubric — an omitted model silently inherits the session's most expensive one.
   - `backend-engineer` — service & domain code, APIs, service-coupled infra (`backend-service-patterns`, `cloud-infra`)
   - `devops-engineer` — platform & DevEx: IaC provisioning, CI/CD, local dev loop, containers, observability (`cloud-infra`, `devex`, `ci-cd`). Stand up the local dev loop + pipelines early so the other specialists build against working infra.
   - `security-architect` — threat model + security posture for anything handling auth, money, PII, multi-tenant data, or untrusted input (`threat-modeling`, `security-review`). Threat-model during the architecture phase so security requirements seed the build; run the deep security audit on sensitive diffs.
   - `ux-designer` — design system, tokens, Figma authoring (`figma-design-system`, `design-theming`). **The Figma MCP is a remote OAuth server that a dispatched subagent may not reach.** ux-designer probes (`whoami`) and, if it can't write directly, returns a complete Figma build spec — the main session then executes the writes as its hands. Do not skip ux-designer or improvise the design yourself; it owns every design decision. Accept only a complete system (all components, breakpoints, states), never a token-only stub. Code Connect is **not** its job — it hands the frontend a component inventory (names + node IDs).
   - `frontend-engineer` — React + TanStack Start components, pages, and **Code Connect** for its built components (`react-component-library`, `code-connect-impl`, `pages-templates`). Code Connect publish is CLI + `FIGMA_ACCESS_TOKEN`, so it works even when the Figma MCP can't reach the subagent. **Code Connect publish requires a Figma Org/Enterprise plan** — on Pro or lower, frontend emits the Pro fallback (manual mapping doc + token-parity check) instead; the component library ships regardless.
2. **Review** — invoke `staff-engineer` on the diff.
3. **Merge** — squash-merge the PR; close the issue.
4. **Update tracking** — mark closed; check what the next wave unlocks.
5. **Repeat** — pick the next ready task.

When an implementer escalates a cross-cutting technical decision (a shared interface, an integration contract, a migration order) or gets stuck on an ambiguous spec, send it to `lead-engineer` to make the call and amend the plan — then re-dispatch. Don't let each implementer diverge on a shared decision.

Not every build needs all three specialists. A backend-only feature skips `ux-designer` and `frontend-engineer`. A UI-only feature with no new APIs skips `backend-engineer`. Scale to what the issue actually requires.

### Phase 6 — Finish

Invoke `superpowers:finishing-a-development-branch` to:
- Ensure all issues are closed and PRs merged
- Clean up branches and tracking docs
- Write a final handoff or close-out note

CI auto-versions on merge to main — do not manually bump `plugin.json`.

## Cross-cutting rules

- **Principle skills auto-apply throughout**: `principles-tdd`, `principles-ddd`, `principles-pragmatic-solid`, `principles-dry-kiss` are active in every specialist agent session without explicit invocation.
- **Run `handoff` between work chunks** — before ending any session with open issues, capture state so the next session can resume instantly.
- **Prefer a fresh session per phase** — long sessions accumulate stale context. Clean phase boundaries map cleanly to session boundaries.
- **Phases are skippable** — a one-file utility skips Phases 1–3 (no architecture, no data model, no separate plan). A proof-of-concept skips Phase 5's UX lane entirely. Scale the process to the goal.

## Worked example — logging platform

Goal: Build an observability logging platform — ingest → queue → process → store → query → UI → alerting.

### Phase 0 output (spec)

`docs/superpowers/specs/logging-platform.md`:
- **Problem**: engineers need full-text log search, live tail, and threshold-based alerts without paying Datadog prices.
- **Outcomes**: ingest ≥ 500 k events/s; p95 query < 2 s over 30-day window; alert latency < 30 s.
- **In scope**: HTTP ingest, structured log storage, log explorer UI, alert rules.
- **Out of scope**: distributed tracing, metrics, synthetic monitoring.

### Phase 1 output (architecture)

C4 container diagram: browser → TanStack Start frontend → query API → columnar store; HTTP ingestor → Kafka/NATS queue → processor → columnar store.

ADRs:
- `docs/adr/0001-columnar-store-clickhouse.md` — ClickHouse over Parquet+S3: better query latency at 30-day window, operational maturity, SQL surface.
- `docs/adr/0002-nats-jetstream-queue.md` — NATS JetStream over Kafka: lower ops overhead for target ingest rate; swap path documented if load exceeds 1 M/s.
- `docs/adr/0003-go-gin-ingestion.md` — Go+Gin for ingest: throughput requirement (500 k/s), team familiarity.

### Phase 2 output (data)

- **Hot tier**: ClickHouse on SSD, 7-day retention, all columns indexed.
- **Warm tier**: ClickHouse + S3-backed cold storage, 30-day window, compressed.
- **Cold tier**: Parquet on S3 Glacier, indefinite, query via Athena.
- Schema: `logs(ts DateTime64, service String, level Enum, message String, labels Map(String,String))` — partitioned by day, ordered by `(service, ts)`.
- Vector embeddings table for semantic search: `log_embeddings(log_id UUID, embedding Array(Float32))` — `pgvector` sidecar if semantic search is enabled.

### Phase 3 output (implementation plan)

`docs/superpowers/plans/logging-platform.md` (authored by `lead-engineer`) — the design above sequenced into a build order with the integration seams called out:
- **Foundations first**: the NATS subject + the ClickHouse `logs` schema are the shared contracts the ingestor, processor, and query API all bind to — land them before any service that depends on them.
- **Critical path**: ingestor → processor → query API → explorer UI (each needs the prior's output to test against). Alerting branches off the processor and is parallel-safe with the query API.
- **Parallel-safe & file-disjoint**: the design-system work (Figma + tokens) shares no files with the backend and runs alongside the whole backend critical path.
- Per task: the public interface, the test cases from `test-design` (e.g. ingestor — *Ingest_MalformedPayload_Returns422*, *Ingest_QueueDown_BuffersAndRetries*), and a PR-sized boundary.

### Phase 4 output (issues)

The `project-manager` breaks the plan above into tracked issues + waves (it does not re-derive the order — it transcribes the lead-engineer's sequencing into dependencies):

Wave 0 (foundations, parallelizable):
- `#1 backend-engineer: NATS subjects + ClickHouse logs schema (shared contracts)`
- `#2 ux-designer: log explorer design system + tokens in Figma`

Wave 1 (after #1):
- `#3 backend-engineer: Go+Gin ingestion service (HTTP → queue)`
- `#4 backend-engineer: log processor (queue → columnar store)`

Wave 2 (after #3, #4):
- `#5 backend-engineer: query API (full-text + time-range + label filters)`
- `#6 backend-engineer: alert rules engine + notification dispatch (parallel-safe with #5)`

Wave 3 (after #5, #2):
- `#7 frontend-engineer: TanStack Start log explorer — live tail + nuqs URL state + tanstack-form alert rules`

### Phase 5 output (PRs)

- PR #1: Shared contracts — NATS subjects + ClickHouse `logs` schema migration (the foundations everything binds to).
- PR #2: Figma design system — log explorer tokens, `LogRow`, `LiveTail`, `AlertRuleForm` components, plus the component inventory (names + node IDs) for the frontend's Code Connect.
- PR #3: Go+Gin ingestor — `/ingest` endpoint, NATS JetStream publish, Zod-validated payload schema, unit + integration tests.
- PR #4: Log processor — NATS consumer → ClickHouse batch insert, retry/backoff, health metrics.
- PR #5: Query API — full-text search, time-range, label filters, cursor pagination.
- PR #6: Alert rules engine — rule evaluation loop, Slack/PagerDuty notification dispatch.
- PR #7: TanStack Start log explorer — live tail via SSE, nuqs for URL-driven filter state, tanstack-form for alert rule authoring; Code Connect mappings (`*.figma.tsx`) wired + published for the built components.

### Phase 6 output

All issues closed. Branches deleted. `docs/superpowers/specs/logging-platform.md` annotated with final ADR links and deferred items (distributed tracing — YAGNI for now).

## Cross-references

- `superpowers:brainstorming` — Phase 0 spec
- `architecture` — Phase 1 topology, ADRs, NFRs, tech selection
- `data-modeling` — Phase 2 store selection, schema, retention tiers
- `superpowers:writing-plans` — Phase 3 implementation plan (authored by `lead-engineer`)
- `project-management` — Phase 4 decomposition, issue tracking, dispatch loop
- `superpowers:subagent-driven-development` — per-task implement → review cycle in Phase 5
- `superpowers:finishing-a-development-branch` — Phase 6 cleanup
- `git-workflow` — branching, commit conventions, PR sizing, release automation
- `handoff` — cross-phase session continuity
- `principles-dry-kiss` — KISS/YAGNI governs which phases to skip and how much process to apply
