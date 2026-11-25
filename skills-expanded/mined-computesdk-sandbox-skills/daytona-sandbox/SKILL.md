---
name: daytona-sandbox
description: Guide for creating and managing Daytona sandboxes using ComputeSDK. Use when building applications that need Daytona provider for ComputeSDK - standardized development environments with devcontainer support.
---

# Daytona Sandboxes with ComputeSDK

Daytona provider for ComputeSDK - standardized development environments with devcontainer support.

## Setup

```bash
npm install computesdk @computesdk/daytona
```

Set your credentials:

```bash
# .env
DAYTONA_API_KEY=your_daytona_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { daytona } from '@computesdk/daytona';

compute.setConfig({
  provider: daytona({
    apiKey: process.env.DAYTONA_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Daytona!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { daytona } from '@computesdk/daytona';

const sdk = daytona({
    apiKey: process.env.DAYTONA_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## Daytona Configuration

```typescript
interface DaytonaConfig {

  /** Daytona API key - if not provided, will fallback to DAYTONA_API_KEY environment variable */
  apiKey?: string;
  /** Default runtime environment (e.g. 'python', 'node') */
  runtime?: string;
  /** Execution timeout in milliseconds */
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
