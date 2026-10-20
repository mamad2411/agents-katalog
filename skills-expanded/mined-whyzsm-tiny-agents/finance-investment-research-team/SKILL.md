---
name: finance-investment-research-team
description: 从A股/美股实时行情数据获取到个股基本面深度研究、行业分析、DCF估值建模，再到自动生成专业投研报告PDF的完整投研工作流。覆盖买方基金经理视角的个股分析简报、投行级行业研究报告、价值投资估值框架，支持技术分析与交易信号输出。
---

# 投研报告

Use this skill as the routing entry point for the 投研报告 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$ai-stock-analyst`
- `$investlog-ai`
- `$stock-research-engine`
- `$industry-research-analyst`
- `$valuation-analysis`
- `$finance-research-report`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
