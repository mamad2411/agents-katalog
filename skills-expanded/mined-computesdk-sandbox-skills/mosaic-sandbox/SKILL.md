---
name: mosaic-sandbox
description: Guide for creating and managing Mosaic sandboxes using ComputeSDK. Use when building applications that need Mosaic provider for ComputeSDK - Firecracker-based sandbox environments.
---

# Mosaic Sandboxes with ComputeSDK

Mosaic provider for ComputeSDK - Firecracker-based sandbox environments.

## Setup

```bash
npm install computesdk @computesdk/mosaic
```

Set your credentials:

```bash
# .env
MOSAIC_API_TOKEN=your_mosaic_api_token
MOSAIC_API_URL=your_mosaic_api_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { mosaic } from '@computesdk/mosaic';

compute.setConfig({
  provider: mosaic({
    apiKey: process.env.MOSAIC_API_TOKEN,
    baseUrl: process.env.MOSAIC_API_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Mosaic!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { mosaic } from '@computesdk/mosaic';

const sdk = mosaic({
    apiKey: process.env.MOSAIC_API_TOKEN,
    baseUrl: process.env.MOSAIC_API_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## Mosaic Configuration

```typescript
interface MosaicConfig {

  /** Public or private Mosaic REST endpoint. Falls back to MOSAIC_API_URL. */
  baseUrl?: string;
  /** Bearer token. Falls back to MOSAIC_API_TOKEN. */
  apiKey?: string;
  /** Default template. */
  template?: string;
  /** Default memory allocation in MiB. */
  memoryMb?: number;
  /** Default vCPU allocation. */
  vcpu?: number;
  /** HTTP request timeout. */
  requestTimeoutMs?: number;
  /**
   * How many HTTP requests this client keeps in flight before it starts
   * queueing. `fetch` opens a connection per in-flight request, so an
   * unbounded client answers a burst of sandbox creates with a burst of TLS
   * handshakes. Defaults to 32; Infinity restores the unbounded behaviour.
   */
  maxConcurrentRequests?: number;
  /** Give sandboxes egress. On by default; installs and fetches need it. */
  networkEnabled?: boolean;
  /** How long a preview URL from getUrl stays valid. */
  previewExpiresInSeconds?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
