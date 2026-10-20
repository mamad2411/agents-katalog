---
name: lyrics-and-theory-bridge
description: Bridges lyric writing with music theory concepts — helps composer-lyricists align words with chord function, melody contour, rhythm, and song structure.
category: media
tags: [media, music, lyrics, theory, composition, songwriting, hip-hop]
agents: [opencode, freebuff, antigravity, codex]
---

# lyrics-and-theory-bridge

## Purpose

Connect the lyric-writing process with practical music theory so that words, melody, harmony, and rhythm reinforce each other. Designed for hip-hop, underground, and experimental contexts where the relationship between lyrical cadence, flow pattern, and harmonic backdrop is central to the work.

## Invocation

**OpenCode / Codex:** `Invoke lyrics-and-theory-bridge`
**Freebuff:** `/skill lyrics-and-theory-bridge`

## Workflow Steps

1. **Ingest:** Accept the current lyric draft, chord progression, beat, or melody sketch.
2. **Analyse prosody:** Map syllable stress patterns to the beat grid; identify rhythmic tension and resolution.
3. **Analyse harmony:** Identify chord function (tonic, subdominant, dominant, borrowed); note how lyric emotional intent aligns or contrasts with harmonic colour.
4. **Melodic contour:** Map pitch contour suggestion to lyric phrasing — does the melody rise on stressed syllables? Does the hook sit in the voice's sweet spot?
5. **Flow mapping:** For rap/hip-hop: map multisyllabic rhyme schemes, internal rhymes, and cadence against the bar grid.
6. **Propose:** Suggest targeted edits — a word swap to fix a stressed syllable, a chord substitution to deepen an emotional moment, a structural change (pre-chorus, bridge) to add arc.
7. **Save:** Write analysis and suggestions to `music-project-planner` active project note or `obsidian-music-journal`.

## Theory Reference Points

- **Chord function:** I (tonic/resolution), IV (subdominant/yearning), V (dominant/tension), vi (relative minor/introspection), ♭VII (Mixolydian lift)
- **Rhyme density:** End rhyme, internal rhyme, multisyllabic rhyme, near rhyme, slant rhyme
- **Flow grid:** On-beat, off-beat, triplet feel, polyrhythm over 4/4 or 3/4
- **Song sections:** Intro, verse, pre-chorus, chorus, bridge, outro — each with distinct melodic and lyrical register
- **Cadences:** Perfect authentic (V→I), plagal (IV→I), half (→V), deceptive (V→vi)

## Inputs

- Lyric draft (full or partial) as plain text
- Chord progression (Nashville Number, Roman numeral, or chord names)
- Optional: beat file reference, BPM, time signature, key, and genre context
- Optional: specific problem to solve (flow feels off, hook doesn't land, bridge lacks contrast)

## Outputs

- Prosody analysis: syllable stress map against bar grid
- Harmonic analysis: chord function labels and emotional commentary
- Targeted edit suggestions: word-level, line-level, and structural
- Optional: alternative chord progression suggestions that serve the lyric intent better
- Analysis note saved to active `music-project-planner` or `obsidian-music-journal` entry

## Safety

- Suggest only; never overwrite or delete the user's lyric draft.
- Preserve the user's voice and style — do not homogenise toward generic pop phrasing.
- Flag when a suggestion would change the meaning of a lyric, not just the sound.

## Failure Modes

- Chord progression not provided — request it or proceed with prosody-only analysis.
- Lyric too early/fragmentary for full analysis — offer partial feedback on rhythm and rhyme density only.
- Genre context missing — ask before applying genre-specific conventions (e.g., do not assume 4/4 trap hi-hat grid for jazz-influenced material).

## References

- [MusicTheory.net](https://www.musictheory.net/)
- [Adam Neely YouTube — music theory for contemporary genres](https://www.youtube.com/@AdamNeely)
- [Rhymezone rhyme and near-rhyme lookup](https://www.rhymezone.com/)
- [Hooktheory chord analysis](https://www.hooktheory.com/)
- [Princeton Companion to Hip-Hop — flow and meter](https://press.princeton.edu/)

## Companion Skills

- `music-project-planner` — active project context and note storage
- `obsidian-music-journal` — stores analysis and session notes
- `dj-set-architect` — harmonic context for DJ transitions
- `dj-library-curator` — source of tracks referenced in harmonic analysis
