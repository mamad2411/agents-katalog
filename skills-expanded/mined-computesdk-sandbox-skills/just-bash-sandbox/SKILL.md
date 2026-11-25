---
name: just-bash-sandbox
description: Guide for creating and managing Just Bash sandboxes using ComputeSDK. Use when building applications that need just-bash provider for ComputeSDK - local sandboxed bash execution with virtual filesystem.
---

# Just Bash Sandboxes with ComputeSDK

just-bash provider for ComputeSDK - local sandboxed bash execution with virtual filesystem.

## Setup

```bash
npm install computesdk @computesdk/just-bash
```

No API credentials are required by default for this provider. Configure any optional settings in the config object below.

## Quick Start

```typescript
import { compute } from 'computesdk';
import { justBash } from '@computesdk/just-bash';

compute.setConfig({
  provider: justBash({
    // python: <boolean>,
    // env: "your_env",
    // cwd: "your_cwd",
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from Just Bash!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { justBash } from '@computesdk/just-bash';

const sdk = justBash({
    // python: <boolean>,
    // env: "your_env",
    // cwd: "your_cwd",
  });
const sandbox = await sdk.sandbox.create();
```

## Just Bash Configuration

```typescript
interface JustBashConfig {

  python?: boolean;
  files?: BashOptions['files'];
  env?: Record<string, string>;
  cwd?: string;
  fs?: BashOptions['fs'];
  customCommands?: BashOptions['customCommands'];
  network?: BashOptions['network'];

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
