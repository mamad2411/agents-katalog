---
name: sample-qa-skill
description: "Minimal Q&A skill example with clear inputs and outputs"
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


# Sample QA Skill

A tiny example skill that answers a question succinctly.

## Inputs

- `question` (string)

## Output

- `answer` (string)

## Example

**User:** “What is a geodatabase?”

**Output:** “A geodatabase is Esri’s container format for storing spatial data, tables, and relationships.”

## Intent

State the operational goal of the skill and what good output should accomplish.

## Outputs

Return a concise, usable result with the key artifacts or recommendations.

## Safety

Do not invent data, credentials, or system context. Flag uncertainty and risky operations clearly.

