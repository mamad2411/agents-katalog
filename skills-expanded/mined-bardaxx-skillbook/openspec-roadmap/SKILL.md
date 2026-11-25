---
name: openspec-roadmap
description: Decomposes a PRD or large epic into prioritized OpenSpec slices in openspec/roadmap.md and keeps slice lifecycle in sync with propose, apply, and archive. Use when a PRD exists but work is still one mega proposal, when breaking a feature into multiple OpenSpec changes, when picking the next slice, or when updating roadmap status after OpenSpec steps.
---

# OpenSpec Roadmap

Bridge **PRD / large epic** → **multiple OpenSpec changes** using **`openspec/roadmap.md`**. Do not replace OpenSpec CLI skills (`openspec-propose`, `openspec-apply-change`, `openspec-archive-change`); orchestrate them and keep the roadmap current.

Roadmap format and templates: [REFERENCE.md](REFERENCE.md). The consumer repo uses exactly one roadmap file at `openspec/roadmap.md`.

## When to use

| Situation | Action |
|-----------|--------|
| PRD exists, no execution plan | **Bootstrap** → `openspec/roadmap.md` |
| Need next unit of work | Pick highest-priority slice with status `Ready` |
| Slice is `Ready` | Delegate to `openspec-propose` using **exact** `Candidate OpenSpec change id` (1:1 slice → change folder) |
| Change approved / implementing | Delegate to `openspec-apply-change`; set slice `Applying` |
| Change done | Delegate to `openspec-archive-change`; set slice `Archived` |
| Upstream only conversation | Create a `PRD.md` file first, then bootstrap |

## Orchestration

```
`PRD.md` file / tracked issue
    ↓
openspec-roadmap → openspec/roadmap.md (concise slices)
    ↓ (per slice, status Ready)
openspec-propose → openspec/changes/<Candidate OpenSpec change id>/
openspec-apply-change → implementation
openspec-archive-change → archive
    ↓
openspec-roadmap → update slice status + progress log
```

## File layout

| Artifact | Path |
|----------|------|
| Roadmap | `openspec/roadmap.md` |
| Roadmap config | `openspec/config.yaml` (`openspec_roadmap`) |
| Temporary roadmap assets | `openspec/.temp_assets/` |

The roadmap is a **planning file**, not an OpenSpec change. Do **not** duplicate proposal/design/tasks content from `openspec/changes/` into the roadmap.

Temporary working files used to prepare or apply slices (for example `audit.md`, checklists, scratch analysis notes, or intermediate outputs) must be stored under `openspec/.temp_assets/`.
These files are ephemeral support artifacts and must not be committed.

## Token budget and loading scope

Use `openspec/config.yaml` to keep context bounded. Default to these constraints unless the repo has stricter values:

- Mode: default roadmap format (preferred).
- Load only:
  - `openspec/roadmap.md`
  - selected slice
  - linked OpenSpec change
  - directly referenced files
- Do not load the full PRD unless the selected slice is ambiguous.
- Respect token ceilings from config before adding optional context.
- `openspec/config.yaml` is reference-only guidance for limits and loading; it must never be used to regenerate, rewrite, or recreate OpenSpec specs.

## Slice ↔ change

- **1:1** for implementable slices: each slice has a `Candidate OpenSpec change id` that becomes one change under `openspec/changes/`.
- **Exception:** doc-only / audit slices may use a single `audit-*` change.

### Change id naming rule (mandatory)

- Always prefix `Candidate OpenSpec change id` with the slice id lowercased, followed by the slice title slug.
- Format: `<slice-id-lower>-<slice-title-kebab>`.
- Example: `T10 - audit legacy test harness` -> `t10-audit-legacy-test-harness`.
- Keep `Spec link` aligned with the same id: `openspec/changes/<change-id>/`.
- If the slice title changes while the slice is still non-executed (`Ready` or `Spec Proposed`), update both the candidate id and spec link to keep them aligned.

### At propose (mandatory)

When delegating to `openspec-propose` for a slice in `Ready`:

1. Read `Candidate OpenSpec change id` from that slice block in `openspec/roadmap.md`.
2. Pass that exact id to `openspec-propose` so the change folder is `openspec/changes/<change-id>/`.
3. Do **not** invent a new slug from the goal, PRD text, or conversation — the roadmap id is the source of truth.
4. If `Candidate OpenSpec change id` is missing or does not match `<slice-id-lower>-<slice-title-kebab>`, fix the roadmap first, then propose.
5. After propose, set `Spec link` and progress log to the same id; reject mismatched folder names.

Example: `### T09 - Location Search And Proposal Add Discovery` with candidate id `t09-location-search-and-proposal-add-discovery` → propose into `openspec/changes/t09-location-search-and-proposal-add-discovery/`.

Why this matters: stable 1:1 mapping between slice headings, roadmap status, change folders, and archive paths.

## Slice IDs

| Prefix | Use |
|--------|-----|
| `F` | Product feature slices |
| `R` | Refactoring slices (no intended behavior change) |
| `T` | Testing and quality slices |
| `D` | Documentation-only slices |
| `I` | Infrastructure/tooling slices (optional) |

Number sequentially within prefix (`F01`, `R02`, …).

Prefix decision rules:

- Use `F` when user-visible behavior or API behavior changes.
- Use `R` for structural code improvements without intended behavior changes.
- Use `T` when the primary output is tests, coverage, or reliability harness work.
- Use `D` when the primary output is documentation/runbook/spec support text.
- Use `I` for CI, build, tooling, or environment changes.
- Split mixed slices into smaller slices when possible (for example `R` + `T`).

## Status model

Fixed lifecycle: `Ready` → `Spec Proposed` → `Applying` → `Applied` → `Archived`, plus `Blocked`.

| Transition | Roadmap update | Delegate to |
|------------|----------------|-------------|
| Pick slice | — | — |
| Change created | `Spec Proposed`; `Spec link` = `openspec/changes/<Candidate OpenSpec change id>/` | `openspec-propose` using **exact** `Candidate OpenSpec change id` |
| Implementation started | `Applying`; branch/notes optional | `openspec-apply-change` |
| Code/tests verified | `Applied`; tests + validation commands | (during apply) |
| Change archived | `Archived`; archive path + date | `openspec-archive-change` |
| Cannot proceed | `Blocked`; open question + recommendation | — |

Follow the **Agent update checklist** in [REFERENCE.md](REFERENCE.md) at each step.

## Parallel execution policy

OpenSpec supports multiple open changes, but lifecycle transitions must stay deterministic.

- **Allow parallel proposals:** multiple slices can be in `Spec Proposed`.
- **Limit active implementation:** keep at most **2** slices in `Applying` at once.
- **Critical-area safeguard:** allow at most **1** `Applying` slice at a time for critical domains (for example payments, auth, checkout).
- **Keep `next` atomic:** one `next` command moves exactly one lifecycle gate for one slice.

## Spec verification gate (mandatory)

Between `propose`, `apply`, and `archive`, always run the repository OpenSpec spec verification command and fix any issues before continuing.

- after `openspec-propose`: verify spec health before moving to `openspec-apply-change`
- after `openspec-apply-change`: verify spec health before moving to `openspec-archive-change`
- after `openspec-archive-change`: verify spec health before selecting the next slice

If verification fails, stop progression, resolve issues, re-run verification, then continue.

## Modes

### 1. Bootstrap

Create or update `openspec/roadmap.md` from a PRD or epic:

1. Read PRD/issue, `CONTEXT.md` (domain terms), and `AGENTS.md` (OpenSpec + GitNexus gates).
2. **Legacy migration (mandatory when present):** if `openspec/TIMELINE_*.md` or `openspec/programs/*.md` exists, run [legacy migration](REFERENCE.md#legacy-migration-one-time) **before** writing the roadmap.
   - **Merge** slice content into the single canonical file **`openspec/roadmap.md`** (fixed path; no `<context>` suffix).
   - **Delete** every legacy file after a successful merge. Do **not** `git mv` / rename `TIMELINE_*` → `roadmap.md` and do **not** keep legacy paths as fallbacks.
   - If `openspec/roadmap.md` already exists, merge legacy slices into it (resolve id collisions); do not create a second planning file.
3. Create or update `openspec/config.yaml` with `openspec_roadmap` defaults and token/context limits.
4. Ensure `.gitignore` contains `openspec/.temp_assets/` (create/update it if needed).
5. Decompose into short, actionable slices.
6. Write roadmap sections per [REFERENCE.md](REFERENCE.md) and [ROADMAP_SKELETON.md](ROADMAP_SKELETON.md): header, how-to, status model, compacted history, slices, dependency map, recommended execution order, agent checklist.
7. Link PRD at top (`PRD:` issue URL or path).
8. **Register the workflow in agent docs** — see [Agent documentation](#agent-documentation) below.
9. Do **not** run `openspec-propose` until user asks to start a slice.

**Parameters** (adapt per roadmap):

- `scope` — what the roadmap covers
- Priority scale — default P0 (urgent) / P1 / P2
- `principles` — optional global constraints (testing, security, etc.)
- `execution_order` — ordered slice list; note when reordered
- Item kind — `F` | `R` | `T` | `D` (`I` optional) per slice

### 2. Add slice / lifecycle

- **Add slice:** append one `### <ID> - Title` block using the default skeleton (see REFERENCE).
- **Update lifecycle:** change status and progress log only; link paths, do not copy OpenSpec artifacts.
- **Pick next:** highest priority among `Ready`, respecting execution order unless user overrides.
- **Reorder:** update Recommended Execution Order + short note why.

## Quick commands

Support lightweight command-style prompts that map to deterministic actions on `openspec/roadmap.md`.

| Command | Intent | Required input | Expected action |
|---------|--------|----------------|-----------------|
| `status` | Show roadmap state | none by default | Summarize slice counts by status, current blockers, and recommended next 1-2 slices. |
| `next:dry` | Preview the next OpenSpec gate | none by default | Resolve the active slice and return exactly one next gate action (`propose` or `apply` or `archive`) without executing it. |
| `next` | Execute one OpenSpec gate | none by default | Resolve the active slice and execute exactly one lifecycle gate: `Ready` -> run `openspec-propose` with that slice's `Candidate OpenSpec change id`; `Spec Proposed` -> run `openspec-apply-change`; `Applied` -> run `openspec-archive-change`. Run OpenSpec spec verification after the gate, fix issues if any, update roadmap, and stop. |
| `add "<feature description>"` | Add in-flight feature slice | feature intent only | Generate a compliant slice id and concise title, create a new slice block with minimum fields, and place it at the best point in execution order (not necessarily next), with a short rationale. |
| `add-next "<feature description>"` | Force immediate insertion | feature intent only | Generate a compliant slice id/title, create a new slice block, and place it as the next executable slice when valid; if dependencies block immediate insertion, place it at the earliest valid slot and mark it as forced in pipeline. |
| `start <slice-id>` | Start a specific slice | slice id | Validate slice exists and is actionable, then move lifecycle forward (or report blocker) and point to delegate skill. |
| `update <slice-id> "<feature delta>"` | Update scope of a planned slice | slice id + scope delta | Allowed only for non-executed slices (typically `Ready` or `Spec Proposed`): update goal/files/notes from the new intent, re-evaluate dependencies, and reorder execution as needed. |
| `block <slice-id>` | Mark work as blocked | slice id + blocking reason | Set `Blocked`, capture open question, and suggest an unblock path. |
| `deprecate <slice-id>` | Remove from active roadmap safely | slice id + reason | Mark slice as deprecated in-place (without deleting history), remove it from active execution order, log replacement/follow-up if any, and reorder remaining queue when needed. |
| `restore <slice-id>` | Re-activate deprecated slice | slice id | Clear deprecation marker, choose lifecycle status (usually `Ready`), reinsert in execution order, and reorder if needed. |
| `reorder` | Re-prioritize queue | ordering rationale | Update Recommended Execution Order and add a short reason note. |

Command handling rules:

1. Always operate on `openspec/roadmap.md` unless the user gives another path explicitly.
2. Keep command responses concise and operational: current state, decision, and exact next action.
3. Never skip OpenSpec delegation steps: `openspec-propose` / `openspec-apply-change` / `openspec-archive-change`.
4. On `next`, `start`, or any `Ready` → propose transition: use the slice's `Candidate OpenSpec change id` verbatim for the change folder name; never substitute a goal-derived slug.
5. Always update the roadmap after any command that changes lifecycle state.
6. For `add` and `add-next`, do not require user-provided slice id or title. Generate both from intent using the repository prefix/sequence rules and preserve uniqueness.
7. For `add`, do not append blindly to the end. Evaluate dependencies, risk, and leverage against existing slices, then insert the slice at the most suitable position in `Recommended Execution Order`.
8. When `add` or `add-next` causes reordering, explicitly report inserted position, concise rationale, and whether it changes the next recommended slice.
9. For `add-next`, insert as the nearest valid next position. If hard dependencies prevent immediate placement, place at the earliest valid slot, explain why, and add a short note that it was forced in pipeline.
10. For `update`, reject lifecycle-only edits; use it only for feature-scope updates on non-executed slices. If a slice is already `Applying`, `Applied`, or `Archived`, do not mutate scope and return a follow-up recommendation (for example create a new slice via `add`).
11. For `reorder`, `add`, `add-next`, `update`, `deprecate`, and `restore`, enforce folder-name consistency for non-applied slices only:
    - if execution order or slice title changes and a related `openspec/changes/<change-id>/` folder already exists for a slice in `Ready` or `Spec Proposed`, rename that folder to the new `<slice-id-lower>-<slice-title-kebab>` value
    - update `Candidate OpenSpec change id`, `Spec link`, and any in-roadmap references accordingly
    - do not rename folders for `Applying`, `Applied`, or `Archived` slices
12. For `deprecate` and `restore`, run reorder logic whenever queue consistency or priority is impacted.
13. For `next`, execute one gate only and stop. Never chain propose + apply + archive in a single `next` call.
14. For `next`, stop immediately on blocker, failed verification/tests, or missing required approval; record progress up to the reached step and return the stop reason with the exact next manual action.
15. After every `propose`, `apply`, and `archive`, run the repository OpenSpec spec verification command; if it reports issues, resolve and re-run before proceeding.
16. If temporary helper files are needed during roadmap work, place them only under `openspec/.temp_assets/` and keep them out of version control via `.gitignore`.

Deprecation policy:

- Prefer **deprecate over delete** for slices that are no longer planned, to preserve auditability.
- Keep deprecated slices in the file with a clear marker in `Notes` and `Progress log` (include date and reason).
- Exclude deprecated slices from `Recommended Execution Order`; add a short note if they were replaced.
- Hard delete a slice only when the user explicitly asks for permanent removal.

## Per-slice minimum fields

Lite mode fields only: Status, Goal, Candidate OpenSpec change id, Spec link, Files to inspect, Notes, Progress log.

Do not switch to a full template by default. Keep roadmap entries short and operational.

## Anti-overengineering gate

Do not use `openspec-roadmap` for:

- bugfixes under 30 minutes
- isolated copy/UI tweaks
- one-file refactors
- exploratory spikes

## Repository agent instructions

Coding agents discover repo rules from **repository agent instruction files** (commonly `AGENTS.md`, sometimes additional entrypoints per repo). When this skill is **first adopted** in a repo, or when bootstrapping a roadmap, ensure those files document the roadmap layer — do not rely on the skill folder alone.

### When to update

| Trigger | Action |
|---------|--------|
| Skill copied into repo for the first time | Add or merge **OpenSpec Roadmap** section in agent instruction files |
| Bootstrap of `openspec/roadmap.md` | Ensure agent docs reference `openspec/roadmap.md` and `openspec-roadmap` |
| User asks only for lifecycle on an existing roadmap | Update roadmap only; skip instruction files unless section is missing |

### Files to patch

1. **Primary instruction file** (required) — usually `AGENTS.md`: extend `## OpenSpec Feature Workflow` or add the section from [REFERENCE.md](REFERENCE.md#agent-docs-snippet).
2. **Secondary entrypoints** (required when the repo uses them) — mirror the same OpenSpec Roadmap block in every file that loads agent rules for that repo.
3. **One canonical wording** — pick the primary file as source of truth; keep mirrors aligned.

Use the **skill path actually installed** in routing tables (e.g. `.agents/skills/openspec-roadmap/SKILL.md`, `skills/openspec-roadmap/SKILL.md`).

### What instruction files must say

- Large PRD/epic work uses **`openspec-roadmap`** before multiple `openspec-propose` calls.
- Slices and status live in **`openspec/roadmap.md`**.
- One implementable slice → one OpenSpec change; the roadmap tracks status, not artifact content.
- After propose / apply / archive, update the roadmap and delegate to the OpenSpec CLI skills.
- Roadmap uses the default concise format.
- Token budget is enforced via `openspec/config.yaml` (`openspec_roadmap`).

### Idempotency

- If the **OpenSpec Roadmap** subsection already exists and matches, do not duplicate.
- If wording differs only slightly, reconcile to one canonical block and mirror to secondary entrypoints.

Snippets and a routing table template: [REFERENCE.md — Agent docs snippet](REFERENCE.md#agent-docs-snippet).

## Repo gates (delegate, do not duplicate)

- **OpenSpec:** tests and production behavior changes require a change under `openspec/changes/` before implementation.
- **GitNexus:** explore + impact analysis before editing application symbols (see `AGENTS.md`).
- **Domain language:** use terms from `CONTEXT.md` in slice text and when invoking propose.

## Related skills

| Skill | When |
|-------|------|
| `PRD.md` file | No formal PRD yet |
| `openspec-propose` | Slice `Ready` → create change at `openspec/changes/<Candidate OpenSpec change id>/` (exact id from roadmap) |
| `openspec-apply-change` | Implement approved change |
| `openspec-archive-change` | After completion |
| `grill-with-docs` | Slice text needs domain alignment |
| `gitnexus-exploring` / `gitnexus-impact-analysis` | Before app symbol edits |

## Anti-patterns

- Using verbose, spec-like prose inside `openspec/roadmap.md`.
- One mega OpenSpec change for an entire PRD when slices are independent.
- Duplicating `proposal.md` / `design.md` / `tasks.md` content in the roadmap.
- Skipping roadmap updates after propose / apply / archive.
- Inventing a propose folder name from goal/PRD text instead of the slice's `Candidate OpenSpec change id`.
- Installing the skill or bootstrapping a roadmap without updating repository agent instructions — other sessions will miss the roadmap layer.

## Additional resources

- Overview and intent (agents): [README.md](README.md)
- Roadmap template and checklists: [REFERENCE.md](REFERENCE.md)
