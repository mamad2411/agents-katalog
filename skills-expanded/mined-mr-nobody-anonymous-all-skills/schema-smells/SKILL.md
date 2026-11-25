---
name: schema-smells
description: "Detect common schema and data quality smells in GIS layers"
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


# Schema Smells

Identify schema issues that cause brittle analyses or slow performance.

## Inputs

- `layer_names` (array)
- `checks` (array, optional)

## Use arcgispro-cli

- `arcgispro fields "LayerName"`
- `arcgispro layers --json`

## Output

A list of smells with severity and fixes, for example:
- Mixed field types across similar layers
- Nullable ID fields
- Domainless coded values
- Unindexed join fields
- Geometry type mismatches

## Example

**User:** “Check parcels and addresses for schema smells.”

**Output:** 6–10 smells with fixes and priorities.

## Intent

State the operational goal of the skill and what good output should accomplish.

## Outputs

Return a concise, usable result with the key artifacts or recommendations.

## Safety

Do not invent data, credentials, or system context. Flag uncertainty and risky operations clearly.

