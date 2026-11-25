---
name: io-review
description: 审计代码的 IO 铁律。扫描新增/修改的代码，对照 docs/architecture/io_contract.md §2 三条 IO 铁律（批量优先 / 禁止 N+1 / 禁止独立串行编排）与 §3-§5 聚合并行约束，结合 docs/architecture/ai_dev_guide.md §10.2 grep 锚 rule-id 索引（R-IO-*）机械执行。命中标 🟡 待复核（信号级），最终判定权在人工 reviewer。
disable-model-invocation: true
argument-hint: "[scope] 可选：当前 PR / 指定文件路径 / loop-only（仅审计含循环的文件）；空则审计 git diff main..HEAD"
---

审计代码的 IO 铁律与聚合并行约束。范围：`$ARGUMENTS`（空则审计 git diff main..HEAD）。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 不生成代码，故第 5 步测试同步不适用。
>
> **本 Skill 是审计类 Skill（审计类第 6 个）**。"代码 ↔ IO 铁律"一致性审计。

## 第 0 步：🚫 模块 + 启用状态检查

1. 读 `BUILD_STATUS.md` §0 —— 命中 🚫 模块的文件**跳过**审计
2. 读 `INDEX.md` §0 AIWeave 采纳进度 —— 如 `docs-spec/25_io_aggregation` 标 ⬜ 未启用 → **跳过本 Skill**，提示"本工程未启用 25，跳过 io-review"

## 第 1 步：读取约束源

读以下文件（按顺序）：

1. `docs/architecture/io_contract.md` —— §1 IO 往返预算 + §2 三条铁律 + §2.1/§2.2 豁免登记 + §3 聚合器模式 + §4 并行原语 + §5 聚合约束
2. `docs/architecture/ai_dev_guide.md` §10.7 —— grep 锚 rule-id 索引（R-IO-*）
3. `docs/architecture/performance_contract.md` §4 —— 单次延迟预算（避免与 25 双源真相）
4. `docs/BUILD_STATUS.md` §11 —— 约束清单状态轨道

## 第 2 步：扫描代码范围

按 `$ARGUMENTS` 确定扫描范围：

- 空 / 当前 PR：`git diff main..HEAD --name-only` 取新增/修改的 .go 文件
- `loop-only`：仅取含 `for` / `range` 的文件
- 文件路径：直接以该路径为范围

## 第 3 步：依赖链分析（铁律二的关键）

对每段"连续多次读"的代码，判定查询间是否存在**真实数据依赖**：

- 后一次查询的入参取自前一次查询的结果（外键 / 返回字段）→ **真实依赖**，串行合法
- 后一次查询入参与前一次结果**无关** → **伪串行**，命中铁律二

依赖链是 io-review 区分"违规"与"必要串行"的核心，不可机械只看"连续 await"。

## 第 4 步：grep 锚检查

> grep 锚定位为"信号级"非"判定级"。所有命中标 🟡 待复核；最终判定由人工 reviewer 决定。
> 已在 io_contract.md §2.1 / §2.2 豁免登记表登记的位置 → 跳过；命中但未登记 → 标记。

### 检查 R-IO-N-PLUS-1：循环内单条查询（铁律一 / N+1）

```
范围：所有路径
grep 模式：'for [^{]*\{[\s\S]{0,300}?\.(Find|First|Take|Get|Query|Load|HGet|MGet?|Call)\('
误报排除：
  - 调用的已是批量 API（FindByIDs / In(...) / Pluck / Scan / 批量 MGET）
  - 循环次数硬编码 ≤ {Loop-safe-N}（如 < 5）
  - io_contract.md §2.1 已登记豁免 / 行末 // aiweave:allow=R-IO-N-PLUS-1
判定：命中且未豁免 → 🔴 严重（违反铁律一）
```

### 检查 R-IO-SERIAL-ORCH：独立串行查询编排（铁律二）

```
范围：所有路径
信号：连续 ≥ 2 个 {读操作} 各自 if err != nil 串行展开
判定（结合第 3 步依赖链分析）：
  - 无真实依赖（伪串行）→ 🔴 严重（违反铁律二），建议改聚合器 / 扇出并行
  - 有真实依赖 → 跳过（合法），可提示"是否可预取合并"
误报排除：
  - io_contract.md §2.2 已登记依赖链豁免 / 行末 // aiweave:allow=R-IO-SERIAL-ORCH
```

### 检查 R-IO-LOOP-WRITE：循环内单条写

```
范围：所有路径
grep 模式：'for [^{]*\{[\s\S]{0,300}?\.(Create|Save|Insert|Update|HSet|Set|Exec)\('
误报排除：
  - 批量写 / pipeline（CreateInBatches / pipeline.Exec）
  - 循环次数硬编码 ≤ {Loop-safe-N}
  - 行末 // aiweave:allow=R-IO-LOOP-WRITE
```

### 检查 R-IO-NO-AGGREGATOR：多次跨实例读未走聚合器

```
范围：所有路径
信号：同一函数内 ≥ {N} 次跨实例 / 跨表读，未经聚合器分组批量
误报排除：
  - 已用聚合器（Preload / Fetch 编排）
  - 行末 // aiweave:allow=R-IO-NO-AGGREGATOR
```

### 检查 R-IO-LOOP-RPC：循环内单条 RPC / 外部调用

```
范围：所有路径
grep 模式：'for [^{]*\{[\s\S]{0,300}?\.(Call|Invoke|Do|Post|Get)\(' 命中 api/ 客户端
误报排除：
  - 批量接口 / 并行扇出
  - 行末 // aiweave:allow=R-IO-LOOP-RPC
```

### 检查 §3 聚合器只读契约：共享指针被就地修改

```
信号：Slot.Value() / single-flight 共享结果指针后，对其字段赋值（v.{Field} = ...）
判定：→ 🔴 严重（违反共享只读铁律，并发写竞争）；应先深拷贝
```

### 检查 §1 往返预算完整性：新增数据访问方法未登记预算

```
判定：git diff 含新增的"集合访问资源"方法，但 io_contract.md §1 往返预算 / §3 原语清单未更新
未登记 → 标 🟡（提示补登记）
```

## 第 5 步：IO 回归提示（如有计数断言测试）

如 git diff 含 IO 计数断言测试（`*_test.go` 含查询次数断言）：

- 提示运行该测试，确认处理 N 条数据时查询次数为 O(1) 而非 O(N)
- 缺失 N+1 回归测试的新增"集合访问"方法 → 提示按 io_contract.md §7.1 补齐

## 第 6 步：输出格式

按严重程度分组：

```
🔴 严重 — 违反 IO 铁律（无合法豁免）
  - [R-IO-N-PLUS-1] {文件}: line {N}  → 循环内单条查询，建议批量 + map 装配
  - [R-IO-SERIAL-ORCH] {文件}: line {N}  → 独立读串行（无依赖），建议聚合器并行
  - [共享只读] {文件}: line {N}  → 就地改共享指针字段

🟡 待复核 — grep 锚命中 / 预算未登记（信号级，需人工判定）
  - [R-IO-LOOP-WRITE] {文件}: line {N}  → {代码片段}
  - [R-IO-NO-AGGREGATOR] {文件}: line {N}  → {代码片段}
  - [§1 未登记] {文件}: {Method}  → 建议补 io_contract.md §1 / §3

🟢 通过 — 未命中铁律，聚合 / 并行得当

📊 统计
  - 扫描文件数：N（含循环：L）
  - 违反铁律：{N+1 计数} / {串行编排计数}
  - 建议人工 reviewer 复核：M 处
```

## 第 7 步：测试同步

**不适用**——本 Skill 不生成业务代码。但建议对新增"集合访问"方法在 PR 内附 IO 计数断言测试（io_contract.md §7.1）。

## 第 8 步：文档同步

本 Skill 不直接修改文档；审计输出应记录到 PR/工单，让用户追踪修复进度，并对应到 BUILD_STATUS §11 约束清单状态轨道的"已启用条目数"。

## 与其他 Skill 的关系

- 与 `performance-review`：维度互补——22/performance 管单次延迟，25/io 管往返次数与并行化；两者常同时命中
- 与 `concurrency-review`：聚合器的 worker pool / Slot 共享指针涉及并发安全，交叉复核
- 与 `new-service` / `new-scheduled-task`：建议在生成"集合访问 / 多依赖编排"方法时自动触发


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
