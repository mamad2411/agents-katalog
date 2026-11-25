---
name: pydantic-settings-multi-provider-model-envs
summary: Use pydantic-settings to expose per-provider "reasoning" and "toolcall" model env vars for each supported LLM provider, so users can independently tune cost/quality tiers without code changes.
description: Pattern for pydantic-settings declaration of per-provider per-tier LLM model env vars (e.g. ANTHROPIC_REASONING_MODEL vs ANTHROPIC_TOOLCALL_MODEL) so users can independently tune cost/quality tiers without code changes.
category: configuration
version: 1.0.0
version_origin: extracted
tags: [pydantic-settings, llm, env, tiering]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/Tracer-Cloud/opensre.git
source_ref: main
source_commit: fb5ba0a1b4ef511d16c56a80f1f126b1f581d724
source_project: opensre
source_path: app/config.py
imported_at: 2026-04-18T00:00:00Z
---

# Multi-Provider Model-Tier Env Var Pattern

## When to use
You support multiple LLM providers and want independent reasoning/toolcall model selection for each. Users should be able to set `OPENAI_REASONING_MODEL=gpt-4o` and `OPENAI_TOOLCALL_MODEL=gpt-4o-mini` independently, similarly for Anthropic, Gemini, Bedrock, etc.

## How it works
Every provider has two env knobs: `<PROVIDER>_REASONING_MODEL` (heavy, for diagnosis) and `<PROVIDER>_TOOLCALL_MODEL` (light, for planning/routing). A single `LLMSettings` pydantic-settings class enumerates them all; the LLM factory picks the right one based on `model_type`.

## Example
```python
from pydantic_settings import BaseSettings

class LLMSettings(BaseSettings):
    provider: str = "anthropic"

    anthropic_reasoning_model: str = "claude-opus-4-5-20251101"
    anthropic_toolcall_model:  str = "claude-haiku-4-5-20251101"

    openai_reasoning_model:    str = "gpt-4o"
    openai_toolcall_model:     str = "gpt-4o-mini"

    gemini_reasoning_model:    str = "gemini-1.5-pro"
    gemini_toolcall_model:     str = "gemini-1.5-flash"

    bedrock_reasoning_model:   str = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    bedrock_toolcall_model:    str = "anthropic.claude-3-5-haiku-20241022-v1:0"

    ollama_host:  str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    model_config = {"env_prefix": "", "env_file": ".env", "extra": "ignore"}

    @classmethod
    def from_env(cls) -> "LLMSettings":
        return cls()

# Factory:
def _create_llm_client(model_type: str):
    s = LLMSettings.from_env()
    if s.provider == "openai":
        model = s.openai_reasoning_model if model_type == "reasoning" else s.openai_toolcall_model
        return OpenAILLMClient(model=model, ...)
    # ... other providers
```

## Gotchas
- Use `extra="ignore"` in `model_config` so unrelated env vars don't crash settings loading.
- Document each env var in README with the default; users should be able to grep one file to understand all knobs.
- Keep provider-specific sensible defaults baked in — many users never change them, but those who do need only set the one env they care about.
- Pair with the `multi-llm-provider-router-by-env` skill to tie it all together.
