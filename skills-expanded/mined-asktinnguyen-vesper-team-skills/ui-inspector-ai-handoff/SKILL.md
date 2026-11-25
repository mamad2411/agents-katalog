---
name: ui-inspector-ai-handoff
description: "This skill should be used when porting a Vesper-style dev-mode UI inspector across Electron or web apps so selected UI context can be sent to chat and exposed through read-only agent tools. Triggers on requests like: add a dev-mode UI inspector, send inspected element to chat, expose inspector state as read-only tools, port Electron inspector pattern to web."
---

# UI Inspector AI Handoff

Implement a parity-by-design UI inspector: one shared snapshot/context model, one human handoff path, one read-only agent path.

## When To Use

Use this skill when:
- Building click-to-inspect tooling in development mode.
- Sending selected UI context to an AI chat turn for code edits.
- Exposing the same selected UI context to agent tools/APIs.
- Porting Vesper-style inspector architecture into Electron or web apps.

## Scope Deconfliction

Use this skill when the outcome is cross-platform portability and handoff quality.

Use `electron-ui-inspector` instead when:
- the scope is Electron-only implementation speed
- you do not need a web workflow
- you want a lighter checklist with fewer contracts

Use this skill when you need all of:
- Electron and/or web workflow routing
- strict parity contracts between human and agent paths
- reusable docs/scripts for rollout, testing, and troubleshooting

## Route By Platform

| Platform | Primary Workflow |
|---|---|
| Electron app | `workflows/electron.md` |
| Web app | `workflows/web.md` |

Read only the selected platform workflow first, then load references listed in its `<required_reading>` block.

## Canonical Naming Map

Use one naming model across docs and implementation.

| Layer | Canonical Name |
|---|---|
| Internal action (callback params) | `get_state`, `get_selection`, `get_context`, `capture_screenshot` |
| Session tool IDs | `vesper_ui_get_state`, `vesper_ui_get_selection`, `vesper_ui_get_context`, `vesper_ui_capture_screenshot` |
| MCP-prefixed runtime IDs | `mcp__session__vesper_ui_get_state`, `mcp__session__vesper_ui_get_selection`, `mcp__session__vesper_ui_get_context`, `mcp__session__vesper_ui_capture_screenshot` |

Do not mix `ui_get_*` and `vesper_ui_*` in the same implementation.

## Prerequisites

| Requirement | Electron | Web |
|---|---|---|
| Dev-mode feature flag | Required | Required |
| Typed shared contracts | Required | Required |
| Existing chat send pipeline that accepts hidden context prefix | Required | Required |
| Read-only agent/tool runtime | Recommended | Recommended |
| `rg` available for verification commands | Recommended | Recommended |

## Integration Points

Implement these boundaries explicitly:
1. Capture adapter: DOM element -> normalized snapshot.
2. Context builder: snapshot -> compact structured context payload.
3. Chat adapter: user prompt + `agentContextPrefix` + optional visible inspector attachment.
4. Agent adapter: read-only tools -> callback -> shared inspector state.
5. Permission adapter: mark inspector tools read-only in safe mode.

## Canonical Contracts (Required)

Use `references/contracts.md` as the single source of truth for:
- configuration caps and enforcement ranges
- config resolution order (`defaults < env < runtime`, then clamp)
- typed result schema (`InspectorResult<T>`)
- error codes and fallback behavior

Use `references/troubleshooting.md` when implementation or rollout checks fail.

## Done Criteria

Mark complete only when all are true:
- Canonical naming map is implemented exactly.
- Human capture path and agent read-only path return the same selection data.
- Hidden context prefix is sent through existing chat pipeline (no parallel run path).
- Redaction and payload cap behavior is covered by tests.
- Verification commands in `references/testing-checklist.md` pass.

## Agent Response Contract

Return these fields in the final implementation report:
- `platform`: `electron` or `web`
- `files_changed`: list of absolute paths
- `tool_ids`: implemented inspector tool IDs
- `error_codes`: implemented error taxonomy
- `config_values`: final cap values
- `test_commands_run`: exact commands
- `test_results`: pass/fail summary
- `residual_risks`: unresolved edge cases

## Related Skills

| Trigger Condition | Next Skill | Required Handoff Artifact | Return Point |
|---|---|---|---|
| Electron-only implementation, no web scope | `electron-ui-inspector` | file list + inspector state contract summary | return here for parity checks and final verification |
| New main/preload/renderer plumbing required | `build-electron-features` | IPC/preload contract diff | return here before parity tool wiring |
| Need Electron regression and E2E confidence | `vesper-electron-testing` | test commands + pass/fail output + screenshots (if captured) | return here for done-criteria validation |
| Need browser-level workflow validation | `webapp-testing` | test script or replay steps + results | return here for rollout checks |

## References

- Workflow: `workflows/electron.md`
- Workflow: `workflows/web.md`
- Architecture analysis: `references/vesper-ui-inspector-analysis.md`
- Canonical contracts: `references/contracts.md`
- Platform details: `references/electron-porting-guide.md`
- Platform details: `references/web-porting-guide.md`
- Reusable snippets: `references/code-examples.md`
- Verification and CI checklist: `references/testing-checklist.md`
- Troubleshooting runbook: `references/troubleshooting.md`
- Vesper source map: `references/source-map.md`
- Automation helper: `scripts/verify-inspector-parity.sh`
