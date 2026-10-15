---
name: railway-sandbox
description: Guide for creating and managing Railway sandboxes using ComputeSDK. Use when building applications that need self-hosted sandbox environments on Railway's infrastructure for code execution, containerized development, or persistent services.
---

# Railway Sandboxes with ComputeSDK

Self-host sandbox environments on Railway's infrastructure through ComputeSDK's unified API. Railway provides instant deployments with automatic SSL — ideal for self-hosted sandbox environments, persistent services, and containerized development.

## Prerequisites

Before using Railway as a provider, deploy the ComputeSDK sandbox template to your Railway account (one-time setup):

[![Deploy to Railway](https://railway.com/button.svg)](https://railway.com/new/template/sandbox)

This deploys a lightweight binary that converts Railway into a sandbox provider.

## Setup

```bash
npm install computesdk
```

```bash
# .env
COMPUTESDK_API_KEY=your_computesdk_api_key
RAILWAY_API_KEY=your_railway_api_key
RAILWAY_PROJECT_ID=your_railway_project_id
RAILWAY_ENVIRONMENT_ID=your_railway_environment_id
```

Get your ComputeSDK key at https://console.computesdk.com/register

### Getting Railway Credentials

- **API Token**: Railway workspace settings -> Tokens -> New Token
- **Project ID**: Project -> Settings -> Project Info
- **Environment ID**: Found in the URL: `railway.com/project/{PROJECT_ID}/settings?environmentId=={ENVIRONMENT_ID}`

## Quick Start

```typescript
import { compute } from 'computesdk';
// Auto-detects Railway from environment variables

const sandbox = await compute.sandbox.create();
console.log(`Sandbox: ${sandbox.sandboxId}`);

const result = await sandbox.runCode('print("Hello from Railway!")');
console.log(result.output);

await sandbox.destroy();
```

## Explicit Configuration

For multi-provider setups or when you want to be explicit:

```typescript
import { compute } from 'computesdk';

compute.setConfig({
  computesdkApiKey: process.env.COMPUTESDK_API_KEY,
  provider: 'railway',
  railway: {
    apiToken: process.env.RAILWAY_API_KEY,
    projectId: process.env.RAILWAY_PROJECT_ID,
    environmentId: process.env.RAILWAY_ENVIRONMENT_ID,
  }
});

const sandbox = await compute.sandbox.create();
```

## Railway Configuration Options

```typescript
interface RailwayConfig {
  apiToken?: string;        // Uses RAILWAY_API_KEY env var if not set
  projectId?: string;       // Uses RAILWAY_PROJECT_ID env var if not set
  environmentId?: string;   // Uses RAILWAY_ENVIRONMENT_ID env var if not set
}
```

## Full API

ComputeSDK provides the same API across all providers: filesystem operations, shell commands, managed servers, overlays, terminals, and client access.

Install the main skill for the complete reference:

```
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/