---
name: hopx-sandbox
description: Guide for creating and managing HopX sandboxes using ComputeSDK. Use when building applications that need HopX provider for ComputeSDK - cloud sandboxes with full Linux environments, filesystem access, and microVM isolation.
---

# HopX Sandboxes with ComputeSDK

HopX provider for ComputeSDK - cloud sandboxes with full Linux environments, filesystem access, and microVM isolation.

## Setup

```bash
npm install computesdk @computesdk/hopx
```

Set your credentials:

```bash
# .env
HOPX_API_KEY=your_hopx_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { hopx } from '@computesdk/hopx';

compute.setConfig({
  provider: hopx({
    apiKey: process.env.HOPX_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from HopX!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { hopx } from '@computesdk/hopx';

const sdk = hopx({
    apiKey: process.env.HOPX_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## HopX Configuration

```typescript
interface HopxConfig {

  /** HopX API key - if not provided, will fallback to HOPX_API_KEY environment variable */
  apiKey?: string;
  /** Execution timeout in milliseconds */
  timeout?: number;
  /** Template name for sandbox creation (e.g., 'code-interpreter') */
  template?: string;
  /** Base API URL for custom/staging environments */
  baseURL?: string;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
