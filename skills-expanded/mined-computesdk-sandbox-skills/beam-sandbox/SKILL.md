---
name: beam-sandbox
description: Guide for creating and managing Beam sandboxes using ComputeSDK. Use when building applications that need Beam provider for ComputeSDK - containerized sandbox environments with process management and filesystem access.
---

# Beam Sandboxes with ComputeSDK

Beam provider for ComputeSDK - containerized sandbox environments with process management and filesystem access.

## Setup

```bash
npm install computesdk @computesdk/beam
```

Set your credentials:

```bash
# .env
BEAM_TOKEN=your_beam_token
BEAM_WORKSPACE_ID=your_beam_workspace_id
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { beam } from '@computesdk/beam';

compute.setConfig({
  provider: beam({
    token: process.env.BEAM_TOKEN,
    workspaceId: process.env.BEAM_WORKSPACE_ID,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Beam!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { beam } from '@computesdk/beam';

const sdk = beam({
    token: process.env.BEAM_TOKEN,
    workspaceId: process.env.BEAM_WORKSPACE_ID,
  });
const sandbox = await sdk.sandbox.create();
```

## Beam Configuration

```typescript
interface BeamConfig {

  token?: string;
  workspaceId?: string;
  gatewayUrl?: string;
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
