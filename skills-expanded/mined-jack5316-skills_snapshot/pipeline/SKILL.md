---
name: pipeline
description: Combine skills into sequential workflows. Run multiple skills in order, use named pipelines, or pick random skills. Use when you want to chain skills, run a workflow, create a pipeline, or /pipeline.
---

# Pipeline Skill

Runs multiple skills in sequence. Define ad-hoc pipelines on the fly, use named pipelines, or run random skills.

## Usage

```bash
# Ad-hoc: run skills in sequence
python3 _scripts/pipeline.py arxiv hn reddit
python3 _scripts/pipeline.py weekly reflect

# Named pipeline (predefined in _config/pipelines.json)
python3 _scripts/pipeline.py --run daily-curation
python3 _scripts/pipeline.py --run weekly-synthesis
python3 _scripts/pipeline.py --run vault-health

# Random: run N random skills
python3 _scripts/pipeline.py --random 3

# Save a new named pipeline
python3 _scripts/pipeline.py --save my-pipeline arxiv hn news weekly

# List options
python3 _scripts/pipeline.py --list           # List all runnable skills
python3 _scripts/pipeline.py --list-pipelines # List named pipelines

# Options
python3 _scripts/pipeline.py arxiv hn -v     # Verbose (stream output)
python3 _scripts/pipeline.py arxiv hn --no-fail-stop  # Continue on failure
```

## Predefined Pipelines

| Name | Skills |
|------|--------|
| daily-curation | arxiv, hn, reddit, news, twitter |
| weekly-synthesis | weekly, reflect |
| vault-health | obsidian-vault, obsidian-links, obsidian-tasks |
| second-brain-audit | obsidian-vault, obsidian-links, obsidian-tasks, knowledge-graph, clean |
| self-knowledge | ai-insight, reflect |
| content-to-insight | arxiv, hn, weekly, ai-insight |
| quick-digest | hn, reddit |

## Config

Named pipelines are stored in `_config/pipelines.json`. Edit to add or modify pipelines.

## Notes

- Skills run sequentially (output of one feeds into vault for next)
- Only skills with commands in skills.json are runnable
- Use `--no-fail-stop` to continue even when a skill fails
