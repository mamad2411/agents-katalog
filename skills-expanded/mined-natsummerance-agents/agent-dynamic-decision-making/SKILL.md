---
name: agent-dynamic-decision-making
description: |
  当需要 Agent 进行动态决策和动态上下文检索时使用此 skill。适用于：场景化提示模板生成、专用工具集选择等需要灵活性的场景。不适用于：文件选择、规则匹配、位置定位等需要硬约束的场景。关键 trigger 信号：用户提到"动态决策"、"上下文检索"、"提示优化"、"工具选择"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: Core Design: Deterministic Engineering × Agent Hybrid — Agent Section
tags: [agent-hybrid, dynamic-decision, scenario-tuned]
related_skills: [specialized-toolset-over-generic]
---

# Agent Dynamic Decision-Making（Agent 动态决策）

## R (Reading) — 原文引用

> "The agent's strengths are concentrated where they matter most — dynamic decisions and dynamic context retrieval."
>
> "Scenario-tuned toolset: Distilled from deep analysis of tool-call traces in large-scale production data."

## I (Interpretation) — 方法论骨架

**核心思想**: Agent 的优势在于动态决策和动态上下文检索，应将其集中在这些领域发挥最大价值。

**关键组件**:
1. **Scenario-tuned prompts**: 深度优化的代码审查提示模板，提高效率并减少 token 消耗
2. **Scenario-tuned toolset**: 从大规模生产数据的工具调用轨迹分析中提炼出的专用工具集

**与相邻 skill 的区分**: 
- 与 `deterministic-engineering-hard-constraints` 的区别：前者负责动态决策（需要灵活性），后者负责硬约束（不能出错）
- 与 `specialized-toolset-over-generic` 的关系：Scenario-tuned toolset 是专用工具集优于通用工具集的具体实现

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 生产数据驱动的工具集优化
- **背景**: 分析大规模生产环境中的工具调用轨迹
- **方法**: 统计调用频率分布、每工具重复率、新工具对整个调用链的影响
- **应用**: 提炼出专为代码审查设计的工具集
- **结果**: 比通用 Agent 工具集更稳定、更可预测

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户需要"优化提示模板以提高效率"
- 用户遇到"工具选择不当导致审查质量下降"
- 用户希望"从生产数据中学习最佳实践"
- 用户需要"动态上下文检索支持深度审查"

**不应触发的场景**:
- 需要硬约束的场景（如文件选择、规则匹配、位置定位）
- 纯确定性算法可以解决的问题
- 不需要灵活性的简单任务

**关键 trigger 词**: "动态决策"、"上下文检索"、"提示优化"、"工具选择"、"生产数据"

## E (Execution) — 可执行步骤

1. **分析生产数据**: 收集工具调用轨迹数据，统计调用频率、重复率、影响因子
   - 完成标准: 产出覆盖全部工具的调用统计表，含频率、重复率、影响因子三项数值
2. **提炼专用工具集**: 基于数据分析结果，选择最适合代码审查的工具组合
   - 完成标准: 工具集清单定稿，每个入选或剔除的工具都有对应的数据依据记录
3. **优化提示模板**: 为不同审查场景设计深度优化的提示模板
   - 完成标准: 每个目标审查场景至少有一份对应提示模板并通过试运行验证
4. **集成测试**: 验证专用工具集和提示模板的有效性
   - 完成标准: A/B 对比报告显示效率与准确性两项指标均不低于通用方案基线
5. **持续迭代**: 根据新的生产数据持续优化工具集和提示模板
   - 完成标准: 有固定复盘周期，且每轮迭代留存前后指标对比记录

**完成标准**: 专用工具集和提示模板通过 A/B 测试，效率和准确性显著优于通用方案

**判停条件**: 连续 5 次审查无工具集相关问题，token 消耗降低 30% 以上

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 需要硬约束的场景（文件选择、规则匹配、位置定位）
- 纯确定性算法可以解决的问题
- 不需要灵活性的简单任务

**作者盲点**:
- **数据依赖**: 需要大规模生产数据才能提炼出有效的专用工具集
- **平台限制**: 当前工具集主要针对特定平台，其他平台可能需要额外适配
- **维护成本**: 专用工具集需要持续维护和更新

**时代局限**:
- 当前架构基于现有 LLM 能力，未来可能需要调整
- 工具集优化依赖于当前的工具生态
