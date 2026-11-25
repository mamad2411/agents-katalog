---
name: ship
description: "Ship already-finished work, optionally deploy it, and prepare the next step"
type: shipping
version: v0.9
argument-hint: "[--no-plan] [--no-deploy] [--save-conversation] [--save-all-conversations]"
invocation: orchestrator
---

# Ship

Ship already-finished work, commit it, optionally deploy it, and plan the next step. In Codex, `$exec` usually handles execution plus shipping; use `$ship` when finished work is already present in the tree or there are unpushed commits to package. If `$ARGUMENTS` contains `--no-plan`, skip planning. If `$ARGUMENTS` contains `--no-deploy`, skip deployment. If `$ARGUMENTS` contains `--save-conversation`, save the current conversation to `conversations/`. If `$ARGUMENTS` contains `--save-all-conversations`, export all past conversations to `conversations/`.

## Process

1. Check if there is anything to ship:
   - Run `git status` and `git diff --stat`.
   - If the working tree is clean and there are no unpushed commits, skip to step 3.
   - If there are changes, continue to step 2.
1b. **Pre-ship validation:**
   - First check conversation context for lint/typecheck/test/build output already produced this session (e.g., from a TDD run step). Do NOT re-run commands whose results are already available.
   - For any validation category not already run, find commands from: `CLAUDE.md`, `Makefile`/`Justfile` (check/lint/typecheck/test/build targets), `package.json` (lint/typecheck/check/test/build scripts), `pyproject.toml`/`setup.cfg`, `Cargo.toml`. If none found and no prior output exists, skip.
   - Inspect validation output even when commands exit zero. If warnings are emitted, either fix them, record them as explicitly accepted with rationale, or report them clearly as unresolved.
   - If errors are found (from prior output or fresh runs), fix them and re-run only the failing commands to confirm. Include fixes in the step's commit (or as a separate commit if unrelated).
   - If errors can't be auto-fixed, **STOP. Do not ship.** Report the errors to the user and ask how to proceed. Never commit or push code with known build/lint/type/test failures.
1c. **Quality gate for non-trivial mutations:**
   - Apply `docs/quality-gate-contract.md` when the work to ship changes source code, scripts, configuration, schemas, generated runtime assets, deploy behavior, workflow policy, validation rules, command surfaces, or multiple files.
   - If the shipping boundary creates, deletes, renames, or changes behavior/metadata in any tracked `SKILL.md` or `PACK.md`, refresh the Skills Showcase before commit: run `node apps/skills-showcase/scripts/generate-skills-showcase-data.mjs`, `node apps/skills-showcase/scripts/generate-skills-showcase-github-data.mjs`, and `apps/skills-showcase/scripts/validate-skills-showcase-data.sh`; include changed generated assets in the same shipping boundary.
   - For skill behavior changes, review curated showcase copy, catalog grouping, workflow animation text, and proof receipts. Update affected site files or record why no curated website copy changed.
   - Build a ship manifest from the exact diff and unpushed commits that will be included in the shipping boundary. The manifest must include: User goal, Changed files, Per-file purpose, User-goal mapping, Tests run, Skipped tests, Adversarial review, Residual risk, Rollback note, and Next command. The `Next command` field must use Codex dollar-command syntax; for a completed `$ship` run, default to `$exec` unless project state names a more specific next route. Do not leave `Next command` blank unless all planned work is genuinely complete, in which case use `none`.
   - For non-trivial source changes, run a targeted `quality-sweep audit`, `$expert-review`, configured review lane, or explicitly justified equivalent adversarial review before commit/push. Fix findings or record accepted residual concerns in the manifest.
   - Final output must distinguish executable verification from documentation-only or task-only checks. Documentation/task checks can support source changes, but cannot be the only proof for non-trivial source mutations.
   - If the tree contains unrelated pre-existing changes, the manifest must separate included files from untouched files and explain why the ship boundary is safe. If that cannot be proven, stop instead of shipping.
   - **Pack install artifact boundary:** Treat `.agents/project.json` as the committed project designation. When pack configuration changed, include `.agents/project.json` in the shipping boundary. Treat `.claude/skills/**` and `.codex/skills/**` as generated local skill roots recreated by `scripts/pack.sh refresh`; generated skill roots must not be staged or committed. If those roots are untracked, leave them uncommitted and report them as generated local artifacts. If any path under those roots is already tracked or modified as a tracked file, stop unless the current task explicitly includes repository hygiene to untrack or ignore generated skill roots.
   - If the user corrected the agent during the work being shipped, the pre-commit ship manifest must prove the exact shipping boundary includes a `tasks/lessons.md` update for the current correction. Treat the correction as repeatable unless the manifest proves otherwise. If it exposes a workflow failure, also include the relevant skill contract, validation script, fixture, or test enforcement update in the same shipping boundary, or include `Correction enforcement:` with the blocker or not-applicable rationale and the concrete follow-up file/command when needed.
2. Ship the work:
   - Read `CLAUDE.md` to understand current progress.
   - Update `tasks/todo.md` — mark completed items as done.
   - Update `tasks/history.md` — append a brief record of what was accomplished. Create it if needed.
   - If `tasks/todo.md`, `tasks/roadmap.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md` changed and `scripts/audit-task-docs.mjs` exists, run `node scripts/audit-task-docs.mjs` and fix any failures before final next-work routing.
   - **Save conversation (skip if `--save-conversation` and `--save-all-conversations` both absent):** Run `scripts/save-conversation.sh` to export the current conversation as a markdown file in `conversations/`. If the script is not found or fails (e.g., no local conversation history available), warn and continue — do not block shipping. Include the generated file in the shipping boundary.
     - If `$ARGUMENTS` contains `--save-all-conversations`, run `scripts/save-conversation.sh --all` instead.
   - Commit and push using the `$commit-and-push-by-feature` workflow. That workflow must land the resulting commits on `main` or `master`, not on an existing feature branch.
3. Deploy (skip if `--no-deploy`):
   After shipping, deploy only when the project has an explicit manual deploy contract.
   - Check for deploy contract: look for `deploy.md` or `tasks/deploy.md`.
   - If neither file exists, skip deploy and report `Deploy skipped: no explicit manual deploy contract (deploy.md or tasks/deploy.md)`.
   - If a deploy contract exists, continue.
   - Invoke `$deploy` targeting the default environment (staging).
   - Pass the deploy contract context to `$deploy`.
   - Skip ledger recording and staleness reporting — those are for standalone `$deploy` invocations only.
   - If `$deploy` reports failure, report the error. Do not retry.
4. Plan the next step:
   - **Migration check:** If `tasks/roadmap.md` does not exist but `tasks/todo.md` contains multiple `## Phase` headers, migrate: copy `tasks/todo.md` → `tasks/roadmap.md`, then trim `tasks/todo.md` to just the current phase (first phase with unchecked steps). Commit with `chore: migrate to roadmap.md + todo.md split`.
   - Read only the current active task/phase in `tasks/todo.md` to identify the next uncompleted step. Do not select unchecked boxes from completed sections, historical roadmap notes, reconciliation reports, manual/record/recurring advisory files, or any roadmap section not explicitly promoted into the current todo surface.
   - If `tasks/record-todo.md` or `tasks/recurring-todo.md` exists, count unchecked advisory items for status only. Do not select them as next work.
   - **Check if the current phase is complete** (all steps checked, milestone criteria met):
     - If **YES — Phase transition:**
       1. Archive the completed phase: copy `tasks/todo.md` → `tasks/phases/phase-N.md` (create `tasks/phases/` if needed). Fill in the "On Completion" section.
       1b. If `tasks/manual-todo.md` exists, inspect unchecked items before advancing phases:
           - If any unchecked `_(blocks: Step N.X)_` items still apply to the completed phase, stop. Do NOT archive the manual task file, mark the phase complete, or advance to the next phase unless the user explicitly overrides the blocker.
           - Unchecked `_(after: Step N.X)_` items are non-blocking follow-up tasks. Archive them with the phase and warn the user that they remain incomplete.
       2. Check off the phase milestone in `tasks/roadmap.md`.
       3. Copy the next phase from `tasks/roadmap.md` → overwrite `tasks/todo.md`.
       3b. Extract the next phase's manual tasks (from `**Manual Tasks:**` in roadmap) into a fresh `tasks/manual-todo.md`. If the next phase has no manual tasks, delete the file.
       4. If no more phases remain, run `$roadmap` to recommend the next action based on project state. Then stop.
       5. **Just-in-time planning:** Invoke `$plan-phase` for the new phase. This generates implementation steps, the phase `### Execution Profile`, and file-level detail using the full context of what was learned during prior phases.
     - If **NO:** find the next uncompleted step within the current phase.
   - If the next uncompleted step is verification-only/no-op-only (for example, "refactor if validation exposes drift", "verify", "run validation", or `Files: no source changes expected`) and the current session already has passing validation evidence for the same scope, mark it complete with a review note and continue to the next substantive item. Do not write a fresh execution plan for a step whose expected result is "no source changes".
5. Write a self-contained implementation plan for the next step into `tasks/todo.md`, complete enough for a fresh session to execute from `tasks/todo.md` alone. Preserve the current phase's `### Execution Profile` so `$exec` can decide whether to execute serially, use read-only subagents, use review subagents, or use disjoint write subagents after presenting the plan and proceeding under implicit approval.
6. Ship `tasks/todo.md`, `tasks/roadmap.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, `tasks/recurring-todo.md` (when they exist), and `tasks/phases/` (if created) via `$commit-and-push-by-feature`, landing them on `main` or `master`.
7. Output a brief summary:
   - What was shipped (if anything)
   - Deploy status (if deployed)
   - Validation status — explicitly state whether any failing tests are expected (red phase: tests before implementation) or unexpected (regressions/bugs), and call out any warnings as fixed, accepted, or unresolved
   - Manual tasks — pending count from `tasks/manual-todo.md` (if it exists), note any blocking upcoming steps
   - Advisory tasks — pending record/recurring counts from `tasks/record-todo.md` and `tasks/recurring-todo.md` if they exist
   - **Next work:** the next concrete project task, blocker, smoke test, or follow-up
   - **Recommended next command:** one command or route for that work

## Next-Step Routing

Before handing back, identify the next concrete work item from project state, then recommend the executor and invocation.

Output exactly two lines beyond the normal report:

- **Next work:** <specific task name, manual blocker, verification gap, discovery task, or explicit parked state>
- **Recommended next command:** <one command or route>

Rules:

- Make the next work item primary. Derive it from `tasks/todo.md`, `tasks/manual-todo.md`, deploy status, validation gaps, smoke-test gaps, phase-transition output, or completion of the current queues. Do not use agent mode itself as the next work item.
- Treat `tasks/todo.md` as the only executable current-task surface. Historical roadmap entries and unchecked advisory/manual/record/recurring items are reconciliation candidates, not next executable work, unless the current active todo section explicitly promotes them.
- Never recommend `$ship`, `$ship --no-deploy`, or `$ship --no-plan` as the routine next command from a completed `$ship` run. `$ship` packages current work; after it completes, hand off to the next executable route such as `$exec`, check `.agents/project.json.enabled_packs` for `agent-work-admin` — if `agent-work-admin` is not enabled, recommend `npx skillpacks install agent-work-admin` from the project shell first; if `agent-work-admin` is enabled, recommend `$roadmap`, check `.agents/project.json.enabled_packs` for `guided-walkthrough` — if `guided-walkthrough` is not enabled, recommend `npx skillpacks install guided-walkthrough` from the project shell first; if `guided-walkthrough` is enabled, recommend `$guide`, or check `.agents/project.json.enabled_packs` for `docs-health` — if `docs-health` is not enabled, recommend `npx skillpacks install docs-health` from the project shell first; if `docs-health` is enabled, recommend `$reconcile-dev-docs fix tasks` based on project state. Recommend `$ship` again only when shipping failed before commit/push or when the next concrete work is explicitly to retry an incomplete shipping operation.
- `$brainstorm` routing: when all planned phases, documentation work, and promotable advisory items are exhausted but the project is not parked, route to new-phase discovery: `**Next work:** discover candidate next phase or explicitly park the project`. `$brainstorm` is owned by the `product-design` pack — check `.agents/project.json.enabled_packs` for `product-design` (or `enabled_skills.brainstorm`); if absent, recommend `npx skillpacks install product-design` from the project shell first, then `**Recommended next command:** $brainstorm` (tell the user to start a fresh Codex CLI session if `$brainstorm` is still unavailable after install); if present, recommend `**Recommended next command:** $brainstorm` directly. This is distinct from `none`.
- `none` routing: emit `Recommended next command: none` only when the project is genuinely complete or explicitly parked/archived by the user. Do not emit `none` merely because the current phase is done.
- If a post-roadmap `$research-roadmap` scan reports documentation current with no missing or stale work, do not stop at documentation completeness; recommend `$brainstorm` as the next route for candidate phase discovery, applying the same `product-design` pack-availability check above.
- Use `./scripts/agent-mode.sh` only to choose command text. If it is missing, unset, or non-zero, infer routing from the current invocation and task type instead of asking the user to select a mode by default.
- Normalize copied task routes to Codex syntax before final output. If `tasks/todo.md`, `tasks/roadmap.md`, benchmark reports, or prior handoffs contain Claude slash commands for base skills (for example `/exec`, `/ship`, `/roadmap`, `/guide`, `/reconcile-dev-docs`), treat them as task identifiers, not final command text. Convert the final `Recommended next command` to the equivalent Codex `$...` command unless the next action is explicitly a Claude-only handoff — check `.agents/project.json.enabled_packs` for `agent-bridge` — if `agent-bridge` is not enabled, recommend `npx skillpacks install agent-bridge` from the project shell first; if `agent-bridge` is enabled, recommend `$delegate $exec`.
- Inference defaults:
  - Codex `$ship` invocation after shipping or packaging current work → recommend `$exec` for the next agent-executable project step, or the more specific next skill named by project state.
  - Other Codex skill invocations (`$exec`, `$ship-end`) → recommend the matching `$...` command.
  - Claude slash invocation (`/exec`, `/ship`, `/delegate`) or orchestration-heavy work → recommend the matching `/...` route.
  - External human-only manual work (browser/auth/DNS/service dashboard work with no reliable authenticated CLI/API path, paid account setup, real-device checks, or production smoke-test work needing human sign-off) → check `.agents/project.json.enabled_packs` for `guided-walkthrough` — if `guided-walkthrough` is not enabled, recommend `npx skillpacks install guided-walkthrough` from the project shell first; if `guided-walkthrough` is enabled, recommend `$guide` — or a Claude-guided manual step rather than `$exec`.
  - Agent-executable work misfiled in `tasks/manual-todo.md`, task-doc bookkeeping, stale `tasks/manual-todo.md` cleanup, or reconciliation against repo/history reality → check `.agents/project.json.enabled_packs` for `docs-health` — if `docs-health` is not enabled, recommend `npx skillpacks install docs-health` from the project shell first; if `docs-health` is enabled, recommend `$reconcile-dev-docs fix tasks` — promotion to `tasks/todo.md`, or a direct dev-doc audit, not `$guide`.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, include `npx skillpacks install <pack-name>` from the project shell as the prerequisite.
- Only present multiple commands when the ambiguity materially changes execution safety or there are equally valid next work items. Otherwise choose the best route and mention degraded mode lookup inline.
- Final route contract: completed `$ship` runs must not self-route back to `$ship`; route to `$exec` or a more specific next actionable skill unless shipping itself failed before commit/push, or emit `none` when all planned work is genuinely complete.

## Constraints

- **Fix unrelated issues:** If any step surfaces errors unrelated to the current work, report them separately. Do not fix unrelated issues within the shipping boundary unless they block validation of the current change.
- Do not write plans into `CLAUDE.md`. It is for project conventions only.
- `tasks/roadmap.md` is the source of truth for the full phased plan. `tasks/todo.md` holds only the current phase.
- Do NOT create `tasks/todo.md` from scratch — if it doesn't exist and there's no roadmap, suggest discovery skills instead.
- Do not amend or rewrite history.
- Do not commit secrets.
- Do not push shipping commits to an existing feature branch. Use `$commit-and-push-by-feature` to move the work onto `main` or `master` and push it there, or stop and report a blocker if that cannot be done safely.
- The plan must be actionable with specific file paths, technical details, and the current phase's `### Execution Profile`.
- In Codex, `$ship` is a compatibility/manual cleanup workflow. Prefer `$exec` for the normal execute-and-ship loop.
- Do not execute or plan from `tasks/record-todo.md` or `tasks/recurring-todo.md`; report their counts only unless an item has been promoted into `tasks/todo.md`.
- When task docs changed, do not finish with a next-work recommendation until `node scripts/audit-task-docs.mjs` passes, if that script exists.
- `ship` only runs a deploy when `deploy.md` or `tasks/deploy.md` explicitly documents a manual deployment workflow. Repos without one are assumed to auto-deploy or require no manual deploy step.
- Never use GitHub Actions for deployment. Only use manual deploy scripts, Makefiles, or CLI commands.
- Never deploy to production without explicit user confirmation.
- Do not modify code as part of the deploy process.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
