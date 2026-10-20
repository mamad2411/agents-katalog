---
name: mauro-crud
version: 4.1.0
description: Use when a repository belongs to the Mauro legacy PHP/MySQL CRUD family or when T0/T1/T2/T3 stage detection, Mauro CRUD maintenance, framework contracts, or T1→T2 migration knowledge is required. Pair with mauro-coding-style for shared Mauro coding/database conventions.
---

# Mauro CRUD

Shared framework knowledge for the Mauro legacy PHP/MySQL CRUD application family.

This Skill owns framework-specific contracts only. Shared PHP/MySQL/JavaScript conventions live in `mauro-coding-style`.

## Canonical ownership

The authoritative source is `ai-development-skills/skills/mauro-crud`.

Agent runtime installations are consumers. Application repositories and donor/boilerplate repositories may provide implementation evidence but do not own this Skill.

## Activate when

Use this Skill when one or more are true:
- the repository is registered or observed as Mauro CRUD;
- T0/T1/T2/T3 stage must be detected or validated;
- a Mauro CRUD maintenance/bug/feature task requires framework conventions;
- a T1→T2 conversion is being planned or executed;
- a task touches shared CRUD forms, page builder, AJAX dispatch, legacy compatibility or framework bootstrap.

Do not activate merely because the task uses PHP/MySQL.

When this Skill is active, also apply `mauro-coding-style` unless repository evidence explicitly overrides a shared style convention.

## Ownership boundary

Route responsibilities outside this Skill:
- shared Mauro coding/database/AI conventions → `mauro-coding-style`;
- end-to-end onboarding / READY_FOR_MAC / promotion → `project-onboarding`;
- generic autonomy/safety/scope → global/repository `AGENTS.md`;
- feature planning → `feature-planning`;
- bug investigation → `bug-investigation`;
- code review → `code-review`;
- durable app-specific architecture/facts → `PROJECT.md` / Knowledge DB;
- deployment/FTP → deployment workflow.

`PATTERNS.md` is not a baseline artifact for shared Mauro CRUD knowledge.

## Source-of-truth order

For a concrete repository:

1. actual repository code;
2. database/schema evidence when available;
3. project bootstrap/config/runtime paths;
4. `PROJECT.md` and registered durable project context;
5. this Skill and its references;
6. assumptions.

Never force a generic framework rule over contradictory observed project code without first classifying the difference as a project deviation or drift.

## Stage detection

Classify the repository before applying stage-specific assumptions:

- **T0** — convention-driven legacy application without the Mauro CRUD engine;
- **T1** — homegrown/scattered CRUD micro-framework without the authoritative T2 `crud/` engine/page-builder contract;
- **T2** — shared `crud/` engine with declarative `$CRUD->Page` conventions;
- **T3** — separate OOP generation, outside the normal T1/T2 maintenance path;
- **mixed/unknown** — contradictory evidence or insufficient confidence.

Always report stage, confidence and decisive evidence when stage matters. Load `references/stage-detection.md` for detailed probes.

T0, T3, mixed or low-confidence findings require an explicit architectural decision before applying T1/T2-specific transformations.

## Framework maintenance rules

- Inspect the affected execution path before changing it.
- Treat framework core and shared dispatch as high blast-radius.
- Do not edit shared `crud/` core to solve one application's local behavior when a project-level extension path exists.
- Preserve business behavior before structural cleanup.
- There is no arbitrary file-count approval rule.
- Use `mauro-coding-style` for general naming, SQL, language and compatibility conventions.

## No-invention contract

For maintenance and especially T1→T2 conversion:
- read the original implementation before writing its replacement;
- read an authoritative T2 reference implementation when T2 behavior is required;
- port observed behavior; do not invent buttons, actions, links, filters, modals, fields or business rules;
- preserve labels and targets unless the task explicitly changes them;
- real field/table/function names come from repository evidence;
- compare interactive behavior before accepting a converted page.

An action present in the new implementation with no observed source or explicit requirement is a defect until justified.

## T2 framework contract

When the repository is verified T2:

### Framework core
- the project `crud/` engine is shared core and high blast-radius;
- ordinary application tasks should use established project extension/action paths;
- implementation-specific actions, feeds and forms belong outside immutable/shared engine internals.

### Page/Form shape
A T2 page uses declarative `$CRUD->Page(...)` conventions.

Forms use the repository's established `Form` structure and `Rows` as visual rows containing field definitions. Do not replace this with an invented keyed field map.

### Save semantics
- existing-record `scheda` behavior uses update semantics;
- create/new behavior uses insert semantics;
- do not point update forms at legacy create handlers merely to preserve an old filename;
- verify actual repository behavior before assuming a page is read-only.

### AJAX
Use the repository's verified T2 dispatch contract. Do not mechanically rewrite legacy wrapper calls when the T2 compatibility layer preserves them; first determine which JS/bootstrap implementation is loaded.

Load `references/t2-contracts.md` for detailed framework behavior.

## T1→T2 migration

A stage upgrade is an explicit migration task, not ordinary maintenance.

Requirements:
1. work on a dedicated branch, not the production/default branch;
2. detect and evidence source and target stage;
3. identify an authoritative T2 donor/reference implementation;
4. preserve DB schema/domain naming unless schema change is separately requested;
5. convert in reviewable functional batches/modules;
6. preserve old behavior before structural cleanup;
7. run syntax/structural verification for every batch;
8. run runtime smoke tests when an environment is available;
9. when runtime dependencies/DB are unavailable, mark runtime checks as pending;
10. push reviewable branch state according to repository/Git workflow.

Load `references/t1-to-t2.md` for the migration sequence and compatibility strategy.

## Documentation routing

- project stage, local architecture and deviations → project `PROJECT.md`;
- optional non-obvious topology → `REPO_MAP.md`;
- reusable Mauro coding convention → `mauro-coding-style`;
- reusable Mauro CRUD framework rule → this Skill;
- generic execution rule → global/focused workflow owner;
- secrets → never documentation.

## Verification

Use the strongest practical evidence available:
- PHP syntax checks on changed PHP files;
- focused runtime/smoke tests where environment permits;
- structural checks for bootstrap/page/AJAX contracts;
- final diff inspection;
- original-vs-new behavior comparison for conversions;
- explicit statement of anything not runtime-verified.

Never claim a live DB/runtime test when only syntax/structural validation was possible.

## References

Load on demand:
- `references/stage-detection.md` — T0/T1/T2/T3 probes and confidence;
- `references/t2-contracts.md` — T2 page/form/AJAX/core contracts;
- `references/t1-to-t2.md` — migration and compatibility playbook.
