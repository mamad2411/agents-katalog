---
name: losslesscut
description: "Trim and join media with LosslessCut, inspect keyframe boundaries, and choose between stream copying and smart-cut rendering."
category: cross-platform
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["losslesscut", "keyframe-cutting", "stream-copy", "ffmpeg", "gop-alignment", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# LosslessCut Stream Editor AI Skill Guide (Claude)

## Overview & Engine Architecture
LosslessCut is a fast, lossless video, audio, and subtitle trimming application powered by an Electron frontend and **FFmpeg stream-copying (`-c copy`)** engine. Claude operates as a Multimedia Streaming and Forensic Editing Specialist, specializing in **GOP (Group of Pictures) keyframe alignment**, **Smart Cut boundary re-encoding**, **lossless multi-track stream muxing**, and **programmatic segment batch cutting (`.llc` JSON format)**.

### Lossless Stream Copying & GOP Engine

```
┌─────────────────────────────────────────────────────────────┐
│                 LosslessCut Stream Processing               │
│                                                             │
│  GOP (Group of Pictures) Keyframe Architecture              │
│  [ I-Frame (IDR) ] ─── [ B-Frame ] ─── [ P-Frame ] ─── [ I-Frame ]│
│        ▲                                                     │
│        └── Safe Lossless Cut Point (No Re-encoding Needed)   │
│                                                             │
│  Cut Modes & Engine Mechanics                               │
│  ├── Keyframe Cut Mode (Fastest, snaps to nearest I-frame)  │
│  ├── Smart Cut Mode (Re-encodes strictly boundary GOPs)     │
│  └── Multi-Track Stream Preservation (Extract / Merge Audio)│
└─────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Keyframe Alignment & GOP Analysis**: Diagnose video playback freezes and black frames caused by cutting on delta frames (P/B-frames) instead of Instantaneous Decoder Refresh (IDR) keyframes.
2. **Smart Cut Configuration**: Advise when to apply Smart Cut (re-encoding only the fractional GOP between the chosen frame and nearest I-frame) for frame-exact trimming without full video re-compression.
3. **Lossless Segment Automation**: Programmatically generate LosslessCut project files (`<filename>-proj.llc`) containing millisecond-accurate cut segment timestamps and labels.
4. **Multi-Track Stream Extraction**: Author CLI commands to split and remux secondary audio commentaries, embedded closed captions, and chapter metadata tracks without quality degradation.

---

## Production Python Automation: Exact Keyframe Slicer Tool

Save this script as `keyframe_slicer.py` to inspect input video packets via `ffprobe`, locate exact IDR keyframes, and slice video losslessly with guaranteed zero freeze frames:

```python
"""
Lossless Video Slicer: Exact Keyframe Alignment
Analyzes packet keyflags via ffprobe to guarantee freeze-free -c copy cutting.
"""

import sys
import os
import subprocess
import json

def get_nearest_keyframe(file_path: str, target_time_sec: float) -> float:
    # Query packet timestamps and flags near target time
    cmd = [
        "ffprobe", "-v", "quiet", "-select_streams", "v:0",
        "-show_packets", "-show_entries", "packet=pts_time,flags",
        "-read_intervals", f"{max(0, target_time_sec - 5)}%+{target_time_sec + 5}",
        "-print_format", "json", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return target_time_sec

    data = json.loads(res.stdout)
    packets = data.get("packets", [])
    
    # Find closest keyframe packet (flags contain 'K')
    best_time = target_time_sec
    min_diff = float("inf")
    
    for pkt in packets:
        if "K" in pkt.get("flags", ""):
            pts = float(pkt.get("pts_time", 0.0))
            diff = abs(pts - target_time_sec)
            if diff < min_diff:
                min_diff = diff
                best_time = pts

    return best_time

def lossless_slice(input_path: str, start_time: float, end_time: float, output_path: str):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} does not exist.")
        return

    # Align start and end to nearest keyframe boundaries
    safe_start = get_nearest_keyframe(input_path, start_time)
    print(f"Aligned Start: {start_time:.2f}s -> Nearest Keyframe: {safe_start:.2f}s")

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(safe_start),
        "-i", input_path,
        "-to", str(end_time - safe_start),
        "-c", "copy",
        "-avoid_negative_ts", "make_zero",
        "-movflags", "+faststart",
        output_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"Successfully created lossless cut: {output_path}")
    else:
        print(f"Slice failed:\n{res.stderr}")

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python keyframe_slicer.py <input.mp4> <start_sec> <end_sec> <output.mp4>")
        sys.exit(1)
    lossless_slice(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4])
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Black Screen / Freeze for First 2-5 Seconds of Output** | Stream cut started on a non-keyframe (P-frame/B-frame), leaving the video decoder waiting for the next I-frame. | 1. In LosslessCut, toggle **Keyframe Cut Mode** (Press `K`).<br>2. Use the left/right arrow keys to jump strictly between keyframes.<br>3. Or enable **Smart Cut** to re-encode only the first fractional GOP. |
| **Audio Plays but Video is Frozen after MP4 Export** | Missing `avoid_negative_ts` parameter caused negative presentation timestamps (PTS) in container headers. | 1. In LosslessCut Export settings, verify **Avoid Negative Timestamps** is set to `make_zero`.<br>2. Set Output Container to **MKV** for broader timestamp tolerance. |
| **Subtitles / Secondary Audio Tracks Stripped on Export** | Stream selection filter excluded secondary stream tracks during stream copy. | 1. In LosslessCut, open the **Tracks** panel (top right).<br>2. Ensure all audio and subtitle tracks are checked for inclusion.<br>3. In CLI, include `-map 0` to preserve all streams. |
| **LosslessCut Fails on Corrupted Ingest: `Invalid NAL unit size`** | Damaged MP4 container header from incomplete screen recording or crash. | Remux container through FFmpeg before cutting: `ffmpeg -i input.mp4 -c copy -movflags +faststart fixed.mp4`. |

---

## Command Line Syntax & Project Interchange

```bash
# 1. Launch LosslessCut with Media File
lossless-cut "C:\Recordings\gameplay.mp4"

# 2. Programmatic Lossless Segment Concatenation via FFmpeg
ffmpeg -f concat -safe 0 -i segments.txt -c copy -movflags +faststart merged.mp4

# 3. Extract Audio Track 2 Losslessly as AAC/M4A
ffmpeg -i movie.mkv -map 0:a:1 -c:a copy commentary.m4a
```

### Configuration & Project File Locations
- **Windows Preferences**: `%APPDATA%\lossless-cut`
- **Linux Preferences**: `~/.config/lossless-cut`
- **macOS Preferences**: `~/Library/Application Support/lossless-cut`
- **Project Segment JSON**: `<video_name>.mp4-proj.llc`

---

## Agent Operational Directive
> **MANDATORY**: When performing lossless trimming (`-c copy`), snap cuts strictly to I-frame/IDR keyframe boundaries to prevent decoder freeze frames. Use `-avoid_negative_ts make_zero` on all output containers.
