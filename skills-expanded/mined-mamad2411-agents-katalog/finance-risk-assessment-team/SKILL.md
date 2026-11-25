---
name: finance-risk-assessment-team
description: 覆盖信用风控建模、量化风险管理（VaR/压力测试/蒙特卡洛模拟）、财务欺诈识别、私募合规审查、仓位风控到风险仪表盘可视化的完整金融风控工作流。支持评分卡构建、决策树模型、特征工程分箱、投资组合风险分析及合规报告生成。
---

# 风控评估

Use this skill as the routing entry point for the 风控评估 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$fintech-risk-control`
- `$riskofficer`
- `$a-share-risk-alert`
- `$pe-compliance-expert-pro`
- `$position-risk-manager`
- `$quant-risk-dashboard`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
