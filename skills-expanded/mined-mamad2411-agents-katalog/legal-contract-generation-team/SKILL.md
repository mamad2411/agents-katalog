---
name: legal-contract-generation-team
description: >-
  从模板参考到风险审查再到专业合同文书输出的一站式合同生成工作流，覆盖劳动合同、保密协议、租赁合同、服务协议等主流合同类型。
---

# 合同生成

Use this skill as the routing entry point for the 合同生成 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide sections in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$employment-contract`
- `$legal-advisor`
- `$contract-review-pro`
- `$nathan-legal-os-pro`
- `$hetongzhushou`
- `$legal-doc-writer`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
