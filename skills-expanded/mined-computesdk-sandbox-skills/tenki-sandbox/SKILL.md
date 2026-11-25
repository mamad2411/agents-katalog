---
name: tenki-sandbox
description: Guide for creating and managing Tenki Cloud sandboxes using ComputeSDK. Use when building applications that need Tenki Cloud provider for ComputeSDK - microVM sandboxes with native filesystem, preview URLs, snapshots, and SSH.
---

# Tenki Cloud Sandboxes with ComputeSDK

Tenki Cloud provider for ComputeSDK - microVM sandboxes with native filesystem, preview URLs, snapshots, and SSH.

## Setup

```bash
npm install computesdk @computesdk/tenki
```

Set your credentials:

```bash
# .env
TENKI_API_KEY=your_tenki_api_key
TENKI_API_URL=your_tenki_api_url
TENKI_AUTH_TOKEN=your_tenki_auth_token
TENKI_WORKSPACE_ID=your_tenki_workspace_id
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { tenki } from '@computesdk/tenki';

compute.setConfig({
  provider: tenki({
    apiKey: process.env.TENKI_API_KEY,
    baseUrl: process.env.TENKI_API_URL,
    workspaceId: process.env.TENKI_WORKSPACE_ID,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Tenki Cloud!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { tenki } from '@computesdk/tenki';

const sdk = tenki({
    apiKey: process.env.TENKI_API_KEY,
    baseUrl: process.env.TENKI_API_URL,
    workspaceId: process.env.TENKI_WORKSPACE_ID,
  });
const sandbox = await sdk.sandbox.create();
```

## Tenki Cloud Configuration

```typescript
interface TenkiConfig {

  /** Tenki API key (tk_...). Falls back to TENKI_API_KEY / TENKI_AUTH_TOKEN env vars. */
  apiKey?: string;
  /** API base URL. Falls back to TENKI_API_URL, then https://api.tenki.cloud. */
  baseUrl?: string;
  /** Workspace to create sandboxes in. Falls back to TENKI_WORKSPACE_ID; workspace API keys infer it server-side. */
  workspaceId?: string;
  /** @deprecated Tenki no longer scopes sandboxes by project. */
  projectId?: string;
  /** Default runCommand timeout in milliseconds. */
  timeout?: number;
  /** Default sandbox resources applied at create() time. */
  cpuCores?: number;
  memoryMb?: number;
  diskSizeGb?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
