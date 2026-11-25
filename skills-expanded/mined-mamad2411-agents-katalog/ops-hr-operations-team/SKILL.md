---
name: ops-hr-operations-team
description: "HR 运营团队。用于人力资源管理流程化，招聘筛选、薪酬体系设计、组织发展与 HR 运营流程化管理，助力企业人才战略落地。来源于 WorkBuddy 运营人力卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/运营人力/ops-hr-operations"
  workbuddy_card: "HR 运营团队"
  workbuddy_category: "运营人力"
---

# HR 运营团队

Use this skill as the routing entry point for HR 运营团队 work. It packages the WorkBuddy 运营人力 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `recruiting-screening`
- `compensation-analysis`
- `org-development`
- `hr-process`
- `talent-strategy`
- `hr-ops-dashboard`

## Output

Produce only the deliverables relevant to the request. For a full HR 运营 package, assemble the output set described in `references/workflow.md`.
