---
name: freestyle-sandbox
description: Guide for creating and managing Freestyle sandboxes using ComputeSDK. Use when building applications that need Freestyle provider for ComputeSDK - cloud sandboxes powered by Freestyle.
---

# Freestyle Sandboxes with ComputeSDK

Freestyle provider for ComputeSDK - cloud sandboxes powered by Freestyle.

## Setup

```bash
npm install computesdk @computesdk/freestyle
```

Set your credentials:

```bash
# .env
FREESTYLE_API_KEY=your_freestyle_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { freestyle } from '@computesdk/freestyle';

compute.setConfig({
  provider: freestyle({
    apiKey: process.env.FREESTYLE_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Freestyle!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { freestyle } from '@computesdk/freestyle';

const sdk = freestyle({
    apiKey: process.env.FREESTYLE_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## Freestyle Configuration

```typescript
interface FreestyleConfig {

  apiKey?: string;
  /** Default runtime hint (e.g. 'node', 'python') */
  runtime?: string;
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
