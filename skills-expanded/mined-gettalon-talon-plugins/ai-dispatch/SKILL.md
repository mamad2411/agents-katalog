---
description: "Dispatch subagents to multiple AI backends. Usage: dispatch <backend> \"prompt\". Backends: ark-code, ark-minimax, ark-kimi, ark-deepseek, glm, ark-doubao, ark-auto"
---

# AI Dispatch

Dispatch tasks to different AI backends via `dispatch <backend> "prompt"`.

## First Use — Auto Setup

Before dispatching, check if `dispatch` is available:

```bash
which dispatch
```

If not found, run setup:
```bash
bash $SKILL_DIR/../../scripts/setup.sh
```

If config is missing (`~/.config/ai-dispatch/config.json`), setup will:
1. Check environment for existing `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`
2. If found, auto-create config from env
3. If not, ask the user for API keys
4. Install `dispatch` and `dcheck` to PATH

## Usage

```bash
# Simple — backend + prompt (auto-adds all flags)
dispatch ark-code "implement binary search"
dispatch glm "translate to Chinese: hello world"
dispatch ark-minimax "analyze this codebase"

# Check progress
dcheck --latest

# List backends
dispatch --list
```

## Available Backends

| Command | Model | Best for |
|---------|-------|----------|
| `ark-code` | Doubao Seed 2.0 Code | Code generation |
| `ark-pro` | Doubao Seed 2.0 Pro | General reasoning |
| `ark-minimax` | MiniMax M2.5 | Analysis, research |
| `ark-kimi` | Kimi K2.5 | Long context |
| `ark-deepseek` | DeepSeek V3.2 | Complex reasoning |
| `ark-glm` | GLM-4.7 | Chinese via Ark |
| `ark-auto` | Auto routing | Smart selection |
| `glm` | GLM-5 | Chinese language |

## Adding Custom Backends

Edit `~/.config/ai-dispatch/config.json`:
```json
{
  "backends": {
    "my-api": {
      "description": "My custom API",
      "env": {
        "ANTHROPIC_BASE_URL": "https://my-api.example.com",
        "ANTHROPIC_API_KEY": "sk-..."
      },
      "models": { "opus": "my-model", "sonnet": "my-model", "haiku": "my-model" }
    }
  }
}
```
Then: `dispatch my-api "hello"`

## Advanced

```bash
# Explicit mode (full control over claude flags)
dispatch ark claude -p --dangerously-skip-permissions "prompt"

# Interactive (named pipe for follow-ups)
dispatch ark claude-interactive

# Resume session
dispatch ark claude -p --resume <SESSION_ID> "follow up"

# Codex
dispatch ark codex "prompt"
```

## Output

Simple mode returns structured JSON:
```json
{"summary": "...", "changed_files": ["..."], "findings": ["..."]}
```
