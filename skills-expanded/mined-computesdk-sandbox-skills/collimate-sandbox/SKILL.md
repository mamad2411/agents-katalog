---
name: collimate-sandbox
description: Guide for creating and managing Collimate sandboxes using ComputeSDK. Use when building applications that need Collimate provider for ComputeSDK.
---

# Collimate Sandboxes with ComputeSDK

Collimate provider for ComputeSDK.

## Setup

```bash
npm install computesdk @computesdk/collimate
```

Set your credentials:

```bash
# .env
COLLIMATE_API_KEY=your_collimate_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { collimate } from '@computesdk/collimate';

compute.setConfig({
  provider: collimate({
    apiKey: process.env.COLLIMATE_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Collimate!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { collimate } from '@computesdk/collimate';

const sdk = collimate({
    apiKey: process.env.COLLIMATE_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## Collimate Configuration

```typescript
interface CollimateConfig {

  /** Collimate API server URL. Default: "https://api.collimate.ai" */
  serverUrl?: string;
  /** API key. Falls back to COLLIMATE_API_KEY env var. */
  apiKey?: string;
  /** Default template ID for sandbox creation. */
  templateId?: string;
  /** Default execution timeout in seconds. Default: 900 */
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
