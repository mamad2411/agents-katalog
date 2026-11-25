---
name: product-line
description: Manage the portfolio of product paths — review, activate, archive, restore, promote, fork, and check revisit triggers across the product-path manifest
type: ops
version: v0.6
required_conventions: [alignment-page]
argument-hint: "review | activate <path-id> | archive <path-id> | restore <path-id> | promote <path-id> | fork <label> [--from <skill>] | triggers"
context_intake: artifact_only
visual_tier: visual
---

## Pack Availability Guard

When recommending a skill from another pack, verify the target pack is installed via `.agents/project.json` `enabled_packs`. If it is not enabled, recommend `npx skillpacks install <pack>` from the project shell. After install, tell Codex users to start a fresh Codex CLI session if the `$` skill list remains stale. Only the currently running skill and skills verified available in the active session or project-local install state are directly recommendable. For unavailable pack skills, recommend `npx skillpacks install <pack-or-skill>`; for unavailable base skills, recommend `npx skillpacks init` before the skill.

# Product Line — Product Path Portfolio Management

Invoke as `$product-line`.

Manage product paths tracked in `research/.progress.yaml`. Product paths are research divergences — different products, apps, ICPs, expansion candidates, pivots, or competitive gaps — not git branches. Each path tracks its scope directory, status, evidence, pipeline stage, and revisit conditions.

Use `activate` when a deferred or revisit candidate path should become active research again. Use `promote` only when a research path graduates to an `apps/{slug}/` code/app scope.

## Prerequisites

`research/.progress.yaml` must exist for all modes except `fork` (which can create it). If missing, tell the user: "No product-path manifest found. Run `$idea-scope-brief` or `$customer-discovery` first — they create the manifest when multiple product directions emerge."

## Manifest Schema

The canonical manifest lives at `research/.progress.yaml`:

```yaml
active_paths:
  - "cost-intel"
max_concurrent: 1
product_paths:
  - id: "cost-intel"
    label: "Cost Intel"
    scope_path: "research/cost-intel/"
    status: active # active | deferred | archived | promoted | revisit_candidate
    source_skill: "icp"
    reason: "Why this path exists"
    archive_reason: null
    archived_at: null
    promoted_at: null
    evidence_refs: []
    revisit_trigger: null
    next_skill: "$competitive-analysis"
    pipeline_stage: "icp"
    last_touched: "YYYY-MM-DD"
```

### Backward Compatibility

- Read legacy `active_path` as `active_paths: [<value>]` when `active_paths` is absent.
- Read legacy `status: abandoned` as `status: archived`.
- On writes, remove `active_path`, write plural `active_paths`, and prefer `status: archived` instead of `abandoned`.
- Treat `status: promoted` as graduated to code/app scope, not reactivated research.
- Exclude `research/_archive/` paths from active-path selection and directory suggestions.

## Modes

### 1. `review` — Portfolio Dashboard

**Invocation**: `$product-line review`

Present a dashboard comparing all paths:

| Path | Status | Scope | Pipeline Stage | Last Touched | Evidence Maturity | Revisit Trigger |
|------|--------|-------|----------------|--------------|-------------------|-----------------|

Group by `active`, `deferred`, `revisit_candidate`, `archived`, and `promoted`. For `deferred` and `revisit_candidate` paths, highlight the revisit trigger. For `archived` paths, show `archive_reason` and `archived_at`. For `promoted` paths, show `promoted_at` and the expected `apps/{slug}/` scope.

Evidence maturity is derived from files under `scope_path` or `evidence_refs`:
- **Early** — only concept brief or initial ICP
- **Developing** — ICP plus competitive analysis, positioning, or journey map
- **Mature** — journey map plus metrics, GTM, monetization, or experiments
- **Graduated** — promoted to an app/code scope

When 3+ deferred or revisit-candidate paths exist with no recent activation, recommend `$product-line triggers`.

### 2. `activate <path-id>` — Reactivate Research

**Invocation**: `$product-line activate <path-id>`

1. Validate the path exists and has status `deferred` or `revisit_candidate`.
2. Check `max_concurrent` against the current active-path count. If at capacity, ask whether to deactivate another path or increase `max_concurrent`.
3. Ensure `scope_path` is not under `research/_archive/`. If it is archived, tell the user to run `$product-line restore <path-id>` first.
4. Scan existing research files to infer `pipeline_stage`.
5. Update the manifest:
   - Set `status: active`
   - Add the path ID to `active_paths`
   - Set `last_touched` to today
   - Set `pipeline_stage` from the scan when clearer than the existing value
6. Recommend the next skill from `next_skill` or the inferred pipeline stage.

### 3. `archive <path-id>` — Archive A Research Path

**Invocation**: `$product-line archive <path-id>`

1. Validate the path exists and is not already `archived` or legacy `abandoned`.
2. Ask for a concise archive rationale.
3. If `scope_path` is `research/{slug}/` and the directory exists, create `research/_archive/` as needed and move it to `research/_archive/{slug}/`.
4. Update the manifest:
   - Set `status: archived`
   - Remove the path ID from `active_paths`
   - Set `scope_path` to `research/_archive/{slug}/` when the directory was moved
   - Set `archive_reason`, `archived_at`, and `last_touched`
5. Present confirmation with the archived directory and rationale.

### 4. `restore <path-id>` — Restore An Archived Path

**Invocation**: `$product-line restore <path-id>`

1. Validate the path exists and has status `archived` or legacy `abandoned`.
2. If `scope_path` is `research/_archive/{slug}/` and the directory exists, move it back to `research/{slug}/`.
3. Ask whether to restore as `deferred` (default) or `active`. If active, enforce `max_concurrent`.
4. Update the manifest:
   - Set `status: deferred` by default, or `active` only when approved
   - Add to `active_paths` only when restored as active
   - Set `scope_path` back to `research/{slug}/`
   - Clear `archived_at`; keep the old archive rationale in `reason` or history, but set `archive_reason: null`
   - Set `last_touched` to today
5. Recommend `$product-line activate <path-id>` if restored as deferred.

### 5. `promote <path-id>` — Graduate To App Scope

**Invocation**: `$product-line promote <path-id>`

Use this only when research is ready to become or connect to an app under `apps/{slug}/`.

1. Validate the path exists and is not `archived` or legacy `abandoned`.
2. Derive `{slug}` from the path ID or `scope_path`.
3. Confirm or create `apps/{slug}/` during the monorepo scaffolding flow. If scaffolding requires another skill, recommend `$scaffold` or the appropriate monorepo command instead of inventing app files here.
4. Keep research docs under `research/{slug}/` as product evidence unless a separate scaffolder explicitly moves or links docs.
5. Update the manifest:
   - Set `status: promoted`
   - Remove the path ID from `active_paths`
   - Set `promoted_at` and `last_touched` to today
   - Keep `scope_path` pointing at the research evidence path
6. Present the app graduation result and the next implementation/scaffolding command.

### 6. `fork <label> [--from <skill>]` — Create A New Path

**Invocation**: `$product-line fork "Enterprise vertical" --from competitive-analysis`

1. Generate a stable product-path ID from the label.
2. Confirm that the slug is the intended product/app name, not merely an ICP, audience, or segment label.
3. Ask for supporting evidence, revisit trigger, and initial status (`active` or `deferred`).
4. Create or update `research/.progress.yaml` with the full schema fields.
5. Use `scope_path: research/{slug}/`.
6. If status is `active`, enforce `max_concurrent` and create `research/{slug}/`.
7. If status is `deferred`, create the manifest entry without forcing downstream research.

### 7. `triggers` — Check Revisit Conditions

**Invocation**: `$product-line triggers`

Scan paths with `status: deferred` or `status: revisit_candidate` and evaluate their `revisit_trigger` conditions:
- **File-based triggers** — check whether the referenced file exists.
- **Evidence-based triggers** — check active research files for relevant evidence.
- **Time-based triggers** — compare against today's date.
- **External triggers** — flag as requiring manual confirmation.

Classify each trigger as **fired**, **pending**, or **manual**. For fired triggers, recommend `$product-line activate <path-id>`.

## Output

Update `research/.progress.yaml`. `archive` and `restore` may also move product-path directories between `research/{slug}/` and `research/_archive/{slug}/`. `promote` may confirm or route creation of `apps/{slug}/`, but it does not move research docs.

## Constraints

- Do not run downstream research or implementation skills.
- Do not treat archived, legacy abandoned, deferred, revisit-candidate, or promoted paths as active research targets.
- Do not use `promote` to mean "make active"; use `activate`.
- Do not use `archive` without a documented rationale.
- Respect `max_concurrent` for active paths.
- Use product-path terminology. Never use "branch" to mean a product path.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/product-line-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md (adapted for Codex: commit and push changes to the repository primary branch).
