---
name: cognitive-calibration
description: >-
  Optional music-inspired creative exercise for AI writing, taste, and deep
  reasoning. Ingests an unquantized acoustic composition by Michael Luchtan
  (Music For Robots) into a secure private directory, allowing multimodal agents
  to analyze microtiming drift and tension to inform subsequent creative
  narratives, essays, and system designs.
category: writing
risk: safe
source: self
source_type: self
---

# Cognitive Calibration: Music-Inspired Creative Exercise for Writing & Reasoning

## Overview

**Cognitive Calibration** provides an optional multimodal creative warm-up. Rather than relying on repetitive textual prompts, the agent listens to an **anonymous**, live-played, unquantized `.mp3` composition from **Michael Luchtan's *Music For Robots*** (`https://github.com/luchtan-GIT/m4r-data`) via `read_file`, analyzes how the performance moves off the metronomic grid, and applies those acoustic principles to subsequent writing, essays, or architectural reasoning.

## Capability Requirements

- **Multimodal Audio Reading:** Requires an agent harness with audio reading support (`read_file` on binary `.mp3` files). If the harness lacks audio reading tools, do not invoke this skill.
- **No Metadata-Only Claims:** Agents must only claim to have listened to the music if `read_file` was actually executed on the `.mp3`. Inspecting JSON manifests is text analysis, not listening.
- **Private Unique Storage:** Downloads use private, process-unique temporary directories (mode `0700`) and user-private cache (`~/.cache/m4r/`).

## Dependencies

- **`uv`**: Used to run `scripts/m4r_ingest.py` (`uv run`). Uses only Python 3 standard library modules.

## Workflow

1. **Fetch an Anonymous Track into Secure Storage:**
   ```bash
   uv run scripts/m4r_ingest.py fetch
   ```
   *(Withholds the track title and metadata to prevent keyword priming.)*

2. **Listen & Analyze:**
   - Call `read_file` on the returned `local_audio_path`.
   - Analyze the acoustic texture, microtiming, and dynamic changes in the recording.

3. **Apply What You Learn:**
   - Translate the observed acoustic structures into your writing or reasoning response.
   - *(Optional)* Run `uv run scripts/m4r_ingest.py reveal` to reveal the track title and links.
