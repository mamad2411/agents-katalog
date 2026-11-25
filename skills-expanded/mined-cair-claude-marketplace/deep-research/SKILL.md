---
name: deep-research
description: >
  Deep research harness — fan-out web searches, fetch sources, adversarially verify claims,
  synthesize a cited report. When the user wants a deep, multi-source, fact-checked research
  report on any topic. Before invoking, check if the question is specific enough to research
  directly — if underspecified, ask 2-3 clarifying questions to narrow scope.
---

## Overview

Fans out parallel web searches across multiple query angles, fetches and reads primary sources, adversarially verifies key claims, then synthesizes a cited report.

## Usage

Invoke with `/deep-research <question>`. Ask 2–3 clarifying questions if the topic is underspecified before launching the search.

## Process

1. **Clarify** — if the question is vague (no scope, time period, or region), ask up to 3 targeted questions before searching.
2. **Fan out** — run parallel web searches across multiple query angles (different phrasings, date ranges, source types).
3. **Fetch sources** — read primary sources, not just search snippets.
4. **Adversarial verify** — for each key claim, spawn a skeptical agent to find contradicting evidence.
5. **Synthesize** — write a structured report with inline citations.

## Output format

- Executive summary (2–3 sentences)
- Findings by theme, each with citations
- Conflicting evidence or caveats
- Source list with URLs

## Notes

Works best with Claude Sonnet or Opus. Requires internet access via a search MCP tool.
