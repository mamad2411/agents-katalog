---
name: leap0-sandbox
description: Guide for creating and managing Leap0 sandboxes using ComputeSDK. Use when building applications that need Leap0 provider for ComputeSDK - cloud sandboxed environments for AI agents.
---

# Leap0 Sandboxes with ComputeSDK

Leap0 provider for ComputeSDK - cloud sandboxed environments for AI agents.

## Setup

```bash
npm install computesdk @computesdk/leap0
```

Set your credentials:

```bash
# .env
LEAP0_API_KEY=your_leap0_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { leap0 } from '@computesdk/leap0';

compute.setConfig({
  provider: leap0({
    apiKey: process.env.LEAP0_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Leap0!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { leap0 } from '@computesdk/leap0';

const sdk = leap0({
    apiKey: process.env.LEAP0_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## Leap0 Configuration

```typescript
interface Leap0Config {

  /** Leap0 API key - if not provided, will use LEAP0_API_KEY environment variable */
  apiKey?: string;
  /** Base URL for the Leap0 API (default: https://api.leap0.dev) */
  baseUrl?: string;
  /** Sandbox domain for URL generation (default: sandbox.leap0.dev) */
  sandboxDomain?: string;
  /** Client timeout in seconds */
  timeout?: number;
  /** Default template name to use when creating sandboxes (e.g. 'system/debian:bookworm') */
  template?: string;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
