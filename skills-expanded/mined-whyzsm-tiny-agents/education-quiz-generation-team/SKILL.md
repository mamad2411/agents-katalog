---
name: education-quiz-generation-team
description: 从多题型自动生成（选择题/填空题/简答题/模拟考试/难度分级/题库管理）与中国中小学试卷生成（学科试卷/考点覆盖/格式规范）、教材同步智能出题（知识点讲解/智能出题/作业批改/解题答疑）与教学大纲考点提取（考点结构化/重要等级标注/题型匹配），到K12全学段举一反三练习生成（作业批改/错题分析/练习生成）与学习材料练习测试生成（闪卡/学习计划/计时模拟）的完整题库生成工作流。覆盖多题型生成、试卷组卷、智能出题、考点分析、练习生成、测试评估全链路。
---

# 题库生成

Use this skill as the routing entry point for the 题库生成 workflow. It coordinates the companion skills in this bundle instead of replacing them.

## Workflow

1. Read `references/guide.md` to classify the user request, required inputs, and expected deliverables.
2. Choose the smallest relevant companion skill set. For full-package requests, run the guide steps in order.
3. Preserve user-provided facts and mark assumptions explicitly. Ask only for missing inputs that block the next useful step.
4. Return concrete artifacts named by the guide, plus open questions, risks, and verification notes where relevant.

## Companion Skills

- `$quiz-creator`
- `$exam-generator`
- `$math-edu-assistant`
- `$exam-analyzer`
- `$k12-smart-teacher`
- `$exam`

## Output

Produce only the deliverables relevant to the matched workflow. For full-package requests, assemble the final output package described in `references/guide.md`.
