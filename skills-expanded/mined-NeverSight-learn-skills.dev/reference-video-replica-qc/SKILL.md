---
name: reference-video-replica-qc
description: >
  Analyze and verify reference-video replication. Use when the user asks to
  recreate, copy, match, align, pixel-align, or compare a video against a
  reference; when a remake is judged "not aligned"; or when a video needs
  frame-by-frame breakdown, side-by-side contact sheets, PSNR/SSIM, hash checks,
  or a clear pixel-level vs visual-level vs style-level fidelity decision.
---

# Reference Video Replica QC

## Role

Make reference-video work evidence-driven. First classify the requested fidelity,
then extract frames, describe the source timeline, compare the candidate, and
only then approve or reject the result.

## Canonical Showcase

- Human display name: Presenton 复刻 Bitexact 成片
- Example finished piece: Presenton replica pixel-aligned bitexact output
- File: `assets/showcases/presenton-replica-pixel-aligned-bitexact.mp4`
- Use this as the repository's reference-video replication showcase. It is the
  correct public example for this skill, replacing older short preview clips.

## Fidelity Levels

Read `references/replica-levels.md` before promising any fidelity level.

- Pixel-level: exact decoded pixels, or exact source stream reuse. Requires hard
  evidence such as matching SHA-256/`cmp`, PSNR infinity, or SSIM 1.0.
- Visual-level: hand-authored recreation that matches scene timing, layout,
  motion, typography, and color closely enough for human review.
- Style-level: uses the reference as a design language, not as a frame target.

Never describe a HyperFrames/Remotion rebuild as pixel-level unless it passes
the hard metrics.

## Workflow

### 1. Establish Inputs

Collect:

- reference video path or URL
- candidate video path, if one exists
- requested fidelity level
- sampling interval, default `0.5s`
- output directory for analysis artifacts

If the URL is private or expired, use the download skill or browser/source page
to retrieve a fresh source before analysis.

### 2. Analyze The Reference

Use `scripts/extract_halfsec_frames.py` or equivalent ffmpeg commands to extract
frames at fixed timestamps. Create contact sheets. Then write a timeline report:

- timestamp
- visible text
- primary subject and position
- transition state
- camera/scale movement
- UI/cursor/button behavior
- notes about typography, color, glow, grain, or background

Do not build from memory. The extracted frames are the source of truth.

### 3. Compare Candidate To Reference

If a candidate exists, use `scripts/compare_videos.py` for hard metrics, then
create side-by-side contact sheets at the same timestamps.

Classify every mismatch:

- timing offset
- scene boundary mismatch
- subject size or position mismatch
- missing/extra transition
- wrong typography or text state
- wrong background or color system
- asset mismatch
- compression/encoding-only difference

### 4. Decide

Approve only if the candidate meets the requested level:

- Pixel-level: hard metrics pass.
- Visual-level: side-by-side frames align at the declared interval, with only
  accepted differences.
- Style-level: the style principles are present; exact timing is optional.

If it fails, produce a repair list ordered by timestamp. Say "not aligned" and
name the first failing timestamp.

## Script Usage

```bash
python3 scripts/extract_halfsec_frames.py reference.mp4 --out analysis/reference
python3 scripts/compare_videos.py reference.mp4 candidate.mp4 --out analysis/compare
```

Use the workspace Python from `load_workspace_dependencies` when Pillow is
needed for labeled contact sheets.

## Outputs

Keep these artifacts near the video project:

- `alignment-report.md`
- source contact sheets
- side-by-side contact sheets
- `comparison-report.md`
- PSNR/SSIM logs when comparing videos
- final pass/fail summary

For content-creation projects, copy the final QC artifacts into the desktop
archive `质检/` folder.
