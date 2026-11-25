---
name: project-jira-workflow-admin-team
description: "Jira工作流管理员。用于精通 Jira 配置和敏捷工作流设计，让工具真正服务于团队效率。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-jira-workflow-admin"
  workbuddy_card: "Jira工作流管理员"
  workbuddy_category: "项目质量"
---

# Jira工作流管理员

Use this skill as the routing entry point for Jira工作流管理员 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-jira-workflow-admin-intake`
- `project-jira-workflow-admin-strategy`
- `project-jira-workflow-admin-execution`
- `project-jira-workflow-admin-quality`
- `project-jira-workflow-admin-measurement`
- `project-jira-workflow-admin-handoff`

## Output

Produce only the deliverables relevant to the request. For a full Jira工作流管理员 package, assemble the output set described in `references/workflow.md`.
