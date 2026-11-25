---
name: blaxel-sandbox
description: Guide for creating and managing Blaxel sandboxes using ComputeSDK. Use when building applications that need Blaxel provider for ComputeSDK - lightweight cloud sandboxes for code execution.
---

# Blaxel Sandboxes with ComputeSDK

Blaxel provider for ComputeSDK - lightweight cloud sandboxes for code execution.

## Setup

```bash
npm install computesdk @computesdk/blaxel
```

Set your credentials:

```bash
# .env
BL_API_KEY=your_bl_api_key
BL_WORKSPACE=your_bl_workspace
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { blaxel } from '@computesdk/blaxel';

compute.setConfig({
  provider: blaxel({
    apiKey: process.env.BL_API_KEY,
    workspace: process.env.BL_WORKSPACE,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Blaxel!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { blaxel } from '@computesdk/blaxel';

const sdk = blaxel({
    apiKey: process.env.BL_API_KEY,
    workspace: process.env.BL_WORKSPACE,
  });
const sandbox = await sdk.sandbox.create();
```

## Blaxel Configuration

```typescript
interface BlaxelConfig {

	/** Blaxel workspace ID - if not provided, will fallback to BL_WORKSPACE environment variable */
	workspace?: string;
	/** Blaxel API key - if not provided, will fallback to BL_API_KEY environment variable */
	apiKey?: string;
	/** Default image for sandboxes */
	image?: string;
	/** Default region for sandbox deployment */
	region?: string;
	/** Default memory allocation in MB */
	memory?: number | 4096;
	/** Default ports for sandbox */
	ports?: number[] | [3000];

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
