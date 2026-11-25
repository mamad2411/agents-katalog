---
name: okr-skill
description: "OKR 协作 Skill：与用户把模糊目标写成可度量的 Objective + Key Results，并在周期内映射、周更与复盘。含 OKRClaw 四级十六域九十六实践原子索引。触发条件：(1) 定季度/迭代目标、写 KR、复盘；(2) 只有任务清单无成功标准；(3) 对话发散需对齐「做到什么算赢」。不替代公司绩效制度。"
license: MIT
metadata:
  openclaw:
    emoji: 🎯
---

## 复制给 AI

- **本 Skill 唯一入口**：当前文件 `SKILL.md`（仓库根）。
- **聚合入口**：[`FOR_AI.md`](FOR_AI.md)。
- **规范总纲**：[`docs/RFC-OKRCLAW.md`](docs/RFC-OKRCLAW.md)（讨论深度问题时 **SHOULD** 引用其章节）。
- **实践原子索引**：[`practices/README.md`](practices/README.md)（96 条，16 域 × 6）。
- **术语表**：[`docs/GLOSSARY.md`](docs/GLOSSARY.md)。

# OKR.skill — 让 AI 和你一起「说到做到、还能证明」

## 语言

根据用户**第一条消息**的语言，全程使用同一语言。

## 何时激活

- 用户要：**定目标、拆季度/迭代、写 KR、对齐团队、周更、复盘**。
- 用户只有 **Todo 列表**，没有「怎样算达成」。
- 对话 **发散**，需要把每条工作映射到「为什么服务」。
- 用户明确说「用 OKR」「按关键结果来」「用 OKRClaw」。

## 重要声明

- 本 Skill **用于协作与执行对齐**，**不替代**用人单位的绩效考核、晋升或合同义务。
- **OKRClaw** 仅为本仓库内对「4×16×96 实践分类」的简称；与 [PUAClaw](https://github.com/puaclaw/PUAClaw) **仅形态类比，内容无关**。见 [`docs/RFC-OKRCLAW.md`](docs/RFC-OKRCLAW.md)。

## OKR 是什么（执行版）

| 要素 | 要求 |
|------|------|
| **Objective (O)** | 定性、有方向、周期内可感知**价值变化**（通常 1 个主 O）。 |
| **Key Results (KRs)** | **3–5 条**可度量**结果**（outcome），每条有**证据**约定。 |
| **周期** | 常见**季度**；可约定双周/月（Phase 0 写死起止）。 |
| **健康度** | 周期末 KR **0.6–0.7** 常表示有挑战；**全 1.0** 可反思是否偏保守。 |

## 实践原子索引（卡点 → 域）

| 用户卡点 | 优先打开（`practices/`） |
|----------|---------------------------|
| O 像口号、无时间感 | [`01-l1-objective-design`](practices/01-l1-objective-design/) |
| KR 不可测、无口径/基线 | [`02-l1-kr-measurable`](practices/02-l1-kr-measurable/) |
| 把「上线/写完」当 KR | [`03-l1-outcome-vs-output`](practices/03-l1-outcome-vs-output/) |
| 范围蔓延、周期不清 | [`04-l1-scope-period`](practices/04-l1-scope-period/) |
| 与上级目标挂不上 | [`05-l2-strategic-align`](practices/05-l2-strategic-align/) |
| 等人、等别的团队 | [`06-l2-dependencies`](practices/06-l2-dependencies/) |
| KR 太多、全 P0 | [`07-l2-prioritization`](practices/07-l2-prioritization/) |
| 进度没人知道 | [`08-l2-transparency`](practices/08-l2-transparency/) |
| 周更敷衍、乱打分 | [`09-l3-weekly-score`](practices/09-l3-weekly-score/) |
| 没有证据、对不上数 | [`10-l3-evidence`](practices/10-l3-evidence/) |
| 风险爆了才说 | [`11-l3-risk-correction`](practices/11-l3-risk-correction/) |
| 任务不知道服务哪条 KR | [`12-l3-initiative-map`](practices/12-l3-initiative-map/) |
| 多个 O 抢资源 | [`13-l4-multi-okr`](practices/13-l4-multi-okr/) |
| 跨团队对不齐 | [`14-l4-cross-team`](practices/14-l4-cross-team/) |
| 手抄表、易错 | [`15-l4-tooling`](practices/15-l4-tooling/) |
| 复盘走过场、下期重复踩坑 | [`16-l4-retro-inherit`](practices/16-l4-retro-inherit/) |

**用法**：进入对应目录，阅读 `README.md` 再按需打开单条原子 `.md`；在对话中可写「按 A02-03 自检」。

## 操作顺序

### Phase 0：对齐语境

与用户确认并写下：

- [ ] **周期**：开始日、结束日。
- [ ] **范围**：个人 / 项目 / 小团队；**不在**范围内的不写进 O。
- [ ] **成功语言**：用什么词算「赢」。
- [ ] **数据源**：指标从哪来 — 没有则先设计「建立度量」类 KR。

输出：**一段话摘要** + **约束清单**。

### Phase 1：起草 O + KRs

引导产出 **1 个 O + 3–5 个 KR**（每条：陈述、度量、基线、目标值、证据）。模板：

```markdown
## Objective
> 

## Key Results
| ID | Key Result | 度量方式 | 基线 | 目标 | 证据来源 |
|----|------------|----------|------|------|----------|
| KR1 | | | | | |
```

**自检**：结合 L1 域原子（[`01`](practices/01-l1-objective-design/)–[`04`](practices/04-l1-scope-period/)）逐条过一遍。

### Phase 2：工作映射

每项工作标注 **→ KRn**；不服务任何 KR 的归入运维桶或触发 OKR 变更讨论。参考 [`12-l3-initiative-map`](practices/12-l3-initiative-map/)。

### Phase 3：周更

更新进度分 0.0–1.0 + 证据摘要 + 风险。参考 [`09-l3-weekly-score`](practices/09-l3-weekly-score/)、[`10-l3-evidence`](practices/10-l3-evidence/)。

### Phase 4：周期末复盘

逐条 KR 终分、根因、下期继承。参考 [`16-l4-retro-inherit`](practices/16-l4-retro-inherit/)。

## 反模式库（速查）

| 反模式 | 怎么改 |
|--------|--------|
| 任务当 KR | [`03-l1-outcome-vs-output`](practices/03-l1-outcome-vs-output/) |
| KR 不可测 | [`02-l1-kr-measurable`](practices/02-l1-kr-measurable/) |
| KR >5 或重复 | [`07-l2-prioritization`](practices/07-l2-prioritization/) |
| O 与 KR 无逻辑链 | [`01-l1-objective-design`](practices/01-l1-objective-design/) + KR 重写 |

## 与 [pua-skill](https://github.com/tanweai/pua) 的关系

- **okr-skill**：目标、度量、对齐、复盘。  
- **pua-skill**：卡住时的穷尽与验证。  
- **组合**：先 OKR 再执行；遇阻可并行用 PUA，**叙事不混用**。

## 不做的事

- 不替用户做**绩效评级**或**承诺晋升**。  
- 不**编造**指标完成度。  
- 不将 OKR **强加**给未同意的协作者。

## 路径约定

- **`{repoRoot}`**：仓库根。  
- 示例索引 [`examples/README.md`](examples/README.md)；完整表见 [`examples/sample-okr.md`](examples/sample-okr.md)。配方 [`recipes/quarterly-okr.md`](recipes/quarterly-okr.md)、[`recipes/biweekly-okr.md`](recipes/biweekly-okr.md)。
