---
name: video-gen
description: Generate, poll, and download short video clips through OpenRouter video models such as alibaba/happyhorse-1.1, google/veo-3.1, bytedance/seedance, Kling, Wan, Grok Imagine, or Sora when Codex needs AI video assets, transitions, intro/outro clips, image-to-video motion, reference-to-video shots, or a production plan for generated video. Use for OpenRouter video API workflows; do not use for factual screencasts or model-evaluation evidence that must come from real artifacts.
---

# Video Gen

Run the examples from the directory containing this `SKILL.md`, or set
`SKILL_ROOT` to that directory:

```powershell
if (-not $env:SKILL_ROOT) { throw 'Set SKILL_ROOT to the runtime-discovered directory containing this SKILL.md.' }
$SkillRoot = (Resolve-Path -LiteralPath $env:SKILL_ROOT).Path
if (-not (Test-Path -LiteralPath (Join-Path $SkillRoot 'scripts\openrouter_video.py'))) { throw 'Invalid video-gen SKILL_ROOT.' }
```

Generate short video assets through OpenRouter's asynchronous video API. Use this skill for stylized intro/outro shots, presentation transitions, image-to-video animations, b-roll, or generated explainer clips.

Do not use generated video to fake evidence. Real UI walkthroughs, dataset folder views, training logs, validation samples, and Grad-CAM/heatmap outputs should come from recorded screens or actual model artifacts.

## Safety

- Never ask the user to paste an API key into chat.
- Use `OPENROUTER_API_KEY` from the local environment. The bundled script checks the current process first and, on Windows, falls back to persistent User/Machine environment variables so Codex sessions started before the key was added can still work.
- Do not write API keys into `SKILL.md`, scripts, prompts, project files, shell history examples, or reports.
- Treat medical, financial, legal, and production screenshots as evidence: generate transitions and supporting visuals, but keep claims tied to real artifacts.
- For medical imaging, label generated heatmap transitions as visual aids unless they were produced by an explainability method such as Grad-CAM on the actual trained model.

## Model Selection

First run model discovery when the current model roster matters:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_video.py') check-key
python (Join-Path $SkillRoot 'scripts\openrouter_video.py') list-models
```

Default choices:

- `alibaba/happyhorse-1.1`: strong default for short text-to-video or first-frame guided clips; supports 720p/1080p and 3-15 seconds.
- `google/veo-3.1` or `google/veo-3.1-fast`: use when available and when high cinematic fidelity or audio matters.
- `bytedance/seedance-2.0`: use for smooth motion, character/reference consistency, and longer visual continuity.
- `kwaivgi/kling-v3.0-pro`: use for controlled image-to-video, first/last frame workflows, and audio-capable clips.
- `openai/sora-2-pro`: use when available for highest-end final shots, with cost and latency explicitly acknowledged.

If the user names a specific model, use that model if `list-models` shows it. If unavailable, report that and choose the closest available model by capability.

## Workflow

1. Decide whether the asset must be factual or generated. Use real screencast/data/model outputs for factual content.
2. Create a shot list: clip purpose, source image if any, prompt, duration, size/aspect, model, and acceptance criteria.
3. Run `list-models` if model availability or pricing is uncertain.
4. Generate short draft clips first: 3-5 seconds at 720p.
5. Use `--first-frame` for image-to-video when preserving a screenshot, title card, heatmap image, or generated still.
6. Poll until completion and download the returned content.
7. Inspect the video before using it: no hallucinated UI, no fake metrics, no unreadable text, no misleading medical implication.
8. Save final project-bound videos in the project or presentation asset folder, not temp.

## Script Usage

Text-to-video:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_video.py') check-key
python (Join-Path $SkillRoot 'scripts\openrouter_video.py') generate `
  --model "alibaba/happyhorse-1.1" `
  --prompt "A clean cinematic transition through abstract medical imaging data, subtle blue-gray light, no text, no logos" `
  --duration 5 `
  --size "1280x720" `
  --out "output/video/medical-transition.mp4"
```

Image-to-video from a first frame:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_video.py') generate `
  --model "alibaba/happyhorse-1.1" `
  --prompt "Slow professional camera push-in, preserve the exact image content, subtle parallax only, no new text" `
  --first-frame "C:\path\to\frame.png" `
  --duration 4 `
  --size "1280x720" `
  --out "output/video/frame-motion.mp4"
```

First-frame to last-frame transition, only for models that list `last_frame` support:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_video.py') generate `
  --model "google/veo-3.1-fast" `
  --prompt "Professional camera move from the first frame to the final logo frame, preserve all readable text exactly, no new text, no watermark" `
  --first-frame "C:\path\to\first.png" `
  --last-frame "C:\path\to\last.png" `
  --duration 4 `
  --size "1920x1080" `
  --out "output/video/transition.mp4"
```

Pass provider-specific parameters only when the selected model supports them:

```powershell
python (Join-Path $SkillRoot 'scripts\openrouter_video.py') generate `
  --model "google/veo-3.1" `
  --prompt "..." `
  --duration 6 `
  --size "1920x1080" `
  --extra-json '{"negativePrompt":"watermark, unreadable text","enhancePrompt":true}' `
  --out "output/video/veo-shot.mp4"
```

## Presentation Planning

For ML/medical demos, use `references/ml-demo-video-plan.md` before generating assets. It separates real evidence from generative polish and gives a recommended shot list for dataset, split, validation examples, Grad-CAM overlays, and summary metrics.

## Output Report

When finished, report:

- model id,
- prompt,
- input frame paths,
- duration and size,
- output video path,
- whether the clip is generated, real screencast, or model-derived evidence.
