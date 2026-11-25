---
name: electron-ui-inspector
description: This skill should be used when building a live UI inspector for Electron apps so developers can click components, capture structured context, and hand that context to AI agents through parity-by-design human and agent paths.
---

# Electron UI Inspector

Ship canvas-style component handoff for Electron app development itself.

## When To Use

Use this skill when:
- You need click-to-inspect component context in an Electron renderer.
- Developers want to send live UI context to AI chat/agents for UI edits.
- You need both human and agent access to the same selected UI node.
- You are adding internal dev tooling (inspector, overlay, source mapping) in a running app.

## Core Principle

Always implement as one shared core path with two adapters:

- Human adapter: renderer overlay + panel
- Agent adapter: session-scoped read-only tools

Both must read from the same main-process inspector state to avoid drift.

## Implementation Workflow

1. Define shared contracts:
- Create a dedicated shared types module for inspector mode, state, and snapshot payload.
- Include selector, route, bounds, label, attributes, style subset, optional source mapping, and screenshot payload.

2. Implement main-process inspector service:
- Keep state in memory (`mode`, `snapshot`, `updatedAt`) scoped to workspace/window.
- Add `setMode`, `setSnapshot`, `clear`, `getState`, `subscribe`.
- Capture screenshots with bounds clamping and payload-size safeguards.

3. Add IPC and preload bridge:
- Register channels for get/set mode, set/clear snapshot, capture screenshot, and send-to-chat.
- Expose typed preload methods; renderer should never call raw IPC directly.
- Broadcast inspector state changes back to renderer windows.

4. Build renderer capture path:
- Add inspect overlay with hover highlight and click capture.
- Add snapshot capture utility that extracts:
  - stable selector fallback
  - label, text snippet, `outerHTML` (trimmed/redacted)
  - computed style allowlist
  - `data-*` attributes
  - ancestry/component path
- Add optional React fiber source extraction (best-effort, fail-soft).

5. Build renderer inspector panel:
- Show current selection summary and screenshot preview.
- Add actions: copy context, open file, reveal in folder, clear, send to chat.
- Let developers include/exclude HTML and styles before sending.

6. Wire chat handoff:
- Build a structured context block (`<vesper_ui_inspector_context> ... </vesper_ui_inspector_context>`).
- Inject through existing message send path (context prefix), not a separate execution path.

7. Add agent parity tools:
- Register session-scoped read-only inspector tools that proxy to main process.
- Add callback wiring from agent runtime to main-process inspector service.
- Mark inspector tools read-only in safe mode/permission policy.

8. Add runtime dev controls:
- Support runtime mount/unmount of inspector panel.
- Add discoverable developer UI entry point.
- Add shortcuts:
  - panel toggle shortcut
  - inspect mode shortcut

9. Validate end-to-end:
- Panel toggle works while app is running.
- Capture works on real renderer UI elements.
- Source metadata appears when available and fails soft otherwise.
- Send-to-chat injects expected context.
- Agent read-only tools return same selection state as panel.

## Guardrails

- Keep inspector dev-focused unless product requirements say otherwise.
- Budget payload size aggressively (trim HTML/text, whitelist styles, cap screenshot size).
- Redact sensitive fields (for example password inputs).
- Fail soft when no selection exists or source metadata is unavailable.
- Do not create separate human/agent state stores.

## References

- Implementation checklist: `references/implementation-checklist.md`
- Code map: `references/reference-code-map.md`
- Vesper planning doc: `references/vesper-ui-inspector-plan.md`
