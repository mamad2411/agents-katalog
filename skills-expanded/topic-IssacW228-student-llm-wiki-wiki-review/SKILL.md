---
name: wiki-review
description: Feynman-technique review mode for studying. This skill should be used when the user says "review", "复习", "quiz me", "test my understanding", or names a course/concept they want to study. Quizzes the user, adjusts confidence based on answers, and generates practice questions for weak concepts.
---

# Wiki Review — 费曼复习

用费曼技巧测试理解。
Test understanding using the Feynman technique.

## 步骤 Steps

1. 读 `wiki/hot.md` 和 `wiki/index.md` 定位目标概念
2. 找 confidence:low/medium 的概念（优先复习薄弱的）
3. **费曼提问**: 像一个完全不懂的人一样提问，要求用户用最简单的语言解释
   - 不要问"是什么"，要问"为什么"和"如果...会怎样"
   - 追问到用户答不上来为止，找出理解的边界
4. **评估回答**:
   - 答得好且完整 → confidence 升级，更新 `last_reviewed`
   - 答得有漏洞 → 指出漏洞，解释正确理解，confidence 保持或降级
5. **更新页面**: 调整概念页的 `confidence` 和 `last_reviewed` 字段
6. **生成练习题**: 为仍然是 low 的概念，调用 exam-prep 逻辑生成题目到 `wiki/exam-prep/{course}.md`

## 费曼提问示例 Feynman Question Examples

- ❌ "什么是注意力机制？"（测记忆）
- ✅ "如果去掉 softmax 的缩放因子 √d_k 会发生什么？为什么？"（测理解）
- ✅ "用一个生活中的类比解释 Q、K、V 三个矩阵的作用"（测内化）

## 中英双语 Bilingual

提问和反馈都用中英双语，让用户用任一语言回答都可以。
