---
name: hr-resume-screening-team
description: 从简历漏斗式量化评估（基础匹配度/能力匹配度/动机稳定匹配度）与结构化信息提取解析、四阶段一站式招聘流程（筛选→面试设计→面试评估→推荐）与JD自动匹配排序，到批量简历解析评分排名与循证面试策略设计的完整简历筛选工作流。覆盖简历解析、量化评估、人岗匹配、面试设计全链路。
---

# 简历筛选

Use this skill as the routing entry point for the 简历筛选 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$resume-screening`
- `$resume-parser`
- `$resume-screener-pro`
- `$easy-recruitment`
- `$applicant-screening-zh`
- `$interview-designer`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
