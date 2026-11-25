---
name: score
description: Use when a short film, demo reel or product video needs sound - an original soundtrack written in code and cut to the film's timeline, or a prompt for any music generator (ElevenLabs Music, Suno, Udio, Stable Audio, Lyria...) written from that timeline and the film's mood, then fitted to the cut, sound effects on clicks and cuts (a bundled public-domain kit, a kit made in code, or prompts for any sound-effect generator), a clear mix at a known loudness, or a trailer voiceover (ElevenLabs or similar) laid over a finished video. Also use when music fights the picture, the mix is muddy or bass-heavy, the level drops after a cut, or a voiceover has to be added fast with a limited ffmpeg.
---

# score

Every film gets its own music, cut against the same timeline as the picture. Two ways, same mix and effects after:

- **A. The code band** (`score.py`): written in code, nothing to sign up for, nothing licensed from anyone, hits on
  the cuts by construction. The default, and what works for everyone.
- **B. A produced song** from whatever music generator the person has: `song_prompt.py` writes the prompt from the
  timeline and the mood, `song_fit.py` measures the song and fits the cut to its beats. Better music; ask first if a
  tool is available, and never assume one.

## A. The code band (`assets/score.py`)

```bash
python assets/score.py score.json --out public/audio/soundtrack.wav
```

`score.json` (see `examples/demo/score.json`):

| Key | Meaning |
|---|---|
| `total` | film length, seconds |
| `key`, `mode`, `bpm` | e.g. `"D"`, `"lydian"`, `120` (ionian, dorian, phrygian, lydian, mixolydian, aeolian) |
| `palette` | the riff's voice: `lyre` (plucked), `keys` (FM piano), `marimba`, `glass` (bells) |
| `progression` | chord roots as scale degrees, one per bar, e.g. `[0, 4, 5, 3]` |
| `sections` | `{from, to, energy}`; energy 0 pad only, 1 + riff, 2 + bass and light kit, 3 + full kit and lead |
| `hits` | big drums on cuts; `[time, gain]` for a softer one (keep intro hits under the payoff) |
| `stops` | a 0.2 s silence then a hit: put one right before the match cut or the biggest reveal |
| `risers` | `{to, dur}`: a rising sweep into a moment |
| `end` | the end card time: a hit, and without `finale` the resolve chord rings out from here |
| `finale` | optional: the band plays on under the end card and the last chord lands here, with a short ring-out (a film should end on a hit, not a long fade) |
| `fade`, `seed`, `fx_gain` | the final fade in seconds (1.2); the random seed; the level of every effect (raise it over a dense song) |
| `track`, `track_at`, `track_from`, `track_gain` | optional: a produced song instead of the code band (any file ffmpeg reads), placed at `track_at` s of the film from `track_from` s into the song, shaped by `track_curve` (`[[s, dB], ...]`, e.g. lift a quiet outro under the end card); the sections, hits and risers are then ignored and the effects mix on top; a missing file falls back to the code band |
| `fx` | recorded effects `{file, t, gain}` relative to score.json |

Pick a new key, tempo and palette for every film and keep a list of what earlier films used. A tempo whose bar
divides the film's sections makes the cut easy (120 BPM: 2 s bars; 96 BPM: 2.5 s bars). Shape it to the picture:
sparse under an intro, a stop before the match cut, the band on the product, a break for the payoff, the
band under the end card and a last chord that lands. Never cut the song short; let the end resolve. Then measure it
(below).

## B. A produced song (`assets/song_prompt.py`, `assets/song_fit.py`)

```bash
python assets/song_prompt.py film/src/tl.json --mood epic-tech [--breath 24.6-27.5] [--tool suno] [--out song-prompt.md]
# generate two takes in the person's tool, save them, then:
python assets/song_fit.py song.mp3 --tl film/src/tl.json
```

1. **Ask the mood in the person's words** and pick a preset or pass their words straight through: `epic-tech`,
   `calm-premium`, `bright-playful`, `warm-human`, `dark-intense`, `lofi-focus`, `luxury-sleek`, `retro-synth`,
   `orchestral-hero`. Match the product and the platform: a developer tool reads as `epic-tech` or `calm-premium`,
   a consumer app as `bright-playful` or `warm-human`, a finance or luxury product as `luxury-sleek`.
2. **The prompt carries the film's arc in seconds**, read from `tl.json`: a quiet build under the intro, an entrance
   when the product appears, a rise into the biggest moment (`"moment"` in `tl.json`, or the loudest hit), the full
   section, an optional breath, a last hit on the end card, a short ring-out. Electronic and trailer styles build to
   a drop; everything else swells. It prints one prompt per tool shape: a paragraph (ElevenLabs Music, Lyria,
   Beatoven, Soundraw, Mubert), section tags (Suno, Udio), a short style line with a set duration (Stable Audio),
   and a timed section plan for tools with an API that takes one.
3. **Generate two takes** and let the person choose by ear.
4. **Fit the cut to the song, never the song to the cut.** Models only roughly follow times. `song_fit.py` measures
   the tempo, beat grid, bar lines and strongest hits, puts the biggest moment on the nearest bar line (or `--at` to
   check a placement you chose, such as a strong pickup just before the bar), and lists every cut, the intro beats
   and the end card against the nearest beat. The heroes (`tl.json` `heroes`, 3 to 5 moments) must land: on a beat,
   or on the "and" between two as a pickup; move any marked MOVE IT. Every other cut is free. Leave it where the
   picture wants it, on a beat or clearly off one, and nudge only a near miss (0.06 to 0.12 s off), which reads as a
   slip. Then set `track` and `track_at` in `score.json`, run `cues.py` and `score.py` as usual, and measure the mix.
5. **Licence.** Keep the song out of public repos, and check the person's plan allows the use they have in mind
   (some free tiers are non-commercial or need a credit).

## Effects (`assets/cues.py`, `assets/kit`, `assets/make_kit.py`, `assets/sfx_prompts.py`)

Placed by the picture's own events, and included: every film has its effects out of the box.

```bash
python assets/cues.py film/src/tl.json film/public/scenes --into score.json          # the bundled kit
python assets/cues.py film/src/tl.json film/public/scenes kit/ --into score.json     # your kit first, bundled fills gaps
```

It maps every press and keystroke in the takes into film time and lays a click or key on each, a whoosh into every
cut, a hit on the match cut, a tick as each caption lands and a land on the end card. Sounds the takes cannot show
(a lock, a launch, a download finishing) go in `tl.json` `sfx` as `{"t", "role", "gain"}` and land with the rest.
The demo film uses 43 cues.

- **Heroes get two layers.** On each hero moment the hit (or land) is the punch and a `tail` under it is the bloom:
  air and a soft glassy ring that hangs about 1.5 s. Only heroes get a tail and only hits carry sub, so the 3 to 5
  moments that matter sound bigger than everything else without the mix getting louder.
- **Nothing plays the same way twice.** Clicks, keys, ticks and short whooshes take a different file than last time,
  a few percent of pitch and up to 1.5 dB of level (`"pitch"` in each cue; `score.py` plays it), seeded with
  `--seed` so a re-run gives the same mix. `cues.py` ends by naming any file heard more than 4 times in 30 s: make
  more takes of that role.
- **Every sound lands on its frame.** Recordings often open on a breath of room noise (some bundled clicks carry
  50 to 160 ms of it). `score.py` starts each effect 3 ms before its attack, so a click is heard on the press, not
  a tenth of a second after it. Whooshes keep their lead: they are built to swell into the cut.

Three ways to the sounds, all named by role (`click_1.wav`, `key_4.wav`, `whoosh-short_2.wav`, `hit_1.wav`,
`tail_1.wav`, `land_1.wav`, `tick-crisp_1.wav`):

- **The bundled kit** (`assets/kit`, the default): public-domain recordings for clicks, keys, ticks and lands, and
  whooshes, hits and tails made in code, levelled to sit right at the gains `cues.py` uses. Nothing to download.
- **Made in code** (`make_kit.py kit/`): the whole kit synthesized, for a different character or a seed of its own.
  Whooshes and hits read as the real thing; keys and lands are thinner than recordings.
- **From a sound-effect generator** (`sfx_prompts.py --style cinematic --tl film/src/tl.json --out kit-prompts.md`):
  one prompt per role in the film's style (`clean-tech`, `warm`, `cinematic`, `playful` or your own words), with
  the length, the number of takes and the file names. Works with any text-to-sound tool. Save into `kit/`.

Whooshes peak where the cut is: `cues.py` lays a short one 0.18 s and a long one 0.9 s before it, so a whoosh you
make or generate must be loudest at that point. Check the result against the picture before delivering.

## The mix

- `score.py` levels to -18 dB RMS by default (`rms_db` in score.json) under a -1.5 dBFS ceiling, which lands near
  -14 LUFS, then measures itself: integrated loudness, true peak, and the **peak-to-loudness ratio**. That ratio is
  the room the hits have above the mix. Aim for 12 to 16 dB. Under 12 the ceiling is eating the hits: lower
  `rms_db` (it says by how much) and they come back. Over 16 is a quiet, open mix, fine for a calm film. Louder is
  not better: platforms turn a loud film down to their level anyway, and a squashed one stays squashed. -14 LUFS is
  the loud end of the range, not a target to push to. Check it independently with
  `ffmpeg -af ebur128=peak=true`.
- You cannot hear it: measure. RMS per section, the level either side of every cut (a drop of several dB after the
  match cut means the band came in too thin), and the low end below 120 Hz against the mids. Say that you measured,
  not listened. Use a listening tool if one is available.
- **Measure the render** before it goes out, the way a reference is measured:
  `python assets/measure.py out/film.mp4 --tl src/tl.json` (or the soundtrack wav before a render). It prints the
  pace (cuts per 10 s; brand launch films mostly sit at 0.5 to 4), loudness and true peak, the headroom, each hero
  against the nearest sound that starts there (more than a frame and a half off is a lost hit), and the share of
  cuts on a sound against what random cuts would score. Heroes landing is the rule; the share of the rest can sit
  near chance.

## Voiceover (`assets/voiceover_mix.py`)

1. Few words. A trailer open: "In a world where agents do all the work... nobody keeps score." Then "Until now."
   just before the match cut. Never narrate what a caption already says.
2. Generate with a deep trailer voice (ElevenLabs: a "movie trailer" library voice, a v3 or newer model with audio
   tags such as `[deep, slow, epic movie trailer]` and `...` for pauses). One take per line saves time.
3. Find the gaps between phrases (`ffmpeg -af silencedetect=n=-35dB:d=0.3`), then place each phrase:

```bash
python assets/voiceover_mix.py film.mp4 "film VO.mp4" vo.mp3:0-6.4@1.0 vo.mp3:6.9-8.7@15.9
```

It decodes with any ffmpeg (`FFMPEG` to pick one), mixes in numpy with a gentle duck under the voice, and copies
the picture untouched. Write next to the original, never over it.
