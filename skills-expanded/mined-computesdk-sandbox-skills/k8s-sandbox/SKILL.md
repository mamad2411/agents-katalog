---
name: k8s-sandbox
description: Guide for creating and managing Kubernetes sandboxes using ComputeSDK. Use when building applications that need Kubernetes provider for ComputeSDK - run sandboxes as pods.
---

# Kubernetes Sandboxes with ComputeSDK

Kubernetes provider for ComputeSDK - run sandboxes as pods.

## Setup

```bash
npm install computesdk @computesdk/k8s
```

No API credentials are required by default for this provider. Configure any optional settings in the config object below.

## Quick Start

```typescript
import { compute } from 'computesdk';
import { k8s } from '@computesdk/k8s';

compute.setConfig({
  provider: k8s({
    // kubeConfigPath: "your_kubeConfigPath",
    // kubeConfigRaw: "your_kubeConfigRaw",
    // context: "your_context",
    // namespace: "your_namespace",
    // image: "your_image",
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Kubernetes!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { k8s } from '@computesdk/k8s';

const sdk = k8s({
    // kubeConfigPath: "your_kubeConfigPath",
    // kubeConfigRaw: "your_kubeConfigRaw",
    // context: "your_context",
    // namespace: "your_namespace",
    // image: "your_image",
  });
const sandbox = await sdk.sandbox.create();
```

## Kubernetes Configuration

```typescript
interface K8sConfig {

  kubeConfigPath?: string;
  kubeConfigRaw?: string;
  context?: string;
  namespace?: string;
  image?: string;
  runtime?: Runtime;
  timeout?: number;
  podNamePrefix?: string;
  urlTemplate?: string;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
