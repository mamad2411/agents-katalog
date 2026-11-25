---
name: namespace-sandbox
description: Guide for creating and managing Namespace sandboxes using ComputeSDK. Use when building applications that need Namespace provider for ComputeSDK - cloud-native sandboxes with optional GPU support.
---

# Namespace Sandboxes with ComputeSDK

Namespace provider for ComputeSDK - cloud-native sandboxes with optional GPU support.

## Setup

```bash
npm install computesdk @computesdk/namespace
```

Set your credentials:

```bash
# .env
NSC_TOKEN=your_nsc_token
NSC_TOKEN_FILE=your_nsc_token_file
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { namespace } from '@computesdk/namespace';

compute.setConfig({
  provider: namespace({
    token: process.env.NSC_TOKEN,
    tokenFile: process.env.NSC_TOKEN_FILE,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Namespace!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { namespace } from '@computesdk/namespace';

const sdk = namespace({
    token: process.env.NSC_TOKEN,
    tokenFile: process.env.NSC_TOKEN_FILE,
  });
const sandbox = await sdk.sandbox.create();
```

## Namespace Configuration

```typescript
interface NamespaceConfig {

  /** Namespace API token - if not provided, will fallback to NSC_TOKEN environment variable */
  token?: string;
  /** Path to a JSON token file (e.g. from `nsc login`) containing bearer_token - fallback to NSC_TOKEN_FILE */
  tokenFile?: string;
  /** Virtual CPU cores for the instance */
  virtualCpu?: number;
  /** Memory in megabytes for the instance */
  memoryMegabytes?: number;
  /** Machine architecture (default: amd64) */
  machineArch?: string;
  /** Operating system (default: linux) */
  os?: string;
  /** Documented purpose for the instance */
  documentedPurpose?: string;
  /** Reason for destroying instances (default: "ComputeSDK cleanup") */
  destroyReason?: string;
  /** Target container name for command execution (default: "main-container") */
  targetContainerName?: string;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
