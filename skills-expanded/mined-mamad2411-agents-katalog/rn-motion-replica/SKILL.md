---
name: rn-motion-replica
description: "Analyze a public or local reference video, isolate a time range, deconstruct its layout, motion, timing, and transitions, then build an original verified motion replica with reusable templates and final MP4 QC. Use when the user says 复刻这个视频效果, 参考这个视频做同款动效, 拆解前 N 秒, 还原方框/连线/卡片动画, or provides a video or URL as a motion reference rather than asking to copy its footage or script."
---

# RN Motion Replica

Turn a reference clip into an original motion study that preserves the visual grammar and timing while replacing the source's copy, presenter, footage, and unique assets.

This Skill targets an editable original adaptation. Route any pixel-exact,
render-frame-exact, or encoded-frame-aligned claim through `rn-replica-qc` and
its asset, runtime, and delivery gates.

## Source and rights boundary

- Work only from a public link or local file the user is authorized to use.
- Do not bypass private-account controls, DRM, paywalls, or deleted media.
- Keep the source URL, title, downloaded media, transcript, and source screenshots in a private working directory.
- Do not ship the source media inside the finished project or Skill package.
- Recreate motion structure, layout logic, pacing, and interaction language. Write new copy and use original or generic assets.

## Workflow

### 1. Lock the study range

Identify the exact time range, the requested effects, the delivery aspect ratio, and whether the user wants a study preview or a full production asset. When the request is already specific, proceed without another intake round.

Default the canvas and fps to the reference unless the user or destination requires another format.

### 2. Acquire and verify the reference

Download the public reference with the workspace's trusted downloader or `yt-dlp`. Verify it with `ffprobe`; an HTTP success is not enough.

Require:

- a playable video stream
- non-zero duration
- known dimensions and frame rate
- an untouched source file in the private reference directory

### 3. Generate visual evidence

Run the bundled analyzer on the selected range:

```bash
python3 scripts/analyze_reference.py <reference.mp4> \
  --start 0 --duration 35 --out <private-analysis-dir>
```

Inspect all generated contact sheets and scene frames. Do not infer choreography from one thumbnail.

Record five layers of evidence:

1. visual tokens: background, border, palette, type, shadow, texture
2. geometry: safe margins, anchors, card sizes, connector routing, z-order
3. motion primitives: pop, slide, path draw, swap, push, blur, zoom
4. sequence: what enters first, what waits, what replaces an earlier state
5. timing: entrance duration, dwell, overlap, transition time, final hold

Write `frame.md` for the visual contract and `STORYBOARD.md` for the timestamped sequence before authoring animation.

For outlined cards and orthogonal connectors, read [references/box-motion-pattern.md](references/box-motion-pattern.md).

### 4. Choose the production route

Use HyperFrames by default for an authored finished video:

- short, unnarrated, motion-first shot around 10 seconds or less: route through the `motion-graphics` workflow
- longer, multi-state, or multi-scene replica: route through `general-video`
- existing talking-head footage that stays intact under new graphics: route through `talking-head-recut`

For the bundled box-motion starting point:

```bash
python3 scripts/init_motion_project.py <new-project-dir>
```

The template is an editable example, not a content contract. Replace its labels, timings, colors, and layout with evidence from the current reference.

### 5. Build layout before motion

Construct each scene at its most visible state first. Confirm that cards, labels, and connectors fit without animation.

Then animate in reading order:

1. frame and section label
2. first focus node
3. next endpoint
4. connector between visible endpoints
5. supporting cards one at a time
6. state swap or scene transition
7. readable final hold

Keep connectors behind cards. Initialize every SVG connector and junction as hidden at time zero; reveal each only at its cue. A floating connector or junction before its nodes is a failed frame.

Use seek-safe deterministic timelines. Do not use render-time clocks, unseeded randomness, hover state, or infinite animation loops.

### 6. Validate the composition

Run the framework's full check, then capture explicit snapshots at:

- the opening entrance
- every graph or layout state change
- immediately before, during, and after each scene transition
- the final held frame

Inspect the rendered pixels. Fix premature elements, blank handoffs, connector crossings, clipped text, inconsistent borders, and off-brand easing before rendering a full MP4.

### 7. Render and verify the final MP4

Render only when the user's request includes an output video or the user has approved the preview.

Run post-render QC against the MP4 itself, not only the HTML preview. Read [references/qc-checklist.md](references/qc-checklist.md) and preserve:

- media probe JSON
- final-MP4 contact sheet
- representative opening, state-change, transition, and final frames
- black-frame scan result

### 8. Deliver the reusable package

Use this shape:

```text
<project>/
├── frame.md
├── STORYBOARD.md
├── index.html
├── renders/
│   └── motion-replica.mp4
└── qc/
    ├── media-probe.json
    ├── contact-sheet.jpg
    └── representative-frames/
```

Keep the original reference and source-identifying analysis outside this deliverable.

## Completion gates

- Do not claim a match without inspecting multiple timestamps from the requested range.
- Do not claim pixel or frame exactness from this workflow alone; use `rn-replica-qc` for full-frame evidence.
- Do not copy the source's presenter, subtitles, script, thumbnail, or unique branded assets unless the user owns them and explicitly requests reuse.
- Do not allow a connector, junction, or card to appear before its timeline cue.
- Do not treat preview-only correctness as delivery; recheck the final MP4.
- Do not replace the requested video with contact sheets. Contact sheets are QC evidence, not the deliverable.

## Bundled resources

- `scripts/analyze_reference.py`: generate probe data, overview and dense contact sheets, and scene-change frames.
- `scripts/init_motion_project.py`: copy the reusable HyperFrames box-motion project without overwriting an existing directory.
- `references/box-motion-pattern.md`: card, connector, state-swap, and push-transition implementation guidance.
- `references/qc-checklist.md`: pre-render and final-MP4 validation gates.
- `assets/templates/box-motion-hyperframes/`: editable source project used by the initializer.
- `assets/showcases/box-motion-replica-35s.mp4`: 35-second finished example.
