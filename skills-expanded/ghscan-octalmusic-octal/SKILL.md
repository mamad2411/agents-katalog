---
name: drum-programming
description: Use when writing deterministic house drum patterns, pockets, velocities, and chokes.
---

# Drum Programming

Use this skill whenever drums are created or changed. The goal is a deterministic
pocket: the same source renders the same audio, while still feeling played.

## Engine-Neutral Pocket

- Use 16th-step pattern data.
- Write per-step velocity maps by hand.
- Write fixed micro-timing offsets as data, in milliseconds.
- Use a small number of deliberate variations over 2, 4, or 8 bars.
- Keep the kick stable; put most human feel in hats, claps, and percussion.

Use the installed house pack's `patterns/drum-patterns.json` for pattern IDs,
velocity maps, and `offsetMs` values. In a scaffolded project this is
`.agents/octal-packs/house/patterns/drum-patterns.json`; in this repo source it
is `packages/skills/packs/house/patterns/drum-patterns.json`.

## Octal Contract Rules

- Use `ctx.samples.drumVoice(reference, { chokeGroup })` for drums that need
  velocity or choke behavior.
- Use choke groups for open and closed hats.
- Do not use raw `Tone.Player` for drums when velocity matters.
- Do not use `humanize` or `probability`. Substitute fixed `offsetMs`, velocity
  maps, explicit alternate steps, and `ctx.rng` only for seeded selection.
- Keep Tone.js examples compatible with the project-pinned Tone.js `15.1.22`.

## Swing

House swing belongs in the narrow range: `Transport.swing` 0.05 to 0.2 at a
16th-note subdivision. Keep it subtle; velocity and fixed offsets do most of the
pocket work.

## References

- `references/deterministic-pocket.md`
- `references/drum-voice-patterns.md`
