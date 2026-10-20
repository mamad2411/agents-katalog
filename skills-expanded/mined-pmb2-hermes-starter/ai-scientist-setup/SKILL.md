---
name: ai-scientist-setup
version: 1.0.0
author: Hermes Agent
license: MIT
description: Set up and run SakanaAI AI-Scientist with OpenRouter for free research paper generation
metadata:
  hermes:
    tags: [ai-scientist, sakana, research-paper, paper-generation, openrouter, research-automation]
    triggers: [ai-scientist, sakana, research-paper, paper-generation, openrouter-scientist, automated-research, scientific-paper-generation]
    related_skills: [arxiv, writing-plans]
---

# AI-Scientist Setup & Usage

## Location
**Repo:** `${MY_REPOS}/AI-Scientist/`
**Venv:** `${MY_REPOS}/AI-Scientist/venv/`
**Venv Python:** `${MY_REPOS}/AI-Scientist/venv/Scripts/python.exe`

## OpenRouter Configuration
`.env` file contains:
```
OPENROUTER_API_KEY=sk-or-...a6d9
AI_SCIENTIST_MODEL=openrouter/qwen/qwen3-coder:free
AI_SCIENTIST_IDEA_MODEL=openrouter/openrouter/owl-alpha
AI_SCIENTIST_CODE_MODEL=openrouter/qwen/qwen3-coder:free
AI_SCIENTIST_WRITEUP_MODEL=openrouter/openrouter/owl-alpha
```

**Key principle:** the operator uses FREE models only on OpenRouter. The key `sk-or-...a6d9` is stored in `.env`. The `openrouter/qwen/qwen3-coder:free` and `openrouter/owl-alpha` are the best performing free models for this task.

## MCP Server
Already configured in Hermes `config.yaml` as `ai-scientist`:

```yaml
ai-scientist:
  args:
  - ${MY_REPOS}/Documents/github/AI-Scientist/hermes_mcp_server.py
  - --stdio
  command: ${MY_REPOS}/Documents/github/AI-Scientist/venv/Scripts/python.exe
  env:
    OPENROUTER_API_KEY: ${OPENROUTER_API_KEY}
    AI_SCIENTIST_DIR: ${MY_REPOS}/Documents/github/AI-Scientist
```

## Available Tools (9)
From `hermes_mcp_server.py`:
- `system_status()` — check GPU, venv, templates
- `list_templates()` — available experiment templates
- `read_template_info(experiment)` — template details + seed ideas
- `prepare_baseline(experiment)` — required first step before experiment
- `generate_ideas(experiment, model, num_ideas, num_reflections)` — generate novel ideas
- `list_results(experiment)` — completed results
- `run_experiment(experiment, model, num_ideas, improvement)` — full pipeline
- `review_paper(pdf_path, model)` — review generated paper
- `run_command(command, timeout)` — arbitrary venv command

## Usage Sequence
1. `list_templates()` — see available experiments
2. `system_status()` — verify everything is ready
3. `read_template_info(experiment)` — understand the template
4. `prepare_baseline(experiment)` — run baselines
5. `generate_ideas(experiment)` — generate research ideas
6. `run_experiment(experiment)` — run full pipeline
7. `review_paper(pdf_path)` — review results

## Troubleshooting
- **429 Rate Limited:** Free OpenRouter models have rate limits. Wait and retry with a different model.
- **Free models available:** `qwen/qwen3-coder:free`, `openrouter/owl-alpha` ($0)
- **RTX 3090:** Available for local computation (CUDA_VISIBLE_DEVICES=0)
