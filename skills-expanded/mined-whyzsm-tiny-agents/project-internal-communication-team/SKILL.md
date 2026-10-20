---
name: project-internal-communication-team
description: "内部沟通专家。用于提供状态报告、领导汇报、公司简报、FAQ 和事故报告等沟通模板。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-internal-communication"
  workbuddy_card: "内部沟通专家"
  workbuddy_category: "项目质量"
---

# 内部沟通专家

Use this skill as the routing entry point for 内部沟通专家 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-internal-communication-intake`
- `project-internal-communication-strategy`
- `project-internal-communication-execution`
- `project-internal-communication-quality`
- `project-internal-communication-measurement`
- `project-internal-communication-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 内部沟通专家 package, assemble the output set described in `references/workflow.md`.
