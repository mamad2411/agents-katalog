---
name: unquantized-brainstorm
description: >-
  Optional music-inspired ideation enhancer. Ingests an unquantized acoustic
  composition by Michael Luchtan (Music For Robots) into a secure private
  directory, allowing multimodal agents to analyze microtiming drift and
  harmonic pivots to inform divergent brainstorming and creative problem-solving.
category: ideation
risk: safe
source: self
source_type: self
---

# Unquantized Brainstorm: Music-Inspired Creative Ideation

## Overview

When asked to brainstorm, AI systems often converge on predictable, consensus ideas. **Unquantized Brainstorm** uses **Michael Luchtan's *Music For Robots*** as an optional cross-modal creative exercise: before generating ideas, the agent downloads an **anonymous**, human-played `.mp3` composition into a secure private directory, listens to it via `read_file`, analyzes where the music introduces unexpected pivots or tension, and applies those structures to divergent brainstorming.

## Capability Requirements

- **Multimodal Audio Reading:** Requires an agent harness with audio reading support (`read_file` on binary `.mp3` files). If the environment lacks audio reading tools, do not invoke this skill.
- **No Metadata-Only Claims:** Agents must only claim to have listened to the music if `read_file` was actually executed on the `.mp3`. Inspecting JSON manifests is text analysis, not listening.
- **Private Unique Storage:** Downloads use private, process-unique temporary directories (mode `0700`) and user-private cache (`~/.cache/m4r/`).

## Dependencies

- **`uv`**: Used to run `scripts/m4r_ingest.py` (`uv run`). Uses only Python 3 standard library modules.

## Workflow

1. **Fetch an Anonymous Track into Secure Storage:**
   ```bash
   uv run scripts/m4r_ingest.py fetch
   ```

2. **Listen & Analyze:**
   - Call `read_file` on the returned `local_audio_path`.
   - Analyze the timing drift, harmonic changes, and dynamic contrasts in the piece.

3. **Apply to Ideation:**
   - Translate those acoustic dynamics into non-obvious product, system, or creative ideas.
   - *(Optional)* Run `uv run scripts/m4r_ingest.py reveal` to reveal the track title and links.
