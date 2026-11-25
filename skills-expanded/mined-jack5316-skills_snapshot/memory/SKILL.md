---
name: memory
description: Memory Consolidator - Persist information to LLM/Agent memory. Add preferences, facts, patterns, and workflows to your LLM Context folder for Kilo Code and AI assistants to remember permanently. Use when asked to remember something, save a preference, or store information for later.
---

# Memory Skill

Persists preferences, facts, patterns, and workflows to `LLM Context/` for permanent AI assistant memory across sessions.

## Usage

```bash
python3 _scripts/memory_consolidator.py --summary
python3 _scripts/memory_consolidator.py --preference "I like concise answers" --desc "Prefer brevity"
```

## Options

- `--summary` — Show memory summary and statistics
- `--preference TEXT` — Add a preference (use with `--desc`)
- `--fact TEXT` — Add a fact (use with `--source`)
- `--pattern TEXT` — Add an observed pattern (use with `--desc`)
- `--workflow TEXT` — Add a workflow (`name,step1,step2,...`)
- `--list` — List all memory files (`--category` to filter)
- `--search TEXT` — Search memories containing text

## Output

Files saved to `LLM Context/` organized by category (Preferences, Facts & Knowledge, Workflows & Processes, Patterns & Learnings, etc.)
