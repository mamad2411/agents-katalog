---
name: data-research
description: GBrain-inspired structured research for Codex. Use when the user wants tracked extraction, recurring data collection, or a canonical tracker built from files, connectors, or web sources.
---

# Data Research

Use this skill when the user wants a research pipeline that extracts structured information into a durable tracker.

This port is adapted from `garrytan/gbrain` at commit `b7e3005b5b3f1b54082f9c5990482ebf81a4a807`.

## Workflow

1. Define the research target and tracker schema.
2. Search the relevant sources:
   - local files
   - Gmail or other connectors
   - web sources
   - structured APIs when available
3. Save raw evidence before summarizing.
4. Extract structured fields.
5. Deduplicate before adding to the tracker.
6. Update the canonical tracker file or report.

## Guardrails

- Save evidence before relying on memory or summary text.
- Do not append duplicate rows without checking.
- Keep the tracker schema stable across runs.
