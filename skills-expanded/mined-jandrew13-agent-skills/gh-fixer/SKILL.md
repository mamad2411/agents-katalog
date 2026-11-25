---
name: gh-fixer
description: Address every unresolved review thread on exactly one GitHub pull request, one thread at a time, and hand the PR back for another review pass. Use when a PR in the dev-workflow pipeline sits at board Status Reviewed with open threads from gh-review's findings and/or Codex's automated review. Makes the smallest coherent change per thread, replies in-thread describing the fix (or files a tracked follow-up issue when a finding is deliberately deferred), resolves the thread, pushes, and moves the board Status back to Awaiting Review. Never reviews (gh-review) and never merges (gh-merge).
---

# GH Fixer

**Session shape:** spawned subagent, one per PR fix cycle, in its own worktree off
the PR branch — never the operator's main worktree.
**Conventions scope:** read only §§3, 5, 8, 9, 10 of
the pipeline CONVENTIONS.md — resolve it at `gh-workflow/CONVENTIONS.md`
alongside this installed skill set, else `agents/gh-workflow/CONVENTIONS.md` in
the skill source repo (github.com/JAndrew13/agent-skills); it is NOT in the
target repo. `grep -n "^## "` it for section offsets and read just those
ranges; open any other section only at the moment a step cites it.

## Overview

Fix **exactly one PR's** unresolved review threads per invocation — the
pipeline's standalone fixer stage: `(Reviewed) → gh-fixer → (Awaiting Review)`.

A PR reaches you at board Status **`Reviewed`**: `gh-review` (or a
`gh-validate` kick-back) found something and left findings on the PR. Your job
is to work **every** outstanding finding — across **both** channels findings
arrive on (inline diff **review threads** *and* top-level **COMMENT-review /
issue-comment bodies** tagged `[change-requested]`/`[minor]` under the 422
workaround), from `gh-review` and, **when it has posted one**, Codex's automated
review (de-gated but addressed-if-present, CONVENTIONS.md §8) — to a
coherent close: fix each with the smallest change that resolves it, reply
describing the fix, and dispose it (resolve the thread, or note the
COMMENT-review finding — the latter has no resolvable state), then push. When
every finding in both channels is addressed, hand the PR back to `gh-review`
by setting Status to `Awaiting Review`.

**Content source (extraction, not new logic):** this skill extracts **step 6
("Address review comments") of `agents/gh-resolve/SKILL.md`**, named here so
**DW-10** (the gh-resolve refactor into the pure Worker) can delete that
inlined prose from gh-resolve in the same phase — the logic lives here once.

**Taxonomy, statuses, the state machine, the review gate, and the
testing-cadence policy are owned by
[`agents/gh-workflow/CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md).** This
skill **references** those sections and **never restates** their tables.
Re-inlining any of them here is the duplication debt that file exists to
prevent.

## Scope (single-purpose)

- Input: one PR (number or URL) whose board Status is `Reviewed`.
- If asked to fix several PRs, run this skill once per PR — do not batch.
- **Boundary:** gh-fixer fixes and replies. It does **not** review
  (`gh-review`'s job — the adversarial passes and the findings-vs-clean
  verdict) and does **not** merge (`gh-merge`'s job, the only merger). If a
  finding's disposition is unclear, dispose it as a fix or a tracked deferral
  (below) — do not re-litigate whether the finding was valid; that judgment
  already happened in `gh-review`.

## Workflow

### 1. Get the change and enumerate outstanding findings — BOTH channels

- Work in the PR's **own worktree** — never the operator's main worktree, and
  never another session's worktree. If one does not already exist for this
  PR/issue, create it off the PR's branch before editing.
- Read the PR: `gh pr view <n>` and `gh pr diff <n>` for the current diff, and
  the linked issue's acceptance criteria + `## Refinement` block for context.
- **Enumerate every outstanding finding across BOTH channels** — findings
  arrive two structurally different ways, and a fixer that walks only one
  silently hands the PR back with the other's required changes unaddressed:
  - **(A) Diff review threads** — inline `PullRequestReviewThread`s anchored to
    a `file:line`, from `gh-review`'s inline comments and, **when Codex has
    posted a review, every comment from it** (`chatgpt-codex-connector`). These
    carry an `isResolved` flag and are the *only* channel `resolveReviewThread`
    can close. Query their state via the GitHub tools or
    `gh api graphql` (`reviewThreads { nodes { isResolved } }`); a comment
    existing is not evidence its thread is still open — check `isResolved`.
  - **(B) Top-level COMMENT-review bodies + PR issue-comments** — under the 422
    self-review workaround (CONVENTIONS.md §8), own-account findings are posted
    as **COMMENT-type review bodies** (and sometimes plain PR issue-comments)
    tagged `[change-requested]` / `[minor]`, **not** as diff threads. They have
    **no `isResolved` flag and cannot be closed with `resolveReviewThread`** —
    a fixer following only the channel-(A) `reviewThreads.isResolved` path would
    **miss every `[change-requested]` finding posted this way.** Enumerate them
    separately: list the PR's COMMENT-type reviews (`gh pr view <n> --json
    reviews` / `gh api .../pulls/<n>/reviews`) and its issue-comments
    (`.../issues/<n>/comments`), and extract each `[change-requested]` (a
    required change) and `[minor]` (a nit) tag.
- You must cover **both** (A) and (B) before handing back (step 5). Track the
  two lists explicitly so neither is dropped.
- Resolve the PR's board item id up front so the status transition in step 5 is a
  single command, following the **board-economy contract** (CONVENTIONS.md §3):
  **use the board item-id the dispatcher injected** — a lead/sweeper that already
  resolved the board map passes it down — and do **not** call `item-list`. **Only if
  no item-id was injected** (a standalone/human invocation) fall back to resolving it
  yourself by matching `items[].content.number == <issue#>` from `gh project
  item-list <board-number> --owner <board-owner> --limit 300 --format json`
  (ids from PROFILE.md; mechanics in CONVENTIONS.md §3).

### 2. Work findings one at a time — never batch

Address each outstanding finding from **either channel** (A or B)
**individually**, in its own coherent step:

- **Smallest coherent change per finding.** Make the minimal code/test/doc
  change that resolves *that* finding — do not fold in unrelated fixes,
  drive-by refactors, or other findings' changes into the same edit. Never
  batch unrelated fixes into one opaque commit; a reviewer (or a later
  `gh-fixer` pass) must be able to see which commit answered which finding.
- **Validate before replying.** Run the relevant targeted test/script for the
  change (CONVENTIONS.md §9 — targeted during development, never a full
  `pytest -q` here; that is `gh-merge`'s job at the merge-to-`main` boundary).
- Commit with a message that ties back to the finding, so the history reads as
  "finding → fix," not "batch of changes."

### 3. Reply, then dispose — resolve threads; note COMMENT-review findings

For each finding, once its fix (or deferral — step 4) is in, **reply and then
dispose it by the mechanic its channel supports**:

- **Reply describing the change** and how it was validated (or, for a deferral,
  the tracked follow-up — step 4). A reply that only says "done" without naming
  the file/change/test is not enough — the next reader (human or `gh-review`'s
  next pass) must be able to verify the claim without re-deriving it.
- **Channel (A) — diff review threads:** reply **on the thread**, then **mark it
  resolved** via the GitHub tools / `gh api graphql` (`resolveReviewThread`)
  once the reply is posted. Do not resolve before replying; do not reply
  without resolving — the pair is one unit of work.
- **Channel (B) — top-level COMMENT-review bodies / issue-comments:** these are
  **not resolvable threads**, so `resolveReviewThread` does not apply.
  Disposition them instead: **reply** (a threaded reply to the review, or a PR
  issue-comment that quotes the `[change-requested]`/`[minor]` tag and its
  finding) stating the fix (or the linked deferral), and **note the
  disposition** — check the item off in a tracked checklist and, when it
  materially changed the PR, in the PR description — so a later reader can see
  every channel-(B) finding was answered even though GitHub shows no "resolved"
  state for it.
- Continue until **every** finding — both channel (A) threads and channel (B)
  COMMENT-review findings, from `gh-review` and Codex alike — is addressed.

### 4. Deferred finding → tracked follow-up (no silent scope reduction)

**First, check the tag. `[minor]` findings are never deferred — they are fixed
or dropped, here, now.** Per the 2026-07-29 D8 re-amendment (CONVENTIONS.md §10
and §8), a `[minor]` finding may **not** become a follow-up ticket under any
framing. Fix it on this branch if it is cheap, otherwise resolve the thread with
a one-line "not taking this" and move on. Do not invoke `gh-create-issue` for a
nit. If you believe a nit genuinely warrants a ticket, it was mis-tagged: say so
in the thread and ask the review stage to re-tag it `[change-requested]` — do
not file it yourself.

The rest of this step applies to **`[change-requested]` findings only**.

If such a finding is **deliberately deferred rather than fixed** — genuinely
out-of-scope for this PR, or a larger change than the ticket's blast radius
allows — you may not simply resolve-and-ignore it:

- **File a tracked follow-up issue** for it via the `gh-create-issue` skill
  (per the operator's D8 amendment, CONVENTIONS.md §10: deferred *work* is a
  ticket, so effort is tracked — no untracked TODOs).
- **State the deferral loudly**, both in the reply (link the new issue) and, if
  material to the PR as a whole, in the PR description. Silent scope reduction —
  disposing a finding without a fix or a linked follow-up — is exactly what this
  rule exists to prevent.
- Only then dispose the finding — **resolve** the thread (channel A) or **note**
  the COMMENT-review disposition (channel B) per step 3 — with the reply linking
  the follow-up ticket.

### 5. Push, then set the board Status back to `Awaiting Review`

- Only once **every finding from BOTH channels** in step 1's enumeration is
  disposed — channel (A) threads fixed-and-resolved (or
  deferred-and-tracked-and-resolved), **and** channel (B) COMMENT-review
  findings fixed-and-noted (or deferred-and-tracked-and-noted) — **push** the
  branch.
- Move the board Status via `gh project item-edit` (never a label — mechanics
  and IDs in CONVENTIONS.md §3; ownership in §5): set **`Awaiting Review`** so
  `gh-review` re-reviews the updated PR.
- **Do not set `Awaiting Review` while any finding remains open in either
  channel** — an unresolved channel-(A) thread *or* an unanswered channel-(B)
  `[change-requested]` COMMENT-review finding (`gh-review`'s or Codex's). Zero
  unresolved review threads is necessary but **not sufficient**: a
  `[change-requested]` body that carries no `isResolved` state must still be
  addressed and noted. A remaining finding in either channel means the loop is
  not done; keep working it (step 2) rather than handing back early.

## Boundaries

- **Fixes and replies only.** Never perform the adversarial review passes,
  never post a findings verdict, and never decide `Reviewed` vs.
  `Awaiting Validation` — that is `gh-review`'s job, already done before you
  were invoked.
- **Never merges.** Only `gh-merge` merges; the review gate and full-suite
  gate are re-checked there (CONVENTIONS.md §8, §9).
- **One PR per invocation.** Re-invoke for the next PR.
- **Both channels, every time.** Cover diff review threads AND top-level
  COMMENT-review / issue-comment findings before handing back (step 1); a clean
  `reviewThreads.isResolved` sweep alone is not "all findings addressed."
- **No silent scope reduction.** Every deferred finding is a tracked issue,
  named loudly in its reply — never disposed without one.

## Tool guidance

- Use the GitHub connector tools when available for PR metadata, review
  comments, review bodies, and review-thread state (reading and resolving);
  fall back to `gh` / `gh api graphql` when thread-level resolution
  (`resolveReviewThread`) or the raw reviews/issue-comments lists are required
  and the connector is insufficient. Remember only channel-(A) diff threads are
  resolvable; channel-(B) COMMENT-review findings are disposed by reply + note.
- Use `gh project item-edit` for the board Status write; call `gh project item-list`
  **only** as the no-injected-id fallback (the §3 board-economy contract), never to
  re-fetch the full board map when the dispatcher already supplied the item-id
  (commands and IDs: CONVENTIONS.md §3).
- Use local git commands for branch, commit, and push work in the PR's own
  worktree. Run only the repo's existing targeted tests/scripts per fix —
  never invent unrelated validation, never a full-suite run here
  (CONVENTIONS.md §9).
