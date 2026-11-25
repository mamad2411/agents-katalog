---
name: aisa-clawhub-breakout-editor
description: "Guide for ClawHub breakout variants after the neutral mother skill is already stable."
---

# AIsa ClawHub Breakout Editor

Refine ClawHub-oriented breakout copy after the mother skill is already stable.

## When to use

- When preparing ClawHub-specific breakout variants
- When sharpening JTBD copy for ClawHub search without changing runtime behavior

## Core rules

- Start from a stable mother skill; do not use this profile as the default editor for `targetSkills/`.
- Keep the real auth story explicit: `AISA_API_KEY`, relay targets, OAuth approval, media upload, and external writes.
- Align `SKILL.md`, README, manifests, and registry-facing metadata.
- Use breakout positioning only when it matches the shipped runtime and sibling ladder.
- Keep ClawHub-only breakout slugs inside `targets/clawhub-breakout-variants.json` and generated ClawHub layers.
- Do not delete core runtime behavior just to make a package sound safer.

## Output expectations

- ClawHub copy may be sharper, more task-first, and more explicit about side effects than the mother skill.
- Suspicious remediation belongs in the dedicated `aisa-clawhub-suspicious-remediation-editor` profile, not here.
- The result should stay compatible with the repo's generated ClawHub skill/plugin layers.
