---
description: Bootstrap streaming-docs-style documentation from an existing codebase. 4-phase state machine (Discover → Skeleton → ADR/OQ → Refinement) producing module READMEs, feature records, api.md, database schema docs, sub-ERDs, master ERD, ADR table, and OQ list. Run ONCE per project, BEFORE /w-setup, when docs/ is empty or incomplete.
argument-hint: [continue | --reset | <docs-target-root>]
allowed-tools: Bash, Read, Write, Edit, Agent, Skill
---

# w-document-build-up

One-time skill that scans an existing codebase and generates a draft of the
structured documentation tree that w-task / w-doc-gate expect. Acts as the
"catch-up" mechanism: backfills docs for code already merged so future
incremental tasks (via w-task Phase 5) have something to extend.

**Run order:** `w-document-build-up` → `/w-setup` → `/w-task`.

State: `<docs_target>/.build-up/state.yaml` + `<docs_target>/.build-up/<phase>.md`.

---

## ⚠️ Invocation gate

The skill advances **only** when developer explicitly runs `/w-document-build-up`.
During a gate pause, developer may chat / edit / correct draft files — those
edits are read on the next invocation. A phase transition happens only at the
moment the skill is invoked with `continue` (or empty).

```
$ARGUMENTS:
  --reset                  → wipe .build-up/ state, restart from Phase 1
  <docs-target-root>       → first run; create state.yaml, start Phase 1
  continue / empty         → read state.yaml, advance to next phase
```

If `state.yaml` is missing and no docs-target-root provided: ask
"Target docs folder for build-up? (e.g. `docs/`, `streaming-docs/documents/`)"
and create the dir + state.yaml.

---

## Phase 1 — Discover (INTERACTIVE → GATE 1)

**Goal:** identify modules in the codebase and confirm the list with developer.

### 1.1 Spawn `code-explorer` agent

Brief:

> Survey this codebase to enumerate "feature modules" — coherent units of
> business functionality each owning a folder of related code.
>
> Look for these patterns (any subset may apply):
> - NestJS: `src/modules/<name>/` (presence of `<name>.module.ts`)
> - Next.js: `src/features/<name>/` or `src/app/(<group>)/<page>/`
> - Generic backend: `services/<name>/`, `apps/<name>/`, `packages/<name>/`
> - Domain folders: `src/domain/<name>/`, `src/<bounded-context>/`
>
> For each candidate module, report:
> - **Name** (folder name)
> - **Path** (relative to repo root)
> - **Evidence** (key file count, presence of module.ts / service.ts / resolver
>   / controller / route)
> - **Suggested NN prefix** (numeric ordering — Foundation=00, Auth=01, etc.;
>   propose based on dependency direction or alphabetical)
> - **Dependencies** (other module imports detected)
> - **Type** (api / web / shared / worker / etc.)
>
> Output as a structured table. Also report cross-cutting concerns that don't
> belong to a single module (auth guards, error handlers, shared config,
> Prisma schema) and propose how they should be documented (e.g. under
> `overview/` rather than `modules/`).

### 1.2 Write discovery.md

Path: `<docs_target>/.build-up/discovery.md`

```markdown
# Discovery — codebase module survey

## Detected modules
| NN | Module | Path | Type | Evidence | Suggested deps |
|----|--------|------|------|----------|----------------|
| 00 | foundation | src/common, src/config | shared | ... | — |
| 01 | auth | src/modules/auth | api | resolver.ts, jwt.guard.ts | — |
| 02 | user | src/modules/user | api | ... | auth |
...

## Cross-cutting
- Prisma schema: <path>
- Auth guards: <path>
- Error registry: <path>
- ...

## Web/UI modules (if applicable)
- Pages: <path>
- Features: <path>
```

### 1.3 Pause

```
Phase 1 — Discovery complete.

Found N candidate modules + M cross-cutting groups.
Open .build-up/discovery.md to review:
  • Are the module boundaries correct?
  • Are the NN prefixes in dependency order?
  • Are any modules missing or merged that shouldn't be?

Edit discovery.md to correct the list, then run /w-document-build-up to
proceed to Phase 2 (per-module skeleton generation).
```

Write `state.yaml`: `phase: "1", status: gate_pending, target: <docs_target>`.

**GATE 1:** developer edits discovery.md, runs `/w-document-build-up`.

---

## Phase 2 — Per-module Skeleton (AUTO → GATE 2)

*Triggers when `phase: "1"` + `status: gate_pending`.*

Re-read discovery.md (developer may have edited).

### 2.1 Per-module extraction (parallel)

For each confirmed module, spawn a NARROW-scoped `code-explorer` agent.
Up to 3 in parallel (single message, multiple tool calls).

Per-agent brief (substitute `<module>` and `<path>`):

> Document the module `<module>` (path: `<path>`). Output structured findings
> ready to paste into markdown documentation.
>
> 1. **Services / Domain logic**: list each public service + its responsibilities.
> 2. **API surface**:
>    - GraphQL: scan for `@Query()`, `@Mutation()`, `@Subscription()` decorators
>      and `@ObjectType()` / `@InputType()` classes
>    - REST: scan for `@Controller(...)` + `@Get/@Post/...` decorators
>    For each operation: name, type, auth (look for `@Public()` / `@UseGuards()`),
>    input DTO, return type, side effects (queue jobs, Redis writes, events).
> 3. **Prisma models**: list models defined in `schema.prisma` whose names match
>    module concerns (heuristic: model name contains module name OR is touched
>    only by this module's services). For each: columns with types + constraints,
>    indexes, FKs.
> 4. **Async work**: scan for BullMQ queue names, processor classes, Kafka/SQS
>    references. List each queue + producer + consumer + job payload shape.
> 5. **Redis / cache**: scan for Redis key patterns (`<module>:*`), pub/sub
>    channel names, distributed lock usage.
> 6. **Cross-module deps**: list imports from other module folders.
> 7. **Implementation status**: of the items found above, which look complete
>    (have tests, have happy-path logic) vs. partial (stubs, TODO comments)?
> 8. **Open questions in code**: grep `// TODO:`, `// FIXME:`, `// XXX:`,
>    `// OQ-`, `// HACK:` and list them.

### 2.2 Write per-module files

For each module, write into `<docs_target>/modules/<NN>-<module>/`:

**README.md**:
```markdown
# <module>

## Purpose
<one paragraph — derived from the services' top-level concerns>

## Implementation Status
### ✅ Complete
- <feature> (file: <path>)

### ⏳ Deferred
- <feature> (rationale: <…>)

## Depends on
- <other module>

## Blocks
- <other module>

## Async channels
- Queue: <name> (producer → consumer)
- Pub/sub: <channel>

## See also
- API surface: api.md
- DB schema: ../../database/<NN>-<module>.md
```

**api.md** (only if Step 2.1 found GraphQL/REST operations):
Use `w-api-doc`'s template — write one section per operation.

**features/** (empty subdirectory — for future tasks to fill via w-feature-record).

**workflow-links.md** (empty template):
```markdown
# Workflow Links: <module>

| Task | Folder | Started | Status |
|------|--------|---------|--------|
```

### 2.3 Write database files (if Prisma models found)

For each module with Prisma models, invoke (inline — not via skill since we're
batching) the same logic as `w-db-doc`:
- `<db_docs_root>/<NN>-<module>.md` with column tables
- `<diagrams_root>/<NN>-<module>-erd.puml` with entity blocks + FKs

### 2.4 Pause

```
Phase 2 — Skeletons written for N modules.

Files generated:
  • <docs_target>/modules/<NN>-*/README.md   (N files)
  • <docs_target>/modules/<NN>-*/api.md      (M files)
  • <docs_target>/modules/<NN>-*/workflow-links.md  (N files)
  • <docs_target>/database/<NN>-*.md         (K files)
  • <docs_target>/database/diagrams/<NN>-*-erd.puml (K files)

Spot-check 2-3 module READMEs for accuracy. Edit anything wrong (the agents
work from heuristics — they will get some things wrong). When satisfied, run
/w-document-build-up to proceed to Phase 3 (ADR + OQ extraction).
```

Write `state.yaml`: `phase: "2", status: gate_pending`.

**GATE 2:** developer reviews + corrects, runs `/w-document-build-up`.

---

## Phase 3 — ADR + OQ Extraction (AUTO → GATE 3)

*Triggers when `phase: "2"` + `status: gate_pending`.*

### 3.1 Spawn `code-architect` agent

Brief:

> Read the per-module READMEs in `<docs_target>/modules/*/README.md` plus the
> root code (entry point, app module wiring, shared config). Identify the
> non-obvious architectural decisions that are EVIDENT in the code but not
> documented as ADRs.
>
> Examples of decisions worth surfacing:
> - Choice of auth strategy (JWT vs session)
> - Async fan-out via queue vs inline
> - Soft delete vs hard delete
> - Event sourcing / append-only ledger vs mutable state
> - GraphQL code-first vs schema-first
> - Cache strategy (write-through vs invalidate-on-write)
>
> For each: state the decision, the alternative implied as rejected, and the
> consequence visible in the code. Limit to 5-10 truly non-obvious ones.

### 3.2 Write architecture-overview.md

Path: `<docs_target>/overview/architecture-overview.md`

Build the ADR table and one § Decision Details block per ADR found.
Each ADR's "Origin task" field set to "(historical — backfilled by
w-document-build-up)".

### 3.3 Extract OQs from code

```bash
git grep -nE "(TODO|FIXME|XXX|HACK|OQ-)" -- 'src/**' | head -100
```

Group by file/module. For each cluster, write an OQ entry:

Path: `<docs_target>/overview/open-questions.md`

```markdown
# Open Questions

| ID | Title | Impact |
|----|-------|--------|
| OQ-001 | <title> | <BLOCKS module / Affects module / Low urgency> |
...

---

## OQ-001 — <title>
**Surfaced from:** <file:line>
**Status:** Open

**Context**
<the comment text + immediate code context>

**Options under consideration**
- (to be filled in by developer)

**Decision needed by**
<deadline if obvious, else "next sprint">
```

### 3.4 Build master ERD

If any `<diagrams_root>/<NN>-*-erd.puml` exists from Phase 2:

Path: `<diagrams_root>/00-database-overview-erd.puml`

Merge all sub-ERD entity stubs (PK + FKs only — no full column list) into one
overview file. Add cross-module FK arrows.

### 3.5 Pause

```
Phase 3 — Architecture overview + Open Questions drafted.

Files generated:
  • <docs_target>/overview/architecture-overview.md  (N ADRs)
  • <docs_target>/overview/open-questions.md         (M OQs)
  • <docs_target>/database/diagrams/00-database-overview-erd.puml

ADRs from automated code analysis tend to miss context only humans know.
Review architecture-overview.md and:
  • Promote significant decisions (e.g. "we chose Postgres over MongoDB
    because <reason>")
  • Demote noise (sometimes a "decision" is just a default choice with no
    real alternative considered)
  • Add ADRs the code doesn't reveal (vendor selection, infra choices)

Review open-questions.md and:
  • Resolve any obvious ones inline (and document the decision as a new ADR)
  • Add OQs the code didn't surface but you know exist

When satisfied, run /w-document-build-up to proceed to Phase 4 (optional
refinement of complex modules via doc-coauthoring).
```

Write `state.yaml`: `phase: "3", status: gate_pending`.

**GATE 3:** developer reviews + corrects, runs `/w-document-build-up`.

---

## Phase 4 — Refinement (OPTIONAL, INTERACTIVE)

*Triggers when `phase: "3"` + `status: gate_pending`.*

### 4.1 Identify modules needing deeper docs

Heuristic: from Phase 2 findings, mark a module as "needs deeper docs" if any of:
- `>3 services` interacting in the same module
- State machine logic detected (terms: lifecycle, status, FSM, transitions)
- External system integration (HTTP client, webhook handler, third-party SDK)
- Business logic that took multiple files to express

Build a list. Present to developer:

```
Modules likely needing companion docs:
  1) stream      — state machine (RTMP lifecycle)        → state-machine.md
  2) monetization — external integration (PSP webhooks)  → integration.md
  3) chat        — >3 services interacting               → design.md
  4) auth        — non-obvious config (JWT TTLs, refresh) → config.md

For each, you can:
  R) Refine via doc-coauthoring (interactive — agent asks questions, you answer)
  S) Skip (skeleton is good enough for now)
  M) Manual (you write the companion doc yourself later)

Reply per module, e.g. "1:R, 2:S, 3:R, 4:M", then run /w-document-build-up.
```

### 4.2 Per-module refinement loop

For each module flagged `R`:
- **Invoke skill** `doc-coauthoring` with target file path:
  - `state-machine` candidates: `<docs_target>/modules/<NN>-<module>/state-machine.md`
  - `integration` candidates: `<docs_target>/modules/<NN>-<module>/integration.md`
  - `design` candidates: `<docs_target>/modules/<NN>-<module>/design.md`
  - `config` candidates: `<docs_target>/modules/<NN>-<module>/config.md`
- Stage 1 (Context) of doc-coauthoring: agent asks targeted questions about the
  domain, developer answers in chat
- Stage 2 (Refinement): agent drafts the companion doc; developer corrects
- Save and move to next flagged module.

For each `S`: skip — leave a `<!-- TODO: companion doc deferred -->` marker
in the module README.

For each `M`: leave the manual marker and a TODO list of suggested sections
in the README.

### 4.3 Finalize

Write `<docs_target>/README.md` (top-level index):

```markdown
# Documentation

This documentation was bootstrapped by `/w-document-build-up` on <date>.
From here on, `/w-task` keeps these docs in sync with code automatically.

## Structure
- **overview/** — architecture decisions + open questions
- **modules/<NN>-*/** — per-module docs (README, api.md, features/, workflow-links)
- **database/** — schema docs + PlantUML ERDs

## Index
| Module | API | DB | Status |
|--------|-----|----|--------|
| 00-foundation | n/a | n/a | ✅ skeleton |
| 01-auth | [api.md](modules/01-auth/api.md) | [db](database/01-auth.md) | ✅ skeleton |
...
```

### 4.4 Print suggested workflow.yaml

```
Phase 4 — Refinement complete (or skipped). Bootstrap done.

Suggested .claude/workflow.yaml paths (copy when running /w-setup):

  workflow:
    docs_root: <docs_target>
    module_docs_root: <docs_target>/modules
    feature_records_subdir: features
    api_docs_filename: api.md
    workflow_links_filename: workflow-links.md
    db_docs_root: <docs_target>/database
    diagrams_root: <docs_target>/database/diagrams
    master_erd_path: <docs_target>/database/diagrams/00-database-overview-erd.puml
    oq_docs_path: <docs_target>/overview/open-questions.md
    adr_docs_path: <docs_target>/overview/architecture-overview.md

Next step:
  1. Commit these docs in one or more PRs (recommend splitting per-module).
  2. Run /w-setup and paste the paths above.
  3. Start using /w-task — every feature task from now on keeps docs in sync.
```

Write `state.yaml`: `phase: "4", status: complete`.

---

## State transitions summary

| phase | status | Next `/w-document-build-up` triggers |
|-------|--------|--------------------------------------|
| "1" | gate_pending | Phase 2 — per-module skeleton |
| "2" | gate_pending | Phase 3 — ADR + OQ extraction |
| "3" | gate_pending | Phase 4 — optional refinement |
| "4" | complete | Skill done — proceed to /w-setup |

---

## Composition (skills + agents reused)

| Reused | Source | Used in Phase |
|--------|--------|---------------|
| `code-explorer` agent | everything-claude-code | 1 (discovery), 2 (per-module) |
| `code-architect` agent | everything-claude-code | 3 (ADR extraction) |
| `doc-coauthoring` skill | anthropic-skills | 4 (refinement) |
| `w-db-doc` inline logic | this preset | 2 (sub-ERDs) + 3 (master ERD) |
| `w-api-doc` inline logic | this preset | 2 (api.md per module) |

Heavy lifting is delegated to those skills/agents — this skill is mostly an
orchestrator with gate logic.
