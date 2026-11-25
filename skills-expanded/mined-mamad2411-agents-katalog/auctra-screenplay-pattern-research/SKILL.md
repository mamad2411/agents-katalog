---
name: auctra-screenplay-pattern-research
description: Use when analyzing, grouping, auditing, or adapting collections of Chinese screenplay, short-drama, novel, DOCX, Markdown, or reviewed video-to-script samples for Auctra, including source-safe symbol restoration, semantic block overlays, calibration/holdout/exploratory splits, Pattern Lens evidence, dramatic recipe promotion, blind evaluation, and accepted screenplay handoff to Scaena.
---

# Auctra 剧本样本研究

把多份小说、短剧或视频反推剧本变成可追溯的研究资产。目标是抽象可验证模式并服务原创项目，不是把某一部作品全文塞进提示词仿写。

## 输入

- 源文件或 Auctra corpus refs，以及来源、权限、只读状态和转换方式。
- 研究目标：格式恢复、题材分组、模式研究、recipe、盲测、原创剧本或生产交接。
- 可选：当前 Auctra project、Anatomia analysis 或 Scaena handoff refs。

## 先读取的项目事实

在 Yeisme 仓库内处理当前 28 个样本时，按需读取：

- `data/screenwriting-media-creation/设计/样本分组与评测矩阵.md`
- `data/screenwriting-media-creation/设计/编剧符号与语义块规范.md`
- `openspec/changes/auctra-sample-driven-screenwriting-intelligence-v1/`
- `cli/auctra/openspec/changes/auctra-screenplay-corpus-intelligence-v1/`

需要通用类型、符号、Pattern Lens 和晋级规则时，读取 [research-contract.md](references/research-contract.md)。

## 工作流

### 1. 先冻结来源，不先“清洗”

1. 记录 source ref、digest、permission、reference-only、media refs 和转换状态。
2. 比对 DOCX/Markdown 时区分实际段落文本、修订痕迹和 XML 重复；不要用 raw XML 字符计数推断符号丢失。
3. 保留原始换行、`△/▲`、VO/OS、图片链接和异常文本。
4. 缺字、孤立 `：对白`、异常集/场编号或图片缺失只生成 repair issue；不要猜回原文。

### 2. 建立题材组与用途隔离

- 题材组描述叙事引擎，不替代题材标签。
- `calibration` 用于 parser、符号和 gold set 校准。
- `holdout` 只用于冻结版本后的盲测；正文、embedding、答案和摘录不得进入调参、recipe 或生成上下文。
- `exploratory` 用于权限、格式、续作和新模式压力测试，不计入稳定 benchmark。
- 同源、续作、重写版和同一视频/剧本必须锁在同一 split。

样本较少时优先做分层均衡，不做纯随机划分。当前 28 个样本使用四组各 `2 / 3 / 2`，总计 `8 / 12 / 8`。

### 3. 只恢复语义覆盖，不批量插图标

采用三层：

```text
source-faithful text
  -> semantic overlay candidate
  -> consumer icon + label presentation
```

- Source 层字节不变。
- Overlay 保存 source span/digest、source marker、normalized kind、attributes、confidence、review status 和 repair reason。
- Consumer 使用 Lucide icon、短标签、tooltip 与 aria label；图标不是唯一语义。
- 现有 Fountain enum 保持稳定；episode、cast、prop、VO/OS、media ref 等留在 additive overlay/attributes。
- Unknown 保持 unsupported/needs-review，不静默转成 action。

### 4. 检查 Auctra 当前能力再运行

进入 `cli/auctra`，读取本地 `AGENTS.md`，先检查真实命令：

```bash
auctra corpus --help
auctra corpus import --help
auctra corpus segment --help
auctra corpus extract --help
```

导入命令必须显式给出权限；例如：

```bash
auctra corpus import --from ./samples --kind short_drama_screenplay --permission unknown --json
```

只有 installed help/contract 已列出 `audit`、`screenplay-zh-short-drama-v1`、`dramatic-pattern-v1` 或等价 approved surface 时，才使用其真实语法。若未实现，返回 `capability_missing` 并指向 `cli/auctra/openspec/changes/auctra-screenplay-corpus-intelligence-v1/`；不要拿 `chapter` 或 `satisfaction-v1` 冒充短剧解析。

结构化 corpus、overlay、review、recipe、link 和 eval 必须由 Auctra CLI/application service 写入，不手写 `.auctra/**`、corpus JSON/YAML/JSONL 或 SQLite row。

### 5. 以证据建立 Pattern Lens

先从 accepted semantic blocks 计算边界、节奏、角色出入、动作/对白比例和生产形状，再提出解释性 candidate。每个 pattern 至少保存：

- lens 与可反驳 claim；
- 正例、反例、source refs/spans；
- 跨来源覆盖与单一样本支配；
- 权限、split、置信度和 review 状态；
- 适用边界与失败条件。

模型总结没有 source span 时只能是 finding，不能成为 accepted pattern。

### 6. 把模式晋级为抽象 Recipe

- `exploratory`：允许讨论，不能驱动正式生成。
- `candidate`：至少两个独立来源并经人工抽象审核，可在 sandbox 项目试用。
- `production_ready`：至少三个独立来源、权限允许、holdout 通过，并完成原创性与生产性审核。

Recipe 只保存结构、节奏、角色功能、信息差、情绪兑现、场景/资产预算、禁止表达和 evidence refs。不得复制专名、长台词或独特桥段。

### 7. 通过 Auctra 项目链接创作

Recipe 只能通过 versioned project link 影响 Development、Structure、Scene、Script candidate 或 Quality Eval。结果进入 Auctra review；不自动更新 canon。

需要写具体场景时交给 `$screenplay-scene-writer`，并只传 accepted project brief/recipe refs 与必要 source facts，不传 holdout 正文。

### 8. 视频来源先走 Anatomia

用户给热门剧视频时，先用 `$anatomia-video-analysis-router` 建立候选观察与时间证据，再经 `$anatomia-storyboard-reviewer` 和 `$anatomia-scaena-learning-loop` 复核。只有审核后的剧本/叙事观察才能进入本技能的 pattern evidence；视频观察不能自动变成剧情事实或 recipe。

### 9. 生产只接 accepted screenplay

固定顺序：

```text
sample evidence -> dramatic recipe -> Auctra project candidate
-> human accepted screenplay -> Auctra ProductionHandoff
-> Scaena ShotIntent -> ShotGenerationSpec
```

Corpus item、semantic block、pattern 或 recipe 不能直接创建 ShotIntent。生产操作交给 `$scaena-production-operator`。

## 输出

返回一个紧凑研究 handoff：

```text
source_integrity
permission_state
group_split_matrix
semantic_overlay_status
repair_issues
pattern_evidence_refs
recipe_readiness
holdout_status
project_link_or_blocker
accepted_screenplay_gate
next_real_command
```

## 边界

- 不假定“用户持有文件”等于拥有训练、生成、摘录或发布权。
- 不批量重写源稿，不因高置信度自动接受。
- 不让 holdout 参与提示词、规则或 recipe 调优。
- 不保存 raw prompt、provider payload、隐藏提示、私密工具参数或完整思维链。
- 不以单一样本模式、fixture 成功、命令 exit 0 或视频热度传闻证明效果。

## 验证

- 源文件组合 digest 前后相同。
- 分组无重漏，同系列同 split。
- 每个 accepted block/pattern 可回到 source span/digest。
- holdout contamination 为零，eval run 不可覆盖。
- Recipe 有多来源、反例、权限、原创性和生产性门。
- 新剧本经 Auctra review 后才允许 Scaena handoff。
