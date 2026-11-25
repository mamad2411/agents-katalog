---
name: gh-resolve
description: Implement exactly one refined GitHub issue as the dev-workflow pipeline's Worker — own worktree off base, implement the ticket, run the gates, open a PR, and hand it to the review stage. Use when a ticket at board Status In Progress needs its implementation stage: create a dedicated worktree and branch, implement precisely the refined ticket (reuse over regrowth; update tests/docs/CLI/MCP), light self-check, open the PR, and move the board Status to Awaiting Review. Never self-reviews deeply (gh-review), never addresses review threads (gh-fixer), never merges (gh-merge).
---

# GH Resolve

**Session shape:** spawned subagent, one per ticket, in its own git worktree off the
base branch — never the operator's main worktree.
**Conventions scope:** read only §§1, 3, 5, 7, 9, 10 of
the pipeline CONVENTIONS.md — resolve it at `gh-workflow/CONVENTIONS.md`
alongside this installed skill set, else `agents/gh-workflow/CONVENTIONS.md` in
the skill source repo (github.com/JAndrew13/agent-skills); it is NOT in the
target repo. `grep -n "^## "` it for section offsets and read just those
ranges; open any other section only at the moment a step cites it.

## Overview

Implement **exactly one** refined GitHub issue per invocation — the pipeline's
standalone **Worker** stage: `(In Progress) → gh-resolve → (Awaiting Review)`.

The job is **build, then hand off**. You take one refined ticket, implement it in
your own isolated worktree, run the repo gates, do a **light** self-check, open a
PR, and move the board Status to `Awaiting Review`. You do **not** perform the
deep adversarial review passes — that is `gh-review`'s stage — you do **not**
address review threads (from `gh-review`, or Codex when it posts one) — that is
`gh-fixer`'s stage — and you **never merge** — only `gh-merge` merges.

This is a deliberately narrow contract: **one refined ticket in → one PR out.**
Two big sections that used to live here have moved to their single canonical homes
so the prose is not duplicated:

- The **four deep adversarial review passes** (Architecture / Bug / Test /
  Wiring-&-honesty) now live in **`agents/gh-review/SKILL.md`** — gh-resolve does
  a light self-check only, not those passes.
- The **comment-addressing / review-thread loop** now lives in
  **`agents/gh-fixer/SKILL.md`** — gh-resolve does not reply to or resolve review
  threads.

**Taxonomy, statuses, the state machine, the review gate, the human gates, and the
version-bump / testing-cadence policy are owned by
[`agents/gh-workflow/CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md).**
This skill **references** those sections and **never restates** their tables.
Re-inlining any of them here is the duplication debt that file exists to prevent.

## Scope (single-purpose)

- Input: one refined ticket (issue number or URL) whose board Status is
  `In Progress` and whose `## Refinement` block is present.
- If asked to resolve several tickets, run this skill once per ticket — do not
  batch.
- **Boundary:** gh-resolve implements and opens the PR. It does **not** run the
  deep review passes (`gh-review`), does **not** address review threads
  (`gh-fixer`), and does **not** merge (`gh-merge`). Anything it must defer becomes
  its **own tracked ticket** (D8 as amended, CONVENTIONS.md §10) — stated loudly in
  the PR body, never a silent scope reduction.

## Workflow

### 1. Confirm scope and the base branch

- Read the issue body, its acceptance criteria, the `## Refinement` block
  (Complexity / Blast Radius / blast-radius file list), linked artifacts, and the
  relevant local files before editing.
- Identify the target **base branch**: a `[CHILD]` lands on its **epic/parent**
  branch; a `[TASK]`/`[BUG]`/`[CHORE]`/standalone targets `main` (CONVENTIONS.md
  §1). If the base is genuinely unclear, ask one concise question before creating
  the worktree.
- **Honor the human gates (CONVENTIONS.md §7).** If the ticket is Large/Huge blast
  radius or carries `Unsafe!`, it must not be worked without the operator sign-off
  named there — stop and surface rather than proceeding.

### 2. Create your own isolated worktree off the base

- Work in **your own worktree**, created off the base branch **before editing** —
  **never** the operator's main worktree, and **never** another session's worktree.
  A shared tree lets a co-worker's commit swallow your edits.
- After fetching/syncing the base, add a detached worktree and a new branch on it
  (one branch per issue), e.g. `codex/<issue#>-<short-slug>` unless the user
  requests another name.
- Export **`PYTHONPATH=<worktree>/src`** for every command you run in the worktree
  (tests, scripts, `ks`). Worker/reviewer worktrees share the repo's editable
  `.venv`, which resolves to `main`'s `src` unless `PYTHONPATH` points at **this**
  worktree — otherwise your tests silently run against `main`'s code.
- Preserve unrelated local changes. Never stage or revert work outside the issue
  scope.

### 3. Implement exactly the refined ticket

- Implement **precisely** what the ticket specifies — its requirements, acceptance
  criteria, and validation notes. Make focused changes that satisfy the issue
  without broad unrelated refactors.
- **Reuse over regrowth.** Before adding exit logic, a config read, a policy gate,
  a price/fee helper, a typed payload, or a dependency port, search for the
  canonical home first (CLAUDE.md rules 1–10) and route through it. Do not regrow
  the debt the hardening epic removed.
- Co-locate the change: update **tests, docs (CONFIG_README / CONTRIBUTING /
  `--help`), CLI help, MCP tools, and setup instructions** whenever the issue
  changes behavior or workflows, in the same change (CLAUDE.md rule 10).
- **Never touch the version line.** The profile's `<version-file>` version is bumped
  once, by `gh-merge`, at the merge-to-`main` boundary (CONVENTIONS.md §9). N
  parallel workers each bumping would collide on that one line — note the deferral
  in the PR body instead.
- Anything genuinely out of scope becomes its **own tracked follow-up ticket** (via
  `gh-create-issue`), named loudly in the PR body — never a silent scope reduction
  (CONVENTIONS.md §10, D8 amended).

### 4. Run the repo gates and a light self-check

- **Run the cheap fast gates freely** (CONVENTIONS.md §9): the profile's
  `<fast-gates>` commands (PROFILE.md).
- Run **only the targeted tests** covering the files/behavior the change touches —
  **not** a full `pytest -q` (CONVENTIONS.md §9; the full-suite run is `gh-merge`'s
  at the merge-to-`main` boundary). Use the project 3.11 venv with
  `PYTHONPATH=<worktree>/src`.
- **Light self-check only — a sanity pass, not the deep adversarial passes.**
  Confirm the diff is scoped to the ticket, the acceptance criteria are plausibly
  met, the gates and targeted tests are green, and nothing unrelated was staged. The
  deep Architecture / Bug / Test / Wiring-&-honesty passes are **`gh-review`'s** on
  the opened PR — do not run them here.

### 5. Open the PR

- Commit the implementation with a clear, issue-linked message.
- Push your branch and open a PR into the agreed base branch (`main` for a
  standalone; the epic/parent branch for a `[CHILD]`).
- Write a PR body that states: the linked issue, the problem, the solution,
  validation run (gates + targeted tests), known risks, the version-bump deferral
  (workers never touch the line — CONVENTIONS.md §9), and **loudly** any deferred
  scope with its tracked follow-up ticket.

### 6. Move the board Status to `Awaiting Review`

The PR is now the review stage's input. Move the board Status **on the "KS
Pipeline" Projects v2 board** — a board field, **never** a label (D1 veto) — from
`In Progress` to **`Awaiting Review`** (mechanics and IDs in
[`agents/gh-workflow/CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md) §3;
ownership in §5):

```sh
gh project item-edit --id <PVTI_item-id> \
  --project-id <project-node-id> \
  --field-id <status-field-id> \
  --single-select-option-id <option-id:Awaiting Review>   # ids from PROFILE.md
```

Resolve `<PVTI_item-id>` following the **board-economy contract** (CONVENTIONS.md
§3): **use the board item-id the dispatcher injected** — a lead/sweeper that already
resolved the board map passes it down — and do **not** call `item-list`. **Only if
no item-id was injected** (a standalone/human invocation) fall back to resolving it
yourself by matching `items[].content.number == <issue#>` from `gh project item-list
<board-number> --owner <board-owner> --limit 300 --format json` (ids from
PROFILE.md; mechanics in CONVENTIONS.md §3). Then the
**pipeline** takes over: `gh-review` reviews the PR
(the adversarial passes + reuse-review — its own findings are the review gate) and,
if it raises findings, `gh-fixer` addresses them. gh-resolve does **not** self-review
deeply or address review threads.

### 7. Handoff (parent reconcile is gh-merge's, not gh-resolve's)

- Tell the user the PR is open and now sits at `Awaiting Review` for the pipeline's
  review stage. Summarize the PR URL, branch, commits, gates/targeted tests run,
  remaining risks, and any tracked follow-ups you filed. **Do not merge** — only
  `gh-merge` merges.
- **Note the parent when this issue is a child — do not reconcile it here.** If the
  resolved issue is a child of an epic/parent, state that fact in the PR/handoff
  (the `Parent: #N` / tracked-by reference) so the merge owner has it. But **do
  not** check off the parent's checklist, tell the lead the child is "done", or
  otherwise reconcile the epic at PR-open: the child is not reviewed, validated, or
  landed yet, and marking the parent now would make the epic look complete
  prematurely. **Epic reconciliation is deferred to `gh-merge` Step 7**, which
  checks off the child and reconciles the parent when the child PR actually **lands**
  on its epic branch (CONVENTIONS.md §5 — that transition is `gh-merge`'s, not
  gh-resolve's). gh-resolve's responsibility ends at PR-open plus setting Status
  `Awaiting Review`; it never closes the parent or the child.

## Boundaries

- **Implements and opens the PR — nothing downstream.** Never run the deep review
  passes (`gh-review`), never reply to or resolve review threads (`gh-fixer`), never
  merge (`gh-merge`), never dispatch.
- **Own worktree, always.** Create your own worktree off the base before editing;
  never the operator's or another session's tree. Always
  `PYTHONPATH=<worktree>/src`.
- **Never touch the version line.** `gh-merge` owns the bump at merge
  (CONVENTIONS.md §9).
- **One ticket per invocation.** Re-invoke for the next ticket.
- **No silent scope reduction.** Every deferred item is a tracked follow-up ticket,
  named loudly in the PR body (CONVENTIONS.md §10).

## Tool guidance

- Use the GitHub connector tools when available for issue/PR metadata and PR
  creation; fall back to `gh` when the connector is insufficient.
- Use `gh project item-edit` for the board Status write; call `gh project item-list`
  **only** as the no-injected-id fallback (the §3 board-economy contract), never to
  re-fetch the full board map when the dispatcher already supplied the item-id
  (commands and IDs: CONVENTIONS.md §3).
- Use local git commands for worktree, branch, commit, fetch/sync, and push work in
  **your own** worktree.
- Run only the repo's existing gates and targeted tests/scripts — never invent
  unrelated validation, never a full-suite run here (CONVENTIONS.md §9).

## Safety Rules

- Never overwrite, revert, or stage unrelated local changes.
- Avoid force-pushing unless the user explicitly approves and the PR workflow
  requires it.
- Treat live trading, production credentials, destructive cleanup, and overwrite
  sync as high-risk actions requiring explicit user confirmation, and honor the
  human gates (CONVENTIONS.md §7).
- Keep commits issue-scoped so the PR remains reviewable.
