---
name: cgx-tool-extension
description: Extend Cognigrex/LightSpeed with a new shortcall, skill, typed adapter, provider, API, or assurance method without duplicating existing capabilities or creating a second runtime.
---

# CGX Tool Extension

Use for `/extend`, `/tool`, "add a capability", "make this callable", or equivalent requests.

Read `references/capabilities.json` and the canonical `toolkit_registry.json` first.

## Extension decision

1. Define the user goal and required inputs/outputs.
2. Search existing shortcalls, capability routes, toolkit entries, runtime functions, receipts, and connected providers.
3. If an existing capability already satisfies the goal:
   - reuse it,
   - add only an alias/shortcall or workflow skill when useful,
   - do not create another tool.
4. If a typed operation is genuinely missing:
   - implement the smallest typed LightSpeed adapter/function,
   - define bounded inputs and structured output/receipt,
   - add tests and failure cases,
   - register it once in the shared capability/toolkit registry.
5. Run cgx_plan_tool_extension when the shared lightspeed-cgx MCP plane is available. Reuse/alias an existing route whenever it is sufficient.
6. If first-class ChatGPT/Codex tool discovery is required, expose only the validated typed operation through the single shared CGX MCP tool plane. Do not create a separate MCP server per selector.
7. Rebuild selector packages and validate marketplace/client state.
8. Promotion remains subject to the existing Achilles/owner/LS GO gates.

## New skill rule

Create a skill only for a repeatable recognizable workflow: tool sequence, decision points, proof requirements, output contract, or domain procedure. Do not use a skill as a substitute for a deterministic function that should be code.

## New assurance/domain method

Declare:
- question answered,
- inputs/outputs,
- assumptions,
- applicability limits,
- evidence/provenance requirements,
- uncertainty/defeaters,
- receipt schema.

A method or capability never creates authority or converts simulated/derived output into physical evidence.

## Tool safety

Never expose a general-purpose command executor as a CGX tool. Prefer typed wrappers around existing runtime functions and host applications. Writes must state scope and gate. Heavy/local execution remains separately bounded by resource preflight.
