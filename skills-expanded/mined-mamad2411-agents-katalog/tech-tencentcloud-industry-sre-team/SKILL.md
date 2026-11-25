---
name: tech-tencentcloud-industry-sre-team
description: "腾讯云行业 SRE 专家团。用于按行业场景进行腾讯云巡检、可靠性治理、架构治理、事件响应和 SLO 风险评估。来源于 WorkBuddy 技术工程卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/technical-engineering/tech-tencentcloud-industry-sre"
  workbuddy_card: "腾讯云行业 SRE 专家团"
---

# 腾讯云行业 SRE 专家团

Use this skill as the routing entry point for 腾讯云行业 SRE 专家团 work. It packages the WorkBuddy 技术工程 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target system, repository or cloud scope, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from the visible 技术工程 card metadata; no full expert-detail prompt was present in the local marketplace cache.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `industry-sre-playbook`
- `cloud-inspection`
- `architecture-governance`
- `incident-response`
- `service-reliability`
- `industry-runbook`

## Output

Produce only the deliverables relevant to the request. For a full 腾讯云行业 SRE package, assemble the output set described in `references/workflow.md`.
