---
name: superfinish
description: Use after an implementation plan from a goal folder's plans/ subfolder has been executed — captures findings, writes a closeout report to reports/, annotates the plan, and advances the parent seed's progress-report table. Bookkeeping only; never executes plan work.
license: MIT
related skills: superplan, supertraverse
---

# Superfinish

Run **after** an implementation plan has been executed. Read the execution context, then update the
goal folder's vault: capture findings, write a closeout report, append a brief close-out note to the
plan, and advance the parent seed's progress-report table.

**Input:** `<PLAN.md>` — the executed implementation plan (the `.md` file from a goal folder's
`plans/` subfolder). May be passed explicitly, by a calling skill, or inferred from the session.
For an upfront stage, the caller also passes the execution-entry snapshot and actual delivery evidence
defined by superrun. A recovery invocation may reconstruct them only from authoritative tracked
artifacts and verified branch/PR history; it never guesses from current annotated plan bytes.

## The deliverable is vault bookkeeping — and ONLY that

**superfinish reads execution context and writes vault docs. It NEVER executes, implements, or
resumes any planned work.** It does not write source code, does not run tests or builds, and does not
create worktrees. It runs once the implementation is already done and records what happened. It
publishes only the **vault bookkeeping docs themselves**: `github` uses the commit/PR path and `none`
uses verified local persistence. Publication is automatic under the user's standing authorization.
It never commits source code or execution output. After the Final Report, the skill is done.

| Thought | Reality |
|---------|---------|
| "There's an unchecked task in the plan, I'll just finish it" | NO. superfinish records outcomes; it does not execute remaining work. If work is unfinished, say so in the closeout and stop. |
| "I'll run the tests once more to confirm before writing the report" | NO. Use the evidence already produced in this session. superfinish runs no tests/builds. |
| "There's leftover source/execution work I'll commit alongside the docs" | NO. superfinish commits **only** the vault bookkeeping docs (automatically, via PR). Never source code, never execution output. |

## Input — resolve `<PLAN.md>` (Gate 1)

Resolve the plan in this order; stop at the first that succeeds:

1. **Explicit argument** — `<PLAN.md>` was passed to the skill. Use it.
2. **Passed by a calling skill** — if another skill invoked superfinish, it MUST pass the plan it was
   implementing. Use that.
3. **Infer from the session** — determine the implementation plan file that drove this execution
   session from the conversation context (the plan that was read/executed at session start).
4. **Ask** — if the plan still cannot be determined confidently, ask the user which plan file it is.
   Do **not** guess and do **not** hard-error here.

## Validation (Gate 2) — must be an implementation plan in `plans/`

The input MUST be an implementation plan living in a goal folder's **`plans/`** subfolder. It must
**not** be a seed, master, or sub-master plan.

- Confirm the resolved path is inside a `plans/` directory.
- Confirm the file is not a seed/master/sub-master plan. Signals it IS a seed/master (→ reject): it
  sits in `master-plans/`; its header declares `**Type:** Planning SEED` / `Sub-master plan` /
  `Master plan`; or it contains a progress-report table sequencing multiple sub-PRs rather than a
  single executable task list.

If the input is a seed/master/sub-master plan, **report the error and exit**:

    superfinish operates on an executed implementation plan from a `plans/` subfolder.
    `<PLAN.md>` is a <seed/master> plan (<reason>). Nothing was written. Exiting.

## Repo configuration (.superenv)

Resolve project context before any workflow action by sourcing `${CLAUDE_PLUGIN_ROOT}/scripts/_common.sh` under bash (it refuses zsh and other shells — wrap the call in `bash -c '…'` when your shell is not bash) and calling `superagent_load_context "$PWD" run` (lifecycle control commands first load the registered `SUPERAGENT_PROJECT_ROOT`). Use its exported physical `REPO` and validated `SUPER_GIT_MODE`. Resolution is process environment > nearest/explicit project `.superenv` > packaged default; missing mode means `github`. In `none`, never run git, gh, GitHub API, credential discovery, worktree, commit, push, PR, merge, sync, or CI-poll operations. An existing `.git` directory does not change this rule.

## Vault root

Resolve `SUPER_GOAL_ROOT` (above). If it starts with `/` or `~`, the vault is **external**:
`<vault_root>` is that path (`~` expanded to `$HOME`, one trailing `/` stripped), resolved physically
(`cd "<path>" && pwd -P`) so it matches the paths `launch.sh` stores, and the vault is its own git
repository outside the checkout. Otherwise `<vault_root>` is `<primary_root>/<SUPER_GOAL_ROOT>`
(`primary_root` = the physical `REPO` exported by `superagent_load_context`). Every goal
folder, project folder, loop-status file and lock derives from `<vault_root>`; **never join
`SUPER_GOAL_ROOT` onto the checkout root by hand.** The same rule is `vault_root` /
`vault_is_external` in `scripts/_common.sh`.

## Goal Identification

Identify the **goal folder**: the top-level initiative directory that contains the `plans/`,
`master-plans/`, `findings/`, and `reports/` subfolders. It is the parent of the `plans/` folder the
input plan sits in (worked example from the originating repo: `<vault_root>/2026-05-20-graphgen-grammar-first-redesign/` — see **Vault root**). All
output is written under this goal folder.

**Read `goal-directives.md` at the goal-folder root FIRST, if it exists.** It is the authoritative map
of which subfolder each file type goes in. Route every write according to it. The standard routing
(absent a directives override) is:

- **Findings** → `findings/`
- **Closeout report** → `reports/`

If a goal folder lacks `reports/` or `findings/`, create the subfolder when writing (do not invent a
different location).

## Execution identity and lost-response recovery (Gate 3)

Resolve the root and mode through superstage S1. For an upfront stage require one complete
execution-entry snapshot: root/generation, active stage path and Stage ID/revision, Preparation report
and digest, authoritative vault commit containing the prepared stage/receipt, reviewed code revision,
source revision, and consumed contract/provider receipts. Verify the prepared digest against the stage
blob at that recorded vault commit, omitting only the Preparation line per superstage S5. The current
plan may already contain a closeout note and is therefore not the prepared digest input. A completed
stage never has to satisfy the current *unstarted-stage* preparation predicate forever; closeout proves
which valid historical preparation and execution snapshot produced the actual delivery.

Classify the actual outcome separately:

- **Complete delivery:** verify the code PR and merge commit on authoritative main, an authorized
  direct-integration commit, or (for evidence-only discovery) the specified evidence/decision A7
  publication. This identity plus the execution snapshot can become a delivery receipt and satisfy
  produced contracts.
- **Partial execution:** verify the same execution snapshot plus the actual open PR, exact head commit,
  branch/worktree when retained, and CI run/conclusion or blocker. This permits a partial closeout report
  and `executed — PR open`; it is explicitly **not delivered**, satisfies no produced contract, and is
  non-consumable by dependencies. A later invocation after verified integration revises this same
  identity-bound report into the complete delivery receipt instead of creating another report.

Preserve any repair predecessor PR/branch/worktree and disposition history. Missing or contradictory
evidence for the claimed outcome is BLOCKED. For incremental plans, keep the legacy evidence rules and
record the resolvable plan/code identity available.

Before drafting a timestamped report, derive one stable **execution-attempt key** from the immutable
execution snapshot plus code repository/PR number (or the discovery evidence-publication identity).
The current PR head, CI results, open/merged state and merge commit are versioned observations of that
attempt, not parts of its lookup key. Scan the synchronized authoritative vault and history by this key:

- exactly one matching report plus matching plan note/active-row history means prior publication
  succeeded. If its latest observation already matches the verified outcome, reuse it and perform no
  duplicate write/A7 publication. If it is partial and the same PR later advances head, CI or merge
  state, append/version those observations and upgrade that **same report path** in place; never allocate
  another timestamped report merely because mutable PR outcome fields changed;
- one incomplete closeout A7 publication means resume and complete that same
  report/note/ascent/publication unit, retaining its identity and filename. Do not allocate a second
  timestamped report;
- multiple or conflicting receipts, or a claimed publication absent from authoritative history, is
  BLOCKED until reconciled.

This is the idempotency key for a lost final response. Filename timestamps, session memory, a row
status, or a top note alone are not authoritative execution-attempt identity or delivery evidence.

## After-Run Finish

Do the four steps below. **Draft every write to a scratch path OUTSIDE the goal folder** (e.g.
`$TMPDIR/` or `.claude/scratch/`) and write nothing into the vault until all four drafts are complete —
then write them all into the vault automatically (no confirmation is awaited).
Steps that were already done in a prior superfinish run for this session are idempotent — re-detect
and skip them (see each step).

### 1. Capture Findings

Identify findings, conflicts, or new information discovered **during execution** — paying particular
attention to anything that **contradicts or conflicts with the plan's assumptions** (a mechanism that
didn't work as the plan assumed, a constraint discovered mid-build, a cardinality/contract that
differed from the spec).

For each finding, review the existing docs in the goal folder's **`findings/`** subfolder and decide:

- **Revision** — an existing findings doc already covers this topic → update that doc with the new
  information.
- **Addition** — no existing doc covers it → create a new doc `findings/YYYY-MM-DD-hh_mm-<topic>.md`
  (today's date and the current UTC hour and minute at the start of the basename).

In **both** cases the findings doc **MUST contain an explicit reference to `<PLAN.md>`** (the plan
that produced/supports the finding), as a full-path wikilink. Open new findings docs with the standard
header block (`# Title`, `**Date:**`, `**Status:**`, `**Related:**` / `**Parent:**`).

**Be extra certain of each finding.** If you are unsure a finding is correct, **do not record it** —
false findings poison the goal. Only record what the session's evidence verifies. If there are no
findings, that is fine — record none.

For upfront work, link each finding to the affected stable contract and/or assumption IDs, or state
explicitly that no such ID is affected. Classify from verified evidence. A routine implementation fact
that preserves acceptance, scope, dependencies, contract semantics, and downstream evidence does not
start a planning cycle or invalidate preparation. A verified contradiction of a shared contract or
assumption names each affected unfinished stage and invalidates its old preparation for selection; flag
`REPLAN-REQUIRED` so the existing decision/adoption path can create C8's durable batch. The finding is
evidence for that decision, never proof by assertion and never authority to rewrite the tree itself.

### 2. Closeout Report

Write a closeout report for this session to the **`reports/`** subfolder (per `goal-directives.md`),
named `reports/YYYY-MM-DD-hh_mm-<topic>.md` (today's date and the current UTC hour and minute). It MUST include:

- **What was done** — the work this session shipped/completed.
- **Next steps** — what remains, deferred items, follow-ups.
- **Reference to the findings** uncovered this session (the docs from step 1), if any.
- **Reference to `<PLAN.md>`** — the plan this report grades, as a full-path wikilink.
- **Execution identity** — the execution-entry snapshot from Gate 3, including its historical prepared
  plan commit/blob, receipt path/digest, root generation, Stage ID/revision, reviewed code revision,
  source revision, and consumed delivery receipts (or the available legacy identity).
- **Outcome identity** — for complete delivery, code PR/merge commit, authorized direct integration
  commit, or the discovery evidence/decision publication; for partial execution, the verified open PR,
  exact head, CI result/blocker and explicit `delivered: false`, `consumable: false`.
- **Delivered contracts** — every produced contract ID and semantic revision, with concrete evidence
  that the delivered result satisfies it. For a partial report, list every declared produced contract
  and revision as `pending — not delivered; consumable: false`, with no satisfaction claim. An explicit
  `none` is allowed only when the stage produces no contract. On verified integration, upgrade those
  same entries in place to delivered evidence and `consumable: true`.
- **Attempt observations** — append/version each verified PR head, CI run/conclusion, blocker, merge
  state and merge/direct-integration commit under the stable execution-attempt key. Do not rewrite the
  historical failed/open observation when the attempt later succeeds.
- **Repair/integration history** — every predecessor PR and its verified reuse/replacement/closure or
  adopted disposition, plus the active successor relationship when applicable.
- **Limitations** — every acceptance case met by a test-scoped substitute rather than end-to-end
  evidence, and every case narrowed or postponed by an owner decision, each with its reason and (for a
  postponement) the stage or goal that owns it. A substitute is never reported as end-to-end evidence;
  carry these into any release dossier the project keeps.
- **CI duration** — when CI is test evidence, the longest CI step on the final run: its name, its
  duration (`gh run view <id> --json jobs`), and the limit it runs under when one is configured
  (a job `timeout-minutes`, a test-runner timeout, a `subprocess` deadline) with where it is set. A
  step above about 80% of a known limit is also recorded as a finding (step 1): it will turn into a
  red run before long, and the fix is cheaper now than after a timeout.

Open with the standard header block (`# Title`, `**Date:**`, `**Type:** Sub-PR closeout`,
`**Status:**`, `**Related:**`). When CI evidence exists, cite the source CI run id(s) and verify the
artifact dates postdate the commits. Close the loop both ways — the
report links back to the plan/seed it grades.

For complete delivery this report is the stage's durable **delivery receipt**. For partial execution it
is a durable **partial closeout**, not a delivery receipt; no consumer may use it as prerequisite
evidence. A discovery stage is complete without a code PR only when its plan's experiment evidence and
decision criteria are satisfied, the evidence and documented decision were published through the
applicable internal A7 docs PR/direct commit or external-vault commit, and every produced discovery
contract is identified. If that decision
contradicts a live contract/assumption, publish the verified finding and return REPLAN-REQUIRED through
the same adoption path used for implementation stages; do not mark affected consumers executable.

### 3. Update Plan

Insert a **brief** close-out note **at the top of `<PLAN.md>`** — immediately after the plan's title
heading (and any parent-seed reference block superplan injected), **before** the plan body — that
summarizes the work done and links to the closeout report (step 2) as a full-path wikilink. Place it
at the top, **not** at the end of the file, so a reader sees the outcome first. **Keep it short** — a
few lines at most, not a restatement of the report.

**Idempotency:** if `<PLAN.md>` already contains a close-out note referencing the report for this exact
stable execution-attempt key, keep that link. Reuse the report when observations match or revise it in
place for a partial-to-delivered upgrade. A note for another attempt is history, not a match. Digest
verification continues to use Gate 3's historical prepared-plan blob; never compare the receipt digest
to this newly annotated current file.

### 4. Update the Plan Tree Upward

Identify the **immediate parent** seed/master plan `<PLAN.md>` was derived from — read the parent-seed
reference near the top of `<PLAN.md>` (superplan injects one; this is the `supertraverse` C5 "up" link).
Before ascent, check **supertraverse C7/C8's active-plan guard**. A predecessor closeout must
not overwrite a pending repair or a successor's active row. Record its outcome as historical
only. If that predecessor actually merged, reconcile the delivered code and contracts into the C8
record before any fresh correction work; completed history stays completed and any incompatible
correction gets a fresh stage ID. For a successor, include actual predecessor PR disposition and integration evidence in
the closeout and repair record; mark Resolution `integrated` only after all integration and
predecessor dispositions are verified. Leave unresolved dispositions explicitly blocking.
Then **invoke the `superagent:supertraverse` skill** (Skill tool) and run its **ASCENT in completion mode**,
chaining parent-seed references from this completed leaf up to the root. supertraverse C7 specifies
the per-row update precisely; this section need not restate it. In brief:

- **Local mode:** first write `reports/<timestamp>-<topic>-completed-local.md` with root/active leaf,
  `git_mode: none`, before/result snapshot ids and manifests, added/modified/deleted paths, local
  command results and evidence paths, task/final review outcomes, acceptance coverage, outstanding
  obligations, timestamp, and `PR/commit: N/A (SUPER_GIT_MODE=none)`. Reopen and validate it. Set the
  active leaf to `completed-local`; roll an ancestor to `completed-local` only when every active
  descendant has a valid local receipt or authorized disposition and no repair obligation remains.

- **The leaf's own row** (the row pointing at `<PLAN.md>` in its immediate parent) gets either
  `executed — PR open` (the code PR is still open at superfinish time) or `completed-and-merged`
  (the code PR has been squash-merged to `main`) — pick the one that matches reality. Evidence-only
  discovery with verified evidence/decision publication uses `completed-and-merged` / `done` without a
  code PR. Add a one-line rollup + `Closeout: [[…]]` wikilink in **Comments**. Put `#NNN` in the PR
  column only for code work; leave it blank (or explicit `none`) for evidence-only discovery and cite
  its A7 publication in Comments/report. A follow-up superfinish invocation flips `executed — PR open` →
  `completed-and-merged` once the code PR merges (idempotent re-run).
- **Each ancestor row above the leaf** is flipped to `completed-and-merged` only when *every* row
  in the child's progress-report table is merged-on-`main` per C4 (`completed-and-merged` / `done`
  / `merged` / `shipped` / `closed-out`, with `deferred` / `declined` / `out-of-scope` counting as
  non-blocking; `executed — PR open` does NOT count — the code is not yet on `main`). Otherwise
  the ancestor goes to `in progress (partially executed)` (when it was previously `incomplete`,
  `PLAN WRITTEN — ready to execute`, or `in progress (planning underway)`) and flipping-completes
  stops higher up.

It reads/preserves the `Plan` link via the shared inference (C3 — tolerating a legacy `Plan: [[…]]` in
Comments). If the seed also carries top-of-file closeout banners (`🟦/🟩/🟪/🟧`), update the matching
banner too.

**Idempotency:** a row already matching its evidence-based target state is left untouched (handled
by the shared ascent — `in progress (partially executed)` when ancestors are partial,
`executed — PR open` when the leaf's PR is still open, `completed-and-merged` when the PR has
merged). Re-running superfinish after the code PR merges is the supported way to flip
`executed — PR open` → `completed-and-merged` and propagate the parent rollup upward.

For upfront ascent, C7 consumes the identity-bound closeout record, not the row label alone. A partial
record can support only `executed — PR open`. It may mark an
implementation stage complete only with verified integration and delivered-contract revisions, or a
discovery stage complete with its verified evidence/decision. A verified contract contradiction is
surfaced before the next dispatch and affected unfinished preparation is no longer executable; routine
findings leave preparation valid.

If no parent seed can be identified (no parent-seed reference and none inferable), note this in the
Final Report under "Other files" as "parent plan: none found — not updated" and continue; do not
fabricate a parent.

## Standing authorization — proceed without pausing (REQUIRED)

The user has granted **standing authorization** for superfinish to write its bookkeeping docs to the
vault and merge the resulting PR. **Do NOT pause to ask for approval, and do NOT present the drafts and
wait for a "go" before writing.** Once all four steps' drafts are complete, write the files into the
vault, then commit and merge them — automatically. This is not waived or re-enabled by auto-accept /
`bypassPermissions` mode; it is the default behavior.

Do not dump the full drafts to chat up front. The user's single checkpoint is the **Final Report**
(below), which clearly enumerates every file written this run.

## Commit and merge the vault docs — via PR (REQUIRED)

When `SUPER_GIT_MODE=none`, this heading means durable local publication under superauthor A7's
local branch. Reopen the report, plan note, repair record, and every updated ancestor; verify the
receipt fields above; run no git/GitHub operation; then continue to the Final Report.

Once the vault files are written, commit those bookkeeping docs and merge them to `main` via a pull
request — **without asking the user for confirmation** (standing authorization, above). If
`SUPER_PROTECTED_MAIN=true` (the shipped default), the default branch is a **protected branch** (direct
pushes are rejected), so this MUST go through a feature branch and a PR — merged per
`SUPER_MERGE_METHOD` (default `squash`) — even though it is docs-only. If `SUPER_PROTECTED_MAIN=false`,
a direct commit to the default branch is permitted instead — see `superauthor` clause **A7**'s
`SUPER_PROTECTED_MAIN=false` worked example for the exact recipe (no feature branch, no PR, no `gh`).

**External vault (see Vault root):** the target repo is the vault at `<vault_root>`, and
`superauthor` A7's direct-commit variant always applies — `git -C "<vault_root>" add
<vault-relative paths…> && git -C "<vault_root>" commit -m "docs(finish): <topic> closeout —
superfinish output [skip ci]"`, push only if the vault has an `origin`. The skeleton below is
the internal-mode path. A7's **precondition** applies: if `<vault_root>` is not its own
repository, STOP and report — never improvise a `git init`. The progress-table **PR** cell of a
*planning* row stays blank in external mode (there is no PR for a vault-only commit); an executed code
row records its code PR number, while evidence-only discovery stays blank / `none`.

Treat the report, plan note, findings and ancestor updates as one authoritative A7 publication unit.
On retry, reconcile the exact execution/outcome identity against integrated history before opening a branch or
committing: reuse a complete unit, resume the one unique partial unit, and block on competing units.
An ignored loop-state hint or an unmerged internal docs branch is never authoritative publication.

**Scope of the commit: only the bookkeeping docs** written this run — the closeout report, new/revised
`findings/` docs, the `<PLAN.md>` close-out note, and **every ancestor plan file** the completion-mode
ascent updated (the immediate parent and any further-up ancestors it flipped, up to the root). Add each
with an explicit `git add <path>`; **never `git add -A`** (the working tree may hold unrelated changes
that are not yours to commit).

These are docs-only changes, so tag the commit subject `[skip ci]` to avoid firing CI on the merge.

```bash
# from the repo root, with the vault docs already written
BRANCH="finish/<topic>-$(date +%Y-%m-%d)"
git checkout -b "$BRANCH"
git add <reports-doc> [<findings-doc> ...] <plan-file> <immediate-parent-file> [<ancestor-plan-file> ...]   # explicit paths only
git commit -m "docs(finish): <topic> closeout — superfinish output [skip ci]"
git push -u origin "$BRANCH"
gh pr create --title "docs(finish): <topic> closeout" \
  --body "Closeout written by superfinish for <topic>. Grades <PLAN.md>."
gh pr merge --squash --delete-branch          # plain --squash is the DEFAULT — do NOT reach for --admin
git checkout main && git pull --ff-only
```

Notes:
- `--squash --delete-branch` keeps history clean and removes the feature branch after merge.
- **Merge per `SUPER_MERGE_METHOD` (default `squash`). Pass `gh pr merge --admin` only if
  `SUPER_ADMIN_MERGE=true` — otherwise never.** Reaching for `--admin` when the key is unset or `false`
  buys nothing on a repo whose branch protection doesn't require it, and reliably trips the harness
  security classifier. Full rationale in `superauthor` clause **A7**. Escalate only if a plain merge
  is actually refused (and `SUPER_ADMIN_MERGE=true` permits it), and say why in the Final Report.
- **`--delete-branch` can exit 1 with `fatal: '<branch>' is already used by worktree` — the PR still
  merged.** That is the local delete step, not a rejection: confirm with
  `gh pr view <n> --json state,mergedAt`, then drop the remote ref with
  `gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>`.
- Capture the resulting **PR URL** (from `gh pr create` / `gh pr view --json url`) — report it in the Final
  Report below.
- Do **not** commit Anthropic/Claude attribution or `Co-Authored-By` trailers (repo policy).
- If `SUPER_GH_DISABLE_SANDBOX=true` (macOS hosts where `gh` needs keychain access to verify the
  TLS cert), all `gh` commands need `dangerouslyDisableSandbox: true`. If `false` (the shipped
  default), run `gh` normally.

## Final Report — then exit

After the writes and the PR merge, give the user a **single report** and exit. **This report is the
user's single window into what superfinish wrote — every file path created or modified this run MUST
appear here.**

    ## Superfinish complete

    **Plan:** <full path to PLAN.md>
    **Goal folder:** <full path>
    **Closeout record:** <reports/...> — <stage/generation/revision and outcome identity> (partial / delivered; created / resumed / already integrated)

    **Files created/modified:**
    - <reports/...> — closeout report (created)
    - <findings/...> — finding (created/revised)     (or: none)
    - <PLAN.md> — close-out note inserted at top       (or: already present — skipped)
    - <master-plans/...> — progress-report row updated (one line per ancestor the ascent touched, up to root; or: already complete — skipped / none found)

    **Findings:**
    - <finding summary>                                (or: none)

    ⚠️ **Critical:** <only present when a finding contradicts a plan assumption>

    **PR:** <url> (merged)
    **Commit:** <short-sha> in <vault_root>   (external vault — print this line INSTEAD of the PR line, verbatim form)
    **Persistence:** completed-local receipt verified (SUPER_GIT_MODE=none)  (local mode instead)

After printing the report, the skill is done: take no further action and ask no follow-up question.
