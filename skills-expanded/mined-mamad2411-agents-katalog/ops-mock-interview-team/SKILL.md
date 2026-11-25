---
name: ops-mock-interview-team
description: "面试模拟专家。用于模拟任意职位的真实面试官，覆盖技术产品销售人事等全岗位，逐题评分并给出建议。来源于 WorkBuddy 运营人力卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/运营人力/ops-mock-interview"
  workbuddy_card: "面试模拟专家"
  workbuddy_category: "运营人力"
---

# 面试模拟专家

Use this skill as the routing entry point for 面试模拟专家 work. It packages the WorkBuddy 运营人力 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `ops-mock-interview-intake`
- `ops-mock-interview-strategy`
- `ops-mock-interview-execution`
- `ops-mock-interview-quality`
- `ops-mock-interview-measurement`
- `ops-mock-interview-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 面试模拟专家 package, assemble the output set described in `references/workflow.md`.
