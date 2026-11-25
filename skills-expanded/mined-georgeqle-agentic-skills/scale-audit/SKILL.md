---
name: scale-audit
description: Evaluate codebase against enterprise ICP for production readiness, compliance, and multi-stakeholder journey coverage
type: analysis
version: v0.4
interview_depth: none
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Scale Audit — Enterprise Production Readiness

Invoke as `$scale-audit`.

Automated analysis that evaluates the codebase against `research/enterprise-icp.md`. Identifies gaps for enterprise deals — stakeholder journey coverage, compliance, infrastructure, and operations.

## Prerequisites

`research/enterprise-icp.md` (or `research/{slug}/enterprise-icp.md`) must exist. If not, tell the user to run `$enterprise-icp` first.

## Process

### 0. Product-Path Scope Resolution

Resolve research scope by product path before using code or app structure as a hint:

1. If `$ARGUMENTS` names a non-archived `research/{slug}/` directory or a product-path ID whose `scope_path` points there, use that path. Treat `{slug}` as the product/app name, not the ICP, audience, or segment label.
2. If `$ARGUMENTS` names only `research/_archive/{slug}/` or a manifest entry with `status: archived` or legacy `status: abandoned`, stop and warn that the path is archived; do not write or update scoped outputs there.
3. Read `research/.progress.yaml` when present. Normalize legacy `active_path` to `active_paths` on read and write back `active_paths` on manifest updates. Treat legacy `abandoned` as `archived`; exclude `archived`, `abandoned`, `deferred`, `revisit_candidate`, `promoted`, and any `scope_path` under `research/_archive/` from active target selection.
4. If active product paths exist in the manifest, use those paths. If multiple active paths exist, ask which one to target unless this skill explicitly supports cross-path output.
5. If no active manifest target exists, list non-archived product directories under `research/`, excluding `research/_archive/` and dot directories. Auto-select only when exactly one exists; ask when multiple exist.
6. If no product directories exist, use flat `research/` single-product mode.
7. Detect monorepo/app/package structure only as a secondary hint. Suggest creating a missing `research/{slug}/` product path when code clearly exposes an app, but do not require code or monorepo detection before using `research/{slug}/`.

When product path `{slug}` is active, read and write research under `research/{slug}/`, specs under `specs/{slug}/`, and treat top-level `research/*.md` files as flat-mode documents or cross-path summaries.

### 1. Load Context & Evaluate

1. Read `research/enterprise-icp.md` (or `research/{slug}/enterprise-icp.md`), `research/icp.md` (or `research/{slug}/icp.md`), `research/mvp-gap.md` (or `research/{slug}/mvp-gap.md`) (if they exist), codebase, and in-progress/advisory work from `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, and `tasks/recurring-todo.md` (if they exist).
2. Evaluate the codebase across:
   - **Per-Persona Journey Coverage** — Can each stakeholder complete their workflow?
   - **Onboarding Gaps** — Self-serve, team, SSO-provisioned, migration, training
   - **Compliance Readiness** — SOC 2, GDPR, HIPAA, encryption, secrets management
   - **Infrastructure Readiness** — Multi-tenancy, scaling, DR, observability, CI/CD
   - **Operational Readiness** — Incident response, SLA monitoring, support, customer success
   - **Escalated Startup Gaps** — Unresolved MVP gaps now critical at enterprise scale
3. Tag gaps: `hard-blocker`, `soft-blocker`, or `differentiator`. Estimate effort (S/M/L/XL).

## Deliverables

- `specs/scale-audit.md` (or `specs/{slug}/scale-audit.md`) — Gap analysis with stakeholder coverage matrix, compliance matrix, priority tags, and `$user-flow-map` prompts for each unspecced flow/design-shape gap

The output file must end with a `## Next Steps` section containing a **Recommended** item and 2–4 other contextual options. Choose the recommendation by the first matching condition:

1. IF any `hard-blocker` lacks flow/design shape or a full implementation spec: `$user-flow-map [top blocker]` — map the highest-priority enterprise blocker into concrete screen flow, decisions, branches, states, and recovery paths before UI/layout planning.
2. IF enterprise stakeholder journey context is missing: `$journey-map enterprise` — map enterprise stakeholder journeys before sequencing build work.
3. IF startup gaps escalated and `research/mvp-gap.md` is missing or stale: `$mvp-gap` — re-evaluate startup readiness first.
4. IF enterprise SLA or compliance gaps lack closure metrics: `$metrics` — define metrics covering enterprise SLAs.
5. OTHERWISE: `$roadmap` — sequence the already-specced enterprise work into implementation phases.

Only recommend `$roadmap` as the primary next step when every hard-blocker already has a full spec or is already tracked in `tasks/roadmap.md`, `tasks/todo.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md`.

## Task Classification

When this skill produces follow-up work, file it by execution semantics:

- Immediately actionable implementation or documentation work goes in `tasks/todo.md`.
- Human-only external actions tied to automated steps go in `tasks/manual-todo.md` with `_(blocks: Step N.X)_` or `_(after: Step N.X)_`; repo edits, SDK wiring, generated assets, local commands, tests, audits, and authenticated CLI/API work stay in `tasks/todo.md`.
- One-time condition-gated records, baselines, or future measurements go in `tasks/record-todo.md` with source, condition, non-blocking reason, evidence, and promotion rule.
- Cadence-based reviews, playtests, adoption checks, investor updates, retros, or docs-health checks go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Analysis only — do not make code changes.
- Every gap must cite specific evidence.
- Distinguish "first enterprise deal" from "100th enterprise deal."
- Include `$user-flow-map <topic>` prompts for gaps lacking flow/design shape or full specs. Use `$ux-variations --layout-mode <topic>` only when flow and UI requirements already exist but layout alternatives are missing.
- `## Next Steps` must be the final section in the output file, with a recommended next step and 2–4 other contextual options.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/scale-audit-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
