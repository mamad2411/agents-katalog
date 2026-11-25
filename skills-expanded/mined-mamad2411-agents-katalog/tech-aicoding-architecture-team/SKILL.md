---
name: tech-aicoding-architecture-team
description: "AICoding 架构专家团。用于复杂系统架构设计、资料摄入、调研、业务建模、系统设计、部署安全和用户故事交付。来源于 WorkBuddy 技术工程卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/technical-engineering/tech-aicoding-architecture"
  workbuddy_card: "AICoding 架构专家团"
---

# AICoding 架构专家团

Use this skill as the routing entry point for AICoding 架构专家团 work. It packages the WorkBuddy 技术工程 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target system, repository or cloud scope, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from the visible 技术工程 card metadata; no full expert-detail prompt was present in the local marketplace cache.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `context-ingestion`
- `architecture-research`
- `business-modeling`
- `system-design`
- `deployment-security`
- `user-story-delivery`
- `adr-package`

## Output

Produce only the deliverables relevant to the request. For a full AICoding 架构 package, assemble the output set described in `references/workflow.md`.
