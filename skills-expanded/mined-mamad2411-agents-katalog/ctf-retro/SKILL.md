---
name: ctf-retro
description: Use when a CTF solve, major pivot, or repeated dead loop should be converted into AI-facing heuristics and direct skill improvements. Best after solving a challenge, escaping a misleading path, or noticing a recurring tool-order mistake, routing miss, proof-order mistake, or collaboration failure that future CTF sessions are likely to repeat.
---

# CTF Retro

## Overview

Use this skill to do a short AI-only retrospective after a solve or major pivot, then decide whether the lesson should directly update one or more CTF skills. The default output is changed future behavior, not a new retrospective file.

## Use This Skill For

- A challenge was solved and there is a reusable lesson that could speed up future solves.
- The session escaped a dead loop and the trigger for that pivot should be preserved.
- A routing miss, tool-order mistake, environment mistake, or collaboration mistake became clear.
- A lesson appears general enough to justify changing a skill rather than keeping it as transient reasoning.

## Workflow

1. Reconstruct the decisive path.
   Read the relevant `steps.md`, successful proof steps, and the exact pivot that changed the solve.
2. Separate challenge-local detail from reusable behavior.
   Ignore single-use payloads, credentials, exact addresses, and challenge-specific constants unless they reveal a more general rule.
3. Extract only behavior-changing lessons.
   Focus on reusable signals, dead loops to avoid, earlier pivot triggers, better proof ordering, better tool ordering, and collaboration or environment corrections.
4. Decide whether the lesson should update a skill.
   Patch a skill only when the lesson changes future routing, default tooling, proof order, environment choice, or multi-session behavior across more than one likely future challenge.
5. Patch the smallest relevant surface.
   Update the narrowest skill or reference that would have prevented the mistake or accelerated the solve.
6. Stop when the generalized rule is clear.
   Do not turn one challenge into a broad rewrite of the whole skill suite.

## Guardrails

- Do not create a new retrospective file by default. Internal reasoning plus direct skill updates is the normal path.
- Do not force every challenge to mutate a skill.
- Do not encode single-challenge payloads, target addresses, creds, or secrets into skills.
- Prefer changing the smallest reusable rule that would have changed the future outcome.
- If the lesson is still uncertain, keep it as internal reasoning for now instead of overfitting the skill suite.

## Output Expectations

- State the generalized lesson in one or two lines.
- Identify which skill should change and why.
- Patch the skill immediately if the lesson is clearly reusable.
- If no skill change is justified, say so and stop.
