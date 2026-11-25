---
name: flutter-read-logs-usage
description: Explain what the `flutter-read-logs` plugin does and how to use it. Use when the user invokes `/flutter-read-logs-usage`, asks what this plugin covers, or needs help setting up run-log capture for `/read-logs`.
---

# Read Logs Usage

## How to respond

- If the user invoked this skill without a concrete task, explain what the plugin does and when to reach for `/read-logs`.
- If they need setup, point them at this plugin's `README.md` (the canonical setup home) — VS Code/Cursor `dapLogFile`, or the Zed/`script` task.
- If they already have a concrete log-reading task, briefly explain the fit and then run `/read-logs`.
- Do not reply with filler like "skill loaded" or "ready for the task" before explaining the plugin.

## What this plugin does

- Lets Claude read the running app's latest `flutter run` output as on-demand context, via `/read-logs <task>` — instead of pasting terminal logs.
- Captures `flutter run` output per-project to `/tmp/flutter-<repo>.log` (worktree-stable via `--git-common-dir`, overwritten each launch). Two formats, auto-detected: Zed `script` transcript and VS Code/Cursor `dapLogFile` (DAP).
- Reads **task-led** — reads the whole short run, or investigates a long one against your question (errors, event ordering, a feature, …) — flags stale runs, and on first use guides editor setup.

## When to use it

- "Why did the app crash / behave like this at runtime?"
- "Does the auth flow actually reach the API?"
- "Trace the order these events fired" (races / timing).

## Setup

One-time per developer — full instructions in this plugin's `README.md` (VS Code/Cursor
`dapLogFile` keeps the F5 workflow; Zed uses a `script`-wrapped run task). `/read-logs` also
walks you through setup, and offers to apply it, the first time if no log file exists yet.

## Heads-up

Run logs can contain tokens and customer data, and `/read-logs` sends what it reads to the
model — see the caution in `README.md`.

## Related

- `flutter-marionette` — the **proactive** counterpart: *interact* with a live app via MCP.
  Reach for it to *make* things happen; reach for `/read-logs` to *inspect* what a run
  already logged (including crashes/build errors marionette can't see, since it needs a live
  connection).
