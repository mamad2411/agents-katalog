---

name: video-transcribe-and-timestamp
description: video-transcribe-and-timestamp lets the user convert spoken video content into text with timestamps attached to the right moments, which is useful for editing, captioning, quote extraction, clip selection, summaries, training material, and finding exactly where key statements happen inside a longer recording.
tags: [transcription, whisper, video, timestamps, ffmpeg, google-drive]

---
Transcribes any video (local file, Google Drive link, or direct URL) using faster-whisper and formats output as timestamped bullet point summaries.

## What This Skill Does

This skill video-transcribe-and-timestamp lets the user convert spoken video content into text with timestamps attached to the right moments, which is useful for editing, captioning, quote extraction, clip selection, summaries, training material, and finding exactly where key statements happen inside a longer recording.

## Charles's Approved Format (use this every time)

- Timestamps spaced **10-15 minutes apart**
- Each bullet is **1-2 sentences max** — tight summary of what was discussed, not a transcript dump
- File delivered as `.txt` via Telegram

Example output:
```
[00:00]
• Charles opens the Zoom and addresses a member's OpenClaw/Telegram issue, then demos GoHighLevel's "Build Using AI" feature inside Automations.

[12:00]
• He warns against chasing shiny new objects and live-demos his AI agents Mark and Michael as replacements for two fired VAs.
```

## Step 1 — Download Video

### Google Drive link
```python
# Install gdown if needed
pip install gdown --break-system-packages -q

# Download (extract file ID from share URL)
gdown "https://drive.google.com/uc?id=FILE_ID" -O /tmp/video.mp4
```

### Direct URL
```bash
wget -O /tmp/video.mp4 "https://direct-url-to-video.mp4"
```

## Step 2 — Extract Audio

```bash
ffmpeg -i /tmp/video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 /tmp/audio.wav -y
```

## Step 3 — Transcribe with faster-whisper

```python
from faster_whisper import WhisperModel
import json

model = WhisperModel("base", device="cpu", compute_type="int8")
segments, info = model.transcribe("/tmp/audio.wav", language="en", beam_size=5, vad_filter=True)

results = []
for seg in segments:
    results.append({"start": round(seg.start, 1), "end": round(seg.end, 1), "text": seg.text.strip()})

with open("/tmp/transcript_raw.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"{len(results)} segments. Duration: {results[-1]['end']/60:.1f} min")
```

Install if missing:
```bash
pip install faster-whisper --break-system-packages -q
```

## Step 4 — Generate Timestamped Bullets

```python
import json

with open("/tmp/transcript_raw.json") as f:
    segments = json.load(f)

def fmt_time(seconds):
    m = int(seconds) // 60
    s = int(seconds) % 60
    return f"{m:02d}:{s:02d}"

# Group into ~720-second (12-minute) chunks
CHUNK_SIZE = 720
chunks = []
current_chunk = []
chunk_start = None

for seg in segments:
    if chunk_start is None:
        chunk_start = seg["start"]
    current_chunk.append(seg["text"])
    if seg["end"] - chunk_start >= CHUNK_SIZE:
        chunks.append({"start": chunk_start, "end": seg["end"], "text": " ".join(current_chunk).strip()})
        current_chunk = []
        chunk_start = None

if current_chunk and chunk_start is not None:
    chunks.append({"start": chunk_start, "end": segments[-1]["end"], "text": " ".join(current_chunk).strip()})

# Print full text of each chunk — then write 1-2 sentence summaries manually
for i, c in enumerate(chunks):
    print(f"\n=== CHUNK {i+1} [{fmt_time(c['start'])}] ===")
    print(c['text'])
```

Then write the final output file with 1-2 sentence summaries per chunk:

```python
lines = ["VIDEO TRANSCRIPT — TIMESTAMPED BULLET POINTS", "=" * 60, ""]
for c in chunks:
    lines.append(f"[{fmt_time(c['start'])}]")
    lines.append(f"  • YOUR 1-2 SENTENCE SUMMARY HERE")
    lines.append("")

with open("/tmp/transcript_timestamped.txt", "w") as f:
    f.write("\n".join(lines))
```

## Clip Trimming

To trim a specific time range before transcribing:

```bash
ffmpeg -i /tmp/video.mp4 -ss HH:MM:SS -to HH:MM:SS -c copy /tmp/clip.mp4 -y
```

Then run the same audio extraction + transcription workflow on `/tmp/clip.mp4`.

For per-clip transcription, filter the raw JSON segments by time range:
```python
clip_start = 3734  # seconds
clip_end = 4080
clip_segments = [s for s in segments if s["start"] >= clip_start and s["end"] <= clip_end]
```

## Output

Deliver as `.txt` file via Telegram:
```
MEDIA:/tmp/transcript_timestamped.txt
```

## PDF Generation (for formatted reports)

If Charles asks for a PDF version of the transcript, use `reportlab`. Install it into the system Python, NOT the hermes venv (hermes venv has no pip):

```bash
pip3 install reportlab --break-system-packages
```

Then run the script using system Python (`/usr/bin/python3`), not the hermes venv python. The hermes venv python at `/root/.hermes/hermes-agent/venv/bin/python3` cannot install packages via pip — use it only for packages already in the venv (like `google-genai`, `faster-whisper`).

## Pitfalls

- **faster-whisper not in hermes venv** — install with `pip install faster-whisper --break-system-packages`
- **Google Drive large files** — gdown handles the virus-scan confirmation redirect automatically; use `uc?id=FILE_ID` format
- **Long videos (>1hr)** — `base` model on CPU takes ~3-5 min for 90 minutes of audio; `vad_filter=True` speeds it up by skipping silence
- **Chunk size** — Charles approved 720 seconds (12 min). Do NOT use 60-second chunks — too granular. Do NOT dump raw transcript — always summarize to 1-2 sentences.
- **Clip timestamps in output** — when transcribing a clip, show timestamps relative to the ORIGINAL video (e.g. `[1:02:14]`), not relative to the clip start
