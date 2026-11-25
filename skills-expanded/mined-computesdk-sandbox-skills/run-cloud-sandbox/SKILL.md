---
name: run-cloud-sandbox
description: Guide for creating and managing Run Cloud sandboxes using ComputeSDK. Use when building applications that need Run Cloud provider for ComputeSDK - fast Firecracker microVM sandboxes with snapshots and filesystem access.
---

# Run Cloud Sandboxes with ComputeSDK

Run Cloud provider for ComputeSDK - fast Firecracker microVM sandboxes with snapshots and filesystem access.

## Setup

```bash
npm install computesdk @computesdk/run-cloud
```

Set your credentials:

```bash
# .env
RUN_CLOUD_API_KEY=your_run_cloud_api_key
RUN_CLOUD_API_TOKEN=your_run_cloud_api_token
RUN_CLOUD_API_URL=your_run_cloud_api_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { runCloud } from '@computesdk/run-cloud';

compute.setConfig({
  provider: runCloud({
    apiKey: process.env.RUN_CLOUD_API_KEY,
    apiUrl: process.env.RUN_CLOUD_API_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Run Cloud!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { runCloud } from '@computesdk/run-cloud';

const sdk = runCloud({
    apiKey: process.env.RUN_CLOUD_API_KEY,
    apiUrl: process.env.RUN_CLOUD_API_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## Run Cloud Configuration

```typescript
interface RunCloudConfig {

  /** API key. Falls back to RUN_CLOUD_API_KEY, then RUN_CLOUD_API_TOKEN. */
  apiKey?: string;
  /** API origin. Falls back to RUN_CLOUD_API_URL, then https://api.run.cloud. */
  apiUrl?: string;
  /** Custom fetch implementation, useful in proxies and tests. */
  fetch?: typeof fetch;
  /** Default OCI image registered with Run Cloud. */
  image?: string;
  /** Default vCPU allocation. Fractional values are supported. */
  cpu?: number;
  /** Default memory allocation in MiB. */
  memory?: number;
  /** Default writable disk quota in GiB. */
  disk?: number;
  /** Default automatic idle-pause delay in seconds. Set 0 to disable. */
  idlePauseSeconds?: number;
  /** Default sandbox lifetime in milliseconds. Set 0 to disable. */
  timeout?: number;
  /** Default region. */
  region?: string;
  /** Default organization ID. */
  orgId?: string;
  /** Default command timeout in milliseconds. */
  commandTimeout?: number;
  /** Lifetime of public port URLs in seconds. Defaults to one hour. */
  tunnelTtlSeconds?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
