---
name: omt-ulw
description: ulw / ultrawork in T3 Code. Use when the user says start ulw, start ultrawork, or ulw, or asks to build, fix, or ship something with subagents in a T3 thread. The main thread explores, asks, plans, and builds; one review child and one QA child check the work before it reports done with evidence.
---

# Ultrawork

## Contract

Run the full flow for every task, however small. A small task gets a LIGHT run, not a shortcut. You explore, plan, build, write the planned tests, and fix; one review child (step 8) and one QA child (step 10) check the work, as `build.review` and `build.oracle` allow. A LIGHT run skips only the plan review and the plan approval. Done means a check that can fail ran and passed; a child's claim is not done ([results.md](../omt/references/results.md#a-claim-is-not-evidence)). Dispatch each child by [Dispatching a child](../omt/references/delegation.md#dispatching-a-child).

## Rules

- End your turn only for the owner (a question batch, a plan approval, or the report) or to wait for a child by [Waiting](../omt/references/delegation.md#waiting).
- One brief per child. Each brief stands alone ([brief.md](../omt/references/brief.md)).
- Read only the part of a child's result that your next action needs.
- Tick plan items only with `omt plan mark <slug> <id> <done|open|blocked>`.
- After a context reset, read `omt plan status <slug>`, `omt ledger list --plan <slug>`, and the profile before you act.

## Steps

### 0. Check your mode

Check your mode and family by [Your interaction mode](../omt/references/delegation.md#your-interaction-mode). Ultrawork edits files, so in `plan` mode ask the user to switch this thread to default mode, or offer `omt-plan` to deliver a plan in your final message. Then run the [branch check](../omt/references/delegation.md#branch-check). On the first run in a project, follow [Worktree setup](../omt/references/delegation.md#worktree-setup).

Done when: you run in `default` mode, or the user has the question.

### 1. Question or goal

When the message asks a question and names no change, run the `omt-research` skill instead and stop here.

Done when: the message is a goal, or `omt-research` has the question.

### 2. Explore

Pick the plan slug (`^[a-z0-9][a-z0-9-]{0,63}$`, such as `http-retry`) for the whole run. Read the profile with `omt profile show [<name>] --json`, or `omt profile show --plan <slug> --json` once the plan exists.

Read the code that the goal touches yourself. Send only broad reads to parallel `explore` children, one narrow question each, with `--unit E<k>`.

Done when: you can name the files and functions that the change touches, each with a `path:line` citation.

### 3. Frame

Write down the objective in one sentence, the done conditions, and the tier.

- Each done condition is a check that can fail: a command, a test, or an observable result.
- Tier LIGHT: one or two units, one area of code, no design decision left. Tier HEAVY: anything else.

After `omt plan profile <slug> <name>`, read the profile again.

Done when: your reply has the objective, at least one failable done condition, and the tier, and `omt roles` shows a target for `review` and `qa`, or you report the role that is unavailable and why.

### 4. Ask

Ask every open owner question in one batch, each with 2 to 4 options and your recommendation. Read the code for a question that the code can answer. End the turn and wait. Explore again when an answer opens new code, and ask the next batch.

Done when: no owner question is open.

### 5. Plan

When `$(omt paths --omt)/.gitignore` is missing, run `omt init` first.

- LIGHT: run `omt plan new <slug> --light` and fill it yourself by [planning.md](../omt/references/planning.md). It needs no owner approval.
- HEAVY: run the `omt-plan` skill with the slug before any plan file exists. It writes and reviews the plan, then returns here. The owner approves the plan before you build.

Pass the run's `--profile <name>` to plan creation or to `omt-plan`. With `build.qa: planned`, keep only the owner's approved `## Tests` lines; with `off`, leave `## Tests` empty.

A unit that implements a design or changes UI has the role `ui`, also in a LIGHT plan. It cites an approved design spec when one exists, else the task requirements. Plan an `omt-design` step only when the user asks for a design pass first.

Keep the `F2` oracle item (`- [ ] F2. The oracle role approves the whole change.`) in `## Final verification` only when `build.oracle` requires it for the tier: `heavy` for HEAVY, `always` for both, `off` for neither. Check it again after a profile switch.

Done when: `omt plan status <slug>` shows every unit, every done condition of step 3 maps to a unit or a final check, and (HEAVY) the owner approved the plan.

### 6. Design check

Run `omt git start --plan <slug>` before the first file of the run changes. When the plan holds a requested design pass that has not run, run `omt-design` with the slug, and wait for the owner's approval of the spec before you build the affected UI units. Without one, build the UI from the task requirements.

Done when: the start record exists, and each UI unit has an approved design spec or the task requirements, or the plan has no UI unit.

### 7. Build

Build the units in the order of the `ready:` line of `omt plan status <slug>`. For each unit:

1. Edit the files in its scope.
2. Run its verify command, and save the output in the directory that `omt paths --evidence` prints. Fix and run it again until it passes.
3. With `build.qa: planned`, write the unit's tests from `## Tests`. Write no test that has no line.
4. With `build.failureProofs: on`, prove that each new test fails without the change, in a private copy (`git ls-files -co --exclude-standard -z | tar --null -T - -cf - | tar -x -C "$copy"` into a `mktemp -d` folder, with `node_modules` linked). Break the asserted behavior there, see the test fail, and delete the copy. Never break files in the shared checkout.
5. Run `omt plan mark <slug> <unit> done`.

A `ui` unit follows its approved design spec when one exists. Build it yourself or send it to a `ui` child by [Main thread or child](../omt/references/roles.md#main-thread-or-child). When every `ui` target fails, stop and tell the user; do not switch to `execute`.

Independent track: a large unit whose scope no other open unit touches may go to an `execute`, `ui`, or `writing` child while you build the rest. Check its `DONE` claim, run its verify command yourself, and add its planned tests and failure proofs with items 3 and 4 before you mark it done.

Run each shared build or test command by [Shared builds](../omt/references/delegation.md#shared-builds).

Done when: every unit is marked done and its verify command passed in your own run.

### 8. Review

- When `build.oracle` requires the oracle for the tier, the review child uses the `oracle` role, also when `build.review` is `off`, with `--unit F2`.
- Otherwise it uses the `review` role with `--unit REVIEW`.
- With `build.review: off` and no required oracle, skip this step and step 9.

Write the context to a temp file and pass it with `--context-file`: the objective, the done conditions, the plan `## Summary`, and the scope paths. Leave `docs/design/` out of the scope paths: the owner reviews designs, not a model. For a `ui` unit, apply the [design exclusion](#10-qa) too.

The task tells the reviewer to read `git status --porcelain` and `git diff HEAD` of the scope paths and every untracked file, to fix each local finding itself (a clear fix inside the changed files that agrees with the plan Summary), to report every other finding, and to list its fixes under `FIXES`. A `read-only` reviewer reports every finding with its fix instead.

Before you dispatch, stage your work with `git add -A -- <scope paths>`, so that the reviewer's fixes stay unstaged. Pass `--against <your family> --strict`, and from round 2 every prior finding with its response in `--prior-file`. Use `mode: "wait"`.

Review and QA never run at the same time, because the reviewer edits files.

Done when: the review child returned a result block and `omt ledger done` recorded it, or this step is skipped.

### 9. Read the fix diff and fix

Read the reviewer's unstaged fix diff (`git diff` and `git status --porcelain` of the scope paths) before QA starts, then stage it. Undo a fix that you disprove, and say why in the next `--prior-file`.

Keep a finding that breaks a done condition, a plan requirement, or correctness for inputs that the plan covers. Drop a style preference, a state that the plan rules out, and a missing test that the plan does not name. Never drop a finding because it is rare. Record each dropped finding with its reason under `Log` and in the next `--prior-file`.

Fix each kept finding yourself, and run the verify commands of the units that the fix touches.

- `BLOCK` for a wrong approach, or a finding whose fix changes the plan: mark the unit `blocked`, then re-plan it (step 5) or ask the owner.
- With `build.review: every-round`, run step 8 again with the next `--round`, until it returns `APPROVE` or the run reaches `maxReviewRounds`. With `first-round`, run no second review.
- When findings stay open after the last review, ask the owner.
- With the oracle, mark `F2` done when it returns `APPROVE`, or when you drop every finding of the last oracle round.

Done when: every kept finding is fixed or is with the owner, and you read every fix diff of the reviewer.

### 10. QA

Dispatch one `qa` child with `--unit QA` and `mode: "wait"`. Give it every verify command of the plan, the final checks with a command, and the device flows, each with its steps and expected result. Name the scope paths as the code under test. Route device checks by [Verification and devices](../omt/references/delegation.md#verification-and-devices).

Design exclusion: for a `ui` unit, leave `docs/design/` and every check that compares the result with the design out of the QA and review tasks. QA checks behavior, not looks.

Read only the exit code of each `CHECKS` line and the last lines of each failed log. Mark each `D` and `F` item done after its command passed in the QA run.

Done when: the QA result is recorded and every check passed, or step 11 has the failures.

### 11. Fix failed checks

For each failed check, find the cause in its log, fix it yourself, and run the check yourself. Then dispatch QA again for only the failed checks, with the next `--round`. A busy lock or a failure outside the run's scope follows [Shared builds](../omt/references/delegation.md#shared-builds). After 2 QA re-runs, stop and ask the owner, with each failed command, its exit code, and its log path.

Done when: every check passed in a QA run, or the owner has the failures.

### 12. Ship and report

After every check passed, make one commit for the run with `omt git commit`, then push and open or update the PR with `omt git pr` ([Git actions](../omt/references/delegation.md#git-actions)). When you create a PR, follow [Pull requests](../omt/references/delegation.md#pull-requests).

The report contains:

- What changed, by file or area.
- Each done condition with its command, exit code, and log path from the QA run.
- The review verdict, the reviewer's fixes, and the findings that you fixed or dropped, with the reason.
- The QA verdict and each re-run, with each screenshot as a Markdown image with its absolute path, grouped by screen.
- The commit hash and the PR URL, or the reason that the git policy gave.
- Open items: blocked units, open findings, and decisions left.

Done when: every done condition from step 3 is in the report with evidence or as an open item.
