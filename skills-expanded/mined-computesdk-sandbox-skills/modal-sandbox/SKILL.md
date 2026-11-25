---
name: modal-sandbox
description: Guide for creating and managing Modal sandboxes using ComputeSDK. Use when building applications that need Modal provider for ComputeSDK - serverless Python execution with GPU support and zero cold starts.
---

# Modal Sandboxes with ComputeSDK

Modal provider for ComputeSDK - serverless Python execution with GPU support and zero cold starts.

## Setup

```bash
npm install computesdk @computesdk/modal
```

Set your credentials:

```bash
# .env
MODAL_TOKEN_ID=your_modal_token_id
MODAL_TOKEN_SECRET=your_modal_token_secret
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { modal } from '@computesdk/modal';

compute.setConfig({
  provider: modal({
    tokenId: process.env.MODAL_TOKEN_ID,
    tokenSecret: process.env.MODAL_TOKEN_SECRET,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Modal!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { modal } from '@computesdk/modal';

const sdk = modal({
    tokenId: process.env.MODAL_TOKEN_ID,
    tokenSecret: process.env.MODAL_TOKEN_SECRET,
  });
const sandbox = await sdk.sandbox.create();
```

## Modal Configuration

```typescript
interface ModalConfig {

  tokenId?: string;
  tokenSecret?: string;
  timeout?: number;
  environment?: string;
  ports?: number[];
  daemonSsePort?: number | false;
  appName?: string;
  scalableSandboxes?: boolean;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
