---
name: autoresearch
description: >
  Automatically detects when a user question needs web research and performs it
  without requiring an explicit command. Use when the user asks a factual question
  that likely requires current or external information and has not explicitly
  invoked a research command.
---

## Overview

Monitors incoming questions and proactively performs web research whenever the answer requires current, external, or domain-specific knowledge that Claude may not have reliably in training data. No explicit command needed — it triggers automatically.

## Usage

Simply ask a question. The skill judges whether web research is needed and, if so, searches silently before answering:

```
"What's the current state of transformer efficiency research?"
"Which GPU is best for fine-tuning a 70B model in 2025?"
```

To suppress auto-research for a single turn, prefix your message with `(no-search)`.

## Behavior

1. Classifies the query: does it need fresh or verifiable external data?
2. If yes, runs 2–4 targeted web searches in parallel.
3. Reads top sources and extracts relevant facts.
4. Answers inline, citing sources at the bottom.
5. If no research needed, answers from model knowledge — no latency overhead.

## Trigger heuristics

Research fires on queries about:
- Dates, versions, prices, benchmarks, current events
- Specific people, papers, datasets, or tools not in wide training coverage
- "Best X for Y" questions with recency sensitivity

Research is skipped for:
- Conceptual or definitional questions answerable from training data
- Code generation, math, and logic tasks
- Follow-up clarifications in an active conversation

## Notes

Pairs well with `deep-research` for topics that need full adversarial verification. `autoresearch` is the lightweight, always-on layer; `deep-research` is the deep-dive harness.
