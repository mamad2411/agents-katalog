---
name: tech-mvp-development-team
description: "MVP 开发专家团。用于需求挖掘、竞品调研、三文档产出、Spec 锁定、前后端并行开发、自检、测试部署和用户反馈迭代。来源于 WorkBuddy 技术工程卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/technical-engineering/tech-mvp-development"
  workbuddy_card: "MVP 开发专家团"
---

# MVP 开发专家团

Use this skill as the routing entry point for MVP 开发专家团 work. It packages the WorkBuddy 技术工程 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target system, repository or cloud scope, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from the visible 技术工程 card metadata; no full expert-detail prompt was present in the local marketplace cache.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `requirement-discovery`
- `competitive-research`
- `three-doc-package`
- `spec-lock`
- `frontend-backend-build`
- `test-deploy`
- `user-feedback-loop`

## Output

Produce only the deliverables relevant to the request. For a full MVP 开发 package, assemble the output set described in `references/workflow.md`.
