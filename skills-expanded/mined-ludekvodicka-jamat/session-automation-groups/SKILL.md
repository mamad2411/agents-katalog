---
name: session-automation-groups
description: "Set Jamat automation session groups consistently across workflows. Use when an automated worker starts, waits for a person or review, resumes, is blocked, finishes, or receives follow-up work. Jamat owns and installs this skill for Claude and Codex. Does not close sessions or manage worktrees."
---

# Session automation groups

Use this installed skill's `scripts/session-automation-groups.mjs` with Node. Jamat installs and
updates this adapter automatically. Read [REFERENCE.md](REFERENCE.md) for the CLI and failure rules.

The calling workflow owns task truth and decides when a transition is justified. This skill owns
the presentation. Never reproduce the mapping in a workflow or infer completion from process
activity, `idle`, a stopped process, a closed ticket alone, or a code commit alone.
Complete the caller's mandatory entry and session-ownership proof before any presentation call.

- Report `working` before task work, after an answer, and before any follow-up edits.
- Report `waiting` before asking a person or opening any human review. A cancelled review stays
  waiting. After approval report `working` if further work remains.
- Report `blocked` for a known obstacle that prevents progress; put its reason in the note.
- Report `completed` only after the whole task, all required reviews and final verification.
  A code landing followed by an outstanding trail/documentation review is still unfinished.

The worker applies its own transitions directly, even without a coordinator. Coordinators may
reconcile their current verified workflow state. A workflow must not repaint another pass's or
a person's unrelated session. Do not opt an interactive session into automation implicitly.

For own transitions use `apply --self --state STATE`. Keep the workflow's active color with
`--active-color COLOR` when resuming. An optional `--note-file PATH` replaces the entire note:
preserve ticket/worktree identification. A `waiting` note states what the person must answer or
approve and where, matching the request that ends the reply; a `blocked` note states the obstacle;
a `completed` note states the result and replaces any earlier waiting text. Omitting the note
preserves it. Move no files, tickets, tabs or worktrees as part of this skill. Stopping and removing a
finished session belongs to the session or workflow that launched it, through `appjamat-v3`.

Do not ask permission for the presentation change itself. An unsuccessful result must be reported;
preserve the actual task result and pending work. Do not repeat a commit or create a replacement
session because presentation failed. Retrying this helper with the same current state is safe.
