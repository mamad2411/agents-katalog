---
name: video-pipeline
description: >-
  House pattern for producing videos with code, from a brief to a file ready to
  post: beats, script, voice with word timings, word-level captions, picture as
  a deterministic HTML page (window.__seek) rendered frame by frame or as
  ffmpeg segments, music with license and credit, ducking and loudness master,
  contact-sheet review, and a preflight gate that blocks the post. Covers
  vertical Shorts (1080x1920, under 60 s), clips cut from long streams and
  long-form videos with chapters. Use whenever building or changing a video
  pipeline (Python + ffmpeg + headless Chrome, Remotion, HyperFrames), adding
  captions, music or voice to a video, cutting clips from a live, or when a
  rendered video has sync, loudness, caption-timing or "looks generic" problems.
---

# video-pipeline

A video made by code is a function of a folder: the same inputs render the same file. Every stage writes a
file the next one reads, so any stage can be redone alone (new voice, same picture) and any result can be
checked. Motion vocabulary and taste live in `motion-dictionary`; this skill is the plumbing.

## The stages

```
brief.json -> script -> voice.wav + words.json -> picture (HTML __seek | ffmpeg segments)
          -> captions -> music + sfx -> mix + master -> video.mp4 + cover.jpg -> review -> preflight -> post folder
```

| Stage | Writes | Rule |
|---|---|---|
| Brief | `brief.json` | beats with what each one makes the viewer believe; sources with date; permission to use the footage |
| Script | `script.txt` | ~2.5-3 words/s; one idea per beat; every fact traceable to a primary source |
| Voice | `voice.wav`, `words.json` | whole script in one TTS request (one voice, one prosody); keep word timings |
| Picture | frames or segments | pure function of time; no clock, no randomness without a seed |
| Captions | `transcript.json` / `.ass` | word-level, grouped with their clip; land 0-2 frames before the word is heard |
| Music | `music.*`, `CREDITO.txt` | licence allows commercial use and modification; credit text saved next to it |
| Mix | `mix.wav` | music ducked under speech; master to the platform target |
| Review | `contact.png`, notes | look at the frames before calling it done |
| Preflight | exit code | a script, not a promise: fails block the post |

## Word timings: the spine of the edit

Store words as `[{"w": "texto", "start": 1.234, "end": 1.502}]` (seconds, 3 decimals). Cuts, caption pops, sfx
hits and zooms all key off this list, so a better aligner improves every stage at once.

- Transcribe with faster-whisper (`word_timestamps=True, vad_filter=True`), or WhisperX (transcription plus
  wav2vec2 forced alignment) when word edges must be tight (karaoke captions, cuts on a word). WhisperX runs on
  CPU int8 with no account; only speaker diarization needs a HuggingFace token.
- WhisperX pins its own torch: give it a separate venv and call it as a subprocess that writes the JSON, with a
  fallback to the plain transcriber if it fails.
- Words the aligner cannot place (numbers, acronyms) come back without times: spread them between their neighbours.
- Decode audio with ffmpeg to raw PCM (`-f f32le -ac 1 -ar 16000 -`) and pass the array; library decoders break on new container versions.

## Picture

**HTML page, frame-exact (default for motion graphics).** The page defines `window.__duration` (ms) and
`window.__seek(tMs)`, which draws the exact frame for time t from scratch. A headless Chrome renderer calls
`__seek` for every frame, screenshots, and pipes to ffmpeg. Because nothing reads a clock, any frame renders alone
and identically, which is what makes a frame checkable. Use `motion-dictionary/fx.js` or GSAP with a paused
timeline (`tl.seek(t)`); never CSS animations or `requestAnimationFrame` loops.

**ffmpeg segments (default for footage).** One segment per beat (image with a slow pan, a clip, an overlay PNG),
concat, then burn captions with libass. On Windows run ffmpeg with the project root as cwd and pass the `.ass` path
relative to it: the `subtitles=` filter breaks on a drive letter.

**Remotion.** Good when a team already writes React. Check its licence first: free for individuals and companies
up to 3 people, a paid company licence above that. Keep each clip's video and its captions inside the same
`<Sequence>`, with trimming and playback rate on that shared parent, so moving or trimming a clip moves its captions.

## Captions

- Word-level, 1-3 words on screen, the spoken word highlighted (karaoke). Big, high-contrast, inside the safe area
  (vertical: clear of the bottom ~20 % and the right-side buttons).
- Reaction words or emphasis can pop (scale 0 to 1.15 to 1 in ~8 frames) 2-3 frames *after* the word, with a sound.
- Fix the transcript before burning: names, brands and numbers are where ASR fails. Keep a per-project fix list.
- A synthetic voice is labelled as synthetic in the caption or description.

## Music and sound

- Search only licences that allow commercial use **and** modification (CC0, PDM, CC BY, CC BY-SA; never NC or ND).
  The Openverse API filters this: `https://api.openverse.org/v1/audio/?q=<term>&license_type=commercial,modification`.
- Save the credit text and licence URL next to the file at download time; CC BY and BY-SA need it in the description.
- Some CC tracks still trigger YouTube Content ID; test on an unlisted upload before an important video.
- Cut to the beat: track beats once (librosa `beat_track`, `onset_detect`), then snap planned cut times to the
  nearest beat within ~0.3 s. Snap only when it does not cut a word in half.
- Duck music to ~0.15-0.2 of its level under speech; 1-3 hand-placed hits, silence before the biggest one.

## Master

- Loudness: ~-14 LUFS integrated, true peak <= -1 dBTP (`loudnorm=I=-14:TP=-1:LRA=11`, two-pass when time allows).
- Shorts: 1080x1920, 30 fps, H.264 + AAC 48 kHz, under 60 s (leave margin: 59.5 s). Long-form: 1920x1080.
- Cover: same aspect as the video, readable as a thumbnail at 10 % size.

## Clips from long streams

1. Download the VOD once; keep it until every usable moment has been cut.
2. Find candidate moments without watching 10 hours: chat-rate peaks when the chat replay exists; otherwise
   loudness peaks (RMS per second scored against the local median of the surrounding ~10 minutes, peaks at least
   a few minutes apart). Print what was said around each peak from the transcript.
3. Cut a window around the peak, transcribe it at word level, start on the setup (not the punchline) and end on the reaction.
4. Every clip needs something the source does not have (context, a verdict, a question, an edit). A raw re-upload is not a video.

## Review and preflight

Review: contact sheet (`ffmpeg -i v.mp4 -vf "fps=2,scale=360:-1,tile=6x5" contact.png`), a phone-size still,
ffprobe for duration and streams, loudnorm print for LUFS. Read `motion-dictionary/review.md` for promo pieces.
The agent cannot hear: anything only a listener can judge goes in the notes as pending for the human.

Preflight is a script that exits non-zero on: missing file, wrong resolution or duration, title too long,
missing disclosure labels (paid promotion, synthetic content, affiliate notice), missing credits or licence text,
hashtags out of policy, missing review notes. It runs before every post, and the post step refuses on failure.

## Pitfalls

- Re-rendering everything for one change: stages write files so you can redo only the voice, only the picture.
- Batches of near-identical videos from one template read as mass-produced and get demonetised; vary the idea, not only the text.
- Captions from a previous transcript after the cut changed: regenerate words after every trim.
- Music fitted to an early cut ends in digital silence after a trim: refit the music last.
- Facts in the voice-over that are not in the source: the preflight cannot catch them; the script stage must cite them.

## Source

Extracted from the owner's working pipelines (news Shorts, stream cuts, product spots, tech explainers), 2026-11
(Path 1). Remotion caption grouping from remotion-dev/skills `remotion-captions` (read 2026-11-20).
