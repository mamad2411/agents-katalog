---
name: live-sound-reinforcement
description: "Run live sound: gain structure, system EQ and feedback control, monitor mixes, dynamics and a repeatable soundcheck."
type: procedural
category: audio
domain: audio
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - soundcheck a band
  - stop microphone feedback
  - monitor mix setup
  - system gain structure
  - live mixing console
aliases:
  - foh
  - live-audio
keywords:
  - live-sound
  - foh
  - monitors
  - feedback
  - gain-staging
  - pa
  - soundcheck
mcp_servers:
  - ableton
source: custom
enabled: true
---

# Live Sound Reinforcement

## Purpose

Run live sound: gain structure, system EQ and feedback control, monitor mixes, dynamics and a repeatable soundcheck.

## When to Use

- A live event needs a PA that stays stable as the room fills.
- Feedback, muddiness or clipping appear under real stage volume.
- Musicians need monitor mixes they can hear themselves in.

## When NOT to Use

- The output is a studio recording; use a mixing workflow instead.
- The venue supplies its own tech and only playback is needed.
- The problem is a broken driver or cable — fix the hardware first.

## Capabilities

- Set gain structure from source to speaker with headroom at every stage.
- Ring out monitors and place mics to survive stage volume.
- Build a mix that survives the room, not just the empty hall.
- Document the patch and scene for repeatability.

## Inputs

- Channel list with sources, mic/DI choices and phantom-power needs.
- Venue geometry, speaker placement and the console's output capacity.
- The set list and any instrument changes between songs.

## Workflow

1. Patch and label everything, then verify phantom power per channel before enabling it.
2. Set input gain on the loudest real moment, leaving 6–10 dB of headroom.
3. Tune the system with a measurement mic; correct the room before mixing the band.
4. Ring out each monitor with the mic it will actually use.
5. Build scenes per song and save them; label the show file with the date and venue.
6. Walk the room during the set and correct for the crowd's absorption.

## Tools

- ableton
- rew
- sm-maart
- console-scene-files

## Examples

- `A 31-band cut at the exact feedback frequency is safer than a broad 3 dB shelf that eats the vocal.`
- `Saving a scene per song means a mid-set instrument change is a recall, not a scramble.`

## Safety

- Protect hearing: limit SPL at the mix position and keep earplugs available.
- Mute outputs before patching to avoid a full-level pop into the PA.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `ableton` | stdio | full | medium | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/audio/live-sound-reinforcement`). First-party skill, maintained in this repository.

## Notes

- Gain before EQ: no amount of EQ rescues a clipped converter.
- Document the patch — the next engineer should not have to reverse-engineer it.
- Pairs with: `audio-mixing-mastering`, `music-production-daw`.
