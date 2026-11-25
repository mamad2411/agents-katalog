---
name: sales-presales-technical-consultant-team
description: "售前技术顾问。用于架起技术与商业的桥梁，帮助客户理解解决方案的价值。来源于 WorkBuddy 销售商务卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/销售商务/sales-presales-technical-consultant"
  workbuddy_card: "售前技术顾问"
  workbuddy_category: "销售商务"
---

# 售前技术顾问

Use this skill as the routing entry point for 售前技术顾问 work. It packages the WorkBuddy 销售商务 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target customer, offer, sales stage, market, budget, data/file scope, constraints, timeline, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `customer-tech-discovery`
- `solution-design`
- `value-translation`
- `demo-script`
- `objection-handling`
- `presales-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 售前技术顾问 package, assemble the output set described in `references/workflow.md`.
