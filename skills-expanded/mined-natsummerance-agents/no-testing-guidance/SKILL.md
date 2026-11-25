---
name: no-testing-guidance
description: |
  当用户完成项目后不确定代码是否正确、养成"先写代码后测试"的坏习惯，或遇到回归 bug 频发时调用此 skill。不适用于：纯理论讨论、不需要验证的场景。关键 trigger 信号：测试、TDD、回归 bug、代码质量、验证正确性、先写代码。
source_book: App Ideas Collection Florin Pop
source_project: florinpop17/app-ideas
source_chapter: N/A (absence of content)
tags: [anti-pattern, testing-gap, tdd-absence, code-quality]
related_skills: ["no-systematic-methodology", "no-progress-tracking"]
---

# SKILL.md - No Testing Guidance（缺少测试指导）

## R (Reading) - 原文引用

> (README 中完全没有提到测试、TDD 或代码质量保障)

## I (Interpretation) - 方法论骨架

**核心问题**：App Ideas Collection 完全没有提供任何关于测试、TDD 或代码质量保障的指导。学习者可能构建了功能完整的应用，但缺乏验证正确性的方法，容易养成"先写代码后测试"的坏习惯。

**反模式特征**：
1. **跳过测试**：学习者直接写代码，不写测试或最后才补测试
2. **无法验证正确性**：没有明确的标准来判断代码是否"正确"
3. **回归 bug 频发**：修改代码后引入新问题，因为没有测试保护
4. **代码质量下降**：缺乏测试导致重构困难，技术债务累积

**根本原因**：app-ideas 假设"能跑就是正确的"，但没有教导学习者如何系统性验证代码的正确性。

## A1 (Past Application) - 书中作者用过的案例

App Ideas Collection 的 89 个项目都没有提供任何测试相关的指导：
- 没有提到 TDD 或 RED-GREEN-REFACTOR 循环
- 没有提供测试用例或验收标准
- 没有建议如何使用测试框架（如 Jest、pytest 等）

这种缺失导致学习者可能完成了 Weather App 或 Calculator，但不知道如何验证边缘情况或确保代码质量。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户完成项目后不确定代码是否正确
- 用户养成"先写代码后测试"的坏习惯
- 用户遇到回归 bug 频发的问题
- 用户想学习如何系统性验证代码的正确性
- 用户想知道为什么测试很重要

**与相邻 skill 的区分**：
- 与 `no-systematic-methodology` 的区别：no-testing-guidance 是**具体的技术盲点**（缺少测试指导），而 no-systematic-methodology 是**整体框架的缺失**。前者更具体，后者更宏观。
- 与 `no-progress-tracking` 的区别：no-testing-guidance 关注**代码质量的验证**，而 no-progress-tracking 关注**学习进度的量化**。两者互补：一个确保代码正确，一个确保技能提升。

## E (Execution) - 可执行步骤

1. **识别反模式症状**
   - 询问用户是否写了测试
   - 检查用户是否有回归 bug 的问题
   - 评估用户的代码质量意识
   - 完成标准：三项检查均有明确回答，并判定用户处于"无测试/事后补测/有测试但不覆盖边缘"中的哪一档

2. **引入测试优先思维**
   - 解释 TDD 的核心价值：先写失败测试，再写最少代码让它通过
   - 强调测试不是"额外工作"，而是开发流程的必要部分
   - 提供简单的测试示例（如 Calculator 的加法测试）
   - 完成标准：用户能复述 RED-GREEN 的先后顺序及其理由，并亲手跑通一个最小测试示例

3. **建立测试习惯**
   - 为每个新功能先写测试用例
   - 使用测试框架自动化验证
   - 定期运行测试套件确保没有回归
   - 完成标准：用户当前项目已接入测试框架，新功能均有先行的测试用例，且测试套件可在本地一键运行并通过

4. **避免常见陷阱**
   - 不要等到项目完成才写测试
   - 不要只测试"快乐路径"，要测试边缘情况
   - 不要因为测试失败而沮丧，这是正常的 RED-GREEN 循环
   - 完成标准：用户的测试用例中至少包含一个边缘情况（如空输入/非法输入），且对失败测试能按循环流程处理而非放弃

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯理论讨论（不涉及实际代码）
- 快速原型验证（不需要长期维护）
- 一次性脚本（不需要测试保障）
- 探索性编程（TDD 可能过于严格）

**作者的盲点**：
- Florin Pop 假设"能跑就是正确的"，但没有教导学习者如何系统性验证代码
- app-ideas 缺少对测试、TDD 和代码质量保障的任何提及
- 这种"功能优先于质量"的思路可能导致学习者养成坏习惯，在真实工作环境中难以适应
