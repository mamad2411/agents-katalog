---
name: random-walk
description: Explore your Obsidian vault through serendipitous discovery. Randomly selects notes, traces connection paths, and suggests research directions. Use when you want to discover forgotten insights, find unexpected connections, or need inspiration for research topics.
---

# Random Walk Skill

Explores your vault serendipitously — randomly selects notes, follows wikilinks, and surfaces forgotten insights and unexpected connections.

## Usage

```bash
python3 _scripts/random_walk.py --save
python3 _scripts/random_walk.py --count 10 --topic "AI"
```

## Options

- `--count N` — Number of random notes to select (default: 5)
- `--topic TEXT` — Focus walk on a specific topic
- `--save` — Save exploration note to vault

## Output

`Sources/Random Walk - YYYY-MM-DD.md` (discovery path, key insights, unexpected connections, research questions, suggested next steps)
