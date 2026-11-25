---
name: zero-bill-router
description: Route coding-agent LLM requests through a local OpenAI-compatible proxy with automatic free-tier API failover and local Ollama routing to cut API bills to $0.
---

# Zero-Bill Router Agent Skill

This skill guides AI coding assistants (Cursor, Claude Code, Cline, Codex, Gemini CLI) to configure, verify, and route their requests through a local `zero-bill-router` instance to eliminate recurring API costs.

## When to Use This Skill

Activate this skill when:
- Setting up or troubleshooting the local LLM proxy for coding workflows.
- Verifying available local Ollama models and free-tier cloud provider quotas.
- Reviewing token consumption and dollar savings metrics.
- Configuring environment variables to redirect coding agent traffic through the proxy.

---

## Agent Step-by-Step Workflow

### Step 1: Check if the Proxy Server is Running

Before routing requests, verify if the local `zero-bill-router` daemon is listening on port 8787:

```bash
curl -s http://127.0.0.1:8787/health
```

- **If HTTP 200 is returned**: Parse the JSON response:
  ```json
  {"status": "ok", "ollama_enabled": true, "active_providers": ["groq", "openrouter"]}
  ```
  The router is live and ready to accept requests.
- **If the connection fails or times out**: The router is not running. Instruct the user to initialize and start the service (Step 2).

---

### Step 2: Initialize and Start the Router (If Not Running)

If the router daemon is stopped:

1. **Initialize configuration** (creates `zero-bill.yaml` from template):
   ```bash
   zero-bill init
   ```
2. **Add API keys for free-tier cloud providers** (optional, recommended for heavy workloads):
   - Groq: `export GROQ_API_KEY="gsk_..."`
   - OpenRouter Free: `export OPENROUTER_API_KEY="sk-or-..."`
   - Google AI Studio: `export GEMINI_API_KEY="AIza..."`
3. **Start the proxy daemon**:
   ```bash
   zero-bill serve --config zero-bill.yaml
   ```

---

### Step 3: Verify Provider Health & Quotas

Run a non-destructive ping check across all configured providers:

```bash
zero-bill check --config zero-bill.yaml
```

The output displays an ASCII status table:
- **`OK`**: Endpoint responded within 5 seconds; ready for traffic.
- **`NO KEY`**: Environment variable is unset; provider is marked inactive without crashing.
- **`ERROR`**: Service returned an HTTP error or timed out (e.g., local Ollama is shut down).

---

### Step 4: Configure the Coding Agent Environment

Direct the agent or editor to the local OpenAI-compatible proxy by setting standard environment variables:

```bash
export OPENAI_BASE_URL="http://127.0.0.1:8787/v1"
export OPENAI_API_KEY="zero-bill"
```

Configure your tool/editor settings:
- **Model**: `zero-bill-auto` (or a specific provider alias like `groq`, `gemini`, `ollama`).
- **Base URL**: `http://127.0.0.1:8787/v1`
- **API Key**: `zero-bill` (or any non-empty string).

---

### Step 5: Monitor Token Usage & Dollar Savings

Review accumulated metrics at any time by running:

```bash
zero-bill stats
```

This displays:
- Breakdown by provider (requests count, prompt tokens, completion tokens, actual expenditure).
- Estimated savings compared to industry flagship pricing ($3.00/1M input, $15.00/1M output).
