---
name: tensorlake-sandbox
description: Guide for creating and managing Tensorlake sandboxes using ComputeSDK. Use when building applications that need Tensorlake provider for ComputeSDK - stateful MicroVM sandboxes for agentic applications and LLM-generated code execution.
---

# Tensorlake Sandboxes with ComputeSDK

Tensorlake provider for ComputeSDK - stateful MicroVM sandboxes for agentic applications and LLM-generated code execution.

## Setup

```bash
npm install computesdk @computesdk/tensorlake
```

Set your credentials:

```bash
# .env
TENSORLAKE_API_KEY=your_tensorlake_api_key
TENSORLAKE_API_URL=your_tensorlake_api_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { tensorlake } from '@computesdk/tensorlake';

compute.setConfig({
  provider: tensorlake({
    apiKey: process.env.TENSORLAKE_API_KEY,
    apiUrl: process.env.TENSORLAKE_API_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Tensorlake!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { tensorlake } from '@computesdk/tensorlake';

const sdk = tensorlake({
    apiKey: process.env.TENSORLAKE_API_KEY,
    apiUrl: process.env.TENSORLAKE_API_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## Tensorlake Configuration

```typescript
interface TensorlakeConfig {

  /** Tensorlake API key — falls back to TENSORLAKE_API_KEY environment variable */
  apiKey?: string;
  /** Override for the management API base URL */
  apiUrl?: string;
  /** Override for the sandbox proxy URL */
  proxyUrl?: string;
  /** Default container image for new sandboxes (default: ubuntu-minimal) */
  image?: string;
  /** Default timeout in milliseconds for sandboxes */
  timeout?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
