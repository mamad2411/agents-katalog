---
name: project-experiment-tracking-manager-team
description: "实验追踪管理者。用于系统化管理实验全生命周期，确保每个实验有假设有执行有结论。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-experiment-tracking-manager"
  workbuddy_card: "实验追踪管理者"
  workbuddy_category: "项目质量"
---

# 实验追踪管理者

Use this skill as the routing entry point for 实验追踪管理者 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-experiment-tracking-manager-intake`
- `project-experiment-tracking-manager-strategy`
- `project-experiment-tracking-manager-execution`
- `project-experiment-tracking-manager-quality`
- `project-experiment-tracking-manager-measurement`
- `project-experiment-tracking-manager-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 实验追踪管理者 package, assemble the output set described in `references/workflow.md`.
