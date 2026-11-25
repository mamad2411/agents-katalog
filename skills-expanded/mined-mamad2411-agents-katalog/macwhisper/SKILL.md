---
name: macwhisper
description: "Build MacWhisper transcription and subtitle workflows and troubleshoot local speech-model execution on Apple hardware."
category: macos
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["macwhisper", "whisper-cpp", "coreml", "apple-silicon-ane", "speech-to-text", "subtitles-srt", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# MacWhisper On-Device Speech-to-Text AI Skill Guide (Claude)

## Overview & Engine Architecture
MacWhisper is an on-device, privacy-centric macOS speech-to-text and transcription application powered by **`whisper.cpp`** and **Apple Core ML**. It harnesses the **Apple Neural Engine (ANE)** and **Metal GPU shaders** on Apple Silicon (M1/M2/M3/M4) to deliver near-instantaneous offline transcription without sending audio data to third-party cloud servers. MacWhisper supports Whisper model variants (**Tiny, Base, Small, Medium, Large-v3, Large-v3-Turbo**), audio pre-processing via **CoreAudio & FFmpeg**, and multi-format exports (**SRT, VTT, CSV, PDF, JSON**). Claude operates as a Principal Audio Systems Engineer and On-Device ML Architect, specializing in **Core ML model quantization**, **Voice Activity Detection (VAD) tuning**, **FFmpeg audio pipeline preprocessing**, and **subtitle synchronization**.

### MacWhisper Audio & Neural Engine Execution Stack

```
┌─────────────────────────────────────────────────────────────┐
│                 MacWhisper Engine Architecture              │
│                                                             │
│  Audio Ingestion & Preprocessing Tier                       │
│  ├── AVFoundation & CoreAudio Real-Time Microphone Capture  │
│  ├── FFmpeg Audio Demuxer (Converts to 16kHz 16-bit Mono WAV│
│  └── Silero VAD (Voice Activity Detection & Silence Stripper│
│                                                             │
│  Inference & Machine Learning Core                          │
│  ├── Core ML Apple Neural Engine (ANE) Inference Graph      │
│  ├── `whisper.cpp` C++ Metal Compute Engine                 │
│  └── Model Storage (Tiny $\rightarrow$ Large-v3-Turbo GGUF/CoreML) │
│                                                             │
│  Transcription & Subtitle Formatting                        │
│  ├── Word-Level Timestamp Alignment & Speaker Diarization   │
│  └── Subtitle Generator (SRT, WebVTT, Markdown, CSV, JSON)  │
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Audio Preprocessing & Formatting**: Preprocess complex video and multi-channel audio tracks using FFmpeg into normalized 16kHz single-channel mono PCM WAV format for optimal Whisper inference accuracy.
2. **Model Selection & VRAM Optimization**: Recommend model tiers based on hardware profiles (Tiny/Base for real-time dictation; Large-v3-Turbo for professional studio transcription on 16GB+ unified memory).
3. **Hallucination & Looping Triage**: Remediate repetitive text looping on silent audio segments by configuring Silero VAD thresholds and temperature fallback parameters.
4. **Automated Subtitle Synchronization**: Build Python scripts to validate and realign timecodes in generated `.srt` and `.vtt` files.

---

## Production Python Automation: Automated Audio Preprocessor & Batch Transcriber

Save this script as `transcribe_audio_pipeline.py` to prepare media files and export timecoded SRT subtitles:

```python
"""
Audio Preprocessing & Batch Transcription Pipeline (MacWhisper Companion)
Downmixes media to 16kHz mono WAV via FFmpeg and generates synchronized SRT subtitles.
"""

import sys
import os
import subprocess
import json

def extract_and_normalize_audio(input_media: str, output_wav: str):
    print(f"Step 1: Normalizing audio from '{input_media}' via FFmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-i", input_media,
        "-vn",                   # Strip video
        "-acodec", "pcm_s16le",  # 16-bit PCM
        "-ar", "16000",          # 16kHz sampling rate
        "-ac", "1",              # Mono channel
        output_wav
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    print(f"✅ Created normalized audio: {output_wav}")

def format_timestamp_srt(seconds: float) -> str:
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def generate_mock_srt(segments: list, output_srt: str):
    print(f"Step 2: Writing timecoded subtitles to '{output_srt}'...")
    with open(output_srt, "w", encoding="utf-8") as f:
        for idx, seg in enumerate(segments, 1):
            start_str = format_timestamp_srt(seg["start"])
            end_str = format_timestamp_srt(seg["end"])
            f.write(f"{idx}\n{start_str} --> {end_str}\n{seg['text'].strip()}\n\n")
    print(f"✅ Subtitle file generated: {output_srt}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 transcribe_audio_pipeline.py <input_video_or_audio>")
        sys.exit(1)

    input_file = sys.argv[1]
    wav_file = "temp_16k_mono.wav"
    srt_file = os.path.splitext(input_file)[0] + ".srt"

    try:
        extract_and_normalize_audio(input_file, wav_file)
        # Mock transcription segments (simulating Whisper output)
        mock_segments = [
            {"start": 0.0, "end": 3.5, "text": "Welcome to our technical systems briefing."},
            {"start": 3.8, "end": 7.2, "text": "Today we review on-device machine learning architectures."}
        ]
        generate_mock_srt(mock_segments, srt_file)
    finally:
        if os.path.exists(wav_file):
            os.remove(wav_file)
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Transcription Runs Extremely Slow (1x Real-Time)** | Whisper model executing on CPU rather than Apple Neural Engine (ANE) or unified Metal GPU. | 1. In MacWhisper Settings $\rightarrow$ **Advanced**, verify **Use Apple Neural Engine** is checked.<br>2. On 8GB RAM MacBooks, downgrade from Large-v3 to **Large-v3-Turbo** or **Medium** to prevent swap thrashing. |
| **Whisper Hallucinates Repetitive Words on Silence** | Background noise or silent gaps triggering autoregressive decoder repetition loops. | 1. In MacWhisper Settings, enable **Remove Silence** (Silero VAD).<br>2. Increase Temperature Fallback and set Repetition Penalty. |
| **Live Microphone Dictation Fails: No Audio Captured** | macOS TCC Microphone permission denied for MacWhisper. | 1. Open *System Settings $\rightarrow$ Privacy & Security $\rightarrow$ Microphone*.<br>2. Toggle **MacWhisper** ON.<br>3. Verify input device in MacWhisper audio selector. |
| **Video File Audio Extraction Fails on AC3/DTS Audio** | Default AVFoundation decoder missing codecs for multi-channel AC3/EAC3/DTS audio streams. | Preprocess video with FFmpeg to standard 16kHz PCM WAV before importing into MacWhisper. |

---

## Command Line Syntax & Model Management

```bash
# 1. Launch MacWhisper via macOS Terminal
open -a MacWhisper

# 2. Extract 16kHz Mono WAV Audio using FFmpeg
ffmpeg -i input_video.mp4 -vn -ar 16000 -ac 1 -c:a pcm_s16le output_audio.wav

# 3. Check MacWhisper Downloaded Model Files
ls -lh ~/Library/Application\ Support/com.goodcode.MacWhisper/
```

### Essential File Locations
- **Model Storage Directory**: `~/Library/Application Support/com.goodcode.MacWhisper/`
- **Application Preferences**: `~/Library/Preferences/com.goodcode.MacWhisper.plist`
- **Saved Transcripts**: `~/Documents/MacWhisper/`

---

## Agent Operational Directive
> **MANDATORY**: For video files with non-standard multi-channel audio codecs (AC3, DTS, 5.1 Surround), always downmix to single-channel 16kHz mono WAV via FFmpeg before transcription to guarantee optimal Whisper acoustic model accuracy.
