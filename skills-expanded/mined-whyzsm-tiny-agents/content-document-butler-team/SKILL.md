---
name: content-document-butler-team
description: "文档管家。用于支持新建、搜索、分类整理、分享授权和内容读取。来源于 WorkBuddy 内容创作卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/内容创作/content-document-butler"
  workbuddy_card: "文档管家"
  workbuddy_category: "内容创作"
---

# 文档管家

Use this skill as the routing entry point for 文档管家 work. It packages the WorkBuddy 内容创作 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `content-document-butler-intake`
- `content-document-butler-strategy`
- `content-document-butler-execution`
- `content-document-butler-quality`
- `content-document-butler-measurement`
- `content-document-butler-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 文档管家 package, assemble the output set described in `references/workflow.md`.
