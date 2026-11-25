---
name: railway-sandbox
description: Guide for creating and managing Railway sandboxes using ComputeSDK. Use when building applications that need Railway Sandboxes provider for ComputeSDK - run commands in Railway-hosted sandboxes.
---

# Railway Sandboxes with ComputeSDK

Railway Sandboxes provider for ComputeSDK - run commands in Railway-hosted sandboxes.

## Setup

```bash
npm install computesdk @computesdk/railway
```

Set your credentials:

```bash
# .env
RAILWAY_API_TOKEN=your_railway_api_token
RAILWAY_ENVIRONMENT_ID=your_railway_environment_id
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { railway } from '@computesdk/railway';

compute.setConfig({
  provider: railway({
    token: process.env.RAILWAY_API_TOKEN,
    environmentId: process.env.RAILWAY_ENVIRONMENT_ID,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Railway!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { railway } from '@computesdk/railway';

const sdk = railway({
    token: process.env.RAILWAY_API_TOKEN,
    environmentId: process.env.RAILWAY_ENVIRONMENT_ID,
  });
const sandbox = await sdk.sandbox.create();
```

## Railway Configuration

```typescript
interface RailwayConfig {

  /** Railway API token - falls back to the RAILWAY_API_TOKEN environment variable */
  token?: string;
  /** Railway environment ID - falls back to the RAILWAY_ENVIRONMENT_ID environment variable */
  environmentId?: string;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
