---
name: harvest-adaptive
description: Adaptive content summarization - auto-detect content type and produce relevant summary. Grok-native with Production Contract.
keywords: [harvest, adaptive, summarization, content-type, web, docs]
---

# Harvest Adaptive — Grok Edition

Adaptive content summarization skill. Automatically detects content type (article, docs, product, code, etc.) and produces high-quality, relevant summaries with structure.

## When to Use
- Web crawling or research tasks where content varies.
- Before feeding long pages into LLM context (token savings).
- Harvesting competitor sites, docs, or forum threads.

## Grok Integration (Production Contract — Mandatory)
- Use with layered-recall / memory-palace for storing summaries as L2/L3 facts.
- Friction capture on poor summaries (compound learns better prompts).
- Preflight for large crawls.
- Handoff structured summaries to downstream agents (researcher, analyst).
- Claim-verif: two-pass on any " this page says X\ assertion (read the extracted text).
- Hooks: on_harvest_complete, on_pre_compact (save partial summaries).

## Core Logic (Adaptive)
1. Detect type (title, structure, keywords, url patterns).
2. Choose summarizer template (news: who/what/when; docs: sections + key facts; product: features/pricing; code: purpose + API surface).
3. Output: title, 1-sentence tl;dr, bullet key points, entities, suggested next actions.
4. Confidence score + token count before/after.

## References
- harvest-single, harvest-deep-crawl, harvest-structured (specialized siblings).
- tldr-cli for code/docs.
- Pre-flight + handoff templates.

This skill is part of the full harvest family. Always prefer adaptive first unless the user specifies a sub-type.
