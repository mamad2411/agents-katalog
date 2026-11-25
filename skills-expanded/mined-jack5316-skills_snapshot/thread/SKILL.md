---
name: thread
description: Convert vault insights into Twitter/X threads. Use when user asks for thread, Twitter thread, X thread, convert insights to tweets, or /thread.
---

# Thread Skill

Converts accumulated vault insights into Twitter/X threads — each tweet under 280 characters, hook-first, copy-paste ready. Pulls from Sources (syntheses, digests), Atlas, Maps, and Inbox.

## Usage

```bash
# Open synthesis — AI picks the most shareable insight from recent notes
python3 _scripts/thread_from_insights.py

# Topic-focused thread
python3 _scripts/thread_from_insights.py --topic "inverse problems"
python3 _scripts/thread_from_insights.py --topic "AI agents, LLMs"

# Custom tweet count and lookback
python3 _scripts/thread_from_insights.py --topic "personal AI" --tweets 8 --days 14

# Custom output filename
python3 _scripts/thread_from_insights.py --topic "regularization" --title "Life as Inverse Problem"
```

## Output

`Sources/Thread - {topic-or-date}.md` — numbered tweet list (1., 2., 3., ...). Each tweet is plain text, ≤280 chars, ready to copy into Twitter/X. Source index with [[wikilinks]] at bottom.

## Notes

- Prioritizes weekly/daily synthesis, self-reflection, essays (highest insight density)
- `--topic` filters notes by keyword; multiple keywords separated by comma (OR logic)
- Default lookback: 30 days for Sources/Inbox; Atlas and Maps always included
- Output is plain text per tweet — no markdown in the thread body, so it pastes cleanly
