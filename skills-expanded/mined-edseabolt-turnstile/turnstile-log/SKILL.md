---
name: turnstile-log
description: Show the recent turnstile JSONL journal (gate passes, reviewer verdicts, suspensions, refusals, recovery) via the turnstile CLI. Use when the user asks to see the turnstile journal, gate history, or recent enforcement log entries.
---

# Turnstile log

Tail the turnstile JSONL journal via the CLI. Read-only — never modify
config or journals from this skill.

## Steps

1. Detect context: inside the turnstile repo use `node bin/cli.mjs log`;
   elsewhere `npx opencode-turnstile log`. It reads the per-session sink
   for the requested session (defaulting to the most recent per-session
   journal when no sessionID is given), walking the shared journal and
   rotated generations for that session's rows, and handles missing/rotated
   files.
2. The CLI defaults the tail to the configured replay bound; default to
   `--tail 50` unless the user says otherwise. If the user names any other
   options (e.g. `--tail 100`, a sessionID, `--json`), forward them verbatim
   to the invocation; if the CLI rejects one, surface the usage error
   verbatim — never retry blind, never drop the flag.
3. Pretty-print entry types (GATE / VERDICT / suspended / refused /
   recovery).
