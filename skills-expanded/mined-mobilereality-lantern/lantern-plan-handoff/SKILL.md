---
name: lantern-plan-handoff
description: Hand an approved Lantern plan to `lantern-delegate` and keep it ticked - `plan.mjs handoff` names the items of the next unblocked stage (a stage with unanswered questions gives the questions to ask first), each delegate's brief is written from its item, delegates record `sync.mjs pr ... --plan <slug> --item <id>`, and item status comes from the pull request records. Use when the user says "Plan: <slug>", "delegate the plan", "run the plan", "start the next stage", "what is left in the plan", "plan status", "mark the item verified", "wykonaj plan", or when lantern-delegate is given a plan. Needs an approved plan. Not for writing or reviewing the plan (`lantern-plan-stages`, `lantern-plan-review`).
---

# Lantern plan: hand-off and ticking

An approved plan is the input; pull requests are the ticks. The plan file is not edited per pull request
(many PRs would conflict on it). Each PR record carries `#plan <slug> <item>` and the status follows.
`$P` is the `lantern-plan` folder; run from the project root.

## Hand over

1. `plan.mjs handoff <slug>`. Exit 1 means stop and say why: not approved, a section changed since, or
   `check` errors. Fix with `lantern-plan-review` or `lantern-plan-stages`; never dispatch around it.
2. It prints the next stage. Either **items to delegate** (up to three at once, items of one stage) or
   **questions to ask**: ask the user those, record each answer (`plan.mjs add <slug> answer <id> <who>
   <text>`), run `handoff` again.
3. Write each delegate's brief from its item (`lantern-delegate`, "Write the brief"):
   - **Goal**: the item title, one sentence.
   - **Should**: the acceptance check, as the thing that must be true.
   - **Should not**: the other items of the stage and the stages after it.
   - **Context**: `Plan: <slug>, item <id>`, and the impacted features and files from the plan.
   - **Verify**: the acceptance check, plus the project's own checks. Keep a line that fails if the item
     is not done.
   - **Lantern**: add that the PR record is written with `--plan <slug> --item <id>`.
4. The plan, committed and pushed, must be on the base the delegates fork from; the brief's `Base` says so.
5. Pass `--plan <slug>` to `preflight.mjs`: it also checks that the plan is approved and clean and that
   this skill is installed.

## The delegate's side

Its PR record gets the tick: `node <Skills>/lantern-sync/scripts/sync.mjs pr <id> ... --plan <slug> --item <id>`
(repeat `--item` when one PR does several items). `sync.mjs` refuses a plan or item that does not exist.
`verify` warns when a record names an unknown plan or item, and fails when the branch broke a plan file.

## Status

`plan.mjs status <slug>` derives it from the PR records and git, offline (run `git fetch` first):

| status | when |
|---|---|
| planned | no PR record names the item |
| in progress | a PR that names it is open |
| implemented | a PR that names it is merged and none is open |
| verified | the plan holds `#verified <item>` |

A branch record (`.lantern/local/<branch>.branch`, from a run with no host PR, once the orchestrator has copied it into the project) counts like a PR record: open while its branch exists unmerged, merged when its `#head` is in the base. A declined PR counts for nothing. A stage is done when all its items are implemented or verified, and the
next stage only starts then.

## Verify an item

After the merge, run the item's acceptance check yourself. If it passes, with the user's say-so:
`plan.mjs verified <slug> <item> --by <name>`, then commit that one line (`docs: verify <slug> <item>`).
It is the only progress the plan itself stores, and you make it, one at a time, never in a delegate's PR.

Mark items verified **before** dismissing their pull requests: `sync.mjs dismiss` deletes the record, and
the tick goes with it (it warns).
