# Execution Module

This directory owns the execution capability pack: shell commands, background
processes, code REPL, computer use, and screenshot tools.

- All tool implementations, helpers, and tests live here.
- This is a high-risk capability surface — treat changes carefully.
- Follow the `web-access/` and `filesystem/` directories as layout references.
- This module owns the Python/Node REPL lifecycle and wrapper protocol
  (`repl-session.ts`, `code-wrappers.ts`). `code_exec` and manifest runners
  use session-bound REPLs. Core accesses the neutral `CodeRunner` protocol;
  it does not import execution implementations.
- Long-lived REPLs and background process groups bind their cleanup to the
  scoped session environment that launched them. Session teardown must stop
  those resources before their inherited credential environment can outlive
  its authorization boundary.
- Agent-routed shell, process, and REPL execution must carry the machine
  authority path into the shared fail-closed OS sandbox in
  `src/core/agent-harness/machine-authority-sandbox.ts`. Text parsing cannot
  establish where opaque code writes; keep direct runner calls available for
  host-owned tests and operations, but every harness/loop execution context
  supplies the protected path. Canonical and workspace conversation stores carry
  directory read/write denials through resolved aliases; REPL reuse must retain
  the same sandbox identity.
- Scope policy treats recognized outbound commands and code as compound local
  plus network effects. Keep the execution tool resolvers and Claude Bash on
  the shared opaque-execution classifier; never replace the local write check
  with a network-only classification.
- GUI coordinate actions use one explicit convention: `screenshot` records
  native capture size, displayed image size, and display-to-native scale
  factors; `computer_use` coordinate actions must choose `coordinate_space:
  "native"` or `"last_screenshot_display"`. Browser full-page and element
  screenshots are visual artifacts, not desktop coordinate maps, unless a
  future implementation proves and reports a native transform.
