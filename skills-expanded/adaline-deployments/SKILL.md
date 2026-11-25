---
name: adaline-deployments
description: "Fetch deployed prompt snapshots from Adaline at runtime. Use when integrating prompt deployments, environment-based latest lookups, prompt caching, or pinned deployment IDs."
---

# Adaline Deployments

## Concepts

Adaline deployments are immutable prompt snapshots that your application fetches at runtime. The public v2 API currently exposes deployment **read** operations: create and promote deployments in the Adaline Platform UI, then fetch the approved snapshot from code.

Key terms:
- **Deployment** — a prompt snapshot deployed to an environment
- **Deployment environment** — an isolation boundary such as development, staging, or production
- **Latest deployment** — the current snapshot for a prompt/environment pair, fetched with `deploymentId=latest`
- **Pinned deployment** — a concrete deployment ID fetched directly for reproducibility

## Configuration

Set these environment variables when credentials are available:
- `ADALINE_API_KEY` — workspace API key from Admin > API Keys
- `ADALINE_PROMPT_ID` — prompt to fetch
- `ADALINE_DEPLOYMENT_ENVIRONMENT_ID` — environment for latest lookup

Base URL: `https://api.adaline.ai/v2`

## How It Works

1. Build and test a prompt in the Prompt area of Adaline.
2. Deploy the prompt snapshot to an environment in the Platform UI.
3. Fetch the current snapshot with `GET /deployments?promptId=...&deploymentId=latest&deploymentEnvironmentId=...`.
4. Cache the returned `Deployment` in your app and refresh it on a timer, restart, or product-specific webhook signal.

Each deployment includes `prompt.config`, `prompt.messages`, `prompt.tools`, and `prompt.variables`. Config values use `providerName`, `providerId`, `model`, and flexible `settings`.

## Quick Triage

| Symptom | First Fix |
|---|---|
| Fetch returns 404 | Verify `promptId`, `deploymentId`, and `deploymentEnvironmentId` |
| Latest lookup fails | Include `deploymentEnvironmentId` when `deploymentId=latest` or `current` |
| Wrong model settings | Read `deployment.prompt.config.settings`; temperature/max token fields are not top-level |
| Variables not substituted | Replace `{{name}}` placeholders in text message content before calling the provider |
| Python example returns coroutine | Await SDK methods inside an asyncio event loop |

## Approach 1: REST API

```bash
# Latest deployment for an environment
curl "https://api.adaline.ai/v2/deployments?promptId=$ADALINE_PROMPT_ID&deploymentId=latest&deploymentEnvironmentId=$ADALINE_DEPLOYMENT_ENVIRONMENT_ID" \
  -H "Authorization: Bearer $ADALINE_API_KEY"

# Specific deployment by ID
curl "https://api.adaline.ai/v2/deployments?promptId=$ADALINE_PROMPT_ID&deploymentId=deploy_abc123" \
  -H "Authorization: Bearer $ADALINE_API_KEY"
```

## Approach 2: TypeScript SDK

```typescript
import { Adaline } from '@adaline/client';

const adaline = new Adaline(); // reads ADALINE_API_KEY

const deployment = await adaline.getLatestDeployment({
  promptId: process.env.ADALINE_PROMPT_ID!,
  deploymentEnvironmentId: process.env.ADALINE_DEPLOYMENT_ENVIRONMENT_ID!,
});

const pinned = await adaline.getDeployment({
  promptId: process.env.ADALINE_PROMPT_ID!,
  deploymentId: 'deploy_abc123',
});
```

Install: `npm install @adaline/client @adaline/api`

See references/typescript-sdk.md for a complete inference example.

## Approach 3: Python SDK

```python
import asyncio
from adaline import Adaline

async def main():
    adaline = Adaline()  # reads ADALINE_API_KEY

    deployment = await adaline.get_latest_deployment(
        prompt_id="prompt_abc123",
        deployment_environment_id="environment_abc123",
    )

    pinned = await adaline.get_deployment(
        prompt_id="prompt_abc123",
        deployment_id="deploy_abc123",
    )

asyncio.run(main())
```

Install: `pip install adaline-client adaline-api`

See references/python-sdk.md for a complete inference example.

## Best Practices

1. Use latest lookup for normal runtime traffic and pinned deployment IDs for reproducible tests.
2. Cache deployments in memory; do not fetch on every user request.
3. Store IDs in environment variables or configuration, not source code.
4. Substitute variables only in text content. Preserve image, PDF, tool-call, tool-response, and reasoning content as structured objects.
5. Pass `deployment.prompt.config.settings` through to the provider after adapting provider-specific casing where needed.

## References

See references/api.md for the REST contract.
See references/typescript-sdk.md for TypeScript SDK usage.
See references/python-sdk.md for Python SDK usage.
