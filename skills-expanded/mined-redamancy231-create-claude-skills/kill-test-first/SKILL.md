---
name: kill-test-first
description: '[决策:预注册] Pre-registration audit for new research directions, quant strategies, or thesis topics: falsifiable hypothesis, prior-art check, strongest counter-argument, death criteria before results, cheapest falsification with strong baseline, three-state verdict (GO/STOP/REDESIGN). Use before committing resources to a new direction. Not for bug fixes, experiment reproduction, or routine controlled experiments.'
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch
source: self
source_type: self
license: "CC-BY-4.0"
verified_by: "GPT-5.5, DeepSeek-V4-Pro, Kimi-K2.7, Qwen3.7-Max, GLM-5.2"
---

# Kill-Test First（事前否决 + 预登记）

> **核心信念**：最贵的错误不在执行里，而在「根本该不该做」这个没人事前问的问题上。
> **真正 alpha**：不是「能发现失败方向」，而是把通用好习惯——强基线 + 预登记 + 反方论证——强制前置，并留下审计痕迹。
> **强度**：你是 decision owner，最终 GO/STOP 你拍板。但独立 reviewer 的建议必须单独冻结；要 override 记一条 `override_reason`。

## 快速参考（路由表）

| 场景 | 执行 |
|------|------|
| 新研究想法/策略/选题 → 「值不值得做？」 | 门 1 完整协议（步骤 0→8）→ [gate1-protocol.md](reference/gate1-protocol.md) |
| 已批准项目内的常规实验 | 轻量提醒：仅确认可证伪命题（步骤 1） |
| GO 之后、正式验证数据之前 | 门 2 预登记冻结 → [gate2-preregistration.md](reference/gate2-preregistration.md) |
| 量化策略（含回测/因子） | → 额外过「量化策略红线」→ [quant-redlines.md](reference/quant-redlines.md) |
| 协议概念/合格标准速查 | → [minimum-standards.md](reference/minimum-standards.md) |
| 案例演示 | → [EXAMPLES.md](EXAMPLES.md) |

## 触发分级

**应触发（走完整协议）**：新研究想法 / 新量化策略 / 新论文选题 / 新模型评估 / 新架构方案 / 新数据管线；问「值不值得做 / 有没有 alpha」；准备进入 Phase 1 建设。

**不应触发（负例，别强制）**：修 bug、复现实验、补测试、已冻结协议内的对照臂、已批准项目内的常规实验。

**判定问句**：「这是 Phase 1 建设前的**新方向决策**，还是**已批准项目内的常规实验**？」前者走完整协议；后者只**轻量提醒**＝仅确认可证伪命题（步骤 1）+ 问一句「要不要走完整 kill-test」，不强制全协议。

**用户直接说「帮我实现 / 帮我做个 X」且 X 是新方向时**，也先轻量问一句「要不要先过一道 kill-test？」——别因为没问「值不值得」就跳过。

## 协议路由

```
新方向决策 → 门1 事前否决（步骤 0→8）
  ├─ STOP  → 不进 Phase 1，不开工
  ├─ REDESIGN → 重写命题（累计 ≤2 次，超过升级为 STOP）
  └─ GO    → 门2 预登记冻结 → 进入下一阶段（死亡判据全程挂着）
已批准常规实验 → 轻量提醒（仅步骤 1，不强制全协议）
```

## 参考文件

| 文件 | 内容 |
|------|------|
| [reference/gate1-protocol.md](reference/gate1-protocol.md) | 门1 事前否决完整协议（8步 + 固定输出块） |
| [reference/gate2-preregistration.md](reference/gate2-preregistration.md) | 门2 预登记冻结 |
| [reference/quant-redlines.md](reference/quant-redlines.md) | 量化策略 6 条不可外包红线 |
| [reference/minimum-standards.md](reference/minimum-standards.md) | 关键概念最低合格标准 |
| [reference/death-criteria.md](reference/death-criteria.md) | 本 Skill 的死亡判据 |
| [EXAMPLES.md](EXAMPLES.md) | 实战案例（事后回放） |

> **审计痕迹说明**：「留审计痕迹」指固定输出块中的结构化字段（Independence Declaration / Prior-Art Check / Result / Decision 等），留存于对话记录中。本 Skill 不写文件。
>
> **扩展资源**：[reference/complete-pipeline.md](reference/complete-pipeline.md)（非执行必需，日常使用可忽略）。
