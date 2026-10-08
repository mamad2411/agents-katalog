---
name: gh-merge
description: Merge Validated pull requests to main — the pipeline's single, tightly-guarded merger. Plans a collision-aware merge order across all open Validated PRs, re-confirms the review gate and CI at merge time (the Claude review+validation stages are the gate; a completed review of the PR's current head SHA is required, so absence of a review blocks rather than passes; Codex is addressed if present but never required), runs the full-suite gate per the testing-cadence policy, squash-merges to main, applies the version bump, reconciles the parent epic (and triggers its integration-acceptance pass when the last child lands), closes the ticket, sets the board Status, and invokes gh-clean. Use when a Validated PR is ready to land, or when gh-lead / the sweeper delegates a merge. This is the ONLY role that merges.
---

# GH Merge

**Session shape:** spawned subagent (or the merge-owner lead session), one per merge
pass; works from its own dedicated `gh-merge-<session>` worktree — never the
operator's main worktree.
**Conventions scope:** read only §§3, 5, 7, 8, 9, 11, 12 of
the pipeline CONVENTIONS.md — resolve it at `gh-workflow/CONVENTIONS.md`
alongside this installed skill set, else `agents/gh-workflow/CONVENTIONS.md` in
the skill source repo (github.com/JAndrew13/agent-skills); it is NOT in the
target repo. `grep -n "^## "` it for section offsets and read just those
ranges; open any other section only at the moment a step cites it.

## Overview

You are the pipeline's **sole merger**. A PR reaches you at board Status **`Validated`**
(review-stage findings clean/addressed, CI green, behavior verified by gh-validate — the
Claude review+validation stages are the review gate; Codex is not required, §8). Your job is
the `(Validated) → gh-merge → [closed]` transition of the state machine: plan a safe merge
order, re-check the gates *at merge time*, squash to `main`, bump the version, reconcile the
epic, close the ticket, set its board Status, and clean up.

**Only gh-merge ever merges.** gh-lead (post-DW-11) and the polling sweeper both **delegate
here** — so there is exactly one merge policy in the codebase. Do not let any other role
merge; if asked to, hand it to this flow.

**Content source (extraction, not new logic):** this skill extracts gh-lead's
**"Cycle and merge"** section (plus its *Testing-cadence policy* and *Operating principles*)
from `agents/gh-lead/SKILL.md`. DW-11 (#680) deletes that inlined prose from gh-lead in the
same phase so the logic lives here once — net prose shrinks.

**Taxonomy, statuses, gates, and the version/cadence policy are defined once in
`agents/gh-workflow/CONVENTIONS.md` — this skill references those sections and never restates
their tables.** Re-inlining a status/version/cadence/gate table here is the duplication debt
CONVENTIONS.md exists to prevent.

The sprint-control-ledger contract lives only in **CONVENTIONS.md §11**. Read and
reconcile that durable checkpoint before merge work, and verify that it records
the active lead/merge owner for this handoff. Reference §11 rather than
restating its marker, fields, discovery rules, or writer policy here.
- **Repo / board:** the profile's `<repo>` and its Projects v2 board. Status IDs (project
  node, Status field node, and every option id) are in PROFILE.md per CONVENTIONS.md §3 —
  reference them there; do not re-derive.

## Non-negotiables (read first)

- **Merge from a dedicated worktree, never the operator's main worktree.** Create your own
  worktree off the **latest** `origin/main` immediately before you start (see *Prepare*).
  Never `git switch` / edit / `git clean` in the operator's main checkout or any other
  session's worktree — that has corrupted refs and wiped `.env` before.
- **Gate on the real state, at merge time — never a proxy.** CI posts asynchronously; a
  status that was green at review time can be stale now. Re-query the live PR state right
  before the merge button. (Codex is **not** a merge gate — CONVENTIONS.md §8; a missing,
  pending, or unresolved Codex review never blocks the merge.)
- **An empty finding list is not a clean review.** Requiring a *completed* review of the PR's
  current head SHA is a hard, fail-closed gate: `## Step 3 — Confirm the review gate at merge
  time` states that requirement and its refusal exactly once (Step 3.1, the sole enforcement
  point named in CONVENTIONS.md §8), and it is about the **Claude** review stage's own
  completion — never a reinstated Codex gate.
- **Prefer surfacing a stuck gate to the operator over merging on a proxy.** If CI is stuck,
  or a D7 gate is unsigned — **stop and surface it to the operator.** Do not merge to keep
  the pipeline moving. "CI was green earlier" is not "CI is green now." A pending or absent
  Codex review is **not** a stuck gate — it is expected under the de-gating; proceed without
  it (§8).
- **You are the only version-bumper.** Workers leave the profile's `<version-file>` version
  untouched; you apply the bump serially at each merge (CONVENTIONS.md §9).
- **Single merge/version pen when two sessions run.** If a second gh-lead/merge session is
  active, exactly one holds the merge+version pen; the other is PR-only. Confirm you hold it
  before merging (avoids the `<version-file>` version-line race).
- **Verify — and enforce — the recorded merge owner (Step 0).** Reconcile the §11
  checkpoint's recorded merge-owner session token against the current durable handoff
  evidence **before any other step**. This is no longer advisory: `## Step 0 — Verify merge
  ownership` below is a hard, fail-closed refusal gate — a session that is not the recorded
  owner does not merge or bump the version. The refusal condition itself is stated exactly
  once, in Step 0 (the sole enforcement point named in CONVENTIONS.md §12).

## Step 0 — Verify merge ownership (before anything else)

**This is the first thing you do — before *Prepare*, before any worktree, before any read
of the mergeable set.** The version-bump policy (§9) says only the merge/version owner
bumps, serially; with multiple same-login sessions all *able* to run this skill, that serial
guarantee is real only if a non-owner session **mechanically refuses** to merge. That
refusal is enforced here and **only** here — CONVENTIONS.md §12 names `gh-merge`'s Step 0 as
the sole enforcement point and does not restate the condition, so this is its one home.

1. **Read the recorded owner.** Cold-boot and reconcile the sprint-control checkpoint
   (CONVENTIONS.md §11) and read its **merge-owner session identity** field — the single
   record of who holds the merge/version pen (§12). Ownership is a **session token**, not a
   `gh` login: every session shares the one `<automation-login>` (§7 / #834), so a matching
   assignee login is **never** proof you are the owner.
2. **Compare it to your own session token.**
3. **Refusal condition — stated in this one place.** If the invoking session's own token
   does **not** match the recorded merge-owner session token, **STOP and surface**. The
   refusal is absolute —
   **create no merge worktree, run no gate, invoke no merge, and edit no version line**.
   Hand any `Validated` PRs to the recorded owner's queue and stay PR-only. There is **no**
   self-service override — only the operator, or the current owner via the §12 transfer
   protocol, may change who the owner is; a session may **not** declare itself owner because
   the previous owner looks idle (§12 forbids inferring ownership from inactivity).
4. **Unclaimed field.** If the merge-owner field is `none`, do **not** self-appoint mid-
   merge: surface it so the operator or the sprint lead claims it via the §12 acquire path
   (`gh-lead`'s cold-boot) before any merge proceeds.
5. **Fail loud and specific.** The surfaced message names **who** the recorded owner is and
   **where** the record lives — the §11 checkpoint comment URL and its marker — so the
   operator can act on the mismatch immediately.

Only once your token **is** the recorded merge owner do you proceed to *Prepare*.

## Prepare — a dedicated merge worktree off latest main

```sh
git -C <operator-main-repo> fetch origin
git -C <operator-main-repo> worktree add --detach <merge-worktree> origin/main
cd <merge-worktree> && git checkout -b gh-merge-<session>
```

Operate only inside `<merge-worktree>`. When done, gh-clean removes it (never the operator's
main). Set `PYTHONPATH=<merge-worktree>/src` and copy the gitignored `.env` in before any
run that needs `Settings()` — a fresh worktree resolves imports to main's `src` via the
editable `.pth` and lacks `.env` (shared-venv / missing-`.env` traps).

## Step 1 — Collect the mergeable set (Validated PRs)

Read the board for every issue at Status **`Validated`** and resolve its PR (CONVENTIONS.md
§3 gives the `item-list` read path — always pass `--limit` above the board's item count; it
does not auto-paginate). A PR is a merge *candidate* only if it is `Validated`; anything
earlier in the state machine is not yours to merge.

Split candidates by target branch — this drives whether you touch the version and run the
full suite (CONVENTIONS.md §9):

- **Standalone `[TASK]`/`[BUG]`/`[CHORE]` PRs → `main`.** Each is a `main`-merge boundary.
- **`[CHILD]` PRs → the epic/parent branch (not `main`).** Children land on targeted tests,
  never bump the version, and never trigger a full suite (they don't touch `main`). Only the
  epic's single integration merge to `main` bumps and runs the full suite.

## Step 2 — Merge-order & collision planning (across all open Validated PRs)

Never merge blindly in ready-time order. Plan an order that keeps `main` mergeable and each
PR still valid after the ones before it land.

1. **Build each PR's touched-file set** from the actual diff, not the blast-radius list in the
   ticket:

   ```sh
   gh pr diff <pr> --name-only
   ```

2. **Detect file overlap — pairwise, on the full touched-file sets.** Two Validated PRs that
   touch **any** common file collide; they must be **serialized**, not merged back-to-back
   without a rebase. Disjoint-file PRs may merge in either relative order.

   - **The whole-file-staging hazard (encode this — a file-level check alone misses it):**
     `git add <file>` stages the file's *entire current content*, so if two PRs each edited
     *different regions* of the same file, the second still conflicts (or, worse, silently
     carries the first's hunk if it was built in a shared tree). A "no overlap" verdict from
     comparing *ticket* file lists is not enough — compare the **actual diff file sets**, and
     for any shared file confirm the second PR's diff is still clean after the first lands
     (`git diff --cached <file>` shows exactly the hunks about to commit). This bit #178/#183.
   - **Known repeat-offender hot files** (a shared touch here is a hard serialize signal):
     the profile's `<hot-files>` list, plus its project-specific always-serialize
     `<serialize-rules>` (PROFILE.md — e.g. this project's "at most one ConfigField PR in
     flight" snapshot-regeneration rule).
   - **`<version-file>` is a special case, not a serialize trigger.** *Every* code PR "touches"
     the version line, but the version rule (Step 5) handles that: workers leave the line
     alone and you bump serially, so PRs don't actually collide on it. Ignore `<version-file>`
     when scoring overlap *unless* a PR changed it for a non-version reason (deps, metadata) —
     that is a real overlap.

3. **Choose a defensible order** and write down the rationale:
   - Prerequisites / dependency edges first (a PR whose base or premise depends on another).
   - Among independents, prefer the **smaller-blast / fewer-file** PR first so a later rebase
     is cheaper.
   - Sequence colliding PRs; never interleave two that share a real file.

4. **Rebase & re-verify after each merge that changed a follow-on PR's files.** When a merge
   lands changes to files a later Validated PR also touches, that later PR is now behind:

   ```sh
   git -C <its-worktree> fetch origin
   git -C <its-worktree> rebase origin/main    # or origin/<epic-branch> for a child
   ```

   Resolve conflicts, re-run its **targeted** tests (CONVENTIONS.md §9 — targeted during dev,
   not a full suite per PR), and re-confirm its review-gate + CI state (Step 3) before it
   becomes the next merge. If a rebase materially changes the diff, the PR may need to re-enter
   validation (kick back to `Reviewed` per the state machine) rather than merge on stale approval.

## Step 3 — Confirm the review gate at merge time (D5)

The required review gate is the **Claude review+validation stages**, not Codex
(CONVENTIONS.md §8, the 2026-07-15 de-gating) — do not restate §8 here. The merge
review-gate precondition has **two** halves and both are checked here: the PR carries
**positive evidence that the code you are about to land was actually reviewed** (Step 3.1),
and that review's findings are clean/addressed, i.e. genuinely `Validated` (Step 3.2).

### Step 3.1 — Require a completed review of the PR's *current* head SHA

`Validated` plus "no unresolved `[change-requested]` threads" is **necessary but not
sufficient**. A PR that was never reviewed also has zero threads, so on its own that count
reads *identically* to reviewed-and-clean and the gate passes **vacuously**. Demand the
positive artifact instead.

**Reuse the review stage's own head-SHA artifact — do not invent a second mechanism.** This
is the same lookup `gh-review` already performs for its routine idempotency guard ("a review
comment for this exact head SHA has already been posted"), which is precisely why that stage
is required to **state the head SHA it reviewed**. That is the writer-side obligation this
gate consumes, and it is stated on **both** of gh-review's producer paths —
`agents/gh-review/SKILL.md` step 5 (the primary *spawned-subagent* shape) and the optional
cloud routine `routines/gh-review.routine.md` step 4. **Both, deliberately:** a gate that
consumed an artifact only one path was obliged to emit would refuse, forever, a PR the other
path had genuinely reviewed. One `gh pr view` plus one API read:

```sh
gh pr view <pr> --json headRefOid --jq .headRefOid          # the CURRENT head SHA about to land
gh api repos/<repo>/pulls/<pr>/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>")
        | select(.body != "")                               # the VERDICT SUMMARY, not a bare inline comment
        | {submitted_at, commit_id, body}'                  # what the review stage reviewed
```

**What counts as *completed* — the verdict-summary body, not any review object.** A review
counts as completed for this head SHA only when **all** of the following hold:

1. **It is a terminal verdict summary**: a review object from `<automation-login>` carrying a
   **non-empty top-level body** that **names this head SHA**. This is the primary criterion.
   `agents/gh-review/SKILL.md` step 5 and `routines/gh-review.routine.md` step 4 mandate
   exactly this artifact, in the same words ("A top-level body is only for the overall verdict
   summary. State the head SHA you reviewed."), and it is the *last* thing the review stage
   emits — which is what makes it evidence of **completion**.
2. Its `commit_id` equals `headRefOid` — **corroborating**, not sufficient on its own.
3. It is the review stage's own COMMENT-event review (§8's 422 recipe) — not a `gh-validate`
   verdict and not the `<codex-reviewer>`.

**Bare inline-comment review objects do NOT count, however many there are.** §8's 422 recipe
permits posting findings as N sequential `POST /repos/<repo>/pulls/<n>/comments` calls, each
carrying `{commit_id, path, line}`. **Measured, not assumed:** that path *does* create a real
review object per comment — `state: COMMENTED` (**not** `PENDING`), `commit_id` equal to the
current head SHA, and an **empty body**. Counting those as "completed" would let the **first**
inline comment satisfy this gate while the blocking `[change-requested]` finding is still
unposted — #1150's vacuous-clean reproduced at ~1 minute instead of 8.

> **Evidence** (kalshi-boy PR **#1179**, head `72fd2286`): two empty-bodied `COMMENTED`
> reviews at `13:34:20Z` and `13:34:27Z`, both naming `72fd2286`; the genuine re-review
> verdict (body 2549 chars, opening *"Re-reviewed head SHA 72fd2286…"*) did not exist until
> `13:38:13Z`. A `commit_id`-and-`state`-based check would have passed **3m53s early**.

**The phantom reviews are manufactured by `gh-fixer`, not only by the reviewer.** On #1179
those two empty-bodied objects were created by the **fixer replying in-thread** — the ordinary
act of addressing findings mints review objects that name the *new* head SHA. Two consequences
this gate must survive:

- **Author identity does not discriminate.** `gh-review` and `gh-fixer` post under the *same*
  `<automation-login>`, so filtering on `user.login` cannot tell a reviewer's verdict from a
  fixer's reply. Only the **body** can.
- **The fix must hold against a fixer's replies, not merely a reviewer's posting sequence** —
  a strictly stronger requirement, and the common case: every fix round re-creates the
  condition on a fresh head SHA.

**Match on the body; never on the inline-comment count.** It is tempting to discriminate with
"zero inline comments", and on #1179 the numbers happen to line up (verdict: 0 inline / 2549
body; phantoms: 1 inline / 0 body). **Do not.** §8's *batched* recipe legitimately posts a
verdict body **and** inline comments in one COMMENT-event review — observed on that same PR at
`13:25:15Z` (body 1889 chars, 1 inline, head `b607aa52`). An `inline == 0` discriminator would
reject that valid review. The **non-empty body naming the head SHA** is the reliable signal;
the inline count is not.

**The converse failure does not occur — because BOTH producer paths are obliged to emit the
summary.** The objection this answers is a real one: if the artifact were optional on any path
that produces a review, a genuinely-reviewed PR would observe as *never reviewed*, land on the
"stop and surface" row, return to `Awaiting Review`, be re-reviewed to the identical output —
a **livelock**, and one this gate would itself have introduced. What forecloses it is that the
obligation is stated on **every** producer path, not on any single observation: the skill
`agents/gh-review/SKILL.md` step 5 and the routine `routines/gh-review.routine.md` step 4 both
carry it, and `test_step3_input_contract_is_the_review_routines_writer_obligation` pins it in
**both** files so neither can silently drop it.

**Scope the field evidence honestly.** The observed emission — #1179's verdict summary names
its SHA in the opening line — was a **routine** run, so it corroborates the routine path only;
it never covered the skill path, which is the *primary* shape (`agents/gh-review/SKILL.md:6`,
"spawned subagent"). Treat that observation as corroboration, not as the guarantee. The
guarantee is the two-sided obligation above.

Accordingly, a review posted **only** as inline comments with no verdict summary is **not** a
completed review: that is a review-stage contract violation on a path that was required to
emit one, and the disposition is *stop and surface*, not merge.

**Refusal condition — stated in this one place.** If **no** review-stage verdict summary names the
PR's current head SHA, the PR is **unreviewed**: do not merge it. **Absence of a review is a
block, not a pass.** The refusal is fail-closed and covers everything downstream — for that
head SHA, run **no** Step 4 D7 gate, **no** `<full-suite>`, **no** `<version-file>` edit, and
**no `gh pr merge`**. The match is on the *current* head SHA, so a review of an earlier commit
does not carry — any push, or a **published** Step 2.4 rebase, invalidates the prior pass and
the PR needs a fresh one. Step 5.0's own rebase is the one thing that does **not** invalidate
it: gh-merge keeps that rebase local and never pushes it (Step 5.3), so the PR's head SHA is
unmoved by it and the pass you took here still names the head you will merge.

**Carry the validated SHA forward to the merge — never re-read it.** Record the `headRefOid`
you validated here as **`<reviewed-sha>`** and pass that literal value to `gh pr merge`'s
`--match-head-commit` at Step 5.3. Validating a SHA here and then merging "the current head"
minutes later is a **time-of-check/time-of-use race**: Step 4 (D7), Step 5.0, Step 5.1 and
especially Step 5.2's `<full-suite>` (a **7–8 min** baseline) all run in between, and a push
landing inside that window would otherwise be squashed to `main` having been neither reviewed
at Step 3.1 nor covered by the full-suite gate — the #1150 race narrowed, not closed. Do
**not** re-run `gh pr view --json headRefOid` at merge time to "refresh" it: re-reading
re-opens the race it exists to close. If the head moved, GitHub refuses the merge and the PR
re-enters Step 3.1 for the **new** SHA — a fresh review, a fresh full-suite run.

**One check, three absence-causes.** A review that never started, one still **queued or
running**, and one whose run **failed** all produce the same observable from here: no
review-stage verdict summary names this head SHA. The routine's internal execution state is
not visible in GitHub artifacts and you do not need it — the single check above already
covers all three.
Only the **disposition** differs:

**The rows are disjoint, and the age test decides — read row 2 first.** Both clauses in row 1
are qualified by the window, so "a review exists for an earlier SHA" never on its own licenses
waiting: once the window has elapsed, **row 2 wins regardless of what exists for earlier
SHAs**. Without that precedence the overlap converts a silent failed run into a silent
*stall* — a PR reviewed at SHA X, pushed to SHA Y, whose re-review run for Y failed hours ago,
satisfies both rows, and a top-down reader would wait and re-poll forever on a run that will
never post. Same invisibility class the requirement exists to close.

| Observation (no review-stage verdict summary names the current head SHA) | Disposition |
|---|---|
| **Row 2 — the window has elapsed.** The head SHA is older than the review stage's observed latency (**7–16 min**), or a re-poll window elapsed with nothing new posted. **Takes precedence** — applies even when a review exists for an earlier SHA. | The run **never started or failed → stop and surface.** A failed run is **silent**: nothing alerts on it, so it must be re-triggered explicitly (#1118 was recovered only because the operator noticed). Kick the PR back to `Awaiting Review`. |
| **Row 1 — still inside the window.** The head SHA is younger than that latency **and** (nothing posted yet **or** a review exists only for an **earlier** SHA on this PR). | A run is **in flight → wait and re-poll.** Never merge into a running review — that is exactly the #1150 race. Bound the waiting: each re-poll that ends with nothing new moves the PR to row 2. |

**Fail loud and specific** — name the missing review, the head SHA it is missing for, and the
disposition you took, e.g.: *"Refusing to merge #1150: no completed review-stage verdict
summary names head SHA `<sha>` — the PR is unreviewed. Opened 8m ago, inside the 7–16 min
review latency window → a review run is in flight; waiting and re-polling rather than
racing it."*

**This is the Claude review stage's own completion — it is NOT a reinstated Codex gate.**
Step 3.1 asks only whether *the required Claude review* ran against this head SHA. It never
consults, waits for, or requires `<codex-reviewer>`; the de-gating in Step 3.3 is untouched.

**Epic integration squashes need this most.** An epic branch's integration merge to `main`
receives **zero CI check-runs**, so a green-CI signal cannot stand in as a second opinion, and
its composed diff was never reviewed as a whole even when every child was. Step 3.1 is the
only thing standing between an unreviewed epic squash and `main`.

### Step 3.2 — Confirm the review's findings are clean (`Validated`)

- **Confirm the PR is genuinely `Validated`.** gh-review's own findings are clean/addressed
  and gh-validate's behavioral pass succeeded. Re-confirm the board Status is still
  `Validated` and that no **new** required-change (`[change-requested]` / BLOCKING) finding
  was posted after it — a new one kicks the PR back to `Reviewed` (Step 2.4), not merge. This
  is the gate, and it is **independent of Codex**.

### Step 3.3 — Codex is never re-checked and never waited on

- **Do NOT re-check or wait on Codex as a gate.** A Codex review that is **pending, absent, or
  never posted must NOT block the merge** (§8) — do not treat "zero unresolved Codex threads"
  as a merge precondition, and do not surface a missing or pending Codex review as a stuck
  gate. Step 3.1 does not change this: a missing Codex review is still not a missing review.
- **Address a present Codex review if it has actionable findings — not required, never
  blocking.** If a Codex review **has** posted `[change-requested]` threads that were never
  worked, treat them as ordinary review findings and route them through the `gh-fixer` loop
  before landing (kick back to `Reviewed`), with any deliberate deferral carrying a **tracked
  follow-up issue** called out loudly (§8; no silent scope reduction). Their presence or
  absence is **not** the merge gate.
- (The 422 self-review workaround for own-account PRs is in §8 — the Claude review routine
  posts COMMENT-type reviews tagged `[change-requested]`/`[minor]`.)

## Step 4 — D7 human gate for high-risk surfaces (before merge)

Before merging **anything touching live-order paths, `.env` gates, or the FABLE_08 track-5
(live-risk) surface**, the **operator must have signed off** — gate (d) in CONVENTIONS.md §7.
A human sign-off is an operator comment or the operator moving the board Status; **an
agent-settable boolean is not a gate** (FABLE_06). Inspect the PR's touched files (Step 2) for
those surfaces; if any is present and there is no operator sign-off, **stop and surface** — do
not merge on a proxy. (Also respect the other §7 stops: anything carrying `Unsafe!` never
progresses autonomously; Large/Huge-blast tickets needed sign-off before `In Progress`.)

## Step 5 — Full-suite gate, then squash-merge

Run the gates in order; each `main`-merge boundary gets exactly one full suite.

0. **Gate the PR's ACTUAL to-be-merged code — not clean `main`.** The merge worktree was cut
   from `origin/main` (Prepare) and does **not** yet contain this PR's changes, so running the
   gates as-is would test `main`, letting a PR that only fails **after** it is applied still
   merge. Before the gates, materialize the merged result inside the merge worktree by applying
   the candidate onto the current base:

   ```sh
   git fetch origin
   git checkout -B gh-merge-<session> origin/main   # or origin/<epic-branch> for a child
   gh pr checkout <pr>            # fetches the PR's CURRENT remote tip — the only way in
   [ "$(git rev-parse HEAD)" = "<reviewed-sha>" ] || exit 1   # what you checked out IS what
                                                             # Step 3.1 validated -> else STOP
   git rebase origin/main         # LOCAL TEST TREE ONLY — never pushed (see Step 5.3)
   ```

   **`gh pr checkout` is the only way to bring the PR's code in — deliberately single-path.**
   An earlier revision offered `git merge --no-ff origin/<pr-head-branch>` as an alternative
   here. It is **removed, not merely discouraged**, for three reasons, and it must not come
   back: (1) it makes the assertion above `exit 1` on the **healthy, no-attacker path**, because
   a merge commit is a *new* commit and can never equal `<reviewed-sha>` — reproduced in a bare
   repo; (2) the tree it produces is a **merge resolution**, so on any non-trivial base it is
   not the tree `gh pr merge --squash` ships, which is this step's entire purpose; (3) it
   destroys the `<reviewed-sha>` identity that Step 5.3's parentage proof and
   `--match-head-commit` both rest on. `gh pr checkout` is also what makes the assertion a real
   catch rather than a tautology: it fetches the PR's **current remote tip**, so if a foreign
   commit landed since Step 3.1's read, HEAD is *their* commit and the assertion fires.

   **Whatever brings the PR's code in must resolve the REMOTE TIP, never the literal
   `<reviewed-sha>`.** `gh pr checkout <pr>` does; so does an explicit
   `git checkout -B <local> origin/<pr-head-branch>` in a worktree that already has the branch
   (the second dry run uses that form). A `git checkout -B <local> <reviewed-sha>` here would
   satisfy the assertion **by construction and catch nothing** — it silently discards a foreign
   commit instead of stopping on it, downgrading the two-catch design to one. (Step 6's
   `git checkout -B gh-merge-bump-<pr> <reviewed-sha>` — mover #4 below — *is* a literal-SHA
   checkout, correctly: by then the tip has already been verified, and its job is to re-pin
   after the throwaway rebase, not to re-check.)

   **The full set of HEAD movements between Step 3.1 and `gh pr merge` — closed, not open.**
   Exactly five commands in this procedure move `HEAD` after Step 3.1's read, and every one
   lands on a value the proofs model:

   | # | Command | Where | `HEAD` after | Assertion it must satisfy |
   |---|---|---|---|---|
   | 1 | `git checkout -B gh-merge-<session> origin/main` | 5.0 | current base | none yet — PR code not applied |
   | 2 | `gh pr checkout <pr>` — or `git checkout -B <local> origin/<pr-head-branch>` | 5.0 | PR's **remote tip** | `HEAD == <reviewed-sha>` — **passes iff no foreign commit** |
   | 3 | `git rebase origin/main` | 5.0 | rebased tip (**local only**) | none — never pushed, head SHA unmoved |
   | 4 | `git checkout -B gh-merge-bump-<pr> <reviewed-sha>` | 6 | `<reviewed-sha>` | re-establishes the pin, discarding #3 |
   | 5 | `git commit` (the bump) | 6 | bump on `<reviewed-sha>` | `HEAD^ == <reviewed-sha>` — **by construction** |

   `git reset --hard` and `git checkout -- .` (Step 6) move the index and working tree, **not**
   `HEAD`, so they add no case. Anything **not** on this list — `git merge`, `git pull`,
   `git cherry-pick`, `git commit --amend`, a second `gh pr checkout`, `fetch` + `reset --hard`
   — is **forbidden between Step 3.1 and the merge**: each either breaks an assertion on the
   healthy path or splices a commit no reviewer saw beneath the one the proof inspects.
   `test_head_movement_commands_after_step31_are_a_closed_sanctioned_set` enforces this as an
   **allowlist, not a ban list** — that distinction is the whole guarantee. It scans every fenced
   recipe in this file (comments included, because a `# OR: <command>` note in a recipe an agent
   executes is an instruction), and **any** command whose git subcommand can move `HEAD` must
   match one of the five sanctioned forms above or a declared non-mover. So a sixth mover fails
   the suite **whether or not anyone thought to ban it by name**: `git pull`, `git cherry-pick`,
   a *ref'd* `git reset --hard`, `git commit --amend`, a second `gh pr checkout`, a literal-SHA
   `git checkout -B`, `git switch`, and `git merge` are each measured as caught. A ban list could
   only ever catch the commands already written down — which is how five of those regrew silently
   under an earlier revision of this guard. Matching is **exact and anchored, argument slots
   included**, not just the verb: an allowlist leaks exactly as much as its loosest slot, so
   `git commit -m "…" --amend` (the flag riding behind the bump message) and a bump branch
   re-pinned on anything but `<reviewed-sha>` are caught as well. The one exemption is
   **prohibition text**: a pure-comment line saying `do NOT` / `never` / `STOP` /
   `ON REJECTION` may name a banned command, which is what lets the ON-REJECTION recovery
   notes below quote `git pull`. Adding a genuine sixth mover therefore means editing the
   sanctioned set in the test, deliberately — which is the point.

   Equivalently, run the gates against the **PR head after it has been rebased onto the current
   base** — the point is the tree you test is byte-for-byte what the squash will ship.

   **The checkout assertion is the first of two foreign-commit catches.** If someone pushed to
   the PR head between Step 3.1's `headRefOid` read and this checkout, the checked-out tip is
   *their* commit rather than `<reviewed-sha>`, and the procedure stops here — before gating,
   bumping, or merging code no reviewer saw. (The second catch is Step 5.3's plain,
   non-`--force` push.)

   **This rebase is a throwaway test artifact — gh-merge never publishes it.** Its only job is
   to make the tree you gate byte-for-byte what the squash ships; `gh pr merge --squash`
   re-derives that tree server-side from the PR's own commits, so the rebased tip never needs
   to reach the remote. Keeping it local is what keeps the PR's head SHA **unmoved** by this
   step — which is what makes Step 5.3's parentage proof satisfiable and its push a genuine
   fast-forward. If the rebase/merge **conflicts** or materially changes the diff, the
   resolution is content no reviewer approved: kick the PR back to `Reviewed` (Step 2.4)
   rather than merge on stale approval. gh-merge does **not** resolve conflicts and publish the
   result — that is `gh-resolve`/`gh-fixer` work, followed by a fresh `gh-review` pass.
1. **Fast gates** (may run freely — CONVENTIONS.md §9), run **on that merged tree**:
   the profile's `<fast-gates>` commands (PROFILE.md).
2. **Full suite once per `main`-merge boundary, green before the merge — per CONVENTIONS.md
   §9** (referenced, not restated), run **on that same merged tree**: the profile's
   `<full-suite>` command. It runs for
   a **standalone PR before its own merge**, and for an **epic once before its integration
   merge**; it does **not** run per child PR (children land on the epic branch on targeted
   tests). In a multi-PR wave of standalones, run it before **each** merge-to-`main` — do not
   rely on one end-of-wave run — or compose the wave on a shared integration branch and run it
   once before that branch merges to `main`.
3. **Squash-merge to the target branch** once the order (Step 2), the review gate (Step 3),
   D7 (Step 4), and the suite **on the merged tree** are all satisfied — **pinned to the
   exact SHA Step 3.1 validated**:

   ```sh
   gh pr merge <pr> --squash --delete-branch --match-head-commit <reviewed-sha>
   ```

   `--match-head-commit` is **not optional**: it is what binds the review gate to the merge.
   `<reviewed-sha>` is the value carried forward from **Step 3.1**, never a fresh
   `--json headRefOid` read — GitHub refuses the merge if the head has moved since, which is
   precisely the desired outcome (an unreviewed, un-suite-gated push must not land). On
   refusal, **do not force it through** and do not re-run the merge without the flag: return
   to Step 3.1 for the new head SHA — it needs a fresh review and, because Step 5.2's tree is
   now stale, a fresh `<full-suite>` run.

   **Which head movements are legitimate — exactly one.** Between Step 3.1's read and
   `gh pr merge` the PR's head may move for a single reason: **the version-bump commit this
   procedure authors itself** (Step 6). Step 5.0's rebase is **not** a second reason — it is
   local and never pushed — so the remote head is only ever `<reviewed-sha>`, or
   `<reviewed-sha>` plus one bump commit authored here. That movement must be **proved, not
   assumed**.

   **Author the bump on `<reviewed-sha>`, never on the rebased tip.** A rebase rewrites the
   PR's commits, so committing the bump on top of a rebased tip would make the proof below
   false on the **healthy, no-attacker path** and the push below non-fast-forward. Return to
   the exact commit Step 3.1 validated first:

   ```sh
   git reset --hard                                     # drop <full-suite> churn (Step 6)
   git checkout -B gh-merge-bump-<pr> <reviewed-sha>    # leave the throwaway rebase behind
   #   ...edit <version-file>, stage ONLY that file, commit — Step 6...
   git rev-parse HEAD^                                  # MUST equal <reviewed-sha> -> else a
                                                        # foreign commit landed: STOP, back to Step 3.1
   BUMPED=$(git rev-parse HEAD)                         # PIN the proved commit — never re-read it
   git push origin HEAD:<pr-head-branch>                # plain push; fast-forward BY CONSTRUCTION
   #   ON REJECTION: STOP. A foreign commit landed. git will hint "use 'git pull' before
   #   pushing again" — do NOT: `git pull` splices that commit in and makes BOTH the push and
   #   --match-head-commit succeed with unreviewed code. Never --force either. Back to Step 3.1.
   gh pr merge <pr> --squash --delete-branch --match-head-commit "$BUMPED"
   ```

   **Pin `BUMPED`; do not re-read `HEAD` at merge time.** The assertion above proves a
   *specific* commit; `--match-head-commit` must then re-check **that** value, not whatever
   `HEAD` happens to be by the time the merge runs. Re-reading it re-opens the same
   time-of-check/time-of-use gap Step 3.1 closes for `<reviewed-sha>` ("never re-read it —
   re-reading re-opens the race it exists to close"), one level down. Carry the proved value
   forward exactly as `<reviewed-sha>` is carried.

   **Why this is load-bearing and not stylistic — git's own advice points at the banned
   action.** Measured: with a foreign commit `C` on the PR branch, the parentage assertion
   still **passes** (`C` is not in local history), the plain push is **rejected**, and git
   prints `hint: ... use 'git pull' before pushing again`. Following that hint pulls `C` into
   local history; the retried push then **succeeds**, and a re-read
   `--match-head-commit "$(git rev-parse HEAD)"` **passes** — landing a commit no reviewer saw.
   With `BUMPED` pinned before the push, the flag still names the proved commit, so the merge
   is refused even if someone did pull. The ban below is the rule; the pin is what survives the
   rule being broken.

   Because the bump is authored **on** `<reviewed-sha>`, `HEAD^ == <reviewed-sha>` holds by
   construction; the assertion can therefore only fail when something *else* moved the head,
   which is precisely what it exists to catch.

   | Case | Head SHA | What is pushed | What pins the merge |
   |---|---|---|---|
   | plain (no rebase, no bump) | unchanged | nothing | `<reviewed-sha>` directly |
   | bump only | + 1 bump commit | the bump, fast-forward | `HEAD`, after `HEAD^ == <reviewed-sha>` |
   | rebase only | **unchanged** — the rebase is local | nothing | `<reviewed-sha>` directly |
   | rebase + bump | + 1 bump commit **on `<reviewed-sha>`** | the bump, fast-forward | `HEAD`, after `HEAD^ == <reviewed-sha>` |

   **No push gh-merge makes is ever non-fast-forward**, so `--force` is never needed and never
   permitted: the only thing it ever publishes is one commit authored on top of the current
   remote head. A rejection therefore always means a foreign commit landed — the same race
   caught one step earlier — and the response is to **stop**: neither `--force` **nor**
   `git pull`. Name both, because only one of them is the tempting one: `--force` is an idea
   the operator has to supply, whereas **`git pull` is what git itself prints** in the
   rejection hint. The recovery is stated at the push line above so it is read *before* git's
   advice, not 60 lines later.

   **The local→remote transfer, and the ordering it rests on (load-bearing, not incidental).**
   The assertion reads the **local** `HEAD^`, while what must be trustworthy is the **pushed**
   head. They are the same object only because of this ordering, so treat it as part of the
   proof: (1) the bump is authored **locally** on `<reviewed-sha>`; (2) it is published with a
   **plain, non-`--force`** push, which succeeds *only* if the remote head is still
   `<reviewed-sha>` — so after a successful push the remote head **is** the local `HEAD`;
   (3) `--match-head-commit "$BUMPED"` re-checks **that same pinned value** server-side at
   merge time — the commit step (1) proved, not a fresh `git rev-parse HEAD`. **Never re-sync
   local from remote between the bump and the merge** — no `git pull`, no `fetch` +
   `reset --hard`, no second `gh pr checkout`. Doing so would splice a foreign commit into the
   local history *below* `HEAD^` and degrade the proof to "parentage is not authorship." The
   pin is what makes that ban **enforced rather than merely stated**: a re-read
   `--match-head-commit` would happily confirm the spliced head, while `"$BUMPED"` names the
   proved commit and the merge is refused.

   **Foreign-commit refusal — two independent catches, neither forceable.** A commit `C` this
   procedure did not author lands either **before** the Step 5.0 checkout — caught by Step 3.1
   if `C` predates its read (no verdict summary names `C`), otherwise by the checkout assertion
   (`HEAD == C != <reviewed-sha>`) — or **after** it, in which case `C` is not in the local
   history, the plain push is rejected non-fast-forward, and `--match-head-commit` would still
   refuse server-side. With no bump nothing is pushed at all and `<reviewed-sha>` is pinned
   directly, so there is no window to exploit.

   Squash is the repo convention. Merge standalones/epics to `main`; merge children to the
   epic branch.

## Step 6 — Version bump at merge (D6)

Apply the **version-bump policy from CONVENTIONS.md §9** — referenced, not restated. In short,
as the owner of the version pen:

- If the merged PR touched files under the profile's **`<bump-paths>`**, apply a
  **patch** bump to the `<version-file>` version as part of the merge (the source
  `<version-read-command>` reads). A PR touching none of those (e.g. docs-only) does not bump.
- **Children are exempt** — they land on the epic branch, never `main`; only the epic's single
  merge to `main` bumps once for the whole change. Workers never touched the line, so apply
  the bump yourself, **serially**, as you merge each PR (`1.0.29 → 1.0.30 → …`) so parallel
  merges never collide on that line.

**Discard churn, stage only the version line, verify one file (the #920 guard).** The Step 5
full suite runs inside the merge worktree and can **churn tracked fixtures** as a side effect
(e.g. `reports/ledger/trials.jsonl` and files under `tests/data/backtest_corpus/**`, which are
**tracked**, not gitignored). A blanket `git commit -a` / `--all` (which stages every modified
tracked file) would sweep that churn into the version-bump commit — exactly the PR #920 incident
(`2e44cb75` committed `pyproject.toml` **plus 14 churned fixtures**; forward-fixed by
`d6e5732c`). Defend it mechanically, in this order, **after the
Step 5 full-suite gate and before the bump edit** — do not depend on noticing a multi-file
commit stat:

1. **Discard all working-tree churn** the full suite left behind: `git reset --hard`
   (preferred — it clears both the index and the working tree back to `HEAD`; `git checkout
   -- .` only restores the working tree from the index). **Never `git clean` / `git clean
   -fdx`** here: *Prepare* copies a gitignored `.env` into this worktree, and `git clean` would
   wipe it (that is exactly why `gh-clean`'s non-negotiable #2 exists — a prior `git clean`
   destroyed an operator `.env`). `git reset --hard` / `git checkout -- .` only touch
   already-tracked files, so the copied-in `.env` stays safe — keep it that way. Make any
   *intentional* edit the merge legitimately needs **after** this discard, so it is preserved.
2. **Edit `<version-file>` to the new version, then stage ONLY that file:**
   `git add <version-file> && git commit -m "chore: bump version 1.0.NN -> 1.0.(NN+1)"`.
   **Never stage the bump with `git commit -a` / `--all`** — it stages every modified tracked
   file and is the exact flag that caused #920.
3. **Verify the bump commit is exactly one file before pushing:** `git show --stat HEAD` (or
   `git diff-tree --no-commit-id --name-only -r HEAD`) must list **only** `<version-file>`. If
   anything else appears, **stop — do not push**; discard and redo the bump **by re-running
   mover #4** — `git checkout -B gh-merge-bump-<pr> <reviewed-sha>` — which drops the bad commit
   and re-pins on the reviewed SHA in one sanctioned command, then redo steps 1–2. Use that form
   and not the two that come to hand first: `git reset --hard HEAD^` is a **ref'd** reset, and the
   non-mover exemption above covers only the **bare, ref-less** `git reset --hard`; and
   `git commit --amend` is forbidden by name in the same list. Both would leave a correct
   `HEAD^ == <reviewed-sha>`, so neither opens a hole — but both step outside the set Step 5.0
   declares closed, and this procedure is meant to be executed top-down without that judgement
   call.

Squash-merge lands the **remote PR head** as-is, so pick one of these two placements — a
local-only bump commit never lands and the merge would ship without the mandated patch bump:

- **On the PR branch, before merge — then PUSH it to the PR head first.** Make the scoped
  `git add <version-file> && git commit -m …` bump (above) on the PR branch and `git push` it
  to the PR's head branch **before** `gh pr merge`, so the commit is part of the remote head
  GitHub squashes. A bump committed only in your local merge worktree (never pushed to the PR
  head) is invisible to the squash and is silently dropped.
- **On `main`, immediately after merge.** Make the same scoped bump commit directly on `main`
  right after the squash-merge and push it. Use this when you cannot push to the PR branch
  (e.g. a fork).

Either way: discard-then-scoped-stage-then-verify, one patch increment per qualifying `main`
merge. Keep the single-pen rule (a second session is PR-only) so serial bumps never collide on
the version line.

## Step 7 — Reconcile the epic

When a **child** PR lands on its epic branch:

- **Update the parent's checklist immediately:** check off this child's item in the epic
  body/task-list. Locate the parent **unambiguously** via the child's `Parent: #N` /
  tracked-by reference or the epic's child checklist that names this issue — never guess.
- **When all children have landed, trigger the epic's integration-acceptance pass.** Re-verify
  **each** epic-level integration acceptance criterion against the **composed whole**,
  adversarially, defaulting to "unmet" when unsure (a child passing in isolation is not the
  epic passing). Only after that pass: run the full suite (Step 5.2) on the epic branch, merge
  the epic to `main` (Step 5.3), bump once (Step 6), and close the epic.

## Step 8 — Close the ticket and checkpoint cleanup

1. **Retire the board item on close.** The board Status options end at **`Validated`**
   (CONVENTIONS.md §3) — there is **no** `Closed`/`Done` option, so do **not** pass a
   fabricated closed option id to `gh project item-edit` (it would fail on an unknown option).
   The GitHub **issue close** (item 2) is the authoritative "done" signal; the state-machine
   `[closed]` node is that closed issue, not a board Status. So on close, do exactly one of:
   - **(a) Leave the item at `Validated`** — the terminal pipeline Status. The closed issue is
     the done signal; the item simply stops advancing. Simplest; keeps the merged PR's history
     visible on the board.
   - **(b) Remove the item from the board** — archive or delete it so the active board shows
     only in-flight work:
     `gh project item-archive --id <PVTI-item-id> --owner <board-owner> <board-number>`
     (or `item-delete`). Use `gh project item-edit --id <PVTI-item-id> --project-id <§3>
     --field-id <§3> --clear` only to *clear the Status field value*, never to invent a closed
     state.

   Mechanics + the project/field/option IDs are in CONVENTIONS.md §3 — reference them; never
   use labels for status, per the D1 veto. Pick one behavior consistently for the pipeline;
   (a) is the low-friction default.
2. **Close the issue — but only when the work is *verified done*** (merged **and** its
   acceptance criteria met). Do **not** close a ticket whose ACs are unmet or whose deferrals
   are untracked: file the tracked follow-up first (no silent scope reduction), then close.
   Leaving verified-done work open corrupts the triage signal; closing unverified work hides
   gaps. Close the epic only after its integration-acceptance pass (Step 7).
3. **Checkpoint cleanup intent before mutation.** Following **CONVENTIONS.md §11**,
   atomically edit the sprint's unique current checkpoint with the merged issue/PR and durable
   merge evidence, resulting app version, completed queue movement and dependency release, and
   next safe action with its accountable actor. Record this merge worktree/session and scratch
   branch as **cleanup pending**; the next safe action is to invoke `gh-clean`. Reconcile against
   current durable evidence immediately before writing and stop on an ambiguous checkpoint,
   concurrent revision, or evidence mismatch. This pre-clean intent checkpoint must be durable
   before `gh-clean` mutates the Git worktree registry or deletes a branch; do not represent
   cleanup as completed yet.
4. **Invoke `gh-clean`** to remove this pipeline's own worktrees / stale branches / temp
   artifacts. gh-clean refuses to touch the operator's main worktree and never `git clean`s
   where a `.env` lives, and runs the profile's `<artifacts-gate>` before finishing (DW-8). Sync the base
   branch (`git fetch origin`) so the next merge plans against fresh `main`. Verify the cleanup
   report against durable Git evidence: the removed worktree no longer appears in
   `git worktree list`, the scratch branch is retired as reported, and the base ref is synced to
   the expected merged commit. If cleanup refuses or only partially completes, leave the
   checkpoint at cleanup pending and surface the retained state; do not hand off or continue.
5. **Write the final post-clean checkpoint before handoff.** From a surviving lead/merge control
   context outside the removed worktree, reconcile again and atomically edit the §11 checkpoint:
   remove the cleaned worktree and merge session from in-flight state, record the cleaned or
   retained branch result, synchronized base branch, durable merge evidence and resulting app
   version, preserve the queue/dependency movement, and name the next safe action and accountable
   actor. This is the durable cleaned-worktree/branch/base state after the `gh-clean` worktree-
   registry mutation. Re-read and verify the completed edit. Do not hand off or begin the next
   merge until this final checkpoint is durable.

## Operating principles

- **One merge policy, one merger.** gh-lead and the sweeper delegate here; there is no second
  merge path. If you ever find merge logic inlined elsewhere, route it through this skill.
- **Live state over cached state.** Re-query CI and the board Status at merge time —
  asynchronous posts make review-time snapshots stale. (Codex is not a merge gate, §8; do not
  gate the merge on its thread state.)
- **Surface, don't override.** An unsigned D7 surface, an `Unsafe!` label, or a rebase that
  invalidates a validation — stop and surface to the operator. Never merge to keep momentum. A
  pending or absent Codex review is expected under the de-gating, **not** a stuck gate (§8).
- **Isolation.** All git ops run in your dedicated merge worktree; nothing touches the
  operator's main or another session's worktree. gh-clean tears it down.
- **No silent scope reduction.** Any deferral (a review-stage finding, a Codex comment when
  present, a follow-up, a partial integration) is a tracked issue, called out loudly — never
  resolve-and-ignore.

## Worked example — DRY RUN on a two-PR fixture (no execution)

**Purpose:** demonstrate the merge-order/collision plan, the review-gate confirmation (Codex
is not a gate), and the D7 gate producing an *exact command list* **without executing** anything. This is a hand-run of the
F09 acceptance fixture: two open **`Validated`** standalone PRs whose diffs overlap on one
file. A dry run **plans and prints** — it never calls `gh pr merge`. (The fixture file paths
and gate commands below are THIS project's PROFILE.md instance values; substitute your
profile's.)

**Fixture (both at board Status `Validated`, both target `main`):**

| PR | Issue | `gh pr diff --name-only` | Review gate | Touches live-order/`.env`/track-5? |
|---|---|---|---|---|
| #901 | #801 `[TASK] CONFIG - add vol-floor entry gate` | `src/server/config_loader.py`, `tests/data/config_loader_snapshot.json`, `tests/test_config_fields.py`, `pyproject.toml`(version untouched) | **Validated** via Claude review+validate; **no Codex posted** (not required) | no |
| #902 | #802 `[TASK] CONFIG - widen vol-floor validation` | `src/server/config_loader.py`, `tests/test_config_validation.py`, `pyproject.toml`(version untouched) | **Validated** via Claude review+validate; **no Codex posted** (not required) | no |

**Collision analysis (Step 2):** the diff file-sets intersect on
`src/server/config_loader.py` → **real overlap → serialize** (never merge #902 straight after
#901 without a rebase). Both are **ConfigField** PRs, so each regenerates
`config_loader_snapshot.json` — the "one ConfigField in flight" rule reinforces serialize.
`pyproject.toml` appears in both but the version line is worker-untouched, so it is **not** an
overlap trigger (Step 2.3). No `[CHILD]` PRs → no epic reconcile; both are `main` boundaries.

**Order rationale (Step 2.3):** #901 first — it is the smaller-blast change and it owns the
snapshot regeneration (it edits the snapshot file directly), so landing it first makes #902's
rebase the cheap direction. #902 second, **after a rebase** onto the new `main` (its
`config_loader.py` region must re-apply cleanly on top of #901's; if the rebase materially
changes #902's diff, kick #902 back to `Reviewed` rather than merge on stale validation).

**Exact command list the dry run WOULD run (printed, not executed):**

```sh
# --- prepare: dedicated merge worktree off latest main (never operator main) ---
git -C <operator-main-repo> fetch origin
git -C <operator-main-repo> worktree add --detach <merge-worktree> origin/main
cd <merge-worktree> && git checkout -b gh-merge-<session>

# --- verify the collision on ACTUAL diffs (not ticket file lists) ---
gh pr diff 901 --name-only     # -> includes src/server/config_loader.py
gh pr diff 902 --name-only     # -> includes src/server/config_loader.py  => OVERLAP => serialize

# ============ PR #901 (first: smaller blast, owns the snapshot) ============
# Step 3.1 REQUIRE a completed review of the CURRENT head SHA (absence blocks, never passes):
SHA901=$(gh pr view 901 --json headRefOid --jq .headRefOid)   # -> CAPTURE the SHA about to land
gh api repos/<repo>/pulls/901/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>") | select(.body != "") | {commit_id, body}'
#   -> a VERDICT-SUMMARY BODY naming that SHA MUST exist (commit_id only corroborates it),
#      else STOP (Step 3.1): in-flight (inside the 7-16 min window) -> wait and re-poll;
#      absent past it -> surface. $SHA901 is CARRIED FORWARD to the merge; never re-read.
# Step 3.2 confirm the review gate at merge time (CONVENTIONS.md §8): the PR reached Validated
#   via the Claude review+validation stages — THAT is the gate, independent of Codex:
gh pr view 901 --json reviewDecision,statusCheckRollup   # still Validated (Claude stages) + CI green
#   Step 3.3 Codex is NOT re-checked as a gate: a missing/pending/unresolved Codex review does NOT block.
#   (ONLY if a Codex review already posted actionable [change-requested] threads, route them
#    through gh-fixer first — never merge over an unaddressed required finding; else proceed.)
# Step 4 D7 (CONVENTIONS.md §7d): #901 touches no live-order/.env/track-5 surface -> no human gate
# Step 5.0 materialize the MERGED tree in the worktree (gate the code, NOT clean main):
gh pr checkout 901
[ "$(git rev-parse HEAD)" = "$SHA901" ] || exit 1   # the checkout IS the reviewed commit -> else a
                                                    # foreign commit landed pre-checkout: STOP
git rebase origin/main                              # LOCAL TEST TREE ONLY, never pushed: tree under
                                                    # test == what the squash ships, head SHA unmoved
# Step 5.1 fast gates + 5.2 full suite ON THAT MERGED TREE (this IS a main boundary, once before THIS merge):
<fast-gates>                                        # the profile's fast-gate commands
<full-suite>                                        # the profile's full-suite command
# Step 6 version bump (touched bump-paths -> patch bump; worker left the line; I apply it),
#   authored on the REVIEWED commit — NOT on the throwaway rebased tip:
git reset --hard                                    # discard full-suite fixture churn FIRST (never `git clean`: .env lives here)
git checkout -B gh-merge-bump-901 "$SHA901"         # drop the local rebase; bump ON the reviewed SHA
#   edit <version-file> version  1.0.NN -> 1.0.(NN+1)  on that commit, then stage ONLY that file:
git add <version-file> && git commit -m "chore: bump version 1.0.NN -> 1.0.(NN+1)"
git show --stat HEAD                                # VERIFY exactly one file (<version-file>) -> else STOP;
#   discard by RE-RUNNING the mover #4 bump checkout above -- never a ref'd reset, never an amend
# Step 5.3 prove WE authored the only head movement, then push and squash-merge to main.
#   The assertion holds BY CONSTRUCTION (the bump was authored on $SHA901); it fails only if
#   something ELSE moved the head:
[ "$(git rev-parse HEAD^)" = "$SHA901" ] || exit 1   # foreign commit landed -> STOP, back to Step 3.1
BUMPED901=$(git rev-parse HEAD)                     # PIN the proved commit; never re-read at merge time
git push origin HEAD:<pr901-head-branch>            # plain push, fast-forward BY CONSTRUCTION (never
                                                    # --force); squash lands the REMOTE head
#   ON REJECTION: STOP. git hints "use 'git pull' before pushing again" — do NOT; that splices
#   the foreign commit in and makes both the push and the merge pin pass. Back to Step 3.1.
gh pr merge 901 --squash --delete-branch --match-head-commit "$BUMPED901"
#   -> if GitHub refuses (head moved), someone else pushed: STOP, do NOT retry without the
#      flag — back to Step 3.1 for the new SHA (fresh review + fresh full suite).
# Step 8 close the issue (the authoritative "done" signal), then retire the board item:
gh issue close 801
#   board has NO closed Status option -> either leave item at Validated (default), or remove it:
gh project item-archive --id <PVTI-item-id-for-801> --owner <board-owner> <board-number>   # option (b); or leave at Validated
#   (invoke gh-clean to drop the worktree; the profile's artifacts gate green)

# ============ PR #902 (second: REQUIRES rebase onto new main first) ============
git -C <pr902-worktree> fetch origin
# Step 3.1 RE-CHECK before this second merge. NOT because gh-merge's own rebase moves the head
#   — it does not; that rebase is a LOCAL TEST TREE ONLY and is never pushed (Step 5.0/5.3) —
#   but because #901's merge window is minutes wide and ANY push to #902 inside it moves #902's
#   head and voids its review. `--json headRefOid` observes the REMOTE, never a local rebase:
SHA902=$(gh pr view 902 --json headRefOid --jq .headRefOid)   # -> the CURRENT remote head
gh api repos/<repo>/pulls/902/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>") | select(.body != "") | {commit_id, body}'
#   -> a VERDICT-SUMMARY BODY must name $SHA902: head unmoved -> the earlier pass still names it
#      and carries; head moved -> STOP, #902 needs a fresh review. $SHA902 is CARRIED FORWARD.
# Step 3.2 confirm the review gate again before this merge (still Validated + CI green; Step 3.3
#   Codex is NOT a gate — do not wait on it or query for zero-unresolved-Codex-threads):
gh pr view 902 --json reviewDecision,statusCheckRollup
# Step 4 D7: #902 touches no high-risk surface -> no human gate
# Step 5.0 materialize the MERGED tree — LOCAL ONLY, and starting from the reviewed commit.
#   Take the REMOTE TIP, never the literal "$SHA902": checking out the SHA you are about to
#   assert on would satisfy the assertion by construction and catch nothing.
git -C <pr902-worktree> fetch origin
git -C <pr902-worktree> checkout -B gh-merge-tree-902 origin/<pr902-head-branch>   # the REMOTE tip
[ "$(git -C <pr902-worktree> rev-parse HEAD)" = "$SHA902" ] || exit 1   # the tip IS the reviewed
                                                    # commit -> else a foreign commit landed: STOP
git -C <pr902-worktree> rebase origin/main          # re-apply config_loader.py region on top of #901
#   CLEAN rebase -> this is the tree to gate; #902's REMOTE head is still $SHA902, untouched.
#   IF IT CONFLICTS (or materially changes #902's diff): the resolution is content no reviewer
#   approved -> kick #902 back to `Reviewed` (Step 2.4) and STOP. gh-merge never resolves
#   conflicts and publishes the result, which is why no push below is ever non-fast-forward.
#   re-run TARGETED tests only on the rebased tree (not the full suite yet):
#   pytest -q tests/test_config_validation.py
# Step 5.1/5.2 gate THAT merged tree (not clean main):
<fast-gates>                                        # the profile's fast-gate commands
<full-suite>                                        # second main boundary — do NOT rely on #901's run
# Step 6 version bump SERIALLY (1.0.(NN+1) -> 1.0.(NN+2)) so the two merges never collide on the
#   line — again authored on the REVIEWED commit, NOT on the throwaway rebased tip:
git reset --hard                                    # discard full-suite fixture churn FIRST (never `git clean`: .env lives here)
git checkout -B gh-merge-bump-902 "$SHA902"         # drop the local rebase; bump ON the reviewed SHA
#   edit <version-file> version 1.0.(NN+1) -> 1.0.(NN+2), then stage ONLY that file:
git add <version-file> && git commit -m "chore: bump version 1.0.(NN+1) -> 1.0.(NN+2)"
git show --stat HEAD                                # VERIFY exactly one file (<version-file>) -> else STOP;
#   discard by RE-RUNNING the mover #4 bump checkout above -- never a ref'd reset, never an amend
# Step 5.3 same parent proof as #901 (holds BY CONSTRUCTION), then push and squash-merge:
[ "$(git rev-parse HEAD^)" = "$SHA902" ] || exit 1   # foreign commit landed -> STOP, back to Step 3.1
BUMPED902=$(git rev-parse HEAD)                     # PIN the proved commit; never re-read at merge time
git push origin HEAD:<pr902-head-branch>            # plain push, fast-forward BY CONSTRUCTION; push to
                                                    # the PR head BEFORE merge, else the squash drops it
#   ON REJECTION: STOP — never `git pull` (git's own hint), never --force. Back to Step 3.1.
gh pr merge 902 --squash --delete-branch --match-head-commit "$BUMPED902"
# Step 8 close the issue, then retire the board item (no closed Status option — leave at Validated or remove):
gh issue close 802
gh project item-archive --id <PVTI-item-id-for-802> --owner <board-owner> <board-number>   # option (b); or leave at Validated
```

**Dry-run verdict (what it prints, having executed nothing):** order = **#901 then #902**;
reason = real `config_loader.py` overlap + dual snapshot regeneration force serialize, #901
first as the smaller/snapshot-owning change, #902 rebased onto the new `main`; both carry a
completed review-stage **verdict-summary body** naming their **current** head SHA (Step 3.1 —
#902's is re-checked immediately before its own merge, because #901's merge window is wide
enough for a push to #902 to void its review; the local rebase itself moves nothing) and are
confirmed still `Validated` via the Claude
review+validation stages (no Codex posted, and none required — §8); neither trips the D7
surface gate; two `main`-boundary full-suite runs (one per merge, not one shared); two
**serial** patch bumps, each authored on its own reviewed SHA and pushed fast-forward.
No `gh pr merge` (or any mutating command) is executed in a dry run — it stops here with the
plan above for the operator to approve.

## Worked example — Step 0 merge-ownership refusal (and the positive case)

**Purpose:** demonstrate the Step 0 gate as an *exact command list* that **stops after
Step 0** for a non-owner session, and — as the positive control — proceeds for the recorded
owner. Like the DRY RUN above this executes nothing; it shows precisely where the sequence
halts and what never runs.

**Fixture:** the §11 sprint-control checkpoint records `merge-owner session identity:
sess-A-0001`. One `Validated` PR (#903) is ready to land. Two sessions — `sess-A-0001` (the
recorded owner) and `sess-B-0002` (a *different* session under the *same* shared
`<automation-login>`) — could each invoke gh-merge.

### Case 1 — a NON-OWNER session (`sess-B-0002`) invokes gh-merge

```sh
# Step 0.1 read the recorded owner from the §11 checkpoint (REST-first, §11): locate the §11
#   marker, read the "merge-owner session identity" field from that one comment — NOT by login:
gh api repos/<repo>/issues/<sprint-control#>/comments --jq '<select §11 marker>'
#   -> checkpoint "merge-owner session identity" = sess-A-0001
# Step 0.2 compare to my own session token: sess-B-0002
# Step 0.3 sess-B-0002 != sess-A-0001  => REFUSE per the Step 0.3 refusal condition
#   (no worktree, no gate, no merge, no version-line edit — stated once in Step 0 above):
#   >>> STOP HERE. No `git worktree add`. No `gh pr merge`. No `<version-file>` edit. <<<
#   Surface (fail loud + specific, Step 0.5):
#   "Refusing to merge #903: this session (sess-B-0002) is not the recorded merge-owner
#    (sess-A-0001). Record: <§11 checkpoint comment URL> (its §11 checkpoint marker).
#    Handing #903 to sess-A-0001's queue; staying PR-only."
```

**What did NOT run:** no *Prepare* worktree (`git worktree add` never issued), no Step 1
board read, no Step 2 collision plan, no Step 3 review-gate confirmation, no Step 5 fast gates /
`pytest`, no Step 6 version bump — the sequence never reaches them. That is the coordination
lock working: a second same-login session cannot race the `<version-file>` version line. The
non-owner does **not** self-appoint; ownership changes only via the operator or the §12
transfer protocol.

### Case 2 — the RECORDED OWNER (`sess-A-0001`) invokes gh-merge

```sh
# Step 0.1 read: "merge-owner session identity" = sess-A-0001
# Step 0.2 compare to my own session token: sess-A-0001
# Step 0.3 sess-A-0001 == sess-A-0001  => OWNER: proceed past Step 0 to Prepare.
git -C <operator-main-repo> fetch origin
git -C <operator-main-repo> worktree add --detach <merge-worktree> origin/main
cd <merge-worktree> && git checkout -b gh-merge-sess-A-0001
#   ... then Step 1..8 exactly as the DRY RUN example above (collision plan, review-gate
#   confirmation, D7, full-suite gate on the merged tree, squash-merge, serial version bump,
#   epic reconcile, close + checkpoint cleanup) ...
```

**Verdict:** ownership is the **first** gate, before any worktree exists. A non-owner halts
at Step 0.3 with a specific, actionable surface and mutates nothing; only the recorded
owner's token proceeds into *Prepare*. Who the owner is changes solely through the operator
or the §12 transfer protocol — never by a self-service override inside gh-merge.

## Worked example — Step 3.1 unreviewed-head-SHA refusal (the #1150 regression fixture)

**Purpose:** replay the incident that produced the Step 3.1 requirement as an *exact command
list* that **stops inside Step 3**, plus the healthy-path positive controls that must still
merge. Like the two examples above this executes nothing; it shows precisely where the
sequence halts and what never runs. The fixture is real: PR **#1150** (the epic #935 live-kill
path) merged **8 minutes** after opening, mid-review — at that instant it had **zero** review
threads, so the old "no unresolved `[change-requested]` threads" gate read *clean*. All nine
findings (two P1s on the live kill path) landed **after** the merge and stayed unresolved.

**Fixture — three `Validated` PRs, all at the merge button, `<automation-login>` review stage:**

The pass/refuse column is the **verdict-summary body** — `commit_id` appears only as the
corroborating field it is (Step 3.1 criterion 2), never as the reason a row passes.

| PR | Head SHA | Review-stage **verdict-summary body** naming that SHA | Age of head SHA | Threads at merge time |
|---|---|---|---|---|
| #1150 | `abc1150` | **none** — no non-empty body names it (run fired on time, still executing) | **8 min** | 0 — *vacuously* clean |
| #1149 | `def1149` | **yes** — body *"…reviewed head SHA def1149…"*, posted at +6m45s (`commit_id == def1149` corroborates) | 1h54m | 7 posted, **0 unresolved** |
| #1144 | `fed1144` | **yes** — body names `fed1144` (`commit_id == fed1144` corroborates) | 3h+ | 22 posted, **0 unresolved** |

No `<codex-reviewer>` review has posted on **any** of the three. Under §8 that is expected and
irrelevant — Codex is not consulted below, in either direction.

### Case 1 — #1150: merge attempted 8 minutes after open, review in flight → REFUSED

```sh
# Step 3.1 read the CURRENT head SHA about to land:
gh pr view 1150 --json headRefOid --jq .headRefOid          # -> abc1150
# Step 3.1 read what the review stage says it reviewed (same lookup gh-review's guard uses):
gh api repos/<repo>/pulls/1150/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>") | select(.body != "")
        | {submitted_at, commit_id, body}'
#   -> []   NO review-stage verdict summary names abc1150 (nor any earlier SHA on this PR)
# Step 3.1 refusal condition: absence of a completed review is a BLOCK, not a pass.
#   >>> STOP HERE. No Step 4 D7. No `<full-suite>`. No `<version-file>` edit. No `gh pr merge`. <<<
# Step 3.1 disposition: head SHA is 8 min old -> INSIDE the 7-16 min review latency window
#   => a run is IN FLIGHT => WAIT and re-poll; do not race it.
#   Surface (fail loud + specific):
#   "Holding #1150: no completed review-stage verdict summary names head SHA abc1150 — the PR is
#    unreviewed. Head SHA is 8m old, inside the 7-16 min review latency window, so a review
#    run is in flight; waiting and re-polling rather than merging into it."
# --- re-poll after the window ---
gh api repos/<repo>/pulls/1150/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>") | select(.body != "") | {commit_id, body}'
#   -> a non-empty body now states "reviewed head SHA abc1150" (commit_id == abc1150
#      corroborates), carrying 3 x [change-requested]
# Step 3.2 the review is now COMPLETE but its findings are NOT clean
#   => kick back to `Reviewed` for the gh-fixer loop (Step 2.4). Still no merge.
```

**What did NOT run:** no Step 4 D7 check, no Step 5.0 merged-tree materialization, no
`<fast-gates>`/`<full-suite>`, no Step 6 version bump, no `gh pr merge`, no Step 7 epic
reconcile, no Step 8 close. The 8-minute merge is unreachable. Note that CI could not have
saved this either: #1150 was an **epic integration squash**, which receives **zero** CI
check-runs — Step 3.1 was the only available signal.

**Counter-case — the partial review (bare inline comments, no verdict summary).** Change a
different fact: at minute 1 the review stage has posted its **first** inline finding via §8's
sequential `POST .../pulls/1150/comments` path, so a review object now exists with
`commit_id == abc1150` — and an **empty body**. A `commit_id`-only match would call that
"completed" and merge at **minute 1**, with the blocking `[change-requested]` finding still
unposted; #1150's own nine findings spread over 48 seconds, so this window is real. Step 3.1
matches on the **verdict-summary body** instead, so the observation is unchanged — no
non-empty body names `abc1150` — and the refusal stands until the terminal summary posts.

```sh
gh api repos/<repo>/pulls/1150/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>") | select(.body != "") | {commit_id, body}'
#   -> []   inline-comment review objects exist, but NO verdict summary => still unreviewed
#   >>> STOP HERE. Same refusal, same disposition (in flight -> wait and re-poll). <<<
```

**Counter-case — the fixer's own replies (the common case, measured on #1179).** Now suppose
#1150 went round the `gh-fixer` loop: the fixer pushed a fix, moving the head to `ghi1150`,
and replied in-thread to each finding. Those replies **mint review objects** — `COMMENTED`,
`commit_id == ghi1150`, empty body — under the **same** `<automation-login>` the reviewer
uses. So at the moment the fixer finishes, the PR carries fresh reviews naming the *current*
head SHA that **no reviewer ever wrote**, and neither `user.login` nor `state != "PENDING"`
can tell them apart from a real verdict. This is the ordinary path, not an edge case: every
fix round re-creates it. Only the body filter refuses it.

```sh
# DELIBERATELY UNFILTERED — this one lookup omits `select(.body != "")` to SHOW what the
# discriminator rejects. Every lookup gh-merge actually performs carries the filter.
gh api repos/<repo>/pulls/1150/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>") | {commit_id, state, body_len: (.body|length)}'
#   -> {ghi1150, "COMMENTED", 0}   x N   <- gh-fixer's in-thread replies, NOT a review
#   with `select(.body != "")` applied: []  => correctly still unreviewed at ghi1150
#   >>> STOP HERE. The fix round does not review itself. <<<
```

**Counter-case — the silent failed run.** Change one fact: the review run for `abc1150`
**failed** instead of running long (as it did for #1118). The observation at Step 3.1 is
*identical* — no review names `abc1150` — so the same single check refuses, with no separate
failure-detection instrumentation. Only the disposition differs: past the latency window
nothing will ever post, so **stop and surface** for an explicit re-trigger and kick the PR
back to `Awaiting Review`. A failed run raises no alert on its own; #1118 was recovered only
because the operator happened to notice.

### Case 2 — #1149 and #1144: reviewed, clean → the healthy path still merges

```sh
# ---- #1149 ----
gh pr view 1149 --json headRefOid --jq .headRefOid          # -> def1149
gh api repos/<repo>/pulls/1149/reviews --paginate \
  --jq '.[] | select(.user.login=="<automation-login>") | select(.body != "") | {commit_id, body}'
#   -> ONE object survives the body filter: body "Re-reviewed head SHA def1149 ..." (non-empty,
#      names the CURRENT head SHA) => a COMPLETED VERDICT SUMMARY exists => Step 3.1 PASSES.
#      commit_id == def1149 only CORROBORATES (criterion 2); it is not why this passes.
#      Strip the body and the same lookup returns [] => REFUSED, which is the #1179 phantom shape.
# Step 3.2 board Status still Validated; 7 threads posted, 0 unresolved [change-requested]
# Step 3.3 no Codex review posted -> NOT consulted, NOT waited on, NOT a gate (§8)
#   => proceed to Step 4 D7, then Steps 5-8 exactly as the DRY RUN example above.
# ---- #1144 ---- identical shape: a non-empty verdict-summary body names fed1144 (commit_id ==
#   fed1144 corroborates), 22 threads, 0 unresolved => PASSES
```

**Verdict:** Step 3.1 refuses **only** the PR whose current head SHA has no completed review —
it is a pure addition of positive evidence, so both healthy PRs (#1149, #1144) land exactly as
before and no existing gate is relaxed to accommodate it. Never-run, in-flight, and failed
collapse into the one observation "no review-stage verdict summary names this head SHA"; only the
wait-vs-surface disposition differs. Codex posted on none of the three and was consulted for
none of them — Step 3.1 gates the **Claude** review stage's own completion and is **not** a
reinstated Codex gate.
