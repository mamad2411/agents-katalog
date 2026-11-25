---
name: model-scout
description: Discovers and recommends AI models via the OpenRouter API. Matches task requirements (cost, speed, capabilities, context length, modality) to available models. Use when the user needs to choose a model, compare models, validate model IDs, or when selecting a model for a new script.
---

# Model Scout

Discover and recommend AI models from OpenRouter based on task requirements.

---

## Activation

This skill activates when user:

- Asks "which model should I use for X"
- Wants to compare models side-by-side
- Needs the cheapest/fastest/best model for a task
- Wants to validate that model IDs in `ai-models.md` are still current
- Is building a new script and needs to select a model

---

## Operations

| Operation | Description | Command |
| --- | --- | --- |
| Recommend | Score and rank models for a task | `recommend` |
| Compare | Side-by-side comparison of specific models | `compare` |
| Audit | Validate and improve `ai-models.md` | `audit` |

---

## Quick Start

```bash
# Recommend models for a task
uv run .claude/skills/model-scout/scripts/scout.py recommend \
    --task "summarize 500 documents cheaply"

# With specific requirements
uv run .claude/skills/model-scout/scripts/scout.py recommend \
    --task "agent with tool calling" \
    --needs tools,reasoning \
    --min-context 128000 \
    --top 5

# Compare specific models
uv run .claude/skills/model-scout/scripts/scout.py compare \
    --models anthropic/claude-sonnet-4 google/gemini-2.5-flash-preview openai/gpt-4o

# Audit ai-models.md for stale entries
uv run .claude/skills/model-scout/scripts/scout.py audit --suggest-updates
```

---

## CLI Arguments

### `recommend`

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--task` | str | required | Natural language task description |
| `--needs` | str | none | Required capabilities (comma-separated): `tools`, `reasoning`, `vision`, `structured_outputs`, `audio` |
| `--min-context` | int | 0 | Minimum context window in tokens |
| `--max-cost` | float | none | Max combined cost per 1M tokens (prompt + completion USD) |
| `--top` | int | 5 | Number of results to show |
| `--all-providers` | flag | false | Remove core-three provider bias for full exploration |
| `--json` | flag | false | Output as JSON |

### `compare`

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--models` | str[] | required | 2-5 model IDs to compare |
| `--json` | flag | false | Output as JSON |

### `audit`

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--suggest-updates` | flag | false | Print a ready-to-paste replacement table |
| `--json` | flag | false | Output as JSON |

---

## How Scoring Works

Models are scored across 5 dimensions (0-100 each) with dynamic weights:

| Dimension | What | Default Weight |
| --- | --- | --- |
| Provider tier | Core three (OpenAI/Google/Anthropic) = 100, others = 50 | 15% |
| Cost | Log-scale inverse of prompt+completion per 1M tokens | 25% |
| Context | Size relative to requirement | 15% |
| Capabilities | Required params met + bonus for extras | 20% |
| Quality | Name-based tier lookup (opus=95, sonnet=80, flash=65, etc.) | 25% |

Weights shift based on task signal words (e.g., "cheap" boosts cost weight to 35%).

---

## Environment

| Variable | Description |
| --- | --- |
| `OPENROUTER_API_KEY` | API key from OpenRouter |
