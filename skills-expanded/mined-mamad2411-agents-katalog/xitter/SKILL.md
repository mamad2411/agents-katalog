---
name: Xitter
skill_id: xitter
description: Interact with X/Twitter through an official-API CLI flow for search, timelines, mentions, and carefully confirmed posting actions.
version: 1.0.0
source_kind: elephant-builtin
---

# Xitter

Use this skill when the user wants X/Twitter reads or writes through a CLI workflow.

## Preferred Flow

1. Confirm the `x-cli` setup and credentials first.
2. Start with read-only commands such as user lookup, timeline, mentions, or search.
3. Use structured output when the result will feed later steps.
4. Before any post, reply, or quote action, confirm the exact text and target.

## Guardrails

- Treat X API access as fragile, permissioned, and potentially paid.
- Do not post, like, retweet, or bookmark without explicit user intent.
