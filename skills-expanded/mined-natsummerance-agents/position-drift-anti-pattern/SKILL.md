---
name: position-drift-anti-pattern
description: |
  当需要识别和避免位置漂移反模式时使用此 skill。适用于：代码审查报告生成、问题定位等场景。不适用于：不需要精确定位的场景。关键 trigger 信号：用户提到"位置不准"、"行号漂移"、"文件引用错误"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: The Problem with General-Purpose Agents — Position Drift
tags: [anti-pattern, position-drift, accuracy]
related_skills: [deterministic-engineering-hard-constraints]
---

# Position Drift Anti-Pattern（位置漂移反模式）

## R (Reading) — 原文引用

> "Position drift — Reported issues frequently don't match the actual code location, with line numbers or file references drifting off target."
>
> "The root cause: a purely language-driven architecture lacks hard constraints on the review process."

## I (Interpretation) — 方法论骨架

**核心思想**: 通用 Agent 报告的审查问题经常与实际代码位置不匹配，行号或文件引用发生漂移，根本原因是纯语言驱动架构缺乏独立的定位模块。

**关键特征**:
1. **行号漂移**: 报告的问题行号与实际代码行号不一致
2. **文件引用错误**: 报告的问题指向错误的文件
3. **根本原因**: 缺乏独立的外部定位模块

**解决方案**:
- **External positioning module**: 独立的评论定位模块，基于 AST 解析和行号计算
- **Comment reflection**: 独立的评论反思模块，二次验证位置准确性

**与相邻 skill 的区分**: 
- 与 `incomplete-coverage-anti-pattern` 的区别：前者关注位置不准确，后者关注文件覆盖不全
- 与 `unstable-quality-anti-pattern` 的区别：前者关注位置精度，后者关注质量稳定性

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 内部代码审查系统优化
- **背景**: 通用 Agent 报告的问题位置经常不准确
- **问题**: 开发者需要手动查找实际问题位置，降低审查效率
- **应用**: 引入 External positioning module + Comment reflection
- **结果**: 位置准确性显著提高，开发者无需手动查找问题位置

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户抱怨"报告的问题位置不准确"
- 用户发现"行号或文件引用漂移"
- 用户遇到"需要手动查找实际问题位置"
- 用户需要"确保审查报告的位置精确"

**不应触发的场景**:
- 不需要精确定位的场景（如整体架构建议）
- 纯文本分析任务
- 位置信息不重要的场景

**关键 trigger 词**: "位置不准"、"行号漂移"、"文件引用错误"、"定位不准确"、"外部定位"

## E (Execution) — 可执行步骤

1. **识别风险**: 检查是否存在位置漂移问题
   - 完成标准: 给出是否存在漂移的结论，并附至少一条问题位置与实际代码不符的实例证据（或证明无漂移）
2. **分析原因**: 确认是否是纯语言驱动架构导致的位置漂移
   - 完成标准: 归因结论成文，指明是否缺乏独立定位模块
3. **应用外部定位**: 引入 External positioning module，基于 AST 解析和行号计算
   - 完成标准: 定位模块上线，报告中的文件路径与行号均来自 AST 计算结果而非模型生成
4. **二次验证**: 使用 Comment reflection 模块二次验证位置准确性
   - 完成标准: 抽样复核报告中每条问题的位置，命中实际代码位置的比率达到约定阈值
5. **验证效果**: 检查报告的位置是否与实际代码位置一致
   - 完成标准: 连续抽样比对显示报告位置与实际代码位置一致率 100%

**完成标准**: 所有报告的问题位置与实际代码位置一致，无漂移

**判停条件**: 连续 10 次审查无位置漂移问题

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 不需要精确定位的场景
- 纯文本分析任务
- 位置信息不重要的场景

**作者盲点**:
- **AST 解析依赖**: 需要支持多种编程语言的 AST 解析器
- **性能开销**: 外部定位模块可能增加审查时间
- **复杂代码处理**: 对于宏、模板元编程等复杂代码，定位可能仍有困难

**时代局限**:
- 当前架构基于现有 AST 解析能力，未来可能需要调整
- 定位精度依赖于对编程语言语法的理解
