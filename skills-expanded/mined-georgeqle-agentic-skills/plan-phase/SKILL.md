---
name: plan-phase
description: Decompose a single roadmap phase into implementation steps, tests, and file-level detail
type: planning
version: v0.6
required_conventions: [alignment-page]
invocation: sub-skill
parent: exec
---

# Plan Phase

Invoke as `$plan-phase`.

Fill in the implementation detail for **one** phase of `tasks/roadmap.md`. Invoked just-in-time — either manually, by `$roadmap` (to seed Phase 1), or by `$ship` and `$exec` when a new phase begins. Implementation detail is generated when a phase starts, not upfront, because context from earlier phases informs later decisions.

## Prerequisites

- `tasks/roadmap.md` must exist. If it does not, stop and tell the user to run `$roadmap` (or `$research-roadmap` (research-admin pack) → `$roadmap` if no spec exists).
- The target phase must already have a Goal, Scope, and Acceptance Criteria in the roadmap.

## Input

Read arguments:

- If arguments contain a phase number (e.g., `2`), plan that phase.
- If arguments are empty, plan the **first phase that has acceptance criteria but no implementation steps** (no `### Tests First` or `### Implementation` section yet).
- If arguments contain `--no-tdd`, use `tests-after` for this phase regardless of other signals.

Read:

- `tasks/roadmap.md` for the target phase's Goal, Scope, and Acceptance Criteria.
- `specs/` (or `spec.md`) for the detailed requirements referenced by the phase's scope.
- The codebase as needed to understand existing code, patterns, and which files to modify.
- The roadmap phase's `Parallelization` and `Coordination Notes` fields, if present.

## Planning Process

### Determine Test Strategy

Check in order:

1. If arguments contain `--no-tdd`, use `tests-after`.
2. If `AGENTS.md` or `CLAUDE.md` has a `## Test Strategy` section, follow the project default.
3. Otherwise, classify the phase:
   - **`tdd`**: stable interfaces, APIs, data models, business logic with known contracts, payment/auth flows
   - **`tests-after`**: UI components, prototyping, exploratory features, design-in-flux work
   - **`none`**: pure config, docs, scaffolding, infra setup, CI/CD changes

Annotate the phase with `> Test strategy: tdd|tests-after|none`.

### Determine Execution Profile

Expand the roadmap's strategic parallelization mode into a concrete execution profile for this phase. If the roadmap has no `Parallelization` field, default to `serial`.

Use these modes:

- **`serial`**: one main agent does the work; use when ownership is coupled or unclear.
- **`research-only`**: read-only subagents may gather context before implementation; main agent implements.
- **`review-only`**: main agent implements; subagents review before final validation.
- **`implementation-safe`**: write subagents may work only on disjoint owned paths; main agent integrates.
- **`agent-team`**: work is too broad or cross-cutting for one shared local tree; write lanes must use separate GitHub branches and a consolidation/PR review gate before final integration.

Downgrade `implementation-safe` to `research-only` or `serial` if path ownership overlaps, shared chokepoints dominate, or the likely integration surface is unclear.

Add this section before implementation steps:

```markdown
### Execution Profile
**Parallel mode:** serial | research-only | review-only | implementation-safe | agent-team
**Integration owner:** main agent
**Conflict risk:** low | medium | high
**Review gates:** correctness, tests, security, performance, docs/API conformance, UX, or none

**Subagent lanes:**
- Lane: [lane-name]
  - Agent: explorer | worker | default
  - Role: explorer | implementer | reviewer | docs-researcher | test-reviewer
  - Mode: read-only | write | review
  - Scope: [bounded task]
  - Owns: `path/or/glob` (write lanes only)
  - Must not edit: `path/or/glob` (write lanes only)
  - Branch: `agent-team/phase-N-lane-name` (agent-team write lanes only)
  - Depends on: [lane, step, or none]
  - Deliverable: [findings, patch summary, changed paths, tests, branch + commit SHA + PR URL, or review report]
```

For `serial`, use `**Subagent lanes:** none`. For `research-only` and `review-only`, lanes must not have write mode. For `implementation-safe`, every write lane must have non-overlapping `Owns` paths and explicit `Must not edit` boundaries.
For `agent-team`, every write lane must have a deterministic `Branch:` value that is not `main` or `master`, and the phase steps must include a consolidation/PR review step after all write lanes complete and before final validation or shipping. If GitHub branch push or PR review is unavailable, downgrade to `implementation-safe`, `research-only`, or `serial`, or stop and document the blocker.

### Break the Phase into Steps

Define ordered steps beneath the existing Goal/Scope/Acceptance Criteria. The structure depends on the test strategy:

For new user-facing product, SaaS, marketplace, dashboard, internal tool, or product-experience phases, apply a prototype-first planning gate before writing steps:

- If there is no accepted clickable journey yet and the current roadmap phase combines prototype exploration with production implementation, stop and re-scope the current work into a distinct prototype/experiment phase before writing implementation steps. Prefer `Phase 0: Prototype Experiments` when the project convention allows it; otherwise make the next phase explicitly prototype-only and push production implementation later.
- If the roadmap/spec does not explicitly approve durable database/storage, auth, payments, analytics, deployment, admin tooling, multi-tenancy, or production observability for the current phase, keep those items in a later "eventual production infrastructure" backlog and plan the current phase as a clickable local/static prototype with fake, fixture, or in-memory data.
- For new feature prototypes or uncertain product surfaces, plan multiple small experiments on separate clickable routes such as `/experiments/<variant>` or project-native equivalents. Each route should test a distinct workflow, layout, density, copy, navigation, or interaction hypothesis without sharing hidden production infrastructure.
- Include a calibration step before any infrastructure promotion: the user must be able to try one journey and record what felt wrong, slow, generic, too dense, too sparse, off-brand, or workflow-breaking.
- Promote infrastructure into the current phase only when the phase is explicitly production hardening, the user has approved that infrastructure, or the core prototype cannot test the primary interaction without it. State the evidence in the phase notes.

**For `tdd` phases:**
```
## Phase N: [Title]
> Test strategy: tdd

### Execution Profile
**Parallel mode:** serial | research-only | review-only | implementation-safe | agent-team
**Integration owner:** main agent
**Conflict risk:** low | medium | high
**Review gates:** correctness, tests, security, performance, docs/API conformance, UX, or none

**Subagent lanes:**
- Lane: [lane-name or none]
  - Agent: explorer | worker | default
  - Role: explorer | implementer | reviewer | docs-researcher | test-reviewer
  - Mode: read-only | write | review
  - Scope: [bounded task]
  - Owns: `path/or/glob` (write lanes only)
  - Must not edit: `path/or/glob` (write lanes only)
  - Branch: `agent-team/phase-N-lane-name` (agent-team write lanes only)
  - Depends on: [lane, step, or none]
  - Deliverable: [expected output, including branch + commit SHA + PR URL for agent-team write lanes]

### Tests First
- Step N.1: Write failing tests for this phase's acceptance criteria
  - List specific test cases to write
  - Tests should cover happy path, edge cases, and error cases
  - Tests MUST fail at this point (red)

### Implementation
- Step N.2: [First implementation task]
  - Files: create `path/to/new.ts`, modify `path/to/existing.ts`
- Step N.3: [Next implementation task]
  - Files: modify `path/to/file.ts`
- ...

### Green
- Step N.X: Run tests, verify all pass, and perform only concrete cleanup found by validation

### Milestone: [Phase N Milestone Name]
**Acceptance Criteria:** (preserve from roadmap — do not rewrite)
- [ ] [criterion 1]
- [ ] All phase tests pass
- [ ] No regressions in previous phase tests
```

**For `tests-after` phases:**
```
## Phase N: [Title]
> Test strategy: tests-after

### Execution Profile
**Parallel mode:** serial | research-only | review-only | implementation-safe | agent-team
**Integration owner:** main agent
**Conflict risk:** low | medium | high
**Review gates:** correctness, tests, security, performance, docs/API conformance, UX, or none

**Subagent lanes:**
- Lane: [lane-name or none]
  - Agent: explorer | worker | default
  - Role: explorer | implementer | reviewer | docs-researcher | test-reviewer
  - Mode: read-only | write | review
  - Scope: [bounded task]
  - Owns: `path/or/glob` (write lanes only)
  - Must not edit: `path/or/glob` (write lanes only)
  - Branch: `agent-team/phase-N-lane-name` (agent-team write lanes only)
  - Depends on: [lane, step, or none]
  - Deliverable: [expected output, including branch + commit SHA + PR URL for agent-team write lanes]

### Implementation
- Step N.1: [First implementation task]
  - Files: create `path/to/new.ts`, modify `path/to/existing.ts`
- ...

### Green
- Step N.X: Write regression tests covering acceptance criteria
- Step N.Y: Run all tests, verify they pass, and perform only concrete cleanup found by validation

### Milestone: [Phase N Milestone Name]
**Acceptance Criteria:** (preserve from roadmap)
- [ ] [criterion 1]
- [ ] All phase tests pass
- [ ] No regressions in previous phase tests
```

**For `none` phases:**
```
## Phase N: [Title]
> Test strategy: none

### Execution Profile
**Parallel mode:** serial | research-only | review-only | implementation-safe | agent-team
**Integration owner:** main agent
**Conflict risk:** low | medium | high
**Review gates:** correctness, tests, security, performance, docs/API conformance, UX, or none

**Subagent lanes:**
- Lane: [lane-name or none]
  - Agent: explorer | worker | default
  - Role: explorer | implementer | reviewer | docs-researcher | test-reviewer
  - Mode: read-only | write | review
  - Scope: [bounded task]
  - Owns: `path/or/glob` (write lanes only)
  - Must not edit: `path/or/glob` (write lanes only)
  - Branch: `agent-team/phase-N-lane-name` (agent-team write lanes only)
  - Depends on: [lane, step, or none]
  - Deliverable: [expected output, including branch + commit SHA + PR URL for agent-team write lanes]

### Implementation
- Step N.1: [First implementation task]
  - Files: create `path/to/new.ts`, modify `path/to/existing.ts`
- ...

### Milestone: [Phase N Milestone Name]
**Acceptance Criteria:** (preserve from roadmap)
- [ ] [criterion 1]
```

**On Completion** (fill in when phase is done — all strategies):
- Deviations from plan: [none, or describe]
- Tech debt / follow-ups: [none, or list]
- Ready for next phase: yes/no

### Test Requirements

- **`tdd` phases**: start with writing tests BEFORE implementation. Tests tied to acceptance criteria. Include test file paths.
- **`tests-after` phases**: implementation comes first. The Green step writes regression tests covering the acceptance criteria.
- **`none` phases**: no test steps. Milestone omits "All phase tests pass".
- All `tdd` and `tests-after` milestones must include "All phase tests pass" and "No regressions in previous phase tests".
- If the project has no test framework yet, the first phase's first step should set it up.

### File-Level Granularity

- Every implementation step lists the specific files to create, modify, or delete.
- This gives the executing agent clear scope and prevents steps from becoming unbounded.
- Write-capable subagent lanes must have disjoint owned paths. If they do not, keep implementation serial and use research or review lanes only.
- Agent-team phases must include a final automated consolidation/PR review step that inspects each lane's branch/PR, verifies changed paths against `Owns` and `Must not edit`, records blocker/advisory findings, integrates only approved lane work, and then runs the phase validation gate.

### Task Classification

Classify each step or follow-up as exactly one of:

- **automated** — the agent executes it as implementation or verification work in `tasks/todo.md`.
- **manual** — a human-only external action tied to an automated step in `tasks/manual-todo.md`.
- **record** — a one-time, non-blocking record or measurement that should happen only after a condition becomes true in `tasks/record-todo.md`.
- **recurring** — cadence-based operational, research, or maintenance work in `tasks/recurring-todo.md`.

Use the narrowest classification that can execute without losing context:

- If the agent can do it by editing repo files, running local commands, using an approved CLI/MCP/API integration, or writing a script with already-available credentials, classify it as **automated**.
- If the work is blocked only because a secret, account, payment method, approval, hardware device, or human judgment/evidence is missing, classify only that missing prerequisite as **manual**.
- If one item mixes human and automatable work, split it: the human-gated prerequisite goes to `tasks/manual-todo.md`; the repo/code/config/test follow-up stays in `tasks/todo.md`.

Manual tasks include only human-gated work such as:

- DNS configuration, domain setup, SSL certificates
- Browser/device testing or visual QA that requires a real account, real device, production environment, or subjective human sign-off
- OAuth/API credential setup with third-party services when no authenticated CLI/API path is available
- Deployment approvals, paid environment provisioning, quota/billing approval, or account ownership decisions
- Signing up for services, billing setup
- Any step requiring a GUI, physical device, or human judgment that cannot be scripted

Do not classify these as manual:

- Editing source, docs, `.env.example`, config templates, or task docs
- Installing or wiring SDKs/packages, creating adapters, writing scripts, or updating metadata contracts
- Running builds, unit tests, local smoke tests, Lighthouse, Playwright, linters, or repo audits
- Setting local environment variables when the required non-secret values are known or the user has already provided the secret values
- Running provider CLIs or API calls when authentication is already present or can be requested through the normal approval flow

Manual tasks MUST NOT appear in `tasks/todo.md`. They go in `tasks/manual-todo.md`.
Agent-executable tasks MUST NOT appear in `tasks/manual-todo.md`. If found there, promote them to `tasks/todo.md` or route a reconciliation fix.

Record tasks MUST NOT appear in `tasks/todo.md` unless they are launch gates or current execution work. They go in `tasks/record-todo.md` with source, condition, non-blocking reason, required data/access, measurement/query, target note, revisit cadence/date, completion evidence, and promotion rule.

Recurring tasks MUST NOT appear in `tasks/todo.md` unless the current run is explicitly in scope for this phase. They go in `tasks/recurring-todo.md` with task, cadence, owner/agent, scope, trigger, last run, next due, command/skill, evidence/output path, and escalation conditions.

## Output

1. **Update `tasks/roadmap.md`** — insert the implementation structure (Tests First / Implementation / Green / Milestone, per strategy) into the target phase, beneath the existing Goal/Scope/Acceptance Criteria. Do NOT modify other phases. Do NOT rewrite the Goal, Scope, or Acceptance Criteria.

2. **Write `tasks/todo.md`** — extract the target phase as a standalone working document, including the `### Execution Profile`. Include enough context (project name, current phase number, total phases) so a fresh session can orient itself without reading `tasks/roadmap.md`. If `tasks/todo.md` already has in-progress work for a different phase, ask the user before overwriting.

3. **Write `tasks/manual-todo.md`** (only if this phase has manual tasks):
   ```markdown
   # Manual Tasks — [Project Name]

   > Phase: N — [Phase Title]
   > These tasks require human-only external action. Do not put repo edits, local commands, CLI/API work, tests, audits, or implementation follow-ups here.
   > Check them off as you complete them.

   ## Pre-Phase / Setup
   - [ ] [task] _(blocks: Step N.X)_

   ## During Phase
   - [ ] [task] _(after: Step N.X)_

   ## Post-Phase / Verification
   - [ ] [task]
   ```
   - `_(blocks: Step N.X)_` = must be done before that automated step
   - `_(after: Step N.X)_` = should be done after that automated step
   - No annotation = do anytime during the phase
   - Only create this file when manual tasks exist — no empty files.

4. **Write `tasks/record-todo.md`** (only if this phase identifies non-blocking condition-gated records):
   ```markdown
   # Record Tasks — [Project Name]

   > These tasks are non-blocking records or measurements. Do not execute them through `$exec` unless promoted to `tasks/todo.md`.

   - [ ] [task]
     - Source: [phase/spec/criterion]
     - Condition: [when this becomes eligible]
     - Non-blocking reason: [why this is not a launch gate or current step]
     - Required data/access: [data, portal, aggregate, credential, or user-provided output]
     - Measurement/query: [how to collect evidence]
     - Target/acceptance note: [threshold or expected record]
     - Revisit: [date or cadence]
     - Completion evidence: [where to record the result]
     - Promotion rule: [when to move this into `tasks/todo.md`]
   ```

5. **Write `tasks/recurring-todo.md`** (only if this phase identifies recurring obligations):
   ```markdown
   # Recurring Tasks — [Project Name]

   > These tasks recur on a cadence. Do not execute them through `$exec` unless a due run is promoted to `tasks/todo.md`.

   - [ ] [task]
     - Cadence: [daily/weekly/monthly/quarterly/on release/etc.]
     - Owner/agent: [human, `$skill`, or agent role]
     - Scope: [project/app/area]
     - Trigger: [time, release, data threshold, user request]
     - Last run: [date or never]
     - Next due: [date or rule]
     - Command/skill: [command or skill to run]
     - Evidence/output path: [where results are recorded]
     - Escalation conditions: [when it becomes executable or blocking work]
   ```

## Next-Step Routing

Before handing back, identify the next concrete work item from project state, then recommend the executor and invocation.

Output exactly two lines beyond the normal report:

- **Next work:** <specific first step, manual blocker, or verification gap for the planned phase>
- **Recommended next command:** <one command or route>

Rules:

- Make the next work item primary. Derive it from the first executable step in `tasks/todo.md`, any matching blocker in `tasks/manual-todo.md`, or the phase's verification/setup gap. Do not use agent mode itself as the next work item.
- Use `./scripts/agent-mode.sh` only to choose command text. If it is missing, unset, or non-zero, infer routing from the current invocation and task type instead of asking the user to select a mode by default.
- Inference defaults:
  - Codex skill invocation (`$plan-phase`) → recommend the matching `$...` command; for executable planned work, emit the approved task artifact route rather than a direct execution-loop command.
  - Hybrid execution handoff → check `.agents/project.json.enabled_packs` for `agent-bridge` — if `agent-bridge` is not enabled, recommend `npx skillpacks install agent-bridge` from the project shell, first; if `agent-bridge` is enabled, recommend a cross-agent handoff that consumes the approved task artifact.
  - Imported Claude slash routes or orchestration-heavy work → normalize to the Codex approved task artifact route and let the active executor consume it.
  - External human-only manual work (browser/auth/DNS/service dashboard work with no reliable authenticated CLI/API path, paid account setup, real-device checks, or production smoke-test work needing human sign-off) → check `.agents/project.json.enabled_packs` for `guided-walkthrough` — if `guided-walkthrough` is not enabled, recommend `npx skillpacks install guided-walkthrough` from the project shell, first; if `guided-walkthrough` is enabled, recommend `$guide` — or a Claude-guided manual step rather than an execution-loop command.
  - Agent-executable work misfiled in `tasks/manual-todo.md`, task-doc bookkeeping, stale `tasks/manual-todo.md` cleanup, or reconciliation against repo/history reality → check `.agents/project.json.enabled_packs` for `docs-health` — if `docs-health` is not enabled, recommend `npx skillpacks install docs-health` from the project shell, first; if `docs-health` is enabled, recommend `$reconcile-dev-docs fix tasks` — promotion to `tasks/todo.md`, or a direct dev-doc audit, not `$guide`.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, include `npx skillpacks install <pack-name>` from the project shell, as the install prerequisite before the recommendation.
- Only present multiple commands when the ambiguity materially changes execution safety or there are equally valid next work items. Otherwise choose the best route and mention degraded mode lookup inline.

## Constraints

- **One phase per invocation.** Do not decompose multiple phases ahead of time.
- **Require `tasks/roadmap.md`.** If it's missing, stop and direct the user to `$roadmap`.
- **Preserve the roadmap's Goal, Scope, and Acceptance Criteria exactly.** Those are `$roadmap`'s decisions. Only add implementation detail beneath them.
- **Phase headers must use `## Phase N: [Title]` format** and steps must use `- Step N.X:` format — this is required by `$exec` and `$ship`.
- Every milestone must have specific, checkable acceptance criteria — not vague statements like "works correctly" but concrete conditions like "POST /api/items returns 201 with valid payload and persists to database."
- Every `tdd` phase must start with writing failing tests. `tests-after` phases write tests in the Green step.
- Do not generate standalone cleanup/refactor steps that are conditional on validation finding drift. Fold those checks into the Green validation step and only create a separate follow-up when there is known concrete remediation work.
- Do not include implementation code — describe what to build and what to test.
- Note what already exists in the codebase vs. what needs to be created.
- The `### Execution Profile` must be decision-complete enough for `$exec` to decide whether to use serial execution, read-only subagents, review subagents, or disjoint write subagents after presenting the plan and proceeding under implicit approval.
- Subagents must not own task docs, roadmap/history updates, shipping, or deploy steps. Those stay with the main agent.
- Agent-team write lanes must not target `main` or `master`; each lane gets its own GitHub branch and must return branch, commit SHA, validation evidence, and PR URL before consolidation.
- Manual tasks MUST NOT appear in `tasks/todo.md` — they go in `tasks/manual-todo.md` only.
- Agent-executable work MUST NOT appear in `tasks/manual-todo.md` — it goes in `tasks/todo.md` or an implementation skill.
- Non-blocking record tasks MUST NOT appear in `tasks/todo.md` — they go in `tasks/record-todo.md` unless explicitly promoted.
- Recurring obligations MUST NOT appear in `tasks/todo.md` by default — they go in `tasks/recurring-todo.md` unless a due run is current execution work.
- Do NOT put plans in `AGENTS.md`, `CLAUDE.md`, or `docs/plan.md`.

## Alignment Page

Follow the shared alignment-page convention via the packaged convention resolver; output path is `alignment/plan-phase-{topic}.html`. By default, report results inline and write only this skill's normal durable artifacts; create an alignment page only when explicitly requested or when a concrete clarification/review need cannot be handled cleanly inline.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
