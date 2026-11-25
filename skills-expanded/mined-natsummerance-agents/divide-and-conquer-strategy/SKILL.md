---
name: divide-and-conquer-strategy
description: |
  当需要处理大型代码变更集时使用此 skill。适用于：大 PR 审查、多文件重构、跨目录代码变更等场景。不适用于：小型单一文件修改。关键 trigger 信号：用户提到"大变更集"、"并发审查"、"文件捆绑"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: Core Design: Deterministic Engineering × Agent Hybrid — Smart File Bundling
tags: [divide-and-conquer, smart-bundling, concurrent-review]
related_skills: [deterministic-engineering-hard-constraints]
---

# Divide-and-Conquer Strategy（分治策略）

## R (Reading) — 原文引用

> "Smart file bundling — Groups related files into a single review unit (e.g., `message_en.properties` and `message_zh.properties` are bundled together). Each bundle runs as a sub-agent with isolated context — a divide-and-conquer strategy that stays stable on very large changesets and naturally supports concurrent review."

## I (Interpretation) — 方法论骨架

**核心思想**: 通过智能文件捆绑将大型变更集分解为独立的审查单元，每个单元作为子 Agent 运行，实现分治和并发审查。

**关键组件**:
1. **Smart file bundling**: 将相关文件（如多语言 properties 文件）分组为单个审查单元
2. **Isolated context**: 每个捆绑包作为独立子 Agent 运行，上下文隔离
3. **Concurrent review**: 天然支持并发审查，提高大变更集的处理效率

**与相邻 skill 的区分**: 
- 与 `deterministic-engineering-hard-constraints` 的关系：Smart file bundling 是确定性工程硬约束的具体实现之一
- 与 `agent-dynamic-decision-making` 的区别：前者是分治策略的工程实现，后者是动态决策的 Agent 能力

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 大规模变更集处理
- **背景**: 处理包含数百个文件的大型 PR
- **问题**: 通用 Agent 在大变更集上"偷工减料"，只审查部分文件
- **应用**: 引入 Smart file bundling + 并发子 Agent 审查
- **结果**: 审查覆盖率显著提高，token 消耗仅为 ~1/9

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户需要"审查包含数百个文件的大型 PR"
- 用户遇到"通用 Agent 在大变更集上遗漏文件"
- 用户希望"提高大变更集的审查效率"
- 用户需要"并发审查多个文件组"

**不应触发的场景**:
- 小型单一文件修改
- 不需要并发处理的简单任务
- 文件之间无关联性的场景

**关键 trigger 词**: "大变更集"、"并发审查"、"文件捆绑"、"分治"、"隔离上下文"

## E (Execution) — 可执行步骤

1. **分析变更集**: 识别所有需要审查的文件及其关联性
   - 完成标准: 产出完整的变更文件清单及关联性分组说明，无未分类文件
2. **智能捆绑**: 将相关文件分组为审查单元（如多语言文件、同一模块的文件）
   - 完成标准: 每个捆绑包内文件的关联依据明确（同模块/多语言对应等），无游离文件
3. **分配子 Agent**: 为每个捆绑包分配独立的子 Agent，隔离上下文
   - 完成标准: 每个捆绑包对应一个独立子 Agent，各子 Agent 上下文互不共享
4. **并发执行**: 并行运行所有子 Agent 进行审查
   - 完成标准: 所有子 Agent 并行启动，且各自产出独立的审查结果
5. **汇总结果**: 合并所有子 Agent 的审查结果，生成统一报告
   - 完成标准: 统一报告覆盖全部捆绑包的审查结果，与子 Agent 数量核对一致

**完成标准**: 所有文件都被审查，无遗漏，审查时间显著缩短

**判停条件**: 连续 5 次大变更集审查无遗漏，平均审查时间降低 50% 以上

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 小型单一文件修改
- 文件之间无关联性的场景
- 不需要并发处理的简单任务

**作者盲点**:
- **捆绑策略复杂性**: 需要智能判断哪些文件应该捆绑在一起
- **上下文隔离成本**: 隔离上下文可能导致某些跨文件问题被遗漏
- **并发资源消耗**: 大量并发子 Agent 可能消耗较多系统资源

**时代局限**:
- 当前架构基于现有 LLM 并发能力，未来可能需要调整
- 捆绑策略依赖于对文件关联性的理解
