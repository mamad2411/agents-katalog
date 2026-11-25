---
name: music-notation-engraving
description: "Engrave readable scores: notation entry, layout spacing, parts extraction, transposition and MusicXML interchange for MuseScore and LilyPond."
type: procedural
category: audio
domain: audio
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - engrave a score
  - musescore part extraction
  - lilypond formatting
  - musicxml import export
  - transpose score for instrument
aliases:
  - score-engraving
  - musescore
keywords:
  - notation
  - score
  - musescore
  - lilypond
  - musicxml
  - engraving
  - transposition
mcp_servers:
  - filesystem
source: custom
enabled: true
---

# Music Notation and Engraving

## Purpose

Engrave readable scores: notation entry, layout spacing, parts extraction, transposition and MusicXML interchange for MuseScore and LilyPond.

## When to Use

- Handwritten or MIDI material must become a legible score or set of parts.
- Players need transposed parts and correct page turns.
- A publisher requires a specific house style.

## When NOT to Use

- The deliverable is audio only; that is production, not engraving.
- A single lead sheet in a DAW piano roll suffices.
- The material is a chord chart with no rhythmic notation.

## Capabilities

- Enter and correct notes, rhythms, ties and voices reliably.
- Control spacing, beaming, slurs and page layout for readability.
- Extract and transpose instrumental parts with correct clefs.
- Round-trip MusicXML without semantic loss.

## Inputs

- The source: manuscript scans, MIDI, MusicXML or a chord chart.
- Instrumentation, transpositions and the range constraints per part.
- House style: page size, font, bar numbering, rehearsal marks.

## Workflow

1. Import the source and fix pitch/rhythm before touching layout.
2. Set the score style once (fonts, staff size, spacing) and apply it globally.
3. Resolve enharmonics and transpositions per instrument, not globally.
4. Engrave slurs, articulations and dynamics where they read, not where they were played.
5. Extract parts, set page turns, and proof each part from a player's perspective.
6. Export PDF for print and MusicXML for interchange; keep the editable master.

## Tools

- musescore
- lilypond
- music21
- verovio

## Examples

- ``mscore -o out.pdf score.mscz` renders headless so engraving can sit in CI alongside the build.`
- `Transposing parts are derived from concert pitch, never typed twice.`

## Safety

- Never hand-edit a rendered PDF; regenerate from the master.
- Check copyright status before engraving or distributing a work.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/audio/music-notation-engraving`). First-party skill, maintained in this repository.

## Notes

- MIDI import always needs rhythmic quantisation decisions — verify against the recording.
- Page turns are a musical decision: place rests, not mid-phrase breaks.
- Pairs with: `music-production-daw`, `podcast-production`.
