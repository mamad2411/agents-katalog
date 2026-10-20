---
name: finance-financial-report-analysis-team
description: 从A股/美股财务数据获取到三表深度解读、财务造假识别再到专业分析报告自动生成的完整财报分析工作流。支持利润表、资产负债表、现金流量表的全面解析，覆盖盈利能力、资产质量、现金流健康度等核心维度。
---

# 财报分析

Use this skill as the routing entry point for the 财报分析 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$tushare-data`
- `$marketpulse`
- `$earnings-reader`
- `$financial-fraud-index`
- `$finance-report-analyzer`
- `$financial-report-analysis`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
