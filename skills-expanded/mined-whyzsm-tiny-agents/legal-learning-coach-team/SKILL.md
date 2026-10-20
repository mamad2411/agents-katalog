---
name: legal-learning-coach-team
description: "法学学习教练。用于面向法学生的学习陪练，训练苏格拉底问答、案例摘要、IRAC、课程大纲和律考复习。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-learning-coach"
  workbuddy_card: "法学学习教练"
  workbuddy_category: "法务安全"
---

# 法学学习教练

Use this skill as the routing entry point for 法学学习教练 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-learning-coach-intake`
- `legal-learning-coach-strategy`
- `legal-learning-coach-execution`
- `legal-learning-coach-quality`
- `legal-learning-coach-measurement`
- `legal-learning-coach-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 法学学习教练 package, assemble the output set described in `references/workflow.md`.
