---
name: ollama-local-setup
description: Set up and configure a local Ollama instance for WordPress without needing an API key.
---

# Ollama Local Setup

Use this skill to connect WordPress to a local Ollama instance using the `ai-provider-for-ollama` plugin.

## Configuration
- No API key required for local instances.
- Default host: `http://localhost:11434`.
- Can be changed via the `OLLAMA_HOST` environment variable or in **Settings > Ollama**.
- Automatically discovers models like Llama, Mistral, Gemma, Phi.
