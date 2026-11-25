---
name: blueprint-supabase-run-check
description: "Start the app on this computer against the local Supabase stack and fix what only breaks in the built version."
---

# Start it for real

1. `yarn start --port <a spare port>`: it starts the local stack, builds against it, and serves the build with
   wrangler dev. Open `/`, sign in with a seeded account from the README, and use the main screen once.
2. Fix anything that only breaks in the built version: a missing `VITE_` value (the page stays blank), the
   Content-Security-Policy blocking the call to Supabase (the browser console says so), the SPA fallback.
3. Stop what you started — wrangler dev runs several processes; do not leave one running. Leave the local Supabase
   stack running: the next steps use it.

Done when the check passes: the app started with `yarn start --port <n>` serves a page that renders, its
Content-Security-Policy allows the local Supabase, and the build in `dist/` talks to it.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
