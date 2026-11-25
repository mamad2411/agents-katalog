---
name: gh-review
description: Adversarially review exactly one GitHub pull request and report findings — advisory only. Use when a PR in the dev-workflow pipeline is at status Awaiting Review and needs its review stage: run the adversarial passes, invoke reuse-review on any /src diff, post every finding as a PR comment (never chat-only), and move the board Status to Reviewed (findings) or Awaiting Validation (this stage's own findings clean/addressed, independent of Codex). Never pushes fixes and never merges.
---

# GH Review

**Session shape:** spawned subagent, one per PR review pass; read-only git — no
worktree, no checkout.
**Conventions scope:** read only §§3, 5, 8, 9 of
the pipeline CONVENTIONS.md — resolve it at `gh-workflow/CONVENTIONS.md`
alongside this installed skill set, else `agents/gh-workflow/CONVENTIONS.md` in
the skill source repo (github.com/JAndrew13/agent-skills); it is NOT in the
target repo. `grep -n "^## "` it for section offsets and read just those
ranges; open any other section only at the moment a step cites it.
**Routine trigger (optional):** this stage may run as an event-triggered cloud
routine (PR opened / ready-for-review / commits-pushed). A routine invocation is
a standalone invocation (no injected item-id) and MUST idempotency-guard first:
if the PR's board Status is not `Awaiting Review`, or a review comment for this
exact head SHA already exists, exit without acting — trigger events can fire
redundantly, arrive late, or be capped/dropped.

## Overview

Review **exactly one PR** per invocation, as the pipeline's standalone review
stage: `(Awaiting Review) → gh-review → (Reviewed) | (Awaiting Validation)`.

The job is **adversarial and advisory**. You try to make each acceptance
criterion FALSE, report what you find as PR comments, and set the board Status on
**your own findings** — the required gate is this stage's own review, independent
of Codex (CONVENTIONS.md §8). You **do not** push fixes — that is `gh-fixer`'s job
— and you **never merge** — only `gh-merge` merges.

This skill is an extraction of two existing sources, named here so the later
refactors (DW-10/DW-11) can delete the duplicated prose from the monolith:

- **`agents/gh-lead/SKILL.md` Phase 4 ("Review mode")** — the adversarial-posture
  framing, the advisory/comments-on-PR rule, the five review lenses, and the
  Codex handling (now de-gated — addressed if present, never a required gate; §8).
- **`agents/gh-resolve/SKILL.md` step 5 (the four adversarial review passes)** —
  the Architecture / Bug / Test / Wiring-&-honesty pass definitions.

**Taxonomy, statuses, the state machine, the review gate, the 422 workaround, and
the testing-cadence policy are owned by
[`agents/gh-workflow/CONVENTIONS.md`](../../agents/gh-workflow/CONVENTIONS.md).** This skill
**references** those sections and **never restates** their tables. Re-inlining any
of them here is the duplication debt that file exists to prevent.

## Scope (single-purpose)

- Input: one PR (number or URL) whose board Status is `Awaiting Review`.
- If asked to review several PRs, run this skill once per PR — do not batch.
- Read the linked **issue** (its acceptance criteria and `## Refinement` block) and
  the PR body/diff before judging. The review measures the change against *that
  ticket's* acceptance criteria.

## Posture (non-negotiable)

Review **as an adversary, not the author.** For every acceptance criterion, try to
make it FALSE. **Default to "unmet" when unsure.** Every finding must cite
**`file:line` evidence** — a claim without a location is not a finding. Ask the
hard questions throughout: *What did we miss? Was this done well? What could we
have done better?* Verify anything the ticket "adds" has a real **production**
caller (not just its own tests), and that no acceptance criterion is satisfied by a
proxy.

## Workflow

### 1. Get the change and the intent

- Read the diff **read-only**: `gh pr diff <n>`. **Never** `gh pr checkout` /
  `git switch` / `git checkout <branch>` in a shared worktree — it corrupts local
  refs. Read changed files in full where the diff lacks context.
- Read the linked issue: its acceptance criteria, the `## Refinement` block
  (Complexity / Blast Radius / blast-radius file list), and any human-gate flags.
- Resolve the PR's board item id up front so the status transition in step 5 is a
  single command, following the **board-economy contract** (CONVENTIONS.md §3):
  **use the board item-id the dispatcher injected** — a lead/sweeper that already
  resolved the board map passes it down — and do **not** call `item-list`. **Only if
  no item-id was injected** (a standalone/human invocation) fall back to resolving it
  yourself by matching `items[].content.number == <issue#>` from `gh project
  item-list <board-number> --owner <board-owner> --limit 300 --format json`
  (ids from PROFILE.md; mechanics in CONVENTIONS.md §3).

### 2. reuse-review on any `/src` diff

If the diff touches anything under `/src`, **invoke the `reuse-review` skill** on
it (the CLAUDE.md contribution-standard check for regrown duplication, boundary
violations, and missing config/doc/test co-location). Fold its **BLOCKING** and
**CONSIDER** results into your findings with their `file:line` and named canonical
fix. A docs/skills-only diff (no `/src`) skips this step — note that you did.

### 3. The adversarial passes

Review in these lenses (the union of gh-lead Phase 4's five lenses and
gh-resolve's four passes). Each is a place to try to break the change:

- **Architecture** — structure, ownership boundaries, coupling, abstractions,
  naming, lifecycle, and whether the fix belongs in the changed layer.
- **Issue completion** — does it actually satisfy the ticket's acceptance
  criteria, **fully**? Any criterion met by a proxy (a coverage floor that excludes
  the hardened module; a size budget grandfathering the file the ticket was meant
  to shrink; a drift guard on key names but not values) is **unmet**.
- **Bugs / errors** — runtime behavior, edge cases, error handling, data-loss risk,
  concurrency, and live/simulation parity.
- **Unseen side effects / regression** — what else does this touch? Are the
  guard/parity/golden/snapshot nets green? Did anything get silently scoped down?
  Run only the **targeted** tests covering what the change touches — not a full
  `pytest -q` (CONVENTIONS.md §9; the full suite is `gh-merge`'s at the
  merge-to-`main` boundary).
- **Tests** — missing coverage, weak assertions, fixtures, CLI/MCP coverage,
  docs/help checks. Do the tests feed inputs that *could* fail
  (varied/moving/boundary/fuzzed), or only hand-picked values that make the
  assertion trivially true? For each bug fix, confirm a test exists that **FAILS
  without the fix**, and state how you verified.
- **Wiring & honesty** — confirm anything the issue "adds" (registry, validator,
  gate, typed boundary, helper) has a real **production** caller, not just tests
  (`grep` the execution path; a symbol referenced only by its own tests is unwired
  even if vulture/coverage are green). Confirm every scope reduction (allowlist,
  deselect, grandfather, partial migration) is stated **loudly** in code and has a
  tracked follow-up issue — never silently presented as done.

### 4. Codex is optional — recognize it, address it if present, never gate on it

The required review gate is **this stage's own findings** (step 3), not Codex —
CONVENTIONS.md §8, the 2026-07-15 de-gating ("full Claude"). Codex
(`chatgpt-codex-connector`) posts its automated review **asynchronously**, often
**after** this pass runs, or not at all — and that **never** holds the ticket.

- **Never wait for Codex.** A Codex review that is **pending, absent, or never
  posted must NEVER** block the `Awaiting Review → Awaiting Validation` transition.
  Do **not** leave the PR at `Awaiting Review` because Codex has not posted or its
  threads are unresolved — that is the old required-gate behavior the de-gating
  reversed. Follow **CONVENTIONS.md §8**; do not restate it here.
- **Recognize Codex so it can be addressed.** If a Codex review by the profile's
  `<codex-reviewer>` **has already posted** actionable (`[change-requested]`)
  comments, note them in your PR comment so they enter the `gh-fixer` loop like any
  other finding — recognition serves **addressing**, not gating.
- gh-review is **advisory** — it does not itself resolve Codex threads or push the
  fixes; addressing them (when present) is `gh-fixer`'s stage. gh-review decides the
  step-5 status transition **on its own findings alone**.

### 5. Post findings and set the board Status

**Every finding goes on the PR as its own INLINE, line-anchored review comment —
never chat-only, and never a single flat top-level dump.** Each finding must be its own
**resolvable review thread** anchored to the exact `file:line` it concerns (like the
`<codex-reviewer>`'s), so `gh-fixer` can reply-and-resolve it and the `isResolved` state
is the programmatic gate. Keep each comment specific, testable, and tied to one required
change. A finding with genuinely no single line (a missing-file / architectural gap) may
be top-level, but anchor it to the nearest concrete `file:line` whenever one exists —
inline is the default, not the fallback.

- **Own-account PRs — the 422 workaround makes THREADS, not flat comments
  (CONVENTIONS.md §8):** the `APPROVE`/`REQUEST_CHANGES` review *states* 422 same-account,
  but inline comments (resolvable threads) do not — wrap them in a **COMMENT**-event
  review and tag each `[change-requested]` (required) or `[minor]` (nit). Follow §8's
  recipe so each finding lands as its own `isResolved:false` thread; do not restate it.

**Close the pass with a top-level verdict summary that names the head SHA — the
terminal artifact of every pass, findings or clean.** A top-level body is only for the
overall verdict summary. State the head SHA you reviewed. Post it with the inline threads
(§8's batched `event:"COMMENT"` recipe carries body **and** `comments:[…]` in one call) or
immediately after them, and always before the board write below — it is the *last* thing
this stage emits, which is what makes it evidence that the pass **completed** rather than
merely started.

- **This is a hard obligation, not bookkeeping — `gh-merge` Step 3.1 consumes it.** That
  gate refuses to merge unless a review-stage verdict summary names the PR's *current* head
  SHA: absence of one reads to it as **never reviewed**, and it is fail-closed. A pass that
  posts only inline threads and no SHA-naming summary therefore leaves a genuinely-reviewed
  PR unmergeable — it is kicked back to `Awaiting Review` and re-reviewed to the same
  output. Emitting the summary is what closes that loop.
- **Both producer paths carry this obligation identically** — this skill (the primary
  spawned-subagent shape) and the optional cloud routine
  (`routines/gh-review.routine.md` step 4). Neither may drop it; a merge gate that
  consumed an artifact only one path emitted would livelock on the other.

Then move the board Status via `gh project item-edit` (never a label — mechanics
and IDs in CONVENTIONS.md §3; ownership in §5):

- **Findings raised → `Reviewed`.** Any unresolved `[change-requested]` thread, or any
  BLOCKING reuse-review result — **this stage's own, or an already-posted Codex
  `[change-requested]` thread** — means the PR needs the fixer loop. Set Status
  `Reviewed`; `gh-fixer` picks it up.
- **Own findings clean/addressed → `Awaiting Validation`.** When there are no
  unresolved (`isResolved:false`) `[change-requested]` threads from **this review stage**
  (adversarial passes + reuse-review), advance the PR — **independent of Codex** (CONVENTIONS.md
  §8). A pending, absent, or never-posted Codex review does **not** hold this
  transition: do **not** leave the PR at `Awaiting Review` waiting on Codex, and do
  **not** set `Reviewed` merely to park it (there is nothing for the fixer to fix).

`[minor]`-only nits do not by themselves force `Reviewed` — use judgment: if the
change is otherwise clean, they can ride as non-blocking comments while the Status
advances to `Awaiting Validation`. When in doubt, prefer `Reviewed` (the
adversarial default).

## Boundaries

- **Advisory only.** Never edit code, never push commits, never resolve another
  actor's review threads to make the gate pass. Hand every fix back via PR comments
  for `gh-fixer`.
- **Never merges.** Only `gh-merge` merges; the review gate and full-suite gate are
  re-checked there (CONVENTIONS.md §8, §9). Codex is not a merge gate (§8).
- **One PR per invocation.** Re-invoke for the next PR.
- **Read-only git.** Inspect via `gh pr diff`, `git show`, and reading files — no
  branch switches in a shared worktree.

## Tool guidance

- Use the GitHub connector tools when available for PR metadata, review comments,
  and review-thread state; fall back to `gh` when thread-level state is required and
  the connector is insufficient.
- Use `gh project item-edit` for the board Status write; call `gh project item-list`
  **only** as the no-injected-id fallback (the §3 board-economy contract), never to
  re-fetch the full board map when the dispatcher already supplied the item-id
  (commands and IDs: CONVENTIONS.md §3).
- Run only the repo's existing targeted tests/scripts for the side-effect and test
  passes — never invent unrelated validation, never a full-suite run here
  (CONVENTIONS.md §9).
