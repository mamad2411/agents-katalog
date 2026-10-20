---
description: "Guard: dapat naka one_step_policy: true ang registry."
globs: [".cursor/commands/registry.yaml"]
alwaysApply: false
---

<rule>
name: registry_one_step_policy_guard
description: Warn if one_step_policy is off.
actions:
  - type: reject
    pattern: "one_step_policy:\\s*false"
    message: "Turn on one_step_policy: true to enforce single, deterministic suggestion."
  - type: suggest
    message: "Registry loaded. Ensure defaults.one_step_policy: true (single-step deterministic)."
</rule>
