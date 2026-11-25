---
name: isorun-sandbox
description: Guide for creating and managing Isorun sandboxes using ComputeSDK. Use when building applications that need Isorun provider for ComputeSDK — isolated Linux VM sandboxes for running untrusted and AI-generated code.
---

# Isorun Sandboxes with ComputeSDK

Isorun provider for ComputeSDK — isolated Linux VM sandboxes for running untrusted and AI-generated code.

## Setup

```bash
npm install computesdk @computesdk/isorun
```

Set your credentials:

```bash
# .env
ISORUN_API_KEY=your_isorun_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { isorun } from '@computesdk/isorun';

compute.setConfig({
  provider: isorun({
    apiKey: process.env.ISORUN_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Isorun!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { isorun } from '@computesdk/isorun';

const sdk = isorun({
    apiKey: process.env.ISORUN_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## Isorun Configuration

```typescript
interface IsorunConfig {

  /** API key. Falls back to `ISORUN_API_KEY` env var. The runner endpoint is derived from the key. */
  apiKey?: string

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
