---
name: go-perf-diagnose
description: 排查与优化 Go 服务的运行时问题：goroutine 泄漏、内存持续上涨或容器 OOMKilled、CPU 高、锁竞争与延迟高，接入 pprof、写 benchmark 验证优化。用户说「goroutine 涨」「内存泄漏」「OOM」「CPU 高」「接口变慢」「锁竞争」「加 pprof」「做性能优化」「写 benchmark」时使用。只是新写并发代码时遵循 rules/go/concurrency.md 即可，不使用本 skill。
---

# Go 性能与泄漏排查

逐条约定在 `.claude/rules/go/concurrency.md` 与 `testing.md`。pprof 命令见 `references/pprof.md`，并发模板与实测依据见 `references/concurrency.md`。

## 1. 先确认现象与环境

- 指标：`runtime.NumGoroutine()`、heap、RSS、GC 次数与 CPU、P99 延迟的趋势，问题是单调上涨还是随流量回落。
- 环境：`go.mod` 的 `go` 版本、容器 CPU 与内存限额、是否设置 `GOMAXPROCS` / `GOMEMLIMIT` / `GOGC`。
- 只在开发、测试或预发环境采集；生产采集需用户确认，且只经内网诊断端口。

## 2. 现象到工具

| 现象 | 先看 | 判读 |
|---|---|---|
| goroutine 数单调上涨 | `goroutine?debug=1`，按状态分类 | `chan send` 多：接收方已退出；`chan receive`：发送方未 close 或已退出；`select`：看等的是哪几个 channel；`IO wait` 且有大量 `readLoop` / `writeLoop`：HTTP body 未关；`sync.WaitGroup.Wait`：`Add` / `Done` 不匹配 |
| 请求超时但 goroutine 数不涨 | goroutine profile 中的调用方栈 | 常见是调用方「收 N 次」等不齐（某个子任务出错未发送） |
| heap 持续上涨 | `heap` 的 `inuse_space`，隔一段时间采两次用 `-base` 对比 | 只增不删的 map / 缓存、泄漏 goroutine 栈引用的对象 |
| heap 不高但 GC 占 CPU 高 | `heap` 的 `alloc_objects` | 短命对象过多，按 `allocs/op` 优化 |
| 大缓存常驻、GC 标记耗时长 | CPU profile 中 `gcBgMarkWorker` 的占比 | 标记成本取决于指针数量而非内存大小；百万级 `map[K]*V` 可改为值类型或「下标 + 切片」，牺牲类型安全，先确认 GC 是瓶颈 |
| 调度延迟、goroutine 长时间不运行 | `go tool trace`（`/debug/pprof/trace?seconds=5`） | pprof 看不到等待调度的时间；trace 开销大，只短时采集 |
| RSS 高于 heap、GC 后不降 | `runtime.MemStats` 的 `HeapInuse`、`HeapReleased` | 回收不等于立即归还系统，先确认是否真在增长 |
| 容器 OOMKilled 而 GC 次数不多 | `GOMEMLIMIT` 是否设置 | `GOGC` 只按比例触发，不知道容器限额 |
| CPU 高 | `profile?seconds=30`，`-top -cum` | flat 前几名多是 runtime，沿 cum 找到第一个业务函数再 `-list` |
| 延迟高但 CPU 不高 | `block`、`mutex` | 两者默认关闭，先打开采样率，否则得到空 profile |

## 3. 修复

- 泄漏：给阻塞点补退出路径（`select` + `ctx.Done()`、`close` 责任、body 关闭），模板见 `references/concurrency.md`。
- 分配：预分配、`strings.Builder` + `Grow`、`strconv` 替代 `fmt`；`sync.Pool` 只用于高频创建的临时 buffer。`-gcflags=-m` 只用来找原因，结论以 `allocs/op` 为准。
- 锁：缩小临界区、拆分锁；换 `RWMutex` 或 `atomic` 前先写 benchmark。
- 容器：设置 `GOMEMLIMIT`；`go` < 1.25 的模块 `GOMAXPROCS` 不感知 CPU 限额。

## 4. 验证

- 修改前后用同一 benchmark（`for b.Loop()`、`-benchmem -count=10`）加 `benchstat` 对比，或用 pprof `-base` 对比两次采集。
- 泄漏修复补 `goleak` 测试，超时逻辑用 `testing/synctest` 测，跑 `go test -race`。
- 汇报：现象、证据（profile 截取或 benchmark 数据）、根因、修改、前后对比；未实测的推断明确标出。
