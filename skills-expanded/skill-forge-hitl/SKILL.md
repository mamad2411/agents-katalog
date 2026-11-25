---
name: skill-forge-hitl
description: "Apply a numbered list one item at a time — status board upfront, per-item approve/skip, approve-all mode, commits after each approved item. Use when stepping through skill-forge-judge findings or any numbered changes. Triggers: apply these, go through each one, apply improvements, commit each change. Not for: bulk refactors, one-shot changes, or changes that don't need per-item review."
---

# HITL Loop

Throw the lasso, pull it tight, move to the next. One change at a time, one approval at a time — no bundling, no skipping ahead.

**Core question for every item:** What's the smallest change that makes this finding false? Apply only that — nothing more. Verify: if any part of the change were removed, would the finding still be true? If yes, the change is too large.

## Workflow

### 1 — Read the list

Parse the numbered improvement list from context. If there are multiple lists or it's unclear which to apply, ask once before starting — not mid-loop. If the response does not resolve the ambiguity, stop: "Still unclear which list to apply — please re-invoke with the target list quoted directly."

If improvements reference specific files, verify they still exist and haven't changed substantially since the evaluation. If a target file is missing or heavily modified, note it at the top of the board: "⚠ Target may be stale — <file> has changed since evaluation. Items may not apply cleanly. (c)ontinue / (Q)uit?"

If items have dependencies (item 3 requires item 1), note the dependency at the board level. Do not re-order — apply in sequence and mark dependent items `[○]` if their prerequisite was skipped.

Check git status before showing the board. If the working directory is not a git repo, note this at the top of the board and skip all commit steps:

```
ℹ No git repo — changes will be applied but not committed.
```

Display the full status board upfront: all items with `[ ]` markers, then `(A)pprove all / (s)tart` options. Symbols: `[ ]` pending, `[✓]` done, `[→]` in progress, `[–]` skipped, `[○]` obsolete.

If the user responds `A`: apply and commit all items in sequence, then show the final board per step 3.

If the user responds `s`: begin the per-item loop from item #1.

### 2 — Apply each one

Repeat for every item in order:

**a. Announce** — show `─── #N of M ───` and the full improvement description.

**b. Apply**

If the smallest change requires touching more than one logical unit (function, section, rule), the improvement is under-scoped — note this in the change summary and apply only the first unit.

Do not touch adjacent code, bundle items, or anticipate the next improvement. If applying this item overlaps with a later item (same lines, same function), apply only what's needed now and note the overlap in the change summary.

If an improvement requires non-edit actions (adding a dependency, creating a new file, running a command), describe the action in the change summary and let the user decide whether to perform it.

**c. Show the change**
```
Changed: <file>:<lines> — <one-line description>
<concise diff summary — not the full file>
```

**d. Ask**
```
(a)pprove, (r)evise, (s)kip, (o)bsolete, (A)ccept-all, (k)skip-all, (Q)uit?
```

Wait. Do not advance until the user responds. Any input not in the table below is a stop signal: show the current board and ask "Stop here? (y) to pause, (c)ontinue from #N?"

| Key | Commit? | Mark | Advance to | Special |
|-----|---------|------|------------|---------|
| `a` | yes | `[✓]` | next item | — |
| `r` | no | — | re-apply same item | Collect guidance, re-show. After 3 revisions: "Revised N times — skip and file a separate issue, or keep going?" |
| `s` | no | `[–]` | next item | Note reason if given |
| `o` | no | `[○]` | next item | Already done / no longer applies / impossible |
| `A` | yes (current + all remaining) | `[✓]` each | final board | Skip per-item prompts for remaining |
| `k` | no | `[–]` current + all remaining | final board | — |
| `Q` | no | `[–]` all remaining (current unchanged) | final board | — |

**e. Update the board** — after each decision, show the current state of all items using the status symbols. For accept-all (`A`): skip intermediate board updates — apply and commit each remaining item silently, then show the final board once in step 3.

### 3 — Done

When all items are processed, show the final board and a one-liner: `HITL complete. Applied: N  Skipped: M  Revised then applied: P`

## Commits

If in a git repo: commit after each approved change, before advancing to the next item:

```bash
git add <changed files>
```
```bash
git commit -m "<short description of this improvement>"
```

If commit fails (pre-commit hook, empty diff): show the error, fix the issue, re-stage, and retry. If the fix changes the applied improvement, re-show the diff and re-ask for approval — do not silently commit a different change than what was shown.

If not in a git repo: skip commits entirely. Mark each approved item `[✓]` and continue — do not warn on every item, the single board-level notice is sufficient.

## NEVER

- NEVER apply two improvements in one change — if both items touch the same code, the user loses the ability to approve them independently, which defeats the purpose of the loop.
- NEVER advance past an item without an explicit approve, revise, or skip response — silence is not approval.
- NEVER ask clarifying questions about an improvement's intent mid-loop — ambiguities must be resolved in step 1 before the first item.
- NEVER show the full file diff — show only the changed lines and a one-line description. Full files bury the signal.
- NEVER let a revision loop run silently past 3 attempts — a stuck item means the improvement is under-specified, not that the agent needs to try harder.
- NEVER offer accept-all (`A`) before the status board has been shown — the status board IS the plan review; once the user has seen all items listed, offering approve-all at the board level or from item #2 onwards is acceptable.
- NEVER treat lowercase `q` as a quit signal — only uppercase `Q` quits; lowercase `q` is keyboard-adjacent to `a` and falls through to the unknown-input stop signal.
