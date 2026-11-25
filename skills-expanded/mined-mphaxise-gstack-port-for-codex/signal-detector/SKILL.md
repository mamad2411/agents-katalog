---
name: signal-detector
description: GBrain-inspired signal capture for Codex. Use when the user shares original thinking or entity mentions worth durable capture in the local brain.
---

# Signal Detector

Use this skill when a message contains durable signal:

- a new idea or thesis
- an observation in the user's own words
- a person, company, or concept worth linking into the local brain

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain fires on every inbound message as an always-on sidecar. In this repo, signal detection is explicit and lightweight:

- `python3 scripts/brain_capture_signal.py --text "..." --mode original`
- optionally add explicit entities with `--entity people:"Name"` or `--entity companies:"Name"`

## Workflow

1. Decide whether the message is worth capture or just operational chatter.
2. Preserve the user's phrasing exactly when it is original thinking.
3. Choose the right destination:
   - `originals` for the user's own thinking
   - `ideas` for product or business ideas
   - `concepts` for reusable frameworks
4. Add explicit entity backlinks only when the category is clear.
5. Stay quiet unless the user asked for the capture summary.

## Current Upstream Coverage

Prioritize original ideas and observations, then detect secondary entity signals. Preserve the user's exact wording separately from interpretation, attach source context and timestamp, and avoid converting casual mentions into durable claims.

## Guardrails

- Do not paraphrase away the signal.
- Do not auto-create dubious entity pages from weak mentions.
- Do not block the main task just to capture a signal.
