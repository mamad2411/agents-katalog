---
name: langfuse-prompts
description: Manage prompts in Langfuse, including versioning, labels, compile-time variables, caching, fallbacks, and linking prompts to traces. Use when moving prompts out of code or deploying prompt changes safely.
---

# Langfuse Prompt Management

Prompts live in Langfuse, versioned automatically, and are fetched by your app
at runtime. This decouples prompt deployment from code deployment.

## Prompt types

- **Text**: a single string template.
- **Chat**: an array of `{role, content}` messages (system, user, assistant).

The type is chosen at creation and cannot be changed later. Variables use
`{{doubleBraces}}` syntax in both types.

## Create prompts

Via the Langfuse UI, or via SDK:

```python
from langfuse import get_client
langfuse = get_client()

langfuse.create_prompt(
    name="movie-critic",
    type="text",
    prompt="As a {{criticLevel}} critic, rate {{movie}} out of 10.",
    labels=["production"],
    config={"model": "gpt-4o", "temperature": 0.7},
)
```

`config` is a free-form JSON field: store model, parameters, or tool schemas
next to the prompt so a prompt version pins its full runtime configuration.

## Fetch and compile

```python
prompt = langfuse.get_prompt("movie-critic")            # production label
prompt = langfuse.get_prompt("movie-critic", label="staging")
prompt = langfuse.get_prompt("movie-critic", version=3)

text = prompt.compile(criticLevel="expert", movie="Dune")
model = prompt.config.get("model")
```

JS/TS: `langfuse.prompt.get("movie-critic")` then `prompt.compile({...})`.
By default fetches resolve the `production` label.

## Labels and deployment

- Every save creates a new immutable version.
- Labels (`production`, `latest`, or custom like `staging`, `tenant-a`) are
  movable pointers; deploying = moving a label to a new version.
- Roll back by pointing `production` at an older version, no code change.

## Caching and fallbacks

- Prompts are cached client-side after first fetch, so runtime overhead is
  near zero; tune with the SDK cache TTL option if you need faster rollout of
  label moves.
- Provide a `fallback` prompt in `get_prompt` calls for cold starts when the
  Langfuse API is unreachable, so your app never hard-fails on prompt fetch.

## Link prompts to traces

Pass the fetched prompt object into your generation so Langfuse can correlate
metrics (cost, latency, scores) per prompt version:

- Python OpenAI integration: `langfuse_prompt=prompt` kwarg on the call.
- Manual observations: set the prompt on the generation
  (`langfuse.update_current_generation(prompt=prompt)`).

This powers per-version dashboards: compare version 4 vs 5 on real traffic
before moving the `production` label.

## Practices

- Never hardcode prompt text in code once it is managed in Langfuse; code
  references the name and label only.
- Use a `staging` label plus dataset experiments (see `langfuse-evals`) before
  promoting to `production`.
- Store model and parameters in `config` so prompt iterations can also change
  model settings atomically.
- Managing prompts via MCP is also supported; the bundled Docs MCP server can
  fetch current parameter shapes when in doubt.
