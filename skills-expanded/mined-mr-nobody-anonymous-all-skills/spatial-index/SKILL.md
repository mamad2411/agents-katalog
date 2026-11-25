---
name: spatial-index
description: "Recommend and apply spatial index strategies for GIS datasets"
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


# Spatial Index

Recommend or apply spatial indexing to improve query performance.

## Inputs

- `dataset` (string)
- `platform` (string, optional: file_gdb, enterprise_gdb, shapefile)
- `operation` (string, optional: create, rebuild, check)

## Output

- Recommended index action
- Expected impact
- Exact ArcPy commands if applicable

## Example

**User:** “Create spatial index for Parcels in a file geodatabase.”

**Output:** ArcPy AddSpatialIndex step with warnings about locks.

## Intent

State the operational goal of the skill and what good output should accomplish.

## Outputs

Return a concise, usable result with the key artifacts or recommendations.

## Safety

Do not invent data, credentials, or system context. Flag uncertainty and risky operations clearly.

