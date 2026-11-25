---
name: project-reality-checker-team
description: "现实检查员。用于默认认为一切需要更多证据，需要压倒性证据才批准生产就绪。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-reality-checker"
  workbuddy_card: "现实检查员"
  workbuddy_category: "项目质量"
---

# 现实检查员

Use this skill as the routing entry point for 现实检查员 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-reality-checker-intake`
- `project-reality-checker-strategy`
- `project-reality-checker-execution`
- `project-reality-checker-quality`
- `project-reality-checker-measurement`
- `project-reality-checker-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 现实检查员 package, assemble the output set described in `references/workflow.md`.
