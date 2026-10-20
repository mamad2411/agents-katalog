---
name: grind
description: Autonomously work an issue backlog end to end — repeatedly pick the top resolvable ticket, implement each in its own isolated worktree, verify it, and land it as its own DRAFT pull request with the tracker moved to In Review, looping until the queue is dry. One ticket equals one small PR. Never merges, never deploys. The unattended "overnight worker". Use when the user says "/grind", "work the backlog", "grind the queue", "work through the tickets", or wants unattended progress on a backlog.
---

# Grind the backlog

Work through the actionable ticket queue. Take each ticket as far as a reviewable
draft pull request — implement, verify, open the PR, update the tracker — then
move on to the next resolvable ticket. Keep going until no actionable ticket
remains. This is the formalized "overnight worker": you start it, walk away, and
review a stack of drafts in the morning.

**One ticket equals one small PR.** The loop is over *how many* tickets you take
on. It is **not** license to batch. Never combine two tickets into one branch or
one pull request. Each ticket gets its own isolated worktree, its own branch, its
own draft PR, and its own tracker transition. Then you re-gather and pick the
next one.

## 0. Configure this for your project

This skill needs four things from the project. Record them in your `CLAUDE.md`,
or state them when you start the run. If they are missing and you cannot infer
them, ask once, then proceed.

| What | Example |
|---|---|
| **The ticket pool** | "Linear, label `Backend`, state Todo or In Progress, highest priority first" — or a Jira JQL query, or a GitHub Issues label filter |
| **The branch naming rule** | `feature/abc-123-short-slug`, with the ticket key in the branch so audits are automatic |
| **How to verify** | The test, typecheck, lint, and end-to-end commands, per repository |
| **Who reviews** | The reviewer to request on each PR, or "none" for a solo-owned repository |

If the project has a stacked-PR or branching skill, follow it. This skill defers
to it on branch mechanics.

## Hard invariants — never violate these, attended or not

- **Never merge. Never deploy.** Everything lands as a **draft** pull request off
  a feature branch, in every repository, including ones you normally push
  directly to. If pushing to a branch triggers a deploy anywhere in the project,
  unattended work must never trip it. The grinder parks *every* repository's
  output as a draft PR for a human to merge.
- **Work in isolation.** Make the edits on a fresh feature branch in an isolated
  checkout. Never work in the user's working tree, and never touch untracked
  files. Before any bulk delete, run `git status` first. An overnight worker once
  ran `rm -rf` on untracked scripts because it believed they were scratch files.
- **Never echo secrets.** Use placeholders only, in code, in logs, in PR bodies,
  and in tracker comments.
- **One ticket equals one PR. Never batch.** You may work many tickets in a run,
  but each gets its own branch, its own isolated worktree, and its own small
  draft PR. The loop multiplies pull requests. It does not increase the size of
  any one of them.
- **Bail cleanly, then move on.** If a ticket is underspecified, needs a decision
  only a human can make, or grows past one small PR, **skip it**. Record why (see
  §6) and pick the next resolvable ticket. Bailing on one ticket does **not** end
  the run. Only an empty pool does. A skipped ticket with a clear reason beats a
  bad pull request.
- **Verify before you build** (§1a). Never cut a branch for a ticket you have not
  confirmed against the code. A ticket already fixed by adjacent work gets an
  evidence comment and a proposed close, never a pull request. Changing working
  code to satisfy a stale ticket is worse than doing nothing.

## 1. Select the next ticket

This section runs **once per loop iteration**. Re-gather live state *fresh each
time*: fetch every repository, list open pull requests, and query the tracker.
Every PR you open removes a ticket from the pool and may unblock others, so a
stale snapshot will re-pick work you just finished.

Then **pick the top actionable issue you have not yet handled in this run**:

- It matches the project's ticket-pool filter (§0), it is **unblocked**, it has
  no open pull request already, and it is the highest priority remaining.
- Prefer work that unblocks the nearest milestone.
- Skip anything blocked, anything that is a duplicate of an existing PR's issue,
  anything you cannot finish inside one small PR, and anything you already
  handled or skipped earlier in this run.
- **If nothing qualifies, the pool is dry. Go to §6 and stop the run.**

State the pick and a one-line reason before you start.

### 1a. Confirm the ticket is still real — before you cut a branch

**A ticket body is a claim about the past, not the present.** Verify it against
the code *first*.

This is not a hypothetical risk. On one run, three of the first five Todo tickets
picked were already fixed by adjacent work. Backlog audits usually reconcile
In Progress and Done, never Todo, so tickets fixed as a side effect of other work
sit in Todo indefinitely.

Confirming costs minutes. Cutting a worktree, reading the surrounding code, and
starting an implementation before discovering the bug is gone costs far more, and
it risks opening a pull request that changes working code for no reason.

Open the file and the function the ticket names, and check that the described
behaviour is still there:

- **Never treat a commit-message grep as proof.** `git log --grep=ABC-123`
  matches the whole message, so a "Related: ABC-123" line in an unrelated commit
  reads as a hit. Grep finds candidates. Reading the code decides.
- **Does the thing the ticket guards still exist?** One ticket asked for durable
  delivery of an event that had since been removed entirely.
- **Was a decision-only ticket already decided?** One ticket asked someone to
  choose between two options, and adjacent work had already shipped one of them.
- **For a multi-part fix, check every part.** A ticket is not already done
  because one of its three branches landed. That is a real ticket with a smaller
  scope, so re-scope it and say so.

**If the ticket is already resolved, do not open a pull request.** Instead:

- Post a tracker comment with the evidence: the file, the function, and the
  behaviour you read.
- Propose **Done** if the described work exists in the code. Propose **Canceled**
  if nothing was built and the problem was designed away or superseded. Marking
  the second case Done overclaims.
- Do not change the status unattended. Recommend it and let a human confirm.
- Count it in the run summary under "closed, not implemented" (§6), and pick the
  next ticket. This is a successful outcome, not a bail.

## 2. Isolate

- Identify the target repository and package.
- Run `git fetch`, then cut a feature branch from the correct base. **The branch
  name must carry the ticket key** (§0). The key in the branch name is what makes
  later audits automatic.
- Use an isolated worktree, so the user's checkout and any running dev servers
  are untouched.

## 3. Implement

- Follow the existing patterns in the target repository. Match its conventions.
- **No ticket IDs in the code.** Do not write `ABC-123` into comments, `TODO`
  markers, docstrings, or test names. Tickets are ephemeral and the ID goes
  stale. Write the reason instead. The ID belongs in the pull request title and
  body, and in the commit message. Leave IDs already in the tree alone. Remove
  them only from lines the ticket makes you edit anyway.
- **Never widen the diff for cleanup.** Drive-by refactors make a small PR
  unreviewable, which defeats the whole point of the loop.
- If a shared schema or generated client changed, run whatever propagation step
  the project defines, and do not commit generated churn unless the source
  actually changed.

## 4. Verify before you open the PR

Do not hand over unverified work.

- **Tests, typecheck, and lint first**, using the commands from §0. Where a
  repository has no typecheck in CI, or where database queries come back
  untyped, review those query shapes by hand. No compiler is doing it for you.
- **Then exercise the runtime surface.** Run the change, do not just build it.

### 4a. Click-test the UI — the wrap-up

If the change touches a **user interface**, finish by actually clicking through
the affected flow, the same way a careful human reviews a pull request before
marking it ready.

- **Only when there is UI to click.** A backend-only ticket has no UI. Skip this,
  rely on the test suite, and say so in the report.
- **The app must be running first.** Check it. If the relevant app is down, note
  that and fall back to tests, rather than reporting a false pass.
- **Drive it** with the project's Playwright MCP server or browser harness.
  Navigate to the affected page and exercise the actual flow the ticket changed,
  not just "the page loads". Confirm the fix or the feature behaves.
- **Capture a screenshot** of the working result, to attach to the pull request
  or to drop in the report.
- If you could not click-test, because there is no UI or the app was down, say so
  **explicitly** in the PR body and in the tracker. An unverified draft must
  announce itself.

## 5. Land it as a DRAFT pull request

- Commit, push the branch, and run `gh pr create --draft`.
- **Write the PR title and body in plain, simple English.** If the
  `simple-english` skill is installed, run it first and follow its template, then
  check the body with its `check.py` before you post. On an unattended run this
  is a hard requirement, not a preference. Nobody is there to ask you what you
  meant. The same applies to the tracker issue body.
- **Request the project's reviewer** (§0). Request them as a reviewer only. Do
  not ping or nudge them in a comment.
- If this pull request continues a stack, follow the project's stacked-PR rules
  for the base branch.
- Move the tracker issue to **In Review** with the PR link. Issue and PR bodies
  must be **self-contained**. Never link a document the reader may not be able to
  open.

## 6. Report each ticket, then loop

After **each** ticket, write a short handoff. This is what a human reads in the
morning.

- **Ticket** — key, title, and why you picked it.
- **Branch and draft PR link**, and confirmation that the tracker is now In
  Review.
- **What you verified** — tests and typecheck, plus the click-test (which flow,
  pass or fail, screenshot), or the reason it was skipped.
- **Risks and follow-ups** — anything you were unsure of, or deferred.
- If you **bailed**: how far you got and what blocked you. Leave the branch
  pushed as a draft, or note that nothing was committed.
- If §1a found it **already resolved**: what you read that proves it, and whether
  you proposed Done or Canceled. No branch, no pull request.

Then **return to §1 and pick the next resolvable ticket.** Re-gather state first,
so the ticket you just opened a PR for drops out of the pool. Track what you have
handled and skipped in this run, so you do not pick it again.

### Stop the run

Stop **only when the actionable pool is dry**. That means every remaining ticket
is blocked, is decision-only, already has an open pull request, or cannot fit in
one small PR. Do not stop merely because you finished a ticket.

If you are running unattended against a token or time budget, it is also fine to
stop when the budget is nearly spent. Finish the ticket in hand cleanly. Never
stop in the middle of opening a pull request.

When you stop, end with a **run summary**:

- Every ticket **shipped** — key, draft PR link, and one line on what it did.
- Every ticket **closed, not implemented** — key, what proved it was already
  done, and whether you proposed Done or Canceled.
- Every ticket **skipped or bailed** — key and the one-line reason.
- Anything left that **needs a human** — a decision, an unblock, or a review.

If a run closes more tickets than it ships, say so plainly, and treat it as a
signal about the backlog rather than a poor run. It means the Todo pool has
drifted and a backlog audit is overdue.

Do not merge, do not deploy, and never batch tickets into a shared pull request.
The loop is over the *count of tickets*, not over the one-small-PR rule.

## Running it unattended

`/grind` is on demand. To start it and walk away, launch it headless and let it
grind the queue. It works ticket after ticket until the pool is dry, leaving a
stack of independently reviewable drafts and a run summary.

```bash
cd /path/to/your/workspace
claude -p /grind
```

A headless run needs write permissions: Edit and Write, `git`, `gh pr create`,
and tracker writes. Approve those interactively, or launch with a scoped
allowlist you wrote for this purpose. Do not widen a read-only allowlist that
exists for some other automation. The hard invariants above are the real safety
net either way.

**Start small.** On the first run, cap it: "grind the top three tickets, then
stop." Read those three pull requests carefully before you trust a full
overnight run.
