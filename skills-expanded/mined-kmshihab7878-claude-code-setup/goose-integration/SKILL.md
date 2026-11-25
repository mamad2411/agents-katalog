---
name: goose-integration
description: Dispatch tasks to Goose CLI for model-agnostic execution, recipe running, and persistent scheduled jobs — complementary to Claude Code
type: skill
triggers:
  - /goose
  - When user wants to use a non-Anthropic model
  - When user wants persistent scheduled tasks
  - When user wants to run Goose recipes
---

# Goose Integration for Claude Code

Goose (Block, Apache 2.0) runs as a complementary AI agent alongside Claude Code.
Use it for model-agnostic tasks, persistent scheduling, and recipe execution.

## When to Use Goose vs Claude Code

| Use Goose When | Use Claude Code When |
|----------------|---------------------|
| Need non-Anthropic model (GPT-4, Gemini, DeepSeek, local LLMs) | Need Claude's intelligence (best code quality) |
| Persistent scheduled jobs (survives session restart) | Session-scoped automation |
| Running Goose-format recipes | Running Claude skills/commands |
| Model A/B testing | Production code generation |
| Cost-sensitive bulk tasks (use cheaper models) | Quality-critical tasks |

## Setup

### Installation
```bash
brew install block-goose-cli
```

### Configuration
Config lives at `~/.config/goose/config.yaml`:
```yaml
GOOSE_PROVIDER: anthropic    # Use Claude as default provider
GOOSE_MODEL: claude-sonnet-4-6
```

### Available Providers
anthropic, openai, ollama, google, azure, bedrock, openrouter, deepseek, groq, cerebras, mistral, lm-studio, litellm

## Commands

### Start a Goose Session
```bash
goose session                    # Interactive session
goose session -r                 # Resume last session
goose session --with-extension "command"  # With specific extension
```

### Run a Recipe
```bash
goose run --recipe <path-to-recipe.yaml>
```

### Configure
```bash
goose configure    # Interactive setup
```

### Scheduled Jobs
Goose has built-in persistent cron scheduling:
```bash
# Within a goose session, use the schedule tool to create recurring jobs
```

## Dispatch from Claude Code

To dispatch a task to Goose from Claude Code:

```bash
# Simple task with default provider
echo "<task description>" | goose session --text

# Task with specific model
GOOSE_PROVIDER=openai GOOSE_MODEL=gpt-4o echo "<task>" | goose session --text

# Task with local model (free)
GOOSE_PROVIDER=ollama GOOSE_MODEL=qwen3:8b echo "<task>" | goose session --text

# Run a Goose recipe
goose run --recipe ~/.config/goose/recipes/<name>.yaml
```

## Project Instructions

Goose uses `.goosehints` (equivalent to CLAUDE.md). To share context:
```bash
# Symlink CLAUDE.md to .goosehints for shared project instructions
ln -sf .claude/CLAUDE.md .goosehints
```

## Extension Ecosystem

Goose connects to 3000+ MCP servers. Your existing MCP servers work with Goose too.

## Rules

1. Claude Code remains the primary agent for all quality-critical work
2. Goose is for model diversity, scheduling, and cost optimization
3. Never use Goose for T2+ risk tasks (those need Claude's governance pipeline)
4. Goose sessions are independent — they don't share Claude Code's agent hierarchy
5. For shared MCP servers, be aware both agents may access the same resources
