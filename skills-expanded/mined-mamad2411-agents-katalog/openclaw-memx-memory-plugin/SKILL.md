---
name: openclaw-memx-memory-plugin
description: Use OpenClaw MemX for long-term agent memory with self-learning, relationship graphs, and automatic maintenance
triggers:
  - add long-term memory to openclaw
  - set up memx memory plugin
  - configure openclaw agent memory
  - use relationship-aware memory in openclaw
  - maintain agent memory across sessions
  - retrieve memories from openclaw memx
  - debug openclaw memory system
  - reindex openclaw memory embeddings
---

# OpenClaw MemX Memory Plugin

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClaw MemX is a local-first long-term memory plugin that enables AI agents to maintain working memory across days, projects, and conversations. It provides stable work memory, task state tracking, relationship-aware recall, learned habits, automatic cleanup, and compact evidence injection.

## Key Capabilities

- **Long-term memory**: Remembers project decisions, user preferences, task status, and important events
- **Relationship graphs**: Tracks how projects, repos, tools, people, and resources relate to each other
- **Self-learning**: Notices stable patterns across repeated work (e.g., user preferences, recurring workflows)
- **Self-maintenance**: Consolidates repeated evidence, replaces corrected information, cleans up old task state
- **Smart recall**: Searches across facts, events, state, chunks, relationships, and patterns to inject relevant evidence

## Installation

### Prerequisites

- OpenClaw 2026.3.25 or later
- Node.js 22.14+ or Node 24
- Python 3 (only required for local embeddings)

### Basic Install

```bash
# Clone the repository
git clone https://github.com/NeoLi00/openclaw-memx.git
cd openclaw-memx

# Install plugin
openclaw plugins install .

# Setup with local embeddings (recommended)
openclaw memx setup --local-embedding

# Restart gateway
openclaw gateway restart

# Verify installation
openclaw memx doctor --deep
```

### Development Install with Live Edits

```bash
# Link plugin for development
openclaw plugins install --link .
```

## Configuration

### Setup with Local Embeddings

The recommended configuration uses local sentence-transformers for embeddings:

```bash
# Create Python virtual environment for embeddings
python3 -m venv "$HOME/.openclaw/memx/.venv"
"$HOME/.openclaw/memx/.venv/bin/python" -m pip install -U pip sentence-transformers torch

# Setup MemX with local embeddings
openclaw memx setup \
  --local-embedding \
  --embedding-python "$HOME/.openclaw/memx/.venv/bin/python"
```

### Setup with LLM Provider (DeepSeek Example)

```bash
# Configure LLM provider (use environment variable for API key)
export DEEPSEEK_API_KEY="your-api-key-here"

openclaw config set models.providers.deepseek '{
  "api": "openai-completions",
  "baseUrl": "https://api.deepseek.com",
  "apiKey": "${DEEPSEEK_API_KEY}",
  "models": [
    {
      "id": "deepseek-v4-flash",
      "name": "DeepSeek V4 Flash",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
      "contextWindow": 64000,
      "maxTokens": 8192
    }
  ]
}' --strict-json

# Setup MemX with LLM model and local embeddings
openclaw memx setup \
  --local-embedding \
  --embedding-python "$HOME/.openclaw/memx/.venv/bin/python" \
  --llm-model deepseek/deepseek-v4-flash

openclaw gateway restart
```

### Alternative Embedding Providers

**OpenAI-compatible embeddings:**

```bash
export EMBEDDING_API_KEY="your-embedding-key"

openclaw memx setup \
  --embedding-provider openai-compatible \
  --embedding-model text-embedding-3-small

openclaw config set plugins.entries.memory-memx.config.embedding.baseURL https://api.openai.com/v1
openclaw config set plugins.entries.memory-memx.config.embedding.apiKey '${EMBEDDING_API_KEY}'
```

**Ollama embeddings:**

```bash
openclaw memx setup \
  --embedding-provider ollama \
  --embedding-model nomic-embed-text

openclaw config set plugins.entries.memory-memx.config.embedding.ollamaBaseURL http://127.0.0.1:11434
```

**Custom local model:**

```bash
python3 -m pip install --user sentence-transformers torch

openclaw memx setup \
  --embedding-provider sentence-transformers-local \
  --embedding-model BAAI/bge-m3 \
  --embedding-device auto
```

**Disable embeddings (lexical fallback only):**

```bash
openclaw memx setup --embedding-provider off
```

### Reindex After Configuration Changes

After changing embedding settings, restart the gateway and reindex existing memories:

```bash
openclaw gateway restart
openclaw memx reindex
```

## Key Commands

### Setup and Maintenance

```bash
# Initial setup with local embeddings
openclaw memx setup --local-embedding

# Setup with specific embedding Python runtime
openclaw memx setup --local-embedding --embedding-python /path/to/.venv/bin/python

# Setup with specific LLM model
openclaw memx setup --llm-model provider/model

# Verify installation and configuration
openclaw memx doctor

# Deep verification with embedding and LLM tests
openclaw memx doctor --deep

# Reindex all memories (after embedding provider change)
openclaw memx reindex

# Restart gateway after configuration changes
openclaw gateway restart
```

### Memory Operations

MemX operates automatically through OpenClaw's memory slot system. The plugin:
- Automatically stores relevant information from conversations
- Recalls relevant memories when needed
- Injects memory context into prompts
- Maintains and consolidates memory over time

### Compatibility Mode

By default, MemX does not expose legacy `memory_search` and `memory_get` tools. To enable compatibility tools:

```bash
openclaw config set plugins.entries.memory-memx.config.advanced.enableCompatibilityMemoryTools true
openclaw gateway restart
```

## What `memx setup` Configures

The `openclaw memx setup` command writes the recommended configuration:

1. Adds `memory-memx` to `plugins.allow`
2. Sets `plugins.slots.memory` to `memory-memx` (MemX owns the memory slot)
3. Enables `plugins.entries.memory-memx.hooks.allowPromptInjection` (memory injection)
4. Enables turn scheduler and LLM semantic compiler
5. Keeps `advanced.enableCompatibilityMemoryTools=false` (no legacy tools by default)
6. Configures requested embedding provider and model

**Note:** `memx setup` does not delete or migrate existing `MEMORY.md` files. MemX's recall context tells the agent not to treat `MEMORY.md` or `memory/*.md` as the active memory backend unless explicitly asked.

## Architecture Overview

MemX maintains several types of memory:

- **Facts**: Stable information about preferences, decisions, and learned patterns
- **Events**: Time-stamped occurrences tied to specific contexts
- **Task State**: Current status of ongoing work
- **Chunks**: Segmented conversation turns for precise recall
- **Relationships**: Connections between entities (projects, repos, tools, people)
- **Resources**: References to files, documentation, links

All memories are tied to supporting evidence and are automatically maintained over time.

## TypeScript Integration Examples

### Checking MemX Installation Status

```typescript
import { execSync } from 'child_process';

function checkMemXInstallation(): boolean {
  try {
    const result = execSync('openclaw memx doctor', { encoding: 'utf-8' });
    return result.includes('MemX is ready');
  } catch (error) {
    console.error('MemX not properly installed:', error);
    return false;
  }
}
```

### Verifying Memory Configuration

```typescript
import { execSync } from 'child_process';

function verifyMemXConfig(): void {
  try {
    // Check if memory slot is assigned to MemX
    const config = execSync('openclaw config get plugins.slots.memory', { encoding: 'utf-8' });
    
    if (config.trim() === 'memory-memx') {
      console.log('✓ MemX is active memory provider');
    } else {
      console.warn('⚠ MemX is not the active memory provider');
    }
  } catch (error) {
    console.error('Failed to check MemX configuration:', error);
  }
}
```

### Programmatic Setup Script

```typescript
import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

interface MemXSetupOptions {
  embeddingProvider?: 'local' | 'openai' | 'ollama' | 'off';
  llmModel?: string;
  embeddingPython?: string;
}

function setupMemX(options: MemXSetupOptions = {}): void {
  const {
    embeddingProvider = 'local',
    llmModel,
    embeddingPython
  } = options;

  try {
    // Install Python dependencies for local embeddings
    if (embeddingProvider === 'local') {
      console.log('Installing Python dependencies...');
      const pythonBin = embeddingPython || 'python3';
      execSync(`${pythonBin} -m pip install --user sentence-transformers torch`, {
        stdio: 'inherit'
      });
    }

    // Build setup command
    let setupCmd = 'openclaw memx setup';
    
    if (embeddingProvider === 'local') {
      setupCmd += ' --local-embedding';
      if (embeddingPython) {
        setupCmd += ` --embedding-python ${embeddingPython}`;
      }
    } else if (embeddingProvider === 'off') {
      setupCmd += ' --embedding-provider off';
    }
    
    if (llmModel) {
      setupCmd += ` --llm-model ${llmModel}`;
    }

    console.log(`Running: ${setupCmd}`);
    execSync(setupCmd, { stdio: 'inherit' });

    // Restart gateway
    console.log('Restarting OpenClaw gateway...');
    execSync('openclaw gateway restart', { stdio: 'inherit' });

    // Verify installation
    console.log('Verifying installation...');
    execSync('openclaw memx doctor --deep', { stdio: 'inherit' });

    console.log('✓ MemX setup complete');
  } catch (error) {
    console.error('MemX setup failed:', error);
    throw error;
  }
}

// Usage
setupMemX({
  embeddingProvider: 'local',
  llmModel: 'deepseek/deepseek-v4-flash',
  embeddingPython: `${process.env.HOME}/.openclaw/memx/.venv/bin/python`
});
```

## Common Patterns

### Initial Setup for New OpenClaw Installation

```bash
# 1. Install OpenClaw (if not already installed)
# 2. Configure an LLM provider
export LLM_API_KEY="your-api-key"

openclaw config set models.providers.yourprovider '{
  "api": "openai-completions",
  "baseUrl": "https://api.provider.com",
  "apiKey": "${LLM_API_KEY}",
  "models": [
    {
      "id": "model-id",
      "name": "Model Name",
      "api": "openai-completions",
      "reasoning": false,
      "input": ["text"],
      "cost": { "input": 0, "output": 0 },
      "contextWindow": 32000,
      "maxTokens": 4096
    }
  ]
}' --strict-json

# 3. Install and setup MemX
git clone https://github.com/NeoLi00/openclaw-memx.git
cd openclaw-memx
openclaw plugins install .

python3 -m venv "$HOME/.openclaw/memx/.venv"
"$HOME/.openclaw/memx/.venv/bin/python" -m pip install -U pip sentence-transformers torch

openclaw memx setup \
  --local-embedding \
  --embedding-python "$HOME/.openclaw/memx/.venv/bin/python" \
  --llm-model yourprovider/model-id

openclaw gateway restart
openclaw memx doctor --deep
```

### Switching Embedding Providers

```bash
# Switch from local to OpenAI embeddings
export EMBEDDING_API_KEY="your-key"

openclaw memx setup \
  --embedding-provider openai-compatible \
  --embedding-model text-embedding-3-small

openclaw config set plugins.entries.memory-memx.config.embedding.apiKey '${EMBEDDING_API_KEY}'
openclaw gateway restart
openclaw memx reindex
```

### Migrating from Legacy Memory

```bash
# 1. MemX does not auto-migrate MEMORY.md
# 2. Manually review and convert important content:
#    - Have a conversation with the agent about the content
#    - Important facts will be automatically stored by MemX
# 3. Archive old memory files
mkdir -p legacy-memory
mv MEMORY.md memory/*.md legacy-memory/ 2>/dev/null || true
```

## Troubleshooting

### MemX Doctor Reports Issues

```bash
# Run deep diagnostics
openclaw memx doctor --deep

# Common issues and fixes:

# Issue: Memory slot not assigned to MemX
openclaw memx setup --local-embedding
openclaw gateway restart

# Issue: Embedding model not available
python3 -m pip install --user sentence-transformers torch

# Issue: LLM model not configured
openclaw config set plugins.entries.memory-memx.config.advanced.llmClassifierModel provider/model
openclaw gateway restart

# Issue: Plugin not in allow list
openclaw config set plugins.allow '["memory-memx"]' --json
openclaw gateway restart
```

### Embedding Errors

```bash
# Check Python dependencies
python3 -c "import sentence_transformers; print(sentence_transformers.__version__)"

# Reinstall dependencies
python3 -m pip install --user --force-reinstall sentence-transformers torch

# Use specific Python runtime
openclaw memx setup --local-embedding --embedding-python /path/to/python

# Switch to different provider if local embeddings fail
openclaw memx setup --embedding-provider ollama --embedding-model nomic-embed-text
openclaw gateway restart
```

### Memory Not Being Recalled

```bash
# Verify memory slot ownership
openclaw config get plugins.slots.memory
# Should return: memory-memx

# Verify prompt injection is enabled
openclaw config get plugins.entries.memory-memx.hooks.allowPromptInjection
# Should return: true

# Check if memories exist
openclaw memx doctor --deep
# Look for "stored memories" count

# Force reindex
openclaw memx reindex
```

### Gateway Restart Issues

```bash
# Stop and restart cleanly
openclaw gateway stop
sleep 2
openclaw gateway start

# Check gateway logs
openclaw gateway logs

# Verify plugin loaded
openclaw plugins list
# Should show memory-memx as active
```

### High Memory Usage

```bash
# MemX automatically maintains memory
# To manually trigger maintenance (advanced):
# Contact: neoliriven@gmail.com for maintenance configuration

# Check memory database size
ls -lh ~/.openclaw/memory-memx/
# Typical size varies with usage
```

## Best Practices

1. **Use local embeddings** for cost efficiency and privacy (`intfloat/multilingual-e5-small` recommended)
2. **Run `memx doctor --deep`** after any configuration change
3. **Always restart the gateway** after `memx setup` or config changes
4. **Use environment variables** for API keys, not hardcoded values
5. **Reindex after** changing embedding providers
6. **Let MemX maintain itself** — avoid manual memory file editing
7. **Archive `MEMORY.md`** files after migration to avoid confusion

## Memory Storage Location

MemX stores memory data locally in:

```
~/.openclaw/memory-memx/
```

This includes:
- SQLite database with memories and relationships
- Vector embeddings index
- Configuration snapshots

## Further Information

- Repository: https://github.com/NeoLi00/openclaw-memx
- Architecture documentation: `ARCHITECTURE.md` in repository
- Contact: neoliriven@gmail.com
- OpenClaw documentation: https://openclaw.com (requires OpenClaw 2026.3.25+)
