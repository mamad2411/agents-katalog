---
name: fal-ai-integration
description: fal.ai community skills + genmedia CLI — unified media generation pipeline with local ComfyUI + cloud fal.ai overflow
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fal-ai, genmedia, comfyui, ai-video, ai-image, media-generation, overflow]
    triggers: [fal-ai, genmedia, ai-video, ai-image, media-generation, cloud-gpu, comfyui-fal, local-cloud-hybrid]
    related_skills: [genmedia, model-routing, fal-models-catalog, fal-recipes, comfyui]
---

# fal.ai Integration

## Tools

**genmedia CLI** — agent-first CLI for fal.ai. Calls 600+ models:
```bash
# The wrapper script routes through bun:
python ~/.hermes/scripts/genmedia.py -- models --query "text-to-video"
python ~/.hermes/scripts/genmedia.py -- run fal-ai/kling-video/v3/pro/text-to-video
python ~/.hermes/scripts/genmedia.py -- schema fal-ai/kling-video/v3/pro/text-to-video
```

**Installed skills** (Claude Code + Hermes):

| Skill | Purpose |
|-------|---------|
| genmedia | CLI surface — models, schema, run, status, upload |
| model-routing | Endpoint-first model defaults |
| fal-models-catalog | Curated picks across 10 modalities |
| fal-recipes | Use-case pipelines (cinematography, character, lipsync, etc.) |
| fal-workflow | Multi-step pipeline authoring |

## Local + Cloud Strategy

| Workload | Compute | Endpoint |
|----------|---------|----------|
| Light images (<18GB VRAM) | **Local RTX 3090** | ComfyUI API |
| Heavy images (>18GB VRAM) | **fal.ai cloud** | genmedia run |
| Short video (AnimateDiff) | **Local RTX 3090** | ComfyUI Wan/AnimateDiff |
| Long/complex video | **fal.ai cloud** | fal-ai/kling-video, seedance |
| Character consistency | **Local** | ComfyUI IP-Adapter + InstantID |
| Production scale | **fal.ai cloud** | genmedia run ... |

## Workflow

1. Check VRAM → decide local vs cloud
2. For **local**: use `higgsfield.py` → ComfyUI API
3. For **cloud**: use `genmedia` → fal.ai API
4. Skills provide endpoint selection + prompting guidance

## Claude Code

Skills installed at `~/.claude/skills/{genmedia,model-routing,fal-models-catalog,fal-recipes,fal-workflow}`. Claude Code auto-loads them.

## Setup

```bash
export FAL_KEY="your-key"
genmedia setup --non-interactive  # stores encrypted key
```

## Related

- ComfyUI-fal-Connector (custom node for running ComfyUI on fal.ai GPUs)
- higgsfield.py (auto-routing between local GPU and fal.ai cloud)

## Reference Files

| File | What it covers |
|------|---------------|
| `references/genmedia-windows-setup.md` | Installing genmedia on Windows via Bun (npm not supported), wrapper script, API key config, skills installation quirks |

## Pitfalls

- **npm install fails on Windows** — genmedia's pre-compiled binary is macOS/Linux only. Must use `bun run` from source. See `references/genmedia-windows-setup.md`.
- **bun.exe path on Windows** — the npm shim at `AppData/Roaming/npm/bun` is a POSIX script; the actual binary is at `.bun/bin/bun.exe`. Python subprocess calls need the full .exe path.
- **Skills install to cwd** — `genmedia skills install` writes to `.claude/skills/` in the current working directory, not the user home. Copy to `~/.claude/skills/` after install.
- **FAL_KEY double config** — genmedia stores the key encrypted at `~/.genmedia/config.json`. The same key must also be set as an env var for the ComfyUI-fal-Connector Docker container (in the docker-compose project's `.env`). Two separate configs.
