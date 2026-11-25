---
name: domino-llm-access
description: Decide and implement how code running in Domino reaches a Large Language Model, LLM Gateway 2.0 first where deployed (routed to domino-llm-gateway); otherwise Option A, an external provider (OpenAI, Anthropic, AWS Bedrock, Azure OpenAI, Google Vertex AI) with the API key stored as a Domino environment variable, or Option B, a Domino-hosted model endpoint (vLLM, OpenAI-compatible) created from a Hugging Face model or a registered model and called with an OpenAI-style client and the in-run access token, including the Host an LLM UI and REST API (/api/gen-ai/beta), endpoint metrics and logs. Covers the legacy AI Gateway. Use when a user asks how to call an LLM from a Workspace, Job, App or agent, which LLM path to use, where to put an LLM API key, how to get an endpoint base_url or token, how to host, deploy or serve an LLM with vLLM, or how to use or migrate off the legacy AI Gateway.
compatibility: Domino 6.3 and Domino Cloud. Requires DOMINO_API_HOST; in a run use DOMINO_API_PROXY or the localhost:8899 access-token endpoint, outside a run a Personal Access Token. The legacy AI Gateway section applies to Domino 6.3 only, and only where an administrator has enabled it.
---

# LLM access in Domino

Applies to Domino 6.3 and Domino Cloud. One section differs between them (the legacy AI Gateway); read "Which path applies" first.

## Which path applies

Four ways exist; pick in this order:

1. **LLM Gateway 2.0** (Cloud and 6.3): an extension installed and updated separately from Domino, so availability depends on the installation, not the version; where installed, use it. Callers authenticate with their Domino identity; administrators hold the provider keys, grants, budgets and guardrails. Nothing is injected; finding and confirming the base URL, and everything else: `domino-llm-gateway` skill.
2. **Option A: external provider**, where no gateway is deployed. Code calls OpenAI, Anthropic, Bedrock, Azure OpenAI or Vertex AI through the provider's SDK; Domino injects the API key as an environment variable.
3. **Option B: Domino-hosted endpoint.** Domino serves a registered model (from Hugging Face or an experiment run) with vLLM on a GPU hardware tier behind an OpenAI-compatible URL.
4. **Legacy AI Gateway**: Domino 6.3 only, where an administrator enabled it (off by default); removed from Cloud, where its UI and `/api/aigateway/*` routes are gone.

Options A and B apply to both targets (the Bedrock credential-propagation path is a 6.3 feature); the gateways vary by deployment.

Find the deployment: `GET $DOMINO_API_HOST/version` (send the bearer) returns `version`. `6.3.x` is self-managed 6.3; Cloud reports a later build. On 6.3, whether the legacy gateway is enabled is an administrator setting: confirm it in the UI (**Develop** > **Gateway LLMs** lists endpoints only where it is on) or with the administrator. Do not infer it from a 404 (retry per [HOSTS.md](../domino-api-intro/HOSTS.md#404-on-the-in-run-base)), and never enable the gateway yourself. Below 6.3 this skill does not apply: say so and point to docs.dominodatalab.com. Never tell the user to reinstall or change the plugin.

Choose Option A for a frontier model when prompts may leave the cluster; choose Option B when external providers are not permitted, data must stay resident, or the model was fine-tuned in-house. Endpoints are OpenAI-compatible, so client code moves between them by changing `base_url` and the key. For agents, `@add_tracing` (`domino-genai-tracing` skill) captures every LLM call wherever the model runs.

## Option A: call an external provider

1. Install the provider's SDK in the Compute Environment (Dockerfile instruction such as `RUN pip install openai`) or in the Workspace.
2. Store the API key as a Project environment variable; Domino injects it into Workspaces and Jobs, so it stays out of code and version control.
3. Read it with `os.environ` and call the SDK as anywhere else.

| Provider | Package | Environment variable(s) |
|---|---|---|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| AWS Bedrock | `boto3` | `AWS_PROFILE` with AWS credential propagation (6.3; on Cloud ask Domino Support; `domino-data-connectivity`): the profile name is deployment-specific, from the user or administrator, never guessed. Else `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` |
| Azure OpenAI | `openai` | `AZURE_OPENAI_API_KEY`, `AZURE_OPENAI_ENDPOINT` |
| Google Vertex AI | `google-cloud-aiplatform` | Service account credentials |

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
response = client.chat.completions.create(
    model="gpt-6.1-sol",            # example model name; use one your account can call
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

Never hard-code, commit, or pass keys on a command line.

## Option B: host a model in Domino

Needs **Project Collaborator** permission and a **GPU hardware tier** whose memory holds the model's weights (about 16 GB for a 7B model, 24 GB or more from 13B). UI walkthrough: [HOST-AN-LLM.md](./HOST-AN-LLM.md). REST equivalent (`/api/gen-ai/beta`, identical on 6.3 and Cloud): [HOST-AN-LLM-API.md](./HOST-AN-LLM-API.md).

Once the endpoint is **Running**, its **Calling** tab shows the URL (the `base_url`) and a ready-made snippet. Inside a Workspace, Job or App the bearer is the in-run access token (in an App, the publisher's); it is short-lived, so fetch it per call in an App or long Job:

```python
import os
import requests
from openai import OpenAI

ENDPOINT_URL = os.environ["LLM_ENDPOINT_URL"]            # copied from the Calling tab

def token() -> str:                                      # in-run access token, fresh per call
    proxy = os.environ.get("DOMINO_API_PROXY", "http://localhost:8899")
    return requests.get(f"{proxy}/access-token", timeout=5).text.strip()

client = OpenAI(base_url=ENDPOINT_URL, api_key=token())
response = client.chat.completions.create(
    model="your-model-name",   # the endpoint's servedModelName
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

The OpenAI Responses API is also supported. Keep the URL in a Domino environment variable such as `LLM_ENDPOINT_URL` so promotion to a production endpoint is a configuration change. The access token is short-lived and exists only inside a Domino execution; code outside Domino uses a Personal Access Token as the bearer. Legacy user API keys are deprecated; do not use them.

## Gateways

**LLM Gateway 2.0**: the successor to the legacy AI Gateway, one OpenAI-compatible base URL in front of external providers and Domino-hosted models; an extension an administrator installs and updates separately from Domino. Calling it, coding assistants through it and the administrator's setup: `domino-llm-gateway` skill.

**Legacy AI Gateway** (6.3 only, where enabled): [LEGACY-AI-GATEWAY.md](./LEGACY-AI-GATEWAY.md) covers the Gateway LLMs UI, the MLflow Deployment Client calls it supports, the `/api/aigateway/v1` routes and bodies, and the audit download.

**Migrating off the legacy AI Gateway** (its MLflow Deployment Client calls and `/api/aigateway/` URLs fail on Cloud and where the gateway is disabled): [LEGACY-AI-GATEWAY.md](./LEGACY-AI-GATEWAY.md#migrating-away).

## Documentation

- Set up LLM access: https://docs.domino.ai/cloud/platform-capabilities/features/llms (6.3: replace `cloud` with `6.3`)
- Host an LLM: https://docs.domino.ai/cloud/platform-capabilities/features/llms/host-an-llm
- LLM Gateway 2.0 and migration: https://docs.domino.ai/cloud/platform-capabilities/features/llms/llm-gateway
- Legacy AI Gateway (6.3): https://docs.domino.ai/6.3/platform-capabilities/features/llms/ai-gateway
- Authentication: https://docs.domino.ai/cloud/reference/api/domino-api-authentication
