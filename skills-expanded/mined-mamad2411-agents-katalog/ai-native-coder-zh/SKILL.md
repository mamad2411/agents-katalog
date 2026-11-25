---
name: ai-native-coder-zh
description: "AI 智能体系统提示/技能：强制执行 AI 原生工程规则，配合行为准则约束。优先保障上下文窗口效率、严格隔离、无状态执行以及面向 LLM 优化的语法。"
---

# AI-Native Engineering Spec v6

本技能定义面向 LLM / AI Agent 的**七层工程规范**。
规则按职责分层，按需加载，以最小化 Context 占用。

## 架构总览

| 层 | 职责 | 参考文件 |
|----|------|----------|
| Layer 0 | 绝对运行时法则（最高优先级） | `references/layer-0-runtime-laws.md` |
| Layer 1 | 认知架构（Context 组织） | `references/layer-1-cognitive-architecture.md` |
| Layer 2 | 运行时架构（宿主/逻辑分离） | `references/layer-2-runtime-architecture.md` |
| Layer 3 | 数据与状态工程 | `references/layer-3-data-state.md` |
| Layer 4 | 身份与上下文压缩 | `references/layer-4-identity-compression.md` |
| Layer 5 | 工程约定 | `references/layer-5-engineering-conventions.md` |
| Layer 6 | AI 运行时演化 | `references/layer-6-ai-runtime-evolution.md` |

## 如何使用

- **开始任务前**：先确认 Layer 0 的 10 条绝对法则（见下方速查）。
- **设计系统 / 组织代码时**：读取 Layer 1 + Layer 2。
- **处理数据、Schema、状态时**：读取 Layer 3 + Layer 4。
- **编写具体实现时**：读取 Layer 5。
- **做架构演进决策时**：读取 Layer 6。

每条规则的详细说明、示例和禁止项，均在对应层级的参考文件中。

---

## Layer 0 速查（Absolute Runtime Laws）

Layer 0 拥有最高优先级，任何情况下不得违反。完整内容见 `references/layer-0-runtime-laws.md`。

| # | 法则 | 核心含义 |
|---|------|----------|
| LAW-1 | Runtime Correctness > Token Efficiency | 不得为 LLM 便利性牺牲系统正确性 |
| LAW-2 | State > Code | 代码可重建，状态不可丢失 |
| LAW-3 | All Side Effects Must Be Replayable | DB/MQ/HTTP/文件均须支持 Replay |
| LAW-4 | Replay Must Be Deterministic | 禁止隐式随机、不可控时间依赖 |
| LAW-5 | Runtime Layer != Cognitive Layer | 运行时职责与认知职责不得混淆 |
| LAW-6 | No Hidden Side Effects | 禁止 decorator magic、AOP、隐式 mutation |
| LAW-7 | No Deep Dependency Chains | 依赖深度 ≤ 2 |
| LAW-8 | Context Must Be Locally Closed | 单次推理 ≤ 3 个 Context Unit |
| LAW-9 | Semantic Version Must Be Locked | 禁止用最新规则重放历史流量 |
| LAW-10 | AI Outputs Must Be Traceable | 所有副作用须追溯到 model/prompt/schema |
