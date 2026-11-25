---
name: investigate-user-bug
description: Investigate a bug a specific diri user hit (crash, hang, slowness, memory leak, blank or garbled terminal, spawn/resume/remote failure, copy/paste not working) from diri's telemetry with the diri-debug CLI. Use when given a user's name, Support ID (D-XXXXXXXX), session id (s_…) or Claude/Codex conversation UUID, or asked "what happened to <person>", "look at alex's crash", "why is it slow for them", or to check this Mac's own spool.
---

# Investigate a user's bug from telemetry

Diri records typed events from the app, the Engine and every Holder, and uploads them to the telemetry Worker. `diri-debug` (in `telemetry/cli/`) reads them back. The records hold identifiers, codes, durations and counters, never content. The contract and the event catalog are in `diri/TELEMETRY.md`.

```sh
alias diri-debug="node $(git rev-parse --show-toplevel)/telemetry/cli/bin/diri-debug.mjs"
```

It needs `DIRI_TELEMETRY_URL` and `DIRI_TELEMETRY_ADMIN_TOKEN`, or `~/.config/diri-debug/config.json`. If neither is set, ask the owner; never guess or hunt for the token. For this Mac, use `diri-debug local …` instead, which needs no token.

Add `--json` when you want to filter the output with `jq`. The human output is already compact.

## Workflow

1. **Identify the install.** Start from whatever you were given.
   - A name or Support ID: `diri-debug who alex`. If several match, use the Support ID from now on.
   - A session id or conversation UUID (for example from an error message such as `No conversation found with session ID: 0a40e747-…`): `diri-debug find <id>`. It names the install and suggests a `timeline` command.
   - Note the app version and when the install was last seen. Data older than 30 days is gone.
2. **Find the incident.** Run `diri-debug incidents <who> --since 7d`.
   - Pick the one that matches the report by time and kind. Records at `!` are incidents; `E` are errors.
   - If the user gave a time ("last night around 11"), still list incidents; their clock and memory are approximate.
3. **Read the timeline around it.** Run `diri-debug timeline <who> --around "<incident time>" --window 20m`.
   - Everything from every process is merged in time order. Read what happened *before* the incident: the spawn, the resume mode, a slow RPC, a remote reconnect.
   - Narrow with `--session s_…`, `--kind 'session.*,holder.*'` or `--sev warn+`. Widen `--window` if the cause starts earlier.
4. **Check health** if the report is about slowness, hangs, memory, fans or "it got worse over the day": `diri-debug health <who> --since 24h`.
   - Look for leak hints (a rising floor), fds nearing the limit, CPU plateaus, and frame or RPC p99 spikes that line up with the complaint.
   - A new `p:pid` means that process restarted.
5. **Check breadth.** Run `diri-debug top --since 7d` (add `--version`) to see whether this signature hits other installs. One user means an environment or edge case; many means a regression.
6. **Form a hypothesis** that explains every record in the window, not just the incident. For example: "resume used conversation X, which the agent never wrote; the agent exited 1; the holder reported exit; the tab dropped to the shell with mouse tracking still on".
7. **Find the code.** Grep the event kinds (`"session.resume_failed"`) and codes in `diri/crates/`. The emitting call site shows the branch taken. Then read backwards to the decision that led there.
8. **Report** the evidence first: the timeline lines, with times, kinds and codes. Then give the hypothesis and the code path, then the fix or next step. Say what the telemetry *cannot* show, for example terminal contents or what the user typed.

If a question can't be answered because an event is missing, say which event kind and fields would have answered it, and where it should be emitted. That is how the catalog grows.

## Privacy rules

- The data is for diagnosing diri. Do not profile a person: when they work, what projects they have, how often they use it. Look only at the window you need.
- Never try to reconstruct content: prompts, output, file names from `path_hash`, or clipboard contents. If the bug needs content, ask the user.
- In anything public (GitHub issues, PRs, commit messages, the website), refer to the user by Support ID only. Never include their name, and never pair a name with a Support ID, install UUID or conversation UUID. Quote only the event kinds, codes and timings the fix needs.
- Do not paste whole batches (`raw`) or long timelines into public places. Summarise instead.
- Keep `DIRI_TELEMETRY_ADMIN_TOKEN` out of commands you echo, files you commit and anything you share. Don't write it to disk except in `~/.config/diri-debug/config.json` (mode 600).
- Delete any raw batches you saved locally when you are done.
- A user can turn uploading off in Settings > Privacy. If an install stopped reporting, assume they chose that; do not look for other ways to get their data.
