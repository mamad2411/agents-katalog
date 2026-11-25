---
name: declaw-sandbox
description: Guide for creating and managing Declaw sandboxes using ComputeSDK. Use when building applications that need Declaw provider for ComputeSDK - secure sandboxes with PII scanning, prompt-injection defense, and network egress filtering.
---

# Declaw Sandboxes with ComputeSDK

Declaw provider for ComputeSDK - secure sandboxes with PII scanning, prompt-injection defense, and network egress filtering.

## Setup

```bash
npm install computesdk @computesdk/declaw
```

Set your credentials:

```bash
# .env
DECLAW_API_KEY=your_declaw_api_key
DECLAW_DOMAIN=your_declaw_domain
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { declaw } from '@computesdk/declaw';

compute.setConfig({
  provider: declaw({
    apiKey: process.env.DECLAW_API_KEY,
    domain: process.env.DECLAW_DOMAIN,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Declaw!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { declaw } from '@computesdk/declaw';

const sdk = declaw({
    apiKey: process.env.DECLAW_API_KEY,
    domain: process.env.DECLAW_DOMAIN,
  });
const sandbox = await sdk.sandbox.create();
```

## Declaw Configuration

```typescript
interface DeclawConfig {

  /** Declaw API key. Falls back to `DECLAW_API_KEY` env var. */
  apiKey?: string;
  /** API domain, e.g. `api.declaw.ai`. Falls back to `DECLAW_DOMAIN` env var. */
  domain?: string;
  /** Default create-time timeout in milliseconds. */
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
