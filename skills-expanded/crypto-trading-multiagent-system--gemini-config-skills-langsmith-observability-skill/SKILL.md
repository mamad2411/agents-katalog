---
name: langsmith-observability
description: Use this skill when launching the local LangGraph visual development server (Studio), verifying LangSmith tracing environment variables, or testing agent telemetry.
---

# LangGraph & LangSmith Observability Workflow

This skill manages local agent debugging, tracing configurations, and interaction with LangGraph Studio for real-time state manipulation.

## 🛠️ Tracing & Studio Prerequisites

Before starting local dev servers, verify that your local `.env` contains active tracking credentials to automatically pipe node executions into LangSmith:

    LANGSMITH_TRACING=true
    LANGSMITH_API_KEY=ls__your_api_key_here
    LANGSMITH_PROJECT=langgraph-agent-dev
    LANGSMITH_ENDPOINT=https://api.smith.langchain.com

---

## 🏃‍♂️ Core Observability Commands

### 1. Launch Local LangGraph Dev Server (Studio)

Boot the lightweight local development server. This parses your `langgraph.json` configuration, auto-loads the `.env` parameters, and opens the local streaming visual UI:

```bash
uv run langgraph dev
```

### 2. Verify Local API Liveness

If the studio UI or client SDK is failing to stream transitions, verify that the local routing daemon is responsive (Default port: 2024):

```bash
curl -s http://127.0.0.1:2024/ok
```

### 3. Check LangGraph Project Validation

Explicitly validate your graph mappings, dependencies, and configuration schema defined inside `langgraph.json` without booting the server:

```bash
uv run langgraph validation validate
```

### 4. Check LangGraph Project Validation

Explicitly validate your graph mappings, dependencies, and configuration schema defined inside `langgraph.json` without booting the server:

```bash
uv run langgraph validation validate
```

---

## ⚙️ Environment Integrity Rules

1. **Never Hardcode Keys:** Ensure all `ls__` tokens are extracted natively from environment parameters.
2. **Handle Sync Blocks:** If the UI logs blockages, remind the runtime environment that nodes contain synchronous code by invoking the server with the blocking allowances:

```bash
uv run langgraph dev --allow-blocking
```
