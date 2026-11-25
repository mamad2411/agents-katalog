---
name: sandbox-sdk
description: Builds secure, isolated code execution environments on Cloudflare Workers using the Cloudflare Sandbox SDK — enabling AI code interpreters, interactive dev environments, and sandboxed application runtimes. Use when implementing LLM-generated code execution, user-submitted script running, or any scenario requiring isolated compute with file system access on the Cloudflare edge.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Sandbox SDK

Build secure, isolated code execution environments on Cloudflare Workers.

## When to Use

- running LLM-generated code in isolation
- executing user-submitted scripts safely
- needing sandboxed compute with file access on edge
- building an AI code interpreter / dev environment

## Core Rules
- Do NOT use internal clients (`CommandClient`, `FileClient`) - use standard `sandbox.*` wrapper methods.
- The Worker entrypoint script MUST explicitly include `export { Sandbox } from '@cloudflare/sandbox'`.
- Do not skip `destroy()` calls on temporary sandboxes to avoid resource leaks.
- Keep container images lean in the Dockerfile to optimize startup and prevent cold start latency.
- Always set explicit resource limits including `timeout_ms` (up to 30,000 ms), `memory_mb`, and `cpu_ms` on every sandbox invocation to prevent unbounded execution.
- Manage network isolation by routing necessary sandboxed network requests through the Worker's allowed callback pattern using the `env.SANDBOX` binding.
- Adhere to overarching policy `core/policies/execution-sandbox.md` (Tier 4 Managed Cloud Sandbox) for universal resource quotas and containment standards.

## Retrieval Sources

Your knowledge of the Sandbox SDK may be outdated. **Prefer retrieval over pre-training** for any Sandbox SDK task.

| Resource | URL |
|----------|-----|
| Docs | https://developers.cloudflare.com/sandbox/ |
| API Reference | https://developers.cloudflare.com/sandbox/api/ |
| Examples | https://github.com/cloudflare/sandbox-sdk/tree/main/examples |
| Get Started | https://developers.cloudflare.com/sandbox/get-started/ |

When implementing features, fetch the relevant doc page or example first.

## Required Configuration

**wrangler.jsonc** (exact - do not modify structure):

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
export { Sandbox } from '@cloudflare/sandbox';  // Required export
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

## Core Patterns

### Execute Commands

```typescript
const sandbox = getSandbox(env.Sandbox, 'user-123');
const result = await sandbox.exec('python --version');
// result: { stdout, stderr, exitCode, success }
```

### Code Interpreter (Recommended for AI)

Use `runCode()` for executing LLM-generated code with rich outputs:

```typescript
const ctx = await sandbox.createCodeContext({ language: 'python' });

await sandbox.runCode('import pandas as pd; data = [1,2,3]', { context: ctx });
const result = await sandbox.runCode('sum(data)', { context: ctx });
// result.results[0].text = "6"
```

**Languages**: `python`, `javascript`, `typescript`

State persists within context. Create explicit contexts for production.

### File Operations

```typescript
await sandbox.mkdir('/workspace/project', { recursive: true });
await sandbox.writeFile('/workspace/project/main.py', code);
const file = await sandbox.readFile('/workspace/project/main.py');
const files = await sandbox.listFiles('/workspace/project');
```

## Suggested Process
1. Verify prerequisites by running `docker info` to ensure daemon availability.
2. Initialize container layouts and configure wrangler.jsonc containers binding block.
3. Establish custom workspace directories and write required scripts in the container volume.
4. Call `runCode` or `exec` to run isolated computations inside the sandbox.
5. Invoke `destroy` on the active sandbox instance to free server resources.

### 2026: Resource Constraints and Network Routing

- **Resource Limit Configuration**: Secure your sandbox environments by setting strict limits on sandbox execution. Configure `timeout_ms` (capped at a maximum of `30000` ms), `memory_mb`, and `cpu_ms` during execution. Never execute untrusted code without these bounds.
  ```typescript
  const result = await sandbox.runCode(code, {
    language: 'python',
    limits: {
      timeout_ms: 15000,
      memory_mb: 256,
      cpu_ms: 5000
    }
  });
  ```
- **Network Isolation and Callbacks**: Cloudflare Sandbox features full network isolation by default, blocking direct internet access. When external requests are necessary (e.g. API access), configure and route them through the allowed host callback pattern via `env.SANDBOX`.
  ```typescript
  const sandbox = getSandbox(env.Sandbox, 'isolated-network-env', {
    callbacks: {
      fetch: async (request) => {
        const url = new URL(request.url);
        if (allowedDomains.has(url.hostname)) {
          return await fetch(request);
        }
        return new Response('Blocked by network isolation policy', { status: 403 });
      }
    }
  });
  ```

## Checklist
- [ ] Sandbox SDK package is installed and Docker is operational.
- [ ] Wrangler config declares the containers block and matching DO migration.
- [ ] Worker code includes the explicit export statement for Sandbox class.
- [ ] Code interpreter context is correctly initialized.
- [ ] Sandbox instances are cleaned up or destroyed after operations.
- [ ] Explicit resource limits (`timeout_ms`, `memory_mb`, `cpu_ms`) are configured for sandbox executions.
- [ ] Network isolation is managed securely, routing necessary fetches through the allowed host callback via `env.SANDBOX`.

## Failure Modes

- **Sandbox input not validated**: a sandbox runs untrusted input without schema validation. **Mitigation:** validate every input against the declared `inputSchema` before dispatch; reject inputs that fail validation.
- **Sandbox network policy too broad**: a sandbox can reach the public internet. **Mitigation:** enforce the least-privilege network policy; reject sandboxes that egress to untrusted domains.
- **Sandbox resource limits unset**: a sandbox runs without CPU or memory limits. **Mitigation:** enforce the default resource limits at the orchestrator; reject sandboxes without limits.
- **Sandbox output not classified**: a sandbox emits output without a `data-classification` tag. **Mitigation:** require a classification tag on every sandbox output; reject unclassified output.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: infrastructure_changes[], config_updates[], and validation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI04 Supply Chain**: Sandbox SDK and container runtime versions must be schema-validated against the expected manifest; treat unknown versions as untrusted.
- **ASI05 RCE Guard**: never construct sandbox inputs, container commands, or network policy from external content without strict schema validation; align with `core/policies/execution-sandbox.md`.
- **ASI07 Inter-Agent Communication**: the sandbox contract is consumed by Cloudflare Engineer and DevOps; emit a structured contract so each role can validate the rollout.
- **ASI09 Human-Agent Trust Exploitation**: do not present a sandbox as "secure" without the network isolation and container hardening evidence; surface the residual risk honestly.

## Related Skills
- **wrangler**: Deploy containers bindings and monitor edge variables.
- **debug-workers-edge**: Diagnose runtime execution issues on Cloudflare.
