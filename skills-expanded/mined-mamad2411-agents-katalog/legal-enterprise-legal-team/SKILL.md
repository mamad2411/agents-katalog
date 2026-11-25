---
name: legal-enterprise-legal-team
description: "企业法务专家团。用于面向企业法务的多角色专家团，覆盖合同、交易、隐私、产品、监管、AI治理、雇佣与知识产权分诊。来源于 WorkBuddy 法务安全卡片，并转换为 Codex 可安装的专家团入口格式。"
metadata:
  source: "workbuddy-expert-center/法务安全/legal-enterprise-legal"
  workbuddy_card: "企业法务专家团"
  workbuddy_category: "法务安全"
---

# 企业法务专家团

Use this skill as the routing entry point for 企业法务专家团 work. It packages the WorkBuddy 法务安全 expert-team card into a Codex skill entry that can live in this repository without installing WorkBuddy.

## Workflow

1. Read `references/guide.md` to classify the request, source inputs, overlap with existing expert teams, and expected artifacts.
2. Use the narrowest relevant capability module from the guide. For full-package requests, follow `references/workflow.md` in order.
3. Ask only for missing context that blocks a useful next output: target user, source material, business or legal boundary, data/file scope, quality bar, timeline, current evidence, or expected deliverable.
4. Keep WorkBuddy extraction provenance explicit: this package is converted from visible card metadata and available marketplace candidates, not from a hidden expert-detail prompt.
5. Return concrete deliverables, verification evidence where applicable, open questions, risks, confidence level, and next-step suggestions.

## Source Capability Modules

- `legal-intake`
- `contract-transaction`
- `privacy-data`
- `product-regulatory`
- `ai-governance`
- `employment-ip`

## Output

Produce only the deliverables relevant to the request. For a full 企业法务 package, assemble the output set described in `references/workflow.md`.
