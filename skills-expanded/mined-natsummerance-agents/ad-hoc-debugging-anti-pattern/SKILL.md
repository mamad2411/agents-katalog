---
name: ad-hoc-debugging-anti-pattern
description: |
  当用户遇到凭猜测调试而不是系统性根因追踪导致的问题时调用此 skill。适用于 Bug 反复出现、修复后问题依旧、调试效率低的场景。不适用于：简单语法错误、编译错误、明显的逻辑错误。关键 trigger 信号："guessing"、"ad-hoc debugging"、"root cause"、"systematic debugging"、"bug keeps coming back"、"fix didn't work"。
source_book: 《Superpowers》 obra
source_project: obra/superpowers
source_chapter: What's Inside / Philosophy
tags: [anti-pattern, debugging, systematic, root-cause]
related_skills: ["evidence-over-claims"]
---

# Ad-hoc Debugging Anti-Pattern

## R (Reading) - 原文引用

> "systematic-debugging - 4-phase root cause process (includes root-cause-tracing, defense-in-depth, condition-based-waiting techniques)"

> "Philosophy: Systematic over ad-hoc - Process over guessing"

## I (Interpretation) - 方法论骨架

Ad-hoc Debugging Anti-Pattern 是 Superpowers 明确警示的反模式之一，指凭猜测调试而不是系统性根因追踪的行为。其核心问题是：

1. **凭猜测调试**：没有系统性方法，凭直觉或经验猜测问题所在
2. **临时性修复**：只解决表面现象，不深入根因，导致问题反复出现
3. **缺乏防御性深度分析**：没有多层次的分析，容易被假象误导

Superpowers 通过 systematic-debugging skill 提供 4 阶段根因追踪流程来避免这个问题：
- **Phase 1: Root Cause Tracing** - 追踪问题的根本原因，而非表面症状
- **Phase 2: Defense in Depth** - 多层次分析，确保不是假象
- **Phase 3: Condition-Based Waiting** - 基于条件的等待技术，避免竞态条件
- **Phase 4: Verification** - 验证修复是否真正解决问题

## A1 (Past Application) - 书中作者用过的案例

在 Superpowers 的 skills 库中，systematic-debugging 是一个独立的 skill，专门用于系统性调试和根因追踪。作者 Jesse Vincent 将其列为核心哲学之一，强调"Systematic over ad-hoc - Process over guessing"，这与传统开发中"试一下这个、试一下那个"的做法形成鲜明对比。

## A2 (Future Trigger) - 何时调用

**调用时机**：
- 用户遇到 Bug 反复出现，修复后问题依旧
- 用户调试效率低，凭猜测尝试不同方案
- 用户提到"guessing"、"ad-hoc debugging"、"root cause"、"systematic debugging"等关键词
- 用户需要了解为什么系统性调试比凭猜测更有效

**不调用时机**：
- 简单语法错误：编译器已经明确指出问题，不需要系统性调试
- 编译错误：错误信息清晰，直接修复即可
- 明显的逻辑错误：一眼就能看出的问题，不需要复杂分析

**与相邻 skill 的区分**：
- 与 `evidence-over-claims` 的关系：ad-hoc-debugging-anti-pattern 是反面警示；evidence-over-claims 是正面指导（验证后再声明成功）
- 与 `skipping-tests-anti-pattern` 的区别：ad-hoc-debugging 关注调试方法不当；skipping-tests 关注测试缺失

**关键 trigger 信号**：用户提到"guessing"、"ad-hoc debugging"、"root cause"、"systematic debugging"、"bug keeps coming back"、"fix didn't work"等关键词。

## E (Execution) - 可执行步骤

1. **识别问题**：确认是否存在凭猜测调试的行为
   - 完成标准：已列举出至少一处"未经验证即改动"的具体行为证据，或确认不存在该反模式

2. **启动 4 阶段根因追踪**：
   - **Phase 1: Root Cause Tracing** - 从症状追溯到根本原因，绘制调用链和数据流
   - **Phase 2: Defense in Depth** - 多层次分析，检查日志、监控、测试数据等多维度证据
   - **Phase 3: Condition-Based Waiting** - 如果涉及并发或异步，使用基于条件的等待技术避免竞态条件
   - **Phase 4: Verification** - 设计验证实验，确认根因假设是否正确
   - 完成标准：四个 Phase 各有产出物（调用链图/多维证据清单/等待策略/验证实验结果），且验证实验能复现并消除问题

3. **制定修复方案**：基于根因分析制定修复方案，而非临时性修补
   - 完成标准：方案中每条修改都能对应到已确认的根因，不存在无法溯源到根因的"顺手改"

4. **执行修复**：按方案执行修复，同时更新相关测试
   - 完成标准：方案内修改全部落地，新增/更新的测试覆盖该根因场景

5. **验证修复**：运行验证实验，确认问题真正解决
   - 完成标准：验证实验通过且原复现步骤不再触发问题，连续多次执行结果一致

6. **记录根因**：将根因分析和修复方案写入文档，防止类似问题再次出现
   - 完成标准：文档包含症状、根因、修复方案、预防措施四要素，并已同步到团队可访问的位置

**判停条件**：根因已找到且修复验证通过，或用户明确要求停止。

## B (Boundary) - 边界意识

**不适用的场景**：
- 简单语法错误：编译器已经明确指出问题，不需要系统性调试
- 编译错误：错误信息清晰，直接修复即可
- 明显的逻辑错误：一眼就能看出的问题，不需要复杂分析

**作者的盲点**：
- **4 阶段流程的学习成本**：对于不熟悉系统性调试的开发者，4 阶段流程可能需要时间适应
- **过度分析风险**：对于简单问题，使用完整的 4 阶段流程可能过于繁琐
- **时间成本**：系统性调试可能比凭猜测花费更多时间，对于紧急 hotfix 可能不适用
