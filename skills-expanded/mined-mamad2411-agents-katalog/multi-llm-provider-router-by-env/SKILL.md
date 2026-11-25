---
name: multi-llm-provider-router-by-env
description: One factory function dispatches to the right LLM client based on a single LLM_PROVIDER env var, picking provider-specific base URL, env-var name for the API key, model id, and parameter quirks (e.g. max_completion_tokens for o1/gpt-5).
category: configuration
version: 1.0.0
version_origin: extracted
tags: [llm, provider-routing, anthropic, openai, ollama, bedrock]
confidence: high
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/services/llm_client.py
imported_at: 2026-04-18T00:00:00Z
---

# Multi-LLM Provider Router by Env

## When to use
Your app supports many LLM providers (Anthropic, OpenAI, OpenRouter, Gemini, NVIDIA NIM, Minimax, Ollama, Bedrock) and you want users to switch with a single env var. Reasoning vs tool-call models can be selected independently per provider.

## How it works
- `LLMSettings.from_env()` reads `LLM_PROVIDER` plus per-provider model envs (`OPENAI_REASONING_MODEL`, `ANTHROPIC_TOOLCALL_MODEL`, ...).
- `_create_llm_client(model_type)` is a single dispatch that returns a typed client (`LLMClient` for Anthropic native, `OpenAILLMClient` for any OpenAI-compatible HTTP API, `BedrockLLMClient` for Bedrock-via-Anthropic-SDK).
- OpenAI-compatible providers (OpenRouter, Gemini, NVIDIA, Ollama, Minimax) all reuse `OpenAILLMClient` with a different `base_url` and `api_key_env`.
- Reasoning models (o1, o3, o4, gpt-5*) need `max_completion_tokens` instead of `max_tokens` — picked via `_uses_max_completion_tokens(model)`.
- Singletons cached separately for "reasoning" and "tools" so a single process can route different node types to different model tiers.

## Example
```python
def _create_llm_client(model_type: str):
    settings = LLMSettings.from_env()
    p = settings.provider
    if p == "openai":
        return OpenAILLMClient(model=settings.openai_reasoning_model
                               if model_type == "reasoning"
                               else settings.openai_toolcall_model,
                               max_tokens=OPENAI_LLM_CONFIG.max_tokens)
    elif p == "openrouter":
        return OpenAILLMClient(model=..., base_url=OPENROUTER_BASE_URL,
                               api_key_env="OPENROUTER_API_KEY")
    elif p == "ollama":
        host = settings.ollama_host.rstrip("/")
        return OpenAILLMClient(model=settings.ollama_model,
                               base_url=f"{host}/v1",
                               api_key_env="OLLAMA_API_KEY",
                               api_key_default="ollama")
    elif p == "bedrock":
        return BedrockLLMClient(model=..., max_tokens=...)
    else:  # anthropic default
        return LLMClient(model=settings.anthropic_reasoning_model
                         if model_type == "reasoning"
                         else settings.anthropic_toolcall_model)

def _uses_max_completion_tokens(model: str) -> bool:
    return model.startswith(("o1", "o3", "o4", "gpt-5"))

def get_llm_for_reasoning():
    global _llm
    if _llm is None: _llm = _create_llm_client("reasoning")
    return _llm

def get_llm_for_tools():
    global _llm_for_tools
    if _llm_for_tools is None: _llm_for_tools = _create_llm_client("toolcall")
    return _llm_for_tools
```

## Gotchas
- Bedrock uses IAM auth via `AnthropicBedrock` — no API key. Keep it on a separate client class so `resolve_llm_api_key` doesn't get confused.
- Ollama needs an `api_key_default="ollama"` because the OpenAI SDK refuses an empty key.
- Always expose `reset_llm_singletons()` for tests/benchmarks that flip env vars between calls.
- `_ensure_client()` re-resolves the API key on every invocation so a key rotated mid-process is picked up.
