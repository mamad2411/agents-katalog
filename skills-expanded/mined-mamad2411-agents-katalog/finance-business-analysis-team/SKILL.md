---
name: finance-business-analysis-team
description: 从A股上市公司业绩快报数据获取到自动化财务分析、杜邦体系ROE拆解、预算执行差异分析，再到KPI决策仪表盘和智能图表生成的完整经营分析工作流。支持同比环比趋势分析、多维度KPI计算、预算vs实际差异识别和管理层决策简报输出。
---

# 经营分析

Use this skill as the routing entry point for the 经营分析 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$test-stock-performance-express`
- `$auto-data-analysis-claw`
- `$financial-roe-analysis`
- `$budget-vs-actual`
- `$business-intelligence`
- `$smart-charts`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
