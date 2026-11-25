---
name: wiki
description: Quickly learn about anything using the Feynman technique, presented as a wiki-style tutorial. Use when user wants to learn a topic, understand something, get a tutorial, or /wiki.
---

# Wiki Skill (/wiki)

Learn anything quickly using the **Feynman technique** — explained simply, built from basics, like a wiki tutorial.

*"If you can't explain it simply, you don't understand it."* — Richard Feynman

## Quick Start

```bash
python3 _scripts/wiki.py "quantum entanglement"
```

## Options

- `topic` (required): Anything you want to learn
- `--save`: Save to vault as `Atlas/Wiki - TOPIC.md`
- `--no-save`: Print only (default)

## Examples

```bash
# Learn a concept
python3 _scripts/wiki.py recursion

# Technical topic
python3 _scripts/wiki.py "how SSL certificates work" --save

# Abstract idea
python3 _scripts/wiki.py "game theory"
```

## Output Structure

Each wiki follows the Feynman method:

1. **TL;DR** — Simplest one-paragraph summary
2. **The Core Idea** — Key concept with an analogy
3. **Step by Step** — Digestible chunks, plain language
4. **Common Misconceptions** — What people get wrong
5. **Key Takeaways** — Bullet points to remember
6. **Go Deeper** — Test questions or next topics

## Saved Output

- **Path**: `Atlas/Wiki - TOPIC.md`
- **Tags**: `wiki`, `learning`, `feynman`
