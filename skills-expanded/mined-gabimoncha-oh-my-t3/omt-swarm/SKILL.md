---
name: omt-swarm
description: Build one plan as parallel tracks in separate T3 worktree threads. Splits the plan into tracks with disjoint scopes, launches and waits for each track, reviews every track diff with one child, merges the branches, runs one QA child, and opens one draft PR.
disable-model-invocation: true
---

# Swarm

Each track is a top-level T3 thread on its own worktree and branch, which builds its units with `omt-ulw` and commits. You split, launch, wait, review, merge, test, and open the PR. You do not build.

Invoking this skill is the user request that `t3_thread_launch` needs ([Top-level threads](../omt/references/delegation.md#top-level-threads)).

## Rules

- The input is a plan from `omt-plan`. Ask no question batches, and run no plan review.
- Wait inside your turn: `t3_thread_wait` for tracks, `mode: "wait"` for children. Use no `schedule_task` and no heartbeat.
- End your turn only for a blocker, a check that fails after the last QA re-run, or the report.
- Tracks never push. Children never commit. You commit their accepted fixes and own the PR.
- Dispatch review and QA children by [Dispatching a child](../omt/references/delegation.md#dispatching-a-child). A track is not a `delegate_task` child: record it with `omt ledger add --plan <slug> --unit <track> --role swarm --round 1 --attempt 1 --status <status> --note <note>`, and never settle it.
- Tick plan items only with `omt plan mark <slug> <id> <done|open|blocked>`.
- After a context reset, read `omt plan status <slug>` and `omt ledger list --plan <slug>` first.

## Steps

### 0. Check the modes

Call `t3_thread_configure` with no arguments. `t3_thread_launch` needs `full-access` runtime and `default` interaction mode. Keep the `modelSelection` driver as `<your family>`.

On the default branch, ask the owner for a feature branch and stop. Then run `omt git behind --ff` ([Branch check](../omt/references/delegation.md#branch-check)). On the first run in a project, or after a `WARN` worktree line, follow [worktrees.md](../omt/references/worktrees.md).

Done when: both modes match and you are on an up-to-date feature branch, or you stopped and told the user what to change.

### 1. Read the plan

Find the plan slug in the user's message or `omt plan list`. With no plan, tell the user to run `omt-plan` first, and stop. Keep the output of `omt plan status <slug>` and `omt profile show --plan <slug> --json`.

When `git status --porcelain` lists changes outside `.omt3/` or `.omt/`, tell the user that uncommitted edits do not reach the tracks, and stop. Then run `omt git start --plan <slug>`.

Done when: the plan exists, the checkout is clean, and the start record exists.

### 2. Split

Run the `omt-ulw` step 6 design check here: run a requested design pass with `omt-design`, get the owner's approval, and commit the spec with `omt git commit` before you record `<base>`.

Split the open units into at most `maxParallel` tracks, each with a kebab-case name, its units, and its scope paths. Two tracks share no file, and a unit goes in the track of the units that it depends on.

Keep `<base>` from `git rev-parse HEAD`. For each track, run `omt plan new <slug>-<track> --light --profile <profile>`, and copy in its units, their `## Tests` lines, done conditions, final checks, the `## Summary`, and design specs. Record the tier by `omt-ulw` step 3. Run `omt plan limit <slug>-<track> <k>` with `<k>` 1 or 2, and leave `limits` in the shared `.omt3/` config as it is.

Log the split in the plan: each track, its units, scope, branch `omt/<slug>/<track>`, and `<base>`.

Done when: every open unit is in exactly one track, no two tracks share a file, and each track has a plan `<slug>-<track>`.

### 3. Launch

For each track, call `t3_thread_launch` with:

```json
{
  "title": "<slug>: <track>",
  "clientRequestId": "<slug>-<track>",
  "workspaceStrategy": { "type": "worktree", "baseRef": "<base>", "branch": "omt/<slug>/<track>", "startFromOrigin": false },
  "message": "<launch message>"
}
```

The launch message is a plain task, not an `omt brief`:

1. You are track `<track>` of swarm plan `<slug>`, with plan `<slug>-<track>` and scope `<scope paths>`. Edit no file outside it.
2. Call `t3_thread_configure` with no arguments, and use your driver as `<your family>`. Read your plan and `omt profile show --plan <slug>-<track> --json`. Apply the `F2` rule of `omt-ulw` step 5. Build from the approved design spec in `<base>`, else from the task, without `omt-design`.
3. Run `omt git start --plan <slug>-<track>`, then `omt-ulw` steps 7 to 12 for your units, with your own review and QA children. In step 12, run only `omt git commit --plan <slug>-<track>`: no push, no PR.
4. Report what changed, each check with its exit code and log path, and the commit hash.
5. End with one line: `TRACK <track>: DONE <commit hash>` or `TRACK <track>: BLOCKED <reason>`.

Keep each branch's path from `git worktree list --porcelain` as `<track worktree>`. Record each launch as `dispatched`, with the `threadId` as the note. After a failed or lost launch, launch again with the same `clientRequestId` only when `t3_thread_list` does not show the thread.

Done when: every track has exactly one thread id in the ledger and one worktree path.

### 4. Wait

For each track, call `t3_thread_wait` with `threadId`, `untilDelegatedWorkSettled: true`, and `timeoutMs` up to 3,600,000, again on `waitTimedOut: true`. Read its last message with `t3_thread_read`, and check the commit with `git log --oneline <base>..omt/<slug>/<track>`.

Record `DONE` as `completed` with the commit hash. Record `BLOCKED` or a question as `failed` with the reason, pass it to the owner, send the answer with `t3_thread_send`, and wait again.

Done when: every track reported `DONE` with a commit on its branch, or the owner has its blocker.

### 5. Review before the merge

Run `omt git start --plan <slug>` in each `<track worktree>`. Write a context file: the `## Summary`, the done conditions, and each track's name, branch, worktree, and scope paths, without `docs/design/`.

The review task says:

- Review each `git diff <base>...omt/<slug>/<track>` against the Summary, and check that the tracks fit together: names, interfaces, and behavior.
- Fix each local finding, inside the track's changed files, in its `<track worktree>`, and leave it uncommitted. List each fix under `FIXES` with its track and absolute paths.
- Report each other finding.

Build the brief with `omt brief review --task-file - --context-file <file> --scope <track worktree>/<path> ... --title "review: <slug> tracks" --plan <slug> --unit REVIEW --against <your family> --strict --save --json`, and dispatch it with `mode: "wait"`.

Done when: the review child returned a result block, and `omt ledger done` recorded it.

### 6. Read the fix diff and fix

For each track with fixes, read `git -C <track worktree> diff` and `status --porcelain`. Undo a fix that you disprove, and report why. Commit the rest in the track worktree with `omt git commit -m "<message>" --plan <slug>` and one `--path` per path under `FIXES`.

Apply the relevance check of `omt-ulw` step 9 to each reported finding, and log each dropped one with its reason. Fix each kept finding in its track worktree, run the track's verify commands, and commit there. Send a fix that needs deep track knowledge to that track with `t3_thread_send`, wait as in step 4, and check the new commit. When a finding changes the plan, mark the unit `blocked` and ask the owner.

Done when: every accepted fix and kept finding is committed on its track branch, or the owner has it.

### 7. Merge

Before each merge, run `omt git check merge --plan <slug>`. On `auto`, run `git merge --no-ff omt/<slug>/<track>`. On `ask`, ask the owner. On `off`, do not merge, and report it.

Resolve each conflict yourself. When it needs deep knowledge of one track, run `git merge --abort`, ask that track with `t3_thread_send` to merge your branch, resolve the conflict, verify, and commit without a push, then wait as in step 4 and merge again. After each merge, mark each unit of the track `done`.

Done when: every `DONE` track branch is merged, and its units are marked done.

### 8. QA

Dispatch one `qa` child on the merged code with the plan's verify commands, final checks, and device flows with their steps and expected results. Apply the design exclusion of `omt-ulw` step 10, and route device checks by [Verification and devices](../omt/references/delegation.md#verification-and-devices). Build the brief with `omt brief qa --task-file - --scope <path> ... --verify <command> ... --title "qa: <slug>" --plan <slug> --unit QA --round <n> --save --json`, and dispatch it with `mode: "wait"`.

Read only each `CHECKS` exit code and the tail of each failed log. Mark each `D` and `F` item done after its command passed in QA.

Done when: the QA result is recorded and every check passed, or step 9 has the failures.

### 9. Fix failed checks

For each failed check, find the cause in its log, fix it on your branch, and run the check yourself. Then dispatch QA for only the failed checks with the next `--round`, and mark the items that pass. After 2 re-runs, ask the owner, with each failed command, exit code, and log path.

Done when: every check passed in a QA run, or the owner has the failures.

### 10. Finish

Commit your QA fixes with `omt git commit -m "<message>" --plan <slug>`. Run `omt git pr --title "<title>" --body-file <file> --plan <slug>`, which opens a draft PR. On `split:`, run `omt git stack` by [Git actions](../omt/references/delegation.md#git-actions). Link and watch the PR by [Pull requests](../omt/references/delegation.md#pull-requests).

The report contains what the `omt-ulw` step 12 report contains, plus each track with its units, branch, and commit, and each merge conflict with its resolution.

Done when: every done condition is in the report with evidence or as an open item, and the PR is linked or its policy reason reported.
