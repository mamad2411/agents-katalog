# Skill Hub Registry Steward

## Purpose

Operate, audit, extend, and maintain the Skill Hub Registry without collapsing the boundaries between canonical native skills, migration evidence, external inventories, project-specific doctrine, and runtime execution state.

This root contract describes how an agent should work with the repository as a whole. It does **not** replace the individual `skills/<category>/<slug>/SKILL.md` files and it does **not** make the repository root a compiler-scanned native skill package.

## Invoke when

- adding, reviewing, repairing, normalizing, or promoting reusable skills
- auditing registry integrity, deterministic output, provenance, compatibility, or dependency relationships
- reconciling historical, migration, external, or live evidence against canonical Git-backed definitions
- preparing a candidate for Foundry qualification and possible native promotion
- maintaining Skill Hub / Sophie-X discovery, loading, compatibility, or migration contracts
- validating that repository structure and generated registry artifacts remain coherent

## Do not invoke when

- a request only needs one already-defined specialist skill; invoke that skill directly
- work concerns runtime state alone and does not change Git-backed skill definition truth
- external ecosystem presence is being treated as proof of installation, trust, compatibility, or execution
- project-specific doctrine should remain isolated in a profile or project repository

## Canonical source-of-truth hierarchy

Use the following authority order:

1. `skills/<category>/<slug>/SKILL.md` + `skill.json` — canonical native skill definitions
2. `runtime-contracts/` — invocation, migration, adapter, and compatibility boundaries
3. `profiles/` — project/domain-specific doctrine that must not contaminate native reusable skills
4. `foundry/` — qualification and promotion workflow
5. `inventory/` — historical, migration, census, duplicate, and external evidence
6. `sources/` — provenance/source records
7. `generated/` — deterministic compiler output derived from canonical native packages

Runtime databases, control planes, adapters, telemetry, and service state describe **what happens when a skill runs**. They do not silently redefine **what the skill is**.

## Native skill package contract

A native package lives at:

```text
skills/<category>/<slug>/
├─ SKILL.md
└─ skill.json
```

`SKILL.md` is the human/agent-readable operating methodology.

`skill.json` is the deterministic machine-readable contract for identity, routing, dependencies, compatibility, policy, bindings, and registry compilation.

A candidate is not native merely because it exists in `inventory/`, `sources/`, `profiles/`, a live database, an external catalog, or another repository.

## Inputs

Depending on the task, gather the minimum required evidence from:

- proposed skill purpose and reusable transformation
- existing native package content
- manifests and schemas
- historical or migration definitions
- live census/export evidence
- runtime contracts and adapters
- provenance records
- dependency and compatibility data
- external project/version/license/security evidence
- tests, validation output, and generated registry output

## Outputs

Produce only the artifacts justified by the task, such as:

- repaired or new `SKILL.md`
- repaired or new `skill.json`
- candidate or provenance record
- Foundry qualification decision
- compatibility or adapter decision
- duplicate/identity decision
- validation findings
- deterministic generated registry output
- migration reconciliation evidence
- explicit blocked-state report when promotion or repair cannot be justified

## Method

1. **Identify the population.** Determine whether the target is native, candidate, historical, migration, external, profile-specific, or runtime-only.
2. **Preserve evidence before editing.** Never rewrite archaeology or external evidence to make it look canonical.
3. **Extract the reusable transformation.** Separate general capability from project names, product doctrine, one-off prompts, and runtime implementation details.
4. **Resolve identity.** Check stable IDs, slug, category, aliases, duplicate decisions, and deployed identity constraints before assigning or changing identity.
5. **Define the methodology.** Ensure `SKILL.md` states purpose, invocation conditions, exclusions, inputs, outputs, method, quality gates, and failure behavior.
6. **Define the machine contract.** Ensure `skill.json` matches the repository schema and declares routing, dependencies, compatibility, policy, bindings, and provenance as required.
7. **Check project separation.** Project-specific identity or doctrine belongs in `profiles/` or its project source of truth unless the behavior is genuinely reusable.
8. **Check runtime separation.** Do not embed mutable runtime state into native definitions. Keep adapters and execution boundaries in their designated surfaces.
9. **Qualify dependencies and external sources.** External discovery alone never authorizes adoption or promotion.
10. **Validate.** Run repository validation, tests, deterministic build/census checks, and any task-specific reconciliation required.
11. **Inspect generated drift.** Generated registry output must be a deterministic consequence of canonical native inputs.
12. **Promote only with evidence.** Promotion must be explicit and justified; discovery or census membership is insufficient.

## Foundry qualification flow

Use this progression for non-native material:

```text
discovery
→ provenance capture
→ normalization
→ reusable-capability extraction
→ deduplication / identity resolution
→ static qualification
→ sandbox qualification when required
→ compatibility + dependency evaluation
→ security / license / policy review
→ evidence capture
→ treatment decision
→ validation
→ explicit native promotion only when justified
```

Allowed treatment decisions for external or candidate material:

- `ADOPT`
- `ADAPTER`
- `REFERENCE`
- `DEFER`
- `REJECT`

Never convert discovery directly into native execution authority.

## Migration rules

When working with deployed Skill Hub generations or live databases:

- preserve stable deployed identity unless an explicit migration decision says otherwise
- treat live data, Git files, and historical claims as distinct evidence classes
- compare source ↔ live ↔ shadow definitions field-by-field where applicable
- do not infer counts or missing records from stale UI/product claims
- shadow/audit paths must not silently affect production routing
- migration serving authority must remain explicit
- moving from DB-primary to hybrid or files-primary requires an explicit evidence gate

## External ecosystem rules

For external catalogs such as OpenClaw or future ecosystems:

- normalize into external inventory first
- retain provenance and review status
- verify current upstream version, license, dependencies, security posture, and compatibility before treatment
- keep references outside native compiler scope until explicitly promoted
- do not mirror, install, trust, or execute automatically

## Quality gates

A registry change is acceptable only when all relevant gates pass:

- native package path and naming are correct
- native package contains both `SKILL.md` and `skill.json`
- purpose and reusable transformation are explicit
- invoke / do-not-invoke boundaries are clear
- inputs and outputs are defined
- methodology is executable rather than descriptive fluff
- failure behavior forbids fabrication of execution or evidence
- manifest validates against the current schema
- IDs, slugs, aliases, and dependencies are coherent
- duplicate and collision checks pass
- project-specific doctrine remains isolated
- runtime state is not treated as canonical skill definition truth
- provenance is preserved
- external discovery has not bypassed qualification
- generated registry output is deterministic
- tests and repository checks pass for the changed surface

## Validation commands

Use the repository commands that apply to the change. The standard verification surface is:

```bash
npm run validate
npm run build
npm test
npm run check
```

Migration or external-import work may additionally require:

```bash
npm run census:v7
npm run reconcile:v7 -- path/to/live-v7-export.json
npm run import:openclaw
npm run site:build
```

Do not claim validation passed unless the command or equivalent CI evidence was actually observed.

## Change discipline

- Prefer the smallest change that restores the canonical contract.
- Do not restructure unrelated directories while repairing one skill.
- Do not rewrite preserved historical evidence merely to match current architecture.
- Do not hand-edit generated output when the correct fix belongs in canonical inputs or compiler logic.
- Do not promote candidates automatically.
- Do not create hidden runtime authority through metadata.
- Keep each project separate unless an explicit compatibility contract connects them.
- Preserve backward-compatible Skill Hub / Sophie-X contracts unless the requested task explicitly changes them.

## Failure behavior

If required source material, authority, schema information, compatibility evidence, runtime capability, provenance, or validation access is missing:

1. stop the affected promotion or destructive change;
2. identify the exact missing dependency or unresolved contradiction;
3. preserve the current canonical source of truth;
4. return a blocked or deferred state rather than inventing evidence;
5. continue only with changes that can be justified independently.

Never fabricate repository state, CI success, runtime execution, migration parity, compatibility, source provenance, installation status, or promotion approval.

## Completion criteria

A registry task is complete when the requested canonical files are updated, all relevant boundaries remain intact, deterministic/generated consequences are accounted for, validation evidence is available where required, and no candidate/external/runtime state has been silently elevated into native truth.
