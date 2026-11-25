---
name: arker-sandbox
description: Guide for creating and managing Arker sandboxes using ComputeSDK. Use when building applications that need Arker provider for ComputeSDK - sandboxed VMs with persistent filesystems, forked from golden images.
---

# Arker Sandboxes with ComputeSDK

Arker provider for ComputeSDK - sandboxed VMs with persistent filesystems, forked from golden images.

## Setup

```bash
npm install computesdk @computesdk/arker
```

Set your credentials:

```bash
# .env
ARKER_API_KEY=your_arker_api_key
ARKER_PLATFORMS=your_arker_platforms
ARKER_REGION=your_arker_region
ARKER_SOURCE=your_arker_source
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { arker } from '@computesdk/arker';

compute.setConfig({
  provider: arker({
    apiKey: process.env.ARKER_API_KEY,
    platforms: process.env.ARKER_PLATFORMS?.split(',').filter(Boolean),
    region: process.env.ARKER_REGION,
    source: process.env.ARKER_SOURCE,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Arker!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { arker } from '@computesdk/arker';

const sdk = arker({
    apiKey: process.env.ARKER_API_KEY,
    platforms: process.env.ARKER_PLATFORMS?.split(',').filter(Boolean),
    region: process.env.ARKER_REGION,
    source: process.env.ARKER_SOURCE,
  });
const sandbox = await sdk.sandbox.create();
```

## Arker Configuration

```typescript
interface ArkerConfig {

  /** Arker API key (starts with `ark_`). Falls back to the ARKER_API_KEY environment variable. */
  apiKey?: string;
  /** Region, e.g. `aws-us-east-1`. Falls back to ARKER_REGION, then the us-east-1 default. */
  region?: string;
  /** Golden source VM to fork on create(). Falls back to ARKER_SOURCE, then `ubuntu-small`. */
  source?: string;
  /** Compute platforms to fork onto, e.g. `['graviton4']`. Falls back to ARKER_PLATFORMS (comma-separated). */
  platforms?: string[];

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
