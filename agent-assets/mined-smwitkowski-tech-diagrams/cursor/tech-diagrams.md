---
description: Generate publication-quality technical diagrams using Gemini image generation with 536 brand icons and 14 diagram types
alwaysApply: false
---

<!-- Source of truth: SKILL.md at repo root — read it for the complete workflow. -->

# tech-diagrams

Generate publication-quality technical diagrams via Gemini image generation.

## Prerequisites

- Vertex ADC (`GOOGLE_GENAI_USE_VERTEXAI=1`, `GOOGLE_CLOUD_PROJECT`) or `GEMINI_API_KEY` for local dev
- `python3` and `curl` available

## Quick workflow

1. **Choose diagram type** — C1 System Context, C2 Container, C3 Component, Network, Data Flow, Sequence, Comparison, Layered Ecosystem, Cyclical Loop, Decision Tree, Deployment Topology, Concentric Rings, Threat Model, or Use Case Map. Read `references/diagram-types.md` for summaries, then load the deep reference for your type from `references/`.

2. **Load style** — Read the appropriate style from `styles/` (e.g., `styles/google-cloud.md`).

3. **Compose prompt** — Concatenate style block + diagram type instructions + content specifics. Always include an ASCII layout diagram, use actual resource names, include a legend, and specify 16:9 aspect ratio.

4. **Generate** — Write prompt to a temp file, then:
   ```bash
   python3 scripts/build-request.py /tmp/diagram-prompt.txt /tmp/diagram-request.json --provider gcp
   scripts/generate.sh /tmp/diagram-request.json /path/to/output.png
   ```

5. **Verify** — Read the output PNG to visually check labels, layout, and completeness. Adjust prompt and regenerate if needed.

Read `SKILL.md` for the complete rules, density limits, multi-view patterns, and anti-patterns.
