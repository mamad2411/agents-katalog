---
name: cgx-capability-router
description: Resolve selector shortcalls and natural-language requests against the current Cognigrex toolkit/capability registry, using existing tools first and reporting real capability state.
---

# CGX Capability Router

Read `references/capabilities.json` first, then apply `cgx-handshake` and `cgx-minimum-sufficient-work`.

Recognize the compact form:

`@Selector /shortcall [object] [constraints...]`

A slash is optional when intent is unambiguous. Never claim a capability exists merely because a selector name suggests it.

## Routing order

1. Resolve the selector and current authority/recovery state.
2. Match an explicit shortcall or infer the closest registered route.
3. Inspect route state:
   - `available`: use the registered typed runtime function/tool.
   - `workflow`: execute the registered skill/composite sequence.
   - `gated`: surface the gate and execute only after the required approval.
   - `assisted`: use current source/query/cross-analysis tools and state the missing deterministic adapter.
   - `registered_unwrapped`: the host toolkit exists but must not be represented as a typed LightSpeed tool yet.
   - `missing`: do not simulate success; use `/extend` only when the user asks to build it.
4. Prefer existing receipts/results before new execution.
5. Prefer the selector's registered floors/toolkits, but capability and authority state override preference.
6. Return route ID, tools/functions used, receipt/evidence refs, limitation/gate, and next action.

## Execution boundary

Local runtime handlers are identifiers, not permission to execute arbitrary Python or shell. Use the existing LightSpeed supervisor/adapters or an available trusted connector/desktop tool. Heavy deterministic work remains local-first and separately gated.

Provider tools such as Drive, GitHub, web, desktop control, OpenAI Platform, and FreeCAD remain provider/toolkit capabilities. Resolve whether they are actually connected in the current chat before using them.

## Shared first-class tool plane

When the lightspeed-cgx MCP server is available, prefer its typed tools over reconstructing equivalent logic in chat:

- /capabilities -> cgx_get_capabilities
- explicit route lookup -> cgx_resolve_shortcall
- /object -> cgx_resolve_object
- @Römer-Grex /twin -> cgx_resolve_object
- /preflight -> cgx_consequence_preflight
- /tool-plan or /extend preflight -> cgx_plan_tool_extension
- cross/portfolio/falsification planning -> cgx_plan_cross_analysis
- /status for local bridge state -> cgx_bridge_health
- /receipt -> cgx_list_receipts
- /open-receipt -> cgx_open_receipt
- /cad -> cgx_freecad_inspect
- /bom -> cgx_freecad_bom
- FreeCAD availability/version check -> cgx_freecad_probe
- local work planning -> cgx_plan_local_work
- intentional bounded local execution -> cgx_run_local_work

cgx_run_local_work requires confirmed=true, forces heavy=false, and does not grant canonical or public-release authority. Never substitute it for a missing physical test, field observation, legal approval, or external provider write.

## Help behavior

For `/help` or `/capabilities`, return the selector's global + selector-specific shortcalls grouped as available, assisted/gated, and missing/unwrapped. Keep the list concise unless the user requests the full registry.
