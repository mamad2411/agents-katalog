---
name: project-technical-doc-engineer-team
description: "技术文档工程师。用于将复杂技术概念转化为清晰准确的文档，让技术知识可传播。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-technical-doc-engineer"
  workbuddy_card: "技术文档工程师"
  workbuddy_category: "项目质量"
---

# 技术文档工程师

Use this skill as the routing entry point for 技术文档工程师 work. It packages the WorkBuddy 项目质量 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `project-technical-doc-engineer-intake`
- `project-technical-doc-engineer-strategy`
- `project-technical-doc-engineer-execution`
- `project-technical-doc-engineer-quality`
- `project-technical-doc-engineer-measurement`
- `project-technical-doc-engineer-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 技术文档工程师 package, assemble the output set described in `references/workflow.md`.
