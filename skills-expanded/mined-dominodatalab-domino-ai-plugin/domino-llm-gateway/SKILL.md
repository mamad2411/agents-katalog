---
name: domino-llm-gateway
description: Call Large Language Models through Domino LLM Gateway 2.0, the centrally governed gateway extension an administrator installs in front of external providers and Domino-hosted models. Covers finding and detecting the gateway, authentication with the in-run access token (fresh per call) or a Personal Access Token outside Domino, model aliases and model discovery, the OpenAI-compatible and Anthropic-compatible paths from the OpenAI and Anthropic SDKs, Pydantic AI, LangChain and plain HTTP, streaming, attribution headers, refused calls (login redirect, grants, budgets, guardrails), pointing a coding assistant such as Claude Code or Codex at the gateway, and what the administrator configures. Use when a user mentions LLM Gateway, Gateway 2.0, a gateway alias or URL, asks how to call a model through the Domino gateway, how to run a coding assistant through it, why a gateway call was refused, or what the gateway administrator must set up.
compatibility: Domino 6.3 and Domino Cloud, only where an administrator has installed the LLM Gateway 2.0 extension; availability depends on the installation, not the Domino version. Inside a Domino execution the bearer is the access token from DOMINO_API_PROXY/access-token (localhost:8899), re-read per call; outside Domino a Personal Access Token. Legacy user API keys are not used.
---

# Domino LLM Gateway 2.0

Applies to Domino 6.3 and Domino Cloud where an administrator has installed LLM Gateway 2.0. It is an **extension**: installed separately, updated out of band, so whether it exists depends on the installation, not on the Domino version. It runs as a Domino App. If nobody has installed it, say so and use the `domino-llm-access` skill (a Domino-hosted endpoint or a provider SDK); do not try to install it.

## What the gateway is

One base URL in front of many providers (external LLM vendors and Domino-hosted model endpoints). Provider keys stay in the gateway; callers authenticate with their Domino identity. Every request is tracked (user, Project, model, tokens, latency, estimated cost); administrators grant access per **model alias**, set budgets, and screen prompts and responses with guardrails.

## Find and detect the gateway

The extension injects **nothing** into a Workspace: no URL, no token, no `ANTHROPIC_*` or `OPENAI_*` variable. Use `LLM_GATEWAY_URL` if the user or an administrator created it as a Project or user variable (not a `DOMINO_`-prefixed name; Domino reserves that prefix), else ask for the gateway App's URL (`https://<domino or apps host>/apps/<app id or vanity URL>`). Confirm it **with the bearer**: `GET <base>/v1/models` returns JSON and `GET <base>/health` returns `{"status": "ok"}`. HTML proves nothing: with a bearer `<base>/` is the gateway's UI (200); without one every route is a 302 to the Domino login page.

| Family | Path | Use with |
|---|---|---|
| OpenAI-compatible | `<base>/v1` (`/models`, `/chat/completions`, `/responses`; `/embeddings` where an embedding alias exists) | OpenAI SDK, Pydantic AI, LangChain, any OpenAI-style client |
| Anthropic-compatible | `<base>/anthropic` (`/v1/messages`) | Anthropic SDK, Claude Code |

## Authentication

Send `Authorization: Bearer <token>` on every request.

- **Inside a Domino Workspace, Job or App:** read the access token from `$DOMINO_API_PROXY/access-token` (by default `http://localhost:8899/access-token`). It is short-lived, so re-read it before every request instead of caching it in a long-running process. In an App it is the publisher's token: every viewer's calls use the publisher's grants and budget, so tag them with `X-LLM-Tag-<key>` to attribute usage.
- **Outside Domino (laptop, CI):** a Domino bearer such as a Personal Access Token in a variable the user creates, for example `LLM_GATEWAY_TOKEN`. A Domino access token works from a laptop; a PAT or one of the gateway's own tokens (prefix `dgw_`, issued by an administrator) may be answered with the App login redirect or 401, in which case use a Domino access token.
- Legacy user API keys are deprecated and not used. The Anthropic path needs the bearer in `Authorization`; a credential sent only as `x-api-key` is treated as no credential.

```python
import os
import requests
from openai import OpenAI          # not in the Domino Standard Environment: pip install openai

GATEWAY = os.environ["LLM_GATEWAY_URL"].rstrip("/")

def token() -> str:
    proxy = os.environ.get("DOMINO_API_PROXY")
    if proxy:                                         # inside Domino: fresh per call
        return requests.get(f"{proxy}/access-token", timeout=5).text.strip()
    return os.environ["LLM_GATEWAY_TOKEN"]            # outside: a Domino bearer the user stored

def chat(messages, model="domino/example-alias", **kwargs) -> str:   # an alias from /v1/models
    client = OpenAI(base_url=f"{GATEWAY}/v1", api_key=token())
    return client.chat.completions.create(model=model, messages=messages, **kwargs).choices[0].message.content
```

## Models

`model` is an alias from `GET <base>/v1/models` (OpenAI list shape, `data[].id`). Aliases are administrator-defined and may carry a prefix such as `domino/`; an alias's vendor name may also be accepted, but only listed aliases are guaranteed. `GET <base>/v1/whoami` shows how the gateway resolved your identity.

The `openai`, `anthropic`, `pydantic-ai` and `langchain-openai` packages are **not** in the Domino Standard Environment: `pip install` them in a Workspace to try; add them to the Compute Environment's Dockerfile for repeat use.

## Call it

- OpenAI SDK, Responses API, embeddings, Pydantic AI, LangChain, plain HTTP and streaming: [CALLING-MODELS.md](./CALLING-MODELS.md).
- Anthropic SDK: `Anthropic(base_url=f"{GATEWAY}/anthropic", auth_token=token())`, then `client.messages.create(model="<alias>", ...)`; `api_key=` silently breaks (see errors).
- Attribution: `X-LLM-Tag-<key>: <value>` headers (for example `X-LLM-Tag-team: research`) slice usage; they are labels, not access control.
- Tracing: OpenAI and Anthropic SDK calls are autologged by `mlflow.openai.autolog()` / `mlflow.anthropic.autolog()`, so the `domino-genai-tracing` skill works unchanged.

## When a call is refused

A **302 to the Domino login page** (HTML) is a missing, malformed or expired bearer: re-read the access token per call. A 302 to `/app-consent?appId=...` means the user has not consented to the gateway App acting for them: open the gateway URL in a browser once and accept. The Anthropic SDK with `api_key=` gets that HTML as a string and fails with `AttributeError: 'str' object has no attribute 'content'`; use `auth_token=`. `404 "Model '...' not found"` is an unknown alias: list `/v1/models`. A `4xx` naming a grant, budget or guardrail rule means no access, a spent budget, or a denied prompt or response: ask the administrator, or change the prompt. A 403 such as `Only a gateway admin can manage gateway admins` is an administrator-only route. `413` from the App proxy means the body is too large. Details: [CALLING-MODELS.md](./CALLING-MODELS.md#errors-to-expect).

## Coding assistants through the gateway

Offer the user the choice; never route by default. Claude Code and Codex through the gateway, and the rule: [CODING-ASSISTANTS.md](./CODING-ASSISTANTS.md).

## What the administrator configures

Providers, model aliases, access grants and budgets, guardrails, gateway tokens, and the usage and audit views, all in the gateway UI: [ADMIN-OVERVIEW.md](./ADMIN-OVERVIEW.md). Installing and updating the extension is the administrator's domain.

## Documentation

- LLM Gateway 2.0: https://docs.domino.ai/cloud/platform-capabilities/features/llms/llm-gateway
- Set up LLM access: https://docs.domino.ai/cloud/platform-capabilities/features/llms (6.3: replace `cloud` with `6.3`)
- Authentication: https://docs.domino.ai/cloud/reference/api/domino-api-authentication
