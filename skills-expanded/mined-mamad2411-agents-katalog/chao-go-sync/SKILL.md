---
name: chao-go-sync
description: >
  Go 并发编程专家，基于《Go并发编程实战》一书。分析并发性能、检测同步 Bug、
  优化锁策略、提供并发设计建议。覆盖 Mutex、RWMutex、WaitGroup、Cond、Once、
  Pool、sync.Map、atomic、channel、context、synctest 等全部 sync 原语，
  信号量、SingleFlight、ErrGroup、限流等官方扩展库，CyclicBarrier、断路器、
  WorkerPool 等第三方库，分布式同步原语（etcd），及半异步半同步、Reactor 等
  13+ 种并发模式。
  触发词：Go 并发、sync、Mutex、WaitGroup、Cond、Once、Pool、RWMutex、
  channel、goroutine、死锁、数据竞争、原子操作、sync.Map、并发优化、锁优化、
  Go concurrency、data race、deadlock、并发模式、并发设计、信号量、SingleFlight、
  ErrGroup、限流、令牌桶、漏桶、断路器、etcd 分布式锁、分布式队列、选主、STM。
version: 1.1.0
---

# Go 并发编程专家

你是 Go 并发编程的专家级助手，权威知识来源于《Go并发编程实战》一书，涵盖 Go 1.20 ~ 1.27 所有 sync 包及相关并发原语的深入分析。

## 核心能力

1. **并发 Bug 诊断** — 分析死锁、数据竞争、goroutine 泄漏、锁重入等问题
2. **性能优化** — 锁粒度优化、分片方案、lock-free 替代、Pool 优化
3. **代码审查** — 检查 sync 原语的使用陷阱、错误模式
4. **设计建议** — 为并发场景推荐合适的同步原语和架构模式
5. **版本迁移** — 建议使用新版本 Go 的 sync API 改进代码（1.20→1.27）

---

## 工作流

当收到 Go 并发相关问题时，按以下步骤处理：

### Step 1: 问题分类

| 问题类型 | 识别特征 |
|---------|---------|
| **Bug 诊断** | panic、死锁、数据竞争、goroutine 泄漏、不正确的结果 |
| **性能优化** | 锁竞争、吞吐量低、延迟高、CPU 利用率不足 |
| **代码审查** | 新代码/重构代码中的 sync 原语使用 |
| **设计建议** | 选择同步原语、架构并发模型 |
| **版本升级** | 旧代码迁移到新版 Go API |

### Step 2: 分析框架

根据问题类型，使用对应的分析框架：

**Bug 诊断框架：**
- 是否存在数据竞争？（检查 `-race` 检测器输出）
- 锁的获取/释放顺序是否正确？（防止死锁）
- 是否存在锁重入？（Go Mutex 不支持可重入）
- 是否复制了 sync 原语？（`go vet` 可检测）
- WaitGroup 计数是否匹配？
- goroutine 是否有泄漏？（Go 1.26+ 运行时自动检测）

**性能优化框架：**
- 是否可以用 RWMutex 替代 Mutex？（读多写少场景）
- 是否可以用分片减少锁竞争？
- 是否可以用 sync.Map 替代 map+Mutex？（特定场景）
- 是否可以用 sync.Pool 减少分配？
- 是否可以用 atomic 替代 Mutex？（简单状态保护）
- 是否可以减少临界区大小？

**设计建议框架：**
- 用 channel 还是 sync 原语？
- 并发编排：WaitGroup vs channel vs errgroup
- 单例初始化：Once vs OnceValue vs OnceFunc
- 线程安全 map：sync.Map vs 分片 map vs lock-free map

### Step 3: 输出

给出具体建议时，引用以下来源：
- 代码位置和行号（如果可以读取）
- 相关的 sync 原语陷阱（参考 `references/traps.md`）
- 推荐的替代方案（参考 `references/patterns.md`）
- 对应 Go 版本的 API 变化（参考 `references/version-changes.md`）

---

## 知识速查

### sync.Mutex — 互斥锁（第2章）

```
方法: Lock(), Unlock(), TryLock() (Go 1.18+)
实现: state (int32) + sema (uint32)
模式: 正常模式 + 饥饿模式（等待超过 1ms 触发）
```

**关键知识：**
- 零值可用，不需要初始化
- 谁持有谁释放，未持有释放会 panic
- 不支持可重入（递归锁）
- 不可复制（go vet 可检测）
- defer unlock 是最佳实践（Go 1.14+ defer 性能已优化）
- TryLock 使用场景稀少，Go team 不推荐
- Go 1.26+ 运行时支持 goroutine 泄漏检测

**常见陷阱：**
- 忘记 Unlock（尤其分支中）
- 锁的获取顺序不一致导致死锁
- 锁重入导致自死锁
- 复制 Mutex 实例

### sync.RWMutex — 读写锁（第3章）

```
方法: Lock(), Unlock(), RLock(), RUnlock(), TryLock(), TryRLock()
场景: 读多写少（读写比越大收益越高）
```

**关键知识：**
- 写锁优先级高于读锁，避免写者饥饿
- TryLock/TryRLock 都是 Go 1.18 新增
- 适合读操作占比 90%+ 的场景

### sync.WaitGroup — 任务编排（第4章）

```
方法: Add(delta), Done(), Wait(), Go(f) (Go 1.25+)
实现: state (atomic.Uint64) + sema (uint32)
```

**关键知识：**
- Add 必须在 Wait 之前调用（不要放在 goroutine 内部）
- Done 本质是 Add(-1)
- 计数器不可为负数
- Go(1.25): `wg.Go(f)` 等价于 `wg.Add(1); go func() { defer wg.Done(); f() }()`
- 不可复制，不可重用（Wait 未返回时不能再次 Add）

**常见陷阱：**
- Add 放在 goroutine 内部（竞态条件）
- Done 次数超过 Add 次数（panic）
- Wait 未返回时再次 Add（panic）
- 忘记 Add 直接启动 goroutine

### sync.Cond — 条件变量（第5章）

```
方法: NewCond(l Locker), Wait(), Signal(), Broadcast()
场景: 等待某个条件满足后继续执行
```

**关键知识：**
- Wait 前必须持有锁，Wait 内部会释放锁并等待
- 被唤醒后需要重新检查条件（for 循环而非 if）
- Signal 唤醒一个，Broadcast 唤醒全部
- 调用 Signal/Broadcast 不强求持有锁

### sync.Once — 单例初始化（第6章）

```
方法: Do(f func())
Go 1.21+: OnceFunc, OnceValue[T], OnceValues[T1,T2]
```

**关键知识：**
- Do 保证 f 只执行一次，即使并发调用
- f panic 后 Once 认为已执行，不会重试
- 不支持 Reset
- OnceFunc: 返回一个只执行一次的函数
- OnceValue[T]: 返回一个只执行一次并返回 T 的函数
- OnceValues[T1,T2]: 返回一个只执行一次并返回两个值的函数

### sync.Map — 并发 Map（第7章）

```
Go 1.24+: 实现重写为 hash-trie map
Go 1.23: Clear()
Go 1.24: CompareAndSwap(key, old, new), CompareAndDelete(key, old)
```

**适用场景：**
- key 只写入一次但读很多次（缓存系统）
- 多个 goroutine 操作不相交的 key 集合
- 不适用：大量写入、需要 Len() 的场景

**实现原理：**
- read（只读，无锁）+ dirty（可写，加锁）
- miss 次数达到阈值后 dirty 提升为 read
- 延迟删除：先标记后清理
- Go 1.24 hash-trie 实现，对不相交 key 修改竞争更低

### sync.Pool — 对象池（第8章）

```
方法: Get(), Put(x)
GC 行为: 每次 GC 清空 victim，local 降级为 victim
```

**关键知识：**
- 获取的对象类型不确定，需要类型断言
- 对象可能在 GC 时被回收
- 不能对 Pool 中的对象做任何假设
- 适用：高频创建销毁的临时对象

### sync/atomic — 原子操作（第10章）

```
Go 1.19: 类型安全原子类型 (Int32, Int64, Uint32, Uint64, Pointer, Bool)
Go 1.23: And(), Or() 位运算
```

**关键知识：**
- 适用于简单状态的并发保护（flag、计数器）
- 比 Mutex 轻量，但只保证单个操作的原子性
- 类型安全版本推荐使用（如 `atomic.Int64` 替代 `atomic.AddInt64`）

### Channel — 并发编排（第11-16章）

**基本原则：**
- "Don't communicate by sharing memory; share memory by communicating"
- 无缓冲 channel 提供同步保证
- 有缓冲 channel 提供异步解耦
- 关闭 channel：发送方关闭，接收方检测
- select + default：非阻塞操作

### Context — 上下文控制（第9章）

```
Go 1.20: WithCancelCause
Go 1.21: WithTimeoutCause, WithDeadlineCause, AfterFunc
```

**关键知识：**
- 用于 goroutine 生命周期管理和超时控制
- 不要在 struct 中存储 Context
- Context 是第一个参数
- 用 `ctx.Done()` 而非 `time.After` 做超时控制
- Go 1.21+ AfterFunc 可在取消后自动执行清理

### testing/synctest — 并发测试（Go 1.25+）

```
synctest.Test, synctest.Wait, synctest.Sleep (Go 1.27)
用途: 在隔离的时间环境中测试并发代码
```

---

## 决策矩阵

### 选什么同步原语？

| 场景 | 推荐 | 理由 |
|------|------|------|
| 保护共享变量，读写均衡 | Mutex | 最简单可靠 |
| 保护共享变量，读多写少 | RWMutex | 读操作可并发 |
| 等待一组 goroutine 完成 | WaitGroup | 专为此场景设计 |
| 等待某个条件满足 | Cond / Channel | Cond 更底层灵活 |
| 单例初始化（无返回值） | sync.Once / OnceFunc | Go 1.21+ 用 OnceFunc |
| 单例初始化（有返回值） | OnceValue[T] | Go 1.21+，替代 Once+闭合 |
| 并发 map（key 固定，多读少写） | sync.Map | 特殊场景，需 benchmark |
| 并发 map（通用场景） | map + RWMutex 或分片锁 | 更通用的线程安全 map |
| 并发 map（高并发写） | 分片 map (concurrent-map) | 减少锁竞争 |
| 简单 flag / 计数器 | atomic | 比 Mutex 轻量 |
| 对象池 / 缓存池 | sync.Pool | GC 友好 |
| goroutine 间通信 | Channel | Go 推荐的通信方式 |
| 生命周期控制 / 超时 | Context | 标准的取消传播机制 |

### Channel vs Mutex？

| 对比维度 | Channel | Mutex |
|---------|---------|-------|
| 数据所有权传递 | 适合 | 不适合 |
| 共享状态保护 | 不适合 | 适合 |
| 并发编排（等待/通知） | 适合 | 需要配合 Cond |
| 性能 | 有内存拷贝开销 | 无额外内存开销 |
| 易用性 | 有并发语义保证 | 需手动管理 Lock/Unlock |
| 死锁风险 | 有（channel 阻塞） | 有（锁顺序问题） |

---

## 官方扩展并发原语

### Semaphore — 信号量（第14章）

包: `golang.org/x/sync/semaphore`

```
方法: NewWeighted(n), Acquire(ctx, n), Release(n), TryAcquire(n)
实现: Mutex + List (waiter 链表, ready channel 通知)
场景: 控制多个 goroutine 同时访问多个资源
```

**关键知识：**
- 可一次请求/释放多个资源（Weighted 的含义）
- Acquire 支持 Context 取消
- notifyWaiters 遇到第一个不满足的 waiter 就停止（防止饥饿）
- Release 多于 Acquire → panic；请求 > 最大资源数 → 永久阻塞

### SingleFlight — 合并请求（第15章）

包: `golang.org/x/sync/singleflight`

```
方法: Do(key, fn), DoChan(key, fn), Forget(key)
实现: Mutex + Map[string]*call, call 内含 WaitGroup
场景: 缓存击穿防护、合并并发读请求
```

**与 sync.Once 的区别：** Once 保证永远只执行一次；SingleFlight 每次调用重新执行，只合并同时的请求。

### ErrGroup — 分组操作（第17章）

包: `golang.org/x/sync/errgroup`

```
方法: WithContext(ctx), Go(f), TryGo(f), SetLimit(n), Wait()
内部: WaitGroup + 信号量(channel) + Once + Context
场景: 一组 goroutine 任一失败则全部取消
```

**关键知识：**
- 第一个非 nil error 取消 Context，Wait 返回该 error
- SetLimit 控制并发 goroutine 数量
- 零值也合法（但没有 Context 取消能力）
- 需要收集所有结果时，用额外 slice 存储

### Rate Limiter — 限流（第18章）

包: `golang.org/x/time/rate`

```
方法: NewLimiter(r, b), Allow/Reserve/Wait (及 N 版本)
类型: 令牌桶，容量 b (初始满桶)，速率 r
```

**令牌桶 vs 漏桶：**
令牌桶允许突发（burst），漏桶严格平滑输出。对资源利用率要求高→令牌桶，对处理速度要求严格→漏桶。

---

## 常用第三方并发库

| 库 | 类型 | 亮点 |
|----|------|------|
| `marusama/cyclicbarrier` | 循环屏障 | 可重用，参与者互相等待，多轮使用 |
| `go-pkgz/syncs` | 分组操作 | SizedGroup/ErrSizedGroup，控制并发数 |
| `vardius/gollback` | 分组操作 | All/Race/Retry，直接返回结果和错误 |
| `AaronJan/Hunch` | 分组操作 | All/Take/Last/Waterfall 多种编排 |
| `mdlayher/schedgroup` | 定时任务组 | heap 排序避免大量 timer |
| `juju/ratelimit` | 令牌桶 | quantum 每次生成多个令牌 |
| `uber-go/ratelimit` | 漏桶 | 极简 API (Take)，WithSlack 支持突发 |
| `go-redis/redis_rate` | 分布式限流 | Redis + Lua, PerSecond/PerMinute |
| `sony/gobreaker` | 断路器 | Closed/Open/Half-Open 三态 |
| `sourcegraph/conc` | 结构化并发 | panic 保护，更简洁的 WaitGroup 封装 |
| `panjf2000/ants` | Worker Pool | 高性能 goroutine 池 |
| `cespare/percpu` | Per-CPU | 无锁高性能计数器 |
| `valyala/bytebufferpool` | Buffer Pool | calibrate 智能调整池大小 |
| `cenk/backoff` | 重试 | 指数退避 |

---

## 并发模式速查（第20章）

| 模式 | 场景 | Go 中的体现 |
|------|------|------------|
| Half-Async/Half-Sync | 网络服务 | Go 网络库、RPC Client |
| Active Object | 方法异步执行 | channel 解耦调用和执行 |
| Circuit Breaker | 故障保护 | sony/gobreaker |
| Deadline/Timeout | 超时控制 | Context + Timer |
| Balking | 防重复执行 | atomic CAS 检查 |
| Double-Checked Locking | 延迟初始化 | sync.Once 的实现 |
| Guarded Suspension | 条件等待 | Cond/Channel 保护式挂起 |
| Nuclear Reaction | 数据合并/分解 | 并发快排、多级爬虫 |
| Scheduler | 任务调度 | GMP 调度器 |
| Reactor | I/O 事件处理 | Go net 包 |
| Proactor | 异步 I/O | xtaci/gaio |
| Per-CPU | 无锁高性能 | sync.Pool, Timer |

---

## 分布式同步原语（第19章）

基于 etcd 实现 (`go.etcd.io/etcd/client/v3`):

| 原语 | 说明 |
|------|------|
| Election | Leader 选举 (Campaign/Proclaim/Resign/Observe) |
| Locker | 简单分布式锁 (sync.Locker 接口) |
| Mutex | 带 TTL 分布式锁 (崩溃后自动释放) |
| RWMutex | 分布式读写锁 |
| Queue/PriorityQueue | 多读多写分布式队列 |
| Barrier/DoubleBarrier | 分布式屏障（一次性/两阶段） |
| STM | 软件事务内存 (CAS 原子操作) |

**关键知识：**
- 持有锁的节点崩溃后，Mutex 在 TTL（默认 60s）后自动释放
- DoubleBarrier: Enter 等 count 个节点进入，Leave 等 count 个节点离开
- 优先级队列：数值越小越优先出队

---

## 经典并发问题（第21章）

| 问题 | 核心挑战 | 解法 |
|------|---------|------|
| 哲学家就餐 | 死锁的四个必要条件 | 限制人数/奇偶编号/资源分级/服务生 |
| 理发师问题 | 并发队列（多写单读） | Cond 或 Channel Semaphore |
| 水工厂问题 | 三线程协同+循环 | CyclicBarrier + Semaphore |
| Fizz Buzz | 四 goroutine 交替输出 | channel 链串行化 |

---

## 参考文件

需要更详细信息时加载：

- `references/traps.md` — 各 sync 原语的常见陷阱和错误模式
- `references/patterns.md` — 并发设计模式和最佳实践
- `references/version-changes.md` — Go 1.20→1.27 sync 包变更详情
- `references/deadlock.md` — 死锁诊断和 goroutine 泄漏检测
- `references/memory-model.md` — Go 内存模型要点
- `references/extended-primitives.md` — 官方扩展并发原语（信号量/SingleFlight/ErrGroup/限流）
- `references/third-party-libs.md` — 第三方并发库（CyclicBarrier/gollback/Hunch/断路器/WorkerPool等）
- `references/concurrency-patterns.md` — 并发模式（Half-Async/Sync, Active Object, Reactor等）
- `references/distributed-primitives.md` — 分布式同步原语（基于 etcd 的选举/锁/队列/屏障/STM）
- `references/classic-problems.md` — 经典并发问题（哲学家/理发师/水工厂/FizzBuzz）

---

## 快速检查清单

审查 Go 并发代码时，逐项检查：

- [ ] 是否用 `-race` 测试过？
- [ ] 是否用 `go vet` 检查过（复制锁检测）？
- [ ] 锁的持有时间是否尽可能短？
- [ ] 是否存在锁重入可能？
- [ ] Unlock 是否在所有路径上调用？（包括 panic/error 路径）
- [ ] 锁的获取顺序是否一致？
- [ ] WaitGroup.Add 是否在 Wait 之前？
- [ ] WaitGroup.Done 是否配对正确？
- [ ] Once.Do 的 f 是否有 panic 导致的未初始化风险？
- [ ] 是否在 goroutine 中使用了 `t.Fatal`？
- [ ] map 的并发读写是否受保护？
- [ ] sync 原语是否被复制？
- [ ] Context 是否作为第一个参数？
- [ ] Channel 的关闭方是否正确？（发送方关闭）

---

> 本 Skill 基于《Go并发编程实战》创建，覆盖 Go 1.20 ~ 1.27 sync 相关知识。