---
name: project-audit
description: "Audit ArcGIS Pro projects for broken layers, schema issues, and performance risks"
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


# Project Audit

Scan an ArcGIS Pro project and report actionable issues.

## Inputs

- `project_path` (string, optional)
- `scope` (string, optional: all, active_map)
- `checks` (array, optional)

## Use arcgispro-cli

If available:
- `arcgispro context`
- `arcgispro layers --json`
- `arcgispro connections`

## Output

Findings grouped by severity:
- **Critical**: broken data sources, missing workspaces
- **Warning**: field/schema mismatches, empty layers
- **Info**: heavy layers, slow render risks

Each finding should include: layer name, cause, and suggested fix.

## Example

**User:** “Audit my project for broken layers.”

**Output:** List of broken paths with suggested repair actions.

## Intent

State the operational goal of the skill and what good output should accomplish.

## Outputs

Return a concise, usable result with the key artifacts or recommendations.

## Safety

Do not invent data, credentials, or system context. Flag uncertainty and risky operations clearly.

