---
name: team-release
description: "Release pipeline end-to-end: perf-audit, a11y-audit, security quick check and dependency-audit one after another → changelog → release-checklist → deploy (via an installed deployment skill when present) → post-deploy verification. Use to ship a version."
argument-hint: "[version]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Task, Skill, AskUserQuestion
model: opus
---

# Team: Release

Reply in the project conversation language (CLAUDE.md → Language); code, identifiers, paths and commit messages stay in English.

File writes and any mutation (git, deploy) happen only after an explicit "May I write?" / "Proceed?" — each one `AskUserQuestion` (proceed (Recommended) · show the draft/diff first · not now) → "yes". After the "write" answer: `touch .claude/.write-consent` (rule 7 — the consent-guard hook checks the marker). A partial report on ABORTED at any stage is mandatory.

**Consent for delegated work is collected by this skill.** A subagent spawned through `Task` cannot ask the user. Before each `Task` batch, the "Proceed?" question names the agents and the files each will create or change (reports, test files); that answer covers those files. A delegated step that needs to go beyond its brief (another file, a code or configuration change, a production mutation) stops and reports it, and the parent asks.

Commands are `/web-studio:<name>` in plugin mode and `/<name>` in copy mode. **This skill runs the other studio skills through the `Skill` tool**, one after another; each called skill keeps all of its own phases and gates — the write, commit, tag and "Proceed?" questions of `/changelog`, `/release-checklist` and `/deploy` are asked by those skills, never skipped here — and its verdict comes back as text this skill reads and quotes. `‖` would mean one `Task` batch of agents; this skill launches no two skills at once. Agents are spawned with a studio `subagent_type`: `web-studio:<name>` in plugin mode, `<name>` in copy mode (coordination-rules § Subagents). In the commands below, `<hooks>` is `.claude/hooks/` in copy mode and `${CLAUDE_PLUGIN_ROOT}/hooks/` in plugin mode.

## Phase 1: Checks, one after another
Through the `Skill` tool, in this order: `/perf-audit full` → `/a11y-audit all` → `/security-audit quick` → `/dependency-audit`. Read each verdict line before starting the next. Any failing verdict (`FAIL` from `/a11y-audit` or `/security-audit`, `OVER BUDGET` from `/perf-audit`, `ACTION REQUIRED` from `/dependency-audit`) → stop the sequence at once with a partial report: `ABORTED (stage 1: <skill> <verdict>)` — the remaining checks are named as not run.

## Phase 2: Documents
`/changelog <version>` → `/release-checklist <version>`, each through the `Skill` tool (their own write and commit gates apply; the checklist creates the tag `vX.Y.Z`, with consent, which `/deploy` needs). `NOT READY` from the checklist → `ABORTED (stage 2: release-checklist NOT READY — …)` with the ❌ items (the release file then carries `Verdict: NOT READY (…)`, which `/deploy` reads as BLOCKED).

## Phase 3: Deploy
`/deploy <version>` through the `Skill` tool (confirmations inside; the delegate by `.claude/docs/deploy-target-contract.md`, manual runbook when none is declared) → smoke → monitoring. `BLOCKED (…)` or a red deploy that is rolled back → `ABORTED (stage 3: deploy …)`.

## Phase 4: Summary
1. Version, what shipped, post-deploy metrics, known issues.
2. `production/stage.txt` → `operate`: "May I write `production/stage.txt` → `operate`?" — one `AskUserQuestion`: write (Recommended) · not now. After the "write" answer: `touch .claude/.write-consent`.
3. **Commit gate** (rule 7 (4), `.claude/docs/git-workflow.md` § Documents), recorded before it is asked — `<hooks>session-state.sh set Gate "/team-release Phase 4: commit?"` — and cleared after the answer (`<hooks>session-state.sh set Gate "—"`), so an open gate survives the next turn; one `AskUserQuestion`: `docs: stage operate after vX.Y.Z` staging exactly `production/stage.txt` and `.claude/agent-memory/` when the run changed it (git-workflow § Agent memory), on the default branch (a release is tagged there; when HEAD is a story branch, name it and offer: switch to the default branch and commit there (Recommended) · commit here · leave uncommitted). Nothing is committed without the answer.

Verdict: `RELEASED` | `ABORTED (stage 1: <check> <verdict>)` | `ABORTED (stage 2: …)` | `ABORTED (stage 3: …)`. Next step — one `AskUserQuestion`: `/sprint-plan` for the next cycle (Recommended) · `/incident` if the post-deploy checks fail · stop here.
