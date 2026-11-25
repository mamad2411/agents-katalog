---
name: legal-legal-research-team
description: >-
  从法律知识库检索（法律法规查询/合同条款检索/司法解释查找）与财税法律案例法规检索（税务判例/行政复议/税收法规/税务实践案例），官方API法条查询与多类纠纷检索（劳动纠纷/借贷纠纷/侵权纠纷/合同纠纷/工伤认定/婚姻家事/消费维权）与法条体系定位（上位规范/并列条款/下位细化/程序衔接/竞合分析），到类案检索验证（真实案例验证/裁判分歧/高频败诉原因/法官审查重点）与不确定法律概念深挖（合理期限/重大误解/明显不当/裁判标准/边界案例）的完整法规检索工作流。覆盖法规查询、案例检索、纠纷查找、体系定位、类案验证、概念分析全链路。
---

# 法规检索

Use this skill as the routing entry point for the 法规检索 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide sections in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$legalkb`
- `$case-research`
- `$legal-hybrid-skill`
- `$legal-system-mapper-mctmilk`
- `$legal-case-validator-mctmilk`
- `$legal-concept-deep-dive-mctmilk`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
