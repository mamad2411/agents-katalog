---
name: ai-music-generation
description: >
  Generate music with Google's Lyria models through the Gemini API - instrumental beds, loops,
  soundtracks and game audio with Lyria RealTime (weighted prompt blending, BPM, key/scale,
  density, brightness, temperature, QUALITY/DIVERSITY/VOCALIZATION mode) rendered to a 48 kHz
  stereo WAV by scripts/lyria.py, and full songs with vocals and lyrics with Lyria 3.5 / Lyria 3 Clip.
  Asks vocals-vs-instrumental first and is honest that Suno and Udio have no public API. Use when
  the user says "generate music", "make a beat", "create a song", "compose a soundtrack",
  "background music for my video", "lo-fi beats", "jingle", "intro music", "game music loop",
  "instrumental track", "song with lyrics", or names Lyria, Suno or Udio.
---

# AI Music Generation

Google's Lyria family has a public, self-serve API (unlike Suno and Udio), and one `GEMINI_API_KEY` covers both of its shapes: **Lyria RealTime** (streaming, instrumental,
steerable) and **Lyria 3.5** (request/response, full songs with vocals). Pick the shape from the
one question that matters most, then write a prompt the model can actually steer on.

## Step 1: Ask first - vocals or instrumental?

This single answer picks the model. Ask it before anything else.

| Need | Use | Why |
|---|---|---|
| Instrumental bed, loop, soundtrack, game/ambient audio, exact BPM/key | **Lyria RealTime** via `scripts/lyria.py` | Streams any length, numeric control over tempo/key/density/brightness |
| Song with sung lyrics / a vocalist | **Lyria 3.5** (`lyria-3.5`) | Generates vocals and timed lyrics; can take your lyrics |
| Quick 30 s draft of a song idea | **Lyria 3 Clip** (`lyria-3-clip-preview`) | Fixed 30 s; iterate here before a full 3.5 render |
| Wordless "oohs"/vocal texture inside an instrumental | Lyria RealTime, `--mode VOCALIZATION` | Vocal sounds as an instrument, no lyrics |
| "Use Suno" / "use Udio" | Neither has a public API - see below | |

**Suno and Udio have no public developer API** (checked 2026-09-26). Suno only announced an
invite-only partner-API intake in July 2026 with no self-serve keys; Udio's help centre states it
does not offer a public API. The many "Suno API" sites are unofficial third-party wrappers around
the consumer app - do not wire one in on your own initiative. If the user wants those models,
they generate in their own Suno/Udio account and hand you the file; otherwise use Lyria 3.5 or
another provider the user names that has real, documented API access.

Then gather the rest (one question at a time if not given): purpose/where it will play, length,
genre + mood, tempo or energy, key if it must match other material, anything to avoid.

## Step 2: Write the prompt

Lyria steers on short descriptive tags. Keep genre, instrument and mood as **separate** tags -
in RealTime each becomes its own weighted prompt you can raise or lower independently.

| Layer | Examples (from Google's Lyria prompt guide) |
|---|---|
| Genre | Lo-Fi Hip Hop, Minimal Techno, Deep House, Drum & Bass, Synthpop, Trip Hop, Boom-Bap, Neo-Soul, Jazz Fusion, Bossa Nova, Afrobeat, Indie Folk, Shoegaze, Surf Rock, Celtic Folk, Indian Classical, Orchestral Score, Piano Ballad, Baroque |
| Instruments | Rhodes Piano, Synth Pads, Moog Oscillations, Mellotron, 303 Acid Bass, TR-909 Drum Machine, 808 Hip Hop Beat, Precision Bass, Warm Acoustic Guitar, Slide Guitar, Cello, Viola Ensemble, Sitar, Tabla, Koto, Kalimba, Marimba, Vibraphone, Alto Saxophone, Trumpet |
| Mood | Chill, Dreamy, Ethereal, Euphoric, Groovy, Melancholic, Nostalgic, Ominous, Relaxed, Soulful, Triumphant, Upbeat, Whimsical, Dark, Bright |
| Production / feel | lo-fi tape saturation, vinyl crackle, dry close-miked, wide stereo, punchy drums, sparse arrangement, live performance, 8-bit (general craft tags - verify effect by ear) |

Describe a style rather than naming a real artist or copyrighted song; prompts are safety-filtered
and a filtered prompt is reported back (the script prints it as a warning).

**Songs (Lyria 3.5)**: one prose brief that gives genre, BPM, key, mood, instrumentation, vocal
description (e.g. "female soprano", "weathered male baritone") and structure as tagged sections
(`[Intro] [Verse 1] [Chorus] [Bridge] [Outro]`). Put user lyrics under a `Lyrics:` header with the
same section tags, kept apart from the musical instructions; parentheses mark backing vocals and
ad-libs. Lyrics come out in the language of the prompt. Add "Instrumental only, no vocals" to get
an instrumental from 3.5.

## Step 3: Lyria RealTime controls

All optional; omit a control to let the model decide. Ranges per Google's docs (2026-09-17).

| Control | Script flag | Range / values | Effect |
|---|---|---|---|
| Weighted prompts | `-p "text:weight"` (repeat) | any non-zero float; 1.0 is a good start | Blend influences; higher weight = stronger. A `:` inside the text is fine if the tail isn't a number |
| Tempo | `--bpm` | 60-200 | Beats per minute |
| Key | `--scale` | `C_MAJOR_A_MINOR` ... `B_MAJOR_A_FLAT_MINOR` (12 values, see `--help`) | Relative major/minor pair |
| Density | `--density` | 0.0-1.0 | Sparse to busy |
| Brightness | `--brightness` | 0.0-1.0 | Darker to brighter tone |
| Guidance | `--guidance` | 0.0-6.0 (default 4.0) | Prompt adherence; very high can make transitions abrupt |
| Temperature | `--temperature` | 0.0-3.0 (default 1.1) | Randomness |
| Top-k / seed | `--top-k`, `--seed` | 1-1000 (default 40) / int | Sampling; fix the seed to reproduce a take |
| Stems | `--mute-bass`, `--mute-drums`, `--only-bass-and-drums` | flags | Strip or isolate the rhythm section |
| Mode | `--mode` | `QUALITY` (default), `DIVERSITY`, `VOCALIZATION` | Polish vs variety; VOCALIZATION adds wordless vocals |

In an interactive session, changing `bpm` or `scale` only takes effect after `reset_context()`
(a hard cut); density, brightness and prompt weights morph smoothly. The script sets everything
once before `play()`, so this only matters if you extend it into a live controller.

## Step 4: Generate

### Instrumental - `scripts/lyria.py` (Lyria RealTime)

Needs `pip install -U google-genai` (a release with `client.aio.live.music`) and an API key from
https://aistudio.google.com/apikey in `GEMINI_API_KEY` or `GOOGLE_API_KEY`.

```bash
python scripts/lyria.py -p "lo-fi hip hop:1.0" -p "rhodes piano:0.6" -p "nostalgic, relaxed:0.4" \
  --bpm 80 --scale F_MAJOR_D_MINOR -d 60 -o study-bed.wav
python scripts/lyria.py -p "minimal techno" -p "303 acid bass:0.7" --bpm 124 --density 0.6 -d 30 -o loop.wav
python scripts/lyria.py -p "orchestral score:1.0" -p "triumphant" --dry-run   # check args, no API call
```

It opens a session on `models/lyria-realtime-exp` (API version `v1beta`), sends the prompts and
config, plays, collects PCM chunks until `--duration` seconds are buffered, stops, and writes the
trimmed audio as a 16-bit PCM WAV. `--model` / `--api-version` override the defaults if Google
renames the experimental model - verify against current docs if the connect call fails.
Generation runs at roughly real time, so a 60 s clip takes about a minute.

### Songs with vocals - Lyria 3.5 (Interactions API)

No script ships for this yet; the call is small. Shape per Google's docs as of 2026-09-23 -
verify against current docs before relying on field names:

```python
import base64
from google import genai

client = genai.Client()  # reads GEMINI_API_KEY / GOOGLE_API_KEY
interaction = client.interactions.create(model="lyria-3.5", input=brief)  # or "lyria-3-clip-preview"
if interaction.output_audio:
    open("song.mp3", "wb").write(base64.b64decode(interaction.output_audio.data))
print(interaction.output_text or "")  # the generated/used lyrics
```

Lyria 3.5 runs "a couple of minutes" (steer length in the prompt), accepts up to 10 reference
images, and returns MP3 at 44.1 kHz stereo by default (WAV is selectable). Lyria 3 Clip is fixed
at 30 s. Multi-turn editing of a generated song is not supported - regenerate with a revised brief.

## Step 5: Deliver

- **Output**: RealTime -> WAV, 48 kHz, stereo, 16-bit PCM. Lyria 3.5 -> MP3 44.1 kHz stereo (default).
- **Watermark**: all Lyria output carries an inaudible SynthID watermark - tell the user if the
  track is going somewhere that matters (client work, distribution).
- Report: model used, prompts + weights, BPM/key, seed (if set), duration, file path. Offer one or
  two concrete next moves (raise a weight, change density, swap mode) rather than a blind re-roll.

## Hand-off - scoring a video

When the music is for a video, generate to the video's exact length (or a little longer and fade),
pick BPM to match the cut pace, and keep density low under voiceover. Then hand the WAV to
`content/video-production-pipeline` (its Step 5 "music" asset): it mixes voice over music with
ducking (`audio_mix`, music volume 0.2-0.4) and attaches the result with `video_audio_merge`.
For narration itself use `content/text-to-speech-voice-synthesis`.

## Gotchas

- Lyria RealTime is **experimental** and **instrumental only**; model id and API version have
  changed before (earlier docs used `v1alpha`) - check the RealTime page if calls start failing.
- Weight `0` is rejected; to drop an influence, remove the prompt.
- `--only-bass-and-drums` contradicts `--mute-bass` / `--mute-drums`; the script refuses the combo.
- An empty or short file means the prompt was filtered or the stream closed early - the script
  says which; rephrase descriptively and retry.

Sources: https://ai.google.dev/gemini-api/docs/realtime-music-generation ,
https://ai.google.dev/gemini-api/docs/music-generation ,
https://ai.google.dev/gemini-api/docs/lyria-prompt-guide
