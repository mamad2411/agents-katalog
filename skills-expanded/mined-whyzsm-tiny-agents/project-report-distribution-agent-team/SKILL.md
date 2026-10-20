---
name: project-report-distribution-agent-team
description: "报告分发代理。用于自动化管理报告生成和分发流程。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-report-distribution-agent"
  workbuddy_card: "报告分发代理"
  workbuddy_category: "项目质量"
---

# 报告分发代理

Use this skill as the routing entry point for 报告分发代理 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-report-distribution-agent-intake`
- `project-report-distribution-agent-strategy`
- `project-report-distribution-agent-execution`
- `project-report-distribution-agent-quality`
- `project-report-distribution-agent-measurement`
- `project-report-distribution-agent-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 报告分发代理 package, assemble the output set described in `references/workflow.md`.
