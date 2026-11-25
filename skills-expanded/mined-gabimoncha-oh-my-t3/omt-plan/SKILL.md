---
name: omt-plan
description: Plan before code in T3 Code. Use when the user asks for a plan, a spec, or a design before implementation, asks to stress-test or find the edge cases of a goal, or when omt-ulw needs a reviewed plan for a HEAVY task. The main thread explores, asks owner question batches, writes an omt plan file, and gets it reviewed from the other model family in at most 2 rounds.
---

# Plan

You write a plan that the main thread can build from without another owner decision, and you get it reviewed. You plan only, also when `omt-ulw` calls this skill, and change no code.

You explore, ask, and write the plan yourself. Children only explore (`explore`) and review the plan (`plan-review`). Dispatch each child by [Dispatching a child](../omt/references/delegation.md#dispatching-a-child), and wait by [Waiting](../omt/references/delegation.md#waiting). End your turn for the owner only for a batch of questions, a plan approval, or the hand-off. Read only the part of a child's result that your next action needs.

## Steps

### 0. Check your mode

Call `t3_thread_configure` with no arguments and read your `interactionMode` and `modelSelection` ([delegation.md](../omt/references/delegation.md#your-interaction-mode)). Keep the driver of `modelSelection`, such as `claudeAgent` or `codex`, as your family. Step 4 passes it to `--against`.

In `plan` mode, dispatch only read-only children and `plan-review`, with no `--save`. Write no plan file: put the plan text in the review brief. Deliver the finished plan in your final message.

Then run the [branch check](../omt/references/delegation.md#branch-check).

Done when: you know your mode and your family, and the branch check printed its result.

### 1. Pick the slug and explore

Use the slug that `omt-ulw` passes. Otherwise pick one that matches `^[a-z0-9][a-z0-9-]{0,63}$`. Every brief of this plan uses `--plan <slug>`. When the user names a profile, pass `--profile <name>` to each `omt brief` before the plan file exists.

Read the code that the goal touches yourself. Send only broad reads to 1 to `maxParallel` read-only `explore` children in parallel, one narrow question each, with the unit `E<k>`. Dispatch them with `mode: "async"`, and follow `next` until every result is in.

Done when: you can name each file and function that the change touches, with a `path:line` citation.

### 2. Ask

List the decisions that the plan needs, and settle each one from the code, the docs, or the request. What remains is an owner decision: a choice between valid options that changes what the user gets.

When the goal has no done condition that can fail, or 4 or more owner decisions remain, offer the stress test (step 2a) as the first option of the first batch.

Before you ask, finish all work that does not depend on the answers: the research and a draft plan. Then ask every open owner decision in one batch. Give each question 2 to 4 options and your recommendation. Include the proposed `## Tests` lines, and ask the owner to approve them with the plan. Give a reason for each line outside `workflow.plan.testLayers`. End the turn and wait for the answers.

After the answers, explore again when an answer opens new code, and ask the next batch. Stop when no question is open.

Done when: every decision is settled from evidence or answered by the owner.

### 2a. Stress-test the goal (optional)

Run this step only when the owner picks the stress test. You do it yourself, with no `grill` child and no grill file.

Find these items from the code and the request:

- The edge cases. Give each one an id `GE<k>`, its trigger, its effect, a proposed handling, and a test layer (`integration`, `unit`, or `none`).
- The options for the direction of the work, each with its gain and its cost, and your recommendation.
- The open questions, each with 2 to 4 options and your recommendation.

Ask them in the next step 2 batch. The owner accepts, changes, or drops each edge case by its id. Ask again about an answer that conflicts with the code, and cite the code. Write the chosen direction, the decisions, and each answered edge case under `## Research` in step 3. An accepted or changed edge case with an `integration` or `unit` layer becomes a `## Tests` line with `Reason: edge case GE<k>`. One with the layer `none` goes into the done condition of the unit that handles it. A dropped edge case gets neither.

Done when: a direction is chosen, and each edge case is accepted, changed, or dropped.

### 3. Write the plan

`omt plan status <slug>` prints the absolute plan path, also from a worktree. Edit the plan at that path. When no plan exists, run `omt plan new <slug> --title "<title>" --profile <name>`, after `omt init` when `$(omt paths --omt)/.gitignore` is missing. Keep an existing plan: pass no `--force`. Fill every section yourself by [planning.md](../omt/references/planning.md).

- Under `## Research`, write each research question, its answer, and its sources.
- Paste the output of `omt roles --plan <slug>` under `Roles`.
- UI units use the `ui` role, and cite an approved design spec when one exists. Plan an `omt-design` step only when the user asked for a design pass first. A missing spec or design tool does not block a UI unit.
- Name each shared resource and lock its verify commands, by [planning.md](../omt/references/planning.md).

Test lines, by [planning.md](../omt/references/planning.md):

- When `workflow.build.qa` is `off`, leave `## Tests` empty.
- Otherwise, write the owner's approved lines, with the layers in `workflow.plan.testLayers`.
- Keep edge cases out of the e2e lines.

Fill `## Summary` last, by [planning.md](../omt/references/planning.md), and update it after each review fix.

Done when: `omt plan status <slug>` lists every unit, each unit has all five fields, and `## Summary` is the last section that you filled.

### 4. Plan review

Read `workflow.plan.review` from `omt profile show --plan <slug> --json`, or in `plan` mode, with no plan file, from `omt profile show [<name>] --json`:

- `owner`: ask the owner to approve the plan and its `## Tests` list. Dispatch no child. After the approval, go to step 5.
- `two-families`: 1 `plan-review` child, briefed with `--against <your family> --strict`. When the brief exits 1, stop and tell the user that no reviewer from the other family can run.
- `one`: 1 `plan-review` child on any family, with no `--against`.

Run at most 2 rounds. Each round is a fresh `plan-review` child with the unit `plan` and `--round <n>`; reuse no reviewer thread. Make every plan edit before the brief. The task names the plan path and the effective `workflow.plan.testLayers`. Dispatch with `mode: "wait"`.

Round 1: `APPROVE` ends the review, and notes do not block. Otherwise the reviewer's blocking findings are the frozen blocker list. Write the list under `Log` in the plan. Fix each blocker in the plan yourself, and update `## Summary`.

Round 2: pass `--prior-file` with the frozen blocker list and your response to each blocker. The reviewer checks only the frozen blockers and the regressions from your fixes. Record any other finding as a note.

After round 2, run no more rounds. When blockers stay open, ask the owner about each one in one batch, with 2 to 4 options and your recommendation. Apply the answers to the plan.

Done when: a round returned `APPROVE`, the owner approved under `owner`, or the owner answered each blocker that stayed open after round 2.

### 5. Hand off

Show the plan to the owner, also when `omt-ulw` called this skill. The reply holds:

- the `## Summary` text in full;
- the plan path;
- the review result;
- each decision that is still open.

When `omt-ulw` called this skill, return to its step 5 with the plan slug. There the owner approves the plan, and its design check runs before any `ui` unit is built. Called alone, stop. Start no units.

Done when: the owner has the summary in the reply, and the user, or the `omt-ulw` run, has the plan path and the review result.
