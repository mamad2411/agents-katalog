---
name: "proxyman-traffic-debugging"
description: "Use Proxyman MCP to inspect and debug HTTP, HTTPS, and WebSocket traffic and operate the complete Proxyman MCP surface. Use for flows, API diagnosis, filtering, export, replay, Compose, debugging rules, WebSockets, recording, proxy and certificate control, code generation, or guided setup."
---

# Proxyman Traffic Debugging And MCP Operations

Use Proxyman MCP as a local control plane for the running Proxyman app. Start read-only, identify the relevant captured flow or current state, then make only the change the user requested.

If Proxyman tools are unavailable, use `proxyman-mcp-setup`. If Proxyman is absent, use `proxyman-download-setup`. For target-specific HTTPS configuration, use `proxyman-https-capture`. For current product documentation, use `proxyman-debugging-tools`. For shell automation, use `proxyman-cli`.

## Sources Of Truth

Use this order whenever sources disagree:

1. The connected server's `tools/list`, `resources/list`, and `prompts/list` for available MCP capabilities and exact schemas.
2. Current state returned by Proxyman status/list tools.
3. Built-in MCP resources for version-matched setup, CLI, and scripting guidance.
4. Official live documentation through `proxyman-debugging-tools` for GUI behavior and features beyond the built-in setup index.
5. The bundled references in this skill as an orientation map.

Never invent a tool, enum, parameter, rule ID, flow ID, file path, or command flag. The stdio bridge uses strict schemas.

## Mental Model

- The MCP client launches Proxyman's bundled `mcp-server` over stdio. The bridge reads a local handshake and forwards calls to an authenticated localhost server in the running app.
- Never hardcode the HTTP port or token. Each client bridge lasts only while its stdin remains open.
- Flow tools use the active workspace's sidebar-backed traffic universe. That includes flows from regular folders and, when present, saved, pinned, imported, Atlantis, and remote-device sources; results are deduplicated across folders rather than limited to the selected folder.
- List/filter results are snapshots. A flow ID can disappear after a clear, import, source change, or restart.
- Some actions are platform-specific. System proxy, Terminal injection, Electron `.app` injection, and app control are primarily macOS operations. Trust live discovery on Windows and Linux.

## Start Every MCP Session

1. Discover tools, resources, and prompts if the client exposes discovery.
2. Call `get_version` to verify the bridge reaches Proxyman.
3. Call `get_proxy_status` to learn recording state, proxy port, and SSL Proxying state.
4. Use the smallest read operation that establishes the target: `get_flows`, `filter_flows`, a status call, or the relevant list call.
5. Read detail using returned identifiers. Do not infer IDs from names or visible order.
6. Explain any mutation and its effect, obtain consent where required, call it, then verify with a read operation.

For tool selection, read [MCP tool catalog](references/mcp-tool-catalog.md). For multi-step tasks, read [MCP workflows](references/mcp-workflows.md). For Breakpoint, Map Local, Map Remote, Scripting, or overlapping modification rules, read [request and response rules](references/request-response-rules.md). For built-in knowledge, read [MCP resources and prompts](references/mcp-resources-prompts.md).

## Privacy And Consent

Keep **Settings > MCP > Redact Sensitive Data Before Sending to AI** enabled by default. It covers common secret headers, cookies, query values, JWTs, credentials, and secret-like body fields in MCP output.

Redaction does not sanitize the original HAR or Proxyman log written by `export_flows`. Treat exported files as sensitive.

Require explicit user approval immediately before:

- clearing the session, deleting a rule or Compose draft, closing a WebSocket, quitting Proxyman, or uninstalling a certificate;
- changing system proxy, certificate trust, recording, SSL Proxying, external proxy, or global debugging-tool state when the user did not already request that exact change;
- running guided automation, Terminal injection, Electron injection, or any action that launches or modifies another app;
- exporting original traffic or sending proxy credentials;
- disabling MCP redaction or revealing raw secrets.

Use an explicit approved destination for exports. Do not claim an export is redacted merely because MCP previews are redacted.

## Operating Pattern

### Inspect And Diagnose Traffic

1. Confirm capture state with `get_proxy_status`.
2. Narrow candidates with `get_flows` or `filter_flows`. Use client/device identity when the user names a source.
3. Inspect representative IDs with `get_flow_detail`; use its Summary metadata, timing, sizes, connection/TLS details, headers, query, cookies, and body preview.
4. Correlate method, URL, status, timing, request sequence, client, and matched debugging tools.
5. Return a verdict: passed, suspicious, failed, or inconclusive, with the flow IDs and observations supporting it.
6. Export or generate code only when the user needs a reproducible artifact.

### Mutate Proxyman Safely

1. Read the current state and capture the relevant IDs.
2. State the smallest proposed change and whether it affects capture, trust, traffic, disk, or another app.
3. Use the exact live schema. Omit optional fields only when the tool documents patch semantics.
4. Verify the returned object and call the matching list/status/detail tool.
5. Report changed IDs and an exact rollback action when one exists.

### Handle A Tool Error

1. Read the full MCP error; schema and validation errors are designed to be actionable.
2. Refresh live discovery after an app update or a `tool not found` result.
3. Re-list flows or rules when an ID is stale.
4. Correct the smallest invalid field; do not weaken the user's requested scope.
5. If the capability is not exposed, route to the GUI or `proxyman-cli` and say that MCP cannot perform it in this build.

## Critical Semantics

- `get_flows`/`filter_flows` return at most 500 results and body previews can be truncated. Use a user-approved export for complete archival data.
- `filter_flows` can filter on `client`; prefer it when distinguishing device, simulator, Atlantis, or app sources.
- Use `list_rules` for Breakpoint, Map Local, Map Remote, Block List, Scripting, Allow List, Network Condition, and DNS Spoofing. Reverse Proxy has its own list tool.
- Create/update operations use returned IDs. Updates preserve IDs.
- Successful rule CRUD, rule toggles, and global feature toggles refresh the corresponding open Proxyman lists/editors. Deleting the rule currently being edited closes that editor.
- Rule methods support uppercase `QUERY`; use `ANY` only for all methods. Set `include_paths` deliberately because defaults differ by rule type.
- Creating Scripting, Allow List, Network Condition, DNS Spoofing, or Reverse Proxy enables the associated feature. Verify other feature state with `list_tool_status`.
- Only one Network Condition can be active at a time.
- Network Condition profile names and supported scope come from the live schema. Do not invent custom bandwidth values when it exposes presets only.
- A Map Local literal-response update should send `response_body`, `status_code`, and `content_type` together.
- The reviewed MCP can manage Breakpoint rules but cannot edit or execute/cancel/abort an actively paused breakpoint; that interaction remains in the Proxyman GUI.
- The reviewed MCP Map Local surface creates literal or captured-flow responses, not arbitrary file/directory rules. Map Remote's reviewed MCP schema does not expose the CLI's separate preserve-original-URL option.
- For overlapping Map Local, Map Remote, Scripting, and Breakpoint rules, verify the ordered Debugging Tools summary instead of assuming every matching rule runs.
- External proxy changes should send a complete setting for the selected kind; omitted values are not reliably patch-preserved. Ask before passing credentials.
- Compose IDs are in-memory. `send_compose_http` is HTTP-only; WebSocket URLs are rejected.
- The reviewed MCP has no separate one-click Repeat action. Seeding Compose from a flow is an Edit & Repeat analogue, not exact GUI Repeat/history parity.
- MCP can show Protobuf content after Proxyman decodes it but does not configure Protobuf schemas/rules. TLS Key Logging is also GUI-only in the reviewed MCP.
- WebSocket payload previews are limited and redacted. `close_websocket_session` applies only to an active Compose-created WebSocket session.
- Scripting handlers must use Proxyman's positional signatures. Read `docs://scripting/snippet-code` before non-trivial script generation.
- `get_proxyman_cli_help` only returns safe, version-matched help. It never executes an operational CLI command.

## Expected Result

Finish with:

- what was inspected or changed;
- the relevant flow/rule/draft IDs;
- evidence from the verification read;
- privacy, export, or platform limitations;
- a rollback or next diagnostic step when appropriate.

Do not claim traffic is complete when capture state, time window, client source, or preview truncation makes the result inconclusive.

## Troubleshooting

- Handshake missing: launch Proxyman and enable Settings > MCP, or use `proxyman-mcp-setup`.
- Invalid handshake/401: restart Proxyman and reload the MCP client.
- No flows: check recording, target proxy routing, root trust, SSL Proxying, client source, and target-specific setup with `proxyman-https-capture`.
- HTTPS remains opaque: inspect certificate status and SSL Proxying includes/excludes before changing either.
- Localhost is absent: many clients bypass system proxy; use the Reverse Proxy workflow or the target's explicit proxy configuration.
- VPN blocks device capture: use the Atlantis decision path for supported iOS apps.
- Automation fails: check visible OS permission prompts, target availability, certificate state, and required user consent before retrying.
