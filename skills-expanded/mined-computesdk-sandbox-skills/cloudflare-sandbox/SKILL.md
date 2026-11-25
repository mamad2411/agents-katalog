---
name: cloudflare-sandbox
description: Guide for creating and managing Cloudflare sandboxes using ComputeSDK. Use when building applications that need Cloudflare provider for ComputeSDK - edge code execution using Cloudflare Workers and Durable Objects.
---

# Cloudflare Sandboxes with ComputeSDK

Cloudflare provider for ComputeSDK - edge code execution using Cloudflare Workers and Durable Objects.

## Setup

```bash
npm install computesdk @computesdk/cloudflare
```

Set your credentials:

```bash
# .env
CLOUDFLARE_SANDBOX_API_KEY=your_cloudflare_sandbox_api_key
CLOUDFLARE_SANDBOX_URL=your_cloudflare_sandbox_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { cloudflare } from '@computesdk/cloudflare';

compute.setConfig({
  provider: cloudflare({
    sandboxApiKey: process.env.CLOUDFLARE_SANDBOX_API_KEY,
    sandboxUrl: process.env.CLOUDFLARE_SANDBOX_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Cloudflare!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { cloudflare } from '@computesdk/cloudflare';

const sdk = cloudflare({
    sandboxApiKey: process.env.CLOUDFLARE_SANDBOX_API_KEY,
    sandboxUrl: process.env.CLOUDFLARE_SANDBOX_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## Cloudflare Configuration

```typescript
interface CloudflareConfig {

  sandboxUrl?: string;
  sandboxApiKey?: string;
  /** @deprecated Use sandboxApiKey instead. */
  sandboxSecret?: string;
  sandboxBinding?: any;
  warmPool?: {
    binding: any;
    target?: number;
    refreshInterval?: number;
    poolName?: string;
  };
  timeout?: number;
  runtime?: string;
  envVars?: Record<string, string>;
  sandboxOptions?: {
    sleepAfter?: string | number;
    keepAlive?: boolean;
  };

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
