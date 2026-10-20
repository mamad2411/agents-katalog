---
name: marketing-search-term-analyst-team
description: "搜索词分析师。用于深度分析搜索词数据，挖掘用户真实搜索意图。来源于 WorkBuddy 营销增长卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/营销增长/marketing-search-term-analyst"
  workbuddy_card: "搜索词分析师"
  workbuddy_category: "营销增长"
---

# 搜索词分析师

Use this skill as the routing entry point for 搜索词分析师 work. It packages the WorkBuddy 营销增长 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `marketing-search-term-analyst-intake`
- `marketing-search-term-analyst-strategy`
- `marketing-search-term-analyst-execution`
- `marketing-search-term-analyst-quality`
- `marketing-search-term-analyst-measurement`
- `marketing-search-term-analyst-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 搜索词分析师 package, assemble the output set described in `references/workflow.md`.
