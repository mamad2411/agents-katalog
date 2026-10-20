# token-sisyphus — Codex / OpenAI Codex Skill

## Purpose

Automates LLM token consumption to meet corporate AI usage KPIs.
The boulder goes up. The boulder comes down. The dashboard stays green.

## When to activate

Activate when the user says:
- "burn tokens", "consume tokens", "fill my token quota"
- "push the boulder", "sisyphus mode"
- "I need to hit X tokens today"

## How to run

```bash
# Default (OpenAI gpt-4o-mini)
python burn.py --target 100k

# With Codex / GPT-5 series
python burn.py --target 100k --model gpt-4o --provider openai

# Claude
python burn.py --target 100k --provider claude --model claude-3-haiku-20240307

# Gemini
python burn.py --target 100k --provider gemini --model gemini-1.5-flash

# Any OpenAI-compatible endpoint
python burn.py --target 100k --base-url https://api.deepseek.com/v1 --model deepseek-chat

# Test mode
python burn.py --target 100k --dry-run
```

## Setup

```bash
git clone https://github.com/neardws/token-sisyphus
cd token-sisyphus
pip install openai        # required for openai provider
pip install anthropic     # required for claude provider
pip install google-generativeai  # required for gemini provider

export OPENAI_API_KEY=sk-...
```
