---
name: marketing-automotive-marketing-team
description: "汽车营销专家。用于精通用户选车购车决策，覆盖品牌营销、用户增长、车型分析、购车咨询等汽车服务。来源于 WorkBuddy 营销增长卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/营销增长/marketing-automotive-marketing"
  workbuddy_card: "汽车营销专家"
  workbuddy_category: "营销增长"
---

# 汽车营销专家

Use this skill as the routing entry point for 汽车营销专家 work. It packages the WorkBuddy 营销增长 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `marketing-automotive-marketing-intake`
- `marketing-automotive-marketing-strategy`
- `marketing-automotive-marketing-execution`
- `marketing-automotive-marketing-quality`
- `marketing-automotive-marketing-measurement`
- `marketing-automotive-marketing-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 汽车营销专家 package, assemble the output set described in `references/workflow.md`.
