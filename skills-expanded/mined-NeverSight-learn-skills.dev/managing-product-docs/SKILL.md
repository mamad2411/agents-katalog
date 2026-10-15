---
name: managing-product-docs
description: Use when user asks to create, extract, update, refine, or audit product documentation (PRD, tech stack, architecture, SRS, user stories with INVEST + Gherkin acceptance criteria, sitemap, design system, roadmap, use cases, user flows, business rules, database design, API reference, test cases, external docs) for a software project — covers greenfield init from a brief, brownfield extraction from existing code, incremental updates after scope/feature/tech/architecture/design changes, and gap audits to detect drift between docs and code.
---

# Managing Product Docs

Use this skill to produce and maintain a coherent software product documentation set. Keep `SKILL.md` as the router: load detailed guidance from `reference/` only for the docs you are creating, updating, or reviewing.

## Operating Modes

Pick one mode at the start.

| Mode | Trigger | Output |
|---|---|---|
| `greenfield-init` | New project brief or idea | Doc-set proposal + PRD first (await confirm); then mandatory, then optional docs at v1.0 Draft |
| `brownfield-extract` | Code exists, docs are missing/sparse | Discovered-scope memo + doc-set proposal + PRD first (await confirm); then docs sourced from code, tests, git, README, user validation |
| `update` | Existing docs plus scope/feature/tech/design change | Affected-doc set proposal (await confirm); then edits with version bump + Change Log + traceability |
| `review` | User asks whether docs match current code | `REVIEW_REPORT.md` findings only; do not auto-edit unless approved |

Every mode runs through the **Interview & Confirmation Protocol** below before creating or editing any artifact. Never produce the full doc set in one shot.

If mode is ambiguous, inspect repo/docs briefly and ask one focused question only when needed.

## Loading Rules

1. Always read `reference/STYLE.md` before writing or updating included docs.
2. Read only the `reference/<doc>-guide.md` files for docs selected by archetype or affected by an update/review.
3. Read `examples/*-example.md` only when you need style/pattern examples; examples are illustrative, not structures to copy.
4. Read `reference/INVEST.md` and `reference/STORY_SPLITTING.md` only for `USER_STORIES.md` generation/update/review.
5. For `DESIGN.md`, read `reference/design-spec.md` first, then `reference/design-guide.md`.

## Normative Hierarchy

1. `SKILL.md` — mode selection, loading, doc-set order, and workflow guardrails.
2. `reference/STYLE.md` — global formatting, ID registry, traceability, versioning.
3. `reference/<doc>-guide.md` — doc-specific writing strategy and quality bars.
4. `reference/INVEST.md` / `reference/STORY_SPLITTING.md` — user-story quality gates.
5. `examples/*` — non-normative examples.

## Project Archetypes

Mandatory docs for every archetype: `PRD.md`, `TECHSTACK.md`, `ARCHITECTURE.md`, `SRS.md`, `TESTCASES.md`, `ROADMAP.md`.

| Archetype | Usually include | Usually skip |
|---|---|---|
| Web App | `BUSINESS_RULES.md`, `USER_STORIES.md`, `USECASES.md`, `USERFLOWS.md`, `SITEMAP.md`, `DESIGN.md`, `DATABASE.md`, `API_REFERENCE.md`, `EXTERNAL_DOCS.md` | — |
| Backend Service / API | `BUSINESS_RULES.md`, `USECASES.md`, `DATABASE.md`, `API_REFERENCE.md`, `EXTERNAL_DOCS.md` | `SITEMAP.md`, `DESIGN.md`, `USERFLOWS.md`, usually `USER_STORIES.md` |
| Library / SDK | `API_REFERENCE.md`, `USECASES.md`, `EXTERNAL_DOCS.md` | `SITEMAP.md`, `DESIGN.md`, `USERFLOWS.md`, `DATABASE.md`, usually `USER_STORIES.md` |
| CLI Tool | `BUSINESS_RULES.md`, `USECASES.md`, `DATABASE.md` only if persistent state exists, `EXTERNAL_DOCS.md` | `SITEMAP.md`, `DESIGN.md`, `USERFLOWS.md`, usually `API_REFERENCE.md` and `USER_STORIES.md` |
| Mobile App | `USER_STORIES.md`, `USECASES.md`, `USERFLOWS.md`, `DESIGN.md`, `DATABASE.md`, `API_REFERENCE.md`, `EXTERNAL_DOCS.md` | `SITEMAP.md` |
| Internal Tool / Admin | `USER_STORIES.md`, `USECASES.md`, `SITEMAP.md`, `DATABASE.md`, `EXTERNAL_DOCS.md` | `DESIGN.md` unless visual system matters, usually `USERFLOWS.md` and `API_REFERENCE.md` |

Record skipped optional docs and reasons in PRD §Doc Set. Re-evaluate archetype when the project grows.

## Doc Artifact Map

| Output doc | Read guide | Optional example |
|---|---|---|
| `PRD.md` | `reference/prd-guide.md` | `examples/prd-example.md` |
| `TECHSTACK.md` | `reference/techstack-guide.md` | `examples/techstack-example.md` |
| `ARCHITECTURE.md` | `reference/architecture-guide.md` | `examples/architecture-example.md` |
| `BUSINESS_RULES.md` | `reference/business-rules-guide.md` | `examples/business-rules-example.md` |
| `SRS.md` | `reference/srs-guide.md` | `examples/srs-example.md` |
| `USER_STORIES.md` | `reference/user-stories-guide.md` | `examples/user-stories-example.md` |
| `USECASES.md` | `reference/use-cases-guide.md` | `examples/use-cases-example.md` |
| `USERFLOWS.md` | `reference/user-flows-guide.md` | `examples/user-flows-example.md` |
| `SITEMAP.md` | `reference/sitemap-guide.md` | `examples/sitemap-example.md` |
| `DESIGN.md` | `reference/design-spec.md`, then `reference/design-guide.md` | `examples/design-example.md` |
| `DATABASE.md` | `reference/database-guide.md` | `examples/database-example.md` |
| `API_REFERENCE.md` | `reference/api-reference-guide.md` | `examples/api-reference-example.md` |
| `TESTCASES.md` | `reference/test-cases-guide.md` | `examples/test-cases-example.md` |
| `ROADMAP.md` | `reference/roadmap-guide.md` | `examples/roadmap-example.md` |
| `EXTERNAL_DOCS.md` | `reference/external-docs-guide.md` | `examples/external-docs-example.md` |
| `REVIEW_REPORT.md` | `reference/review-report-guide.md` | `examples/review-report-example.md` |

## Source-of-Truth Order

Lower-numbered docs own upstream intent. Downstream docs refine; they do not invent scope.

1. PRD — business scope and decisions
2. TECHSTACK — technology choices
3. ARCHITECTURE — components and ADR-lite decisions
4. BUSINESS_RULES — durable policy
5. SRS — testable FR/NFR behavior
6. USER_STORIES — sprint-ready slices
7. USECASES — actor interactions
8. USERFLOWS — end-to-end journeys
9. SITEMAP — UI routes/surfaces
10. DESIGN — visual design system
11. DATABASE — physical schema
12. API_REFERENCE — API contracts
13. TESTCASES — verification coverage
14. ROADMAP — sequencing and exit gates
15. EXTERNAL_DOCS — external references registry

## Interview & Confirmation Protocol

Applies to every mode. Discovery → Interview → Recommend doc set → Confirm → generate in waves. Business scope and mandatory docs come first; optional docs only on explicit opt-in.

**HALT at every gate.** Output the doc-set proposal / PRD / wave plan, then **wait for an explicit user reply**. Do NOT infer approval from silence, from the user's original request, or from your own judgment that the proposal looks reasonable. No artifact is generated before its gate is cleared.

### 1. Discovery

Read what already exists: brief, README, manifests, config, routes/commands/pages, schema/models/migrations, tests, git history, external integrations. Use it to pre-answer questions — never ask what the code or brief already states.

### 2. Interview

Ask only **material** and **still-unknown** questions — ones whose answer changes scope, archetype, doc selection, or verification. Batch them into a single round where possible; do not drip questions across many turns. Cover, as relevant:

- Business scope, goals, success measures, out-of-scope
- Users / personas
- Archetype signals (UI? API? library? CLI? mobile? internal admin?)
- Tech stack & pinned versions
- Data / persistence needs
- Security / compliance constraints
- Integrations / external dependencies
- Release plan / milestones / deadlines
- Constraints / risks

### 3. Archetype detection

Infer archetype from Discovery signals, then confirm. Heuristics (cross-check the Project Archetypes table):

| Signal | Archetype |
|---|---|
| UI routes + DB + API | Web App |
| API handlers only, no UI | Backend Service / API |
| Publishable package manifest, no app entry point | Library / SDK |
| CLI entry point (argparse / cobra / commander) | CLI Tool |
| Mobile project (Android / iOS / Flutter / React Native) | Mobile App |
| Auth-gated internal admin surface | Internal Tool / Admin |

### 4. Recommend doc set

Present a proposal table grounded in archetype + Discovery signals. Each row: doc, Include/Skip, reason, priority label (`mandatory` / `business-scope` / `optional`):

| Doc | Include? | Why | Priority |
|---|---|---|---|
| `PRD.md` | Include | Business scope owner | business-scope |
| `TECHSTACK.md` | Include | Tech choices needed to implement | mandatory |
| `DESIGN.md` | Skip | No visual surface in this archetype | optional |

Record the final decision in PRD §Doc Set. **HALT — wait for the user to approve or edit the set.**

### 5. Generate in waves

Only after the set is confirmed:

- **Wave 1 — PRD only** (business scope). Record §Doc Set. **HALT — wait for the user to confirm scope is frozen.**
- **Wave 2 — remaining mandatory**: `TECHSTACK.md`, `ARCHITECTURE.md`, `SRS.md`, `TESTCASES.md`, `ROADMAP.md`, in Source-of-Truth Order.
- **Wave 3 — optional**: generate each only on explicit user opt-in (or the batch the user approved in step 4).

Never jump to optional or downstream docs before PRD is confirmed and mandatory docs are done.

## Core Workflows

All workflows run through the Interview & Confirmation Protocol. The notes below are mode-specific deltas, not a bypass.

### Greenfield

1. Discovery + Interview + Recommend set, then confirm (Protocol steps 1–4).
2. Wave 1: draft PRD; HALT for scope confirmation.
3. Wave 2: generate remaining mandatory docs in Source-of-Truth Order.
4. Wave 3: generate optional docs on opt-in.
5. Keep docs reader-friendly and visual when useful; run verification checks and list unresolved questions explicitly.

### Brownfield

1. Inventory README, manifests, config, routes/commands/pages, schema/models/migrations, tests, git history, and external integrations.
2. Present a discovered-scope memo, then Interview to fill gaps and confirm intent; Recommend set + confirm.
3. Generate in waves (PRD → mandatory → optional), citing sources: file paths, line numbers when available, commits, tests, or user decisions.
4. Mark inferred decisions as inferred and ask for rationale when critical.

### Update (light gate)

1. Classify change severity: patch/minor/major.
2. Present the affected-doc set (ripple from the owning source-of-truth doc); HALT for confirmation.
3. First touch the owning doc, then cascade downstream. Bump versions, update headers, append Change Log rows, and refresh traceability.
4. Re-run affected verification checks.

### Review (light gate, no doc generation)

1. Confirm the audit scope with the user.
2. Compare docs against current code/tests/config and recent git history.
3. Produce `REVIEW_REPORT.md` using `reference/review-report-guide.md`; group findings by severity and concrete fix path.
4. Do not apply fixes until the user approves them.

## Global ID Prefixes

Use the canonical registry in `reference/STYLE.md`. Common owners:

| Prefix | Owner |
|---|---|
| `F-*` | PRD features |
| `TS-*` | TECHSTACK choices |
| `C-*`, `AD-*` | ARCHITECTURE components/decisions |
| `BR-*` | BUSINESS_RULES |
| `FR-*`, `NFR-*` | SRS |
| `US-*`, `AC-*` | USER_STORIES |
| `UC-*` | USECASES |
| `UF-*` | USERFLOWS |
| `API-*` | API_REFERENCE |
| `TC-*` | TESTCASES |
| `M*` | ROADMAP |
| `EXT-*` | EXTERNAL_DOCS |

Do not invent new prefixes unless `reference/STYLE.md` is intentionally updated.

## Verification Summary

Apply only checks relevant to included docs. Detailed checks live in the guides.

- Headers/version/source fields follow `reference/STYLE.md`.
- Every downstream ID traces to its upstream owner.
- Every `FR-*`/`NFR-*` has test coverage in `TESTCASES.md`.
- When user stories are included, every `US-*` passes INVEST and every `AC-*` maps to at least one `TC-*`.
- UI routes/pages trace to use cases or flows when SITEMAP/USERFLOWS are included.
- Database tables and API endpoints trace to SRS/architecture when included.
- External dependencies and design tokens cite source files or upstream docs.
- PRD §Doc Set records included/skipped docs and reasons.

## Red Flags

Stop and re-check when:

- Any doc is being generated before the interview and doc-set are confirmed.
- Optional or downstream docs are being generated before PRD scope is confirmed.
- The full set is being produced in one shot, skipping the wave gates.
- The doc-set proposal is not grounded in codebase/brief signals.
- Approval is being inferred from silence or from the original request instead of an explicit user reply.
- PRD has unresolved scope questions but downstream docs are being written.
- A downstream doc introduces a feature absent from PRD.
- Tests are being written without SRS requirements to trace to.
- A doc is skipped without recording the reason.
- Examples are being copied verbatim instead of adapted to the project.
- DESIGN is being written without reading `reference/design-spec.md`.
