---
name: brief-light
description: This skill should be used when the user asks for "a quick project brief", "orient me on this project", "give me a fast overview", "catch me up on this codebase", or wants a cheap, fast introduction to what a project is and what systems it has without a deep read of every knowledge/ file.
---

# Mnemonica: brief-light

Give a real, substantive orientation to a project — not two sentences, but not the full depth
of `brief-full` either — by reading the CLAUDE.md index plus a bounded slice of each module
file, so the cost stays predictable regardless of how large any individual module has grown.
This skill never writes anything.

If the user's invocation includes extra wording (for example, "focus the brief on the
payments system"), treat it as narrowing which modules to cover — it cannot turn this into an
unbounded read of every module file in full; that is what `brief-full` is for.

## Step 1: Check whether Mnemonica is installed

Run `${CLAUDE_PLUGIN_ROOT}/scripts/check-index-integrity.sh <project-root>`. Exit 2
(`NO_MNEMONICA_BLOCK`) means there is no index to brief from — tell the user and suggest
`mnemonica:setup`, and stop. Exit 1 means some module files are missing; note which ones,
but continue — a brief can still be useful with partial coverage.

## Step 2: Read the module index and README

Read the module index from `.claude/CLAUDE.md`. Read `README.md` at the project root if it
exists, for the project's own framing of what it is (name, purpose, how it runs) — this skill
only reads `README.md`, never writes it, same as every other Mnemonica skill.

## Step 3: Read a bounded slice of each module

For each module file that exists on disk, read roughly its first 40 lines (or its first
major heading section, whichever is shorter) — not the whole file. This is what keeps
`brief-light` light: cost stays roughly constant per module regardless of how long any one
of them has grown. Do not read further just because a file looks interesting; that tradeoff
is what `brief-full` exists for.

## Step 4: Check freshness

Check whether `<project-root>` is inside a git working tree.

- **No git:** if `knowledge/.mnemonica-state.json` exists, read its `last_run_utc` for the
  only freshness signal available; otherwise say freshness can't be assessed.
- **Git available:** run
  `${CLAUDE_PLUGIN_ROOT}/skills/audit-light/scripts/diff-since-checkpoint.sh <project-root>`
  purely to read its output — never act on what it reports as changed. Exit 2/3/4 all mean
  "no reliable freshness signal, docs may not reflect recent work" — say that plainly rather
  than guessing. On success, read `COMMITS_BEHIND` and mention it if it is more than a
  handful of commits.

## Step 5: Present the brief

Write a real narrative, not a bare list: what the project is (from README plus the module
descriptions), what systems it has and roughly what each does (from the bounded reads), and
a one-line freshness caveat if the docs might be behind. Mention at the end that
`mnemonica:brief-full` exists for a deeper read into every module's full content when the
light version isn't enough.
