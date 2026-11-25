---
name: nanobot
description: Leverage nanobot — ultra-lightweight personal AI assistant from HKUDS. Chat via nanobot agent, check status, start gateway, list skills. Use when user wants nanobot, /nanobot, or to interact with their nanobot assistant.
---

# Nanobot Skill

Chat with [nanobot](https://github.com/HKUDS/nanobot) — ultra-lightweight personal AI assistant (~4K lines). Integrates with PAI vault skills.

## Usage

```bash
python3 _scripts/nanobot_skill.py chat "Summarize today's notes"
python3 _scripts/nanobot_skill.py status
python3 _scripts/nanobot_skill.py gateway   # how to start Telegram/Discord/Feishu
python3 _scripts/nanobot_skill.py info      # setup guide
python3 _scripts/nanobot_skill.py list-skills
```

## Options

- `--save` — Save chat response to `Sources/Nanobot Chat - YYYY-MM-DD.md`

## Prerequisites

- Install: `uv tool install nanobot-ai` or `pip install nanobot-ai`
- Config: run `nanobot onboard` first (`~/.nanobot/config.json`)
- Set workspace to vault path for PAI skill indexing

See `_scripts/nanobot_setup.md` for full setup (Telegram, Discord, etc.).

## Output

Terminal response, or `Sources/Nanobot Chat - YYYY-MM-DD.md` with `--save`
