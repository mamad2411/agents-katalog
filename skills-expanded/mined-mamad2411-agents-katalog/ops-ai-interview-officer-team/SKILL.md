---
name: ops-ai-interview-officer-team
description: "AI面谈官。用于提供九大智能面谈大纲与线上实时指引，基于云录制自动生成结构化纪要与待办。来源于 WorkBuddy 运营人力卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/运营人力/ops-ai-interview-officer"
  workbuddy_card: "AI面谈官"
  workbuddy_category: "运营人力"
---

# AI面谈官

Use this skill as the routing entry point for AI面谈官 work. It packages the WorkBuddy 运营人力 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `ops-ai-interview-officer-intake`
- `ops-ai-interview-officer-strategy`
- `ops-ai-interview-officer-execution`
- `ops-ai-interview-officer-quality`
- `ops-ai-interview-officer-measurement`
- `ops-ai-interview-officer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full AI面谈官 package, assemble the output set described in `references/workflow.md`.
