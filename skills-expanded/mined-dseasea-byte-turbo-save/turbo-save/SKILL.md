---
name: turbo-save
slug: turbo-save
version: 1.0.5
displayName: Turbo Save
display_name_en: Turbo Save
description: 把批量任务拆成「强模型规划 + 低成本模型并行执行」的分层工作流：省钱靠降档，提速靠并行。需具备可降档的多档模型，或可并行派发的子代理；两者皆无时不要安装。当任务包含可重复单元（批量改写、逐条检查、字段提取、多份分别生成、大批量整理）且产物对错可判定时使用。单一连续产出、需要整体立意判断、或用户明确要求全力输出时不适用。旧中文名：快省双全·快省·分层执行（检索用）。
description_en: Split batch work into a strong-model planning layer plus parallel low-cost execution. Cost savings come from downgrading, speed comes from parallelism. Requires either a cheaper model tier or parallel subagent dispatch; without at least one of them, do not install. Use when a task has repeatable units whose output can be verified mechanically.
author: "董海洋（DHY.sea）"
---

# Turbo Save

> 作者：董海洋（DHY.sea）｜版本 1.0.5
> 不绑定具体 Agent：凡支持「切分任务、并行或分批调用、按结果验收」的运行环境都可直接套用，WorkBuddy、CodeBuddy、Claude Code、Cursor、Codex、DSH 及自建 Agent 均在适用范围。

## 先看能力，再决定装不装

省钱和提速是两个独立的杠杆，依赖两种不同的环境能力。缺一个，就只拿一半；两个都缺，装了也是白装。

| 能降档到更便宜的模型 | 能并行派发 | 你能拿到的收益 |
|---|---|---|
| 是 | 是 | 省成本 50% 至 85% **＋** 提速 4 至 6 倍（实测约 6 倍） |
| 是 | 否 | 省成本 50% 至 85%，不提速（串行换成本，这是本流程的合法用法） |
| 否 | 是 | 只提速，且倍率受同账号速率限制，**低于 6 倍，未实测**；另得上下文隔离收益 |
| 否 | 否 | 无收益，**不要安装** |

一句话：**省钱只取决于能不能降档，提速只取决于能不能并行。** 单模型用户唯一稳定的结构收益是「把一次巨型上下文拆成多次小上下文」，主线程只收摘要，不会被几十份产出撑爆或截断；这一项与模型数量无关。

## 优势

1. **双收益可调。** 并行换时间，串行换成本。按任务性质取其一，不承诺两头同时拉满。
2. **三道门禁防亏。** 规模门槛、可判性、可切分性，任一不过就不拆，避免「拆了反而更贵」。
3. **先写验收再降档。** 降档前必须交出机器可验证的验收标准，杜绝产物看着对、其实跑偏。
4. **定点打回，不整批重跑。** 强制写明不合格单元的识别方式，返工只重跑坏的那几份。
5. **跨 Agent 通用。** 只依赖「切分 / 并行 / 验收」三个动作，不依赖特定工具名、模型名或计费体系。
6. **结束即报账。** 三行交代执行档位、主模型介入次数、节省来源，收益可核查而非口头宣称。

## 性能

用例：10 份、每份 600 字的中文批量改写任务。

| 项目 | 数据 | 口径 |
|---|---|---|
| 串行基线 | 113.0 秒 | 全程使用当前会话模型逐份生成 |
| 并行执行 | 18.8 秒 | 10 路并发，执行层降档 |
| 提速 | 约 6.0 倍 | 实测，同机同任务 |
| 成本下降 | 80% 至 85% | 抽检验收、单批产出量大，主模型仅保留规划与抽检 |
| 成本下降 | 50% 至 60% | 逐条全读验收，验收本身占用主模型大量额度 |
| 8 路并发提速 | 约 5 倍 | 按拥塞趋势推算，非实测 |

本表数据的成立前提是「执行层可降档 **且** 可 10 路并发」。单模型环境的提速未被实测，不应引用本表数字。

两条硬边界，不满足时收益趋近于零：

- **两个收益不可同时取满。** 并行越充分，执行层重复传递上下文的开销越高，节省比例随之下降。
- **所有比例均相对于当前会话所选的模型，不是绝对值。** 若会话本身已用最低成本档，降档无价差，收益接近于零。

## English Overview

**Turbo Save** turns a batch job into two layers: the strong model plans and inspects, while the cheapest available model does the bulk work in parallel batches. Where a cheaper tier is available and work can be dispatched in parallel, it cuts execution cost by 50–85% and wall-clock time by 4–6×.

**Requirements.** The two gains rest on two independent capabilities. Cost savings require a cheaper model tier to downgrade to; speed requires the ability to dispatch work in parallel. With a single model and no parallel dispatch, this skill yields nothing — do not install it. With a single model but parallel dispatch, expect speed and context isolation only, at a multiplier lower than 6× (not measured; the same account's rate limit applies).

**When to use.** The task breaks into repeatable units — batch rewriting, item-by-item checks, field extraction, generating several variants, bulk cleanup — and each unit's output can be verified mechanically (row counts, schema, required fields, exit status, assertions). Do not use it for a single continuous piece of writing, work that needs one coherent editorial judgment, or when the user explicitly asks for maximum quality regardless of cost.

**Advantages.**

- Two separate levers: parallel batching buys speed, serial downshifting buys cost. Neither is over-promised.
- Three gates before splitting — size, verifiability, separability — so a task is never split when splitting would cost more than it saves.
- Acceptance criteria are written *before* downgrading a single call, preventing output that looks right but is not.
- Rejections are targeted, not whole-batch reruns.
- Agent-agnostic: it relies only on split / dispatch / verify, never on a specific tool name, model name, or billing unit.
- Every run ends with a three-line ledger — execution tier, how often the strong model intervened, and where the savings came from.

**Performance.** Measured on ten 600-character Chinese rewriting tasks: 113.0 s serially with the session model, 18.8 s with 10-way parallel execution on a cheaper tier — about 6.0× faster, with 50–85% lower cost depending on whether acceptance is sampled or read in full.

**Caveats.** Gains are relative to the model already selected in the session, not absolute. Parallelism and cost savings trade against each other. If the session already runs on the cheapest tier, expect near-zero benefit.

## 术语对照

平台叫法不一，本文统一用下列说法，按你的环境自行映射：

| 本文说法 | 含义 |
|---|---|
| 主控模型 | 承担规划与验收的当前会话模型 |
| 执行模型 | 成本更低的模型、档位或后端 |
| 成本 | 该环境的计费单位：积分、额度、token 费用均可 |
| 价差 R | 高成本档单价 ÷ 低成本档单价 |
| 返工率 p | 同类任务历史打回比例，无历史取 20% |
| 派发开销 o | 每单元写指令、传上下文、读产出、验收的固定成本，约 1000 token |
| 派发 | 交给子代理执行，或按独立请求分批调用 |

## 生效规则

- 批量类任务默认启用本流程。
- 用户说「全力做」「别降档」「用最好的」时停用，全程使用当前会话模型。
- 规划与验收始终由主控模型承担。只有执行环节允许降档。

## 判据

### 判据零 规模门槛 · 决定是否值得拆分

单次执行产出不足 1500 token（中文约 1500 字）时不派发，直接在当前会话完成；合并后单次产出达到 3000 token 以上，才值得派发。

- 派发存在固定开销：写指令、传上下文、读产出、验收，每次约 800 至 1500 token，与任务量无关。
- 任务越碎，固定开销占比越高。将 50 个单元拆成 50 次调用，开销会吞掉全部收益。
- 正确做法是合并：把同类小单元并成一批再派发，不按最小单元逐个派发。

### 判据零之二 成本比门槛 · 决定降档是否可能划算

规模够了不代表降档划算。先算两个数：价差 `R`（高成本档单价 ÷ 低成本档单价），返工率 `p`（同类任务历史打回比例，无历史取 20%）。

**硬边界：`R ≤ 1 + p` 时不降档。** 成本降幅不超过返工率时，降档永远不划算，批量再大也没用。

| 返工率 p | 硬边界 R | 含义 |
|---|---|---|
| 10% | > 1.10 | 价差 1.2 倍仍可用 |
| 20% | > 1.20 | 价差 1.3 倍仍可用 |
| 30% | > 1.30 | 价差 1.5 倍才起步 |

过了硬边界，再查单单元产出是否够大，公式 `E × (R − 1 − p) / R > o`，其中 `o` 为派发固定开销（约 1000 token）。下表按 `p = 20%` 计算，与上表 `p = 10%` 的示例不同，勿混用：

| 价差 R | 最小单单元产出（o≈1000，p=20%） |
|---|---|
| 5 倍 | 1,300 token（中文约 1,300 字） |
| 3 倍 | 1,700 token |
| 2 倍 | 2,500 token |
| 1.5 倍 | 5,000 token |
| 1.2 倍 | 永不划算（R−1−p = 0） |

不满足就合并批次，而不是硬降档。会话本身已在最低成本档时 `R = 1`，直接不降档。

### 判据一 可判性 · 决定是否降档

判断产物能否被机器判对错。

- 能判：条数、格式、字段完整性、是否含指定词、能否运行通过。
- 不能判：措辞好坏、立意、合规边界、方案取舍、风格是否得体。

能判则交执行模型；不能判则留主控模型。

### 判据二 可切分性 · 决定是否并行

检查切分后的单元是否同时满足三条：

- 不共享原料
- 不依赖彼此产出
- 不争夺同一判断标准

三条全满足则并行；任一不满足则串行执行。

### 判据三 降档前置动作 · 先写验收标准

写不出可判定的验收标准，不允许降档。

- 每条步骤的验收标准不超过 5 条。
- 每条必须可被机器验证，禁止出现「质量要好」这类无法判定的表述。
- 必须写明不合格单元的识别方式，否则打回会退化成整批重跑。

### 判据四 并行前置动作 · 先写单元差异

同一指令并行会产生高度雷同的产出。

每个单元必须显式指定差异点，可选维度包括切入角度、目标读者、风格、长度、数据范围。无法指定差异点时不做并行。

## 执行顺序

0. 判规模与成本比（不过就停，别硬拆）
1. 判可判性
2. 判可切分性
3. 写验收标准
4. 写单元差异
5. 按批派发执行
6. 按标准验收
7. 定点打回不合格单元

## 参数

- 执行档：执行层取环境内可用的最低成本档；规划与验收使用主控模型。
- 并发：默认 6 路，单批上限 10 路，超出部分排队，跑完一批补下一批。
- 打回：上限 2 轮，超限则该步骤收回主控模型执行。
- 报账：任务结束给出三行——执行档位与步数、主控模型介入次数、结构性节省说明。

## 能力缺失时的降级

| 环境限制 | 处理 |
|---|---|
| 不能并行、但可换模型 | 只降档不并行，拿成本收益，不承诺提速 |
| 无低成本模型可选 | 本流程不生效，直接用当前模型执行 |
| 无法感知计费 | 仍按判据拆分，收益体现为上下文占用下降 |
| 子代理无法共享上下文 | 每个单元自带完整指令与验收标准，不依赖前序产出 |

## 禁止事项

- 将单一连续产出拆段并行：风格割裂，合并成本高于收益。
- 将批量任务切得过碎：固定开销按次重复支付，切得越细亏得越多。
- 同指令并行多份：产出雷同，等于同一篇做了多遍。
- 规划层降档：标准本身含糊，整条链路随之失效。
- 在无法判定对错的步骤降档：产物看似正确实则跑偏，返工成本高于节省。
