---
name: symbology-compat
description: "Check symbology compatibility between ArcGIS Pro, AGOL, and target formats"
category: geospatial
domain: geospatial
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "danmaps/gis-agent-skills"
  commit: "47afe3a4b5"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Symbology Compat

Review layer symbology and flag compatibility issues across platforms.

## Inputs

- `target` (string: AGOL, ArcGIS Pro, QGIS, WebMap)
- `layer_names` (array)

## Use arcgispro-cli

- `arcgispro layers --json`
- `arcgispro context`

## Output

- List of unsupported renderers
- Suggestions for alternative symbols
- Notes on labeling and scale dependencies

## Example

**User:** “Will this map work in AGOL?”

**Output:** Flags for unsupported renderers and recommended fallbacks.

## Intent

State the operational goal of the skill and what good output should accomplish.

## Outputs

Return a concise, usable result with the key artifacts or recommendations.

## Safety

Do not invent data, credentials, or system context. Flag uncertainty and risky operations clearly.

