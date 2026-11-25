---
name: sail-sandbox
description: Guide for creating and managing Sail sandboxes using ComputeSDK. Use when building applications that need Sail provider for ComputeSDK - fast, isolated microVM sandboxes with native filesystem access.
---

# Sail Sandboxes with ComputeSDK

Sail provider for ComputeSDK - fast, isolated microVM sandboxes with native filesystem access.

## Setup

```bash
npm install computesdk @computesdk/sail
```

Set your credentials:

```bash
# .env
SAIL_API_KEY=your_sail_api_key
SAIL_APP=your_sail_app
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { sail } from '@computesdk/sail';

compute.setConfig({
  provider: sail({
    apiKey: process.env.SAIL_API_KEY,
    app: process.env.SAIL_APP,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Sail!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { sail } from '@computesdk/sail';

const sdk = sail({
    apiKey: process.env.SAIL_API_KEY,
    app: process.env.SAIL_APP,
  });
const sandbox = await sdk.sandbox.create();
```

## Sail Configuration

```typescript
interface SailConfig {

  /** Sail API key. Falls back to `SAIL_API_KEY`. */
  apiKey?: string;
  /** App that owns created Sailboxes. Falls back to `SAIL_APP`, then `computesdk`. */
  app?: string;
  /** Image used by created Sailboxes. Defaults to Sail's ARM64 Devbox builtin. */
  image?: ImageSpec | Image;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
