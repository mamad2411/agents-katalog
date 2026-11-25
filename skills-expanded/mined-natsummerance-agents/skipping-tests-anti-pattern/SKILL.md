---
name: skipping-tests-anti-pattern
description: |
  当用户遇到跳过测试或先写代码后写测试导致的问题时调用此 skill。适用于代码质量下降、回归 bug 频发、测试覆盖率低的场景。不适用于：探索性编程、原型开发、一次性脚本。关键 trigger 信号："skip tests"、"code before tests"、"no tests"、"regression"、"test coverage low"、"bugs after deploy"。
source_book: 《Superpowers》 obra
source_project: obra/superpowers
source_chapter: The Basic Workflow / What's Inside
tags: [anti-pattern, testing, tdd, quality]
related_skills: ["test-first-philosophy"]
---

# Skipping Tests Anti-Pattern

## R (Reading) - 原文引用

> "test-driven-development - Activates during implementation. Enforces RED-GREEN-REFACTOR: write failing test, watch it fail, write minimal code, watch it pass, commit. Deletes code written before tests."

## I (Interpretation) - 方法论骨架

Skipping Tests Anti-Pattern 是 Superpowers 明确警示的反模式之一，指跳过测试或先写代码后写测试的行为。其核心问题是：

1. **跳过测试**：直接写实现代码，不写测试或事后补测试
2. **先写代码后写测试**：违反 TDD 原则，导致测试只是为了通过而写，无法真正保证质量
3. **删除在测试之前写的代码**：Superpowers 的严格做法是删除违规代码，强制重新按 TDD 流程执行

这种反模式的后果包括：代码质量下降、回归 bug 频发、测试覆盖率低、维护成本增加。Superpowers 通过强制执行 TDD 和删除违规代码来避免这个问题。

## A1 (Past Application) - 书中作者用过的案例

在 Superpowers 的基本工作流中，第 5 步明确说明：test-driven-development skill 会强制执行 RED-GREEN-REFACTOR 循环，并删除在测试之前写的代码。作者 Jesse Vincent 将这种行为列为必须避免的反模式，强调 TDD 是强制性的而不是可选的。

## A2 (Future Trigger) - 何时调用

**调用时机**：
- 用户遇到代码质量下降问题，怀疑是跳过测试导致的
- 用户遇到回归 bug 频发，测试覆盖率低
- 用户提到"skip tests"、"code before tests"、"no tests"、"regression"等关键词
- 用户需要了解为什么 TDD 应该是强制性的

**不调用时机**：
- 探索性编程：需要先尝试不同方案，TDD 可能过于严格
- 原型开发：快速验证想法，不需要完整测试
- 一次性脚本：不需要长期维护，TDD 成本过高

**与相邻 skill 的区分**：
- 与 `test-first-philosophy` 的关系：skipping-tests-anti-pattern 是反面警示；test-first-philosophy 是正面指导
- 与 `ad-hoc-debugging-anti-pattern` 的区别：skipping-tests 关注测试缺失；ad-hoc-debugging 关注调试方法不当

**关键 trigger 信号**：用户提到"skip tests"、"code before tests"、"no tests"、"regression"、"test coverage low"、"bugs after deploy"等关键词。

## E (Execution) - 可执行步骤

1. **识别问题**：确认是否存在跳过测试或先写代码后写测试的行为
   - 完成标准：已用提交历史或代码现状举证确认反模式存在与否，结论为二值判定

2. **评估影响**：分析这种行为对代码质量、回归 bug、测试覆盖率的影响
   - 完成标准：影响报告至少含覆盖率数字与回归 bug 个例各一项，均为可核查的数据

3. **删除违规代码**：如果先写了代码后写测试，删除代码重新按 TDD 流程执行
   - 完成标准：违规部分已从代码库移除（git 记录可查），仅保留测试文件作为行为规格

4. **重写测试**：按 RED-GREEN-REFACTOR 循环重新编写测试和代码
   - 完成标准：每个功能点都有"先红后绿"的提交顺序记录，重构后测试保持绿色

5. **验证修复**：运行测试套件，确认所有测试通过
   - 完成标准：全量测试套件一次通过，输出日志已留存

6. **预防措施**：建立自动化检查机制，防止再次出现跳过测试的行为
   - 完成标准：CI 或钩子中已配置覆盖率/测试门禁，且门禁在无测试提交时确实会拒绝合并

**判停条件**：所有违规代码已删除并重新按 TDD 流程执行，测试全部通过。

## B (Boundary) - 边界意识

**不适用的场景**：
- 探索性编程：需要先尝试不同方案，TDD 可能限制创造力
- 原型开发：快速验证想法，不需要完整测试
- 一次性脚本：不需要长期维护，TDD 成本过高

**作者的盲点**：
- **"删除代码"的极端性**：要求删除在测试之前写的代码可能过于严格，在某些情况下可能导致大量返工
- **TDD 学习曲线**：对于不熟悉 TDD 的开发者，强制执行可能导致初期效率低下
- **测试覆盖率 vs 速度**：严格的 TDD 可能降低开发速度，对于快速迭代的项目可能不适用
