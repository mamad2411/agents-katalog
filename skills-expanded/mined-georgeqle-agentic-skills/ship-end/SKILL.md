---
name: ship-end
description: "Wrap up the current session — update docs, commit, and push"
type: shipping
version: v0.9
required_conventions: [social-ledger]
argument-hint: "[--no-deploy] [--save-conversation] [--save-all-conversations]"
---

# Ship End

Invoke as `$ship-end`.

Use this skill when the user wants the current session wrapped up cleanly. If `$ARGUMENTS` contains `--save-conversation`, save the current conversation to `conversations/`. If `$ARGUMENTS` contains `--save-all-conversations`, export all past conversations to `conversations/`.

## Process

1. Inspect `git status` and diffs.
2. If the tree is clean and there are no unpushed commits, report that there is nothing to ship and stop.
3. Update `tasks/todo.md` with completed items and blockers. Also update milestone progress in `tasks/roadmap.md` if criteria were met.
3b. Check `tasks/manual-todo.md` (if it exists) — note the status of manual tasks (checked vs unchecked). Do NOT modify checked items.
3c. Check `tasks/record-todo.md` and `tasks/recurring-todo.md` if they exist — note unchecked advisory counts only. Do NOT treat them as blockers unless an item has been promoted into `tasks/todo.md`.
4. Update `tasks/history.md` with a brief record of the session. Create it if needed.
4b. If `tasks/todo.md`, `tasks/roadmap.md`, `tasks/manual-todo.md`, `tasks/record-todo.md`, or `tasks/recurring-todo.md` changed and `scripts/audit-task-docs.mjs` exists, run `node scripts/audit-task-docs.mjs` and fix any failures before final next-work routing.
5. **Pre-ship validation:**
   - First check conversation context for lint/typecheck/test/build output already produced this session (e.g., from a TDD run step). Do NOT re-run commands whose results are already available.
   - For any validation category not already run, find commands from: `CLAUDE.md`, `Makefile`/`Justfile` (check/lint/typecheck/test/build targets), `package.json` (lint/typecheck/check/test/build scripts), `pyproject.toml`/`setup.cfg`, `Cargo.toml`. If none found and no prior output exists, skip.
   - Inspect validation output even when commands exit zero. If warnings are emitted, either fix them, record them as explicitly accepted with rationale, or report them clearly as unresolved.
   - If errors are found (from prior output or fresh runs), fix them and re-run only the failing commands to confirm. Include fixes in the session-wrap-up commit, or a separate commit if unrelated.
   - If errors can't be auto-fixed, **STOP. Do not ship.** Report the errors to the user and ask how to proceed. Never commit or push code with known build/lint/type/test failures.
5b. **Quality gate for non-trivial mutations:**
   - Apply `docs/quality-gate-contract.md` when the session changed source code, scripts, configuration, schemas, generated runtime assets, deploy behavior, workflow policy, validation rules, command surfaces, or multiple files.
   - Build a ship manifest from the exact diff and unpushed commits that will be included in the session wrap-up. The manifest must include: User goal, Changed files, Per-file purpose, User-goal mapping, Tests run, Skipped tests, Adversarial review, Residual risk, Rollback note, and Next command.
   - For non-trivial source changes, run a targeted `quality-sweep audit`, `$expert-review`, configured review lane, or explicitly justified equivalent adversarial review before commit/push. Fix findings or record accepted residual concerns in the manifest.
   - Final output must distinguish executable verification from documentation-only or task-only checks. Documentation/task checks can support source changes, but cannot be the only proof for non-trivial source mutations.
   - If no executable check is relevant, state why in `Skipped tests` and explain the residual risk. Do not write "not run" without a rationale.
   - If the user corrected the agent during the session, the pre-commit ship manifest must prove the exact shipping boundary includes a `tasks/lessons.md` update for the current correction. Treat the correction as repeatable unless the manifest proves otherwise. If it exposes a workflow failure, also include the relevant skill contract, validation script, fixture, or test enforcement update in the same shipping boundary, or include `Correction enforcement:` with the blocker or not-applicable rationale and the concrete follow-up file/command when needed.
6. Deploy (skip if `--no-deploy`):
   After shipping, deploy only when the project has an explicit manual deploy contract.
   - Check for deploy contract: look for `deploy.md` or `tasks/deploy.md`.
   - If neither file exists, skip deploy and report `Deploy skipped: no explicit manual deploy contract (deploy.md or tasks/deploy.md)`.
   - If a deploy contract exists, continue.
   - Invoke `$deploy` targeting the default environment (staging).
   - Pass the deploy contract context to `$deploy`.
   - Skip ledger recording and staleness reporting — those are for standalone `$deploy` invocations only.
   - If `$deploy` reports failure, report the error. Do not retry.
7. **Save conversation (skip if `--save-conversation` and `--save-all-conversations` both absent):** Run `scripts/save-conversation.sh` to export the current conversation as a markdown file in `conversations/`. If the script is not found or fails (e.g., no local conversation history available), warn and continue — do not block shipping. Include the generated file in the shipping boundary.
   - If `$ARGUMENTS` contains `--save-all-conversations`, run `scripts/save-conversation.sh --all` instead.
8. Commit and push using the `commit-and-push-by-feature` workflow. That workflow must land the resulting commits on `main` or `master`, not on an existing feature branch.
8b. **Pack install artifact boundary:** Treat `.agents/project.json` as the committed project designation. When pack configuration changed, include `.agents/project.json` in the shipping boundary. Treat `.claude/skills/**` and `.codex/skills/**` as generated local skill roots recreated by `scripts/pack.sh refresh`; generated skill roots must not be staged or committed. If those roots are untracked, leave them uncommitted and report them as generated local artifacts. If any path under those roots is already tracked or modified as a tracked file, stop unless the current task explicitly includes repository hygiene to untrack or ignore generated skill roots.
9. Report:
   - What was accomplished
   - Validation status — explicitly state whether any failing tests are expected (red phase: tests before implementation) or unexpected (regressions/bugs), and call out any warnings as fixed, accepted, or unresolved
   - Manual tasks — X/Y complete (from `tasks/manual-todo.md`, if it exists)
   - Advisory tasks — pending record/recurring counts from `tasks/record-todo.md` and `tasks/recurring-todo.md` if they exist
   - What is still outstanding
   - Branch name
   - Commit list
   - Final working-tree state
   - **Next work:** the next concrete project task, blocker, smoke test, or follow-up
   - **Recommended next command:** one command or route for that work
10. **BIP post suggestions** (advisory; never blocks wrap-up — run after the report, even if shipping reported nothing):
    - Read `.agents/project.json`.
    - If `alignment.build_in_public === true`, skip only the enablement question, then run the enabled BIP post-suggestion path below. Do not report only that the BIP gate was skipped.
    - Else if `alignment.bip_prompt_dismissed === true`, skip both enablement and post suggestions.
    - Otherwise ask the user once, concisely — explain that Build-In-Public mode generates source-safe social posts from your alignment pages and shipped work, and ask whether to enable it for this project.
    - On **yes**: run `scripts/pack.sh set-bip on` (or `npx skillpacks set-bip on`) **and** `scripts/pack.sh set-bip-prompt dismiss` (or the `npx` equivalent). Then run the enabled BIP post-suggestion path for this shipped session.
    - On **no**: run `scripts/pack.sh set-bip-prompt dismiss` (or the `npx` equivalent). Do not ask again.
    - Enabled BIP post-suggestion path: inspect the shipped boundary from the session report, changed files, commits, task/history notes, and any alignment pages. Read `.agents/project.json.alignment.bip_platforms`; use only those saved platforms for suggestions. If no saved platforms exist, ask one project-platform setup question, persist the answer with `scripts/pack.sh set-bip-platforms <platform...>` (or `npx skillpacks set-bip-platforms <platform...>`), and then continue with the saved platform list. Do not fall back to ad hoc per-session channels.
    - Infer `bip_phase` as exactly one of `research`, `prototyping`, or `implementation` from the shipped boundary. Following `docs/social-ledger-convention.md` plus the loaded platform conventions, draft an exhaustive phase-aware batch of source-safe Build-In-Public post candidates per saved platform, or state that there is no safe public angle for this wrap-up. Mark top-ranked options clearly and keep rejected/not-now options visible when useful for dedupe or future context. For each candidate, include target platform, `bip_phase`, angle, source basis, loaded convention path, risk level, claim-safety notes, publish precheck, and draft post text or a concise video/community-post outline. Do not publish externally.

## Next-Step Routing

Before closing out the session, identify the next concrete work item from project state, then recommend the executor and invocation.

Output exactly two lines beyond the normal report:

- **Next work:** <specific task name, manual blocker, verification gap, or "none">
- **Recommended next command:** <one command or route>

Rules:

- Make the next work item primary. Derive it from `tasks/todo.md`, `tasks/manual-todo.md`, deploy status, validation gaps, smoke-test gaps, phase-transition output, outstanding session work, or the absence of any remaining work. Do not use agent mode itself as the next work item.
- Treat `tasks/todo.md` as the only executable current-task surface. Historical roadmap entries and unchecked advisory/manual/record/recurring items are reconciliation candidates, not next executable work, unless the current active todo section explicitly promotes them.
- Use `./scripts/agent-mode.sh` only to choose command text. If it is missing, unset, or non-zero, infer routing from the current invocation and task type instead of asking the user to select a mode by default.
- Prefer an owning workflow/domain route over execution-loop defaults. If the next work item names a research, alignment, design, UI, UX, prototype-test, or copy-audit artifact or review page, recommend the specific owning skill, required user review, or compiled-YAML step directly. Use `$exec` only when no narrower installed skill, artifact contract, or review route owns the next action.
- Inference defaults:
  - Codex skill invocation (`$exec`, `$ship`, `$ship-end`) → after applying owning-route precedence above, recommend the matching `$...` command.
  - Hybrid execution handoff → check `.agents/project.json.enabled_packs` for `agent-bridge` — if `agent-bridge` is not enabled, recommend `npx skillpacks install agent-bridge` from the project shell first; if `agent-bridge` is enabled, recommend `$delegate $exec`.
  - Claude slash invocation (`/exec`, `/ship-end`, `/delegate`) or orchestration-heavy work → recommend the matching `/...` route.
  - External human-only manual work (browser/auth/DNS/service dashboard work with no reliable authenticated CLI/API path, paid account setup, real-device checks, or production smoke-test work needing human sign-off) → check `.agents/project.json.enabled_packs` for `guided-walkthrough` — if `guided-walkthrough` is not enabled, recommend `npx skillpacks install guided-walkthrough` from the project shell first; if `guided-walkthrough` is enabled, recommend `$guide` — or a Claude-guided manual step rather than `$exec`.
  - Agent-executable work misfiled in `tasks/manual-todo.md`, task-doc bookkeeping, stale `tasks/manual-todo.md` cleanup, or reconciliation against repo/history reality → check `.agents/project.json.enabled_packs` for `docs-health` — if `docs-health` is not enabled, recommend `npx skillpacks install docs-health` from the project shell first; if `docs-health` is enabled, recommend `$reconcile-dev-docs fix tasks` — promotion to `tasks/todo.md`, or a direct dev-doc audit, not `$guide`.
- When recommending a skill from another pack, verify the pack is installed via `.agents/project.json` `enabled_packs`. If not installed, include `npx skillpacks install <pack-name>` from the project shell as the prerequisite.
- Only present multiple commands when the ambiguity materially changes execution safety or there are equally valid next work items. Otherwise choose the best route and mention degraded mode lookup inline.

## Constraints

- **Fix unrelated issues:** If any step surfaces errors, warnings, or lint issues — even ones unrelated to the current work — investigate and fix them before continuing. Commit these fixes separately with a descriptive message (e.g., `fix: resolve unused import warning in auth.ts`).
- Do not modify `CLAUDE.md` as part of progress tracking.
- Do not execute or block wrap-up on `tasks/record-todo.md` or `tasks/recurring-todo.md` items unless they were explicitly promoted into `tasks/todo.md`.
- When task docs changed, do not finish with a next-work recommendation until `node scripts/audit-task-docs.mjs` passes, if that script exists.
- Do not switch or create branches unless the current state requires it.
- Do not amend or rewrite history.
- Stop and report if secrets are detected.
- Do not push session-wrap-up commits to an existing feature branch. Use `commit-and-push-by-feature` to move the work onto `main` or `master` and push it there, or stop and report a blocker if that cannot be done safely.
- `ship-end` only deploys when `deploy.md` or `tasks/deploy.md` exists. Repos without one are assumed to auto-deploy or require no manual deploy step.
- Never use GitHub Actions for deployment. Only use manual deploy scripts, Makefiles, or CLI commands.
- Never deploy to production without explicit user confirmation.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
