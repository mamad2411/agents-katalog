---
name: content-zhihu-strategist-team
description: "知乎策略师。用于精通知乎推荐机制和知识营销策略，通过高质量回答建立权威。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-zhihu-strategist"
  workbuddy_card: "知乎策略师"
  workbuddy_category: "内容创作"
---

# 知乎策略师

Use this skill as the routing entry point for 知乎策略师 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-zhihu-strategist-intake`
- `content-zhihu-strategist-strategy`
- `content-zhihu-strategist-execution`
- `content-zhihu-strategist-quality`
- `content-zhihu-strategist-measurement`
- `content-zhihu-strategist-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 知乎策略师 package, assemble the output set described in `references/workflow.md`.
