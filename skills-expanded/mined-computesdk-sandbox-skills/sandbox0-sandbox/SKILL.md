---
name: sandbox0-sandbox
description: Guide for creating and managing Sandbox0 sandboxes using ComputeSDK. Use when building applications that need Sandbox0 provider for ComputeSDK - fast persistent sandboxes with command execution and native filesystem access.
---

# Sandbox0 Sandboxes with ComputeSDK

Sandbox0 provider for ComputeSDK - fast persistent sandboxes with command execution and native filesystem access.

## Setup

```bash
npm install computesdk @computesdk/sandbox0
```

Set your credentials:

```bash
# .env
SANDBOX0_API_KEY=your_sandbox0_api_key
SANDBOX0_BASE_URL=your_sandbox0_base_url
SANDBOX0_TEAM_ID=your_sandbox0_team_id
SANDBOX0_TEMPLATE=your_sandbox0_template
SANDBOX0_TOKEN=your_sandbox0_token
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { sandbox0 } from '@computesdk/sandbox0';

compute.setConfig({
  provider: sandbox0({
    token: process.env.SANDBOX0_TOKEN,
    baseUrl: process.env.SANDBOX0_BASE_URL,
    teamId: process.env.SANDBOX0_TEAM_ID,
    templateId: process.env.SANDBOX0_TEMPLATE,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Sandbox0!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { sandbox0 } from '@computesdk/sandbox0';

const sdk = sandbox0({
    token: process.env.SANDBOX0_TOKEN,
    baseUrl: process.env.SANDBOX0_BASE_URL,
    teamId: process.env.SANDBOX0_TEAM_ID,
    templateId: process.env.SANDBOX0_TEMPLATE,
  });
const sandbox = await sdk.sandbox.create();
```

## Sandbox0 Configuration

```typescript
interface Sandbox0Config {

  /** Team API key, or an access token when teamId is set. */
  token?: string;
  /** Team ID for access-token authentication. Falls back to SANDBOX0_TEAM_ID. */
  teamId?: string;
  /** API endpoint. Falls back to SANDBOX0_BASE_URL, then the SDK default. */
  baseUrl?: string;
  /** Default template for new sandboxes. Falls back to SANDBOX0_TEMPLATE, then `coding-agent`. */
  templateId?: string;
  /** Default soft runtime TTL in seconds. */
  ttl?: number;
  /** Default hard sandbox TTL in seconds. */
  hardTtl?: number;
  /** Default memory limit as MiB or a Kubernetes quantity such as `1Gi`. */
  memory?: number | string;
  /** Default environment variables for new sandboxes. */
  envs?: Record<string, string>;
  /** Default command timeout in milliseconds. */
  commandTimeout?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
