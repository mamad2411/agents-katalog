---
name: superserve-sandbox
description: Guide for creating and managing Superserve Provides Sandbox Infrastructure To Run Code In Isolated Cloud Environments Powered By Firecracker MicroVMs sandboxes using ComputeSDK. Use when building applications that need Superserve provides sandbox infrastructure to run code in isolated cloud environments powered by Firecracker MicroVMs.
---

# Superserve Provides Sandbox Infrastructure To Run Code In Isolated Cloud Environments Powered By Firecracker MicroVMs Sandboxes with ComputeSDK

Superserve provides sandbox infrastructure to run code in isolated cloud environments powered by Firecracker MicroVMs.

## Setup

```bash
npm install computesdk @computesdk/superserve
```

Set your credentials:

```bash
# .env
SUPERSERVE_API_KEY=your_superserve_api_key
SUPERSERVE_BASE_URL=your_superserve_base_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { superserve } from '@computesdk/superserve';

compute.setConfig({
  provider: superserve({
    apiKey: process.env.SUPERSERVE_API_KEY,
    baseUrl: process.env.SUPERSERVE_BASE_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Superserve Provides Sandbox Infrastructure To Run Code In Isolated Cloud Environments Powered By Firecracker MicroVMs!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { superserve } from '@computesdk/superserve';

const sdk = superserve({
    apiKey: process.env.SUPERSERVE_API_KEY,
    baseUrl: process.env.SUPERSERVE_BASE_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## Superserve Provides Sandbox Infrastructure To Run Code In Isolated Cloud Environments Powered By Firecracker MicroVMs Configuration

```typescript
interface SuperserveConfig {

  /** Superserve API key. Falls back to `SUPERSERVE_API_KEY` env var. */
  apiKey?: string;
  /** API base URL. Falls back to `SUPERSERVE_BASE_URL` env var, then `https://api.superserve.ai`. */
  baseUrl?: string;
  /** Default sandbox idle timeout in milliseconds. */
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
