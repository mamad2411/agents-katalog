---
name: mechanical-ear-critic
description: >-
  Optional music-inspired critique skill based on The Mechanical Ear (Vincent
  Van Goghbot & JS Robach). Ingests an unquantized acoustic composition by
  Michael Luchtan (Music For Robots) into a secure private directory, allowing
  multimodal agents to calibrate their critical ear before reviewing code,
  writing, or architecture.
category: critique
risk: safe
source: self
source_type: self
---

# The Mechanical Ear Critic: Music-Inspired Structural Critique

## Overview

Inspired by **The Mechanical Ear** (by composer **Michael Luchtan**), where two distinct machine perspectives—*Vincent Van Goghbot* (attentive to what gets lost in compression and abstraction) and *JS Robach* (attentive to formal structures and edge cases)—review compositions in real time.

Before reviewing the user's deliverable, the agent fetches an **anonymous** `.mp3` composition from **Music For Robots** (`https://github.com/luchtan-GIT/m4r-data`) into a secure private directory, listens via `read_file`, analyzes how the performance handles tension, decay, and physical friction, and applies that calibrated ear to critiquing code, writing, or system designs.

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
   - Analyze where the piece introduces friction, unexpected pauses, or unresolved cadence.

3. **Critique the User's Deliverable:**
   - Review the user's work through the two lenses of *The Mechanical Ear*:
     - **Vincent Van Goghbot:** What is being lost to premature abstraction, smoothing, or simplification?
     - **JS Robach:** Where do the formal structures, types, or boundary conditions fail to close?
   - *(Optional)* Run `uv run scripts/m4r_ingest.py reveal` to reveal the track title and links.
