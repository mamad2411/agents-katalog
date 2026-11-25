---
name: template-engine-over-language-driven
description: |
  当需要基于模板引擎进行规则匹配而非纯语言驱动时使用此 skill。适用于：代码规范检查、安全规则匹配、性能反模式检测等场景。不适用于：需要主观判断的场景。关键 trigger 信号：用户提到"模板引擎"、"规则匹配"、"稳定性"等问题。
source_book: alibaba/open-code-review
source_project: alibaba/open-code-review
source_chapter: Core Value: Template Engine > Language-Driven Rules
tags: [template-engine, rule-matching, stability]
related_skills: [deterministic-engineering-hard-constraints, hard-constraints-over-soft-prompts, unstable-quality-anti-pattern]
---

# Template Engine > Language-Driven Rules（模板引擎优于语言驱动规则）

## R (Reading) — 原文引用

> "Fine-grained rule matching — Matches review rules to each file's characteristics, keeping the model's attention sharply focused and eliminating information noise at the source. Compared to purely language-driven rule guidance, template-engine-based rule matching is more stable and predictable."

## I (Interpretation) — 方法论骨架

**核心思想**: 基于模板引擎的规则匹配比纯语言驱动更稳定、更可预测，能够保持模型注意力集中并消除信息噪声。

**关键原则**:
1. **文件特征分析**: 分析每个文件的特征（语言类型、框架、用途等）
2. **模板匹配**: 基于文件特征匹配预定义的规则模板
3. **精准提示**: 将匹配的规则模板注入提示，保持模型注意力集中
4. **消除噪声**: 只传递相关规则，避免无关信息干扰模型判断

**与相邻 skill 的区分**: 
- 与 `hard-constraints-over-soft-prompts` 的关系：模板引擎是硬约束的具体实现方式之一
- 与 `specialized-toolset-over-generic` 的区别：前者关注规则匹配，后者关注工具集选择

## A1 (Past Application) — 书中作者用过的案例

**案例**: Alibaba Group 多语言规则集实现
- **背景**: 需要支持 NPE、线程安全、XSS、SQL 注入等多种规则
- **问题**: 纯语言驱动的规则指导难以调试，质量波动大
- **应用**: 引入基于模板引擎的细粒度规则匹配
- **结果**: 规则匹配更稳定可预测，模型注意力更集中

## A2 (Future Trigger) — 用户在什么情境下会需要这个

**触发场景**:
- 用户需要"根据文件类型应用不同的审查规则"
- 用户遇到"纯语言驱动的规则难以调试"
- 用户希望"提高规则匹配的稳定性"
- 用户需要"消除无关信息对模型的干扰"

**不应触发的场景**:
- 需要主观判断的场景（如代码风格偏好）
- 规则本身不明确的场景
- 需要灵活性和创造力的场景

**关键 trigger 词**: "模板引擎"、"规则匹配"、"稳定性"、"细粒度"、"消除噪声"

## E (Execution) — 可执行步骤

1. **定义规则模板**: 为不同类型的文件定义预审查规则模板
   - 完成标准: 规则模板库覆盖全部目标文件类型，每个模板有唯一标识
2. **分析文件特征**: 识别每个文件的语言类型、框架、用途等特征
   - 完成标准: 每个待审文件产出特征标签集，无特征缺失文件
3. **匹配规则**: 基于文件特征匹配对应的规则模板
   - 完成标准: 每个文件命中有且仅有一组规则模板，匹配结果可复现
4. **生成精准提示**: 将匹配的规则注入提示，保持模型注意力集中
   - 完成标准: 注入提示仅包含该文件命中的规则，无未命中规则混入
5. **验证效果**: 测试规则匹配的稳定性和准确性
   - 完成标准: 同一批文件重复匹配结果完全一致，准确率 >95%

**完成标准**: 规则匹配准确率 >95%，无无关信息干扰

**判停条件**: 连续 10 次规则匹配无错误，模型注意力集中度显著提高

## B (Boundary) — 什么时候不适用 / 作者的盲点

**不适用场景**:
- 需要主观判断的场景
- 规则本身不明确的场景
- 需要灵活性和创造力的场景

**作者盲点**:
- **模板维护成本**: 需要持续维护和更新规则模板
- **覆盖范围限制**: 预定义模板可能无法覆盖所有边缘场景
- **灵活性牺牲**: 模板引擎可能限制某些特殊场景的处理能力

**时代局限**:
- 当前架构基于现有规则体系，未来可能需要调整
- 模板设计依赖于对审查规则的深入理解
