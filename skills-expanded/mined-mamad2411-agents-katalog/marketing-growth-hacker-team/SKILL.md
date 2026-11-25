---
name: marketing-growth-hacker-team
description: "增长黑客。用于用数据驱动的实验方法论找到未开发的增长渠道，实现指数级增长。来源于 WorkBuddy 营销增长卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/营销增长/marketing-growth-hacker"
  workbuddy_card: "增长黑客"
  workbuddy_category: "营销增长"
---

# 增长黑客

Use this skill as the routing entry point for 增长黑客 work. It packages the WorkBuddy 营销增长 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `marketing-growth-hacker-intake`
- `marketing-growth-hacker-strategy`
- `marketing-growth-hacker-execution`
- `marketing-growth-hacker-quality`
- `marketing-growth-hacker-measurement`
- `marketing-growth-hacker-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 增长黑客 package, assemble the output set described in `references/workflow.md`.
