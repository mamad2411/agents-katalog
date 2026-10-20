# token-sisyphus — Claude Code Skill

## What this does

Burns LLM tokens toward a target count, so you can satisfy your company's AI usage KPI
without actually doing anything meaningful. Push the boulder. Watch it roll back. Repeat.

## Trigger phrases

- "burn tokens"
- "consume tokens"
- "fill my KPI"
- "push the boulder"
- "sisyphus mode"

## Usage

When triggered, run the burn script with the user's specified target and provider.

```bash
# OpenAI (default)
python burn.py --target 100k

# Claude
python burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# Custom OpenAI-compatible (DeepSeek, Qwen, Kimi, etc.)
python burn.py --target 100k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Dry run (no real API calls)
python burn.py --target 100k --dry-run
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--target` | required | Token count: `50000`, `100k`, `1m` |
| `--provider` | `openai` | `openai`, `claude`, `gemini` |
| `--model` | provider default | Model name |
| `--api-key` | env var | API key |
| `--base-url` | — | Custom endpoint (openai provider) |
| `--max-tokens` | `500` | Max tokens per request |
| `--delay` | `0.5` | Seconds between requests |
| `--dry-run` | off | Simulate without real calls |

## Environment variables

| Provider | Env var |
|----------|---------|
| OpenAI / compatible | `OPENAI_API_KEY` |
| Claude | `ANTHROPIC_API_KEY` |
| Gemini | `GEMINI_API_KEY` |

## Install dependencies

```bash
# OpenAI / compatible
pip install openai

# Claude
pip install anthropic

# Gemini
pip install google-generativeai
```
