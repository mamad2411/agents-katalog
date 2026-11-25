---
name: consulting-super-partner-team
description: "超级合伙人。用于面向企业家和创业者的虚拟合伙人团队，先判断公司下一步，再给出可执行、可复盘的结果卡。来源于 WorkBuddy 行业顾问卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/行业顾问/consulting-super-partner"
  workbuddy_card: "超级合伙人"
  workbuddy_category: "行业顾问"
---

# 超级合伙人

Use this skill as the routing entry point for 超级合伙人 work. It packages the WorkBuddy 行业顾问 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `company-diagnosis`
- `next-step-strategy`
- `partner-collaboration`
- `execution-card`
- `review-mechanism`
- `automation-delivery`

## Output

Produce only the deliverables relevant to the request. For a full 超级合伙人 package, assemble the output set described in `references/workflow.md`.
