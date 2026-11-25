
---
name: skill-hub
description: Search, browse, and install Claude Code skills from skills.sh and clawhub.ai into your local vault. Use when you want to discover new skills, install a skill from GitHub, convert a GitHub repo to a local Claude Code skill, browse trending skills, or /skill-hub.
---

# Skill Hub (/skill-hub)

Unified gateway to the external skills ecosystem. Searches skills.sh REST API (88,000+ skills) and attempts clawhub.ai, then fetches SKILL.md from GitHub and registers skills locally as Claude Code-compatible entries.

## Quick Start

```bash
# Browse top 30 trending skills
python3 _scripts/skill_hub.py browse

# Search for skills
python3 _scripts/skill_hub.py search "obsidian"

# Install a skill from skills.sh (monorepo format)
python3 _scripts/skill_hub.py install anthropics/skills/claude-api

# Convert any GitHub URL to local skill
python3 _scripts/skill_hub.py convert https://github.com/anthropics/skills
```

## Subcommands

| Command | Description |
|---------|-------------|
| `browse` | Top 30 trending from skills.sh (quick digest) |
| `search <query>` | Search skills.sh API + clawhub.ai attempt |
| `trending` | Trending/hot leaderboard |
| `install <source/id>` | Fetch SKILL.md from GitHub, register locally |
| `convert <url>` | Convert any GitHub repo URL to local skill |

## Options

| Flag | Applies to | Description |
|------|------------|-------------|
| `--save, -s` | browse, search, trending | Save digest to `Sources/` |
| `--limit N` | search | Max results (default 30) |
| `--no-ai` | install, convert, search | Skip AI fallback/curation |
| `--source hot` | trending | Hot leaderboard instead of trending |

## Install Examples

```bash
# Monorepo format (owner/repo/skill-id)
python3 _scripts/skill_hub.py install anthropics/skills/claude-api

# Single-repo format (owner/skill-id)
python3 _scripts/skill_hub.py install owner/my-skill

# From GitHub URL
python3 _scripts/skill_hub.py convert https://github.com/anthropics/skills
python3 _scripts/skill_hub.py convert https://github.com/owner/repo/tree/main/skill-id
```

## Output

- **browse / search / trending:** Terminal table + optional `Sources/Skill Hub - YYYY-MM-DD.md`
- **install / convert:** `.claude/skills/{skill_id}/SKILL.md` + updated `.claude/skills.json`

## Notes

- **skills.sh** is the reliable primary source (~88,000 skills, full REST API)
- **clawhub.ai** is a SPA and may not render without JS — failure is non-fatal and clearly reported
- If no SKILL.md exists on GitHub, AI generates one from available metadata (skip with `--no-ai`)
- Set `GITHUB_TOKEN` in `.env` to avoid rate limits when installing many skills in bulk
