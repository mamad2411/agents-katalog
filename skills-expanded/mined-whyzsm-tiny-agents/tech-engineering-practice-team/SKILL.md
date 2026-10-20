---
name: tech-engineering-practice-team
description: "工程实践专家。用于基于 Google 工程师的 Agent Skills，覆盖规范驱动开发、代码评审、CI/CD 发布。来源于 WorkBuddy 技术卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/技术/tech-engineering-practice"
  workbuddy_card: "工程实践专家"
  workbuddy_category: "技术"
---

# 工程实践专家

Use this skill as the routing entry point for 工程实践专家 work. It packages the WorkBuddy 技术 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `tech-engineering-practice-intake`
- `tech-engineering-practice-strategy`
- `tech-engineering-practice-execution`
- `tech-engineering-practice-quality`
- `tech-engineering-practice-measurement`
- `tech-engineering-practice-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 工程实践专家 package, assemble the output set described in `references/workflow.md`.
