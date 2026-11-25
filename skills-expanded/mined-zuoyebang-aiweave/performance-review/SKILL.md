---
name: performance-review
description: 审计代码的性能合约。扫描新增/修改的代码，对照 docs/architecture/performance_contract.md §2 热路径清单与 §3-§6 性能约束，结合 docs/architecture/ai_dev_guide.md §10.2 grep 锚 rule-id 索引（R-PERF-*）机械执行。命中标 🟡 待复核（信号级），最终判定权在人工 reviewer。
disable-model-invocation: true
argument-hint: "[scope] 可选：当前 PR / 指定文件路径 / hot-path-only（仅审计热路径文件）；空则审计 git diff main..HEAD"
---

审计代码的性能合约。范围：`$ARGUMENTS`（空则审计 git diff main..HEAD）。

> 公共步骤模板见 [skills-spec/01_skill_authoring_guide.md](path) §A-§E。本 Skill 不生成代码，故第 5 步测试同步不适用。
>
> **本 Skill 是 新增的审计类 Skill**。"代码 ↔ 约束"一致性审计。

## 第 0 步：🚫 模块 + 启用状态检查

1. 读 `BUILD_STATUS.md` §0 —— 命中 🚫 模块的文件**跳过**审计
2. 读 `INDEX.md` §0 AIWeave 采纳进度 —— 如 `docs-spec/22_performance_contract` 标 ⬜ 未启用 → **跳过本 Skill**，提示"本工程未启用 22，跳过 performance-review"

## 第 1 步：读取约束源

读以下文件（按顺序）：

1. `docs/architecture/performance_contract.md` —— §1 SLA + §2 热路径清单 + §3 内存预算 + §4 数据访问约束 + §6 背压策略 + §7 性能回归
2. `docs/architecture/ai_dev_guide.md` §10.2 —— grep 锚 rule-id 索引（R-PERF-* / R-CACHE-* / `R-LOCALMIRROR-STALE-READY`）；§10.10 尾延迟 / 运行时调优类（R-TAIL-*）；§10.9 部署运行时（R-DEPLOY-GOMAXPROCS / R-RUNTIME-MEMLIMIT）
3. `docs/circuit_breaker/circuit_breaker_design.md` §2 —— 熔断参数（避免与 22 双源真相）
4. `docs/BUILD_STATUS.md` §11 —— 约束清单状态轨道

## 第 2 步：扫描代码范围

按 `$ARGUMENTS` 确定扫描范围：

- 空 / 当前 PR：`git diff main..HEAD --name-only` 取新增/修改的 .go 文件
- `hot-path-only`：仅取 `performance_contract.md §2` 清单中列出的文件
- 文件路径：直接以该路径为范围

## 第 3 步：热路径分类

对每个被扫描的 .go 文件，判定其是否属于"热路径"：

- 在 §2 热路径清单中显式列出 → 热路径
- 入口路由匹配 §2 清单中的路径 → 热路径
- service 方法被热路径直接或间接调用（≤ 1 跳）→ 准热路径
- 其他 → 普通路径

热路径文件适用 §3 全部 grep 锚 + §2.2 "禁止操作"列；普通路径仅适用 §3 中标 "all-paths" 的 grep 锚。

## 第 4 步：grep 锚检查（R-PERF-* 7 项 + R-DEPLOY/R-RUNTIME/R-TAIL 尾延迟 6 项 + SLO/profiling 2 项）

> grep 锚定位为"信号级"非"判定级"。所有命中标 🟡 待复核；最终判定由人工 reviewer 决定。
>
> R-DEPLOY-GOMAXPROCS / R-RUNTIME-MEMLIMIT / R-TAIL-* 多为信号级（🟡），grep 仅给线索，判定结合 deployment.md §4/§7 + performance_contract.md §6.4 时序与幂等语义。

### 检查 R-PERF-HOT-REFLECT：热路径用反射

```
范围：热路径 + 准热路径文件
grep 模式：'reflect\.'
误报排除：
  - 文件含 //go:build !hotpath 标记
  - 行末含 // aiweave:allow=R-PERF-HOT-REFLECT 注解
```

### 检查 R-PERF-HOT-FMT：热路径用 fmt.Sprintf

```
范围：热路径 + 准热路径文件
grep 模式：'fmt\.Sprintf\(|fmt\.Errorf\('
误报排除：
  - 错误路径（与 if err != nil 相邻）—— 错误路径不算热
  - 仅 fmt.Errorf 用于 wrap error
  - 行末含 // aiweave:allow=R-PERF-HOT-FMT 注解
```

### 检查 R-PERF-LOOP-DB-QUERY：for 循环内 DB 查询（N+1）

```
范围：所有路径
grep 模式：'for [^{]*\{[\s\S]{0,300}?\.(Find|First|Where|Take)\('
误报排除：
  - 显式批量 API（In(...) / Pluck / Scan）
  - 循环次数硬编码 ≤ {Loop-DB-safe}（如 < 5）
  - 行末含 // aiweave:allow=R-PERF-LOOP-DB-QUERY 注解
```

### 检查 R-PERF-LOOP-ALLOC：for 循环内大对象分配

```
范围：热路径 + 准热路径
判定：循环体内含 make([]T, N) 或 new(big-struct) 且 N > 1024 或 struct 字段数 > 20
误报排除：
  - 循环前已 capacity 预分配
  - 仅在 error 分支分配
  - 行末含 // aiweave:allow=R-PERF-LOOP-ALLOC 注解
```

### 检查 R-PERF-FULL-COUNT：全表 COUNT(*)

```
范围：所有路径
grep 模式：'COUNT\(\*\)\s+FROM'，且无 WHERE 或 WHERE 列无索引
误报排除：
  - 小表（行数 < {Small-table-rows}，如 < 1 万）
  - 后台批处理任务（明确非热路径）
  - 行末含 // aiweave:allow=R-PERF-FULL-COUNT 注解
```

### 检查 R-RESOURCE-SLEEP-SYNC：time.Sleep 做同步

```
范围：所有路径
grep 模式：'time\.Sleep\(' 出现在 `go func` 或 `for` 内
误报排除：
  - 重试退避（指数退避例外）
  - 测试代码（*_test.go）
  - 行末含 // aiweave:allow=R-RESOURCE-SLEEP-SYNC 注解
```

### 检查 R-CACHE-LARGE-KEY：Redis 大 Key

```
范围：所有路径
判定：`\.Set\(.*,.*` 紧随大对象（> 1 MB 序列化）或 SADD 巨量元素（一次 > 1000）
误报排除：
  - 显式分片代码（key:%s:shard:%d）
  - 行末含 // aiweave:allow=R-CACHE-LARGE-KEY 注解
```

### 检查 R-DEPLOY-GOMAXPROCS：GOMAXPROCS 未对齐容器 CPU limit

```
范围：main.go / 子命令入口 + 编排清单
判定：编排有 cpu limit 而代码无 automaxprocs / maxprocs.Set / GOMAXPROCS 对齐（用默认宿主核数 → 节流抖动抬 P99）
误报排除：
  - 已用 automaxprocs（deployment.md §7）
  - 行末含 // aiweave:allow=R-DEPLOY-GOMAXPROCS 注解
```

### 检查 R-RUNTIME-MEMLIMIT：GOMEMLIMIT 未设 / 未对齐 mem limit

```
范围：main.go / 子命令入口 + 编排清单
判定：编排有 mem limit 但无 GOMEMLIMIT / debug.SetMemoryLimit（GC 太晚 → OOMKilled）
误报排除：
  - 已设软上限（~90% mem limit，deployment.md §7）
  - 行末含 // aiweave:allow=R-RUNTIME-MEMLIMIT 注解
```

### 检查 R-TAIL-RETRY-NOBUDGET：重试无预算

```
范围：入口 / 编排 / api 调用 + 重试库使用处
判定：retry 循环 / 库调用无全局预算 / 令牌限制（重试风暴放大级联故障）
误报排除：
  - 已接重试预算（≤X% + 与熔断联动，performance_contract.md §6.4）
  - 行末含 // aiweave:allow=R-TAIL-RETRY-NOBUDGET 注解
```

### 检查 R-TAIL-RETRY-NOJITTER：backoff 无 jitter

```
范围：重试退避计算处
grep 模式：退避计算（backoff / `<<` 指数项）无 rand 抖动项
误报排除：
  - 含随机抖动（rand.* 叠加退避）
  - 行末含 // aiweave:allow=R-TAIL-RETRY-NOJITTER 注解
```

### 检查 R-TAIL-HEDGE-UNSAFE：对冲 / 重试包裹非幂等调用

```
范围：hedge / retry 入口下游
判定：hedge / retry 入口下游为写类方法（Create / Update / Delete / Incr）→ 重复副作用
误报排除：
  - 调用幂等（幂等 Key / 唯一索引）
  - 行末含 // aiweave:allow=R-TAIL-HEDGE-UNSAFE 注解
```

### 检查 R-TAIL-COLDSTART：冷启 readiness 早于预热

```
范围：启动时序 / readiness handler
判定：readiness 置 true 早于缓存 / 连接池预热完成（流量打到冷实例 → 头部 P99 飙高）
对照：deployment.md §4 启动就绪时序（readiness 晚于预热）
误报排除：
  - readiness 晚于预热
  - 行末含 // aiweave:allow=R-TAIL-COLDSTART 注解
```

### 检查 P999 SLO 已定义？

```
判定：热路径方法所属路由在 performance_contract.md §1 仅定义 P99，未定义 P999 尾延迟目标
未定义 → 标 🟡 待复核（尾延迟治理缺上界，建议补 §1 P999 SLO）
```

### 检查 热路径回归是否有生产 profiling(pprof) 兜底？

```
判定：git diff 触及热路径文件，但工程未暴露 /debug/pprof 持续采集（performance_contract.md §7.4 / observability.md §3.3）
缺兜底 → 标 🟡 待复核（热路径回归无生产侧定位手段，建议接入 pprof）
```

### 检查 §2 热路径清单完整性：新增热路径方法未登记

```
判定：git diff 含新增的 service 方法，且其入口路由出现在已有 §2 清单中
对照：方法 docs §4.N.3 处理步骤是否含 [HOT-PATH] 标记
未标 → 标 🔴 严重（清单遗漏是结构性问题）
```

## 第 5 步：性能回归提示（如有 bench）

如 git diff 含 `*_bench_test.go` 改动：

- 提示运行 `go test -bench=. -benchmem ./...` 并与基线比对
- P99 偏差 > 20% 或 allocs/op 增加 > 10% → 提示在 PR 中附 benchmark 输出供 reviewer 评估

## 第 6 步：输出格式

按严重程度分组：

```
🔴 严重 — 新增热路径方法未在 performance_contract.md §2 登记 / 伪码缺 [HOT-PATH] 标记
  - {文件}: {Method}  → 建议补 §2 + 伪码标记

🟡 待复核 — grep 锚命中（信号级，需人工判定）
  - [R-PERF-HOT-REFLECT] {文件路径}: line {N}  → {代码片段}
  - [R-PERF-LOOP-DB-QUERY] {文件路径}: line {N}  → {代码片段}
  - [R-TAIL-RETRY-NOJITTER] {文件路径}: line {N}  → {代码片段}
  - [R-TAIL-HEDGE-UNSAFE] {文件路径}: line {N}  → {代码片段}
  - [R-DEPLOY-GOMAXPROCS] {入口/编排}  → 缺 automaxprocs 对齐
  - [R-TAIL-COLDSTART] {readiness 时序}  → readiness 早于预热
  - [P999-SLO-UNDEF] {路由}  → §1 未定义 P999
  - ...

🟢 通过 — 未命中危险模式

📊 统计
  - 扫描文件数：N（其中热路径：H，准热路径：W）
  - 命中规则数：M（按 rule-id 分布）
  - 建议人工 reviewer 复核：M 处
```

## 第 7 步：测试同步

**不适用**——本 Skill 不生成业务代码。但建议在 PR 内附 `go test -bench=. -benchmem` 输出（如 git diff 涉及热路径或 bench 文件）。

## 第 8 步：文档同步

本 Skill 不直接修改文档；审计输出应记录到 PR/工单，让用户追踪修复进度，并对应到 BUILD_STATUS §11 约束清单状态轨道的"已启用条目数"。

## 与其他 Skill 的关系

- 与 `concurrency-review`：并列的审计类 Skill；并发与性能问题常相关
- 与 `doc-sync-check`：审计维度互补
- 与 `new-service`：建议在 `/new-service` 生成涉及热路径方法时自动触发


---

> 🧩 **AIWeave 骨架 · 作者 XuRuibo** <hustxurb@163.com> · Apache-2.0 · 模板文件，复制到工程后按业务语义填充
