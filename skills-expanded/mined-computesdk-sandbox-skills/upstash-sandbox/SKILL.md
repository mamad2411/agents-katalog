---
name: upstash-sandbox
description: Guide for creating and managing Upstash Box sandboxes using ComputeSDK. Use when building applications that need Upstash Box provider for ComputeSDK - cloud sandboxes with code execution, filesystem access, and AI agent support.
---

# Upstash Box Sandboxes with ComputeSDK

Upstash Box provider for ComputeSDK - cloud sandboxes with code execution, filesystem access, and AI agent support.

## Setup

```bash
npm install computesdk @computesdk/upstash
```

Set your credentials:

```bash
# .env
UPSTASH_BOX_API_KEY=your_upstash_box_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { upstash } from '@computesdk/upstash';

compute.setConfig({
  provider: upstash({
    apiKey: process.env.UPSTASH_BOX_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Upstash Box!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { upstash } from '@computesdk/upstash';

const sdk = upstash({
    apiKey: process.env.UPSTASH_BOX_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## Upstash Box Configuration

```typescript
interface UpstashConfig {

  /** Upstash Box API key - if not provided, will fallback to UPSTASH_BOX_API_KEY environment variable */
  apiKey?: string;
  /** Default runtime environment (e.g. 'node', 'python') */
  runtime?: string;
  /** Execution timeout in milliseconds (default: 600000) */
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
