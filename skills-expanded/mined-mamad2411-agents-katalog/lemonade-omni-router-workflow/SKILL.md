---
name: lemonade-omni-router-workflow
description: Orchestrate multimodal workflows through Lemonade OmniRouter using OpenAI-compatible tool-calling. Use when an agent must analyze images, edit/generate images, transcribe audio, generate speech, and optionally produce a narrated video with ffmpeg.
triggers:
- omni-router
- lemonade
- multimodal
- image analysis
- image editing
- speech synthesis
- transcription
- ffmpeg video
- tool calling
---

# OmniRouter Workflow Skill

Use this skill to integrate Lemonade OmniRouter into any agent without hardcoding specific model IDs or fixed server addresses.

## Scope Boundary

This skill is a foundational capability layer, not a business workflow script.

This skill SHOULD:
- expose OmniRouter tool-calling patterns,
- define capability discovery and fallback rules,
- define reliability and validation requirements.

This skill SHOULD NOT:
- hardcode user-domain prompts,
- hardcode project-specific model names,
- encode one-off business logic for a single dataset.
- require repository-specific helper scripts to be usable.

## No-Business-Script Policy

This skill must remain directly reusable by other agents.

Implementation guidance:
- Prefer describing orchestration contracts over shipping task-specific scripts.
- If examples are needed, keep them minimal and generic, and do not depend on project-local paths.
- Keep runtime adaptation in the caller/executor layer, not in the skill artifact itself.

## When To Use

Use this skill when the user wants one or more of the following in a single workflow:
- Analyze images and identify defects or quality issues.
- Generate or edit images from text prompts.
- Convert narration text to speech.
- Transcribe speech/audio.
- Build a simple narrated video from image sequences with ffmpeg.

Do not use this skill for single-modality, one-off tasks that do not require agentic tool orchestration.

## Core Principles

- Keep orchestration stateless per run.
- Discover capabilities dynamically at runtime.
- Avoid hardcoding model names where possible.
- Keep intermediate artifacts on disk for replay and debugging.
- Separate planning from execution:
  - Planner: decides sequence and parameters.
  - Executor: performs API/tool calls with retries and validation.

## Docs-Aligned Integration Rules

From Lemonade OmniRouter design:
- You bring the LLM loop. Lemonade brings the tools.
- Tools are OpenAI-compatible and should be executed through a normal tool-calling loop.
- Prefer Collection-first operation for best success rate.
- If not using collections, discover models via `GET /v1/models?show_all=true` and match labels.

Canonical tools and endpoints:
- `generate_image` -> `POST /v1/images/generations`
- `edit_image` -> `POST /v1/images/edits`
- `text_to_speech` -> `POST /v1/audio/speech`
- `transcribe_audio` -> `POST /v1/audio/transcriptions`
- `analyze_image` -> `POST /v1/chat/completions` (vision-capable LLM)

## Required Runtime Inputs

- `LEMONADE_BASE_URL` (example: `http://127.0.0.1:13305`)
- `LEMONADE_API_KEY` (optional; set if your server requires auth)
- Input directory of images
- Output directory for repaired images, audio narration, and final video

## Capability Discovery (Mandatory)

Before executing any multimodal chain:
1. Query `GET /v1/models?show_all=true`.
2. Build a capability map from model `labels` (for example image, edit, tts, audio/transcription, vision/tool-calling).
3. Check endpoint availability for:
   - `POST /v1/chat/completions`
   - `POST /v1/images/generations`
   - `POST /v1/images/edits`
   - `POST /v1/audio/speech`
   - `POST /v1/audio/transcriptions`
4. If capabilities are missing, return an explicit fallback plan instead of failing late.

Use the bundled script at `scripts/discover_omni_router_capabilities.py` for capability discovery (canonical implementation).

If needed, platform wrappers are available:
- `scripts/discover_omni_router_capabilities.sh`
- `scripts/discover_omni_router_capabilities.ps1`

## Prompting Boundary (Important)

Do not treat this skill as a place to store business prompts.

Recommended split:
- Skill-level prompts: generic orchestration instructions only (tool ordering, validation, fallback).
- Runtime task prompts: created by the calling agent per user request and input files.
- Tool arguments: derived by the LLM at runtime, validated by executor.

In other words, this skill should expose tools and process constraints; the LLM should decide task-specific prompts and parameters at call time.

### What To Keep In Skill vs Runtime

Keep in skill:
- output schema requirements (for example analysis JSON fields),
- guardrails (path safety, retry limits, quality checks),
- capability checks and fallback policy.

Keep at runtime:
- style/content prompts for image generation or edits,
- narration tone and language,
- per-job constraints and acceptance criteria.

## Suggested Execution Pattern

1. Discover capabilities.
2. Load task manifest (input images, desired style/repair rules, narration style, video settings).
3. For each image:
   - Analyze image and produce a structured issue report.
   - Repair/regenerate image if needed.
   - Save output plus metadata JSON.
4. Produce a scene-level summary and a final narration script.
5. Call TTS to generate narration audio.
6. Build slideshow-style video with ffmpeg.
7. Emit a run report with:
   - files generated
   - per-step durations
   - retries and failures
   - final quality checks

## OpenAI-Compatible Tool Loop

Your agent should run the standard tool-calling loop:
1. Send user request + tool definitions to `POST /v1/chat/completions`.
2. Parse returned `tool_calls`.
3. Execute each call against the mapped Lemonade endpoint.
4. Return tool results as `tool` messages.
5. Repeat until final assistant response.

Tool definitions should match Lemonade OmniRouter definitions from official docs.

If a local copy of tool definitions is unavailable, construct equivalent tool schemas from the official endpoint contract and keep names stable for model consistency.

## Reliability Rules

- Add bounded retries with exponential backoff for network/5xx failures.
- Persist every intermediate file before moving to next stage.
- Validate output existence and file size at each stage.
- Prefer idempotent naming:
  - `image_0001.original.*`
  - `image_0001.fixed.*`
  - `image_0001.meta.json`
- On partial failure, continue with remaining images and summarize skipped items.

- Avoid hard-failing the entire run when one modality is unavailable; degrade gracefully according to fallback policy.
- Prefer downloaded models for each required label to reduce first-call startup and fetch-related failures.

## Quality Gate Suggestions

- Image analysis must output structured JSON with at least:
  - `defects`
  - `severity`
  - `repair_plan`
- Repaired image should pass a second analysis check.
- TTS output should have non-zero duration.
- ffmpeg output should include all expected frames/scenes.

## Fallback Strategy

If any capability is unavailable:
- Missing image-edit model: switch to image-generation replacement workflow.
- Missing TTS model: output narration text and skip audio/video merge.
- Missing transcription model: skip STT validation but keep TTS and video.

Always report which fallback path was selected and why.

## Practical Reliability Notes

- Capability probe semantics:
  - For endpoint probes with minimal/invalid payload, `400` can still mean endpoint exists.
  - Treat `404/405` as unavailable, not generic non-2xx statuses.
- TTS robustness:
  - First speech call may fail transiently during backend startup; apply bounded retries.
  - If multilingual text fails due encoding/locale mismatch, retry with normalized UTF-8 text or a short ASCII-safe fallback.
- ffmpeg interoperability:
  - When generating concat input files on Windows, write ASCII/UTF-8 (not UTF-16) to avoid parse failures.
  - Validate concat file syntax (`file ...`, `duration ...`) before invoking ffmpeg.
- Encoding hygiene:
  - Keep text artifacts UTF-8 and avoid mixed code pages in intermediate files.
  - Validate narration text readability before sending to TTS.

## Security And Safety

- Do not log secrets or API keys.
- Keep all paths explicit and sanitized.
- Reject path traversal in user-provided filenames.
- Keep generated media in a dedicated output root.

## Minimal Deliverables Per Run

- `run_manifest.json`
- `analysis/*.json`
- `images_fixed/*`
- `audio/narration.wav` (or mp3)
- `video/summary.mp4` (if ffmpeg stage enabled)
- `run_report.md`

## Success Checklist

- Capability report exists and indicates endpoint readiness.
- At least one vision-capable model and one tool-calling-capable LLM are discoverable.
- Required modality labels are present for requested tools.
- Tool loop returns either successful outputs or an explicit fallback report.

## Fast Validation Checklist

Use this short checklist before first real run in any new environment:
1. Read this skill and confirm required inputs are provided.
2. Run capability discovery and confirm endpoint/label readiness.
3. Run live smoke tests for runnable modalities.
4. Select downloaded models first for each required modality.
5. Start production workflow only after smoke calls succeed.

Suggested commands:

```bash
python scripts/discover_omni_router_capabilities.py --strict-ready --out-file ./omni_capabilities.json
python scripts/smoke_test_omni_router.py --strict --out-file ./omni_smoke_test.json
```

## Agent Consumption Contract

When another agent loads this skill, treat the following as mandatory preflight:
1. Execute discovery in strict mode.
2. Execute smoke test in strict mode.
3. Persist both JSON reports in the working directory.
4. If either check fails, produce a fallback plan and stop short of full production run.

This contract keeps behavior deterministic across different hosts and model inventories.

## Operator Notes

- If the user asks for fully autonomous mode, keep planning in the LLM and execution in deterministic tool adapters.
- If the user asks for maintainability, pin the workflow schema, not specific model IDs.
- If the user asks for portability, externalize endpoint and auth via environment variables only.
