---
name: opencomputer-sandbox
description: Guide for creating and managing OpenComputer sandboxes using ComputeSDK. Use when building applications that need OpenComputer provider for ComputeSDK - persistent cloud VMs with checkpoints, preview URLs, command execution, and filesystem access.
---

# OpenComputer Sandboxes with ComputeSDK

OpenComputer provider for ComputeSDK - persistent cloud VMs with checkpoints, preview URLs, command execution, and filesystem access.

## Setup

```bash
npm install computesdk @computesdk/opencomputer
```

Set your credentials:

```bash
# .env
OPENCOMPUTER_API_KEY=your_opencomputer_api_key
OPENCOMPUTER_API_URL=your_opencomputer_api_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { opencomputer } from '@computesdk/opencomputer';

compute.setConfig({
  provider: opencomputer({
    apiKey: process.env.OPENCOMPUTER_API_KEY,
    apiUrl: process.env.OPENCOMPUTER_API_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from OpenComputer!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { opencomputer } from '@computesdk/opencomputer';

const sdk = opencomputer({
    apiKey: process.env.OPENCOMPUTER_API_KEY,
    apiUrl: process.env.OPENCOMPUTER_API_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## OpenComputer Configuration

```typescript
interface OpenComputerConfig {

  /** OpenComputer API key - falls back to OPENCOMPUTER_API_KEY. */
  apiKey?: string;
  /** OpenComputer API URL - falls back to OPENCOMPUTER_API_URL, then production. */
  apiUrl?: string;
  /** Default template for new sandboxes. Defaults to OpenComputer's `base` template. */
  template?: string;
  /** Default idle timeout in milliseconds. OpenComputer receives this as seconds. */
  timeout?: number;
  /** Default environment variables for new sandboxes. */
  envs?: Record<string, string>;
  /** Default metadata for new sandboxes. */
  metadata?: Record<string, string>;
  /** OpenComputer CPU count for new sandboxes. */
  cpuCount?: number;
  /** OpenComputer memory size in MB for new sandboxes. */
  memoryMB?: number;
  /** OpenComputer workspace disk size in MB for new sandboxes. */
  diskMB?: number;
  /** Secret store to attach to new sandboxes. */
  secretStore?: string;
  /** Create Burst sandboxes by default. */
  burst?: boolean;
  /** Require bearer auth on preview URLs. */
  previewAuth?: { scheme?: 'bearer'; token?: 'auto' | string };

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
