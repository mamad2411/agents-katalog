---
name: apiiro-mcp-secure-prompt
description: |
  Use the Apiiro MCP tool `apiiro_secure_prompt` when Apiiro MCP is configured in the client and the user wants security guidance added to a coding task before implementation. Trigger on secure-prompt via MCP, or when the user asks for security-aware prompt enhancement before coding (auth, new APIs, persistence, secrets, integrations).
---

# Apiiro Secure Prompt (MCP: `apiiro_secure_prompt`)

Enhance a coding prompt with security context through the **Apiiro MCP** tools. Relevant whenever you have **Apiiro MCP configured** in your environment (IDE, agent, or other MCP client).

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| Apiiro MCP configured | MCP client is connected to an Apiiro MCP server; tools are available after a successful session. |
| Tool available | If `apiiro_secure_prompt` does not appear, the server may not expose that tool—check with your Apiiro administrator or deployment docs. |
| Auth | Follow whatever authentication your organization configured for that MCP server. |

## Workflow (resolve key, then enhance)

1. **`apiiro_resolve_repository_key`** — Pass `repository_name` (optional `branch`, `remote_url`). Returns a `repository_key` string or an error payload.
2. **`apiiro_secure_prompt`** — Pass the **original user task** as `developer_prompt`, the `repository_key` from step 1, and optionally `file_path` (current file for scoped context).

If you already have a valid `repository_key` for the repo, skip step 1.

**Resolve key with less ambiguity:** When the repo might not match by name alone, pass `remote_url` from `git remote get-url origin` and the current branch from `git branch --show-current`.

**Run in parallel with exploration:** Do not block codebase reads or searches on the MCP call—invoke `apiiro_secure_prompt` (after you have or can cheaply obtain `repository_key`) alongside looking up relevant files, unless the task strictly depends on the enhanced text before any read.

## Tool parameters

| Argument | Required | Purpose |
|----------|----------|---------|
| `developer_prompt` | Yes | Verbatim coding task or feature request to enrich. |
| `repository_key` | Yes | From `apiiro_resolve_repository_key`, or an existing key for that repository. |
| `file_path` | No | File path string for tighter scope (e.g. the file being edited). |

**Return value:** On success, the **enhanced prompt text** (plain string). On failure, a structured error string from the MCP server.

## When to skip or deprioritize

- Pure refactors, docs-only edits, comment-only changes, or read-only exploration (no new surface area).
- The upstream tool is aimed at **new features, API/auth changes, data model updates, integrations**—not debugging, perf-only work, or routine test fixes.

## Tips for better enrichments

| Situation | What to do |
|-----------|------------|
| Task is one line or vague (e.g. “check auth flow”) | Expand `developer_prompt` to a short spec: goal, constraints, environment; add `file_path` to the main file under review. |
| Output looks unchanged or nearly identical to input | Retry once with `file_path` and a fuller `developer_prompt`; if still thin, proceed and apply normal secure-design practices (input validation, least privilege, secrets handling, audit logging) per org standards. |
| Monorepo or fork | Prefer accurate `repository_name` + `remote_url` so `apiiro_resolve_repository_key` maps to the right Apiiro project. |

## Optional: known repository keys

Some environments document a fixed `repository_key` for a specific repo (e.g. to skip resolve). Use only if your team’s docs list one; otherwise always resolve via `apiiro_resolve_repository_key`.
