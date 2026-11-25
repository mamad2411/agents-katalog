---
name: data-ai-engineer-team
description: "AI工程师。用于精通 ML 模型开发部署优化的全栈 AI 工程师，将 AI 从论文带到生产环境。来源于 WorkBuddy 数据智能卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/数据智能/data-ai-engineer"
  workbuddy_card: "AI工程师"
  workbuddy_category: "数据智能"
---

# AI工程师

Use this skill as the routing entry point for AI工程师 work. It packages the WorkBuddy 数据智能 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `data-ai-engineer-intake`
- `data-ai-engineer-strategy`
- `data-ai-engineer-execution`
- `data-ai-engineer-quality`
- `data-ai-engineer-measurement`
- `data-ai-engineer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full AI工程师 package, assemble the output set described in `references/workflow.md`.
