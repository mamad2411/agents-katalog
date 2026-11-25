---
name: onboarding-map
description: Plan signup, setup, activation, first success, onboarding drop-offs, and time-to-value for each lifecycle persona
type: analysis
version: v0.4
argument-hint: "[optional: app, persona, or onboarding segment]"
interview_depth: full
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` inside Codex, or `npx skillpacks install <pack>` from the project shell, instead of the target skill.

# Onboarding Map

Invoke as `$onboarding-map`.

Create the stage-level onboarding plan that expands `research/journey-map.md`.

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

1. Resolve product-path scope using the same `research/{slug}/` convention as `$journey-map`.
2. Read `research/.progress.yaml` when present. Normalize `active_path` (singular legacy) to `active_paths` (plural list) when reading; treat legacy `abandoned` as `archived` and exclude archived/deferred/revisit/promoted paths plus `research/_archive/` scopes from active target selection. Scope the onboarding map to the active product path by default.
3. Require `research/journey-map.md` or `research/{slug}/journey-map.md`; if missing, recommend `$journey-map`.
4. Load ICP, journey map, specs, customer feedback, metrics, and current product routes/components when present.
5. Interview and recommend around: signup entry points, account creation, required setup, imports/integrations, team invites, empty states, first-session guidance, first 5 minutes/hour/day, aha threshold, drop-offs, recovery, and support touchpoints.
6. Present the proposed onboarding model before writing.
7. Write `research/onboarding-map.md` and `research/onboarding-map-interview.md` in flat mode, or `research/{slug}/onboarding-map.md` and `research/{slug}/onboarding-map-interview.md` when product-path scope is active, after validation.

## Output Shape

```markdown
# Onboarding Map

> Based on: research/journey-map.md
> Date: YYYY-MM-DD

## Summary
## Personas And Entry Points
## Signup And Setup Flow
## Activation Path
## First Success
## Drop-Offs And Recovery
## Instrumentation Needs
## Product Gaps
## Next Steps
```

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/onboarding-map-{topic}.html`.

## Constraints

- Stay stage-specific; do not rewrite the whole journey map.
- Make onboarding steps concrete enough to drive specs, UX variations, and instrumentation.
- End with `## Next Steps`, preferring `$conversion-map`, `$lifecycle-metrics`, `$ux-variations` as context dictates.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
