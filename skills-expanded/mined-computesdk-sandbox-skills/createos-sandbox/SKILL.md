---
name: createos-sandbox
description: Guide for creating and managing CreateOS sandboxes using ComputeSDK. Use when building applications that need CreateOS provider for ComputeSDK — NodeOps VM sandboxes with pause/resume/fork snapshots.
---

# CreateOS Sandboxes with ComputeSDK

CreateOS provider for ComputeSDK — NodeOps VM sandboxes with pause/resume/fork snapshots.

## Setup

```bash
npm install computesdk @computesdk/createos-sandbox
```

Set your credentials:

```bash
# .env
CREATEOS_SANDBOX_API_KEY=your_createos_sandbox_api_key
CREATEOS_SANDBOX_BASE_URL=your_createos_sandbox_base_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { createosSandbox } from '@computesdk/createos-sandbox';

compute.setConfig({
  provider: createosSandbox({
    apiKey: process.env.CREATEOS_SANDBOX_API_KEY,
    baseUrl: process.env.CREATEOS_SANDBOX_BASE_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from CreateOS!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { createosSandbox } from '@computesdk/createos-sandbox';

const sdk = createosSandbox({
    apiKey: process.env.CREATEOS_SANDBOX_API_KEY,
    baseUrl: process.env.CREATEOS_SANDBOX_BASE_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## CreateOS Configuration

```typescript
interface CreateosConfig {

  /** createos-sandbox API key. Falls back to the CREATEOS_SANDBOX_API_KEY env var. */
  apiKey?: string;
  /** Control-plane base URL. Falls back to the CREATEOS_SANDBOX_BASE_URL env
   *  var, then the production control plane. */
  baseUrl?: string;
  /** Default shape when create options pin neither `shape` nor cpus/memoryMb. */
  shape?: string;
  /** Default rootfs catalog name or template id. Empty = host default. */
  rootfs?: string;
  /** Reported `getInfo().timeout` in ms. Informational only. */
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
