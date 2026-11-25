---
name: csswitch-change-checks
description: Select bounded CSSwitch WIP or candidate checks after source, test, or Markdown changes; does not establish source closure.
---

# CSSwitch change checks

Use this Skill to select and report checks after an implementation, test, or documentation change. Read [代码作者规则](../../rules/code-authoring.md), [开发](../../../docs/operations/development.md), and [自动测试](../../../docs/operations/testing.md) before selecting evidence.

- In quick WIP mode, work from the requester’s declared goal and changed paths. Report the highest `F0`–`F3` risk, scope, suggested owning checks, evidence layer, and items not run. Do not guess a base or read untracked-file contents.
- In candidate or committed-range mode, require the requester to supply base and head. Report the resolved base, head, merge-base, and the committed, staged, unstaged, and untracked path layers; list untracked paths only.
- Do not turn a static-mapping miss into a lower risk. A focused PASS is not `SOURCE-GREEN`; use the single source-closure gate only under the conditions in the linked operations.
