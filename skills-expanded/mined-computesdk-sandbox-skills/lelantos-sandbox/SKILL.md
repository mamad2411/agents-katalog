---
name: lelantos-sandbox
description: Guide for creating and managing Lelantos sandboxes using ComputeSDK. Use when building applications that need Lelantos provider for ComputeSDK - EU-native Firecracker microVM sandboxes (E2B-API-compatible) with full Linux environments, filesystem access, and per-port preview URLs.
---

# Lelantos Sandboxes with ComputeSDK

Lelantos provider for ComputeSDK - EU-native Firecracker microVM sandboxes (E2B-API-compatible) with full Linux environments, filesystem access, and per-port preview URLs.

## Setup

```bash
npm install computesdk @computesdk/lelantos
```

Set your credentials:

```bash
# .env
E2B_API_KEY=your_e2b_api_key
E2B_API_URL=your_e2b_api_url
E2B_DOMAIN=your_e2b_domain
LELANTOS_API_KEY=your_lelantos_api_key
LELANTOS_API_URL=your_lelantos_api_url
LELANTOS_DOMAIN=your_lelantos_domain
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { lelantos } from '@computesdk/lelantos';

compute.setConfig({
  provider: lelantos({
    apiKey: process.env.LELANTOS_API_KEY,
    apiUrl: process.env.LELANTOS_API_URL,
    domain: process.env.LELANTOS_DOMAIN,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Lelantos!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { lelantos } from '@computesdk/lelantos';

const sdk = lelantos({
    apiKey: process.env.LELANTOS_API_KEY,
    apiUrl: process.env.LELANTOS_API_URL,
    domain: process.env.LELANTOS_DOMAIN,
  });
const sandbox = await sdk.sandbox.create();
```

## Lelantos Configuration

```typescript
interface LelantosConfig {

  /**
   * Lelantos API key. Accepts the `lel_…` form OR the `e2b_…` form of a
   * lelantos key (a native `lel_<hex>` key is transparently presented to the
   * e2b SDK as its `e2b_<hex>` alias). If not provided, falls back to the
   * `LELANTOS_API_KEY` environment variable, then `E2B_API_KEY`.
   */
  apiKey?: string;
  /**
   * Lelantos control-plane + sandbox domain, e.g. `'lelantos.ai'`. The e2b SDK
   * derives the control-plane URL as `https://api.${domain}` and the sandbox
   * preview host as `{port}-{sandboxId}.${domain}`. If not provided, falls back
   * to the `LELANTOS_DOMAIN` then `E2B_DOMAIN` environment variable, then
   * defaults to `'lelantos.ai'`.
   */
  domain?: string;
  /**
   * Explicit control-plane URL override (e.g. a non-`api.` host or a port).
   * Takes precedence over `domain`-derived URLs for control-plane calls. Falls
   * back to `LELANTOS_API_URL` then `E2B_API_URL`.
   */
  apiUrl?: string;
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
