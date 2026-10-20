---
name: design-prototype-handoff-team
description: 设计原型专家团。用于从 Figma JSON、UI 截图、设计描述或组件规格出发，完成设计转代码、截图转代码、无障碍审查、设计评审、设计交付、设计系统管理、用户研究综合和 UX 文案优化。来源于 WorkBuddy design-to-code 团队能力，并转换为 Codex 可安装的专家团入口格式。
metadata:
  source: workbuddy-cb-teams-marketplace/design-to-code
---

# 设计原型专家团

Use this skill as the routing entry point for design-to-code, prototype handoff, design system, and UX polish work. It packages the WorkBuddy design-to-code team workflow into a Codex skill entry instead of requiring the WorkBuddy plugin to be installed.

## Workflow

1. Read `references/guide.md` to classify the source material, target framework, and expected deliverables.
2. Use the narrowest relevant WorkBuddy capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. If the user provides Figma, ask for a frame/component JSON export when no direct design connector is available. If the user provides a screenshot, verify that the image path is accessible.
4. Prefer accessible, production-ready output: semantic HTML, keyboard behavior, ARIA where needed, tokenized styles, responsive breakpoints, and documented states.
5. Return concrete artifacts: component code, design critique, handoff spec, design-system notes, accessibility findings, UX copy, or blockers.

## Source Capability Modules

- `design-to-code-workflows`
- `accessibility-review`
- `design-critique`
- `design-handoff`
- `design-system`
- `research-synthesis`
- `user-research`
- `ux-copy`

## Output

Produce only the deliverables relevant to the request. For a full design prototype handoff package, assemble the output set described in `references/workflow.md`.
