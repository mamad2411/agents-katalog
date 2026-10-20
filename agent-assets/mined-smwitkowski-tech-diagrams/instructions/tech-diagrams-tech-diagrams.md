---
applyTo: "**/*.{png,diagram,arch}"
---

<!-- Source of truth: SKILL.md at repo root — read it for the complete workflow. -->

# tech-diagrams

Generate publication-quality technical diagrams via Gemini image generation.

## Prerequisites

- `GEMINI_API_KEY` environment variable set
- `python3` and `curl` available

## Quick workflow

1. **Choose diagram type** — Read `references/diagram-types.md` for the 14 supported types, then load the deep reference from `references/`.

2. **Load style** — Read from `styles/` (e.g., `styles/google-cloud.md`).

3. **Compose prompt** — Concatenate style block + diagram type instructions + content specifics. Always include an ASCII layout diagram, use actual resource names, include a legend, and specify 16:9 aspect ratio.

4. **Generate** — Write prompt to a temp file, then:
   ```bash
   python3 scripts/build-request.py /tmp/diagram-prompt.txt /tmp/diagram-request.json --provider gcp
   scripts/generate.sh /tmp/diagram-request.json /path/to/output.png
   ```

5. **Verify** — Read the output PNG to visually check labels, layout, and completeness.

Read `SKILL.md` for the complete rules, density limits, multi-view patterns, and anti-patterns.
