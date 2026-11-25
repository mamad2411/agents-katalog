---
name: brainstorm
description: Run parallel, evidence-grounded research ideation with main-agent rebuttal. Use for research brainstorming, research directions, or finding research gaps from a paper/wiki context.
---

# brainstorm — 对抗式研究 idea 生成

先并行探索机会桶，再由 main 对每张候选进行**致命反驳**：只有现有证据与约束均无法推翻的 `survived` card 才能进入 wiki。

## 流程

1. 运行 `curate`，形成 Context Pack：主题、page ID/论文、证据等级、缺口/矛盾、用户原始约束。
2. 并行运行 `ideate(candidate_only: true)`，获得互补的候选 cards。
3. main 去重并逐卡反驳，写入审计记录。
4. 将全部 `survived` cards 作为一个 `reviewed_cards` 批次交给 `ideate` 持久化。

`ideate` 是 Idea Card schema、字段校验和 wiki 持久化的唯一来源（持久化备好 md 经 `ingest` 统一写入）；本 skill 不重述其 schema 或写入细节。

## Pre-flight

- 用 `wiki_get` 读取相关 wiki 页面；不足时可用 browser 补充，并标注来源与证据等级。
- Context Pack 必须含有可引用的证据。没有 domain/topic、论文引用或其他证据材料时询问用户；证据不足时停止，不生成泛化 idea。

## 并行候选

固定启动五个 self subagent：`gap`、`contradiction`、`failure`、`transfer`、`constraint`。仅在 Context Pack 有额外且独立的机会桶时，加入 `ablation`、`metric`、`assumption-challenge`，最多到 `subagents.maxConcurrent`（以 `openclaw.json` 为准）。

遵循 `paper-batch-ingest` 的 self-spawn 协议：每个视角连续调用 `sessions_spawn`，省略 `agentId`，使用 `context="isolated"`、`mode="run"` 和合适的 `runTimeoutSeconds`。全部发出后调用一次 `sessions_yield` 等待 completion events；不轮询 session 工具。每个 session 必须进入成功、失败或超时之一的终态后才能汇总。

### Task 契约

每次 spawn 前，main 读取**当前** `workspace/skills/brainstorm/SKILL.md` 的完整正文，并把真实全文（不是路径、摘要或占位符）嵌入该 task。task 还必须包含：

- 用户原始请求与完整 Context Pack；
- 分配的唯一机会桶；
- `ideate(candidate_only: true)`；
- “仅内联返回 1–3 张完整候选 card，不写 wiki”的交付要求。

子 session 只返回最终 reply text。失败/超时也记录 label 与原因，不阻断其余候选的审查。

## main 反驳门禁

main 合并候选后，删除机制、锚点和目标痛点实质相同的重复项，仅保留证据链最强的变体。对每张剩余 card，尝试提出一个基于 Context Pack 的致命反驳：核心 claim 无来源支撑、已有工作已覆盖、违反硬约束、实验不能区分竞争解释或指标不可检验、风险使关键假设不可执行。

为每张 card 附加：

```text
challenge: <具体反驳；或“未找到基于现有证据和约束的致命反驳”>
verdict: rejected | survived
verdict_reason: <反驳成立或未成立的理由>
```

只有会使核心假设、可行性或可检验性不成立的具体反驳才是 `rejected`。笼统的不确定性不是反驳。

## 交付与完成门禁

- 没有 `survived` cards 时，不调用 `reviewed_cards` 模式，也不写 wiki；回复所有淘汰原因。
- 有 survivor 时，将**全部** survivor 一次性作为 `reviewed_cards` 交给 `ideate`。该模式负责原子校验，并备好 md 经 `ingest` 统一写入、lint 和返回写入位置。
- 最终回复包含：子 session 终态、survived cards 及审计记录、rejected 卡片和反驳、`ideate` 返回的 wiki/lint 结果。

完成条件：至少启动五个 self session；每张合并候选只有一个 verdict；只有 `survived` cards 进入 `reviewed_cards`；持久化批次成功通过 `ideate` 的校验与 lint。

## 输入

| Field | Required | Description |
| --- | --- | --- |
| Domain / topic | 否 | idea 生成范围，缺省全部 wiki 论文 |
| Paper list | 否 | 论文标题、wiki 路径或 URL |
| Constraints | 否 | 数据、代码、算力、时间、指标或风险偏好 |
