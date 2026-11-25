---
name: data-intelligence-analysis-team
description: "智数分析专家团。用于6人AI数据分析团队，擅长自然语言转SQL、Python建模、RAG知识问答、仪表盘可视化与报告生成。来源于 WorkBuddy 数据智能卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-cb-teams-marketplace/data"
  workbuddy_card: "智数分析专家团"
  workbuddy_category: "数据智能"
---

# 智数分析专家团

Use this skill as the routing entry point for 智数分析专家团 work. It packages the WorkBuddy 数据智能 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `nl-to-sql`
- `python-modeling`
- `rag-qa`
- `data-validation`
- `dashboard-visualization`
- `insight-reporting`

## Output

Produce only the deliverables relevant to the request. For a full 智数分析 package, assemble the output set described in `references/workflow.md`.
