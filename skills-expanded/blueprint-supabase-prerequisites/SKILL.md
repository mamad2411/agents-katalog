---
name: blueprint-supabase-prerequisites
description: "Confirm Node 22 or later, yarn, and a running Docker Desktop for the local Supabase stack."
---

# Tools

This step carries the **review** gate: the user has read the spec and approved it.

1. Run the base manifest's `requires` probes. If Node is older than 22, or Docker Desktop is not installed or not
   running, tell the user in one plain sentence and give the install hint; do not install or start them yourself.
2. The Supabase CLI and wrangler are installed into the project in the next step and run as `yarn supabase` and
   `yarn wrangler` (never through npx: npx can pick another Node on this machine). Signing in to Supabase or
   Cloudflare is not needed until the publish step.

Done when the check passes: Node 22 or later, yarn answers, and Docker is running.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
