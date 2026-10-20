---
name: project-strategy-report-advisor-team
description: "战略报告顾问。用于将冗长报告浓缩为高管可快速消化的精华摘要，节省每分钟。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-strategy-report-advisor"
  workbuddy_card: "战略报告顾问"
  workbuddy_category: "项目质量"
---

# 战略报告顾问

Use this skill as the routing entry point for 战略报告顾问 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-strategy-report-advisor-intake`
- `project-strategy-report-advisor-strategy`
- `project-strategy-report-advisor-execution`
- `project-strategy-report-advisor-quality`
- `project-strategy-report-advisor-measurement`
- `project-strategy-report-advisor-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 战略报告顾问 package, assemble the output set described in `references/workflow.md`.
