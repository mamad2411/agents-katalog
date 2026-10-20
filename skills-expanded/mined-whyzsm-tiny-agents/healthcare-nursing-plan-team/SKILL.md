---
name: healthcare-nursing-plan-team
description: 从护理研究理论支持论证（理论选择/文献检索/护理科研开题）与临床护理支持系统（文档记录/患者沟通/护理计划制定），阿尔茨海默症专病照护（疾病认知/日常照护/安全管理/沟通技巧/行为管理/照护者支持）与慢性病主动健康监测（Apple
  Health整合/模式识别/异常预警/患者照护），到复杂损伤高级康复方案（生物特征分析/神经营养/物理治疗/恢复优化）与医学信息通俗化转译（复杂医学摘要/患者友好/照护者可读/科学性保持）的完整护理方案工作流。覆盖理论支撑、临床护理、专病照护、健康监测、康复方案、通俗转译全链路。
---

# 护理方案

Use this skill as the routing entry point for the 护理方案 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$nursing-theory-matcher`
- `$nurse`
- `$alzheimer-care`
- `$nurse-monistor-pathway`
- `$bio-reabilita-z`
- `$lay-summary-gen`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
