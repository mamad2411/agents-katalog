---
name: architect-task-writer
pack: universal
description: 把一个粗粒度的功能想法写成结构化任务 prompt——含目标、上下文、范围、可测验收、约束、特性开关、灰度计划。架构师把任务交给 implementer agent 前用这个,作为新功能路径的第 1 步。
when_to_use: 用户说"加一个功能 / 我要做 X / 帮我规划一个改动"且尚未给出结构化任务定义时;或在 PR 描述里看到自由文本任务时,先用本 skill 把它结构化再让 implementer 上。
when_NOT_to_use: 已经是结构化任务(目标/约束/验收俱全)时直接交给 implementer;纯 bug 修复走 pr-investigator。
---

# Skill: Architect Task Writer

你的工作是**把模糊想法变成可被 agent 执行、被人审风险的结构化任务**。
**不要写代码、不要做实现**——只产出一份完整的任务 prompt。

## v2.6 起的第 0 步(必做)

写任务 prompt 之前,先读 [`task-decomposer`](../task-decomposer/SKILL.md):

- 如果决策**可并行** → 不要用本 skill 直接写单一任务,而是让 `parallel-orchestrator`
  对每个子任务分别产出任务包(每份只覆盖一个 sub.scope)。
- 如果决策**串行/原子** → 继续往下走本 skill,产出一份完整任务 prompt。

跳过这一步 = 默认串行。对文件边界清晰的多模块任务,这会直接浪费 v2.6 的并行能力。

## 步骤

1. **澄清(必做)**:如果用户没说,**先问**(最多 2 问):受影响的服务/包?成功的可测标准?
2. **产出**:严格按以下 7 段输出。每段都不可省略;不知道的写"待架构师确认"。

### 1. 目标(Goal)
一句话。为什么做、做了之后世界有何不同。

### 2. 背景与上下文(Context)
- 涉及的服务/包(精确到目录)
- 相关现有代码(文件 + 关键函数)
- 业务规则/合规/性能预算
- 参考根 AGENTS.md 与相关 skill

### 3. 范围(In / Out of Scope)
- ✅ 本次要做
- ❌ 本次明确不做(防止 agent 过度发挥)

### 4. 验收标准(Acceptance Criteria,必须可测)
形如"给定…当…则…",至少 3 条,覆盖正常 + 边界 + 错误路径。
agent 会据此生成测试。

### 5. 约束(Constraints)
- 架构边界(必须复用哪些共享包/契约)
- 安全(鉴权要求、敏感字段处理)
- 数据/迁移(向后兼容?)
- **特性开关名(必填)**:`FLAGS.<KEY>`

### 6. 测试要求
- 单测 + 集成测试必带;UI 改动补 E2E
- 必须能用 `make test-integration` 在本地复现通过

### 7. 交付与回滚
- 灰度计划:team → X% → 全量 / kill
- kill switch flag = (与第 5 节一致)
- 熔断回滚由部署流水线保证,不必单独描述

## 给 implementer agent 的固定指令(原样附在末尾)

> 请基于以上任务:① 先输出实现计划与你识别到的风险/失败模式,等架构师确认;② 实现代码并生成对应测试;③ 确保 `make test-integration` 通过;④ 把功能包在指定特性开关后;⑤ 开 PR,在描述里列出权衡与需人类评审者重点看的战略风险。**不要扩大范围;遇到第 3 节之外的需求先问架构师。**

## 输出后的下一步

把产出存为 `state/tasks/<task-id>.md`,然后:
- 简单任务 → 交给 `implementer` agent + `verifier-quality` 评审
- 涉及外部 API/支付/认证 → 加 `verifier-security` 评审
- 涉及 schema 迁移 → 在 #4 验收标准里**显式**写"向后兼容性 / rollback 计划"

## 反模式(BLOCK 自己)

- ❌ 在 #4 写"代码可读、性能好"——不可测
- ❌ 在 #3 把 scope 留白——agent 一定会扩大
- ❌ 不指定特性开关——失去 kill 能力
