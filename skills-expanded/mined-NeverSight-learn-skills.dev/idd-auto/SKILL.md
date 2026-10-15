---
name: idd-auto
description: "User-invoked autonomous completion of an exact convention-linked IDD project, delivering one issue at a time until PRD implementation scope is complete or a fail-closed blocker requires the user."
compatibility: "Requires git and GitHub CLI (gh); works with Claude Code, Codex, Pi, and OpenCode."
---

# /idd-auto — finish one PRD-driven project

Drive an existing exact `{project}` ↔ `{project}-prd` pair through repeated `/idd-plan` → `/idd-issue` → `/idd` → `/idd-land` cycles. Keep one active issue at a time and preserve every constituent duplicate, acceptance, verification, review, merge, cleanup, and reconciliation gate. Publication is outside this command and is never invoked or scheduled by `/idd-auto`.

An explicit `/idd-auto` invocation authorizes private creation of the uniquely missing implementation sibling for an existing clean PRD repository, plus creation and delivery of sequential PRD-derived issues, including their branches, commits, pushes, linked PRs, squash merges, closures, branch cleanup, and verified `PROGRESS.md` reconciliation. It does not authorize deployment, publication, force-push, bypassing a gate, accepting residuals, inventing requirements, parallel issue delivery, or changes outside the exact pair.

## Orient and bind the completion target

1. Resolve this installed skill directory and its sibling `idd-plan`, `idd-issue`, `idd`, `idd-land`, and `idd-acceptance` directories in the same installation root. Read their current skill sources in full and execute their procedures and bundled scripts rather than copying stale phase logic. A missing sibling is an incomplete composite installation and stops with the exact required skill names. Their standalone completion messages become internal phase transitions while this orchestrator remains active.
2. Resolve the supplied project name/path or current checkout with the sibling `idd-plan/scripts/resolve-prd-pair.sh`. When starting from an existing clean PRD repository whose exact implementation sibling alone is absent, run `idd-plan/scripts/init-implementation.sh` and read back its private remote, initial commit, and clean sibling checkout; ambiguity or any other missing pair state still stops. Require matching GitHub origins, authentication, repository instructions, and clean trees; an existing clean issue branch may be resumed only when live state binds it uniquely to the one active issue.
3. Pull clean default branches with `--ff-only`. Read `PRD.md`, `PROGRESS.md`, live issues/comments, PRs/reviews/checks, closing links, and squash commits. GitHub owns lifecycle truth; the PRD owns accepted requirements and dependency/release boundaries; the tracker is reconciled evidence, not permission to skip either.
4. Define completion as every accepted implementation requirement in the PRD mapped to landed or validated tracker evidence, with no corresponding open issue or PR. Preserve `Landed` versus `Validated`; deployment, publication, or a product decision that cannot be completed by this issue workflow is an external blocker. A user may separately invoke `$idd-publish <project>` after this command finishes.

## Run the one-issue loop

At the start of every iteration, reconstruct state from the pair and GitHub. Never create a trace, queue, speculative backlog, or hidden progress file.

1. **Resume before creating.** If tracker/live state has one active issue, continue its current phase. An issue without a PR resumes `idd`; an open PR with introduced failures resumes `idd` repair and verification; a fully accepted green PR advances through `idd-land`. A merged issue with stale progress advances through `idd-plan --reconcile`. Multiple plausible active issues, PRs, repositories, or tracker rows stop as ambiguous.
2. **Select one next outcome.** When no work is active, execute `idd-plan` default mode. Require its earliest dependency-respecting, independently reviewable issue contract. If it reports no next implementation issue, audit the completion definition before declaring the project finished.
3. **Create exactly one issue.** Execute `idd-issue` with that public-safe contract and target implementation repository. Honor its open-and-closed duplicate search and read-back gate. A duplicate becomes the active issue; never create a second issue in the same iteration.
4. **Implement and publish.** Execute `idd` for the active issue through focused implementation, repository-native verification, explicit staging, commit, push, and one linked PR. Wait for reported checks and reviews. Repair introduced failures through the same issue branch; stop on an unrelated required red gate, conflict, requested changes needing user intent, or unproved acceptance.
5. **Land and reconcile.** When every acceptance item and required check is green, execute `idd-land` without residual acceptance. Verify squash merge, closure, default-branch refresh, local/remote branch deletion, and automatic PRD reconciliation, then begin the next iteration from fresh live state.
6. When `idd-plan` reports no remaining implementation outcome, invoke `/idd-acceptance <project>` from clean default branches. Treat its result as a required final gate. A product failure against an accepted requirement becomes one linked repair issue under the existing slice; it does not rewrite the PRD. A genuinely new feature or changed behavior is outside the frozen contract: stop for explicit user authorization, then update the PRD and delivery slices before creating its issue. Update `PROGRESS.md` only with verified lifecycle evidence through normal reconciliation. Do not declare completion from issue-level checks alone.

## GATE — fail closed or finish

Never weaken a constituent gate to keep the loop moving. When authority is ambiguous, either tree contains unrelated work, the next issue needs a material product choice, acceptance remains unproved, CI/review/conflict policy is red, external state is required, or PRD reconciliation fails, name one precise blocker. If user choice or authority can clear it, ask one focused question through the runner's interactive input when available (otherwise chat), then reconstruct live state and resume after the answer; a non-user-clearable blocker ends the run. Do not auto-apply `--accept-residuals`; only a fresh user instruction can accept named gaps. Do not invoke `/idd-evolve` for a project defect; reserve it for proven IDD methodology lessons.

Never end with a checkpoint or progress report. If the final audit finds remaining implementation scope and no permitted blocker, start the next iteration. Declare completion only after the audit proves the completion target, both repositories are clean and synchronized on their default branches, no run feature branch remains, and `PROGRESS.md` contains verified issue/PR/squash evidence. Return the created and landed issue/PR URLs, final implementation and PRD commits, verification state, and either `complete` or the single resumable blocker.
