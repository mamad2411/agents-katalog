---
name: project-workflow-optimizer-team
description: "工作流优化专家。用于找到瓶颈修复流程并自动化一切，让团队效率最大化。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-workflow-optimizer"
  workbuddy_card: "工作流优化专家"
  workbuddy_category: "项目质量"
---

# 工作流优化专家

Use this skill as the routing entry point for 工作流优化专家 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-workflow-optimizer-intake`
- `project-workflow-optimizer-strategy`
- `project-workflow-optimizer-execution`
- `project-workflow-optimizer-quality`
- `project-workflow-optimizer-measurement`
- `project-workflow-optimizer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 工作流优化专家 package, assemble the output set described in `references/workflow.md`.
