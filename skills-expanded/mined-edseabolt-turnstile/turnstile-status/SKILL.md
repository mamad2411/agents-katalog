---
name: turnstile-status
description: Run the turnstile status CLI and present the result readably (gate state, suspension, journal paths, replayed state). Use when the user asks about turnstile gate state, whether gates are armed/passed, or the turnstile install status.
---

# Turnstile status

Run the turnstile status CLI and present the result readably. Read-only —
never modify config or journals from this skill.

## Steps

1. Detect context: inside the turnstile repo use `node bin/cli.mjs status`;
   elsewhere `npx opencode-turnstile status`.
2. If the user names any status options (e.g. `--json`, `--check-updates`),
   forward them verbatim to the CLI invocation. If the CLI prints a usage
   error, show it to the user — do not retry or drop flags.
3. Present the result: gate state, suspension, journal paths, replayed state.
