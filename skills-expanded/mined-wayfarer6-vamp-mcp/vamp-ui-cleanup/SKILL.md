---
name: vamp-ui-cleanup
description: Simplify VAMP VS Code webviews and user-facing MCP copy while preserving automation controls, accessibility and installation warnings. Use for UI text translation, redundant controls and layout cleanup.
---

# VAMP UI cleanup

1. Locate the webview generator, message handlers and existing UI tests. List the element IDs consumed by scripts before removing markup.
2. Use concise English product text. Keep status, errors, permission requirements and recovery actions visible. Preserve language-recognition patterns; they are not product copy.
3. Keep one primary action for each task. Move manual recovery, environment reset and diagnostics into a labeled disclosure. Remove duplicate guide links and implementation prose from the main flow.
4. Preserve VS Code theme variables, keyboard focus, accessible labels, narrow layouts and live status announcements. Hide unsupported host/backend options; do not advertise unimplemented features.
5. Preserve the guest setup warning: wait for setup completion before locking or suspending the guest. Describe display settings as best effort unless verified. Do not present input delivery as successful installation.
6. Test the generated HTML with mocked webview messages. Cover loading, ready, busy, missing dependency and failure states. Verify stable IDs, event wiring and disabled controls, especially shared HTTP server Start/Stop.

Use static fixtures for layout checks. UI editing does not authorize creating or controlling a VM. Honor an existing automation pause. Report changed controls and actual validation separately from untested guest behavior.
