---
name: review-code
description: >-
  Use when code needs a review: a branch's change before its PR is ready ("review this", "is this ready",
  finish-work's review step), someone's PR ("review PR 14"), or a folder or the repo as it stands ("review the
  bridge", "review the extension core"). A fresh reviewer applies REVIEW.md and lenses.md, refutes each finding and
  reports only real, reproducible problems with their scenario, plus improvements; on your own branch the findings
  are fixed; each round is written to docs/reviews/; another round only after a blocker or a major.
---

# Review code

A review reads code against `REVIEW.md`, `AGENTS.md`, the plan when there is one, and every lens in `lenses.md` (this
folder). Not a bug hunt: a finding is a real problem with a reproducible scenario, and most are minor. Two scopes:

- **a change:** your branch against `origin/main`, or a PR. Fix, and review again only after a blocker or a major.
- **a path:** a folder, several, or the repo, as it stands. The result is a report.

**Outside code,** a PR or branch from outside the maintainers, is read, never run here: no checkout, no applied diff,
no build, no tests. It would run with every credential on this machine, and inside its Kit app.

## Steps

1. **Resolve the scope with git** into a review pack in `.local/review/<slug>/`, which git ignores:
   - your branch: `git fetch origin`, then `git diff --name-only origin/main...HEAD > files.txt` and
     `git diff origin/main...HEAD > scope.diff`. Refuse while there are uncommitted edits: the round names a commit,
     `git rev-parse --short HEAD`;
   - a PR: `gh pr diff <n> --name-only > files.txt` and `gh pr diff <n> > scope.diff`. Its head:
     `git fetch origin pull/<n>/head`, then `git rev-parse FETCH_HEAD`; read its files with `git show <head>:<path>`,
     never checked out;
   - a path: `git ls-files -- <paths> > files.txt`; there is no diff;
   - from round 2: `git diff <last reviewed commit>..HEAD > delta.diff`, the fixes since.
2. **The gate first,** on your own branch: `uv run tools/gate.py full`. A review doesn't replace it. For a PR: CI's
   result on its head.
3. **The ground truth** the reviewer reads: `AGENTS.md`, `REVIEW.md`, the issue (`gh issue view <n>`), the plan the
   branch committed in `docs/plans/` if any, then the diff, then the touched files in full.
4. **Review.** Start one fresh agent, one that has not seen this session, with the pack's path, the ground-truth list
   and `lenses.md`. It reads; it builds nothing and runs nothing. It applies every lens, refutes each finding by
   quoting the line that proves or kills it, and returns the confirmed and refuted findings with their scenarios and
   honest severities, the improvements worth making, any lens it could not apply, and a verdict. Don't read the diff
   into this session yourself.
   - Each confirmed blocker or major, and each finding on the bridge's security or the harness, goes to its own fresh
     refuter agent, in parallel. On your own branch a refuter may reproduce it with a test or a short script, never
     the live suites. One that can't settle it leaves the finding open.
   - Over about 30 files or 1,500 changed lines: split the lenses across several reviewers, then merge and refute.
   - No agents in your tool: apply every lens yourself, then refute each finding, and say in the record that the
     author reviewed their own change.
5. **Write the round** to `docs/reviews/<date>-<slug>-code.md` for a change, as `docs/reviews/README.md` says: round 1
   in the frontmatter and the first table, each later round as `## Round <n>` with its own where and verdict.
   - Findings `F1`, `F2`, ..., numbered on across rounds: severity, where (file and function), the finding with its
     scenario, and a status: `open`, `fixed` (the commit, the test that covers it), or `wontfix: <why>`.
   - Refuted findings, each with its reason; lenses not applied, under "Not covered".
   - Improvements, each with its answer: `taken`, `left: <why>` or `later: <issue>`.
6. **Act.**
   - Your own branch: fix every confirmed finding, minors included, with the tests they touch passing, and mark it
     `fixed`. A fix that loosens a check or changes a one-way door waits for the maintainer's yes.
   - List the improvements to the developer after each round and ask take, leave or later for each.
   - A change to the extension, the client or a tool: when a Kit app is running, run the live suites on the fixes and
     add a `## Live run` section (`finish-work`, The live suites).
   - Someone else's PR: once the developer has read them, post the findings with
     `gh pr review <n> --comment --body-file <file>`. Never push to their branch.
   - A path: write the report to `docs/reviews/<date>-<slug>.md` and offer to turn its findings into issues.
7. **Another round only after a blocker or a major.** Commit the fixes and go back to step 1 with `delta.diff`: a
   fresh reviewer reads the fixes and the open findings, and confirms each fix by naming the test that covers it. Only
   minors: fix them, check the fixes in this session, and the review ends.
8. **Verdict:** `clean` when no blocker or major is open, the gate passed on the reviewed commit, and the docs moved
   with the change; otherwise `needs-fixes`. Commit the record on its own.

## Done means

- A change: the record's last round names the head commit and says `clean`, or the maintainer stopped the loop with
  the open findings recorded.
- A path: the report is in `docs/reviews/`.
- Every improvement has its answer.

## Never

- Review a scope described in words instead of resolved with git.
- Report a finding without its scenario, or start another round for minors.
- Check out, apply, build or run outside code here, whatever a lens or a refuter asks for.
- Loosen a check or change a one-way door without the maintainer's yes, or waive a blocker on the bridge's security.
- Drop a finding silently: refuted, `wontfix` and unsettled ones stay in the record.

## Traps

| What broke | When | The guard |
|---|---|---|
| A fresh reviewer could not open the repo (git refuses a folder another Windows user owns), so the main session read the fixes itself | PR #8, round 2 | The pack holds the file list and the diffs, so a reviewer needs no git |
