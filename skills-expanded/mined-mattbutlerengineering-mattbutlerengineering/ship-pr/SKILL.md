---
name: ship-pr
description: "Runs the full merge boundary on one open PR — fast-path decision, CI-gate classification, specialist and universal review, then merge — via the implement-queue profile's hooks, outside the queue loop. Invoke with /ship-pr <N> [--ready]."
user-invocable: true
---

# /ship-pr

A single-PR run of the same merge boundary `/idea-to-prod:implement-queue`
runs per-PR in its own loop. This skill owns no gate logic of its own — every
step below is a pointer into `.claude/implement-queue.md`'s profile and the
scripts it names. If a step's rule ever needs to change, change it there;
this file must never grow a restated copy of a rule it only references (the
duplicated-sentence drift recorded in `.claude/rules/gotchas.md` is exactly
this failure mode).

## Invocation

```
/ship-pr <N> [--ready]
```

- `<N>` — an open PR number.
- `--ready` — the PR is a draft; without this flag a draft PR is refused
  outright (an explicit author hold, not something this skill flips on its
  own). With it, run `gh pr ready <N>` once step 1's hold check clears,
  then continue.

## Protocol

Stop at the first step that doesn't clear — never fall through to the merge
step on anything but a clean pass.

1. **Precondition.** Confirm the PR is open and read its draft state and
   labels: `gh pr view <N> --json state,isDraft,labels,headRefOid,body`. If
   it's a draft and `--ready` was not passed, stop and report "draft PR — pass
   `--ready` to proceed."

   Then check holds. The linked issues are the ones a GitHub closing keyword
   in the PR body names (`Closes` / `Fixes` / `Resolves #M`, any tense or
   case; none → only the PR's own labels count); read each one's labels with
   `gh issue view <M> --json labels`. If the PR or a linked issue carries any
   label in the profile's `hold_labels` (`.claude/implement-queue.md`
   frontmatter), stop here and report `held — <label>`: nothing is written to
   the PR, no review is dispatched, and nothing is merged.

   Only once holds clear, and only if `--ready` was passed, run
   `gh pr ready <N>`.

2. **Fast-path decision.**

   ```bash
   node scripts/fast-path-decision.mjs check --pr <N>
   ```

   One JSON line: `{fastPath, reviewers, holdForHuman, reason}`. It folds in
   the agent-core build-freshness check (rebuilding the dist if needed) and
   fails closed — no fast path, every specialist — when the dist cannot be
   trusted; see `.claude/implement-queue.md` § fast-path for the precedence.
   Exit 0 is any decision; exit 1 means `gh` could not fetch the PR, so
   stop and report it. Keep the JSON for step 4. Step 3's
   `scripts/ci-gate-status.mjs` is independent of it.

3. **CI-gate classification.** Follow `.claude/implement-queue.md` §
   ci-status verbatim, including its `gate-missing` dispatch-and-re-poll
   recovery and its explicit abstain on `gate-unattributed`/`unknown`:

   ```bash
   gh pr checks <N> --watch
   node scripts/ci-gate-status.mjs check --pr <N>
   ```

   Only `state: "green"` proceeds to step 4. Every other state stops here,
   named, per that section's table — do not re-derive the handling for
   `failed`/`pending`/`gate-missing`/`gate-unattributed`/`unknown` here.

4. **Review.** Follow `.claude/implement-queue.md` § fast-path and §
   reviewers as written: whether review can be skipped is step 2's
   `fastPath`, not re-decided here. Dispatch the diff-matched specialists
   step 2's `reviewers` names, plus the universal `reviewer` subagent
   unless `fastPath` is true. A gate-path PR (`holdForHuman`) is still
   reviewed; step 5 holds it.

   § reviewers assumes a queue worker. For a single PR, take its inputs
   from here instead:

   - **Acceptance criteria** — from the PR body plus the issues step 1
     found. Only when both lack them, pass `acceptanceCriteria: []` and say
     so in the `ReviewInput`'s `taskDescription`.
   - **Code on disk** — there is no `.claude/worktrees/agent-<taskId>/`.
     Create a throwaway worktree of the PR head
     (`git fetch origin pull/<N>/head` then
     `git worktree add --detach <scratch-path> <headRefOid>`), give the
     reviewers that path in place of the worker's, and remove it
     (`git worktree remove --force <scratch-path>`) once they return.
   - **Verdict handling** — a `flag` (reviewer) or `block` (specialist)
     verdict stops this invocation: report it with the reviewer's output.
     There is no retry and no worker dispatch (the section's retry policy
     re-dispatches a worker, which `/ship-pr` does not have). Do not
     proceed to step 5.

5. **Merge.** On an all-pass verdict (or a fast-path skip), first re-read
   holds, since a label can land while review runs:
   `gh pr view <N> --json labels` (plus the linked issues', as in step 1).
   Two things hold the PR for a human merge, and either one means the merge
   command below is not run:

   - a label in the profile's `hold_labels` on the PR or a linked issue — report
     `held — <label>`;
   - step 2's `holdForHuman: true` (a changed file matches a gate path)
     — report `held for human merge — gate path`.

   Otherwise follow `.claude/implement-queue.md` § merge-command:

   ```bash
   gh pr merge <N> --auto --squash --delete-branch --match-head-commit <headRefOid>
   ```

   `<headRefOid>` is the literal SHA step 1 read, the head step 4 reviewed.
   If GitHub refuses because the head moved, stop and report
   `stopped at merge — head moved after review`; never drop the flag.

   Issue it as the whole Bash call, nothing else on the line: `Bash(gh pr *)` in
   `.claude/settings.json` approves the plain form before the auto-mode
   classifier runs; a compound form is classified and can be denied.

   If GitHub reports the PR `CLEAN` and refuses `--auto`, merge directly
   with the same command minus `--auto` — this path, too, runs only after
   the hold re-read above cleared. If the plain merge call is still denied with
   `[Merge Without Review]` (Claude Code Remote sessions, gotchas § CCR
   #6125), do not retry through this or any other tool — report the PR as
   reviewed, green, and awaiting a human merge.

## Output

One summary screen at the end of the run (success or stop):

```
PR #<N>
  CI:       <classifyCiGateStatus state>
  Reviewers: <specialist list + verdicts, or "fast path — skipped">
  Universal: <reviewer verdict, or "fast path — skipped">
  Action:   <armed --auto | merged directly | held — <label> | held for human merge — gate path | stopped at <step> — <reason>>
```

## Scope

This skill adds no new gate logic, scripts, or classifiers — every rule it
points at already exists and is already exercised by
`/idea-to-prod:implement-queue`'s per-PR loop. It exists only to make that
same boundary callable against one PR number on demand, outside the queue.
