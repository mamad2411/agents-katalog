---
name: refactor-web-02-modules
description: Frontend business-module division auditing and governance tool (version-adaptive). Use this skill when the user asks for a "module division check", "module structure governance", "business module splitting", "module dependency check", "sub-module structure" review, or "create business module" scaffolding on a Vue 3 + TypeScript frontend. It selects the matching versioned ruleset from the project `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`). This is step 2 of 5 of the frontend governance lane in the refactor-chain bundle.
---

# Frontend Business Module Division Check & Governance — refactor-chain · Web lane · step 02/05

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** Frontend project governance (versioned) · **Position:** step 02 of 05 · **Prerequisite:** refactor-web-01-structure · **Next:** refactor-web-03-components.
**Adaptivity:** Selects the versioned ruleset from the project `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`).

## Purpose
This skill audits and governs the division of business modules in a Vue 3 + TypeScript frontend project. Based on the `framework-web2-server` packaging convention, it enforces standardized constraints on module division, each module's internal structure, inter-module dependencies, and module size. Because module conventions can differ between project versions, the skill detects the version declared in `package.json` and loads the corresponding ruleset before executing. It offers two functions: module checking (scanning `modules/` to surface non-compliant module structures and division problems) and module governance (adjusting module structure to match the standard, or scaffolding a compliant module from templates).

## When to use
- The user wants to verify whether module division is compliant. Trigger phrases: "module division check", "module structure check", "module dependency check".
- The user wants to create a new business module. Trigger phrases: "create business module", "new module", "module scaffold".
- The user wants to remediate module division problems. Trigger phrases: "module structure governance", "business module splitting", "module rectification".

## Rules enforced
The versioned ruleset (`S10` series, 10 rules) is applied against the standard module layout. Modules are divided by **business domain**, not by page type; a candidate becomes its own module when it satisfies at least 3 of these decision criteria: business independence, data boundary, functional cohesion, team ownership, reusability. The standard internal layout is `modules/{module-name}/` containing `views/` (e.g. `ListView.vue`, `DetailView.vue`, `FormView.vue`), `components/` (module-private), `composables/`, `api/index.ts`, `types/index.ts`, and `index.ts` (module export entry).

| ID | Check | Severity | Rule |
|------|--------|---------|------|
| `S10-01` | Internal structure completeness | ERROR | Each module must contain `views/`, `api/`, `types/`, `index.ts` |
| `S10-02` | Module size control | WARNING | A single module's `views/` file count must not exceed 10 |
| `S10-03` | Module naming convention | ERROR | Module directory names use kebab-case |
| `S10-04` | Export entry completeness | ERROR | Each module must have an `index.ts` export entry |
| `S10-05` | API–Types correspondence | WARNING | Files in `api/` and `types/` should map one-to-one |
| `S10-06` | Sub-module structure convention | WARNING | Sub-modules should follow the same structure as modules |
| `S10-07` | Inter-module dependency direction | ERROR | Directly referencing another module's internal files is forbidden |
| `S10-08` | Route correspondence | WARNING | Each module should have a corresponding route configuration |
| `S10-09` | Store correspondence | WARNING | Modules using state management should have a corresponding store |
| `S10-10` | View naming convention | WARNING | Page components under `views/` use PascalCase |

**Dependency-direction constraints:** `modules/A → components/`, `modules/A → services/`, and `modules/A → utils/` are permitted. Forbidden: `modules/A → modules/B/` internals and `modules/A → modules/B/api/` (must be brokered through a shared layer). When a module's `views/` exceeds 10 files, split it into sub-modules by sub-business-domain.

## Procedure
1. **Step 0 — detect version (never skip).** Read `package.json` at the project root, extract `version`. If it cannot be extracted, default to `3.6.0-SNAPSHOT`. Match against the version map: exact match wins; otherwise match the `major.minor` series and take the newest directory in that series; otherwise fall back to the `3.6.0-SNAPSHOT` baseline and emit a warning.
2. **Step 1 — load rules.** Read the `REFERENCE.md` in the resolved version directory under `references/original/versions/<version>/`.
3. **Step 2 — execute.** For a check: scan all subdirectories under `src/modules/`, apply rules `S10-01` through `S10-10` (detailed in `scripts/check-rules.md`), then report compliant items, violations, and fix suggestions. For scaffolding: confirm module name (kebab-case), business domain, and whether sub-modules are needed; generate the standard module from `templates/module-structure-template.md`; register the route under `framework/router/modules/` and update the export entry; then validate against the same rules.

## Guardrails
- Do not change business logic/behavior; structural + standards refactoring only.
- Present a split plan and wait for explicit user confirmation before splitting; synchronize every `import` path after moving files, and keep route configuration in sync after any module structure change.

## Verify
- Version was detected from `package.json` (or the documented fallback applied) and the correct version directory was loaded.
- Every `S10-01` through `S10-10` rule was evaluated and reported.
- Each module contains `views/`, `api/`, `types/`, and `index.ts`; directory names are kebab-case and view components are PascalCase; no module references another module's internals; routes and stores stay in sync.
- All `import` paths still resolve after any file moves.

## References
The exhaustive original rules, versioned rule sets, and component/page templates are bundled verbatim under `references/original/` (source of truth). Consult them for per-version detail and code samples.

## Chain position
Runs after refactor-web-01-structure. On success the orchestrator advances to refactor-web-03-components. `refactor-code-solid` runs by default as the final step of the lane.
