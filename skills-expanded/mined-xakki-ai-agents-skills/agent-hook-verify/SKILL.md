---
name: agent-hook-verify
description: 'Verify agent hook registration and behavior with safe allow/block cases. Use after changing hook configuration or when a hook does not fire. RU: проверка хуков, настройки агента.'
---

# Test agent configuration

Discover the active runtime's actual hooks, permissions and supported configuration interface. Inspect a hook for side effects before executing it. Verify both expected block and expected allow behavior with isolated, representative inputs; distinguish an isolated script test, static configuration lint and an actual runtime registration test. A green script or valid configuration alone does not prove a hook is active or that a permission policy is enforced.

For Claude Code specifically, the bundled hook test and settings linter use Claude's event schema and exit semantics. Use the [Claude-specific workflow](references/claude.md) and its conditional [event reference](reference.md) only for that runtime; do not infer compatibility with another agent. For other runtimes, use their documented test interfaces and report unverified capabilities.

Choose harmless probes appropriate to the runtime and authorization, preserve user configuration, and avoid live side effects. Report the exact scope, outcomes and untested enforcement boundaries.

For lifecycle notification hook controls and safe verification, see
[notification hooks](references/notification-hooks.md).
