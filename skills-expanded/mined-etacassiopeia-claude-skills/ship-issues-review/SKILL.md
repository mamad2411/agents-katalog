---
name: ship-issues-review
description: "Same pipeline as /ship-issues — triage -> fix-issue -> commit-push-pr -> CI to green (fix-on-fail) — but it NEVER merges on its own. Every green PR stops at a review gate: you get a review packet written for learning (what changed, where to start reading, the decisions and their alternatives, what the tests prove, what could break, questions to check your understanding), then choose approve-and-merge, request changes, ask questions, or leave it open. Serial: the next issue starts only once you have decided on the current PR. Usage: /ship-issues-review [<issue-number>...] [--all] [--label <name>] [--force-model]"
user_invocable: true
argument-hint: "[<issue-number>...] | --all | --label <name> [--force-model]"
allowed-tools:
  - Bash(gh issue view:*)
  - Bash(gh issue list:*)
  - Bash(gh pr list:*)
  - Bash(gh pr view:*)
  - Bash(gh pr diff:*)
  - Bash(gh pr checks:*)
  - Bash(git remote get-url:*)
  - Bash(git branch:*)
  - Bash(git status:*)
  - Bash(git worktree list:*)
  - Bash(git ls-remote:*)
---

## Live Context (loaded at invocation)

- **Args**: `$ARGUMENTS` (issue numbers and/or flags; empty → treat as `--all`)
- **Repo remote**: !`git remote get-url origin 2>/dev/null`
- **Current branch**: !`git branch --show-current 2>/dev/null`
- **My login**: !`gh api user --jq .login 2>/dev/null`
- **Open issues**: !`gh issue list --state open --json number,title,labels --limit 100 2>/dev/null`
- **My open PRs**: !`gh pr list --author @me --state open --json number,title,headRefName,baseRefName 2>/dev/null`

---

# Ship Issues — with a human review gate before every merge

**What this is.** `/ship-issues` with one thing changed: **you are the merge button.** Everything
up to a green PR is the same pipeline, run the same way. Then the loop stops, explains the PR to you
well enough that reviewing it teaches you something, and waits. Nothing merges until you say so,
and the next issue does not start until you have decided on this one.

**Why it exists.** `/ship-issues` is for throughput: it babysits a PR to green and merges it. This
command is for understanding: the PR is the product *and* the lesson, so the packet is written to
be read, not skimmed, and the gate is a conversation, not a rubber stamp.

## Step 0 — Load the base pipeline (mandatory, every invocation)

Read `~/.claude/skills/ship-issues/SKILL.md` **in full** before doing anything else, and follow it
— its guiding principles, model policy, Phase 0 (claim, worklist, ordering, umbrellas, dashboard),
Phase 1 steps 1a–1d, 1e·mem, 1f, 1f-cross, 1g, Phase 2, resume rules and hard caps — **except where
this file overrides it.** It is the single source of truth for the pipeline; this file is the delta.
If that file and this one disagree, this one wins for the points it names and that one wins for
everything else.

## Overrides

### O1 — Never merge without an explicit approval in this conversation

- Nothing in this run merges a PR on its own: not 1e, not a merge sweep, not an `--admin` override,
  not a "it was already approved last time" — an approval covers **one PR at one head SHA**.
- `--no-merge` and `--admin-merge` are not accepted (every PR is review-gated; there is nothing to
  merge without you). If passed, say so in one line and continue.
- **Pipelining is off** (1·coord): implementation stays serial and so does review. Record
  `pipeline: off — review-gated` in the run-log header.
- **Stacks are off** (Phase 0 step 8): a stack merges bottom-up without a pause per layer, which is
  the opposite of this command. Record `stacks: off — review-gated`.

### O2 — 1e becomes "CI to green, then the review gate"

Replace `/ship-issues` 1e with:

1. **Watch CI to a terminal state** for the PR's head — every check, not only the required ones.
   Poll in a background shell loop (never "arm a monitor and end the turn"); a watcher that only
   reports, never merges.
2. **Red → fix-on-fail exactly as `babysit-prs` would**, minus its merge step: diagnose with
   1e·mem first (known signatures are hypotheses, confirmed by evidence — a same-SHA re-run, or a
   diff proving the failing test cannot reach the change), fix on the PR's own head in its worktree,
   re-run the local gate, push, re-watch. Same 3-cycle cap, same 1e→1c escalation. A fix pushed
   here is shown to the reviewer in the packet; nothing is hidden behind "CI is green now".
3. **Green → stop at the review gate (O3).** Set `status=awaiting-review` in the run-log, with the
   head SHA the packet describes.

### O3 — The review gate

Before asking anything, **re-read the PR as it is on GitHub** (`gh pr view`, `gh pr diff`,
`gh pr checks`) — the packet describes the published artifact, never the worktree from memory.
Then write the **review packet** in the conversation, in this order, as prose and short tables:

1. **Head line** — PR number and link, title, head SHA, CI status (all checks, with any re-run and
   why), files changed / +/- lines.
2. **What was asked, what was built** — the issue's problem in two sentences; what the PR does in
   two more. If the PR does less or more than the issue asked, say so first.
3. **Where to start reading** — a reading order: 3–6 `file:line` anchors, each with one line on
   why it matters and what to look for there. The core of the change first, plumbing last, tests
   after the code they pin.
4. **Decisions and their alternatives** — each real choice the PR made, the alternative it
   rejected and why, and the `D-n` that records it (repos with a decision register). This is the
   part most worth learning; never omit a choice because it was obvious to the implementer.
5. **What the tests prove** — a table: test name → the claim it pins → how it would fail if the
   code were wrong. Mutation results if any (killed / survived). Name a claim **without** a test
   plainly.
6. **What review found and what changed because of it** — the reviewer-agent findings that were
   fixed, the ones declined and why, and any CI fix. A reviewer finding the implementer disagreed
   with is exactly what a human reviewer should look at.
7. **Risk** — what could break and where, what is deliberately out of scope, operator/upgrade
   impact (a format change, a whole-fleet upgrade, a new flag), and anything you would want a second
   pair of eyes on.
8. **Check your understanding** — 2–4 questions a careful reviewer should be able to answer after
   reading the diff, each with the anchor where the answer lives. Do not answer them in the packet.
9. **How to look yourself** — the exact commands: `gh pr diff <n>`, `gh pr view <n> --web`, and the
   worktree path to browse or run tests in (never the user's own checkout).

Then ask with **AskUserQuestion** (one question, header `Review #<n>`):

- **Approve & merge** — merge now (O4).
- **Request changes** — you describe what to change; it is applied (O5).
- **Ask questions first** — answer in conversation, then return to this gate with the same options.
- **Leave open, continue** — the PR stays open and unmerged, `status=left-open`; the next issue is
  cut from the remote base **without** it (say so, since later work cannot build on it).

Also accept a free-text answer: treat it as a question or a change request as it reads, and confirm
which before acting.

### O4 — Merging an approved PR

- Re-read the PR first. Merge only if **the head SHA is the one the packet described**, every check
  is green, and it is mergeable. If anything moved (a new push, a rebase, a red check), do not merge:
  describe what changed since the packet and return to the gate.
- Merge with `--match-head-commit <sha>` and `babysit-prs`' merge-method rule (squash a
  single-commit issue PR; preserve history for an epic/milestone branch). Never `--admin` unless the
  user says so for this PR.
- Then `/ship-issues` 1g as usual: verify the merge content on the base, fast-forward the clean
  main checkout, re-sync the graph, delete the branch, remove the worktree.
- `status=merged`, and record in the run-log that it was **merged by approval** and when.

### O5 — Requested changes

- Restate the change you understood in one line before touching anything; ask if it is ambiguous.
- Apply it **in the PR's worktree, on the session model** (this is `fix-issue`'s Fix Phase, not a
  Haiku task): edit, re-run the full local gate, re-run any mutation check whose guard the edit
  touched, push to the same branch (never force-push), re-watch CI to green.
- Re-present a **delta packet**: what changed since the last review (`git diff <old-sha>..<new-sha>`),
  why, the new head SHA and CI — not the whole packet again unless asked. Then the same gate.
- A change that contradicts a recorded decision (`D-n`) is a decision change: amend the register
  in the same PR, as the repo's design-sync rules require, and say so in the delta packet.
- Count review rounds in the run-log (`review: 2 rounds`). There is no cap — this is the user's
  time — but after the third round, offer to leave the PR open and continue.

### O6 — Run-log and report

- Statuses add `awaiting-review`, `changes-requested`, `left-open`, and `merged` carries
  `(approved <date>)`. A resumed run that finds a PR in `awaiting-review` re-reads it and goes
  straight to the gate (O3) — it never re-implements and never merges on resume.
- The Phase 2 report adds a **Review** column: rounds, and what changed on review.
- `left-open` issues are listed with their PR link under **Awaiting your merge**.
- Circuit breakers are unchanged; `left-open` counts toward neither (it is a decision, not a failure).

## Hard rules (in addition to `/ship-issues`')

- Approval is per PR, per head SHA, given in this conversation. Nothing else is approval: not a
  previous PR's approval, not green CI, not a review agent, not a comment in the issue.
- The packet describes what is on GitHub, re-read immediately before the gate — never memory.
- Never merge, rebase, force-push or close a PR the user has not decided on.
