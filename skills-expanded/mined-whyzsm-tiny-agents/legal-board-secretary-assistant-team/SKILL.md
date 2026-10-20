---
name: legal-board-secretary-assistant-team
description: "董秘助手。用于面向公告、路演、投资者问答、互动回复和沟通稿，在对外使用前做合规审查。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-board-secretary-assistant"
  workbuddy_card: "董秘助手"
  workbuddy_category: "法务安全"
---

# 董秘助手

Use this skill as the routing entry point for 董秘助手 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-board-secretary-assistant-intake`
- `legal-board-secretary-assistant-strategy`
- `legal-board-secretary-assistant-execution`
- `legal-board-secretary-assistant-quality`
- `legal-board-secretary-assistant-measurement`
- `legal-board-secretary-assistant-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 董秘助手 package, assemble the output set described in `references/workflow.md`.
