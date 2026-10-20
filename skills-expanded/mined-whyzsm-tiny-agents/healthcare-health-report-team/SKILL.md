---
name: healthcare-health-report-team
description: 从全维度健康管理与中西医融合（运动训练/饮食营养/健康数据追踪/中医体质辨识/节气养生）与结构化健康摘要报告生成（体征/症状/药物/生活方式数据汇总），健康数据深度分析（睡眠质量/运动恢复/健康趋势/数据查询）与体检报告通俗解读（异常项标注/紧急程度/随访问题/可能含义），到个人健康档案记录（体征数据/结构化记录/每日总结/风险分级）与健康数据跟踪管理（血压/心率/运动/用药/症状分析/健康建议）的完整健康报告工作流。覆盖健康管理、报告生成、数据分析、体检解读、档案记录、跟踪管理全链路。
---

# 健康报告

Use this skill as the routing entry point for the 健康报告 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. For healthcare or finance work, present outputs as informational analysis unless the user supplies licensed-professional context; clearly flag urgent/high-risk findings and recommend qualified professional review when appropriate.
5. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$healthfit-cn`
- `$health-report`
- `$health-score-pro`
- `$health-checkup-report`
- `$personal-health-journal`
- `$health-manager`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
