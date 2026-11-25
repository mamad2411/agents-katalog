---
name: media-pipelines
description: |
  Media content pipelines: audio/video cutting, silence/filler removal,
  ffmpeg workflows, transcription-aligned edits, and simple indexing/reporting
  over media files. Use for ffmpeg-based tasks, audiobook/essay narration
  assembly, and A/V deliverables — not for general coding or tabular ML.
---

# media-pipelines

Load `safe-agent-scope` before any state-changing action; media edits do not waive sandbox, recipient, or injection rules.

## Why

Media tasks fail on **timebases, sample rates, and concat order**. Always
probe streams first; prefer deterministic ffmpeg filter graphs over manual
guessing.

## Procedure

1. **Probe** — `ffprobe` (or equivalent) for duration, codec, sample rate, streams.
2. **Plan cuts** — list segments with start/end; keep a manifest CSV/JSON if useful.
3. **Filter graph** — silence detect → cut → concat; keep PCM/wav intermediates if needed.
4. **Sync** — when aligning to transcript or another track, verify offsets on a short sample.
5. **Encode once** at the end with the required container/codec.
6. **Verify** — duration sanity; playhead spot-check; `verify-task-output`.

## Heuristics

- Re-encode less: stream-copy when cuts are keyframe-aligned and allowed
- Normalize loudness only if the task asks
- Keep intermediate files until final QA passes

## Anti-patterns

- Concatenating mismatched sample rates without resampling
- Dropping streams (subs/audio) unintentionally
- Huge one-liner ffmpeg commands you can't debug — build stepwise
