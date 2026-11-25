---
name: render-sandbox
description: Guide for creating and managing Render sandboxes using ComputeSDK. Use when building applications that need self-hosted sandbox environments on Render's cloud platform for code execution with zero infrastructure setup.
---

# Render Sandboxes with ComputeSDK

Self-host sandbox environments on Render's cloud platform through ComputeSDK's unified API. Render provides a unified cloud platform with zero infrastructure setup — ideal for self-hosted sandbox environments where you want full control over your compute.

## Setup

```bash
npm install computesdk
```

```bash
# .env
COMPUTESDK_API_KEY=your_computesdk_api_key
RENDER_API_KEY=your_render_api_key
RENDER_OWNER_ID=your_render_owner_id
```

Get your ComputeSDK key at https://console.computesdk.com/register

## Quick Start

```typescript
import { compute } from 'computesdk';
// Auto-detects Render from environment variables

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCode('print("Hello from Render!")');
console.log(result.output);

await sandbox.destroy();
```

## Explicit Configuration

For multi-provider setups or when you want to be explicit:

```typescript
import { compute } from 'computesdk';

compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'render',
  render: {
    apiKey: process.env.RENDER_API_KEY,
    ownerId: process.env.RENDER_OWNER_ID,
  }
});

const sandbox = await compute.sandbox.create();
```

## Render Configuration Options

```typescript
interface RenderConfig {
  apiKey?: string;     // Uses RENDER_API_KEY env var if not set
  ownerId?: string;    // Uses RENDER_OWNER_ID env var if not set
}
```

## Full API

ComputeSDK provides the same API across all providers: filesystem operations, shell commands, managed servers, overlays, terminals, and client access.

Install the main skill for the complete reference:

```
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/