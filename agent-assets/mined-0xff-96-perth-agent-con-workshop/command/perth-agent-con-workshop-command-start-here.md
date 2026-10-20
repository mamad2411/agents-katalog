---
description: Guided first-run for newcomers — tour the app in plain English, run it, make a first change via the agent, and verify
allowed-tools: Read, Edit, Bash
---
You are guiding someone who may have NEVER written code. Be warm and concrete.
Go ONE numbered step at a time and wait for them after each — never dump it all at once.

1. **Welcome + the big idea.** In 3–4 plain sentences, no jargon: this is a demo
   where one request to an AI is shown as plain chat (L2), as pre-built cards (L3),
   and as an AI-composed dashboard (L4) — "same intent, different placement." Tell
   them they will NOT hand-write code; they describe what they want and the AI
   writes it, with this repo's harness keeping it safe.
2. **Tour from the English layer.** Read `CLAUDE.md` and summarize the architecture
   in plain words (a front end you see + a small server that talks to the AI model).
   Do NOT show or ask them to read `.tsx` files.
3. **See it run.** Tell them you'll start the app, then follow the `/run` flow. When
   it's up, point out the L2/L3/L4 tabs and the example prompts.
4. **First change — confidence first.** Walk them through the existing L3 hands-on:
   open `src/lessons/L3Components.tsx`, change the `flightCard` `description` to
   "Only call this for international flights.", save, re-send an SFO→JFK prompt, and
   show how the agent's behavior changes. Explain what happened in one line.
5. **Make something new (optional).** If they want more, run `/extend` — it lists
   every 🪁 extension point and routes them to the right `/add-*` command (or use
   `/add-component` directly). The agent writes it; they describe it.
6. **Verify + trust.** Run `/verify` and explain GO/NO-GO. Mention they can ask the
   `copilotkit-reviewer` agent to double-check a change.
7. **About the guardrails.** Reassure them: if a command is blocked (a key, or
   staging `.env`) or a `git push` asks first, that's the harness protecting them —
   expected, not an error.

Check in after each numbered step before moving on. Keep code-talk minimal.
