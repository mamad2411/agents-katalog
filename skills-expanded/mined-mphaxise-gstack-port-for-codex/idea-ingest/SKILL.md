---
name: idea-ingest
description: GBrain-inspired source and idea ingest for Codex. Use when the user shares a local file, fetched text, or article notes that should become a durable brain artifact.
---

# Idea Ingest

Use this skill when the user wants to save a source, article, memo, quote set, or other text-bearing artifact into the local `brain/` corpus.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain can fetch directly from the network and upload raw artifacts to its own backing store. In this repo, idea ingest is grounded in material already available to Codex:

- a local file
- fetched text already present in the workspace
- notes copied into a file

Primary helper:

- `python3 scripts/brain_ingest_source.py <file> --title ... --category ...`

## Workflow

1. Make sure the source text is actually available locally.
2. Choose the primary subject category instead of dumping everything into `sources`.
3. Ingest the source file and preserve the raw copy.
4. If the author matters, create or update their people page.
5. Add explicit related entities when confidence is high.
6. Follow with `enrich` if the ingest needs deeper synthesis.

## Current Upstream Coverage

Separate source context, concise summary, key claims/data, analysis, and open questions. Preserve uncertainty and provenance instead of smoothing an early idea into a finished thesis.

## Guardrails

- Do not claim a URL was ingested unless the content was actually fetched.
- Do not create duplicate pages when a relevant page already exists.
- Do not preserve raw text without also adding a readable summary or analysis stub.
