---
name: project-document-generation-team
description: "专业文档生成团队。用于企业级长文档生成，4角色协作完成深度调研、大纲规划、内容撰写与合规审核全流程。来源于 WorkBuddy 项目质量卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/项目质量/project-document-generation"
  workbuddy_card: "专业文档生成团队"
  workbuddy_category: "项目质量"
---

# 专业文档生成团队

Use this skill as the routing entry point for 专业文档生成团队 work. It packages the WorkBuddy 项目质量 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `document-research`
- `outline-planning`
- `content-writing`
- `spec-normalization`
- `compliance-audit`
- `review-loop`

## Output

Produce only the deliverables relevant to the request. For a full 专业文档生成 package, assemble the output set described in `references/workflow.md`.
