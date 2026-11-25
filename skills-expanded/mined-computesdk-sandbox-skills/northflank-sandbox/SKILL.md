---
name: northflank-sandbox
description: Guide for creating and managing Northflank sandboxes using ComputeSDK. Use when building applications that need Northflank provider for ComputeSDK - Deploy and manage compute workloads on Northflank's container platform.
---

# Northflank Sandboxes with ComputeSDK

Northflank provider for ComputeSDK - Deploy and manage compute workloads on Northflank's container platform.

## Setup

```bash
npm install computesdk @computesdk/northflank
```

Set your credentials:

```bash
# .env
NORTHFLANK_PROJECT_ID=your_northflank_project_id
NORTHFLANK_TOKEN=your_northflank_token
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { northflank } from '@computesdk/northflank';

compute.setConfig({
  provider: northflank({
    token: process.env.NORTHFLANK_TOKEN,
    projectId: process.env.NORTHFLANK_PROJECT_ID,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Northflank!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { northflank } from '@computesdk/northflank';

const sdk = northflank({
    token: process.env.NORTHFLANK_TOKEN,
    projectId: process.env.NORTHFLANK_PROJECT_ID,
  });
const sandbox = await sdk.sandbox.create();
```

## Northflank Configuration

```typescript
interface NorthflankConfig {

  token: string;
  projectId: string;
  teamId?: string;
  host?: string;
  servicePrefix?: string;
  image?: string;
  runtime?: string;
  deploymentPlan?: string;
  ports?: NorthflankPortInput[];
  timeout?: number;
  /** Deploy from a Northflank build service instead of an external image */
  internalDeployment?: NorthflankInternalDeployment;
  /** Ephemeral storage per container in MB (e.g. 5120 for 5 GiB). Maps to `deployment.storage.ephemeralStorage.storageSize` in the Northflank API. */
  ephemeralStorageSize?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
