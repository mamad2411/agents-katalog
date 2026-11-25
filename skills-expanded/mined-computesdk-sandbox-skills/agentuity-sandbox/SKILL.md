---
name: agentuity-sandbox
description: Guide for creating and managing Agentuity sandboxes using ComputeSDK. Use when building applications that need Agentuity provider for ComputeSDK - isolated cloud sandboxes with native filesystem, snapshot/checkpoint support, and flexible runtimes.
---

# Agentuity Sandboxes with ComputeSDK

Agentuity provider for ComputeSDK - isolated cloud sandboxes with native filesystem, snapshot/checkpoint support, and flexible runtimes.

## Setup

```bash
npm install computesdk @computesdk/agentuity
```

Set your credentials:

```bash
# .env
AGENTUITY_CATALYST_URL=your_agentuity_catalyst_url
AGENTUITY_REGION=your_agentuity_region
AGENTUITY_SANDBOX_URL=your_agentuity_sandbox_url
AGENTUITY_SDK_KEY=your_agentuity_sdk_key
AGENTUITY_TRANSPORT_URL=your_agentuity_transport_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { agentuity } from '@computesdk/agentuity';

compute.setConfig({
  provider: agentuity({
    apiKey: process.env.AGENTUITY_SDK_KEY,
    region: process.env.AGENTUITY_REGION,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Agentuity!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { agentuity } from '@computesdk/agentuity';

const sdk = agentuity({
    apiKey: process.env.AGENTUITY_SDK_KEY,
    region: process.env.AGENTUITY_REGION,
  });
const sandbox = await sdk.sandbox.create();
```

## Agentuity Configuration

```typescript
interface AgentuityConfig {

    /** Agentuity SDK key — falls back to AGENTUITY_SDK_KEY env var */
    apiKey?: string;
    /**
     * Region for API endpoints.
     * - "local"  → https://catalyst.agentuity.io
     * - "usc"    → https://catalyst-usc.agentuity.cloud  (default)
     * - or a full custom base URL
     */
    region?: string;
    /** Override the sandbox base URL entirely */
    baseURL?: string;
    /** Default runtime, e.g. "bun:1", "python:3.14", "node:22" */
    runtime?: string;
    /** Idle timeout passed to the sandbox (e.g. "5m", "1h") */
    idleTimeout?: string;
    /** Execution timeout passed to the sandbox (e.g. "30m", "2h") */
    executionTimeout?: string;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
