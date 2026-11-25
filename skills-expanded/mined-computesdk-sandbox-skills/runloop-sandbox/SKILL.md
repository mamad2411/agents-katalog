---
name: runloop-sandbox
description: Guide for creating and managing Runloop sandboxes using ComputeSDK. Use when building applications that need Runloop provider for ComputeSDK - AI-optimized code execution with built-in devtools and debugging.
---

# Runloop Sandboxes with ComputeSDK

Runloop provider for ComputeSDK - AI-optimized code execution with built-in devtools and debugging.

## Setup

```bash
npm install computesdk @computesdk/runloop
```

Set your credentials:

```bash
# .env
RUNLOOP_API_KEY=your_runloop_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { runloop } from '@computesdk/runloop';

compute.setConfig({
  provider: runloop({
    apiKey: process.env.RUNLOOP_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Runloop!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { runloop } from '@computesdk/runloop';

const sdk = runloop({
    apiKey: process.env.RUNLOOP_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## Runloop Configuration

```typescript
interface RunloopConfig {

  /** Runloop API key - if not provided, will fallback to RUNLOOP_API_KEY environment variable */
  apiKey?: string;
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
