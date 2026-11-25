---
name: nyxid-service-call
description: Invoke an operation on a connected and authorized NyxID service through Aevatar's dynamically typed connected-service tools or the credential-injecting nyxid_proxy fallback. Use when a user asks to read, search, create, update, send, run, download, or otherwise call a NyxID service while keeping upstream credentials inside NyxID and respecting provider scopes, approvals, and service routing. 中文触发包括“调用我的 NyxID 服务”“使用服务”“让服务执行”。
version: "1.1"
metadata:
  category: tool-based
  tool-list:
    - nyxid_services
    - nyxid_proxy
  tag:
    - nyxid
    - services
    - invocation
    - proxy
    - openapi
    - aevatar
---

# Call a NyxID service

Route every provider request through NyxID. Never use the NyxID CLI, call the upstream endpoint directly, request a raw bearer, or add an upstream `Authorization` or credential header. NyxID injects the stored credential and owns audit, approval, routing, and delegation.

## Resolve the target

1. Call `nyxid_services` with `action: "list"` unless the current connected-services context already identifies one exact active slug.
2. Resolve by exact service ID or slug. If a label maps to multiple instances, ask the user to choose; never pick the first one for a write.
3. If the service is absent, inactive, missing credentials, or not authorized for this app, stop and use `nyxid-service-connect` or `nyxid-service-maintenance` as appropriate.

## Select an operation

Prefer an exposed typed connected-service tool named like `nyxid_{service-slug}__{operation}`. These tools exist only when the active route includes the `nyxid.connected_services` tool set and the service OpenAPI operation opts in with `x-aevatar-tool`. Follow the selected tool's schema exactly.

If no matching typed tool is exposed, use the API hints in the current connected-services context and call `nyxid_proxy` with the exact slug, relative path, method, and JSON-string body. Do not duplicate a version prefix already present in the service base URL. Do not guess undocumented paths, methods, fields, or provider scopes; ask for the API contract when no trustworthy hint exists.

Use `response_mode: "file_artifact"` only for a GET binary download in a managed workflow run. Use the normal text mode otherwise.

## Mutation and approval rules

Execute read-only requests when they directly answer the user's request. For writes, require clear user intent for the exact target and effect. Before destructive, irreversible, externally visible, financial, permission-changing, or bulk operations, summarize the effect and obtain explicit confirmation if it was not already unambiguous.

Never bypass an Aevatar or NyxID approval. A provider approval can keep a proxy request open for 30 seconds or more; do not issue a duplicate request while it is pending. Do not turn a failed write into a retry loop.

## Handle results

- On an app service-authorization error, surface the chat's authorization action for that exact connected service; do not ask for a token.
- On an upstream 401 or credential error, send the user to secure credential repair through `nyxid-service-maintenance`; do not request the credential in chat.
- On 404, verify the relative base path and target identifier once before concluding the object is absent.
- On 429 or transient 5xx, report the retry condition. Retry only when the operation is read-only or idempotency is established.
- Preserve returned identifiers, status, and actionable error details. Summarize large payloads without inventing fields or hiding partial failure.
