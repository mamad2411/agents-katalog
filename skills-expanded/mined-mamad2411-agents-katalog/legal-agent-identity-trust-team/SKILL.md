---
name: legal-agent-identity-trust-team
description: "智能体身份信任专家。用于构建 AI 智能体间的身份认证和信任机制。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-agent-identity-trust"
  workbuddy_card: "智能体身份信任专家"
  workbuddy_category: "法务安全"
---

# 智能体身份信任专家

Use this skill as the routing entry point for 智能体身份信任专家 work. It packages the WorkBuddy 法务安全 expert card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, scenario, source material, constraints, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata, not from a hidden expert-detail prompt.
5. Return concrete deliverables, evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-agent-identity-trust-intake`
- `legal-agent-identity-trust-strategy`
- `legal-agent-identity-trust-execution`
- `legal-agent-identity-trust-quality`
- `legal-agent-identity-trust-measurement`
- `legal-agent-identity-trust-handoff`

## Output

Produce only the deliverables relevant to the request. For a full 智能体身份信任专家 package, assemble the output set described in `references/workflow.md`.
