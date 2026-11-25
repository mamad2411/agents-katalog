---
name: legal-contract-review-team
description: >-
  从基于CUAD数据集41个风险类别的法律合同分析（保密协议/SaaS协议/并购协议/雇佣协议/支付协议/寻源协议）与智能合同风险识别条款解读（多合同类型/法律咨询/合规管理），合同风险条款自动识别与缺失条款补充（差异条款对比/风险标注）与商业合同审查（NDA/MSA/SaaS协议/供应商合同/风险/缺失/合规），到合同关键信息提取与到期追踪（风险条款/关键信息/到期日）与合同文本提取审查（Word格式/金额条款/付款节点/违约金）的完整合同审查工作流。覆盖风险识别、条款解读、缺失补充、差异对比、关键提取、金额审查全链路。
---

# 合同审查

Use this skill as the routing entry point for the 合同审查 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide sections in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$contract-review`
- `$contract-risk-reviewer`
- `$audit-new`
- `$contract-reviewer`
- `$contract-guardian`
- `$contract-auditor`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
