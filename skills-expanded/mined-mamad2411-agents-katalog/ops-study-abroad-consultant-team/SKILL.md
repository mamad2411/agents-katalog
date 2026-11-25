---
name: ops-study-abroad-consultant-team
description: "留学顾问。用于精通各国留学申请流程和院校信息。来源于 WorkBuddy 运营人力卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/运营人力/ops-study-abroad-consultant"
  workbuddy_card: "留学顾问"
  workbuddy_category: "运营人力"
---

# 留学顾问

Use this skill as the routing entry point for 留学顾问 work. It packages the WorkBuddy 运营人力 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `ops-study-abroad-consultant-intake`
- `ops-study-abroad-consultant-strategy`
- `ops-study-abroad-consultant-execution`
- `ops-study-abroad-consultant-quality`
- `ops-study-abroad-consultant-measurement`
- `ops-study-abroad-consultant-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 留学顾问 package, assemble the output set described in `references/workflow.md`.
