---
name: ollama-cli
description: 'Execute and manage local LLMs using the ollama CLI, including pulling models and launching agents with MCP configurations. You MUST load this skill when interacting with the `ollama` CLI.'
license: MIT
---
# ollama-cli

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

## WHEN TO USE

- When querying, pulling, or managing local LLMs via the `ollama` CLI.
- When configuring local model backends for AI agents.
- When launching wrapper tools (like Claude Code) using an Ollama model with Model Context Protocol (MCP) configurations.

## WHEN NOT TO USE

- When making standard REST API calls to remote cloud providers (e.g., OpenAI, Anthropic) without a local proxy.
- For managing Python environments or general CLI tools unrelated to local inference.

## Step-by-Step Workflows

### 1. Verification and Setup

1. **Check Daemon Status**:
   Run `ollama list` to verify the local Ollama daemon is active and responsive.
2. **Pull Model**: If the target model is missing, execute `ollama pull <model-name>` (e.g., `ollama pull gemma4:e2b`) to cache it locally before running.

### 2. Execution and Agent Launch

1. **Interactive Run**:
   Use `ollama run <model-name>` to test the model directly in the CLI.
2. **Launch with MCP Config**: When integrating Ollama models with agent workflows (like Claude Code) that require Model Context Protocol configurations, use process substitution to pass dynamic JSON configurations safely.

## Command Examples

- **List Available Models**:
  ```bash
  ollama list
  ```

- **Pull a Specific Model**:
  ```bash
  ollama pull gemma4:e2b
  ```

- **Launch Claude Code with Ollama and MCP Config**:
  Demonstrates how to launch Claude via Ollama, specifying the model and injecting an inline JSON MCP configuration using bash process substitution:
  ```bash
  ollama launch claude --model gemma4:e2b -- --mcp-config <(echo '{"mcpServers":{}}') --strict-mcp-config
  ```

## Common Pitfalls

- **Missing Daemon**: Forgetting to start the Ollama background daemon before running commands. Symptoms include connection refused on `127.0.0.1:11434`.
- **Process Substitution Syntax Errors**: Using `<(echo ...)` requires `bash` or `zsh`. Running it in standard `/bin/sh` will result in a syntax error. Always ensure your execution shell is set to `bash`.
- **Un-pulled Models**: Attempting to launch an agent against a model that hasn't been cached locally will cause the agent initialization to fail or hang.
- **Resource Exhaustion**: Local models can consume significant RAM/VRAM. Monitor usage when running complex models like `gemma4:e2b` to avoid Out of Memory (OOM) kernel kills.

## Troubleshooting

- **Connection Refused**: Start the Ollama server manually with `ollama serve &` if it's not running as a system service.
- **Model Loading Hangs**: If a model hangs during `ollama run`, check `dmesg` or system logs to ensure the system hasn't run out of memory.
