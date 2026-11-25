---
name: review-question
description: 根据当前 profile 资料生成一道结构化复习题。用于 /review 中调用 review_answer 之前。
---

# Review Question

根据当前 profile、复习范围、难度和题型，生成且只生成一道题。

## 需要读取的资料

- `subject.md`：科目风格和考试目标。
- `knowledge_index.json`：知识点 ID、名称、常见误区、关联知识点、题型建议和难度基线。
- `cards/`：模式 1 中的概念卡片资料。
- `chapters/`：当前章节或小节的详细资料。
- `exam_points/`：可用时作为考试导向参考。
- `problem_templates/`：如果存在，优先作为数学、真题风格或深度训练题的生成依据。

生成题目前必须读取相关文件。如果资料缺失或含糊，说明缺失内容，不要编造。

## 输出契约

题目必须是可传给 `review_answer` 的 JSON 对象：

```json
{
  "type": "choice",
  "question_text": "题干",
  "options": ["A 选项", "B 选项", "C 选项", "D 选项"],
  "correct_answer": "A",
  "knowledge_points": ["kp_or_existing_id"],
  "difficulty": "S-U",
  "explanation_l1": "简短直接解析",
  "source_basis": "依据：第1章考点总结 / active_recall 卡片",
  "rubric_hint": "可选：简答、计算、证明题的判分要点",
  "related_knowledge_chain": ["可选", "关联", "知识点"]
}
```

支持的 `type`：

- `judgment`：判断题。可使用选项 `["正确", "错误"]`。
- `choice`：单选题。使用 3-5 个选项，推荐 4 个。
- `multi_choice`：多选题。必须让正确答案无歧义。
- `short_answer`：简答题，可省略 `options`。

当前代码层仍以这些 `type` 为主。数学、离散数学、论文阅读等深度题型可以先用 `short_answer` 承载，并在题干或 `rubric_hint` 中说明子风格：

- `calculation`：计算题，要求列步骤。
- `derivation`：推导题，要求说明关键变形。
- `proof`：证明题，要求写出证明主线。
- `step_diagnosis`：步骤诊断题，给出过程并要求找错或补全。
- `template_variant`：题型模板变式题，基于 `problem_templates/` 改写参数或场景。

## 质量规则

- 一题只考一个清晰概念、一个清晰的概念关系，或一个明确题型模板。
- 干扰项优先来自 profile 中的 `common_misconceptions`。
- 不要把正确答案或解析写进 `question_text`。
- 不要一次生成多道题。
- 必须填写 `source_basis`，说明题目依据的知识点、卡片、章节或考点总结。
- 如果使用 `problem_templates/`，`source_basis` 必须写明模板文件或模板名称。
- 对计算、推导、证明、步骤诊断题，必须给出可判分的 `correct_answer` 或 `rubric_hint`，不要只说“答案合理即可”。
- 尽量匹配指定难度；如果资料不足以支撑该难度，需要说明。
- 保持跨科目中立。只有当 profile 支持时，才使用代码、公式、案例或例句。

## 难度含义

- `S-R`：记忆或直接识别。
- `S-U`：单一概念，但需要区分细节。
- `M-U`：比较或连接 2-3 个相关概念。
- `M-A`：用多个概念分析场景。
- `C-A`：串联多个概念形成完整分析链。
