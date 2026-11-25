---
name: neevcloud-sandbox
description: Guide for creating and managing NeevCloud sandboxes using ComputeSDK. Use when building applications that need NeevCloud provider for ComputeSDK - secure cloud sandboxes with command execution, filesystem access, and preview URLs.
---

# NeevCloud Sandboxes with ComputeSDK

NeevCloud provider for ComputeSDK - secure cloud sandboxes with command execution, filesystem access, and preview URLs.

## Setup

```bash
npm install computesdk @computesdk/neevcloud
```

Set your credentials:

```bash
# .env
NEEV_API_KEY=your_neev_api_key
NEEV_ORG_ID=your_neev_org_id
NEEV_PROJECT_ID=your_neev_project_id
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { neevcloud } from '@computesdk/neevcloud';

compute.setConfig({
  provider: neevcloud({
    apiKey: process.env.NEEV_API_KEY,
    orgId: process.env.NEEV_ORG_ID,
    projectId: process.env.NEEV_PROJECT_ID,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from NeevCloud!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { neevcloud } from '@computesdk/neevcloud';

const sdk = neevcloud({
    apiKey: process.env.NEEV_API_KEY,
    orgId: process.env.NEEV_ORG_ID,
    projectId: process.env.NEEV_PROJECT_ID,
  });
const sandbox = await sdk.sandbox.create();
```

## NeevCloud Configuration

```typescript
interface NeevCloudConfig {

  /** NeevCloud API key. Read from NEEV_API_KEY when omitted. */
  apiKey?: string;
  /** Org the sandboxes belong to. Read from NEEV_ORG_ID when omitted. */
  orgId?: string;
  /** Project the sandboxes belong to. Read from NEEV_PROJECT_ID when omitted. */
  projectId?: string;
  /** Request timeout in milliseconds. */
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
