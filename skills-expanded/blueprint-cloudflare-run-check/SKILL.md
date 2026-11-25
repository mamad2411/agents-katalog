---
name: blueprint-cloudflare-run-check
description: "Build, run it with wrangler dev, and make sure the screen and the API answer."
---

# Start it for real

1. `yarn build`, then `yarn start --port <a spare port>` (wrangler dev on this computer, with the local D1), and open
   `/` and `/api/health`.
2. Fix anything that only breaks in the built version (the assets directory, the SPA fallback, a migration that does
   not apply).
3. Stop what you started — wrangler dev runs several processes; do not leave one running.

Done when the check passes: the app started with `yarn start --port <n>` answers `/api/health` with `{"ok":true}` and
`/` serves the app.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
