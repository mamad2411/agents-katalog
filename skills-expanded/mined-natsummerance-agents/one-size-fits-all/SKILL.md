---
name: one-size-fits-all
description: |
  当用户在不需要生产级标准的项目上过度工程化、缺乏灵活性，或不知道如何根据项目类型调整技能应用时调用此 skill。不适用于：纯生产环境项目、已有明确工程标准的场景。关键 trigger 信号：过度工程化、原型验证、内部工具、实验性项目、差异化需求、一刀切。
source_book: Agent Skills Addy Osmani
source_project: addyosmani/agent-skills
source_chapter: Introduction / problem statement
tags: [anti-pattern, flexibility-gap, project-type, over-engineering]
related_skills: ["no-systematic-methodology", "faster-is-safer", "spec-driven-development"]
---

# SKILL.md - One-Size-Fits-All（一刀切）

## R (Reading) - 原文引用

> "Production-grade engineering skills for AI coding agents."

## I (Interpretation) - 方法论骨架

**核心问题**：Agent Skills 假设所有项目都适用同样的生产级标准，但没有考虑不同项目的差异化需求（如原型验证、内部工具、实验性项目等）。这种"一刀切"的思路可能导致用户在不需要生产级标准的项目上过度工程化。

**反模式特征**：
1. **过度工程化**：在原型验证或内部工具上应用完整的生产级流程
2. **缺乏灵活性**：无法根据项目类型调整技能应用
3. **效率低下**：在不必要的项目上浪费时间和资源
4. **资源浪费**：为简单项目配置复杂的质量门禁和测试流程

**根本原因**：agent-skills 专注于"Production-grade"，但没有提供针对不同项目类型的差异化指导。

## A1 (Past Application) - 书中作者用过的案例

Agent Skills 的标题就是"Production-grade engineering skills for AI coding agents"，强调生产级标准。但 README 中没有提到：
- 如何区分生产级项目和非生产级项目
- 如何根据项目类型调整技能应用
- 何时可以跳过某些质量门禁或测试环节

这种缺失导致用户可能在原型验证或内部工具上也应用完整的生产级流程，造成不必要的开销。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户在原型验证项目上应用完整的生产级流程
- 用户想知道如何根据项目类型调整技能应用
- 用户感到流程过于繁琐，想简化但不确定哪些环节可以跳过
- 用户想了解不同项目类型的工程标准差异

**与相邻 skill 的区分**：
- 与 `no-systematic-methodology` 的区别：one-size-fits-all 是**具体的灵活性盲点**，而 no-systematic-methodology 是**整体学习框架的缺失**。前者更具体，后者更宏观。
- 与 `faster-is-safer` 的区别：one-size-fits-all 关注**项目类型差异化**，而 faster-is-safer 关注**部署频率和风险**。两者互补：一个确保灵活适配，一个确保快速安全交付。

## E (Execution) - 可执行步骤

1. **识别项目类型**
   - 询问用户的项目类型（生产环境、原型验证、内部工具、实验性项目等）
   - 评估项目的生命周期和重要性
   - 确定合适的工程标准级别
   - 完成标准: 项目类型判定结论成文，附生命周期与重要性依据

2. **调整技能应用**
   - 生产环境项目：应用完整的生产级流程
   - 原型验证：简化流程，重点关注核心功能验证
   - 内部工具：适度简化，保留必要的质量保障
   - 实验性项目：最小化流程，快速迭代
   - 完成标准: 各项目类型对应的标准级别已明确成文并与用户确认
   - 完成标准: 调整技能应用的执行产物已产出并可验证，无遗漏项

3. **定义可跳过的环节**
   - 明确哪些质量门禁可以简化或跳过
   - 确定测试覆盖率的合理目标
   - 平衡速度与质量的取舍
   - 完成标准: 可简化项与必须保留项清单获批，覆盖率目标量化

4. **避免过度工程化**
   - 不要为一次性脚本编写完整测试套件
   - 不要为原型验证配置复杂的 CI/CD 流程
   - 根据项目价值决定投入的工程资源
   - 完成标准: 工程投入与项目价值匹配的检查记录通过复查

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 纯生产环境项目（需要完整的生产级标准）
- 已有明确工程标准的团队
- 严格合规要求的行业（如金融、医疗）
- 用户只需要单个技能建议，不需要项目类型指导

**作者的盲点**：
- Addy Osmani 假设所有项目都需要生产级标准，但实际上不同项目有不同的工程需求
- agent-skills 缺少对项目类型分类和差异化指导的任何设计
- 这种"一刀切"的思路可能导致用户在不需要生产级标准的项目上过度工程化，降低效率
