---
name: azure-llm-bridge
description: Bridge to Azure AI Foundry LLMs (Mistral 3 Large and Kimi K2 Thinking). Use when you need to call Azure-hosted language models directly from scripts or command line. Provides simple CLI interfaces to Mistral and Kimi models without complex OpenAI SDK setup.
---

# Azure LLM Bridge

Simple command-line interface to Azure AI Foundry language models.

## Supported Models

- **Mistral 3 Large** - General purpose LLM with strong reasoning
- **Kimi K2 Thinking** - Advanced thinking model for complex tasks

## Prerequisites

1. Azure AI Foundry account with deployed models
2. Azure API key set in environment
3. Python 3.8+ with `requests` library

## Setup

### 1. Set Environment Variables

```bash
export AZURE_API_KEY="your-azure-api-key"

# Optional: Override default endpoints
export MISTRAL_ENDPOINT="https://your-resource.cognitiveservices.azure.com/openai/deployments/Mistral-Large-3/chat/completions?api-version=2024-05-01-preview"
export KIMI_ENDPOINT="https://your-resource.cognitiveservices.azure.com/openai/deployments/Kimi-K2-Thinking/chat/completions?api-version=2024-05-01-preview"
```

### 2. Install Dependencies

```bash
pip install requests
```

## Usage

### Mistral 3 Large

```bash
# Direct prompt
python scripts/mistral.py "Explain quantum computing"

# From stdin
echo "Write a Python function" | python scripts/mistral.py

# With variables
prompt="Debug this code"
python scripts/mistral.py "$prompt"
```

### Kimi K2 Thinking

```bash
# Direct prompt
python scripts/kimi.py "Analyze this architecture"

# From stdin
cat problem.txt | python scripts/kimi.py

# Complex reasoning
echo "Step through this logic" | python scripts/kimi.py
```

### From Python Code

```python
import subprocess

# Call Mistral
result = subprocess.run(
    ['python', 'scripts/mistral.py', 'Your prompt'],
    capture_output=True,
    text=True
)
print(result.stdout)

# Call Kimi
result = subprocess.run(
    ['python', 'scripts/kimi.py', 'Your prompt'],
    capture_output=True,
    text=True
)
print(result.stdout)
```

## Model Selection Guide

| Model | Best For | Temperature | Max Tokens |
|-------|----------|-------------|------------|
| Mistral 3 Large | General tasks, coding, analysis | 0.7 | 4096 |
| Kimi K2 Thinking | Complex reasoning, step-by-step | 0.7 | 4096 |

## Troubleshooting

**Error: AZURE_API_KEY environment variable not set**
- Solution: `export AZURE_API_KEY="your-key"`

**Error: 401 Access denied**
- Check that your API key is correct
- Verify the endpoint URL matches your Azure deployment

**Error: 404 Deployment not found**
- Confirm the model deployment name in Azure
- Check the endpoint URL is correct

**Error: Connection timeout**
- Verify network connectivity to Azure
- Check if Azure service is available in your region

## Advanced Configuration

Modify the scripts to customize:
- `max_tokens` - Response length (default: 4096)
- `temperature` - Creativity vs determinism (default: 0.7)
- `messages` - Add system prompts or conversation history

## References

- [Azure OpenAI Documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Mistral Documentation](https://docs.mistral.ai/)
- [Kimi Documentation](https://platform.moonshot.cn/docs)

## Examples

### Code Review

```bash
python scripts/mistral.py "Review this code for bugs: $(cat mycode.py)"
```

### Architecture Analysis

```bash
echo "Analyze trade-offs between microservices and monoliths" | python scripts/kimi.py
```

### Documentation Generation

```bash
python scripts/mistral.py "Write documentation for a REST API with these endpoints: /users, /posts, /auth"
```

### Debugging Help

```bash
python scripts/kimi.py "Debug: I'm getting a 500 error when calling this API endpoint"
```

## Integration with Other Tools

### Alias for Easy Access

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias mistral="python /path/to/azure-llm-bridge/scripts/mistral.py"
alias kimi="python /path/to/azure-llm-bridge/scripts/kimi.py"
```

### VS Code Task

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Ask Mistral",
      "type": "shell",
      "command": "python scripts/mistral.py '${input:prompt}'",
      "problemMatcher": []
    }
  ]
}
```

## Security Notes

- Never commit API keys to version control
- Use environment variables or secure secret management
- Rotate keys regularly
- Monitor usage in Azure portal

## License

MIT - Feel free to modify and distribute
