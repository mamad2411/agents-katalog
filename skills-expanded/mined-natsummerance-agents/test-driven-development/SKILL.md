---
name: test-driven-development
description: |
  当用户询问"如何证明代码正确"、"测试应该什么时候写"或"如何确保代码质量"时调用此 skill。不适用于：纯理论讨论、不需要验证的场景、探索性编程。关键 trigger 信号：测试、TDD、证明、验证、RED-GREEN-REFACTOR、tests are proof。
source_book: Agent Skills Addy Osmani
source_project: addyosmani/agent-skills
source_chapter: Commands table / VERIFY phase + auto-build description
tags: [tdd, testing, verification, red-green-refactor]
related_skills: ["spec-driven-development", "auto-build-mode", "faster-is-safer"]
---

# SKILL.md - Test-Driven Development（测试驱动开发）

## R (Reading) - 原文引用

> "/test | Prove it works | Tests are proof"
> 
> "every task is still test-driven and committed individually"

## I (Interpretation) - 方法论骨架

**核心思想**：测试是证明，不是可选的。每个任务都是测试驱动的，遵循 RED-GREEN-REFACTOR 循环。这种方法确保代码正确性有可验证的证据支持，而不是凭感觉声明成功。

**关键要素**：
1. **Tests are proof**: 测试作为证据，证明代码按预期工作
2. **Test-driven**: 每个任务都先写测试再写实现
3. **Committed individually**: 每个任务单独提交，便于追溯

## A1 (Past Application) - 书中作者用过的案例

Agent Skills 的 `/test` 命令对应 VERIFY 阶段，强调"Tests are proof"。Addy Osmani 在描述 `/build auto` 模式时特别指出："every task is still test-driven and committed individually"，即使在自动化模式下也不跳过测试环节。

这种设计确保 AI agents 在自主工作时仍然保持测试驱动的习惯，保证代码质量。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户不确定如何证明代码正确
- 用户想建立测试驱动的开发习惯
- 用户遇到回归 bug 频发的问题
- 用户想知道测试在开发流程中的位置

**与相邻 skill 的区分**：
- 与 `spec-driven-development` 的区别：test-driven-development 关注**代码正确性验证**（写代码时），而 spec-driven-development 关注**需求明确化**（写代码前）。两者互补：先明确需求，再测试驱动实现。
- 与 `auto-build-mode` 的区别：test-driven-development 是手动编写测试和实现，而 auto-build-mode 是自动生成计划并实现（但仍保留测试驱动）。前者更灵活，后者更高效。

## E (Execution) - 可执行步骤

1. **写失败测试（RED）**
   - 根据规格说明编写测试用例
   - 运行测试确认它失败
   - 确保测试覆盖核心功能和边缘情况
   - 完成标准: 测试运行结果为失败（RED），且用例同时覆盖核心功能与边缘情况

2. **写最少代码让它通过（GREEN）**
   - 只写能让测试通过的最少代码
   - 不要过度设计或添加额外功能
   - 运行测试确认它通过
   - 完成标准: 目标测试全部转为通过且代码中无超出测试要求的功能

3. **重构（REFACTOR）**
   - 在测试保护下优化代码结构
   - 确保重构后测试仍然通过
   - 提高代码可读性和可维护性
   - 完成标准: 重构提交后测试套件保持全绿

4. **单独提交**
   - 每个任务完成后单独提交
   - 提交信息清晰描述变更内容
   - 便于追溯和回滚
   - 完成标准: 一个任务对应一次提交，提交信息能定位到对应任务

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯理论讨论（不涉及实际代码）
- 快速原型验证（不需要长期维护）
- 一次性脚本（不需要测试保障）
- 探索性编程（TDD 可能过于严格）

**作者的盲点**：
- Addy Osmani 假设所有任务都适合测试驱动，但实际上某些场景（如 UI 调整、配置修改）可能不适合
- agent-skills 缺少对测试覆盖率目标的具体指导
- 没有提到如何选择测试框架或编写高质量的测试用例
