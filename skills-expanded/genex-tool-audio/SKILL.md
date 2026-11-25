# Genex audio in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's audio card,
with the passages of advice Studio does not ship taken out. Where it disagrees with this preface,
this preface wins.

- Run every command through `genex__asset`, never `npx genex`. `npx genex sfx "<sound>"
  --duration 3` is `genex__asset {"operation":"sfx","prompt":"<sound>","options":
  {"duration":3}}`; `music` takes `duration`, and `voice` takes `voice` or `voice-id`.
- Give every sound effect a `duration` when its length matters: left out, the model decides. An
  ambient bed the game repeats needs `"loop":true`.
- Studio submits every create without waiting and delivers the MP3 into the game: never pass
  `out-dir`, `no-wait` or `no-download`. Pick it up with operation `wait` and its generationId.
- The audio-context troubleshooting line is about browsers; it does not apply to an Unreal game.

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-tool-audio/SKILL.md v1.40.0 sha256 65c8630d34e1c9f8f668d2dbe088f7b2079e28187b57b5b706d12f6407504813 -->
---
name: genex-tool-audio
description: Generate game audio as mp3 files with `npx genex sfx` (sound effects — impacts, pickups, UI clicks, weapons, ambience), `npx genex music` (one looping instrumental track) and `npx genex voice` (a short spoken line from a cast of archetypes). Files download to ./assets and are yours to ship.
---

# Genex Tools · Audio

Three lanes, one file format (mp3), one destination (`./assets`).

## Sound effects

```bash
npx genex sfx "punchy laser zap"
npx genex sfx "heavy wooden door creaking open" --duration 3
```

`--duration <sec>` targets a clip length; leave it off and the model decides.
Generate each sound separately — one prompt, one sound, in the vendor's own
vocabulary where it fits ("impact", "whoosh", "ambience", "drone"); a sequence
is written in order ("footsteps on gravel, then a metal door opens"). For an
ambient bed the game plays on repeat, add `--loop`: the clip is generated to
close on itself, so it wraps without a pop.

## Music

```bash
npx genex music "battle loop, seamless, no intro or outro"
npx genex music "sparse ambient synth pads" --duration 120
```

ONE looping instrumental track is the shape this lane is built for.
`--duration` is 10–300 seconds, default 90. Say "seamless loop, no intro or
outro" in the prompt — a track that opens with a flourish is unusable on repeat.


## Voice

```bash
npx genex voice "You shall not pass!" --voice gruff
npx genex voice "Systems nominal." --voice-id <raw-voice-id>
```

- `--voice <archetype>` — `narrator` (default), `heroine`, `gruff`, `elder`, `robot`, `imp`.
- `--voice-id <id>` — any raw provider voice id, past the curated cast.

Billed per submitted character and hard-capped at 1000, so split longer copy
into separate lines.

## Shared options

`--out-dir <dir>` (default `./assets`) · `--no-download` (URL only) ·
`--no-wait` (enqueue, pick up with `npx genex wait <id>`).

## Cost

From **2 credits** an sfx · **27** a 90 s music track · **2** a short voice line
(voice bills per character, up to 12 at the 1000-character cap; 1 credit = $0.01).
Longer `--duration`s cost more. Live prices and your balance: `npx genex doctor`.

## Waiting

`--no-wait` returns an id. `npx genex wait <id>` picks it up and never bills;
**re-running a generate command bills a new asset.**

## Troubleshooting

- **Audio does not play on the first click** — nearly always the audio context, not the file: browsers require it to be created inside a real user gesture, and a sound fired before it exists is lost rather than queued. Create it on the first click or key press, then re-trigger whatever track was already selected.
- **Out of credits** — Studio keeps the generation's card, which says so and offers Get credits. Never relay the balance, price or refill date, and don't retry.
- **Anything else** — `npx genex doctor` reports whether the audio lanes are live on this account.
