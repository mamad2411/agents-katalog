---
name: ollama
description: Local LLM inference using Ollama. Use when you need privacy, offline capability, or zero-cost AI. Runs models locally on your machine without API calls. Perfect for sensitive data, development without internet, or cost-effective AI tasks.
---

# Ollama Local LLM Bridge

Run large language models locally on your machine with zero API costs.

## Supported Models

- **joker** - General purpose, 5.4GB
- **gemma2:2b** - Lightweight, 1.6GB
- **gemma2:9b** - More capable, 5.4GB

## Prerequisites

1. Ollama installed: https://ollama.ai
2. Models pulled (optional - first run auto-pulls)

## Quick Start

```bash
# List available models
ollama list

# Run a model directly
ollama run joker "Hello"

# Or use our script
python /home/bc/skills/ollama/run.py "Your prompt"
```

## Usage

### Basic Prompt

```bash
python /home/bc/skills/ollama/run.py "Explain quantum computing"
```

### From stdin

```bash
echo "Write a Python function" | python /home/bc/skills/ollama/run.py
```

### Specify Model

```bash
python /home/bc/skills/ollama/run.py --model gemma2:9b "Complex reasoning task"
```

### Interactive Mode

```bash
python /home/bc/skills/ollama/run.py -i
```

## Model Selection Guide

| Model | Size | Best For | Speed |
|-------|------|----------|-------|
| joker | 5.4GB | General conversation | Medium |
| gemma2:2b | 1.6GB | Quick tasks, testing | Fast |
| gemma2:9b | 5.4GB | Complex reasoning | Slow |

## Configuration

Edit `/home/bc/skills/ollama/config.json`:

```json
{
  "default_model": "joker",
  "temperature": 0.7,
  "max_tokens": 512,
  "system_prompt": "You are a helpful AI assistant."
}
```

## Troubleshooting

**Ollama not found**
- Install: https://ollama.ai
- Or: `curl -fsSL https://ollama.ai/install.sh | bash`

**Model not found**
- First run auto-pulls the model
- Or: `ollama pull <model-name>`

**Out of memory**
- Use smaller model: gemma2:2b
- Or: `ollama prune`

**Port already in use**
- Check: `ollama list`
- Kill: `pkill -f ollama`

## Advanced

### Stream Responses

```bash
python /home/bc/skills/ollama/run.py --stream "Tell me a story"
```

### Custom System Prompt

```bash
python /home/bc/skills/ollama/run.py --system "You are a Python expert" "Debug this code"
```

### API Server Mode

```bash
# Start Ollama server
ollama serve

# Use as API
curl http://localhost:11434/api/generate -d '{
  "model": "joker",
  "prompt": "Hello",
  "stream": false
}'
```

## Integration

### Bash Alias

Add to `~/.bashrc`:

```bash
alias ollama-chat="python /home/bc/skills/ollama/run.py"
```

### VS Code Task

```json
{
  "label": "Ask Local LLM",
  "type": "shell", 
  "command": "python /home/bc/skills/ollama/run.py '${input:prompt}'"
}
```

## Advantages Over Cloud APIs

| Feature | Ollama | Cloud APIs |
|---------|--------|-------------|
| Cost | Free | Pay-per-use |
| Privacy | 100% local | Data leaves machine |
| Offline | Works offline | Requires internet |
| Speed | Local | Network latency |
| Custom models | Yes | Limited |

## Use Cases

- **Security-sensitive work**: Code that shouldn't leave your machine
- **Offline development**: Air-gapped environments
- **Cost savings**: Unlimited inference
- **Experimentation**: Try many models quickly
- **Learning**: Understand AI without API costs

## Notes

- First run downloads model (5-10 minutes)
- Subsequent runs are instant
- Models use ~4-8GB RAM depending on size
- Can run multiple models simultaneously

## References

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Model Library](https://ollama.ai/library)
- [API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
