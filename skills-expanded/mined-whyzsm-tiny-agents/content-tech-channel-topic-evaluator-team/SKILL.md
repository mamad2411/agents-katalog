---
name: content-tech-channel-topic-evaluator-team
description: "科技频道选题评估师。用于双层级4维评分与5方向对比，输出评分详情、硬源清单和风险提示。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-tech-channel-topic-evaluator"
  workbuddy_card: "科技频道选题评估师"
  workbuddy_category: "内容创作"
---

# 科技频道选题评估师

Use this skill as the routing entry point for 科技频道选题评估师 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-tech-channel-topic-evaluator-intake`
- `content-tech-channel-topic-evaluator-strategy`
- `content-tech-channel-topic-evaluator-execution`
- `content-tech-channel-topic-evaluator-quality`
- `content-tech-channel-topic-evaluator-measurement`
- `content-tech-channel-topic-evaluator-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 科技频道选题评估师 package, assemble the output set described in `references/workflow.md`.
