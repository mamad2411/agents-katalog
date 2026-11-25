---
name: education-student-assessment-team
description: 从教师评估工具箱（评分标准Rubric设计/评估方案/学生反馈/课堂评价）与评分标准差距分析（草稿对标/差距识别/提分计划），错题归类与知识点定位（薄弱环节分析/复习建议/知识图谱）与K12全学段作业批改（错题分析/举一反三/九大学科），到学员成长档案管理（学情记录/家长反馈/咨询留档）与成绩单家长评语生成（作业评语/校园沟通/温暖得体）的完整学生评估工作流。覆盖评估设计、标准分析、错题诊断、作业批改、档案管理、评语生成全链路。
---

# 学生评估

Use this skill as the routing entry point for the 学生评估 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$teacher-assistant`
- `$rubric-gap-analyzer`
- `$error-analysis`
- `$k12-smart-teacher`
- `$student-growth-ops`
- `$xueersi-parent-comment`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
