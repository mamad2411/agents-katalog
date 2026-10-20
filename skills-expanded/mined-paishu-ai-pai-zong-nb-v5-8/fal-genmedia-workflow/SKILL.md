---
name: fal-genmedia-workflow
description: Plan fal.ai or genmedia-style image, video, audio, and 3D generation workflows, including model search, schema inspection, prompt routing, async job planning, cost awareness, and downloadable output handling.
---

# fal-genmedia-workflow

## Purpose

Use a structured fal/genmedia workflow when the user wants model-based creative generation and the required tool is available.

## Workflow

1. Identify modality: image, video, audio, voice, 3D, or edit.
2. Decide whether smart routing or explicit model selection is needed.
3. Inspect model inputs before using custom parameters.
4. Plan generation, polling, file handling, and cost checks.
5. If the tool is unavailable, provide prompt packs and execution instructions instead.

## Required Checks

- Do not install CLIs, configure accounts, run paid generation, or transfer local files without confirmation.
- Do not invent endpoint names or prices.
- Do not claim outputs were generated without evidence.

## Output

Return modality, model-selection plan, prompt, parameters to verify, execution checklist, and fallback.
