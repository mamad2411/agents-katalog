---
name: content-kuaishou-strategist-team
description: "快手策略师。用于深谙快手下沉市场特性和老铁文化，打造接地气的内容策略。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-kuaishou-strategist"
  workbuddy_card: "快手策略师"
  workbuddy_category: "内容创作"
---

# 快手策略师

Use this skill as the routing entry point for 快手策略师 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-kuaishou-strategist-intake`
- `content-kuaishou-strategist-strategy`
- `content-kuaishou-strategist-execution`
- `content-kuaishou-strategist-quality`
- `content-kuaishou-strategist-measurement`
- `content-kuaishou-strategist-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 快手策略师 package, assemble the output set described in `references/workflow.md`.
