---
name: rn-replica-qc
description: >
  Analyze, recreate, align, and verify reference-video motion. Use when the
  user asks to recreate, copy, match, align, pixel-align, or compare a video;
  when a HyperFrames or Remotion remake is judged not aligned; when fixed
  reference playback and reusable motion components must be separated; or when
  delivery needs full-frame runtime, render, decode, boundary, timing, and
  archive evidence instead of sampled screenshots alone.
---

# Reference Video Replica QC

## Role

Turn reference-video recreation into a red/green evidence loop and, when useful,
capture the aligned motion as reusable HyperFrames or Remotion components.

Read [replica-levels.md](references/replica-levels.md) before naming or promising
fidelity. A source-stream copy, an exact lossless render frame, an encoded
frame-aligned MP4, a visual rebuild, and a style reference are different claims.

## Canonical Showcase

- Human display name: Presenton 复刻 Bitexact 成片
- File: `assets/showcases/presenton-replica-pixel-aligned-bitexact.mp4`
- This showcase demonstrates source-stream bit exactness. Do not use it as proof
  that a hand-authored HTML composition is bit exact.

## Operating Modes

- **Analysis-only**: inspect and report; do not edit implementation code.
- **Replica-loop**: repair the candidate until the declared evidence gate passes.
- **Component-capture**: register a proven motion pattern with inputs and limits.

## Workflow

### 1. Declare The Contract

Record the reference, exact segment, renderer, fidelity label, deliverables,
component-library destination, and evidence required for approval. Use Goal mode
when available; otherwise keep `alignment-report.md` and `patch-log.md` beside
the project.

**Complete when:** the segment and every acceptance claim can be tested without
relying on chat memory.

### 2. Lock The Timebase

Probe FPS, duration, start time, pixel format, frame count, and audio presence.
For exact work, map timestamps to source frame numbers and extract by frame
index. Inclusive segment count is `(end_frame - start_frame) + 1`. When joining
adjacent inclusive segments, keep the earlier boundary frame and skip the first
frame of the next segment.

Use `extract_halfsec_frames.py` for discovery and `extract_frame_range.py` for
full-frame acceptance sequences.

**Complete when:** reference frame 1, final frame, count, and PTS mapping are
explicit and reproducible.

### 3. Choose The Architecture

- **Exact replay**: fixed reference content rendered from verified lossless
  frames or sprite rows. It is not a freely generative component.
- **Parametric motion**: DOM/SVG/GSAP/React/Three.js with replaceable content.
- **Hybrid**: ship exact replay for fidelity and keep a separate parametric
  implementation for later abstraction.

Never present an exact-replay texture layer as a parameterized AI component.

### 4. Analyze And Repair

Read [alignment-workflow.md](references/alignment-workflow.md). Start with a
`0.5s` contact sheet, add `0.1s` windows around fast motion, then repair the
earliest or largest mismatch one visible cause at a time. Sampling locates
problems; it does not approve pixel or frame-aligned delivery.

For the Presenton failure modes and the dynamic-image decode race, read
[presenton-lessons.md](references/presenton-lessons.md).

**Complete when:** the candidate reaches the declared visual state and no known
earlier mismatch remains hidden behind a later fix.

### 5. Pass Three Evidence Gates

1. **Asset gate**: reference extraction count is exact; generated sprite cells
   or lossless intermediates round-trip to their source frames with zero error.
2. **Runtime gate**: the real registered timeline advances sequentially through
   every required frame. Do not call a test-only setter. Check arbitrary seeks,
   every dynamic-asset boundary, and previously aligned neighboring segments.
3. **Delivery gate**: run the renderer, decode the delivered MP4, compare every
   frame, check temporal candidates, inspect worst and boundary frames, probe
   media metadata, and verify archive copies by SHA-256.

For HyperFrames, `npx hyperframes check .` must pass before render. A successful
render log is not delivery evidence. For Remotion, use the project's equivalent
runtime and decoded-frame checks.

**Complete when:** all three gates are green and the report states which layer
each metric proves.

### 6. Extend And Join

When continuing a replica in segments, rerun the previous segment, render the
new segment independently, skip duplicate inclusive boundary frames, and check
the frame before, at, and after every join. Then probe the combined frame count
and duration.

**Complete when:** both old and new ranges pass and no join repeats, drops, or
rewinds a frame.

### 7. Capture Components

Register exact replay and parametric motion separately. Each entry includes:

- type: `exact-replay` or `parametric-motion`
- source and timestamp range
- intended content pattern
- inputs and timing contract
- implementation stack and assets
- evidence files and acceptance level
- known limits

### 8. Decide

Approve only the fidelity label proved by current evidence. If a gate is red,
say `not aligned`, name the first failing frame or timestamp, and continue the
replica loop.

## Script Usage

```bash
# Discovery samples and contact sheets
python3 scripts/extract_halfsec_frames.py reference.mp4 --out analysis/sample --contact

# Exact inclusive frame range
python3 scripts/extract_frame_range.py reference.mp4 --start-frame 720 --end-frame 1020 --out analysis/reference-fullfps

# Lossless sprite rows and round-trip proof
python3 scripts/build_frame_sprite_rows.py analysis/reference-fullfps assets/textures --prefix replica-row --frames-per-row 7
python3 scripts/verify_frame_sprite_rows.py analysis/reference-fullfps assets/textures --prefix replica-row --frames-per-row 7

# Real timeline capture, followed by full-frame comparison
node scripts/verify_timeline_playback.cjs --html ./index.html --timeline-id composition_id --start 24 --frames 301 --fps 30 --out analysis/runtime
python3 scripts/verify_frame_sequence.py analysis/reference-fullfps analysis/runtime --output analysis/runtime-metrics.json --boundary-every 7

# Delivered video comparison and decoded-frame gate
python3 scripts/compare_videos.py reference.mp4 candidate.mp4 --out analysis/delivery --reference-start-frame 720 --candidate-start-frame 0 --frame-count 301 --boundary-every 7
```

Use a Python runtime with Pillow for frame and sprite verification. Timeline
capture requires Playwright in the Node runtime.

## Required Outputs

- `alignment-report.md` and `patch-log.md`
- source and candidate contact sheets
- full-frame runtime and delivery metrics JSON
- worst-frame and boundary-frame evidence
- side-by-side comparison video or sheet
- media probe and checksum evidence
- component catalog entry when requested
- final pass/fail summary

For content-creation projects, copy final videos into `成片/` and the compact QC
evidence into the sibling `质检/` directory.
