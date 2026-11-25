---
name: mcp-engineering
description: Build and harden Model Context Protocol (MCP) servers, transports (stdio, SSE, Streamable HTTP), Zod/JSON Schema tool contracts, workspace path-traversal sandboxing, and bounded process execution.
---

# MCP Server & Tool Engineering (`/mcp-engineering`)

> **Role**: Principal MCP & Agent Tooling Architect  
> **Philosophy**: *Treat every MCP tool argument as hostile input. Sandbox filesystem paths with realpath prefix checks. Bound stdout/stderr memory. Return structured recovery errors instead of crashing the transport.*

Distilled from real local-agent MCP server engineering (`domodomo`), this skill governs server transports, tool schema design, workspace filesystem security, and deterministic process cleanup.

---

## 1. Quick Navigation & References

| Resource | Purpose |
| :--- | :--- |
| [references/mcp-transport-and-sandboxing.md](references/mcp-transport-and-sandboxing.md) | `stdio` vs `SSE`/`Streamable HTTP` lifecycle, Zod tool schemas, `realpath` sandbox patterns, stdout caps. |
| [scripts/verify_mcp_hygiene.py](scripts/verify_mcp_hygiene.py) | CLI auditor detecting unsafe `path.join` traversal, `shell: true`, unbounded `execSync`, and missing schema checks. |

---

## 2. Core MCP Security & Architecture Invariants

| Gate | Prohibited Pattern | Mandatory Production Standard |
| :--- | :--- | :--- |
| **Workspace Sandbox** | `path.join(root, args.path)` without normalization | Resolve `fs.realpathSync` and assert `resolved.startsWith(realRoot + path.sep)` before read/write. |
| **Tool Schemas** | Untyped `any` args or vague `"data"` descriptions | Explicit Zod / JSON Schema with `.describe()`, `.min()`, `.max()`, `.enum()`, and `additionalProperties: false`. |
| **Process Execution** | `exec(userCmd)` or `shell: true` | `spawn(cmd, argsArray, { shell: false })` with `30s` timeout and `1 MB` stdout/stderr cap. |
| **Transport & Logs** | Writing `console.log()` onto `stdio` MCP stream | On `stdio` servers, reserve `stdout` strictly for JSON-RPC frames; log diagnostics to `stderr`. |
| **Error Recovery** | Throwing uncaught exceptions killing the server | Return `{ isError: true, content: [{ type: "text", text: JSON.stringify({ code, message, hint }) }] }`. |

---

## 3. Safe Path Resolution Pattern (TypeScript)

```typescript
import fs from "node:fs";
import path from "node:path";

export function resolveSandboxedPath(workspaceRoot: string, userPath: string): string {
  const realRoot = fs.realpathSync(workspaceRoot);
  const candidate = path.resolve(realRoot, userPath);
  const realTarget = fs.existsSync(candidate)
    ? fs.realpathSync(candidate)
    : path.resolve(fs.realpathSync(path.dirname(candidate)), path.basename(candidate));

  if (realTarget !== realRoot && !realTarget.startsWith(realRoot + path.sep)) {
    throw new Error(`PATH_OUTSIDE_WORKSPACE: ${userPath}`);
  }
  return realTarget;
}
```

---

## 4. Automated MCP Hygiene Auditor

```bash
python3 skills/mcp-engineering/scripts/verify_mcp_hygiene.py --path . --strict
```
