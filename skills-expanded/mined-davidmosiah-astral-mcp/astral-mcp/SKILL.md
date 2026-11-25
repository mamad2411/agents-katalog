---
name: astral-mcp
description: >-
  Compute precision-audited astrology with the local astral MCP server: natal charts with houses and aspects, current transits, synastry between two people and moon phase. Use when the user asks for a birth chart, rising or moon sign, transits, compatibility or synastry, or the current moon phase. Presents astrology as symbolic reflection, not prediction.
---

# Astral

MCP server `astral` from the `astral-mcp@0.3.2` npm package, run locally through `npx`. It reads natal charts (planets, houses, aspects, chart signature, precision audit), transits, synastry and moon phase. Data source: local ephemeris computation (circular-natal-horoscope-js cross-checked with astronomy-engine); astral_search_birthplace looks up place names to coordinates.

## Workflow

1. Start with `astral_demo`. Then pick what fits the question: `astral_search_birthplace`, `astral_compute_natal_chart`, `astral_current_transits`.
2. Lead with the answer to the user's question and keep supporting detail short.

## Setup (the user runs this in a terminal, not in chat)

No setup and no keys.

## Safety

- Present astrology as symbolic and reflective, not as prediction or advice for health, money or legal decisions.
- Birth date, time and place identify a person: use them only for the chart the user asked for.
