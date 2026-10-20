---
name: local-llm-coding-assistant
description: Wire a local LLM into VS Code and the terminal as a Copilot fallback using Continue, Cline, Aider, or llama.vscode. Use when premium copilot tokens are exhausted or when working offline / on private code, and you want inline completions, chat, and edit-apply loops backed by a local model.
source: self
date_added: 2026-05-01
---

# Local LLM Coding Assistant

Use a local LLM as a practical day-to-day coding assistant — not just a chatbot. Goal: inline suggestions, repo-aware chat, and "apply this edit" workflows that approximate hosted copilots well enough to keep you productive.

## When to Use

- Premium Copilot / Cursor / Claude credits are exhausted and you need to keep shipping
- You are on a plane, train, or air-gapped network
- The code or prompt cannot legally leave your machine
- You want to A/B a local model against a hosted one on the same task

## Prerequisites

- A working local inference endpoint (see `local-llm-setup`)
- A model chosen for coding (see `local-llm-model-selection`) — Qwen2.5-Coder family is the current default
- An OpenAI-compatible base URL like `http://localhost:11434/v1` (Ollama) or `http://localhost:8080/v1` (llama-server)

## Tool Picks By Workflow

| Workflow | Tool | Why |
| --- | --- | --- |
| Inline completions in VS Code | `llama.vscode` or `Continue` autocomplete | FIM-aware, low-latency, works with local servers |
| Chat with file/repo context | `Continue` | Mature VS Code/JetBrains plugin, OpenAI-compatible providers, `@file` / `@codebase` |
| Agentic edits ("apply diff") | `Cline` (VS Code) or `Aider` (CLI) | Plan → edit → run loops; both speak OpenAI-compatible |
| Terminal pair-programming | `Aider` | Git-aware, surgical edits, repo map, runs tests |
| Quick one-shot from shell | `ollama run` / `llm` CLI | No project setup needed |

You can run several in parallel — e.g. `llama.vscode` for ghost-text completions plus `Continue` for chat — pointed at the same daemon.

## Minimal Configurations

### Continue (`~/.continue/config.json`)

```jsonc
{
  "models": [
    {
      "title": "Local Qwen Coder 14B",
      "provider": "openai",
      "model": "qwen2.5-coder:14b-instruct-q4_K_M",
      "apiBase": "http://localhost:11434/v1",
      "apiKey": "ollama"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Local Qwen Coder 7B (FIM)",
    "provider": "openai",
    "model": "qwen2.5-coder:7b-base-q4_K_M",
    "apiBase": "http://localhost:11434/v1",
    "apiKey": "ollama"
  }
}
```

Use the **base** (not instruct) variant for autocomplete — it follows fill-in-the-middle templates correctly. Use the **instruct** variant for chat.

### Aider

```bash
# OpenAI-compatible endpoint
export OPENAI_API_BASE=http://localhost:11434/v1
export OPENAI_API_KEY=ollama
aider --model openai/qwen2.5-coder:14b-instruct-q4_K_M
```

Add `--no-auto-commits` while you trust-build the model. Use `/add` to scope context tightly — local models degrade fast past their effective context window.

### Cline

In Cline settings, choose "OpenAI Compatible", set base URL to your local endpoint, and pick an instruct-tuned model with tool-use training (Qwen2.5-Coder-Instruct 14B+ recommended for agent loops).

## Patterns That Actually Work Locally

- **Tight context.** Hosted models forgive sloppy context; local 7B–14B models do not. Use `@file`/`/add` to include only what's needed.
- **Short turns.** Ask for one function or one diff at a time, then iterate. Long monolithic answers degrade.
- **Constrain the output.** "Reply with only a unified diff", "Reply with only the function body" — local models obey format constraints well when stated up front.
- **Pin the model.** Switching tags between sessions changes behavior subtly; pin exact quant tags.
- **Separate completion from chat.** Use a small base model (1B–7B) for ghost-text and a larger instruct model for chat; the autocomplete one needs to be fast, the chat one smart.
- **Bring your own retrieval.** For repo-wide questions, a local embeddings model (`nomic-embed-text`, `bge-m3`) plus a simple top-k retriever beats stuffing the whole repo into context.

## Anti-Patterns

- Pointing autocomplete at a 32B model — latency makes it unusable; use a 1B–7B base model instead.
- Using an instruct-only model for FIM completion — it will narrate instead of completing.
- Letting an agent loop run unbounded against a weak local model — it will burn time on bad plans. Cap iterations and require human approval per edit.
- Ignoring the chat template — every front-end has a "raw prompt" debug view; check that `<|im_start|>` / `<|user|>` tokens look right.
- Running long contexts without verifying the model's *effective* window. Many "128k" models start to drift past 16–32k.

## Verification

- Inline completion latency feels < 300 ms to first token on the autocomplete model
- Chat responses are coherent and respect format constraints on a 5-turn conversation
- An Aider/Cline edit cycle produces a clean diff that applies and passes existing tests
- A 30-minute work session does not require restarting the local daemon

## References

- Continue: <https://github.com/continuedev/continue>
- Cline: <https://github.com/cline/cline>
- Aider: <https://github.com/Aider-AI/aider>
- llama.vscode: <https://github.com/ggml-org/llama.vscode>
