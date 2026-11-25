---
name: setup-topic-scout
description: Interview a user about a research topic and initialize AI Topic Scout. Use when topic.json is missing, when starting a new research workspace, or when the user wants generated agent roles, scout skills, queries, taxonomy, and inclusion/exclusion rules.
---

# Setup Topic Scout

At the beginning of setup, collect the user's raw intent and initialize the LLM refinement step.
Do not use a sentence-length intent directly as the topic title.

Ask the user for one complete intent that covers, where known:

1. topic or research question;
2. business decision or outcome;
3. audience and domain or policy constraints;
4. evaluation concerns and agent-system design concerns.

Then run `python3 scripts/init_topic.py --intent "..."` with explicit flags or interactively.
Pass additional known answers as optional constraints; do not delay refinement to conduct a full
manual taxonomy interview.
Normal setup uses `codex exec` and the Codex CLI's saved ChatGPT subscription login. If Codex is
not authenticated, run `codex login`. Use `--provider api` only when direct API usage is requested,
and use `--offline` only when deterministic initialization without LLM refinement is requested.

The refined contract must contain:

- a concise title and explicit research question;
- business purpose, domain constraints, and policy requirements;
- evaluation dimensions and agent-system design concerns;
- dashboard sections, taxonomy, and evidence types;
- direct, adversarial, and citation-graph scouting queries and strategy.

Verify that initialization creates:

- `topic.json`
- `AGENTS.md`
- `agents/*.md`
- `skills/topic-paper-scout/SKILL.md`
- `skills/analyze-research-gaps/SKILL.md`
- `data/papers.json`

Do not start broad scouting until the user confirms the generated topic contract.
