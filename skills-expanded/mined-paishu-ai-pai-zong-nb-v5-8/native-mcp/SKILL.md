---
name: native-mcp
description: "Design or review native MCP client/server integration, tool registration, stdio/HTTP transport, schemas, and runtime boundaries."
---

# native-mcp

## Purpose

Design or review native MCP client/server integration, tool registration, stdio/HTTP transport, schemas, and runtime boundaries.

## Use When

- The task involves MCP client design, server connection, tool registration, transport selection, or schema validation.
- The user needs a native MCP integration plan rather than a generic plugin explanation.

## Workflow

1. Identify client, server, transport, auth, tool schema, and lifecycle boundaries.
2. Prefer existing SDKs or official docs for version-specific implementation details.
3. Define tool inputs/outputs, error handling, timeout, logging, and permission model.
4. Separate local-only tools from external or credentialed tools.
5. Verify with a minimal server/tool handshake or provide a concrete smoke-test plan.

## Codex Runtime Rules

- Use only tools, plugins, MCP servers, files, and credentials that are actually available in the current Codex session.
- If an external write, install, publish, deploy, paid action, credential use, or account operation is needed, ask for explicit confirmation first.
- If the required tool is unavailable, return a portable fallback such as Markdown, CSV, prompt pack, implementation plan, or verification checklist.
- Do not claim files, videos, images, issues, API calls, or integrations were created unless there is concrete local or tool evidence.
- Keep long vendor recipes and examples out of the prompt path; load only task-relevant references when they exist.

## Avoid

- Do not import source-runtime commands, reload semantics, home-directory paths, or tool names as if they are Codex capabilities.
- Do not fabricate external state, API results, generated media, issue updates, or test outcomes.
- Do not broaden the task into unrelated setup or account configuration.

## Output

Architecture, schema boundaries, implementation steps, verification checks.

For non-trivial work, include:

```markdown
Result: ...
Evidence: ...
Verification: PASS/FAIL/NOT RUN
Risks / Next Steps: ...
```
