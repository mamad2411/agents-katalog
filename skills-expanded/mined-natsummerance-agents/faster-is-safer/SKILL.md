---
name: faster-is-safer
description: |
  当用户询问"应该频繁部署还是批量部署"、"如何降低部署风险"或"快速迭代的价值是什么"时调用此 skill。不适用于：纯理论讨论、不需要部署的场景、严格变更管理的场景。关键 trigger 信号：部署、ship、快速迭代、频繁发布、降低风险、faster is safer。
source_book: Agent Skills Addy Osmani
source_project: addyosmani/agent-skills
source_chapter: Commands table / SHIP phase
tags: [deployment, shipping, fast-iteration, risk-reduction]
related_skills: ["auto-build-mode", "test-driven-development", "no-team-collaboration-guidance"]
---

# SKILL.md - Faster Is Safer（更快更安全）

## R (Reading) - 原文引用

> "/ship | Ship to production | Faster is safer"

## I (Interpretation) - 方法论骨架

**核心思想**：快速部署到生产环境比长期分支更安全。这种"快速部署"的原则减少合并冲突，降低风险，并允许早期用户反馈。挑战传统"慢而稳"的观念，强调小步快跑的价值。

**关键要素**：
1. **Frequent deployments**: 频繁部署，小步快跑
2. **Reduced merge conflicts**: 减少合并冲突
3. **Early feedback**: 允许早期用户反馈
4. **Lower risk per deployment**: 每次部署的风险更低

## A1 (Past Application) - 书中作者用过的案例

Agent Skills 的 `/ship` 命令对应 SHIP 阶段，强调"Faster is safer"。Addy Osmani 将快速部署作为核心原则，挑战传统的"慢而稳"观念。

这种设计使得团队能够更快地交付价值，同时通过小步快跑降低每次部署的风险。

## A2 (Future Trigger) - 用户在什么情境下会需要这个

**适用场景**：
- 用户不确定应该频繁部署还是批量部署
- 用户想降低部署风险
- 用户想获得早期用户反馈
- 用户想建立持续交付的文化

**与相邻 skill 的区分**：
- 与 `auto-build-mode` 的区别：faster-is-safer 关注**部署策略**，而 auto-build-mode 关注**开发自动化**。前者是发布阶段，后者是实现阶段。
- 与 `test-driven-development` 的区别：faster-is-safer 关注**部署频率和风险**，而 test-driven-development 关注**代码正确性验证**。两者互补：TDD 保证代码质量，快速部署保证及时交付。

## E (Execution) - 可执行步骤

1. **评估部署频率**
   - 检查当前团队的部署频率
   - 识别阻碍频繁部署的因素
   - 设定改进目标（如从每周一次到每天多次）
   - 完成标准: 产出部署频率基线数据和量化的改进目标值

2. **优化部署流程**
   - 自动化构建和测试流程
   - 简化审批环节（保留必要的安全检查）
   - 建立回滚机制
   - 完成标准: 构建与测试全自动执行，回滚流程演练通过一次

3. **小步快跑**
   - 将大变更分解为小变更
   - 每次部署只包含少量变更
   - 确保每次部署都可独立验证
   - 完成标准: 连续多次部署的单次变更量均低于设定阈值且各自独立验证通过

4. **监控和反馈**
   - 部署后密切监控系统状态
   - 收集用户反馈
   - 根据反馈快速迭代
   - 完成标准: 监控告警与反馈渠道上线，每次部署后均有状态确认记录

## B (Boundary) - 什么时候不适用

**不适用场景**：
- 严格变更管理的场景（如金融、医疗行业）
- 大规模基础设施变更
- 需要长时间测试的复杂系统
- 用户无法承受频繁变更的场景

**作者的盲点**：
- Addy Osmani 假设所有团队都能受益于快速部署，但实际上某些行业有严格的合规要求
- agent-skills 缺少对部署策略差异化指导（如蓝绿部署、金丝雀发布等）
- 没有提到如何处理部署失败后的回滚策略
