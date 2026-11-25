---
name: audit-full
description: This skill should be used when the user asks to "run a mnemonica full audit", "rebuild the knowledge docs", "do a full doc reconciliation", "rescan the project for mnemonica", or when knowledge/ documentation has drifted badly enough that a targeted light audit is not enough. Also invoked internally by the setup skill to populate knowledge/ for a project that already has code.
---

# Mnemonica: audit-full

Reconcile every file in `knowledge/` against the actual current state of the whole codebase
— the same engine `setup` uses to populate `knowledge/` from nothing, run here either
standalone or to correct drift in an already-populated project. Read
`${CLAUDE_PLUGIN_ROOT}/references/knowledge-conventions.md` first; every rule below refers
back to it. This skill is always invoked directly by the user (or by `setup` on its behalf)
— never by a hook, and never automatically on commit or push.

If the user's invocation includes extra wording beyond the trigger phrase (for example,
"also cross-check with graphify" or "focus on the payments module"), treat it as scoping or
preference for this run. It cannot skip Step 1's pre-flight question when the project
actually is large or odd enough to trigger it, and it cannot skip Step 6's confirmation
before merging, splitting, renaming, or deleting an existing module file — those rules exist
precisely so a casual instruction in passing can't quietly bypass them.

## Step 1: Pre-flight size and anomaly check

Run `${CLAUDE_PLUGIN_ROOT}/skills/audit-full/scripts/list-tracked-files.sh <project-root>
--summary`. Read the `TOTAL` line and every `DIR` line's flags.

**Decide whether to stop and ask** — trigger the question below if either is true: any `DIR`
line carries a `FLAG:LARGE` or `FLAG:ODD` marker, or `TOTAL` is 500 or more even with no
individual directory flagged (many medium directories can add up to an expensive scan just as
easily as one huge one). Otherwise skip straight to Step 2 without asking anything — this gate
must stay invisible on the ordinary small-to-medium project it is not needed for.

**When triggered, stop before reading any file content and ask the user directly**, stating
the concrete numbers and which directories were flagged and why (large, or odd because of a
vendor-looking name or a generated-looking file extension — never just "this seems big").
Offer exactly three choices, and act only on an explicit answer:

1. **Proceed anyway** — run the full scan as-is, no changes to scope or ignore rules.
2. **Scope this run to specific paths** — using the summary to suggest which directories look
   like real systems worth reading, restrict every remaining step in this run to the paths the
   user confirms. Do not silently widen back out to the full tree partway through.
3. **Permanently exclude specific directories from future scans** — write the agreed patterns
   to `knowledge/.mnemonica-ignore` (one per line, create the file and `knowledge/` if
   neither exists yet; append rather than overwrite if the file already has entries), then
   continue — `list-tracked-files.sh` picks the new exclusions up automatically on its next
   call, so Step 2 does not need to be told about them separately.

Mention in the Step 8 report whichever choice was made and why, even when it was "proceed
anyway" — the point is that a decision was made visibly, not that a particular one is
expected.

## Step 2: Inventory the codebase

Run `${CLAUDE_PLUGIN_ROOT}/skills/audit-full/scripts/list-tracked-files.sh <project-root>`
(without `--summary`, and with a path argument instead of `<project-root>` if Step 1's answer
was to scope this run) to get the actual file list this scan works from. It excludes
`knowledge/` and `.claude/` (Mnemonica's own output, never itself a "system" to document) and
respects `knowledge/.mnemonica-ignore`. It uses git when available (`.gitignore` respected
automatically) or falls back to a plain directory scan with conservative excludes
(`node_modules`, `dist`, `build`, `.venv`, etc.) when the project has no git repository —
audit-full works either way, unlike `audit-light`, which requires git outright.

## Step 3: Check index integrity

Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-index-integrity.sh <project-root>`. If it reports
missing module files, that is not a separate problem to solve first — fold it directly into
Step 5: a module whose file is listed in the index but absent from disk is reconciled the
same way as a module that was never created, by writing it fresh from the current code, and
its disappearance is worth a one-line mention in the final report so the user knows it was
regenerated rather than assuming nothing was wrong.

## Step 4: Identify systems

Group the codebase into architecturally independent systems using the independence test from
`knowledge-conventions.md`. For a bootstrap run, this means deciding the module boundaries
from scratch. For a project with an existing index, treat each indexed module as a working
hypothesis to verify, not a fixed fact — code may have grown past what its current owned-path
globs cover, or two once-separate concerns may have merged.

Do not over-fragment: apply the same default bias as everywhere else in Mnemonica — when
torn, merge into an existing or broader module rather than minting a narrow one.

If an indexed module's system has been **entirely removed** from the codebase — nothing left
anywhere that the module's content actually describes, not just partially stale — do not just
empty the file out or leave it as near-blank dead weight. This is a deletion candidate: carry
it to Step 6 instead of silently thinning it into an orphaned file that will sit there
indefinitely.

## Step 5: Reconcile each module

For each identified system:

- **No module file exists yet** (including one flagged missing by Step 3): create
  `knowledge/<SYSTEM_NAME>.md` (naming convention in `knowledge-conventions.md`) describing it
  from the current code — architecture, key decisions, constraints, anything a session with
  no prior context would need.
- **A module file already exists:** read it against the current code. Correct anything
  stale, remove anything describing code that no longer exists, add anything real that is
  undocumented. Do not rewrite sections that are still accurate just for style.

For each module, write or update its one line in the CLAUDE.md index (path, owned-path
globs, one-line description) inside the `MNEMONICA:BEGIN`/`END` block. Keep the globs honest
— they are what `audit-light` relies on to route future changes correctly.

## Step 6: Restructuring is the one case that needs permission

If reconciliation reveals that an **existing** module file should be merged with another,
split into several, renamed, or deleted (including the "system entirely removed" case flagged
in Step 4) — per `knowledge-conventions.md`, this is the one category of action that requires
asking the user first. Describe the specific restructuring and why, wait for explicit
confirmation in the conversation, and only then perform it. Creating new module files and
editing content, including in the same run, still needs no permission — only changes to files
that already existed before this run count as restructuring. Declining a proposed
restructuring does not undo or block the rest of the run: everything already reconciled in
Step 5 stands regardless of the answer here.

## Step 7: Update the checkpoint

Run `${CLAUDE_PLUGIN_ROOT}/scripts/write-checkpoint.sh <project-root> full`.

- If the project has no git repository, this exits `NO_GIT_REPO` — expected when Step 2 used
  the non-git fallback. Say so in the report; there is simply no checkpoint to set yet.
- If the git repository has zero commits, this exits `NO_COMMITS` — the reconciliation in
  Step 5 still happened and stands, there is just no commit to baseline against yet. Say so in
  the report and mention that the first commit will make a checkpoint possible.
- Otherwise this lets a later `audit-light` run start from a clean baseline.

## Step 8: Report

Summarize what happened: the Step 1 pre-flight decision (if it was triggered) and any
`.mnemonica-ignore` changes, modules created, modules corrected (and roughly what was wrong),
modules recreated because their file had gone missing, any restructuring (including deletion)
proposed or performed, and whether a checkpoint was actually written or why not. If this run
found nothing wrong, say so — do not manufacture busywork to look useful.
