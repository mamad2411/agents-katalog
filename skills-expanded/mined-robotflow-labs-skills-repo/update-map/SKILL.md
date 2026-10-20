# /update-map — Refresh DATASETS_MAP.md from disk

Regenerate the `DATASETS_MAP.md` file that agents use to find models, datasets, and repos.

## Instructions

Run this command:

```bash
cd /Users/ilessio/Development/AIFLOWLABS/R&D/Wave-5-research
uv run scripts/update_map.py
```

Then show the user a brief summary of what changed (done count, pending count).

The map is at: `/Users/ilessio/Development/AIFLOWLABS/R&D/Wave-5-research/DATASETS_MAP.md`

## When to use
- After downloads complete
- After reorganizing storage
- When an agent needs to know where data lives
- When the user asks "what's downloaded?" or "where is X?"
