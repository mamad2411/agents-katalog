---
name: project-api-testing-team
description: "API测试专家。用于在用户之前发现 API 的每一个缺陷，确保接口稳定性和正确性。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-api-testing"
  workbuddy_card: "API测试专家"
  workbuddy_category: "项目质量"
---

# API测试专家

Use this skill as the routing entry point for API测试专家 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-api-testing-intake`
- `project-api-testing-strategy`
- `project-api-testing-execution`
- `project-api-testing-quality`
- `project-api-testing-measurement`
- `project-api-testing-handoff`

## Output

Produce only the deliverables relevant to the request. For a full API测试专家 package, assemble the output set described in `references/workflow.md`.
