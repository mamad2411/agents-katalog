---
name: exam-prep
description: Generate practice exam questions from weak concepts. This skill should be used when the user says "exam-prep", "备考", "make practice questions", "generate a quiz", or is preparing for an exam in a specific course. Scans concept pages, prioritizes low-confidence ones, and writes a practice question set.
---

# Exam Prep — 出题

基于薄弱概念生成练习题。
Generate practice questions from weak concepts.

## 步骤 Steps

1. 读 `wiki/index.md` 找到目标课程的所有概念页
2. 读这些概念页的 frontmatter，按 `confidence` 排序（low 优先）
3. 为每个 low/medium 概念生成 1-2 道题
4. 保存到 `wiki/exam-prep/{course}.md`

## 题目类型 Question Types

混合以下类型，不要全是记忆题:
- **概念应用题**: 给一个场景，问该用哪个方法及原因
- **对比题**: 两个相关概念的区别和各自适用场景
- **推导题**（数学/ML课）: 要求推导或解释公式
- **攻防题**（安全课）: 给一个攻击，问防御措施，反之亦然
- **陷阱题**: 针对常见误解设计

## 页面格式 Page Format

```markdown
---
tags: [exam-prep, {course}]
generated: YYYY-MM-DD
based_on: [concept-pages]
---
# {课程} 练习题 Practice Questions

## Q1: {概念名} (confidence: low)
**题目**: ...
**参考答案**: ...
**相关页面**: [[concept]]
```

## 原则 Principles

- 优先 confidence:low 的概念
- 每题标注来自哪个概念页，方便回去复习
- 参考答案要完整，但鼓励用户先自己答
