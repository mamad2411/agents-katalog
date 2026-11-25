---
name: dogfood
description: Derive owner/operator dogfood scenarios from product evidence and active-use cadence, then produce adoption instructions and manual evaluation checks
type: analysis
version: v0.3
argument-hint: "[optional: scenario focus, persona, feature, or release]"
interview_depth: none
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `$pack install <pack>` instead of the target skill. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Dogfood

Invoke as `$dogfood`.

Create a practical dogfood plan for the app owner or operator. Read the codebase, specs, journey maps, stories, roadmap, and pack-specific research, then tells the operator how to adopt the product into their own workflow so they can understand, evaluate, and improve it through real use.

Dogfood is not UAT. Dogfood asks how the app owner can use the product in their own work and observe what that reveals. UAT asks whether a target user can complete meaningful real-world journeys and would accept the product as fit for use; use `$uat` for that.

This is a human-run product adoption plan, not automated testing. Do not run the product, start servers, drive a browser, call APIs, create accounts, or perform the scenarios yourself.

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

1. **Resolve project context**
   - Read `.agents/project.json` if it exists.
   - Use `project_type` and `enabled_packs` when present.
   - If project metadata is missing, infer the project type from repo signals:
     - business-app: SaaS, marketplace, productivity, workflow, enterprise, or user-facing app
     - devtool: SDK, CLI, API, library, infrastructure, docs, examples, or package-first developer workflow
     - game: game engine files, playable prototypes, store assets, or game-specific README/spec language
     - generic: no strong domain signal
   - Read `README.md`, `AGENTS.md`, `CLAUDE.md`, relevant `docs/`, `specs/`, `spec.md`, and `tasks/` files when present.

2. **Load journey and story evidence**
   - Business app: read `research/icp.md`, `research/journey-map.md`, `research/customer-feedback.md`, `research/metrics.md`, and `research/mvp-gap.md` when present.
   - Devtool: read `research/devtool-user-map.md`, `research/devtool-dx-journey.md`, `research/devtool-integration-map.md`, `research/devtool-adoption.md`, docs, examples, and package manifests when present.
   - Game: read `research/game-core-loop.md`, `research/game-prototype-test.md`, `research/game-playtest-metrics.md`, `research/game-audience.md`, `research/game-fantasy.md`, and `research/game-comparables.md` when present.
   - Generic: use specs, README, routes, tests, examples, and task acceptance criteria.
   - In product-path workspaces with `research/{slug}/` or `specs/{slug}/`, produce product-path-scoped scenarios for the requested app. If no app is specified and multiple apps are plausible, ask the user to choose.

3. **Identify active-use cadence**
   - Infer how often the app owner or operator should use the product in their own workflow: first session, daily, weekly, per incident, per project, per release, monthly review, or another cadence supported by the docs.
   - If cadence is unclear, recommend a default and state the assumption in the audit.
   - Prefer scenarios that exercise owner/operator adoption, repeated use, and product understanding over isolated feature checks.

4. **Create owner/operator scenarios**
   - Generate 3-7 scenarios unless the user requested a narrower focus.
   - Cover at least one happy path, one recovery/failure path, and one return-use or retention path when the product evidence supports them.
   - Each scenario must include:
     - owner/operator role
     - active cadence
     - trigger
     - setup and preconditions
     - exact task for the operator to perform in their own workflow
     - expected success state
     - acceptance checks
     - evidence to capture
     - friction or failure signals
     - follow-up routing
   - Use concrete product language from specs and journeys. Avoid vague instructions such as "verify the flow works."
   - If the scenario is primarily about whether a target user would accept the product, route it to `$uat` instead.

5. **Classify follow-up work**
   - Operator-run dogfood scenarios go in `tasks/manual-todo.md` under `## Dogfood Operator Scenarios`.
   - Use `_(after: research/dogfood-audit.md)_` unless the scenario blocks or follows a known roadmap step. If tied to a known step, use `_(blocks: Step N.X)_` or `_(after: Step N.X)_`.
   - Do not put operator scenarios in `tasks/todo.md`.
   - Agent-executable implementation fixes discovered after a human run belong in `tasks/todo.md`, but do not invent fixes before the operator has attempted the scenario.
   - Cadence-based dogfood obligations, such as weekly dogfood or pre-release dogfood, go in `tasks/recurring-todo.md` with cadence, owner/agent, next due, evidence path, and escalation conditions.
   - If a scenario needs click-by-click help for a human-only external blocker, recommend `$guide`.

6. **Present findings before writing when risk is high**
   - If source material is thin, contradictory, or missing the target user journey, summarize the gap and ask whether to proceed with assumptions.
   - If source material is sufficient, write the audit and task sections directly.

## Deliverables

- `research/dogfood-audit.md` - scenario matrix, source evidence, owner/operator adoption instructions, evaluation checklist, findings template, and next steps.
- `tasks/manual-todo.md` - append or replace only the `## Dogfood Operator Scenarios` section.
- `tasks/recurring-todo.md` - optional, only when a recurring dogfood cadence is useful and not already tracked.

If `tasks/manual-todo.md` does not exist, create it with a `# Manual Tasks - [Project Name]` title, a short note that these items require human-only action, and the dogfood section. Preserve all non-dogfood sections when updating an existing file.

Use this scenario format in `research/dogfood-audit.md`:

```markdown
### Scenario N: [Name]

- Owner/operator role: [role]
- Active cadence: [first session/daily/weekly/per incident/per release/etc.]
- Trigger: [why the user opens the product]
- Setup: [accounts, data, environment, permissions, or sample state needed]
- Task: [specific action sequence in the operator's own workflow]
- Expected success state: [observable result]
- Acceptance checks:
  - [ ] [specific check]
- Evidence to capture: [screenshots, command output, notes, timestamps, records]
- Friction/failure signals: [what counts as confusion, delay, breakage, or mismatch]
- Follow-up routing: [manual note, $uat, $customer-discovery, $journey-map, $guide, or task promotion guidance]

#### Operator result log

- Status: Not run | Pass | Fail | Blocked
- Evidence captured:
- Notes:
- Follow-up tasks promoted:
```

Use this item format in `tasks/manual-todo.md`:

```markdown
## Dogfood Operator Scenarios

- [ ] Perform dogfood scenario: [Scenario name] for [owner/operator role] ([cadence]) _(after: research/dogfood-audit.md)_ - capture evidence in `research/dogfood-audit.md`.
```

## Task Classification

- Human/operator scenario execution goes in `tasks/manual-todo.md`.
- Immediate implementation or documentation fixes confirmed by a completed dogfood run go in `tasks/todo.md`.
- One-time condition-gated evidence collection goes in `tasks/record-todo.md`.
- Cadence-based dogfood checks go in `tasks/recurring-todo.md`.
- Do not put non-blocking records or recurring obligations in `tasks/todo.md` unless they have been explicitly promoted into current execution work.

## Constraints

- Do not run or operate the product in this skill.
- Do not start dev servers, launch browsers, use Playwright, call APIs, create accounts, or perform CLI workflows.
- Do not mark scenarios complete; only the human operator can do that after performing them.
- Do not duplicate existing unchecked dogfood/manual tasks. Reference existing items when they already cover the same scenario.
- Prefer evidence-backed owner/operator adoption scenarios over exhaustive coverage.
- Keep dogfood and UAT separate: use `$dogfood` for owner/operator adoption into the builder's workflow; use `$uat` for target-user acceptance journeys.
- If no credible user journey, story, spec, or product surface can be found, stop and recommend `$customer-discovery`, `$journey-map`, or the relevant pack research skill. For `$customer-discovery`, `$journey-map`, and other pack-based skills, apply the Pack Availability Guard — if the target skill's pack is not in `.agents/project.json` `enabled_packs`, recommend `$pack install <pack>` before the skill.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/dogfood-{topic}.html`.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
