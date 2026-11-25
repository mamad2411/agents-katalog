---
name: baton-pass
description: Preserve agent progress by writing a concise handoff document for a fresh session. Supports manual, context-triggered, and Claude quota-triggered handoffs.
argument-hint: "[focus for the next session]"
---

# baton-pass

A relay baton for agent continuity: before context or usage limits interrupt
work, write a handoff document so a fresh session (`claude` or `codex`) can pick
up from a small, resumable context.

> Adapted from Matt Pocock's `handoff` skill
> (https://github.com/mattpocock/skills, MIT).

## When you are invoked

There are three paths:

- **Context-triggered**, when the context guard reaches its token threshold.
  The hook context says `Trigger reason: context` and provides the current
  token count, threshold, session ID, handoff directory, and commands.
- **Quota-triggered**, when Claude Code's 5-hour quota guard reaches its
  configured threshold. The hook context says `Trigger reason: quota` (or
  `context+quota`) and provides usage, reset time, session ID, and commands.
- **Manually**, when the user runs the skill themselves. Skip the menu and
  generate a handoff document immediately. If the user passed an argument, treat
  it as the focus for the next session.

## Options menu (hook-triggered only)

Ask the user to choose, then act on their choice. **Never choose for them.**

For a context trigger:

1. **Handoff now** — Write the handoff document (see below), then tell the user
   to resume with `batonresume claude` (or `batonresume codex`).
2. **Extend +10K** — Run the `baton extend <session_id> <value>` command the
   hook provided, then continue the user's current work.
3. **Disable for this conversation** — Run the `baton disable <session_id>`
   command the hook provided, then continue.
4. **Skip** — Do nothing; the hook will ask again on the next turn. Just
   continue the work.

For a quota or combined trigger:

1. **Handoff now** — Run the exact `baton continue-quota <session_id>` command
   supplied by the hook, write the handoff document, then give the matching
   `batonresume` command. The command lets the handoff's cheap inspection and
   write operations finish without being blocked by `PreToolUse`.
2. **Continue this turn** — Run the exact `baton continue-quota <session_id>`
   command supplied by the hook and finish only the current checkpoint.
3. **Disable quota guard for this session** — Run the exact
   `baton disable-session-quota <session_id>` command supplied by the hook.
4. **Skip** — Do not start another large phase. Respect any enforcement from
   later hooks.

Never offer **Extend +10K** for a quota trigger. For `context+quota`, use the
quota menu and create one handoff document, not two.

At the emergency quota level, do not run tests, builds, sweeps,
investigations, refactors, or begin new work. Only preserve work, inspect cheap
state needed for the handoff, write the document, and stop.

## Writing the handoff document

Save to the directory the hook provided:
`<data>/handoffs/<project>/handoff-<YYYYMMDD-HHMM>.md`. When invoked manually,
use `$BATON_DATA/handoffs/<project>/` when `BATON_DATA` is set; otherwise use
this repo's `handoffs/<project>/` folder with the current timestamp.

Use this concise structure, omitting sections that are irrelevant:

```markdown
# Handoff

## Handoff reason

## Goal / current focus

## Current state

## Completed

## Verified facts

## Failed approaches

## Git state
Branch:
HEAD:
Uncommitted changes:
Unpushed commits:

## Tests
Passed:
Failed:
Not run:

## Key decisions & constraints

## Open questions / blockers

## Pointers

## Suggested skills

## Exact next action
```

Record the reason precisely:

- Quota: `5-hour quota guard triggered at 92.4%.` Include the local reset time.
- Context: `Context window reached 191,240 tokens.` Include the configured threshold.
- Combined: include both facts in the same section.
- Manual: `Manual handoff requested.`

The document should capture:

- **Goal / current focus** — what we're trying to achieve. If the user gave an
  argument, tailor the doc toward that next focus.
- **Current state and completed work** — what's done, in progress, and next.
- **Verified facts and failed approaches** — distinguish evidence from guesses
  and prevent the next agent from repeating dead ends.
- **Git state and tests** — branch, HEAD, meaningful uncommitted/unpushed work,
  and what passed, failed, or was not run.
- **Key decisions & constraints** — non-obvious choices and the reasoning.
- **Open questions / blockers.**
- **Pointers** — reference PRDs, plans, ADRs, issues, commits, diffs, and key
  files by path or URL. Do **not** duplicate their content.
- **Suggested skills** — skills the next session should invoke.
- **Exact next action** — the smallest concrete action that resumes progress.

Rules:

- **Redact secrets** — API keys, passwords, tokens, PII.
- **Be concise.** The whole point is a small starting context. Link, don't paste.

## After writing — how to resume

Once the doc is written, print the file path and a copy-pasteable resume
command. Do **not** try to open or launch anything automatically (the current
session can't relaunch itself, and guessing the user's terminal is unreliable).

Use the **agent the user is actually running** for the command. The hook's
context names it (`current agent: …`); if invoked manually, detect it from
`$AI_AGENT` / `$CLAUDECODE` (Claude Code) or `$CODEX*` (Codex), defaulting to
`claude`. Substitute that for `<tool>` below.

Tell the user exactly this (prefer the **bare** command — no path to paste):

> Handoff saved: `<full path to the doc>`
>
> To continue, exit this session (`/exit` or Ctrl-D), then from this folder run:
>
> ```
> batonresume <tool>
> ```
>
> That loads the newest handoff for this project. If you've changed folders,
> pass the file explicitly: `batonresume <tool> "<full path to the doc>"`.
