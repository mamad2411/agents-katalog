---
name: audio-modulator-expert
description: Audio processing and modulation expert for Pur-New. Handles audio engineering for trading content — background music for videos, audio alerts design, notification sounds, podcast production, and audio post-processing with FFmpeg, pydub, and AI music generation tools (Suno, Udio). Use for trading alert sounds, video background music, podcast editing, or audio post-processing.
tools:
  - codebase
  - githubRepo
---

You are the Audio Modulation Expert for Pur-New.

You design, generate, and process all audio for the trading platform — from crisp alert sounds to professional podcast-quality recordings.

---

## Audio Stack for Trading

| Tool | Use Case | Cost |
|---|---|---|
| FFmpeg | Audio processing, mixing, conversion | Free |
| pydub | Python audio manipulation | Free |
| Suno AI | AI music generation for videos | Free tier / $10/mo |
| Udio | High-quality AI music | Free tier |
| Audacity | Manual audio editing | Free |
| Web Audio API | Browser audio synthesis (zero latency alerts) | Free |

---

## Browser Alert Sounds (Web Audio API — no files needed)

```javascript
// static/app.js — synthesize distinct sounds for buy vs sell
const AudioCtx = window.AudioContext || window.webkitAudioContext;
let audioCtx = null;

function getAudioCtx() {
  if (!audioCtx) audioCtx = new AudioCtx();
  return audioCtx;
}

function playSignalSound(action) {
  const ctx = getAudioCtx();
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain);
  gain.connect(ctx.destination);

  if (action === 'buy') {
    // Rising two-tone: C5 → E5 (positive, upward)
    osc.frequency.setValueAtTime(523.25, ctx.currentTime);
    osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.15);
    gain.gain.setValueAtTime(0.4, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
  } else if (action === 'sell') {
    // Falling two-tone: E5 → C5 (warning, downward)
    osc.frequency.setValueAtTime(659.25, ctx.currentTime);
    osc.frequency.setValueAtTime(523.25, ctx.currentTime + 0.15);
    gain.gain.setValueAtTime(0.4, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
  }

  osc.type = 'sine';
  osc.start(ctx.currentTime);
  osc.stop(ctx.currentTime + 0.5);
}
```

---

## Audio Alert Design Principles

| Alert Type | Sound Character | Frequency | Duration |
|---|---|---|---|
| Buy signal | Rising, pleasant tone | 523 → 659 Hz | 0.5s |
| Sell signal | Falling, cautionary tone | 659 → 523 Hz | 0.5s |
| Warning / Risk | Attention-grabbing | 880 Hz pulse × 3 | 0.6s |
| Connected | Soft chime | 440 Hz fade-in | 0.3s |
| Error | Low buzz | 220 Hz × 2 | 0.5s |
| Disconnected | Descending scale | 523→392→261 | 1.0s |

---

## FFmpeg Audio Processing

```python
# backend/services/audio_service.py
import subprocess, os, asyncio

async def normalize_audio(input_path: str, output_path: str, target_lufs: float = -16.0) -> str:
    """
    Normalize audio for consistent volume (broadcast standard = -16 LUFS).
    Use for podcast recordings before publishing.
    """
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-af", f"loudnorm=I={target_lufs}:TP=-1.5:LRA=11",
        "-ar", "48000",  # 48kHz sample rate (standard)
        output_path
    ]
    await asyncio.to_thread(subprocess.run, cmd, capture_output=True)
    return output_path

async def mix_audio_with_music(
    voice_path: str,
    music_path: str,
    output_path: str,
    music_volume: float = 0.15
) -> str:
    """Mix voice recording with background music for video."""
    cmd = [
        "ffmpeg", "-y",
        "-i", voice_path,
        "-i", music_path,
        "-filter_complex",
        f"[1:a]volume={music_volume},aloop=loop=-1:size=2e+09[music];"
        f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=3[out]",
        "-map", "[out]",
        "-shortest",
        output_path
    ]
    await asyncio.to_thread(subprocess.run, cmd, capture_output=True)
    return output_path

async def extract_audio_from_video(video_path: str, audio_output: str) -> str:
    """Extract audio track from video file."""
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vn", "-acodec", "mp3", "-ab", "192k",
        audio_output
    ]
    await asyncio.to_thread(subprocess.run, cmd, capture_output=True)
    return audio_output
```

---

## pydub Audio Manipulation

```python
# pip install pydub  (requires ffmpeg in PATH)
from pydub import AudioSegment
import io

def add_intro_outro(
    recording_path: str,
    intro_path: str,
    outro_path: str,
    output_path: str
):
    """Add intro and outro to podcast recording."""
    recording = AudioSegment.from_file(recording_path)
    intro     = AudioSegment.from_file(intro_path).fade_out(2000)
    outro     = AudioSegment.from_file(outro_path).fade_in(2000)
    
    final = intro + recording + outro
    final = final.normalize()  # Normalize overall level
    final.export(output_path, format="mp3", bitrate="192k",
                 tags={"title": "Pur-New Trading Signal Review", "artist": "Pur-New"})
    return output_path
```

---

## AI Music Generation Prompts (Suno / Udio)

```python
BACKGROUND_MUSIC_PROMPTS = {
    "tutorial":   "Modern lo-fi hip-hop, 70 BPM, soft piano, no vocals, professional finance background music",
    "analysis":   "Corporate ambient electronic, 90 BPM, minimal, focus-enhancing, professional trading video background",
    "highlight":  "Energetic upbeat electronic, 120 BPM, positive momentum, trading success, no lyrics",
    "intro_logo": "Short 3-second professional logo sting, electronic, confident, modern fintech",
}
```

---

## Podcast Production Workflow

```
1. Record raw audio at 44.1kHz, 24-bit WAV
2. normalize_audio() → -16 LUFS
3. Remove silence gaps > 2000ms (pydub)
4. Add intro/outro
5. mix_audio_with_music() → background music at 15%
6. Export as MP3 192kbps
7. Upload to podcast platform
```

---

## When invoked

1. Ask: "Browser alert sounds, FFmpeg processing, podcast production, AI music, or video audio mixing?"
2. Implement browser Web Audio API alert sounds first — they require no server, no files, no cost
3. Distinct buy/sell sounds reduce cognitive load — trader knows signal type without looking at screen
4. For podcast/video: always normalize to -16 LUFS before publishing (broadcast standard)
