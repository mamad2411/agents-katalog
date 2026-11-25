---
name: chatgpt-image-short-video
description: Method for producing short vertical videos from ChatGPT image generation through a fixed browser tab, local TTS narration, timed subtitle burn-in, cover exports, and a manifest. Use when an operator needs a reproducible image-to-short workflow with pinned session consistency, per-beat visual prompts, 1080x1920 safe-area rules, local ffmpeg/PIL assembly, and private access kept outside the skill.
version: "0.1"
license: MIT
metadata:
  category: plain
  tag:
    - short-video
    - image-generation
    - subtitles
    - media-pipeline
---

# ChatGPT Image Short Video

Use this method to turn a script or content plan into a vertical short video whose primary visual is generated in ChatGPT through an operator-provided fixed browser tab, then assembled locally with narration, burned subtitles, platform covers, and a manifest.

For the full production checklist, prompt pattern, timing rules, render rules, cover contract, and manifest schema, read [references/workflow.md](references/workflow.md).

## Core Workflow

1. Confirm inputs: title, subtitle or hook, spoken script, visual style brief, target language, TTS voice/rate, output directory, and platform metadata.
2. Use the fixed image-generation browser tab supplied by the operator. Do not open a fresh ChatGPT session unless the fixed tab is broken and the operator approves replacement.
3. Generate one primary image or a small set of beat images using the per-beat prompt pattern in the reference.
4. Save generated images as local source assets and record the prompt, browser-tab label, image index, timestamp, and any manual retries.
5. Generate narration locally with TTS and save both media and subtitle sidecar when available.
6. Measure true audio duration with `ffprobe`; derive frame count from audio duration, not expected script length.
7. Align subtitles from TTS sidecar or a local speech-aligner, then split them into readable blocks.
8. Render 1080x1920 frames with safe title/subtitle placement, light motion, and burned subtitles.
9. Encode with `ffmpeg`, mux narration, create 4:3 and 3:4 covers, and write a manifest pointing to every final artifact.
10. Validate that the video, covers, subtitles, and manifest are public-safe and contain no internal handles, local paths, credentials, browser slugs, or draft labels.

## Non-Negotiables

- Fixed-tab access is a private operator setting. Never include actual tab URLs, account names, access tokens, local workspace paths, or handles in reusable output.
- The fixed tab exists for session continuity and image-tool consistency. It isolates image generation from unrelated conversations and reduces style drift across retries.
- Keep the final video at 1080x1920, 24 or 30 fps, H.264, yuv420p, AAC audio, and `+faststart` unless the target platform requires another contract.
- Burn subtitles into the video; do not rely only on external caption files for short-form previews.
- Export both horizontal 4:3 and vertical 3:4 covers as separate files.
- The manifest must use repo- or package-relative artifact paths when possible. Do not serialize machine-local private paths into a portable manifest.
