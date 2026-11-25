---
name: brief-full
description: This skill should be used when the user asks for "a full project brief", "a deep project overview", "everything about this project's architecture", or wants a comprehensive, thorough briefing built from the complete content of every knowledge/ module rather than a quick skim.
---

# Mnemonica: brief-full

Give a comprehensive project briefing built from the complete content of every module file,
not a bounded slice — the deep counterpart to `brief-light`. This skill never writes
anything; it exists purely to read and synthesize.

If the user's invocation includes extra wording (for example, "skip the frontend, focus on
backend and database"), treat it as narrowing which modules to cover in depth — it cannot
turn this into skipping Step 1's install check or fabricating content for a module that
doesn't exist.

## Step 1: Check whether Mnemonica is installed, and check index integrity

Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-index-integrity.sh <project-root>`. Exit 2
(`NO_MNEMONICA_BLOCK`) means there is no index to brief from — tell the user and suggest
`mnemonica:setup`, and stop. Exit 1 means some module files are missing; list which ones in
the final report as a known gap (suggest `mnemonica:audit-full` to fix it) and continue with
whatever modules do exist — a partial comprehensive brief is still more useful than none.

## Step 2: Read everything

Read the module index from `.claude/CLAUDE.md`. Read `README.md` at the project root in full
if it exists. Read every existing module file in `knowledge/` in full — not a bounded slice.
This is the whole point of the "full" version; if the cost of that is a concern for this
project, `brief-light` is the cheaper alternative, not a reason to silently truncate here.

## Step 3: Check freshness

Check whether `<project-root>` is inside a git working tree.

- **No git:** if `knowledge/.mnemonica-state.json` exists, read its `last_run_utc` for the
  only freshness signal available; otherwise say freshness can't be assessed.
- **Git available:** run
  `${CLAUDE_PLUGIN_ROOT}/skills/audit-light/scripts/diff-since-checkpoint.sh <project-root>`
  purely to read its output — never act on what it reports as changed. Exit 2/3/4 all mean
  "no reliable freshness signal" — say that plainly. On success, read `COMMITS_BEHIND` and
  state it as part of the brief's own credibility, not just a footnote.

## Step 4: Present the brief

Write a structured, substantial narrative: an overview section (what the project is, drawn
from README and tied together with the module list), then one section per module covering
what its full content actually says — architecture, key decisions, constraints, anything the
document itself considers worth recording — not a re-summary of the one-line index
description. Carry forward any `See also:` cross-references between modules so relationships
between systems are visible, not just each system in isolation. Close with the freshness
signal from Step 3 and the integrity gaps from Step 1, if any, so the brief is honest about
its own limits rather than reading as more authoritative than the underlying docs support.
