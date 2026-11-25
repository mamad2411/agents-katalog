---
name: tencent-makers-development-team
description: "Makers 开发专家团。用于EdgeOne Makers 应用开发部署专家，覆盖前端、后端、AI Agent 与全球加速。来源于 WorkBuddy 腾讯专区卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/腾讯专区/tencent-makers-development"
  workbuddy_card: "Makers 开发专家团"
  workbuddy_category: "腾讯专区"
---

# Makers 开发专家团

Use this skill as the routing entry point for Makers 开发专家团 work. It packages the WorkBuddy 腾讯专区 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `frontend-build`
- `backend-api`
- `ai-agent-integration`
- `edgeone-deploy`
- `serverless-ops`
- `delivery-verification`

## Output

Produce only the deliverables relevant to the request. For a full Makers 开发 package, assemble the output set described in `references/workflow.md`.
