---
name: claude-video-enhance-audio
description: >
  AI-powered audio enhancement for video using Demucs v4 (source separation, isolate
  vocals/drums/bass/other, 7GB VRAM), pyannote-audio 4.0 + WhisperX (speaker diarization),
  DeepFilterNet3 (AI noise reduction, superior to FFmpeg), ElevenLabs/OpenAI/Bark TTS
  (voiceover generation), and AudioSR (phone-to-studio quality upsampling). Use when user
  says "separate audio", "isolate vocals", "remove music", "diarize", "speaker detection",
  "AI denoise", "deep noise reduction", "voiceover", "TTS", "text to speech",
  "upsample audio", "enhance audio quality", or "studio quality audio".
allowed-tools:
  - Bash
  - Read
  - Write
---

# claude-video-enhance-audio — AI Audio Enhancement

This sub-skill handles AI-model-based audio processing. For FFmpeg-native audio operations
(loudnorm, EQ, compression, silence removal, mixing), use `claude-video-audio` instead.

## Pre-Flight

1. Activate venv: `source ~/.video-skill/bin/activate`
2. Check free VRAM: `nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits`
3. Verify required tools are installed for the requested operation

## Source Separation (Demucs v4)

Isolate vocals, drums, bass, or other instruments from audio/video.

```bash
source ~/.video-skill/bin/activate
python3 scripts/audio_enhance.py separate "$INPUT" \
  --stems vocals \
  --model htdemucs_ft \
  --output vocals.wav
```

**Options:**
- `--stems vocals` — Extract vocals only (most common for video)
- `--stems all` — Separate into 4 stems: vocals, drums, bass, other
- `--stems vocals,other` — Extract specific combination
- `--model htdemucs_ft` — Best quality model (default, 7GB VRAM, SDR 9.20 dB)
- `--model htdemucs` — Faster, slightly lower quality (5GB VRAM)
- `--output FILE` — Output path (or directory for `--stems all`)

**VRAM:** 7GB for htdemucs_ft. Model is unloaded after processing.

**Use cases:**
- Extract clean dialogue from video with background music
- Remove background music while keeping speech
- Create music-only track for audio ducking
- Isolate instruments for remix

## Speaker Diarization (pyannote-audio 4.0)

Identify who spoke when in a video.

```bash
source ~/.video-skill/bin/activate
python3 scripts/audio_enhance.py diarize "$INPUT" \
  --output speakers.json
```

**Options:**
- `--hf-token TOKEN` — HuggingFace token (required for pyannote models)
- `--with-transcript` — Combine with WhisperX transcript for speaker-labeled text
- `--output speakers.json` — Output path

**VRAM:** 2-4GB for pyannote, +6GB if `--with-transcript` (WhisperX runs sequentially).

**Output format (speakers.json):**
```json
{
  "speakers": ["SPEAKER_0", "SPEAKER_1"],
  "segments": [
    {"speaker": "SPEAKER_0", "start": 0.5, "end": 5.2, "text": "Welcome to the show..."},
    {"speaker": "SPEAKER_1", "start": 5.8, "end": 12.1, "text": "Thanks for having me..."}
  ]
}
```

**Requires:** HuggingFace token with access to pyannote/speaker-diarization-3.1. Set via `HF_TOKEN` env var or `--hf-token` flag.

## AI Noise Reduction (DeepFilterNet3)

Superior noise reduction compared to FFmpeg's afftdn filter.

```bash
source ~/.video-skill/bin/activate
python3 scripts/audio_enhance.py denoise "$INPUT" \
  --output clean.wav
```

**VRAM:** <1GB (very lightweight)

**Quality comparison:**
- DeepFilterNet3 PESQ score: 3.17-3.50
- FFmpeg afftdn PESQ score: ~2.50
- Dramatically better for speech with background noise

**Fallback:** If DeepFilterNet3 is not installed, falls back to FFmpeg `afftdn`:
```bash
ffmpeg -n -i "$INPUT" -af "afftdn=nf=-25:nt=w" -c:v copy "$OUTPUT"
```

**Options:**
- `--compensate-delay` — Compensate for processing delay (default: true)
- `--atten-limit N` — Maximum attenuation in dB (default: 100)

## TTS Voiceover Generation

Generate voiceover narration from text.

```bash
source ~/.video-skill/bin/activate
python3 scripts/audio_enhance.py tts \
  --text "Welcome to this tutorial on video editing with Claude." \
  --provider elevenlabs \
  --voice "Rachel" \
  --output voiceover.wav
```

### ElevenLabs (Best Quality — API)

```bash
python3 scripts/audio_enhance.py tts --text "..." --provider elevenlabs --voice "Rachel" --output vo.wav
```
- Quality: Best available
- Cost: $5/month starter (30 min), $22/month creator
- Requires: `ELEVENLABS_API_KEY` env var
- Voices: 10,000+ available

### OpenAI TTS (Good Quality — API)

```bash
python3 scripts/audio_enhance.py tts --text "..." --provider openai --voice alloy --output vo.wav
```
- Quality: Very good
- Cost: $15/1M characters (tts-1), $30/1M (tts-1-hd)
- Requires: `OPENAI_API_KEY` env var
- Voices: alloy, echo, fable, onyx, nova, shimmer, ash, ballad, coral, sage, ember, vale, verse
- `--model tts-1-hd` for higher quality

### Bark (Local — Free)

```bash
python3 scripts/audio_enhance.py tts --text "..." --provider bark --output vo.wav
```
- Quality: Good, expressive, supports non-verbal sounds
- Cost: Free
- VRAM: 12GB (exclusive use — unloads all other models)
- Supports: laughter, sighs, music (via text prompts like `[laughs]`)

**Cost confirmation:** Always confirm before API-based TTS generation.

## Audio Upsampling (AudioSR)

Upscale phone-quality audio to studio quality.

```bash
source ~/.video-skill/bin/activate
python3 scripts/audio_enhance.py upsample "$INPUT" \
  --output hd_audio.wav
```

**VRAM:** 6-8GB

**What it does:**
- Input: 8-16kHz bandwidth (phone recordings, compressed audio)
- Output: 24kHz bandwidth at 48kHz sample rate
- Dramatically improves clarity and presence

**Options:**
- `--model speech` — Optimized for speech content (default)
- `--model music` — Optimized for music content
- `--model general` — General purpose

## Routing Guide: This Sub-Skill vs claude-video-audio

| Task | Use This Sub-Skill | Use claude-video-audio |
|------|-------------------|----------------------|
| Isolate vocals from music | Yes (Demucs) | No |
| Who said what (diarization) | Yes (pyannote) | No |
| AI noise reduction | Yes (DeepFilterNet3) | FFmpeg afftdn (simpler) |
| Generate voiceover | Yes (TTS) | No |
| Upsample phone audio | Yes (AudioSR) | No |
| Normalize loudness (LUFS) | No | Yes (loudnorm) |
| EQ / compression / effects | No | Yes (FFmpeg filters) |
| Remove silence | No | Yes (auto-editor) |
| Mix audio tracks | No | Yes (amix) |
| Extract audio from video | No | Yes (stream copy) |

## VRAM Management

| Operation | VRAM | Can Coexist With |
|-----------|------|-----------------|
| Demucs htdemucs_ft | 7GB | Light models (<5GB) |
| WhisperX (for diarize) | 6GB | Light models only |
| AudioSR | 6-8GB | Light models only |
| DeepFilterNet3 | <1GB | Anything |
| pyannote | 2-4GB | Medium models |
| Bark TTS | 12GB | Nothing (exclusive) |

All models are loaded on-demand and unloaded after processing with `torch.cuda.empty_cache()`.

## Safety Rules

1. Always confirm cost before API-based TTS generation
2. Run `bash scripts/preflight.sh` for output path validation
3. Warn about processing time for long audio files with heavy models
4. Never overwrite source audio files

## Reference

Load `references/audio-enhance.md` for model details, API setup, and quality comparisons.
