---
name: concurrency-review
description: 审计代码的并发安全性。扫描新增/修改的代码，对照 docs/architecture/concurrency_safety.md §2 共享状态注册表与 §6 危险操作清单，结合 docs/architecture/ai_dev_guide.md §10.1 grep 锚 rule-id 索引（R-CONC-*）机械执行。命中标 🟡 待复核（信号级），最终判定权在人工 reviewer。
disable-model-invocation: true
argument-hint: "[scope] 可选：当前 PR / 指定文件路径 / 指定 service 模块；空则审计 git diff main..HEAD"
---

审计代码的并发安全性。范围：`$ARGUMENTS`（空则审计 git diff main..HEAD）。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 不生成代码，故第 5 步测试同步不适用。
>
> **本 Skill 是 新增的审计类 Skill**。"代码 ↔ 约束"一致性审计，与 `doc-sync-check`（代码 ↔ 文档一致性）互补不替代。

## 第 0 步：🚫 模块 + 启用状态检查

1. 读 `BUILD_STATUS.md` §0 —— 命中 🚫 模块的文件**跳过**审计（不报问题）
2. 读 `INDEX.md` §0 AIWeave 采纳进度 —— 如 `docs-spec/20_concurrency_safety` 标 ⬜ 未启用 → **跳过本 Skill**，提示"本工程未启用 20，跳过 concurrency-review"

## 第 1 步：读取约束源

读以下文件（按顺序）：

1. `docs/architecture/concurrency_safety.md` —— §2 共享状态注册表 + §3 锁策略 + §4 channel 清单 + §6 危险操作清单
2. `docs/architecture/ai_dev_guide.md` §10.1 —— grep 锚 rule-id 索引（R-CONC-*）
3. `docs/BUILD_STATUS.md` §11 —— 约束清单状态轨道（确认哪些 rule-id 启用）

## 第 2 步：扫描代码范围

按 `$ARGUMENTS` 确定扫描范围：

- 空：`git diff main..HEAD --name-only` 取新增/修改的 .go 文件
- 文件路径：直接以该路径为范围
- service 模块：`service/{module}/**/*.go`

## 第 3 步：10 项 grep 锚检查

> grep 锚定位为"信号级"非"判定级"。所有命中标 🟡 待复核；最终判定由人工 reviewer 决定是否阻断合并。

### 检查 R-CONC-LOCK-IO：锁内做网络 IO

```
grep 模式：'\.Lock\(\)[\s\S]{0,500}?(http\.|Mysql|Redis|tlog\.)'
误报排除：
  - RLock 中读小对象
  - 同步只读类操作（如 Redis GET 单次 < 1ms 的情况）
  - 行末含 // aiweave:allow=R-CONC-LOCK-IO 注解
```

### 检查 R-CONC-LOCK-LOG：锁内打日志

```
grep 模式：'\.Lock\(\)[\s\S]{0,300}?(tlog\.|log\.)'
误报排除：
  - 异常路径的关键日志（不可避免）
  - 行末含 // aiweave:allow=R-CONC-LOCK-LOG 注解
```

### 检查 R-CONC-MAP-RACE：map 并发写

```
判定：文件含 `var .* map\[` 且同文件存在 `go func` 且未引用 sync.RWMutex / sync.Map
误报排除：
  - 局部 map 不跨 goroutine
  - main / init 中只读 map（启动后只读）
  - 行末含 // aiweave:allow=R-CONC-MAP-RACE 注解
```

### 检查 R-CONC-DOUBLE-CLOSE：关闭已关闭的 channel

```
判定：`close\([^)]+\)` 同一 channel 在文件内出现多次且无 sync.Once 保护
误报排除：
  - 单一所有者 close 模式
  - 行末含 // aiweave:allow=R-CONC-DOUBLE-CLOSE 注解
```

### 检查 R-CONC-SEND-CLOSED：向已关闭的 channel 发送

```
判定：`<-` channel 关闭后仍有 send 路径（静态分析判定，准确率较低 → 优先标 🟡）
```

### 检查 R-RESOURCE-DEFER-LOOP：defer 在 for 循环内

```
grep 模式：'for [^{]*\{[\s\S]{0,300}?defer '
误报排除：
  - 循环体内显式调用 Close 而非 defer
  - 循环次数 ≤ {Loop-defer-safe}（如 < 10，影响小）
  - 行末含 // aiweave:allow=R-RESOURCE-DEFER-LOOP 注解
```

### 检查 R-CONC-GOROUTINE-LEAK：忽略 ctx.Done()

```
判定：`go func` 块内无 `ctx\.Done\(\)` 且无 `select` 等退出信号
误报排除：
  - 短周期任务（< 1s）
  - 由 errgroup.WithContext / sync.WaitGroup 跟踪
  - 行末含 // aiweave:allow=R-CONC-GOROUTINE-LEAK 注解
```

### 检查 R-CONC-COUNTER-CONTENTION：超高频计数单点争用

```
判定：热路径单一 atomic.Add / Mutex 计数器被高频写（单点 Mutex / 单 atomic 计数）
误报排除：
  - 已分片计数（striped）读时求和（concurrency_safety.md §2）
  - 非热路径 / 低频计数
  - 行末含 // aiweave:allow=R-CONC-COUNTER-CONTENTION 注解
```

### 检查 R-CONC-FALSE-SHARING：分片计数未对齐缓存行

```
判定：分片 / 原子计数器相邻字段未按缓存行对齐（false-sharing，分片白拆）—— 非 grep 可判（人工 / AST）
误报排除：
  - 已 padding 到 64B / 独占 cache line
  - 行末含 // aiweave:allow=R-CONC-FALSE-SHARING 注解
```

### 检查 §2 注册表完整性：新增共享状态未登记

```
判定：git diff 中含 `var .* sync.Mutex` / `sync.RWMutex` / `sync.Map` / `chan T` / `make(chan T, N)`
对照：concurrency_safety.md §2 / §4.1 是否新增对应行
未登记 → 标 🔴 严重（漏登记是结构性缺陷，不是单点 grep 误报）
```

## 第 4 步：输出格式

按严重程度分组：

```
🔴 严重 — 新增共享状态未在 concurrency_safety.md §2 / §4.1 登记
  - {文件路径}: {变量名}  → 建议补 §2 / §4.1 + 同步 BUILD_STATUS §11

🟡 待复核 — grep 锚命中（信号级，需人工判定）
  - [R-CONC-LOCK-IO] {文件路径}: line {N}  → {代码片段}
  - [R-RESOURCE-DEFER-LOOP] {文件路径}: line {N}  → {代码片段}
  - [R-CONC-COUNTER-CONTENTION] {文件路径}: line {N}  → {代码片段}
  - [R-CONC-FALSE-SHARING] {文件路径}: {结构体}  → 分片字段无 padding（人工/AST 判定）
  - ...

🟢 通过 — 未命中危险模式

📊 统计
  - 扫描文件数：N
  - 命中规则数：M（按 rule-id 分布）
  - 建议人工 reviewer 复核：M 处
```

## 第 5 步：测试同步

**不适用**——本 Skill 不生成业务代码。但建议运行 `go test -race ./...` 在审计前后各跑一次，作为兜底验证。

## 第 6 步：文档同步

本 Skill 不直接修改文档；但**审计输出应记录到 PR/工单**，让用户追踪修复进度，并对应到 BUILD_STATUS §11 约束清单状态轨道的"已启用条目数"。

## 与其他 Skill 的关系

- 与 `doc-sync-check`：审计维度互补（前者代码 ↔ 文档；本 Skill 代码 ↔ 约束）
- 与 `performance-review`：并列的审计类 Skill；并发问题往往是性能问题的根因
- 与 `new-service` / `new-controller`：建议在 `/new-*` 生成代码后自动触发 `/concurrency-review`，作为审计兜底


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
