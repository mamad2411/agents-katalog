---
name: video-auto-snapshot
description: Process local video files by reading duration and exporting 10 evenly spaced screenshots, preferably choosing frames with people or faces when available. Use when the user wants to sample a local video, inspect its length, extract representative frames, or prioritize human-visible frames over raw interval snapshots.
---

# Video Auto Snapshot

## Overview

Use this skill to turn one local video into a small, representative set of screenshots.
Prefer direct file paths or uploaded video files, then probe duration, sample 10 evenly spaced timestamps, and choose the best frame near each timestamp with a face/person preference.

## Workflow

Use `scripts/video_auto_snapshot.py` for the actual extraction work.

1. Ask for the video path if the user has not already provided one.
2. Read the video duration first.
3. Compute 10 sample points across the full duration.
4. For each sample point, inspect nearby frames and prefer:
   - a frame with a visible person or face
   - otherwise the sharpest non-black frame nearest the target time
5. Export the selected frames and return:
   - the 10 image files
   - the chosen timestamps
   - whether person detection succeeded for each frame

## Quick Start

Example run:

```bash
scripts/video-auto-snapshot /path/to/video.mp4 --output-dir ./out --contact-sheet ./out/contact-sheet.jpg --json ./out/result.json
```

If the user does not provide an output directory, create `<video-stem>-截图/` and place screenshots in `shots/` with `result.json` at the root.

## Interaction Rules

- Prefer a single clarifying question: ask only for the file path or upload if the video is missing.
- Treat the skill as a local-file workflow, not a GUI file picker.
- If person detection is unavailable or unreliable, continue with evenly spaced frames rather than blocking.
- Avoid sampling the first or last few percent of the clip unless the user explicitly asks for intro/outro coverage.

## Output Expectations

- Return concise results with timestamps and file names.
- If the user asks for a contact sheet, create one from the selected frames after the 10 stills are chosen.

## References

- See [video-workflow.md](references/video-workflow.md) for the sampling and fallback policy.
