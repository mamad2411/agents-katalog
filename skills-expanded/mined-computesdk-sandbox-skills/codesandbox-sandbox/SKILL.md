---
name: codesandbox-sandbox
description: Guide for creating and managing CodeSandbox sandboxes using ComputeSDK. Use when building applications that need CodeSandbox provider for ComputeSDK - fast browser-compatible sandboxes with npm and Python support.
---

# CodeSandbox Sandboxes with ComputeSDK

CodeSandbox provider for ComputeSDK - fast browser-compatible sandboxes with npm and Python support.

## Setup

```bash
npm install computesdk @computesdk/codesandbox
```

Set your credentials:

```bash
# .env
CSB_API_KEY=your_csb_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { codesandbox } from '@computesdk/codesandbox';

compute.setConfig({
  provider: codesandbox({
    apiKey: process.env.CSB_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from CodeSandbox!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { codesandbox } from '@computesdk/codesandbox';

const sdk = codesandbox({
    apiKey: process.env.CSB_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## CodeSandbox Configuration

```typescript
interface CodesandboxConfig {

  /** CodeSandbox API key - if not provided, will fallback to CSB_API_KEY environment variable */
  apiKey?: string;
  /** Template to use for new sandboxes */
  templateId?: string;
  /** Default runtime environment (e.g. 'node', 'python') */
  runtime?: string;
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
