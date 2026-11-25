---
name: sound-studio
description: Songs, karaoke, mixtapes, music boxes and soundscapes without any paid service. Emotion and interaction first, writing melody and lyrics, the score JSON format, the karaoke player (lyrics highlighted in time with score.json, mute), cassette and music-box objects to touch, the Web Audio synth and player in kit/sound, WAV export, the optional robot rendition, ambient mixers, the share frame, and the render-it-yourself sheet every song gift includes.
license: MIT
---

# Sound Studio

You write the music; the browser plays it. No provider, no key, no upload. A song gift is a score, a **karaoke player** that highlights the lyrics in time with it, a WAV rendered from it, and a sheet the person can paste into any music generator they like.

Read `gift-director` first. A song is not an audio file with a play button: it is an object to touch (a cassette whose tape you scrub, a music box whose crank you turn, a karaoke screen whose words light up), with one clear `emotion` (`funny` and `ridiculous` songs are often the most shared; a lullaby for their cat is `cute`), and a share frame people can see without hearing it.

## Forms

| Form | Scope | Kit |
|---|---|---|
| Music box | 16–32 bars, one melody voice plus a soft bass, loops | `synth.js` (`musicbox`), `score.js`, `player.js`, `wav.js` |
| Karaoke song | Verse/chorus, 2–4 voices (pluck or pad, bass, light drums), lyrics aligned to notes and highlighted word by word | all of `kit/sound`, `kit/sound/karaoke.js` when present, `sing.js` optional |
| Mixtape | A cassette with 3–6 short tracks and fake liner notes; scrub the tape, flip to Side B | `kit/sound/cassette.js` when present, `score.js`, `synth.js` |
| Jingle / theme | 4–8 bars that stick; used in a game or card | `synth.js`, `score.js` |
| Soundscape | Rain, fire, wind, snow mixed under a short loop or alone, with sliders | `ambient.js`, `player.js` |

## Writing the music

- Pick a key and a mode for the mood: major for warm, Dorian or Aeolian for wistful, Lydian for wonder. Tempo 60–90 for lullaby and music box, 100–128 for cheerful.
- Melody first. Mostly steps, one leap per phrase, a clear high point, rests. 8-bar phrases, AABA or verse/chorus.
- Harmony: a 4-chord loop is fine (I–V–vi–IV, vi–IV–I–V, I–vi–ii–V). Bass plays roots on beats 1 and 3.
- Rhythm: keep the melody's rhythm singable; drums light (kick on 1 and 3, hat on eighths, snare on 2 and 4 or none).
- Lyrics: short lines, one syllable per note where possible, concrete images from the brief; chorus repeats exactly; avoid words from `dislikes`/`avoid`. No invented personal facts.
- Length: 60–120 seconds. A loop that repeats cleanly beats a long piece that wanders.

## The score format

`kit/sound/score.js` defines and validates it (full spec in `references/score-format.md`):

```json
{
  "tempo": 84, "key": "G major", "timeSignature": "3/4",
  "tracks": [
    { "voice": "musicbox", "notes": [ { "t": 0, "p": 67, "d": 1, "v": 0.8 }, { "t": 1, "p": 71, "d": 1, "v": 0.7 } ],
      "lyrics": [ { "t": 0, "text": "Snow" }, { "t": 1, "text": "falls" } ] },
    { "voice": "bass", "notes": [ { "t": 0, "p": 43, "d": 3, "v": 0.6 } ] }
  ]
}
```

`t` and `d` are in beats, `p` is MIDI pitch (60 = middle C), `v` is 0–1. Voices: `musicbox`, `pad`, `pluck`, `bass`, `kick`, `snare`, `hat` (drums ignore `p`). Call `validate(score)` and fix every error before packaging; the gate checks `tracks` and `tempo` (`score_tracks`, `score_tempo`).

## Playing it

- `synth.js`: `createSynth()` lazily creates the AudioContext on first user gesture; `play(voice, midi, when, dur, vel)`. ADSR per voice, master gain, `mute()`.
- `score.js`: `schedule(score, cb)` hands you every note with absolute seconds; `totalBeats(score)` for the progress bar.
- `player.js`: `createPlayer(container, { score, synth })` renders Play/Pause/Stop, progress, time, a lyrics line and keyboard handling (Space, Home). **No autoplay**: nothing sounds before a click or key.
- `sing.js`: optional. Speaks the lyrics with `speechSynthesis` at the right moments, pitched roughly along the melody. Feature-detected; labelled in the UI as **"Robot rendition"** so nobody mistakes it for singing. Off by default, a toggle turns it on.
- `ambient.js`: procedural rain, fire, wind, snow from filtered noise with per-layer sliders; a soundscape gift is a mixer with a preset and a "Play" button.

## The karaoke player (required for songs)

Every song gift shows its lyrics **in time with the music**, driven by the `lyrics[]` beats in `score.json`, not by a separate timing list you could get wrong.

- Use `kit/sound/karaoke.js` when present. Otherwise build it from `score.js`: `schedule()` for the notes, `lyricsAt(score, beat)` each animation frame, the current word highlighted, the current line large, the next line dimmed below.
- Controls: Play/Pause, restart, **mute** (always visible), and a progress bar. Keyboard: Space plays and pauses, M mutes, Home restarts. Nothing sounds before a click or key.
- Under reduced motion, highlight by colour change only; no bouncing ball.
- Lines with names or places get `data-advent-private`.
- The share frame is the karaoke screen on the chorus line, with the title: expose `window.adventCapture.prepare(kind)` that seeks to the chorus beat, renders the highlighted line and hides the controls, **without playing sound**. For a loop, animate the highlight silently for `durationMs`.

## WAV export (required for songs)

`wav.js`: `renderScore(score, synthFactory)` renders through `OfflineAudioContext` and `encodeWav(buffer)` returns a 16-bit PCM Blob. In launched mode, if you cannot run a browser, use the kit's Node-friendly path: `kit/sound/wav.js` also exports `synthesizeScoreToWav(score)`, a pure-JS renderer with simple sine/triangle voices, so `song.wav` can be written with Node. The gate decodes it (`wav_invalid`).

## The render-it-yourself sheet (required for songs)

`render-it-yourself.md`, shown as a card with copy buttons. Contents, in this order:

1. Title, one-line description.
2. Full lyrics with section labels (`[Verse 1]`, `[Chorus]`, …).
3. Style tags (genre, instruments, era), tempo, key, mood, vocal description (e.g. "warm alto, close-miked, slight smile").
4. **Ready-to-paste prompt** (one paragraph) for any text-to-music tool, and a **short variant** (under 200 characters).
5. A line: "Paste this into the music generator of your choice to hear a full production. The version in the gift is the music-box original."

List it in `downloads` too (`{ "label": "Render it yourself", "file": "assets/render-it-yourself.md" }`), next to the WAV.

**Name no provider.** Not in the sheet, not in the note, not in the UI. The sheet is `references/render-sheet.md` as a skeleton.

## Packaging

```json
"schema": "advent-agent/gift@2",
"family": "sound", "emotion": "ridiculous", "interaction": ["play", "sing along"], "form": "interactive-html", "tierUsed": "S",
"entry": "index.html",
"song": { "score": "assets/score.json", "renderSheet": "assets/render-it-yourself.md", "wav": "assets/song.wav" },
"share": { "still": { "capture": "still" }, "loop": { "capture": "loop", "durationMs": 8000 }, "caption": "My Secret Santa wrote a power ballad about my sourdough starter" },
"downloads": [
  { "label": "Music-box version (WAV)", "file": "assets/song.wav" },
  { "label": "Render it yourself", "file": "assets/render-it-yourself.md" }
]
```

`entry: index.html` with the karaoke player. Without a render sheet the gate flags `render_sheet_missing`. Jingles inside a game need no sheet; only a gift *about* a song does. Audio never plays during capture: the calendar records a silent loop.

## Self-check

Play it through once in your head bar by bar. Check that the melody ends on the tonic or a satisfying note, lyrics syllables match notes, the karaoke highlight lands on each word as it sounds, mute works, no note is outside the voice's comfortable range (musicbox 60–96, bass 36–55), WAV decodes, the player works with the keyboard, nothing autoplays, and the sheet names no provider.
