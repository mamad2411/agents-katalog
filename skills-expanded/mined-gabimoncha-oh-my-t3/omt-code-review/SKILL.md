---
name: omt-code-review
description: Code review with subagents in T3 Code. Use when the user asks to review uncommitted changes, a branch, a commit, or a pull request. Accepts --profile. Runs report-only reviewers and an oracle, merges the findings, and offers fixes.
---

# Code review

## Rules

- Each `review` and `oracle` task says `Report every finding with its fix. Change no files, and write none under FIXES.` and `You run in plan mode. Stay in it. Do not call ExitPlanMode and do not write a proposed plan. Put the result block in your final assistant message.` Its `delegateTask` sets `interactionMode` to `"plan"`, because the roles alone do not stop edits.
- Dispatch as [Dispatching a child](../omt/references/delegation.md#dispatching-a-child) says, with the plan id `review-<slug>` and `--profile <profile>` in every `omt brief`.
- You make every fix and write every approved test in the main thread.

## Steps

### 0. Check your mode

Call `t3_thread_configure` with no arguments ([delegation.md](../omt/references/delegation.md#your-interaction-mode)). The driver of `modelSelection` is `<your family>`. In `plan` mode, dispatch only `review` and `oracle` children with `interactionMode: "plan"`, write no files, and put the merged findings in your final message. Fixes and a PR checkout need default mode.

Read `profile` and `workflow.review` from `omt profile show [<name>] --json`, with the run's `--profile <name>` when given.

Done when: you know your mode, family, and profile.

### 1. Pick the target

Reviewers diff uncommitted changes with `git status --porcelain -- <paths>` and `git diff HEAD -- <paths>`, and read untracked files in full. A branch uses `git diff <base>...<branch>`, and a commit `git show <sha>`. For a PR, follow [PR review](#pr-review).

Ask only when the target is ambiguous. Pick a kebab-case slug.

Done when: you have the diff command and the file list.

### 2. Size and split

Leave `docs/design/` out of the groups and the count, because the owner reviews designs, not a model. When only design files changed, list them and stop.

With `review.reviewers: auto`, count changed lines with `git diff --shortstat`. Below 200 is the small shape. The large shape has 2 groups from 200, 3 from 1,000, and 4 from 3,000. A number from 1 to 4 sets the groups instead, and 1 is the small shape.

- Small shape: 1 reviewer over the whole change, as `oracle` when `review.oracle` is `on`, else as `review`.
- Large shape: 1 `review` child per group, then 1 `oracle` over the whole change when `review.oracle` is `on`.

Group files by directory, in groups of similar size. With `review.families: both`, odd groups go to Codex (`--unit G<k>.codex --against claudeAgent --strict`) and even groups to Claude (`--unit G<k>.claude --against codex --strict`). The small shape then gets 1 `review` child per family and no oracle. Never start more than 4 reviewers and 1 oracle.

Done when: each changed file outside `docs/design/` is in exactly one group.

### 3. Dispatch the reviewers

Per group, run `omt brief review ... --plan review-<slug> --unit G<k> --round <n> --profile <profile> --save --json`; a small-shape oracle uses `omt brief oracle --unit oracle`. Each task holds the group's diff command, the change's intent, and the report-only lines. Round 1 passes no `--against`, because the author is unknown. Dispatch them together with `mode: "async"`.

A round after fixes dispatches 1 `review` child over all fixes of the round, with `--unit FIX --against <your family>`. Its task gives each finding, its fix, and `git diff HEAD -- <fix paths>`. From round 2, `--prior-file` carries the earlier findings and your responses.

Done when: every group, or the fix review, has a verdict.

### 4. Merge

Drop duplicates of one location and failure, and keep the higher severity. Keep each failure scenario. Keep a missing-test finding only when the plan or the task names that test.

Done when: one list exists, sorted by severity.

### 5. Oracle pass

In the large shape with `review.oracle: on`, dispatch 1 `oracle` with `--unit oracle --against <family>` and `mode: "wait"`, where `<family>` ran most reviews of the round, or is `<your family>` on a tie. Give it the merged findings and the whole diff without `docs/design/`. It confirms or refutes each finding, with evidence, and reports misses.

Done when: the oracle's verdict is merged, or the step is skipped.

### 6. Report and fix loop

In default mode, write the findings to `review-<slug>-r<n>.md` under `omt paths --evidence`, in the [review result](../omt/references/results/review.md) format. Show the owner the verdict, findings, and design files.

With `review.fixLoop: offer`, ask before each fix loop and wait for yes. Then fix each P0 to P2 finding, run its checks, and run the fix review of step 3 with round `<n+1>`. Repeat up to `maxReviewRounds`, then report again.

Done when: the owner has the verdict and any offer.

## PR review

Use the steps above. When any of `review.ci`, `review.verify`, `review.tests`, or `review.crap` is not `off`, read [pr-extras.md](pr-extras.md) and run those extras at the steps it names. The defaults turn all four off.

### PR 1. Target

Run `gh pr view <n> --json title,body,url,baseRefName,baseRefOid,headRefOid,files`, and link the PR. For the return command, save `git branch --show-current`, or `git rev-parse HEAD` for a detached HEAD. Run `git fetch origin <baseRefName> pull/<n>/head`.

Check out the PR only when a step needs it: ask the owner first when `git status --porcelain` prints anything, then run `gh pr checkout <n>`.

Done when: the PR is linked, and its commit ids and your branch are saved.

### PR 2. Rules

List `AGENTS.md` and `CLAUDE.md` in the root and above each changed file, `CONTRIBUTING.md`, the docs they link to, the fitting project skills, and the lint and CI config files, for every review task. Each finding that breaks a written rule cites the rule file and line.

Done when: the rule-file list is in the briefs.

### PR 3. Round 1

Run step 3 with the rule-file list. Round 1 and its oracle use `git diff <baseRefOid>...<headRefOid> -- <paths> ':(exclude)docs/design'`, and read files with `git show <headRefOid>:<path>`. Without a PR checkout, reviewers run no tests or builds.

Done when: every group has a verdict.

### PR 4. Merge and oracle

Merge with step 4, and run step 5 with `.` as `<paths>`.

Done when: the oracle's verdict is merged, or the oracle is off.

### PR 5. Report

Write `review-<slug>-r<n>.md` under `omt paths --evidence`, with:

- the verdict and findings by severity, with rule citations
- the result of each extra that ran
- the design files
- the return command: `git switch <branch>`, or `git switch --detach <commit>`

Done when: the owner has the evidence file and the return command.

### PR 6. Offers

Offer the fix loop of step 6. After yes, check out the PR (PR step 1). Run `omt git start --run review-<slug>` before the first fix. Commit each fix with `omt git commit -m "<message>" --path <path>`, and push to the PR branch with `omt git pr --pr <n>`, which updates only that PR and asks for a fork PR or another author's PR. Pass `--run review-<slug> --profile <profile>` to both. For a fork PR, leave the commits local and tell the owner. Follow [Git actions](../omt/references/delegation.md#git-actions) on `ask:` and `off:`. Post nothing else to GitHub.

Done when: each approved fix is pushed, or the owner said no.
