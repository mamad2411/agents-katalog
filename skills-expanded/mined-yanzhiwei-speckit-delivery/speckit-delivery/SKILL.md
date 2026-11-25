---
name: speckit-delivery
description: 启动 Speckit Delivery 的手动 SDD 路由。
disable-model-invocation: true
---

# Spec Kit Delivery

Use the installed `speckit.delivery.route` command with the user's request.
In Codex Skills mode, that installed command is a skill named
`speckit-delivery-route` under an active skills root (for example
`$CODEX_HOME/skills/speckit-delivery-route/SKILL.md` or
`.agents/skills/speckit-delivery-route/SKILL.md`). Read and execute that skill
instead of checking for a `speckit*` executable on PATH. Other hosts render
the same extension command through their native surface: Claude Code uses
`/speckit-delivery-route`, OpenCode uses `/speckit.delivery.route`, and generic
adapters use the rendered command file. Do not rely on `Get-Command`,
`which`, or PATH lookup as the installed-command check for any of these hosts.
The extension command is the canonical cross-integration owner of lane
routing, ADR lifecycle, Ralph orchestration, and completion conditions.

The native skill is a convenience surface only. Preserve the selected project's
existing workflow and report a missing Delivery extension as an installation
blocker only when neither the rendered extension command nor the matching
Codex skill entry is available. Do not publish, push, merge, or create external
resources unless the user separately authorized that action.
