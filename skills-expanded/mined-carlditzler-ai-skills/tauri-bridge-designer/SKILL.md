---
name: tauri-bridge-designer
description: Use for Tauri frontend-backend boundaries: commands, events, state management, capabilities, plugin usage, config, typed payloads, and desktop-safe error handling between Rust and the frontend.
---

# Tauri Bridge Designer

## Use when
- the task involves `invoke`, commands, events, plugins, capabilities, config, or Rust-frontend integration
- the shape of the Tauri boundary affects correctness, security, or desktop UX
- the work needs typed contracts or bridge hardening before or during implementation

## Do not use when
- the change is purely frontend styling with no bridge impact
- the task is purely internal Rust logic with no Tauri boundary concern

## Working rules
- Treat each command as a real product API.
- Prefer typed request and response models over loose maps and stringly contracts.
- Keep permissions and capabilities least-privilege.
- Centralize frontend invoke wrappers and error mapping.
- Use events only when pub/sub semantics are genuinely required.

## Workflow
1. Decide whether the behavior belongs in frontend state, a Rust command, a plugin, or configuration.
2. Define typed inputs, outputs, and failure states before wiring UI.
3. Implement the Rust side with narrow responsibilities.
4. Implement a thin frontend client wrapper and product-level error handling.
5. Validate success, failure, cancellation, duplicate invocation, and unavailable-capability behavior.

## Quality bar
- No raw command names scattered through UI code.
- Serialization and versioning are deliberate.
- User-facing errors are safe and understandable.
- New capabilities do not widen filesystem, shell, network, or OS exposure casually.

## Reference routing
- Read `references/tauri-docs.md` for command, IPC, and config behavior.
- Read `references/rust-guidelines.md` for Rust-side API discipline.
- Read `references/release-quality-gates.md` when the bridge affects security, permissions, packaging, or release risk.

## Output contract
Provide:
- commands, contracts, or bridge boundaries changed
- frontend state or error-handling impact
- tests or validation added
- security or capability implications
- real remaining risks
