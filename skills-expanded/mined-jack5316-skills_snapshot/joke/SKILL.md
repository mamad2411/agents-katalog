---
name: joke
description: Generate dad jokes (冷笑话) with a sense of humor. Creates punny, cheesy jokes on any topic. Use when user wants a joke, dad joke, 冷笑话, or /joke.
---

# Joke Skill

Generates dad jokes (冷笑话) — punny, cheesy jokes that are so bad they're good. Provide a topic or get a random one.

## Usage

```bash
# Random topic
python3 _scripts/joke.py

# Joke about a specific topic
python3 _scripts/joke.py "Python"
python3 _scripts/joke.py "coffee"
python3 _scripts/joke.py "meetings"

# Save to vault
python3 _scripts/joke.py "AI" --save
```

## Output

- **Terminal**: Prints the joke
- **With --save**: `Sources/Joke - YYYY-MM-DD.md`

## Notes

- Dad joke style: setup → punchline with pun or twist
- Family-friendly
- Works in English or Chinese depending on topic
