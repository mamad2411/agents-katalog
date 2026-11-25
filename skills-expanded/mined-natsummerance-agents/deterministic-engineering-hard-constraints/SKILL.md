---
name: deterministic-engineering-hard-constraints
description: |
  当需要确保代码审查中关键步骤的正确性时使用此 skill。适用于：文件选择、规则匹配、位置定位等不能出错的场景。不适用于：动态决策、上下文检索等需要灵活性的场景。关键 trigger 信号：用户提到"必须精确"、"不能遗漏"、"位置不准"、"规则不稳定"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: Core Design: Deterministic Engineering × Agent Hybrid
tags: [deterministic-engineering, hard-constraints, code-review]
related_skills: [divide-and-conquer-strategy, hard-constraints-over-soft-prompts, template-engine-over-language-driven]
---

# Deterministic Engineering Hard Constraints（确定性工程硬约束）

## R (Reading) — 原文引用

> "For review steps that *must not go wrong*, engineering logic — not the language model — guarantees correctness."
>
> "The root cause: a purely language-driven architecture lacks hard constraints on the review process."

## I (Interpretation) — 方法论骨架

**核心思想**: 对于代码审查中不能出错的步骤，必须由工程逻辑而非语言模型来保证正确性。

**关键组件**:
1. **Precise file selection**: 精确确定哪些文件需要审查、哪些应该过滤，确保不遗漏重要变更
2. **Smart file bundling**: 将相关文件分组为单个审查单元，每个捆绑包作为独立子 Agent 运行
3. **Fine-grained rule matching**: 基于模板引擎的规则匹配，比纯语言驱动更稳定可预测
4. **External positioning & reflection**: 独立的定位和反思模块系统性地提高 AI 反馈的准确性

**与相邻 skill 的区分**: 
- 与 `agent-dynamic-decision-making` 的区别：前者负责硬约束（不能出错），后者负责动态决策（需要灵活性）
- 与 `divide-and-conquer-strategy` 的关系：Smart file bundling 是分治策略的具体实现

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 内部验证
- **背景**: 服务数万名开发者，处理数百万代码缺陷
- **问题**: 通用 Agent 在大变更集上"偷工减料"，只审查部分文件
- **应用**: 引入 Precise file selection + Smart file bundling，确保所有重要变更都被审查
- **结果**: Precision 和 F1 显著高于通用 Agent，token 消耗仅为 ~1/9

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户抱怨"审查漏掉了重要文件"
- 用户发现"报告的问题位置不准确"
- 用户遇到"审查质量随提示变化而波动"
- 用户需要"确保某些关键文件必须被审查"

**不应触发的场景**:
- 纯信息查询（如"这个函数做什么？"）
- 日常琐碎选择（如"变量名用什么好？"）
- 需要灵活性和创造力的场景（如"如何重构这段代码？"）

**关键 trigger 词**: "必须精确"、"不能遗漏"、"位置不准"、"规则不稳定"、"硬约束"

## E (Execution) — 可执行步骤

1. **识别硬约束步骤**: 列出审查过程中不能出错的步骤（文件选择、规则匹配、位置定位）
   - 完成标准: 得到明确的硬约束步骤清单，每一项都标注"不能出错"的理由
2. **设计工程逻辑**: 为每个硬约束步骤设计确定性算法（而非依赖 LLM）
   - 完成标准: 每个硬约束步骤都有对应的确定性算法设计说明，且不依赖 LLM 输出
   - 文件选择：基于 git diff 和文件类型过滤规则
   - 规则匹配：基于模板引擎的文件特征匹配
   - 位置定位：独立的 AST 解析和行号计算模块
3. **实现外部模块**: 将硬约束步骤实现为独立的外部模块，与 Agent 解耦
   - 完成标准: 硬约束模块代码合入，可脱离 Agent 主流程独立运行
4. **集成测试**: 编写测试用例验证每个硬约束步骤的正确性
   - 完成标准: 每个硬约束步骤的单元测试全部通过，用例覆盖正常与异常路径
5. **监控和反馈**: 记录硬约束步骤的执行日志，用于持续改进
   - 完成标准: 执行日志落盘可查询，能定位到具体失败的步骤与原因

**完成标准**: 所有硬约束步骤通过单元测试，无位置漂移，无文件遗漏

**判停条件**: 连续 10 次审查无硬约束相关错误

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 需要灵活性和创造力的场景（如代码重构建议）
- 动态上下文检索（如查找相关代码片段）
- 主观判断（如代码风格偏好）

**作者盲点**:
- **Recall 较低**: 为了精度牺牲召回率，可能漏掉一些真实缺陷
- **学习曲线**: 需要理解 deterministic engineering 的设计哲学
- **依赖 Git**: 要求 Git >= 2.41，可能在旧系统上存在问题

**时代局限**:
- 当前架构基于现有 LLM 能力，未来可能需要调整
- 插件生态目前支持有限平台
