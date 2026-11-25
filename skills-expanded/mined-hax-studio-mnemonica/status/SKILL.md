---
name: status
description: This skill should be used when the user asks to "check mnemonica status", "is mnemonica up to date", "show the knowledge docs status", "how stale are the docs", or wants a quick read-only health check of a project's Mnemonica installation without running an actual audit.
---

# Mnemonica: status

Report the current state of Mnemonica in a project — module count, index integrity, and how
far behind the last audit is — without changing anything. This skill never writes a file;
if a step below would normally cause a write in another skill, here it only reads what that
step would have needed and reports on it.

If the user's invocation includes extra wording beyond the trigger phrase (for example,
asking to focus the report on one specific module), treat that as scoping this run's report,
not as license to skip a check below or to write anything — this skill has no rules to
override in the first place, since it never modifies the project.

## Step 1: Check whether Mnemonica is installed

Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-index-integrity.sh <project-root>`.

- Exit 2 (`NO_MNEMONICA_BLOCK`): Mnemonica isn't installed here (or `.claude/CLAUDE.md` has no
  Mnemonica block). Report that plainly and suggest `mnemonica:setup`, and stop — there is
  nothing further to check.
- Exit 0 or 1: continue. Note whether any module files were reported missing (exit 1) — carry
  that list into the final report; do not try to fix it here (that's `audit-full`'s job).

## Step 2: Read the module index

Read the module index from `.claude/CLAUDE.md` (the `MNEMONICA:BEGIN`/`END` block). List each
module: its file, its owned-path glob(s), and its one-line description. This is the whole
index, not a summary of it — the point of `status` is to make this visible without the user
having to open the file themselves.

## Step 3: Check git availability and audit freshness

Check whether `<project-root>` is inside a git working tree.

- **No git:** report that `audit-light` is unavailable here and staleness can't be measured
  in commits; if `knowledge/.mnemonica-state.json` exists, still report its `last_run_utc`
  and `last_mode` as the only freshness signal available.
- **Git available:** run
  `${CLAUDE_PLUGIN_ROOT}/skills/audit-light/scripts/diff-since-checkpoint.sh <project-root>`
  purely to read its output — never act on what it reports as changed.
  - Exit 2 (`NO_CHECKPOINT`): report "never audited" and suggest `mnemonica:audit-full`.
  - Exit 3 (`STALE_CHECKPOINT`): report the checkpoint as stale and suggest `audit-full` to
    re-baseline.
  - Exit 4 (`CORRUPT_CHECKPOINT`): report the state file as unreadable and suggest
    `audit-full` to re-baseline.
  - Exit 0: read the `COMMITS_BEHIND` line for how many commits have landed since the last
    audit, and read `knowledge/.mnemonica-state.json` directly for `last_run_utc` and
    `last_mode`. Also read the `FILES_CHANGED` section — this is what turns "12 commits
    behind" into an actual sense of what happened, not just a count. List the changed paths
    if there are few enough to read comfortably; if there are many, report the count and a
    handful of examples instead of the full list, so this step stays a cheap read rather than
    turning into its own small audit. Report all of this together (for example: "12 commits
    behind, last audit was a light run 4 days ago; recent changes touch server/api/ and
    src/components/").

## Step 4: Report

Present a compact summary: installed (yes/no), module list with descriptions, any missing
module files, git/checkpoint availability, freshness (commits behind, last audit time and
mode), and a brief sense of what has changed recently (from Step 3's `FILES_CHANGED` read).
Recommend a next action only when the data actually calls for one (missing modules →
`audit-full`; stale or absent checkpoint → `audit-full`; large `COMMITS_BEHIND` with an
otherwise healthy checkpoint → `audit-light`) — don't recommend an audit just because one is
always technically possible to run.
