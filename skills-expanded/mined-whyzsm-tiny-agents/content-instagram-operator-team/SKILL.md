---
name: content-instagram-operator-team
description: "Instagram运营专家。用于精通 Instagram 视觉美学和内容策略，打造令人向往的品牌形象。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-instagram-operator"
  workbuddy_card: "Instagram运营专家"
  workbuddy_category: "内容创作"
---

# Instagram运营专家

Use this skill as the routing entry point for Instagram运营专家 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-instagram-operator-intake`
- `content-instagram-operator-strategy`
- `content-instagram-operator-execution`
- `content-instagram-operator-quality`
- `content-instagram-operator-measurement`
- `content-instagram-operator-handoff`

## Output

Produce only the deliverables relevant to the request. For a full Instagram运营专家 package, assemble the output set described in `references/workflow.md`.
