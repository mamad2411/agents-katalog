---
name: brain-ops
description: Brain-first local memory workflow for Codex. Use to search, update, cite, or cross-link the local brain before outside research or after new user signal.
---

# Brain Ops

Use this skill when the user wants memory-grounded work and the local `brain/` corpus should influence the response or capture new context.

This port is adapted from `garrytan/gbrain` at commit `0b47afbf402a4e27a648bb9d131ce584461461ea`.

## Important Adaptation

Upstream GBrain treats brain ops as an ambient behavior layer. In this repo, the equivalent is an explicit workflow backed by local file operations:

- `python3 scripts/brain_search.py "<query>"`
- `python3 scripts/brain_put.py ...`
- `python3 scripts/brain_link.py ...`
- `python3 scripts/brain_citations.py`

## Workflow

1. Check the local brain first:
   - search for the entity, topic, or project
   - read the top matching pages before doing outside research
2. If the user shared new information, write it back:
   - create or update the right page under `brain/`
   - add a dated timeline entry
3. Maintain graph hygiene:
   - add backlinks for referenced people, companies, meetings, or concepts
   - keep inline `[Source: ...]` citations on any new fact
4. Answer or continue the task using the retrieved context.

## Current Upstream Coverage

Enforce the brain-first loop on inbound and outbound work: read relevant context, enrich or write durable signals, update structured relationships, then answer from refreshed context. Every new durable page must backlink to its source or parent context; cross-source answers must identify which source supports each claim.

## Guardrails

- Do not claim this is always-on ambient capture; run it deliberately.
- Do not use external research before checking the local brain when the task is memory-sensitive.
- Do not invent citations or backlinks just to satisfy formatting.
