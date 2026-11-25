---
name: cloud-run-sandbox
description: Guide for creating and managing Google Cloud Run sandboxes using ComputeSDK. Use when building applications that need Google Cloud Run Sandboxes provider for ComputeSDK.
---

# Google Cloud Run Sandboxes with ComputeSDK

Google Cloud Run Sandboxes provider for ComputeSDK.

## Setup

```bash
npm install computesdk @computesdk/cloud-run
```

Set your credentials:

```bash
# .env
CLOUD_RUN_AUTH_TOKEN=your_cloud_run_auth_token
CLOUD_RUN_SANDBOX_BINARY=your_cloud_run_sandbox_binary
CLOUD_RUN_SANDBOX_SECRET=your_cloud_run_sandbox_secret
CLOUD_RUN_SANDBOX_URL=your_cloud_run_sandbox_url
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { cloudRun } from '@computesdk/cloud-run';

compute.setConfig({
  provider: cloudRun({
    gatewayAuthToken: process.env.CLOUD_RUN_AUTH_TOKEN,
    sandboxBinary: process.env.CLOUD_RUN_SANDBOX_BINARY,
    sandboxUrl: process.env.CLOUD_RUN_SANDBOX_URL,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Google Cloud Run!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { cloudRun } from '@computesdk/cloud-run';

const sdk = cloudRun({
    gatewayAuthToken: process.env.CLOUD_RUN_AUTH_TOKEN,
    sandboxBinary: process.env.CLOUD_RUN_SANDBOX_BINARY,
    sandboxUrl: process.env.CLOUD_RUN_SANDBOX_URL,
  });
const sandbox = await sdk.sandbox.create();
```

## Google Cloud Run Configuration

```typescript
interface CloudRunConfig {

  /** URL of the deployed Cloud Run gateway service for remote mode. */
  sandboxUrl?: string
  /** Shared bearer token for the deployed Cloud Run gateway service. */
  sandboxSecret?: string
  /** Optional Google-signed identity token for Cloud Run services that require IAM auth. */
  gatewayAuthToken?: string
  /** Execution mode. Ephemeral uses `sandbox do`; stateful uses `sandbox run`, `exec`, and `delete`. Defaults to ephemeral. */
  executionMode?: CloudRunExecutionMode
  /** Path to the Cloud Run sandbox binary. Defaults to CLOUD_RUN_SANDBOX_BINARY or /usr/local/gcp/bin/sandbox. */
  sandboxBinary?: string
  /** Sandbox CLI mode. Cloud Run's CLI defaults this to local. */
  mode?: 'local' | 'container'
  /** Allow network egress from sandboxed commands. GCP service account access remains blocked by Cloud Run. */
  allowEgress?: boolean
  /** Root filesystem to expose to sandboxes. Defaults to /. */
  rootfs?: string
  /** Working directory for sandboxed commands or newly-created stateful sessions. */
  workdir?: string
  /** Container template name for Cloud Run multi-container services. */
  template?: string
  /** Writable persistent host path shared across executions. */
  persistDir?: string
  /** Writable overlay directory. Caller is responsible for cleanup. */
  overlayDir?: string
  /** Allow mounted filesystems to be writable. */
  write?: boolean
  /** Bind mounts to attach to the sandbox. */
  mounts?: CloudRunMount[]
  /** Environment variables applied to sandboxed commands or newly-created stateful sessions. */
  env?: Record<string, string>
  /** Extra args passed before the sandbox subcommand, e.g. global debug flags. */
  globalArgs?: string[]
  /** Extra args passed to `sandbox do` and `sandbox run`. */
  runArgs?: string[]
  /** Extra args passed to `sandbox exec` in stateful mode. */
  execArgs?: string[]

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
