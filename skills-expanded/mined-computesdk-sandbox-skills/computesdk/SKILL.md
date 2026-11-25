---
name: computesdk
description: Guide for building sandbox applications with ComputeSDK, a unified TypeScript SDK for running untrusted code in sandboxed environments across 42 compute providers. Use this skill when implementing sandboxed code execution, isolated development environments, running LLM-generated code safely, or integrating dynamic code execution into applications.
---

# ComputeSDK

A unified TypeScript SDK for running code in remote sandboxes. Write code once, switch providers by changing environment variables or the provider config. Supports 42 sandbox providers.

## Installation

```bash
npm install computesdk
```

You will also need the provider package(s) you intend to use, e.g.:

```bash
npm install @computesdk/e2b
```

> **No ComputeSDK API key is required.** ComputeSDK itself does not have its own API key. Each sandbox provider needs its own credentials; the examples below read them from environment variables.

## Hosted platform (no provider keys)

Sandboxes can also run on ComputeSDK's hosted platform ([platform.computesdk.com](https://platform.computesdk.com)) instead of your own provider accounts — the platform places each sandbox on your org's registered providers or a compute-market fill, bills the org, and exposes everything over REST, the `compute` CLI, or the `@computesdk/platform` provider, authenticated with an org API key in `COMPUTE_API_KEY` (or `compute login`).

From code, use the `platform` provider — same `compute` interface as every other provider:

```bash
npm install computesdk @computesdk/platform
```

```typescript
import { compute } from 'computesdk';
import { platform } from '@computesdk/platform';

compute.setConfig({
  provider: platform({ apiKey: process.env.COMPUTE_API_KEY }),
});

const sandbox = await compute.sandbox.create({ size: 'small' });
const result = await sandbox.runCommand('echo hello');
await sandbox.destroy();
```

Placement and pricing options (`size`, `providerOrder`, `orderType`, `maxPrice`) go on the create call or the provider's `defaults`. From a shell, see the `compute-sandboxes-cli` skill (`compute sandboxes`), and the `compute-actions-cli` skill for the Actions CI engine (`compute actions`).

## Quick Start

```typescript
import { compute } from 'computesdk';
import { e2b } from '@computesdk/e2b';

compute.setConfig({
  provider: e2b({ apiKey: process.env.E2B_API_KEY }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello World!"');
console.log(result.stdout);

await sandbox.destroy();
```

## Multi-Provider Setup

Use multiple providers for resilience or to route workloads to the best backend:

```typescript
import { compute } from 'computesdk';
import { e2b } from '@computesdk/e2b';
import { modal } from '@computesdk/modal';

compute.setConfig({
  providers: [
    e2b({ apiKey: process.env.E2B_API_KEY }),
    modal({
      tokenId: process.env.MODAL_TOKEN_ID,
      tokenSecret: process.env.MODAL_TOKEN_SECRET,
    }),
  ],
  providerStrategy: 'priority', // or 'round-robin'
  fallbackOnError: true,
});

// Creates a sandbox using the first provider that succeeds
const sandbox = await compute.sandbox.create();
```

Pick a specific provider at creation time:

```typescript
const sandbox = await compute.sandbox.create({ provider: 'modal' });
```

## Sandbox Lifecycle

```typescript
const sandbox = await compute.sandbox.create({
  timeout: 300000,
  metadata: { userId: '123' },
});

const existing = await compute.sandbox.getById('sandbox-id');
const all = await compute.sandbox.list();
await compute.sandbox.destroy(sandbox.sandboxId);
```

## Command Execution

```typescript
const result = await sandbox.runCommand('ls -la');
// result.stdout, result.stderr, result.exitCode, result.durationMs

const bg = await sandbox.runCommand('npm run dev', { background: true });

const withOpts = await sandbox.runCommand('npm install', {
  cwd: '/app',
  env: { NODE_ENV: 'production' },
  timeout: 60000,
  onStdout: (chunk) => console.log(chunk),
});
```

## Filesystem

```typescript
await sandbox.filesystem.writeFile('/app/index.js', 'console.log("hi")');
const content = await sandbox.filesystem.readFile('/app/index.js');
await sandbox.filesystem.mkdir('/app/data');
const files = await sandbox.filesystem.readdir('/app');
const exists = await sandbox.filesystem.exists('/app/index.js');
await sandbox.filesystem.remove('/app/index.js');
```

## Sandbox Info & Networking

```typescript
const info = await sandbox.getInfo();
// info.id, info.provider, info.status, info.createdAt, info.timeout, info.metadata

const url = await sandbox.getUrl({ port: 3000, protocol: 'https' });
```

## Snapshots

```typescript
const snapshot = await compute.snapshot.create(sandbox.sandboxId, { name: 'baseline' });
const snapshots = await compute.snapshot.list();
await compute.snapshot.delete(snapshot.id);
```

## Platform & Provider-Specific Skills

Hosted-platform skills:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill compute-sandboxes-cli
npx skills add https://github.com/computesdk/sandbox-skills --skill compute-actions-cli
```

Provider-specific setup guides:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill agentcore-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill agentuity-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill archil-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill arker-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill beam-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill blaxel-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill cloud-run-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill cloudflare-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill codesandbox-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill collimate-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill createos-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill daytona-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill declaw-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill docker-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill e2b-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill freestyle-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill hopx-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill isorun-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill just-bash-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill k8s-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill leap0-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill lelantos-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill lightning-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill modal-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill mosaic-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill namespace-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill neevcloud-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill northflank-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill opencomputer-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill quilt-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill railway-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill run-cloud-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill runloop-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill sail-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill sandbox0-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill secure-exec-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill sprites-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill superserve-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill tenki-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill tensorlake-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill upstash-sandbox
npx skills add https://github.com/computesdk/sandbox-skills --skill vercel-sandbox
```

Provider skill summaries:

- `agentcore-sandbox` — AWS Bedrock AgentCore Code Interpreter provider for ComputeSDK - secure, session-based code execution sandboxes
- `agentuity-sandbox` — Agentuity provider for ComputeSDK - isolated cloud sandboxes with native filesystem, snapshot/checkpoint support, and flexible runtimes
- `archil-sandbox` — Archil provider for ComputeSDK - exec commands against an Archil disk
- `arker-sandbox` — Arker provider for ComputeSDK - sandboxed VMs with persistent filesystems, forked from golden images
- `beam-sandbox` — Beam provider for ComputeSDK - containerized sandbox environments with process management and filesystem access
- `blaxel-sandbox` — Blaxel provider for ComputeSDK - lightweight cloud sandboxes for code execution
- `cloud-run-sandbox` — Google Cloud Run Sandboxes provider for ComputeSDK
- `cloudflare-sandbox` — Cloudflare provider for ComputeSDK - edge code execution using Cloudflare Workers and Durable Objects
- `codesandbox-sandbox` — CodeSandbox provider for ComputeSDK - fast browser-compatible sandboxes with npm and Python support
- `collimate-sandbox` — Collimate provider for ComputeSDK
- `createos-sandbox` — CreateOS provider for ComputeSDK — NodeOps VM sandboxes with pause/resume/fork snapshots
- `daytona-sandbox` — Daytona provider for ComputeSDK - standardized development environments with devcontainer support
- `declaw-sandbox` — Declaw provider for ComputeSDK - secure sandboxes with PII scanning, prompt-injection defense, and network egress filtering
- `docker-sandbox` — Docker provider for ComputeSDK - local containerized sandboxes for development and testing
- `e2b-sandbox` — E2B provider for ComputeSDK - cloud sandboxes with full Linux environments, filesystem access, and microVM isolation
- `freestyle-sandbox` — Freestyle provider for ComputeSDK - cloud sandboxes powered by Freestyle
- `hopx-sandbox` — HopX provider for ComputeSDK - cloud sandboxes with full Linux environments, filesystem access, and microVM isolation
- `isorun-sandbox` — Isorun provider for ComputeSDK — isolated Linux VM sandboxes for running untrusted and AI-generated code
- `just-bash-sandbox` — just-bash provider for ComputeSDK - local sandboxed bash execution with virtual filesystem
- `k8s-sandbox` — Kubernetes provider for ComputeSDK - run sandboxes as pods
- `leap0-sandbox` — Leap0 provider for ComputeSDK - cloud sandboxed environments for AI agents
- `lelantos-sandbox` — Lelantos provider for ComputeSDK - EU-native Firecracker microVM sandboxes (E2B-API-compatible) with full Linux environments, filesystem access, and per-port preview URLs
- `lightning-sandbox` — Lightning AI provider for ComputeSDK - cloud sandboxes for code execution, command running, and filesystem access
- `modal-sandbox` — Modal provider for ComputeSDK - serverless Python execution with GPU support and zero cold starts
- `mosaic-sandbox` — Mosaic provider for ComputeSDK - Firecracker-based sandbox environments
- `namespace-sandbox` — Namespace provider for ComputeSDK - cloud-native sandboxes with optional GPU support
- `neevcloud-sandbox` — NeevCloud provider for ComputeSDK - secure cloud sandboxes with command execution, filesystem access, and preview URLs
- `northflank-sandbox` — Northflank provider for ComputeSDK - Deploy and manage compute workloads on Northflank's container platform
- `opencomputer-sandbox` — OpenComputer provider for ComputeSDK - persistent cloud VMs with checkpoints, preview URLs, command execution, and filesystem access
- `quilt-sandbox` — Quilt provider for ComputeSDK - tenant-scoped Linux sandboxes with exec, published services, and snapshots
- `railway-sandbox` — Railway Sandboxes provider for ComputeSDK - run commands in Railway-hosted sandboxes
- `run-cloud-sandbox` — Run Cloud provider for ComputeSDK - fast Firecracker microVM sandboxes with snapshots and filesystem access
- `runloop-sandbox` — Runloop provider for ComputeSDK - AI-optimized code execution with built-in devtools and debugging
- `sail-sandbox` — Sail provider for ComputeSDK - fast, isolated microVM sandboxes with native filesystem access
- `sandbox0-sandbox` — Sandbox0 provider for ComputeSDK - fast persistent sandboxes with command execution and native filesystem access
- `secure-exec-sandbox` — Secure execution provider for ComputeSDK - isolated sandbox environments using secure-exec
- `sprites-sandbox` — Sprites provider for ComputeSDK - cloud sandboxes powered by Sprites
- `superserve-sandbox` — Superserve provides sandbox infrastructure to run code in isolated cloud environments powered by Firecracker MicroVMs
- `tenki-sandbox` — Tenki Cloud provider for ComputeSDK - microVM sandboxes with native filesystem, preview URLs, snapshots, and SSH
- `tensorlake-sandbox` — Tensorlake provider for ComputeSDK - stateful MicroVM sandboxes for agentic applications and LLM-generated code execution
- `upstash-sandbox` — Upstash Box provider for ComputeSDK - cloud sandboxes with code execution, filesystem access, and AI agent support
- `vercel-sandbox` — Vercel Sandbox provider for ComputeSDK - serverless code execution for Python and Node.js on Vercel's edge network

## TypeScript Types

```typescript
import type {
  SandboxInterface,
  SandboxInfo,
  CommandResult,
  CreateSandboxOptions,
  SandboxFileSystem,
} from 'computesdk';
```

## References

- Documentation: https://www.computesdk.com/docs/
- GitHub: https://github.com/computesdk/computesdk
- LLM-optimized docs: https://www.computesdk.com/llms-full.txt
