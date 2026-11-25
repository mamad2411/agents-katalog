---
name: comfyui-api-and-sdk
description: Use for ComfyUI HTTP APIs, WebSockets, job submission, object/node discovery, uploads/downloads, Python/TypeScript/Swift SDKs, comfy-cli, comfy-api-proxy, comfy-mcp, Cloud versus self-hosted integration, and external applications that drive ComfyUI.
metadata:
  version: "00.01.11"
---
# ComfyUI API and SDK

## First classify the target

Identify whether the client talks to:

- self-hosted ComfyUI server;
- Comfy Cloud;
- `comfy-api-proxy`;
- an SDK abstraction;
- MCP;
- CLI.

Do not merge route/payload assumptions across these surfaces.

## Sources

Use the matching official SDK/tool repository, `Comfy-Org/docs`, and the target/current core server source.

## Procedure

1. Determine target service and version.
2. Prefer the official SDK for that language when it supports the required operation.
3. Inspect current SDK signatures and examples instead of recalling them.
4. If direct HTTP/WebSocket access is required, inspect current official server routes/messages for the target.
5. Implement timeouts, connection failures, execution errors, and output retrieval explicitly.
6. Treat node discovery as target-specific data.
7. Avoid embedding secrets in workflow JSON, logs, or source.
8. Add a small integration test against a controlled target when practical.

## Compatibility

If supporting both Cloud and self-hosted, keep differences explicit behind an adapter rather than pretending the endpoints are identical.

## MCP

Treat MCP as an integration layer, not as specification authority for ComfyUI internals. Verify underlying behavior against the target/core when needed.

## Acceptance gate

Before calling an integration complete:

- identify the exact service surface: self-hosted, Cloud, proxy, SDK, MCP, or CLI;
- verify current routes or SDK signatures from the matching official source;
- test timeout and error handling, not only the successful response;
- keep credentials out of source, workflow files, and logs;
- run a controlled integration test when practical;
- report untested network/service paths explicitly.

