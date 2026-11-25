---
name: skill-grab
description: Collect the latest best skills from skills.sh into an Obsidian digest note. Use when the user asks to grab skills, fetch skills from skills.sh, discover new agent skills, or /skill-grab.
---

# Skill Grab

Fetches the skills.sh leaderboard (trending, hot, or all-time), parses skills, and optionally uses AI to curate a digest. Saves to `Sources/`.

## Quick Start

```bash
python3 _scripts/skill_grab.py
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-s, --source` | trending | Leaderboard: `trending`, `hot`, or `all` |
| `-c, --count` | 50 | Max skills to fetch |
| `--no-ai` | — | Skip AI curation; output raw list only |
| `--print` | — | Print to stdout instead of saving |

## Examples

```bash
# Default: trending, AI-curated, save to Sources/
python3 _scripts/skill_grab.py

# Hot skills, raw list, no AI
python3 _scripts/skill_grab.py --source hot --no-ai

# All-time top 30, print only
python3 _scripts/skill_grab.py --source all --count 30 --print
```

## Output

- **With AI:** Curated digest with top picks, categories, and install commands
- **Without AI:** Raw ranked list with `npx skills add <owner/repo>` for each
- **Path:** `Sources/Skills Digest - YYYY-MM-DD.md`

## Install

Skills are installed via the [skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add <owner/repo>
```

## Cross-Domain

Skills span coding, marketing, AI workflows, and knowledge work. The AI may flag relevant skills for Obsidian, [[Personal AI Infrastructure]], or Claude Code usage.
