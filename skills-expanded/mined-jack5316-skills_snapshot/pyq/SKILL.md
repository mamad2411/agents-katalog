---
name: pyq
description: Generate WeChat Moments (朋友圈) copywriting with hackable templates. Use when user asks for "发朋友圈", "pyq", "wechat moments", or "/pyq".
---

# WeChat Moments (/pyq)

Generate engaging WeChat Moments (朋友圈) copy with pre-built, hackable templates for different scenarios.

## Quick Start

```bash
# List all templates
python3 _scripts/wechat_pyq.py

# Generate daily life post
python3 _scripts/wechat_pyq.py --template daily

# Generate insight about AI
python3 _scripts/wechat_pyq.py -t insight --topic "AI"

# Save output to vault
python3 _scripts/wechat_pyq.py -t gratitude --save
```

## Features

1. **8 Hackable Templates** - Different scenarios covered
2. **Quick Generation** - One command to get publish-ready copy
3. **Customizable Topics** - Add your specific theme
4. **Vault Integration** - Save generated copy to Obsidian

## Templates Available

- `daily` - Daily life moments (warm & relatable)
- `insight` - Thoughts & realizations
- `gratitude` - Appreciation posts
- `work` - Tasteful work updates
- `book` - Book/media recommendations
- `photo` - Short, evocative captions
- `weekend` - Relaxed weekend vibes
- `question` - Engaging questions for friends

## Options

- `-t, --template TEXT`: Template to use
- `--topic TEXT`: Topic or theme for the post
- `--list`: List all available templates
- `--save`: Save output to vault

## Examples

```bash
# List templates
python3 _scripts/wechat_pyq.py

# Generate daily post
python3 _scripts/wechat_pyq.py -t daily

# With specific topic
python3 _scripts/wechat_pyq.py -t book --topic "Atomic Habits"

# Save to vault
python3 _scripts/wechat_pyq.py -t weekend --save
```

## Hacking the Templates

Edit `_scripts/wechat_pyq.py` and modify the `TEMPLATES` dictionary to add your own or customize existing ones.

## Output

- **Terminal**: Generated copy displayed immediately
- **Saved note**: `Sources/WeChat Moments - {topic} - YYYY-MM-DD.md`
