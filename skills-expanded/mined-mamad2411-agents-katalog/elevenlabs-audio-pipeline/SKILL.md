---
name: elevenlabs-audio-pipeline
description: ElevenLabs beyond TTS, speech to text with Scribe, dubbing, sound effects, music, audio isolation, and speech to speech. Use when the user wants to transcribe, dub, clean up, or generate non-speech audio.
---

# ElevenLabs audio pipeline

Everything below is available through the connected MCP server tools or the
REST API at `https://api.elevenlabs.io` with the `xi-api-key` header. Each
call spends account credits.

## Speech to text (Scribe)

- Endpoint: `POST /v1/speech-to-text` with the audio file.
- Models: `scribe_v1` (about 99 languages) and the newer Scribe v2 family,
  including a realtime variant. Check `GET /v1/models` or the docs for the
  exact v2 id before hardcoding.
- Features: word-level timestamps, speaker diarization (returns per-speaker
  segments; ask for it when the user says "who said what"), and audio event
  tagging (laughter, applause).
- Long recordings: prefer uploading the file once and letting the API chunk;
  do not transcode to lossy formats first if the source is clean.

## Dubbing

- The Dubbing API (`/v1/dubbing`) takes audio or video, transcribes,
  translates, and re-voices it in a target language while preserving
  speakers.
- Async: create a dubbing job, poll its status, then download the dubbed
  media. Expect minutes for video.
- Review the transcript before final render when quality matters; the
  dubbing studio flow allows manual correction of segments.

## Sound effects

- `POST /v1/sound-generation`: text prompt to a sound effect.
- Prompt with source, action, and environment ("heavy wooden door creaking
  open in a stone hallway"), and set the duration parameter for timed cues.
- Iterate in small batches; short effects are cheap, so generate variants
  and pick.

## Music

Eleven Music generates studio-grade tracks from natural language prompts
(genre, mood, tempo, instrumentation, structure). Use it through the MCP
tool or the Music API in the docs; confirm commercial-use terms on the
user's plan before shipping generated tracks in a product.

## Audio isolation

`POST /v1/audio-isolation` strips background noise and music, returning
clean speech. Run it before Scribe on noisy field recordings; the
transcription accuracy gain is large.

## Speech to speech

`POST /v1/speech-to-speech/{voice_id}` with model
`eleven_multilingual_sts_v2` re-voices existing audio into a target voice
while keeping the performance (timing, emotion). Use it to fix a word in a
recorded line or convert a scratch take to the production voice.

## Pipeline patterns

- Podcast cleanup: audio isolation -> Scribe with diarization -> TTS or STS
  for pickups.
- Localized video: Scribe -> dubbing to target languages -> sound effects
  for missing ambience.
- The MCP server writes output files to disk by default
  (`ELEVENLABS_MCP_BASE_PATH`, default `~/Desktop`); tell the user where the
  artifacts landed and clean up intermediates.
