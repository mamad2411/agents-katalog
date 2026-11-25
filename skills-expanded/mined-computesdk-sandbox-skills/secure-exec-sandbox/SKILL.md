---
name: secure-exec-sandbox
description: Guide for creating and managing Secure Execution sandboxes using ComputeSDK. Use when building applications that need Secure execution provider for ComputeSDK - isolated sandbox environments using secure-exec.
---

# Secure Execution Sandboxes with ComputeSDK

Secure execution provider for ComputeSDK - isolated sandbox environments using secure-exec.

## Setup

```bash
npm install computesdk @computesdk/secure-exec
```

No API credentials are required by default for this provider. Configure any optional settings in the config object below.

## Quick Start

```typescript
import { compute } from 'computesdk';
import { secureExec } from '@computesdk/secure-exec';

compute.setConfig({
  provider: secureExec({
    // memoryLimitMb: <number>,
    // cpuTimeLimitMs: <number>,
    // allowedCommands: "your_allowedCommands",
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Secure Execution!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { secureExec } from '@computesdk/secure-exec';

const sdk = secureExec({
    // memoryLimitMb: <number>,
    // cpuTimeLimitMs: <number>,
    // allowedCommands: "your_allowedCommands",
  });
const sandbox = await sdk.sandbox.create();
```

## Secure Execution Configuration

```typescript
interface SecureExecConfig {

  /** Memory cap for the V8 isolate in MB. Default: 128 */
  memoryLimitMb?: number;
  /** CPU time budget per exec call in ms. Default: 30_000 */
  cpuTimeLimitMs?: number;
  /** Allowlist of commands sandboxed code can spawn. Default: all allowed */
  allowedCommands?: string[];

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
