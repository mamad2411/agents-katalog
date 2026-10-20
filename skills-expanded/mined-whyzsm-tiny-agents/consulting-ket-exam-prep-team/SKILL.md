---
name: consulting-ket-exam-prep-team
description: "KET备考专家团。用于剑桥认证考官领衔，为小学生提供 KET 全流程备考：学情测评、词汇语法地基、听说读写专项提升、考前冲刺模考。来源于 WorkBuddy 行业顾问卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/行业顾问/consulting-ket-exam-prep"
  workbuddy_card: "KET备考专家团"
  workbuddy_category: "行业顾问"
---

# KET备考专家团

Use this skill as the routing entry point for KET备考专家团 work. It packages the WorkBuddy 行业顾问 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `student-assessment`
- `vocabulary-grammar`
- `listening-speaking`
- `reading-writing`
- `mock-exam`
- `parent-coaching`

## Output

Produce only the deliverables relevant to the request. For a full KET备考 package, assemble the output set described in `references/workflow.md`.
