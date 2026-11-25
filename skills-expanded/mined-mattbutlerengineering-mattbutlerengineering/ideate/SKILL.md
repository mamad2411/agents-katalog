---
name: ideate
description: "Advances the ideation batch (vetoes, decompose past the veto window, completion sweep); once it is complete, files 4-5 new feature proposals grounded in PRODUCT.md. Invoke with /ideate; runs daily in the mbe-morning routine."
user-invocable: true
---

# Ideate

One skill, two phases. Phase 1 (cycle-check) always runs and is cheap. Phase 2
(ideation) runs only when the previous batch is fully complete, so batches are
strictly sequential: ideate 4-5 → implement all → ideate again.

**State lives in GitHub only** — the open `ideation-batch` issue and its
task-list are the single source of truth. No local state files (cloud and
local sessions must see the same state).

## Hard rules

- **Never add the `ready` label to a `feature-proposal` issue.** The
  implement-queue claims by `ready` and would try to implement an
  un-decomposed proposal. `ready` belongs only to the children `/decompose`
  creates. Defensively strip `ready` from any `feature-proposal` issue you see.
- **Never fetch live site URLs** — cloud routines have no egress
  (docs/scheduled-tasks.md). Grounding = tracked files + `gh` only.
- **Never re-propose a vetoed idea** — vetoes are permanent dedup memory.
- Labels used: `feature-proposal`, `ideation-batch`, `vetoed`, `deferred`
  (create-if-missing with `gh label create` before first use).

## Flags

| Flag               | Effect                                                        |
| ------------------ | ------------------------------------------------------------- |
| `--window-hours N` | Override the 66h veto window (testing only; e.g. `0`)         |
| `--dry-run`        | Report what would happen; create/edit/close nothing on GitHub |

## Phase 1: Cycle-check (always)

### 1. Find the current batch

```bash
gh issue list --label ideation-batch --state open --json number,title,body,createdAt
```

- **None open** → previous batch is complete (or this is the first run) → go
  to Phase 2.
- **Exactly one** → process it below.
- **More than one** (should never happen): process the oldest; comment on the
  newer one(s) noting the anomaly.

Parse the batch body task-list. Each line is one proposal:
`- [ ] #123 — <title>` (optionally suffixed ` → tracking #456` once decomposed).

### 2. Honor vetoes

For each proposal issue:

- **Closed by a human without the `vetoed` label** → add `vetoed`
  retroactively (`gh issue edit N --add-label vetoed`) so dedup memory stays
  complete. Closing IS vetoing.
- **Open with the `vetoed` label** → close it as not-planned with a comment
  ("Vetoed — will never be re-proposed."). Check the box in the batch
  task-list.

A veto wins right up to the moment of decomposition — always re-check
closed/`vetoed` state immediately before flipping.

### 3. Flip proposals past the veto window (max 2 per run, minus open feature runs)

Eligible: open, `feature-proposal`, not `vetoed`, `createdAt` older than
**66 hours** (nominal 72h window; 66h ensures the third daily run flips it
instead of slipping to day 4).

**Feature-run WIP cap (#8743):** first count open issues labeled `tracking`
whose title starts with `[Feature]` and that are not labeled `ideation-batch`.
If the count is 2 or more, flip nothing this run and say so; proposals stay
eligible and flip once a feature run closes. Otherwise flip at most
`2 - count` proposals.

For each eligible proposal, oldest first, **at most `2 - count` per run**
(never more than 2; bounds run cost and feature-run WIP):

1. Comment: "Veto window elapsed — decomposing into implementation issues."
2. Run `/decompose` with the proposal body as the feature description (its
   _Suggested decomposition_ section is the seed). Decompose creates 3-10
   `feature`+`ready` child issues plus one `tracking` issue.
3. **Verify the tracking issue exists** (`gh issue list --label tracking`
   filtered to the new title) before touching the proposal.
4. Append ` → tracking #T` to the proposal's line in the batch task-list and
   check its box; close the proposal with a comment linking the tracking
   issue.
5. **Decompose failed** (no tracking issue): leave the proposal open, comment
   `decompose-failed (attempt N of 3)`. On retry the next day, tell decompose
   to reuse any `[Feature] <name> [i/M]` children that already exist — resume,
   never duplicate. After 3 failed attempts: label the proposal `deferred`,
   close it, note it in the batch, move on.

### 4. Completion sweep

For each decomposed proposal's tracking issue `#T` (open ones only):

- Fetch `#T`'s task-list children. If **every child is closed or labeled
  `deferred`** → close `#T` with a one-line summary comment.
- **Stuck-child escape hatch:** any open child labeled `agent-failed`,
  `stealable`, `needs-review`, or `agent-skip` with no updates
  (`updatedAt`) for **7 days** → remove `ready` if present, add `deferred`,
  comment why. It stays open as an ordinary issue but no longer blocks the
  batch.
- **Batch timeout:** 28 days after the last proposal was decomposed (fallback:
  31 days after batch `createdAt`) → force-complete: label all remaining open
  children `deferred` (removing `ready`), close remaining tracking issues with
  a "batch timed out" comment, and proceed.

### 5. Close the batch when done

Batch complete = every proposal in the task-list is **vetoed**, **deferred**,
or **decomposed with its tracking issue closed**. When complete:

- Close the batch issue with a scorecard comment:
  `proposed N / vetoed N / shipped N / deferred N`, plus links.
- Fall through to Phase 2 in the same run.

If not complete: print a one-line status (`batch #B: x/y proposals resolved`)
and stop. Do not ideate.

## Phase 2: Ideation (only when no open batch)

### 1. WIP gate (defense in depth)

Re-query open `ideation-batch` AND open `feature-proposal` issues. Either
non-zero → abort with a log line. Also verify `PRODUCT.md` exists at the repo
root — if missing, file one `needs-info` issue saying ideation is blocked on
the charter, and stop.

### 2. Read grounding (tracked files + gh only)

- `PRODUCT.md` — themes, non-goals, guardrails (mandatory).
- Signals: `metrics/process-metrics.jsonl`, `metrics/last-audit.json`,
  `metrics/pr-acceptance.json`,
  `metrics/queue-telemetry.jsonl`,
  `metrics/audit-coverage.jsonl` (per-surface sweep status; zones with no row are
  "never recorded" — `.audit-state/` is gitignored and invisible to you), `.claude/acmm/state.json`,
  `docs/incidents/` (if present).
- `metrics/ui-quality-findings.json` (if consulted): only records with
  `state: "open"` are signals — a `closed` seed (`closed_at`, `state_reason`)
  was re-audited and no longer observed, and a `declined` one was vetoed.
- Open issues labeled `audit`, `sentry`, `ci-fix`, `enhancement` — these ARE
  the committed outputs of site-audit and sentry-triage.
- `git log --oneline --since="30 days ago"` — momentum and recency per app.
- Sampled `grep -rn "TODO\|FIXME" apps/ services/ packages/ --include="*.ts*"`.
- Best-effort `pnpm outdated` (tolerate failure — registry egress may be
  blocked in cloud; fallback signal is open `dependency-freshness` issues).

### 3. Dedup (hard rule)

```bash
gh issue list --label feature-proposal --state all --limit 200 --json title,body,labels
gh issue list --label tracking --state all --limit 100 --json title,state
```

Skip any candidate that semantically matches a **vetoed** proposal (permanent)
or overlaps an existing tracking issue / open `feature` chain (already
built or building).

### 4. Generate 4-5 proposals

Hard minimum 4, maximum 5. Respect every PRODUCT.md guardrail (≤1 per app,
hospitality up to 3, unless a signal is overwhelming; every proposal cites ≥1
signal and states its venue/guest impact; sized to decompose into 3-10 child
issues). A proposal whose only signal is internal fails the decision filter:
drop it, or tie it to the hospitality work it speeds up or protects.

Per proposal — title `[Proposal] <app>: <feature>`, label `feature-proposal`
**only**, body (write it to a temp file and create with
`gh issue create --body-file <path>`; an `@<path>` value given to `--body`
is posted as the literal string, only `--body-file` reads a file):

```markdown
## Problem & Evidence

<signal citations: file paths, issue links, trend numbers>

## Charter alignment

<quoted PRODUCT.md theme>

## Venue/guest impact

<who feels this (operator, host, guest) and what changes for them; or, for
tooling, the named hospitality work it speeds up or protects>

## Proposed feature

<what the user gets, 2-4 sentences>

## Target app/surface

## Scope estimate

<S/M/L + expected child-issue count (3-10)>

## Suggested decomposition

<3-6 bullets — seeds /decompose>

## Non-goals & risks

## Veto

Reject by closing this issue or adding the `vetoed` label. Un-vetoed
proposals are decomposed automatically after ~72h (first morning run past
66h).
```

### 5. Create the batch issue

Title `[Ideation] Batch <YYYY-MM-DD>`, labels `ideation-batch` + `tracking`.
Body: PRODUCT.md git SHA it was grounded on, a 3-5 line signal summary, then
the task-list (create with `gh issue create --body-file <path>`, never
an `@<path>` `--body` value):

```markdown
- [ ] #<n1> — <title>
- [ ] #<n2> — <title>
      ...
```

### 6. Report

Batch URL + proposal URLs, one line each. In the mbe-morning routine, a new
batch ends the run (give Matt the veto window headline).

## Edge cases

| Case                                   | Handling                                        |
| -------------------------------------- | ----------------------------------------------- |
| Closed proposal, no `vetoed` label     | back-fill the label (closing IS vetoing)        |
| Veto arrives after 66h but before flip | veto wins — re-check at flip time               |
| All proposals vetoed                   | batch completes; re-ideate same run             |
| Decompose crashes                      | retry-with-resume daily, 3 strikes → `deferred` |
| Child stuck failed/needs-review 7d     | `deferred`, excluded from completion            |
| Batch stuck 28d post-decompose         | force-complete with deferral sweep              |
| `ready` on a proposal                  | strip it defensively, comment                   |
| Routine misses a day                   | window widens by 24h — harmless                 |
| Two open batches                       | process oldest, flag anomaly                    |
