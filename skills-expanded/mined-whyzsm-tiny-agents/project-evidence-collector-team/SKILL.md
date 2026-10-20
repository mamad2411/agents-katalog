---
name: project-evidence-collector-team
description: "证据收集员。用于不放过任何没有截图证据的问题，用视觉证据确保缺陷无处遁形。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-evidence-collector"
  workbuddy_card: "证据收集员"
  workbuddy_category: "项目质量"
---

# 证据收集员

Use this skill as the routing entry point for 证据收集员 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-evidence-collector-intake`
- `project-evidence-collector-strategy`
- `project-evidence-collector-execution`
- `project-evidence-collector-quality`
- `project-evidence-collector-measurement`
- `project-evidence-collector-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 证据收集员 package, assemble the output set described in `references/workflow.md`.
