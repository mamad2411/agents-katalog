---
name: data-deep-research-team
description: "深度研究团队。用于深度研究报告输出，7角色5阶段聚合多源信息，经审稿修订循环输出带引用的专业报告。来源于 WorkBuddy 数据智能卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-cb-teams-marketplace/deep-research"
  workbuddy_card: "深度研究团队"
  workbuddy_category: "数据智能"
---

# 深度研究团队

Use this skill as the routing entry point for 深度研究团队 work. It packages the WorkBuddy 数据智能 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `research-planning`
- `multi-source-search`
- `evidence-synthesis`
- `draft-writing`
- `editor-review`
- `citation-delivery`

## Output

Produce only the deliverables relevant to the request. For a full 深度研究 package, assemble the output set described in `references/workflow.md`.
