---
name: specialized-toolset-over-generic
description: |
  当需要使用专用工具集而非通用工具集时使用此 skill。适用于：代码审查场景、静态分析场景、动态上下文检索等场景。不适用于：通用编程任务。关键 trigger 信号：用户提到"专用工具"、"生产数据"、"工具优化"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: Core Value: Specialized Toolset > Generic Toolkit
tags: [specialized-toolset, production-data, tool-optimization]
related_skills: [agent-dynamic-decision-making]
---

# Specialized Toolset > Generic Toolkit（专用工具集优于通用工具集）

## R (Reading) — 原文引用

> "Scenario-tuned toolset: Distilled from deep analysis of tool-call traces in large-scale production data — including call frequency distributions, per-tool repetition rates, and the impact of new tools on the overall call chain — resulting in a purpose-built toolset that is more stable and predictable for code review than a generic agent toolkit."

## I (Interpretation) — 方法论骨架

**核心思想**: 从大规模生产数据的工具调用轨迹分析中提炼出的专用工具集，比通用 Agent 工具集更稳定、更可预测。

**关键原则**:
1. **生产数据分析**: 收集和分析大规模生产环境中的工具调用轨迹
2. **频率分布统计**: 统计每个工具的调用频率和重复率
3. **影响因子评估**: 评估新工具对整个调用链的影响
4. **专用工具集提炼**: 基于数据分析结果，选择最适合代码审查的工具组合

**与相邻 skill 的区分**: 
- 与 `agent-dynamic-decision-making` 的关系：Scenario-tuned toolset 是其具体实现之一
- 与 `template-engine-over-language-driven` 的区别：前者关注工具集选择，后者关注规则匹配

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 生产数据驱动的工具集优化
- **背景**: 分析大规模生产环境中的工具调用轨迹
- **方法**: 统计调用频率分布、每工具重复率、新工具对调用链的影响
- **应用**: 提炼出专为代码审查设计的工具集
- **结果**: 比通用 Agent 工具集更稳定、更可预测

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户需要"优化代码审查工具集"
- 用户遇到"通用工具集不稳定或不可预测"
- 用户希望"从生产数据中学习最佳实践"
- 用户需要"提高工具调用的效率和准确性"

**不应触发的场景**:
- 通用编程任务（如代码生成、调试等）
- 不需要专用工具集的简单任务
- 工具集本身已经优化的场景

**关键 trigger 词**: "专用工具"、"生产数据"、"工具优化"、"调用轨迹"、"稳定性"

## E (Execution) — 可执行步骤

1. **收集生产数据**: 记录工具调用轨迹数据（调用频率、重复率、影响因子等）
   - 完成标准: 轨迹数据集落盘，字段含调用频率、重复率、影响因子且样本量满足统计要求
2. **统计分析**: 分析调用频率分布、每工具重复率、新工具对调用链的影响
   - 完成标准: 输出三份统计结论：频率分布、逐工具重复率、新工具影响评估
3. **提炼专用工具集**: 基于数据分析结果，选择最适合代码审查的工具组合
   - 完成标准: 专用工具集清单定稿，每个取舍决定附数据依据
4. **集成测试**: 验证专用工具集的稳定性和可预测性
   - 完成标准: A/B 对比显示稳定性与可预测性指标优于通用工具集基线
5. **持续迭代**: 根据新的生产数据持续优化工具集
   - 完成标准: 建立数据回流机制，每次调整留存前后对比记录

**完成标准**: 专用工具集通过 A/B 测试，稳定性和可预测性显著优于通用方案

**判停条件**: 连续 5 次审查无工具集相关问题，调用效率提高 30% 以上

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 通用编程任务
- 不需要专用工具集的简单任务
- 工具集本身已经优化的场景

**作者盲点**:
- **数据依赖**: 需要大规模生产数据才能提炼出有效的专用工具集
- **平台限制**: 当前工具集主要针对特定平台，其他平台可能需要额外适配
- **维护成本**: 专用工具集需要持续维护和更新

**时代局限**:
- 当前架构基于现有 LLM 能力，未来可能需要调整
- 工具集优化依赖于当前的工具生态
