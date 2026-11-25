---
name: turnstile-off
description: Suspend turnstile gate enforcement for this session by composing a copy-ready suspension prompt for the user to send themselves; use when the user asks to pause gate enforcement or turn turnstile off for the session.
---

# Turnstile off (suspend enforcement)

Compose a copy-ready suspension prompt for the **user** to send themselves.
You never send or relay the marker — it is honored only from user-typed
prompts, so an agent relaying it does nothing.

## Steps

1. Read the resolved suspension config from the status CLI (detect context:
   inside the turnstile repo use `node bin/cli.mjs status --json`; elsewhere
   `npx opencode-turnstile status --json`). Take `suspension.suspendMarker`
   and `suspension.allowSuspend` from the JSON — never hardcode the marker
   literal; a custom setup may have renamed it.

2. If `allowSuspend` is `false`: tell the user suspension is disabled by
   config (the `allowSuspend: false` kill switch) and stop. Do not compose a
   prompt that would be refused.

3. Otherwise compose a copy-ready prompt for the user, e.g.:

   > Send this yourself (do not let the agent send it):
   > `<suspendMarker> <the user's stated reason>`

   State plainly that the marker is honored only from the user's own typed
   prompt — relaying it as the agent does nothing.

4. If the user names any status options, forward them to the CLI invocation.
   If the CLI rejects an option, surface the usage error verbatim; never
   retry blind, never drop the flag.

## Mechanics (one sentence)

While suspended, deliberate gate blocks stop being enforced but every
would-block is journaled, no gate credit is earned, and the suspension
survives a restart.
