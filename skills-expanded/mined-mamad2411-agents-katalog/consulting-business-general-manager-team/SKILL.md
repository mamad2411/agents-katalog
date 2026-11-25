---
name: consulting-business-general-manager-team
description: "经营总管。用于经营总管调度四位领域专家，覆盖财务、营收、客户合规和运营，小企业管理一站搞定。来源于 WorkBuddy 行业顾问卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/行业顾问/consulting-business-general-manager"
  workbuddy_card: "经营总管"
  workbuddy_category: "行业顾问"
---

# 经营总管

Use this skill as the routing entry point for 经营总管 work. It packages the WorkBuddy 行业顾问 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `finance-control`
- `revenue-growth`
- `customer-compliance`
- `operations-management`
- `decision-dashboard`
- `action-tracking`

## Output

Produce only the deliverables relevant to the request. For a full 经营总管 package, assemble the output set described in `references/workflow.md`.
