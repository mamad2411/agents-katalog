---
name: namespace-sandbox
description: Guide for creating and managing Namespace sandboxes using ComputeSDK. Use when building applications that need Namespace cloud container instances with customizable CPU/RAM resources for code execution or isolated development environments.
---

# Namespace Sandboxes with ComputeSDK

Run code on Namespace's cloud container instances through ComputeSDK's unified API. Namespace provides ephemeral containers with customizable CPU and memory allocation — ideal when you need control over compute resources, specific architectures, or lightweight isolated environments.

## Setup

```bash
npm install computesdk
```

```bash
# .env
COMPUTESDK_API_KEY=your_computesdk_api_key
NSC_TOKEN=your_namespace_nsc_token
```

Get your ComputeSDK key at https://console.computesdk.com/register

## Quick Start

```typescript
import { compute } from 'computesdk';
// Auto-detects Namespace from environment variables

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCode('print("Hello from Namespace!")');
console.log(result.output);

await sandbox.destroy();
```

## Explicit Configuration

For multi-provider setups or when you want to be explicit:

```typescript
import { compute } from 'computesdk';

compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'namespace',
  namespace: {
    token: process.env.NSC_TOKEN,
  }
});

const sandbox = await compute.sandbox.create();
```

## Custom Resources

Namespace lets you customize the compute resources for your sandboxes:

```typescript
compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'namespace',
  namespace: {
    token: process.env.NSC_TOKEN,
    virtualCpu: 4,
    memoryMegabytes: 8192,
  }
});
```

## Namespace Configuration Options

```typescript
interface NamespaceConfig {
  token?: string;              // Uses NSC_TOKEN env var if not set
  virtualCpu?: number;         // CPU cores (default: 2)
  memoryMegabytes?: number;    // RAM in MB (default: 4096)
  machineArch?: string;        // Architecture (default: 'amd64')
  os?: string;                 // Operating system (default: 'linux')
}
```

## Full API

ComputeSDK provides the same API across all providers: filesystem operations, shell commands, managed servers, overlays, terminals, and client access.

Install the main skill for the complete reference:

```
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/