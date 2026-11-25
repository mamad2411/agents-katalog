---
name: legal-chinese-consulting-team
description: "中文法律咨询团。用于案情采集、法条研究、判例分析、建议撰写，为民事、婚姻、合同、劳动等高频场景出具专业法律咨询报告。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-chinese-consulting"
  workbuddy_card: "中文法律咨询团"
  workbuddy_category: "法务安全"
---

# 中文法律咨询团

Use this skill as the routing entry point for 中文法律咨询团 work. It packages the WorkBuddy 法务安全 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `case-intake`
- `statute-research`
- `case-analysis`
- `legal-advice`
- `document-drafting`
- `disclaimer-review`

## Output

Produce only the deliverables relevant to the request. For a full 中文法律咨询 package, assemble the output set described in `references/workflow.md`.
