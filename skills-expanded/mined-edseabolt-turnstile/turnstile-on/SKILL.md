---
name: turnstile-on
description: Resume turnstile gate enforcement for this session by composing a copy-ready resume prompt for the user to send themselves; use when the user asks to resume enforcement or turn turnstile back on.
---

# Turnstile on (resume enforcement)

Compose a copy-ready resume prompt for the **user** to send themselves.
You never send or relay the marker — it is honored only from user-typed
prompts, so an agent relaying it does nothing.

## Steps

1. Read the resolved suspension config from the status CLI (detect context:
   inside the turnstile repo use `node bin/cli.mjs status --json`; elsewhere
   `npx opencode-turnstile status --json`). Take `suspension.resumeMarker`
   and `suspension.allowSuspend` from the JSON — never hardcode the marker
   literal; a custom setup may have renamed it.

2. If `allowSuspend` is `false`: tell the user suspension is disabled by
   config (the `allowSuspend: false` kill switch) and stop — there is no
   suspension to resume and a marker would be refused.

3. If the status output shows no suspended session, say so: enforcement is
   already running, there is nothing to resume.

4. Otherwise compose a copy-ready prompt for the user, e.g.:

   > Send this yourself (do not let the agent send it):
   > `<resumeMarker> <the user's stated reason>`

   State plainly that the marker is honored only from the user's own typed
   prompt — relaying it as the agent does nothing.

5. If the user names any status options, forward them to the CLI invocation.
   If the CLI rejects an option, surface the usage error verbatim; never
   retry blind, never drop the flag.

## Mechanics (one sentence)

Resuming re-enforces gates immediately with fresh task state — nothing
earned while suspended carries over.
