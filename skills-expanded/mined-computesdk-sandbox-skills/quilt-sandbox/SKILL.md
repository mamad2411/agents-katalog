---
name: quilt-sandbox
description: Guide for creating and managing Quilt sandboxes using ComputeSDK. Use when building applications that need Quilt provider for ComputeSDK - tenant-scoped Linux sandboxes with exec, published services, and snapshots.
---

# Quilt Sandboxes with ComputeSDK

Quilt provider for ComputeSDK - tenant-scoped Linux sandboxes with exec, published services, and snapshots.

## Setup

```bash
npm install computesdk @computesdk/quilt
```

No API credentials are required by default for this provider. Configure any optional settings in the config object below.

## Quick Start

```typescript
import { compute } from 'computesdk';
import { quilt } from '@computesdk/quilt';

compute.setConfig({
  provider: quilt({
    // baseUrl: "your_baseUrl",
    // apiKey: "your_apiKey",
    // accessToken: "your_accessToken",
    // tenantId: "your_tenantId",
    // image: "your_image",
    // timeout: <number>,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Quilt!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { quilt } from '@computesdk/quilt';

const sdk = quilt({
    // baseUrl: "your_baseUrl",
    // apiKey: "your_apiKey",
    // accessToken: "your_accessToken",
    // tenantId: "your_tenantId",
    // image: "your_image",
    // timeout: <number>,
  });
const sandbox = await sdk.sandbox.create();
```

## Quilt Configuration

```typescript
interface QuiltConfig {

  baseUrl?: string;
  apiKey?: string;
  accessToken?: string;
  tenantId?: string;
  image?: string;
  timeout?: number;
  publishedServiceAuthMode?: QuiltServiceAuthMode;
  publishedServiceTtlSecs?: number;
  pollIntervalMs?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
