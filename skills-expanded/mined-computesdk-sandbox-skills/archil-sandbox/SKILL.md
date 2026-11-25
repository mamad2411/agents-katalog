---
name: archil-sandbox
description: Guide for creating and managing Archil sandboxes using ComputeSDK. Use when building applications that need Archil provider for ComputeSDK - exec commands against an Archil disk.
---

# Archil Sandboxes with ComputeSDK

Archil provider for ComputeSDK - exec commands against an Archil disk.

## Setup

```bash
npm install computesdk @computesdk/archil
```

Set your credentials:

```bash
# .env
ARCHIL_API_KEY=your_archil_api_key
ARCHIL_REGION=your_archil_region
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { archil } from '@computesdk/archil';

compute.setConfig({
  provider: archil({
    apiKey: process.env.ARCHIL_API_KEY,
    region: process.env.ARCHIL_REGION,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Archil!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { archil } from '@computesdk/archil';

const sdk = archil({
    apiKey: process.env.ARCHIL_API_KEY,
    region: process.env.ARCHIL_REGION,
  });
const sandbox = await sdk.sandbox.create();
```

## Archil Configuration

```typescript
interface ArchilConfig {

  /** Archil API key. Falls back to ARCHIL_API_KEY env var. */
  apiKey?: string;
  /** Archil region (e.g. "aws-us-east-1"). Falls back to ARCHIL_REGION env var. */
  region?: string;
  /** Override the control-plane base URL (useful for testing). */
  baseUrl?: string;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
