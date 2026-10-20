---
name: openai-transcribe
description: Transcribe audio with OpenAI speech-to-text models (gpt-4o-transcribe, gpt-4o-mini-transcribe, whisper-1) using prompt-guided terminology, segment-level timestamps, optional diarization via post-processing, and reliable artifact delivery. Use when converting interviews, calls, podcasts, or meeting recordings into reviewable text. Requires OPENAI_API_KEY.
---

# OpenAI Transcribe

Produce trustworthy, reviewable transcripts from audio using OpenAI's speech-to-text APIs with deliberate model selection, terminology priming, chunking for long media, and explicit confidence reporting.

## Stack Baseline (2026)

| Concern | Choice | Notes |
|---|---|---|
| Default model | `gpt-4o-transcribe` | Highest accuracy; multilingual; lower WER than whisper-1 |
| Cost-tier model | `gpt-4o-mini-transcribe` | Use for bulk/low-stakes work |
| Legacy fallback | `whisper-1` | Only when needing `verbose_json` segment timestamps natively |
| Endpoint | `POST /v1/audio/transcriptions` | Multipart upload |
| Streaming | `stream=true` (Realtime/SSE) | Live captions, voice agents |
| Max file size | 25 MB per request | Chunk longer files (≤10 min slices recommended) |
| Supported formats | mp3, mp4, m4a, wav, webm, flac, ogg, mpga, mpeg | Re-encode unusual codecs to wav 16kHz mono first |
| Diarization | Not native | Use `pyannote.audio` 3.x or AssemblyAI for speaker labels, then align |
| Timestamps | `timestamp_granularities=["segment","word"]` (whisper-1) or response includes segments (gpt-4o-transcribe) | |
| SDK | `openai` Python ≥1.50, Node `openai` ≥4.70 | |

## When to Use

- Interview, podcast, lecture, or meeting transcription.
- Compliance recordings requiring searchable text.
- Generating subtitle/caption tracks (SRT/VTT).
- Building a voice-input feature where latency tolerates batch.

## Prerequisites

- `OPENAI_API_KEY` exported in environment (never hard-coded).
- Audio file path and duration known; file readable and within format support.
- Decision on output: plain text, timestamped, speaker-labeled, SRT/VTT, or summary derivatives.
- For long audio: `ffmpeg` available for re-encoding/chunking.

## Instructions

1. **Inspect input.** Check duration, container, sample rate, channels, and noise floor:
   ```bash
   ffprobe -v error -show_entries format=duration,bit_rate,format_name \
     -show_entries stream=codec_name,sample_rate,channels file.m4a
   ```
2. **Normalize if needed.** Convert to 16 kHz mono WAV for best accuracy and smallest size:
   ```bash
   ffmpeg -i input.m4a -ac 1 -ar 16000 -c:a pcm_s16le normalized.wav
   ```
3. **Chunk if >25 MB or >25 min.** Split on silence to avoid mid-word cuts:
   ```bash
   ffmpeg -i normalized.wav -f segment -segment_time 600 \
     -c copy chunks/part_%03d.wav
   ```
4. **Prime terminology with the `prompt` parameter** (≤244 tokens) — list proper nouns, product names, jargon. The model treats it as prior context, not literal text:
   ```python
   from openai import OpenAI
   client = OpenAI()

   prompt_terms = (
     "Speakers: Dr. Acharya, Mei-Lin Park. "
     "Project: Helios. Acronyms: SLO, RTO, FAPI."
   )

   with open("normalized.wav", "rb") as f:
       result = client.audio.transcriptions.create(
           model="gpt-4o-transcribe",
           file=f,
           language="en",            # ISO-639-1 hint
           prompt=prompt_terms,
           response_format="json",   # "text" | "json" | "srt" | "vtt" | "verbose_json"
           temperature=0,            # deterministic
       )
   transcript = result.text
   ```
5. **For per-segment timestamps**, use `whisper-1` with `verbose_json`:
   ```python
   v = client.audio.transcriptions.create(
       model="whisper-1",
       file=open("normalized.wav", "rb"),
       response_format="verbose_json",
       timestamp_granularities=["segment", "word"],
   )
   for seg in v.segments:
       print(f"[{seg.start:.2f}-{seg.end:.2f}] {seg.text}")
   ```
6. **Reassemble chunks** by adding cumulative offsets to each chunk's segment timestamps before merging.
7. **Diarize (optional).** Run `pyannote/speaker-diarization-3.1` separately, then assign each transcript segment to the speaker whose RTTM span overlaps most. Never fabricate speaker labels without a diarization step.
8. **Clean for human review.** Fix punctuation/casing only; preserve numbers, names, product terms verbatim. Mark unclear regions with `[unclear]` rather than guessing.
9. **Emit artifacts**: raw response JSON, cleaned `.txt`, optional `.srt`/`.vtt`, and a `confidence_notes.md` listing low-quality regions (high WER risk: overlapping speech, music bleed, clipping).
10. **Cost & latency check.** gpt-4o-transcribe is billed per minute of audio; log duration × rate before bulk runs.

## Common Pitfalls

| Pitfall | Impact | Fix |
|---|---|---|
| Sending raw 48 kHz stereo m4a | Higher cost, no accuracy gain | Downmix to 16 kHz mono WAV first |
| Treating `prompt` as a transcript prefix | Model hallucinates the prompt into output | Use only as terminology hint; verify output start |
| Splitting on fixed time without silence detection | Words cut mid-syllable, segment loss | Use `silencedetect` filter or `pydub.split_on_silence` |
| Hardcoding `OPENAI_API_KEY` in scripts | Credential leak in repo/CI logs | Read from env / secret manager only |
| Trusting transcripts of low-SNR audio | Confident-sounding hallucinations | Compute audio RMS; flag segments below threshold |
| Assuming diarization from speaker-like punctuation | Wrong speaker attribution | Run a real diarizer; align by overlap |
| Retrying on 429 without backoff | Rate-limit spiral | Exponential backoff + `Retry-After` header |
| Logging full transcript to stdout in CI | PII leak in build logs | Write to file only; redact in summaries |

## Output Format

Deliver to the caller:

1. `transcript.raw.json` — provider response, untouched.
2. `transcript.clean.txt` — punctuation/casing normalized; verbatim content.
3. `transcript.srt` or `.vtt` — when timestamps requested.
4. `confidence_notes.md` — list of `[start–end]` ranges flagged low-confidence with reason (noise, overlap, accent).
5. Optional derivatives (only if requested): `summary.md`, `action_items.md`, `decisions.md`.

## Authoritative References

- OpenAI Speech-to-text guide: https://platform.openai.com/docs/guides/speech-to-text
- Audio transcriptions API: https://platform.openai.com/docs/api-reference/audio/createTranscription
- OpenAI prompting for Whisper/transcribe: https://platform.openai.com/docs/guides/speech-to-text/prompting
- pyannote.audio (diarization): https://github.com/pyannote/pyannote-audio
- ffmpeg silencedetect: https://ffmpeg.org/ffmpeg-filters.html#silencedetect
