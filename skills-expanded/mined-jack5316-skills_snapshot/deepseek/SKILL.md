---
name: deepseek
description: Chat with DeepSeek API for cost-effective AI conversations. Use DeepSeek to reduce model usage costs while maintaining high-quality AI responses. Use when user says "deepseek", "/deepseek", or wants a cost-effective AI conversation.
---

# DeepSeek Skill

Chat with DeepSeek API directly — cost-effective alternative for general chat and coding tasks.

## Usage

```bash
python3 _scripts/deepseek_chat.py "Explain quantum computing"
python3 _scripts/deepseek_chat.py "Write a sort function" --model deepseek-coder
echo "What is the meaning of life?" | python3 _scripts/deepseek_chat.py
```

## Options

- `-s, --system TEXT` — System prompt to set AI behavior
- `-m, --model TEXT` — `deepseek-chat` (default) or `deepseek-coder` (coding tasks)
- `-t, --temperature FLOAT` — 0–2; lower = focused, higher = creative (default: 0.7)
- `--max-tokens INT` — Maximum tokens in response
- `--stream` — Stream response in real-time

## Output

Terminal only. Requires `DEEPSEEK_API_KEY` in `.env`.
