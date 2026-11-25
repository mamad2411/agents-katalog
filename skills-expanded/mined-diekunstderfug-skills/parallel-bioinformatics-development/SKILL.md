---
name: parallel-bioinformatics-development
description: "Use when planning or executing bioinformatics work with multiple analysis or development lanes whose scientific dependencies, write sets, or local resource relationships need concurrency judgment."
---

# 生物信息学并行开发

这是 `superpowers:dispatching-parallel-agents` 的生物信息学判断层，不是独立
调度器。它负责发现分析 lane；是否并发由当前模型结合收益、耦合、资源和验证
成本决定。

**REQUIRED BASE:** 只有多 lane 协调确实需要正式计划时才使用
`superpowers:writing-plans`；不要为范围清楚的常规科研分析自动生成长计划。
执行选定的并行 lane 时使用 `superpowers:dispatching-parallel-agents` 完成派发、
上下文隔离和集成。已有批准且决策完整的计划可直接执行；设计仍不确定时使用
`superpowers:brainstorming`。

## 科研验证不是 TDD

科研分析、队列迁移、统计建模、数据整理和复现工作默认**不使用**
`superpowers:test-driven-development`。不要为了满足软件工程仪式先制造失败测试，
也不要把分析脚本、配置、cohort adapter、模型 wrapper、图表或结果表强行改写成
单元测试驱动开发。

默认验证顺序：

1. 冻结科学合同：样本纳排、endpoint、阳性类、表达尺度、数据版本、训练/验证边界。
2. 核对 baseline/parity：与可信旧结果、官方示例或手工可核算小例一致。
3. 运行最小 smoke：真实输入能加载、维度和 complete-case 数符合预期。
4. 检查 invariants：唯一键、样本集合、方向、缺失、范围、无泄漏、无静默重排。
5. 审计 artifacts：产物存在、非空、schema、hash、来源和角色标签正确。
6. 做科学 sanity check：效应方向、分布、已知生物学和敏感性分析合理。

只有以下情形才考虑局部 TDD：

- 独立、可复用、确定性的纯软件组件；
- 明确的软件 bugfix，且回归行为可稳定表达；
- 用户明确要求 TDD。

即使使用，也只覆盖该软件组件，不扩散到整个科研项目。单元测试通过不等于统计
有效、生物学正确或外部验证成立。

## Superpowers 计划合同

计划以 `superpowers:writing-plans` 的格式为主体。默认保存到
`docs/superpowers/plans/YYYY-MM-DD-<name>.md`，并保留其标准标题、agentic-worker
handoff、`Global Constraints`、每个 `Task N` 的 `Files`、`Interfaces`、checkbox
步骤、精确命令和期望结果。用户指定的计划路径优先。

标准 handoff 原样使用：

```markdown
> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.
```

在标准 handoff 后追加以下路由声明；它补充而不替换 Superpowers：

```markdown
> **Parallel bioinformatics overlay:** When concurrency is selected, REQUIRED SUB-SKILLS:
> use `parallel-bioinformatics-development` as the cross-lane decision layer and
> `superpowers:dispatching-parallel-agents` for the chosen independent lanes.
> Use `superpowers:subagent-driven-development` only inside one lane, not as the
> cross-lane scheduler.
```

在 `Global Constraints` 后、`Task 1` 前加入扩展矩阵：

```text
Task | Lane | Consumes -> Produces | Write set | Depends on / Ready when |
Scientific role | Resource | Wave | Owner | Verify / Evidence
```

矩阵行必须引用标准 `Task N`；任务正文仍是执行事实源。`Scientific role` 使用
`gate / producer / reducer / release`；`Resource` 记录本机 CPU、内存或 I/O 约束；
`Wave` 是计划提示而非强制调度；`Owner` 在派发时认领；checkbox 继续记录任务
状态，不另建状态机。

每个矩阵行必须有对应的 Superpowers 任务正文，格式保持为：

```markdown
### Task N: [独立可验证的交付物]

**Files:**
- Create/Modify/Test: `exact/path`

**Interfaces:**
- Consumes: [精确输入或上游接口]
- Produces: [精确产物或下游接口]

- [ ] **Step 1: [精确动作]**
  - Run: `[精确命令]`
  - Expected: `[可观察结果]`

- [ ] **Step 2: [实现、运行或验证动作]**
```

任务采用与科学风险匹配的验证策略。关键共享数据生成或转换优先使用可执行的
合同、baseline、smoke、invariant 和 artifact Verify；普通分析 lane 同样如此。
仅符合“科研验证不是 TDD”一节的局部纯软件组件才使用 TDD。矩阵不能代替这些
checkbox 步骤。

## 判断顺序

### 1. 先处理会改变下游结论的合同

优先冻结多个 lane 共同依赖的样本纳排与去重、endpoint/label/阳性类、数据和
标识符版本、表达尺度与预处理、批次和缺失值规则、训练/验证/外部边界、共同
特征与协变量、评价指标、cutoff 来源及多重检验 family。方法或敏感性分支只
改变预先声明的维度。

共享 loader、矩阵、关键数据生成或其他会影响大量下游的步骤先完成必要验证，
再解锁其消费者。验证强度由风险决定，不以 reviewer 数量决定。

### 2. 展开候选 lane

同一功能按 cohort、batch、endpoint、subgroup、omics、platform、model、method、
scoring、normalization、sensitivity、negative control 或 internal/external
validation 展开的分支，通常是独立候选 lane。功能不同但互不消费新产物的
数据审计、实现、运行、统计复核、图形和溯源任务也同样是候选 lane。

扩展矩阵中的 `Write set` 同时覆盖代码、结果目录、缓存、manifest fragment 和
正式产物；`Depends on / Ready when` 只引用已命名任务及可验证条件。拒绝依赖环、
未知依赖及并发写同一可变状态。

### 3. 用 Superpowers 决定是否并发

当任务可独立理解、科学合同稳定、互不消费新产物、写集合互斥且资源允许时，
将其作为并发候选交给 Superpowers。模型可因任务过小、派发与集成成本更高、
根因仍未知、上下文高度耦合或本机资源不足而选择单独完成或串行，并简述理由。

任务编号和功能差异本身不构成依赖。CPU、内存或 I/O 限制只约束重计算并发，
不应伪造代码依赖；重任务串行时，轻量实现、审阅和解释仍可并行。

### 4. 保留 producer/reducer 边界

producer lane 写私有结果目录和 fragment。需要完整 producer 集合或写 canonical
共享产物的全局 FDR、pooled normalization、meta-analysis、跨 lane 比较、最终
选择、manifest、registry 和报告，由单一 owner 在相应 producers 验证后执行。

### 5. 执行和验证

对决定并发的 lanes，按 Superpowers 在同一轮派发 fresh、focused、self-contained
任务；worker 只写自己的 `Write set`，不执行 Git。任一 lane 结束后重新评估
新解锁任务，并在确有收益时补位。

lane 失败只阻塞其传递下游、要求完整集合的 reducer 和相应 release gate；独立
旁支继续。若失败否定共享科学合同，则重新评估该合同的全部消费者。

worker 的完成报告是待核实声明。每条 lane 提供实际文件、精确验证命令、产物
和 concerns，主 agent 检查越界与冲突并完成跨 lane 集成验证。科研任务默认采用
合同、baseline、smoke、invariant、artifact 和 scientific sanity Verify；不要
自动调用通用 TDD。仅在方法争议、异常结果、泄漏风险或高代价发布时升级独立
复核。

完成报告说明实际并发选择及理由、各 lane 证据、reducer 屏障和最终集成结果。
