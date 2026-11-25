---
name: data-databrain-sentiment-team
description: "DataBrain舆情分析专家。用于面向口碑与舆情侦察，覆盖评分告警、内容趋势、竞品对比与热点挖掘。来源于 WorkBuddy 数据智能卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/数据智能/data-databrain-sentiment"
  workbuddy_card: "DataBrain舆情分析专家"
  workbuddy_category: "数据智能"
---

# DataBrain舆情分析专家

Use this skill as the routing entry point for DataBrain舆情分析专家 work. It packages the WorkBuddy 数据智能 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `data-databrain-sentiment-intake`
- `data-databrain-sentiment-strategy`
- `data-databrain-sentiment-execution`
- `data-databrain-sentiment-quality`
- `data-databrain-sentiment-measurement`
- `data-databrain-sentiment-handoff`

## Output

Produce only the deliverables relevant to the request. For a full DataBrain舆情分析专家 package, assemble the output set described in `references/workflow.md`.
