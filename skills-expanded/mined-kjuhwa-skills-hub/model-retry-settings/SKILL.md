---
name: model-retry-settings
description: Configure exponential backoff and retry policy for transient model API errors.
category: agents
version: 1.0.0
version_origin: extracted
confidence: high
tags: [openai-agents, retry, backoff, resilience, model-settings]
source_type: extracted-from-git
source_url: https://github.com/openai/openai-agents-python.git
source_ref: main
source_commit: e80d2d2319eb300ac17ec496988b70246a5042d6
source_project: openai-agents-python
source_path: examples/basic/retry.py
imported_at: 2026-04-18T00:00:00Z
---

# model-retry-settings

Set `ModelRetrySettings` on `ModelSettings` to configure max retries, backoff strategy, and a custom retry policy. Pass to `RunConfig` for run-wide defaults or per-agent `model_settings`.

## When to apply

When running agents in production where 429/5xx errors are expected. Prevents hard failures on transient rate-limit or server errors.

## Core snippet

```python
from agents import Agent, ModelRetrySettings, ModelSettings, RetryDecision, RunConfig, Runner, retry_policies

apply_policies = retry_policies.any(
    retry_policies.provider_suggested(),
    retry_policies.retry_after(),
    retry_policies.network_error(),
    retry_policies.http_status([408, 409, 429, 500, 502, 503, 504]),
)

retry = ModelRetrySettings(
    max_retries=4,
    backoff={
        "initial_delay": 0.5,
        "max_delay": 5.0,
        "multiplier": 2.0,
        "jitter": True,
    },
    policy=apply_policies,
)

run_config = RunConfig(model_settings=ModelSettings(retry=retry))

agent = Agent(
    name="Assistant",
    instructions="You are a concise assistant.",
    model_settings=ModelSettings(retry=retry),
)

result = await Runner.run(agent, "Hello!", run_config=run_config)
```

## Key notes

- `RunConfig.model_settings` sets run-wide defaults; per-agent `model_settings` overrides for overlapping keys
- `retry_policies.provider_suggested()` respects `x-should-retry` headers from OpenAI
- `jitter=True` adds randomness to avoid thundering-herd retries
- Per-agent retry config overrides `RunConfig` when both are set
