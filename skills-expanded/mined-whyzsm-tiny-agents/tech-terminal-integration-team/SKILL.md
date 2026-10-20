---
name: tech-terminal-integration-team
description: "终端集成专家。用于精通终端应用与空间计算环境的集成。来源于 WorkBuddy 技术卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/技术/tech-terminal-integration"
  workbuddy_card: "终端集成专家"
  workbuddy_category: "技术"
---

# 终端集成专家

Use this skill as the routing entry point for 终端集成专家 work. It packages the WorkBuddy 技术 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `tech-terminal-integration-intake`
- `tech-terminal-integration-strategy`
- `tech-terminal-integration-execution`
- `tech-terminal-integration-quality`
- `tech-terminal-integration-measurement`
- `tech-terminal-integration-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 终端集成专家 package, assemble the output set described in `references/workflow.md`.
