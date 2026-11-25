---
name: ingest
description: GBrain-inspired local-brain ingest for Codex. Use when turning notes, links, meetings, or observations into durable pages under the local brain corpus.
---

# Ingest

Use this skill when the user wants to save material into the local `brain/` corpus.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain writes into a separate brain system. In this repo, ingestion means creating or updating Markdown pages under `brain/`.

## Workflow

1. Identify the primary subject:
   - person
   - company
   - concept
   - original idea
   - source
   - meeting
2. Search for an existing page before creating a new one.
3. Create or update the page with:
   - frontmatter
   - compiled truth
   - timeline evidence
4. Preserve citations or source notes inline when possible.

## Current Upstream Coverage

- Detect notable people, organizations, concepts, ideas, and decisions in every source, including the user's original thinking.
- Preserve the raw source or a durable source pointer before synthesis.
- Route articles, audio/video transcripts, PDFs, screenshots, meetings, and social posts through format-aware extraction.
- Test one representative artifact before bulk ingest and require citations on factual claims.

## Guardrails

- Do not create duplicate pages if a matching one already exists.
- Keep raw evidence separate from synthesized compiled truth.
- Favor small, durable updates over giant dumps of unstructured text.
