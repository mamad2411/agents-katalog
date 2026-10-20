---
name: academic-gaokao-expert-team
description: >-
  面向高考出分后的家庭决策场景，覆盖分数线与一分一段查询、位次判断、冲稳保志愿方案、院校与专业选择、专业背后的行业研究和企业调研，以及后续实习、校招、简历与面试准备。通过腾讯文档沉淀可协作的志愿表、调研报告和行动计划，并用简历与面试三方评估结果生成后续求职准备方案。
---

# 高考专家

Use this skill as the routing entry point for the 高考专家 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide sections in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$tencent-docs`
- `$tencent-yuanbao-gaokao-regional-passing-scores`
- `$tencent-yuanbao-gaokao-score-to-rank-lookup`
- `$gaokao-tool`
- `$business-writing`
- `$resume-interview-3party-optimizer`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
