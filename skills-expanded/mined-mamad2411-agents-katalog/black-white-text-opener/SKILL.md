---
name: black-white-text-opener
description: >
  Create reusable black-background white-text opening animations for new videos.
  Use when the user asks for "黑底白字开场", "纯黑加白字", "白色文字逐渐出来",
  "一个个字出来", "打字效果", "打字音效", "字体变化开头", "opening title
  animation", "kinetic text opener", or a short black-and-white intro before a
  HyperFrames, Remotion, ffmpeg, SaaS/product, tutorial, commentary, or course
  video. This is for original opener creation, not pixel-level reference
  matching.
---

# Black White Text Opener

## Role

Create a short, reusable opening animation: black background, large white text
that appears one character at a time, synchronized typing click SFX, optional
word replacement, and a clean transition into the main video.

This skill is generative. Do not copy source frames or promise pixel-level
alignment with a reference. If the user asks to exactly match an existing video,
route to `reference-video-replica-qc` first.

## Required Reads

Before building an opener, read:

1. `references/motion-contract.md`
2. `references/timing-presets.md`

Read `references/tool-recipes.md` when choosing HyperFrames, Remotion, or ffmpeg.

## Inputs

Collect or infer:

- main opening phrase
- optional replacement words or contrast words
- final hold phrase, logo text, or next-scene lead-in
- target ratio and resolution
- duration preset: `micro`, `standard`, or `slow`
- tone: cinematic, clean tutorial, product launch, or opinion opener
- transition into the next scene: fade, white velocity wipe, text smear, or cut
- typing cadence and SFX preference, default `14 chars/s` with subtle key clicks

If the user gives only a topic, write 2-3 short phrase options and choose the
cleanest one. Avoid long sentences.

## Defaults

- Duration: `standard` 4.8-5.8s.
- Background: pure or near black, no busy decorative background.
- Text: large white sans-serif, centered or slightly above center.
- Motion: black hold -> white text types in character by character -> phrase
  holds -> replacement text types in -> final typed phrase holds -> transition
  out.
- Audio: quiet typing clicks aligned to visible character appearances. Do not
  add clicks during black hold, final hold, or transition-only frames.
- Build tool: HyperFrames for polished video projects; Remotion when the project
  already uses Remotion; ffmpeg only for simple utility openers.

## Workflow

### 1. Create The Timing Plan

Use the bundled script to generate a deterministic plan:

```bash
python3 scripts/create_opener_plan.py \
  --title "AI workflow engine" \
  --replace "from idea" "to shipped video" \
  --final "Build in minutes" \
  --preset standard \
  --typing-cps 14 \
  --out opener-plan.json
```

Use the plan as the source of truth for scene timing and copy. Do not improvise
new copy during rendering unless the user asks.

### 2. Build The Animation

Follow the motion contract:

- hold black before text appears
- reveal each text state one character at a time
- align typing click SFX to the same character timestamps
- keep the first readable phrase large
- use only 1-3 replacement states
- hold the final phrase long enough to read
- transition out cleanly into the next scene

For dark SaaS/product videos, this opener can precede `dark-saas-magic-video`;
keep the opener simpler than the main product scene.

### 3. QC

Before handoff, verify:

- first frames are black or near black
- characters appear sequentially rather than all at once
- typing clicks line up with the character reveal and stop during holds
- white text is readable at mobile size
- no text clips outside frame
- no accidental colored flash
- no persistent neon-line background
- transition lands before the next scene starts
- media specs match the target project

If this opener is inserted into a longer video, export both the standalone opener
and the full composition when practical.

## Output

Return:

- opener MP4 path or composition path
- timing plan path
- key text states and timestamps
- typing cadence and SFX schedule
- QC notes, especially first-frame blackness and text readability
