---
name: hard-constraints-over-soft-prompts
description: |
  当需要在代码审查中建立硬约束而非软提示时使用此 skill。适用于：文件选择、规则匹配、位置定位等不能出错的场景。不适用于：需要灵活性和创造力的场景。关键 trigger 信号：用户提到"硬约束"、"工程逻辑"、"稳定性"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: Core Value: Hard Constraints > Soft Prompts
tags: [hard-constraints, engineering-logic, stability]
related_skills: [deterministic-engineering-hard-constraints, template-engine-over-language-driven]
---

# Hard Constraints > Soft Prompts（硬约束优于软提示）

## R (Reading) — 原文引用

> "For review steps that *must not go wrong*, engineering logic — not the language model — guarantees correctness."
>
> "The root cause: a purely language-driven architecture lacks hard constraints on the review process."

## I (Interpretation) — 方法论骨架

**核心思想**: 对于代码审查中不能出错的步骤，必须用工程逻辑建立硬约束，而不是依赖语言模型的软提示。

**关键原则**:
1. **识别硬约束步骤**: 确定哪些步骤绝对不能出错（文件选择、规则匹配、位置定位）
2. **设计确定性算法**: 为每个硬约束步骤设计确定性算法，不依赖 LLM
3. **外部模块实现**: 将硬约束步骤实现为独立的外部模块，与 Agent 解耦
4. **测试验证**: 编写严格的测试用例验证每个硬约束步骤的正确性

**与相邻 skill 的区分**: 
- 与 `deterministic-engineering-hard-constraints` 的关系：这是其核心设计哲学的提炼
- 与 `template-engine-over-language-driven` 的关系：模板引擎是硬约束的具体实现方式之一

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 内部架构重构
- **背景**: 从纯语言驱动架构转向 deterministic engineering × agent hybrid
- **问题**: 通用 Agent 在大变更集上缺乏硬约束，导致不完整覆盖、位置漂移、质量不稳定
- **应用**: 引入硬约束机制，用工程逻辑保证关键步骤的正确性
- **结果**: Precision 和 F1 显著高于通用 Agent，token 消耗仅为 ~1/9

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户抱怨"审查漏掉了重要文件"
- 用户发现"报告的问题位置不准确"
- 用户遇到"审查质量随提示变化而波动"
- 用户需要"确保某些关键步骤必须正确执行"

**不应触发的场景**:
- 需要灵活性和创造力的场景（如代码重构建议）
- 动态上下文检索（如查找相关代码片段）
- 主观判断（如代码风格偏好）

**关键 trigger 词**: "硬约束"、"工程逻辑"、"稳定性"、"不能出错"、"确定性"

## E (Execution) — 可执行步骤

1. **识别硬约束步骤**: 列出审查过程中不能出错的步骤
   - 完成标准: 硬约束步骤清单定稿，每项附"不能出错"的影响说明
2. **设计确定性算法**: 为每个硬约束步骤设计不依赖 LLM 的确定性算法
   - 完成标准: 每个步骤都有算法设计文档，明确输入、输出与判定规则，零 LLM 依赖
3. **实现外部模块**: 将硬约束步骤实现为独立的外部模块
   - 完成标准: 模块代码合入并通过独立运行冒烟测试
4. **编写测试用例**: 为每个硬约束步骤编写严格的测试用例
   - 完成标准: 每个步骤至少有正常路径与异常路径两类用例且全部通过
5. **集成验证**: 在完整审查流程中验证硬约束步骤的正确性
   - 完成标准: 端到端试跑中硬约束步骤零错误，结果与单测预期一致

**完成标准**: 所有硬约束步骤通过单元测试，无位置漂移，无文件遗漏

**判停条件**: 连续 10 次审查无硬约束相关错误

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 需要灵活性和创造力的场景
- 动态上下文检索
- 主观判断

**作者盲点**:
- **过度工程化风险**: 对于简单任务，硬约束可能过于复杂
- **维护成本**: 硬约束模块需要持续维护和更新
- **灵活性牺牲**: 硬约束可能限制某些边缘场景的处理能力

**时代局限**:
- 当前架构基于现有 LLM 能力，未来可能需要调整
- 硬约束的设计依赖于对审查过程的深入理解
