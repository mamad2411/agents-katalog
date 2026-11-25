---
name: sprites-sandbox
description: Guide for creating and managing Sprites sandboxes using ComputeSDK. Use when building applications that need Sprites provider for ComputeSDK - cloud sandboxes powered by Sprites.
---

# Sprites Sandboxes with ComputeSDK

Sprites provider for ComputeSDK - cloud sandboxes powered by Sprites.

## Setup

```bash
npm install computesdk @computesdk/sprites
```

Set your credentials:

```bash
# .env
SPRITES_TOKEN=your_sprites_token
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { sprites } from '@computesdk/sprites';

compute.setConfig({
  provider: sprites({
    apiKey: process.env.SPRITES_TOKEN,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Sprites!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { sprites } from '@computesdk/sprites';

const sdk = sprites({
    apiKey: process.env.SPRITES_TOKEN,
  });
const sandbox = await sdk.sandbox.create();
```

## Sprites Configuration

```typescript
interface SpritesConfig {

  /** Sprites API token - if not provided, will fallback to SPRITES_TOKEN environment variable */
  apiKey?: string;
  /** Base URL for the Sprites API */
  baseUrl?: string;
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
