---
name: vercel-sandbox
description: Guide for creating and managing Vercel sandboxes using ComputeSDK. Use when building applications that need Vercel Sandbox provider for ComputeSDK - serverless code execution for Python and Node.js on Vercel's edge network.
---

# Vercel Sandboxes with ComputeSDK

Vercel Sandbox provider for ComputeSDK - serverless code execution for Python and Node.js on Vercel's edge network.

## Setup

```bash
npm install computesdk @computesdk/vercel
```

Set your credentials:

```bash
# .env
VERCEL_OIDC_TOKEN=your_vercel_oidc_token
VERCEL_PROJECT_ID=your_vercel_project_id
VERCEL_TEAM_ID=your_vercel_team_id
VERCEL_TOKEN=your_vercel_token
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { vercel } from '@computesdk/vercel';

compute.setConfig({
  provider: vercel({
    token: process.env.VERCEL_TOKEN,
    projectId: process.env.VERCEL_PROJECT_ID,
    teamId: process.env.VERCEL_TEAM_ID,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Vercel!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { vercel } from '@computesdk/vercel';

const sdk = vercel({
    token: process.env.VERCEL_TOKEN,
    projectId: process.env.VERCEL_PROJECT_ID,
    teamId: process.env.VERCEL_TEAM_ID,
  });
const sandbox = await sdk.sandbox.create();
```

## Vercel Configuration

```typescript
interface VercelConfig {

  token?: string;
  teamId?: string;
  projectId?: string;
  timeout?: number;
  ports?: number[];
  daemonSsePort?: number | false;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
