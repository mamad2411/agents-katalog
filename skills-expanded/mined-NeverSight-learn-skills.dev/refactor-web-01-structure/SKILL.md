---
name: refactor-web-01-structure
description: Frontend project directory-structure auditing and governance tool (version-adaptive). Use this skill when the user asks for a "project structure check", "directory convention review", "layered architecture audit", "project initialization", "scaffold generation", or "project structure governance" of a Vue 3 + TypeScript frontend. It selects the matching versioned ruleset from the project `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`). This is step 1 of 5 of the frontend governance lane in the refactor-chain bundle.
---

# Frontend Project Structure Check & Governance — refactor-chain · Web lane · step 01/05

**Bundle:** refactor-chain (orchestrated, self-healing refactor chain-of-skills).
**Lane:** Frontend project governance (versioned) · **Position:** step 01 of 05 · **Prerequisite:** none — entry step · **Next:** refactor-web-02-modules.
**Adaptivity:** Selects the versioned ruleset from the project `package.json` `version` (supports `3.6.0-SNAPSHOT`, `3.6.1-SNAPSHOT`, `3.7.0-SNAPSHOT`).

## Purpose
This skill audits and governs the top-level directory structure of a Vue 3 + TypeScript frontend project. Based on the `framework-web2-server` packaging convention and the Alibaba frontend development standard, it enforces standardized constraints on the top-level directories, layered architecture, component tiers, and reference direction. Different project versions may carry structural differences, so the skill first detects the version declared in `package.json` and loads the corresponding ruleset before executing. It offers two functions: structure checking (scanning the project tree to surface non-compliant issues) and structure governance (adjusting the directory layout to match the standard, or scaffolding a compliant project from templates).

## When to use
- The user wants to verify whether the project directory structure is compliant. Trigger phrases: "project structure check", "directory convention", "layered architecture audit".
- The user wants to initialize the standard structure of a new project. Trigger phrases: "project initialization", "scaffold generation", "set up project".
- The user wants to remediate an existing project's structure. Trigger phrases: "project structure governance", "directory rectification", "structure optimization".

## Rules enforced
The versioned ruleset (`S9` series, 8 rules) is applied against the standard layered architecture. The canonical `src/` layout is: `assets/` (with `styles/`, `icons/`, `images/`), `components/` (with `common/`, `layout/`, `business/`), `composables/`, `modules/`, `framework/` (with `router/`, `store/`, `plugins/`, `directives/`, `config/`), `services/` (with `http/`, `api/`), `utils/`, and `types/`.

| ID | Check | Severity | Rule |
|------|--------|---------|------|
| `S9-01` | Top-level directory completeness | ERROR | `src/` must contain the 7 standard directories |
| `S9-02` | `assets` directory structure | WARNING | Static assets should be split into `styles`/`icons`/`images` |
| `S9-03` | `components` tiering | ERROR | Must be divided into `common`/`layout`/`business` three tiers |
| `S9-04` | Composite component directory form | WARNING | Multi-file components should be organized as directories |
| `S9-05` | `framework` directory structure | WARNING | The framework layer should be split by `router`/`store`/`plugins`/etc. |
| `S9-06` | `services` directory structure | WARNING | The service layer should contain `http/` and `api/` subdirectories |
| `S9-07` | `composables` naming | ERROR | File names must begin with the `use-` prefix |
| `S9-08` | No cross-layer references | ERROR | References between layers must follow the dependency direction |

**Legal reference directions:** `modules/ → components/`, `modules/ → composables/`, `modules/ → services/`, `modules/ → utils/`, `modules/ → types/`, `components/ → composables/`, `components/ → utils/`, and `framework/ → modules/` (route registration only) are permitted. Forbidden: `components/ → modules/`, `utils/ → modules/`, `services/ → modules/`, and `modules/A → modules/B/` internals.

## Procedure
1. **Step 0 — detect version (never skip).** Read `package.json` at the project root, extract `version`. If it cannot be extracted, default to `3.6.0-SNAPSHOT`. Match against the version map: exact match wins; otherwise match the `major.minor` series and take the newest directory in that series; otherwise fall back to the `3.6.0-SNAPSHOT` baseline and emit a warning that no matching ruleset was found.
2. **Step 1 — load rules.** Read the `REFERENCE.md` in the resolved version directory under `references/original/versions/<version>/`.
3. **Step 2 — execute.** For a check: scan all directories and files under `src/`, apply rules `S9-01` through `S9-08` (detailed in `scripts/check-rules.md`), then produce a report of compliant items, violations, and fix suggestions. For scaffolding: confirm project name and type, generate the standard structure from `templates/project-scaffold-template.md`, then validate the result against the same rules.

## Guardrails
- Do not change business logic/behavior; structural + standards refactoring only.
- Present a governance plan and wait for explicit user confirmation before moving anything; confirm the user has backed up the project before adjusting directories, and synchronize every `import` path after moving files.

## Verify
- Version was detected from `package.json` (or the documented fallback applied) and the correct version directory was loaded.
- Every `S9-01` through `S9-08` rule was evaluated and reported.
- The `src/` tree matches the standard layered architecture, `composables` files use the `use-` prefix, and no forbidden cross-layer references remain.
- All `import` paths still resolve after any file moves.

## References
The exhaustive original rules, versioned rule sets, and component/page templates are bundled verbatim under `references/original/` (source of truth). Consult them for per-version detail and code samples.

## Chain position
Runs after none (this is the entry step). On success the orchestrator advances to refactor-web-02-modules. `refactor-code-solid` runs by default as the final step of the lane.
