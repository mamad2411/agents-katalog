---
name: flomo
description: Send notes to flomo floating notes via webhook. Use when user says "flomo", "send to flomo", "floating note", or /flomo.
---

# Flomo Skill - Floating Notes

Send quick notes to your flomo floating notes application using the incoming webhook API. Perfect for capturing ideas that you want in flomo.

## Quick Start

```bash
python3 _scripts/flomo_send.py "Your note here"
```

## Setup

1. **Get your flomo webhook URL** from flomo settings
2. **Add to your .env file**:
   ```
   FLOMO_WEBHOOK_URL=https://flomoapp.com/iwh/your/secret/key/
   ```

## Usage

Basic note:
```bash
python3 _scripts/flomo_send.py "My great idea"
```

With tags:
```bash
python3 _scripts/flomo_send.py "Project brainstorm" --tag "idea" --tag "project"
```

With custom webhook:
```bash
python3 _scripts/flomo_send.py "Note" --webhook "https://flomoapp.com/iwh/your/key/"
```

## Options

- `-t, --tag TAG`: Add a tag to the note (can use multiple times)
- `-w, --webhook URL`: Custom flomo webhook URL (overrides env var)

## Defaults

- **Webhook**: Uses `FLOMO_WEBHOOK_URL` from .env
- **Tags**: Supports `#tag` format in content or via `--tag` option

## Output

- Terminal: Confirmation message with ✅ emoji on success
- flomo: Your note appears in your flomo inbox with any specified tags

## Tips

- You can include tags directly in the content like: `My note #idea #important`
- The skill works with both inline content and piped input
- Use alongside the `/mem` skill - `/mem` saves to Obsidian, `/flomo` sends to flomo
