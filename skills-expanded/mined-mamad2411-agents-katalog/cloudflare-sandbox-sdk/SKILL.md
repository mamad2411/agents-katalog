---
name: cloudflare-sandbox-sdk
description: Build sandboxed applications for secure code execution on Cloudflare. Use when building AI code execution, code interpreters, CI/CD systems, interactive dev environments, or executing untrusted code.
license: Apache 2.0
metadata:
  source: https://github.com/cloudflare/skills
  category: cloudflare
---

# Cloudflare Sandbox SDK

Build secure, isolated code execution environments on Cloudflare Workers.

## FIRST: Verify Installation

```bash
npm install @cloudflare/sandbox
docker info  # Must succeed - Docker required for local dev
```

## Retrieval Sources

| Resource | URL |
|----------|-----|
| Docs | https://developers.cloudflare.com/sandbox/ |
| API Reference | https://developers.cloudflare.com/sandbox/api/ |
| Examples | https://github.com/cloudflare/sandbox-sdk/tree/main/examples |
| Get Started | https://developers.cloudflare.com/sandbox/get-started/ |

## Required Configuration

**wrangler.jsonc**:

```jsonc
{
  "containers": [{
    "class_name": "Sandbox",
    "image": "./Dockerfile",
    "instance_type": "lite",
    "max_instances": 1
  }],
  "durable_objects": {
    "bindings": [{ "class_name": "Sandbox", "name": "Sandbox" }]
  },
  "migrations": [{ "new_sqlite_classes": ["Sandbox"], "tag": "v1" }]
}
```

**Worker entry** - must re-export Sandbox class:

```typescript
import { getSandbox } from '@cloudflare/sandbox';
export { Sandbox } from '@cloudflare/sandbox';
```

## Quick Reference

| Task | Method |
|------|--------|
| Get sandbox | `getSandbox(env.Sandbox, 'user-123')` |
| Run command | `await sandbox.exec('python script.py')` |
| Run code (interpreter) | `await sandbox.runCode(code, { language: 'python' })` |
| Write file | `await sandbox.writeFile('/workspace/app.py', content)` |
| Read file | `await sandbox.readFile('/workspace/app.py')` |
| Create directory | `await sandbox.mkdir('/workspace/src', { recursive: true })` |
| List files | `await sandbox.listFiles('/workspace')` |
| Expose port | `await sandbox.exposePort(8080)` |
| Destroy | `await sandbox.destroy()` |

## When to Use What

| Need | Use | Why |
|------|-----|-----|
| Shell commands, scripts | `exec()` | Direct control, streaming |
| LLM-generated code | `runCode()` | Rich outputs, state persistence |
| Build/test pipelines | `exec()` | Exit codes, stderr capture |
| Data analysis | `runCode()` | Charts, tables, pandas |

## Code Interpreter

```typescript
const ctx = await sandbox.createCodeContext({ language: 'python' });
await sandbox.runCode('import pandas as pd; data = [1,2,3]', { context: ctx });
const result = await sandbox.runCode('sum(data)', { context: ctx });
// result.results[0].text = "6"
```

**Languages**: `python`, `javascript`, `typescript`

## Sandbox Lifecycle

- `getSandbox()` returns immediately - container starts lazily on first operation
- Containers sleep after 10 minutes of inactivity (configurable via `sleepAfter`)
- Use `destroy()` to immediately free resources
- Same `sandboxId` always returns same sandbox instance

## Anti-Patterns

- Don't use internal clients (`CommandClient`, `FileClient`) - use `sandbox.*` methods
- Don't skip the Sandbox export - Worker won't deploy without `export { Sandbox }`
- Don't hardcode sandbox IDs for multi-user - use user/session identifiers
- Don't forget cleanup - call `destroy()` for temporary sandboxes

## Keywords

Cloudflare, sandbox, code execution, code interpreter, isolated, Docker, untrusted code, CI/CD
