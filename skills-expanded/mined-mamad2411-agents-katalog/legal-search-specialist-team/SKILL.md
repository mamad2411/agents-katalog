---
name: legal-search-specialist-team
description: "法律检索专家。用于识别检索意图与场景，按法源位阶检索法规与类案，验证效力评估相似度。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-search-specialist"
  workbuddy_card: "法律检索专家"
  workbuddy_category: "法务安全"
---

# 法律检索专家

Use this skill as the routing entry point for 法律检索专家 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-search-specialist-intake`
- `legal-search-specialist-strategy`
- `legal-search-specialist-execution`
- `legal-search-specialist-quality`
- `legal-search-specialist-measurement`
- `legal-search-specialist-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 法律检索专家 package, assemble the output set described in `references/workflow.md`.
