---
name: model-router
description: Pick the cheapest model that can do each task well. Use before every task to size it as light, regular or heavy and hand it to the matching router helper. Also handles "router auto" and "router manual".
---

# Model Router

Expensive models should not do cheap work. Before each task, size it as
light, regular or heavy, then get it done on the cheapest model that can do it
well. Think in tiers, never in brand names. `tiers.md` maps each tier to a model
for each provider. `samples.md` has example requests with their tiers.

## Tiers

| Tier | Typical work |
|---|---|
| Light | One file, small edit (about 20 lines or fewer), clear instruction, no design decision: colour, text or spacing tweaks, renames inside one file (however many occurrences), typos, formatting, short copy (under about 150 words), simple lookups |
| Regular | Multi-file features, research with sources, articles and longer writing, explaining code, debugging with a clear error message |
| Heavy | Architecture and system design, maths, algorithms and calculations, bugs that survived one fix attempt (even if the next fix looks small), security-sensitive changes, migrations, large refactors, anything where a wrong answer is costly |

Count files first: if the work creates or changes more than one file, it is at
least regular, however small each edit is. When the signals are mixed, round up
one tier.

## Routing (auto mode)

1. Read the request and pick a tier. Find your own tier by matching the model
   you are running on to `tiers.md`; if it isn't listed, assume regular.
2. Same tier as the model you are running on: do the work directly. No handoff.
3. Different tier: hand it to the matching helper (`router-light`,
   `router-regular` or `router-heavy`) with a sharp brief (see below).
4. Too small to be worth a handoff: if the brief would be longer than just doing
   the work (for example a one-line edit to a file already in your context), do
   it yourself.
5. Escalation: if a helper fails, says it is unsure, or its result fails an
   obvious check (does not build, does not answer the question), retry once on
   the next tier up. Never step down a tier in the middle of a task.
6. End each reply with exactly one tag, in one of these three forms and nothing
   else inside the brackets (explanations go outside them):
   - a helper ran: `[router: <tier> → <helper's model>]`, e.g. `[router: heavy → opus]`
   - you did it yourself: `[router: <tier> → <your model>]`, e.g. `[router: light → sonnet]`
   - you suggested switching (step 7): `[router: heavy → switch suggested]`
   Use model names from `tiers.md`.
7. Heavy work that needs back-and-forth (architecture discussions, multi-round
   debugging) is not handed off, because helpers return one result and cannot
   talk to the user. Even in auto mode, suggest in one line that the user switch
   the main model to the heavy tier. Count it as back-and-forth only when the
   user invites a discussion or the work cannot start without their decisions.
   One-shot heavy work still goes to `router-heavy`: a calculation, a
   well-specified refactor, or a bug that survived a fix (put the failed fix in
   the brief). Do not keep heavy work yourself because it looks small.

The best main model is the regular tier, so routing runs on a mid-priced model
and regular work needs no handoff.

## How to hand off

Launch the helper named `router-<tier>` with your agent's subagent feature.
In Claude Code, use the Agent tool with that subagent type, and reuse the same
helper for follow-up tasks in a session so it keeps its context.

If your agent cannot launch a helper on a different model, you are in manual
mode. Say so once, plainly, and do not claim any switch happened.

If no `router-<tier>` helper is installed for your agent, you are in manual mode
even after `router auto`. Only write a tag naming a model if that exact helper
ran.

Never say a switch happened unless a helper actually ran.

## Sharp briefs

Every handoff includes:

- the goal in one line
- exact files and line numbers, when known
- constraints, taken from the memory file
- what "done" looks like

The helper should never need to search for something you already know.

## Shared memory

File: `.model-router/context.md` in the project root. Example:

```
Project: Next.js site, Tailwind
Key files: app/page.tsx (home), components/Button.tsx
Decisions: brand green = #16a34a, no new dependencies
Current task: redesigning signup flow
```

- Read it once per conversation; re-read it only after you change it.
- Helpers read it before working. Tell them to in the brief.
- Update it when a decision changes, and trim it. Hard cap: about 40 lines.
- Never put secrets, keys, tokens or personal data in it.
- Never edit `.gitignore`. The first time you create the file, tell the user once
  that they may want to ignore `.model-router/`.

## Modes

- `mode: auto`: route as above. (Which mode is the default is covered below.)
- `mode: manual`: work on whatever model the user picked. When the recommended
  tier differs from your own tier (matched via `tiers.md`, regular if unlisted),
  add one line at the top, for example
  `Light task: switch to Haiku to save tokens.` Say it only when the tier changes
  from the previous message, never on every message.
- The user switches by saying `router auto` or `router manual`. A `mode:` line
  is written to `.model-router/context.md` only when the user says `router auto`
  or `router manual`, and it then applies to every agent working in this project.
- With no memory file, use the default mode from your instruction block (the
  always-loaded router lines). If that says nothing, use auto in Claude Code, manual everywhere else.
- On agents with no helper support, run in manual mode and say so once.
