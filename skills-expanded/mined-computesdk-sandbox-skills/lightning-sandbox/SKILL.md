---
name: lightning-sandbox
description: Guide for creating and managing Lightning AI sandboxes using ComputeSDK. Use when building applications that need Lightning AI provider for ComputeSDK - cloud sandboxes for code execution, command running, and filesystem access.
---

# Lightning AI Sandboxes with ComputeSDK

Lightning AI provider for ComputeSDK - cloud sandboxes for code execution, command running, and filesystem access.

## Setup

```bash
npm install computesdk @computesdk/lightning
```

Set your credentials:

```bash
# .env
LIGHTNING_API_KEY=your_lightning_api_key
LIGHTNING_CLOUD_URL=your_lightning_cloud_url
LIGHTNING_SANDBOX_API_KEY=your_lightning_sandbox_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { lightning } from '@computesdk/lightning';

compute.setConfig({
  provider: lightning({
    apiKey: process.env.LIGHTNING_SANDBOX_API_KEY,
    baseUrl: process.env.LIGHTNING_CLOUD_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Lightning AI!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { lightning } from '@computesdk/lightning';

const sdk = lightning({
    apiKey: process.env.LIGHTNING_SANDBOX_API_KEY,
    baseUrl: process.env.LIGHTNING_CLOUD_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## Lightning AI Configuration

```typescript
interface LightningConfig {

  /** Lightning AI API key - falls back to LIGHTNING_SANDBOX_API_KEY, then LIGHTNING_API_KEY env vars. */
  apiKey?: string;
  /** Lightning Cloud base URL - falls back to LIGHTNING_CLOUD_URL, then production. */
  baseUrl?: string;
  /** Instance type for new sandboxes (e.g. "cpu-1", "cpu-2", ... "cpu-16"). Defaults to "cpu-1". */
  instanceType?: string;
  /** Curated runtime image for new sandboxes (e.g. "node24", "python313"). */
  runtime?: string;
  /** Whether new sandboxes persist filesystem state across stops via auto-snapshots. */
  persistent?: boolean;
  /** Request spot capacity for new sandboxes. */
  spot?: boolean;
  /** Ports to expose on new sandboxes when none are supplied per-create. */
  ports?: number[];
  /** Maximum sandbox lifetime in milliseconds before auto-stop. */
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
