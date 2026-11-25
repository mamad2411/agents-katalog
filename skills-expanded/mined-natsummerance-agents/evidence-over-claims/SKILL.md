---
name: evidence-over-claims
description: |
  当用户需要验证 Bug 是否真的被修复、功能是否真正完成、或性能优化是否有效时调用此 skill。适用于 Bug 修复验证、功能完成确认、性能优化验证。不适用于：纯理论讨论、未实现的计划、无法量化的主观判断。关键 trigger 信号："verify"、"ensure fixed"、"actually works"、"evidence"、"proof"、"test passed"、"benchmark"。
source_book: 《Superpowers》 obra
source_project: obra/superpowers
source_chapter: What's Inside / Philosophy
tags: [principle, verification, evidence, debugging]
related_skills: ["test-first-philosophy", "ad-hoc-debugging-anti-pattern"]
---

# Evidence over Claims

## R (Reading) - 原文引用

> "verification-before-completion - Ensure it's actually fixed"

> "Philosophy: Evidence over claims - Verify before declaring success"

## I (Interpretation) - 方法论骨架

Evidence over Claims 是 Superpowers 的核心设计原则之一，强调基于证据而非声称来验证成功。其核心是：

1. **验证后再声明成功**：在宣布 Bug 已修复或功能已完成之前，必须有可重复的证据（如测试通过、基准测试数据）
2. **系统性验证**：不是凭感觉或一次性观察，而是通过系统性的方法（如自动化测试、基准测试）确保证据可靠
3. **防御性深度分析**：不仅验证表面现象，还要深入分析根因，确保问题不会复发

这种方法的优势在于：避免 Agent 过度自信导致的虚假成功声明，通过可重复的证据保证问题真正解决，通过系统性分析防止问题反复出现。

## A1 (Past Application) - 书中作者用过的案例

在 Superpowers 的 skills 库中，verification-before-completion 是一个独立的 skill，专门用于确保 Bug 真的被修复。作者 Jesse Vincent 将其列为核心哲学之一，强调"Verify before declaring success"，这与传统开发中"看起来修好了就提交"的做法形成鲜明对比。

## A2 (Future Trigger) - 何时调用

**调用时机**：
- 用户需要验证 Bug 是否真的被修复（而不是看起来修好了）
- 用户需要确认功能是否真正完成（而不是代码写完了）
- 用户需要验证性能优化是否有效（而不是凭感觉说变快了）
- 用户提到"verify"、"ensure fixed"、"actually works"、"evidence"、"proof"等关键词

**不调用时机**：
- 纯理论讨论：还没有实现，无法验证
- 未实现的计划：计划阶段不需要验证
- 无法量化的主观判断：如"代码更优雅了"这类主观评价

**与相邻 skill 的区分**：
- 与 `test-first-philosophy` 的区别：evidence-over-claims 关注验证成功；test-first-philosophy 关注测试先行
- 与 `systematic-debugging` 的关系：evidence-over-claims 是 systematic-debugging 的最后一步（验证修复）

**关键 trigger 信号**：用户提到"verify"、"ensure fixed"、"actually works"、"evidence"、"proof"、"test passed"、"benchmark"等关键词。

## E (Execution) - 可执行步骤

1. **明确验证目标**：确定要验证什么（Bug 修复、功能完成、性能优化等）
   - 完成标准：验证目标已被表述为可判定的命题（如"复现步骤不再触发错误"），而非模糊的"应该好了"

2. **设计验证方法**：选择合适的验证手段（自动化测试、手动测试、基准测试、代码审查等）
   - 完成标准：已确定一种以上可执行的验证手段，并写明每种的预期通过判据

3. **执行验证**：运行验证方法，收集证据
   - 完成标准：验证已实际运行并留下原始输出（测试日志、基准数据等），无凭记忆转述的证据

4. **分析证据**：确认证据是否支持成功声明（测试是否通过、性能是否提升等）
   - 完成标准：对每项判据给出"满足/不满足"的明确结论，不满足项已列出缺口

5. **记录结果**：将验证结果写入文档或日志，包括证据数据和结论
   - 完成标准：记录中同时含有原始证据与结论，第三方无需重跑即可复核

6. **用户确认**：向用户展示验证结果，询问是否接受
   - 完成标准：用户已看到证据并给出明确的接受/不接受答复，未获接受前不得声明成功

**判停条件**：验证通过且用户确认，或验证失败需要重新修复。

## B (Boundary) - 边界意识

**不适用的场景**：
- 纯理论讨论：还没有实现，无法验证
- 未实现的计划：计划阶段不需要验证
- 无法量化的主观判断：如"代码更优雅了"这类主观评价难以用证据量化

**作者的盲点**：
- **验证成本**：系统性验证可能需要额外的时间和资源，对于快速迭代的项目可能不适用
- **证据的可伪造性**：如果验证方法设计不当，可能产生误导性证据（如测试覆盖不全）
- **过度验证**：对于低风险变更，过度验证可能导致效率低下
