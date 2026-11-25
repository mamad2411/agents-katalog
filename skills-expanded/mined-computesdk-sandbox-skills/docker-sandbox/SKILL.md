---
name: docker-sandbox
description: Guide for creating and managing Docker sandboxes using ComputeSDK. Use when building applications that need Docker provider for ComputeSDK - local containerized sandboxes for development and testing.
---

# Docker Sandboxes with ComputeSDK

Docker provider for ComputeSDK - local containerized sandboxes for development and testing.

## Setup

```bash
npm install computesdk @computesdk/docker
```

Set your credentials:

```bash
# .env
DOCKER_HOST=your_docker_host
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { docker } from '@computesdk/docker';

compute.setConfig({
  provider: docker({
    image: { name: 'python:3.11-slim', pullPolicy: 'ifNotPresent' },
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Docker!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { docker } from '@computesdk/docker';

const sdk = docker({
    image: { name: 'python:3.11-slim', pullPolicy: 'ifNotPresent' },
  });
const sandbox = await sdk.sandbox.create();
```

## Docker Configuration

```typescript
interface DockerConfig {

  connection?: DockerConnection;
  /** Default image runtime identifier, e.g. 'python' or 'node' */
  runtime?: string;
  timeout?: number;
  image: DockerImage;
  container?: ContainerDefaults;
  createOptions?: ContainerCreateOptions;
  startOptions?: ContainerStartOptions;
  cleanup?: CleanupPolicy;
  streamLogs?: boolean;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
