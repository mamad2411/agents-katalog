<!-- Source of truth: SKILL.md — read it for the complete workflow, rules, and reference docs. -->

# tech-diagrams

Generate publication-quality technical diagrams using Gemini image generation.

## Setup

- Auth: Vertex ADC (`GOOGLE_GENAI_USE_VERTEXAI=1`, `GOOGLE_CLOUD_PROJECT`) or `GEMINI_API_KEY` for local dev
- Requires `python3` and `curl`

## Usage

Read `SKILL.md` for the complete workflow including:
- Diagram type selection (14 types: C1–C3, network, data flow, sequence, and more)
- Style system (Google Cloud, Azure, AWS)
- Icon library (536 icons auto-injected via `scripts/build-request.py`)
- Prompt composition rules (ASCII layout, density limits, anti-patterns)
- Generation via `scripts/generate.sh`
- Multi-view diagram sets for complex flows

## Gemini Enterprise

GE remote agent hosting is **not** in this repo — see internal [66degrees/tech-diagrams-agent](https://github.com/66degrees/tech-diagrams-agent).
