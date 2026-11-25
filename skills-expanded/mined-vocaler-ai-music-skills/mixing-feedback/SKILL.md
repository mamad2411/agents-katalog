---
name: mixing-feedback
description: "Gives structured mix feedback and fixes: balance, EQ, compression, low end, vocals, stereo, depth and loudness, from a description, a screenshot of meters or a spectrum, or analysis output. Use when the user asks for mix feedback, says their mix sounds muddy, harsh, thin, quiet or amateur, or asks for loudness targets."
license: MIT
metadata:
  author: Vocaler
  version: "1.3.0"
  category: music-production
  homepage: https://skills.vocaler.ai/mixing-feedback/
  repository: https://github.com/Vocaler-AI/music-skills
---

# Mixing Feedback

Gives clear mix notes with fixes: muddy low end, harsh highs, buried vocals and loudness targets, with settings to try.

## When to use

- The user describes how their mix sounds wrong.
- The user shares a spectrum, meter readings or a mix screenshot.
- Loudness questions for streaming.

## What to look for in the request

- Genre and reference (described).
- The complaint in the user's words.
- Any data: LUFS, true peak, spectrum image, DAW and plugins.

Do not interview the user. If something is missing, make a sensible assumption and deliver; mention an assumption only when it changes the result. Ask only when the answer would change the result completely.

Lead with the deliverable and skip closing notes that only restate it. Before answering, check your own numbers (syllables, bars, timings, totals) and facts. Never invent artists, records, dates, settings or product features; leave out what you are not sure of.

Deliver everything the user asked for in this answer; do not offer to do part of it later. Follow explicit requests exactly (named attributes, counts, limits). Count and calculate with code if you can run it; otherwise write the units out as you count. Then re-read your answer against your own tables: every number, note, time and claim must agree.

## Workflow

1. Translate the complaint into a technical cause (muddy = buildup 200-500 Hz; harsh = 2-5 kHz; boomy = 80-200 Hz; thin = lacking 100-250 Hz; buried vocal = level or masking).
2. Work in order: balance, low end, vocal, EQ, dynamics, space, stereo, loudness.
3. For each note: the problem, the likely cause, a fix with starting settings, and how to check it.
4. Give loudness guidance for the genre (see Rules), noting that streaming services normalise playback (Spotify and YouTube around -14 LUFS).
5. If you cannot hear the audio, say your notes are hypotheses based on the description.

## Rules

- Starting values, not rules: give ranges and tell the user to trust ears and references.
- Prioritise: three notes that matter beat fifteen.
- In genres built on sub-bass (trap, drill, EDM, hip-hop), do not high-pass the kick or 808 low end. Solve kick-808 clashes by arrangement (they take turns), tuning the 808 to the key, and sidechain or dynamic EQ on the 808 keyed from the kick.
- Judge loudness against the genre: loud genres commonly master around -10 to -6 LUFS integrated, acoustic and classical far lower. Platforms turn loud masters down; that only costs something if the master is over-compressed. Keep true peak below -1 dBTP.
- Separate symptoms by cause: a mix that is muddy only on some speakers is a translation problem (low mids, mono low end, monitoring), not a loudness problem.

## Output format

```markdown
**Top 3 issues**
1. Problem · cause · fix (settings) · how to check
**Loudness:** ...
**Next pass:** ...
```

## Example

**Request:** My mix is muddy and the vocal is lost.

**Response (abridged):**

```
1) Low-mid buildup: high-pass everything but kick and bass at 100-150 Hz; cut 2-4 dB around 300 Hz on pads and guitars. 2) Vocal masking: cut 2-3 dB at 2-4 kHz on guitars, sidechain or dynamic EQ keyed from the vocal.
```

## Works well with

- `release-checklist` for getting ready to release

Suggest one of these only when the user's next step needs it.
