# task 模块知识

> 包路径：`com.bookcollector.task` · 最后更新：2026-09-23
> **本模块是全项目知识最密的地方。改 `task/` 下任何代码前，先读完第 6 节。**

## 1. 这个模块是干什么的

一个「采集任务」= 某个采集目标（188 个分类 / 7 个榜单之一）+ 最大页数。
分类 = **22 个一级 + 166 个二级**，二级同样是合法采集目标（清单见 `config.SeedRunner.SUB_CATEGORIES`）。
用户建任务、启动它，采集引擎按页抓取并把书 upsert 进 `books`；
中途可以暂停 / 恢复 / 取消；进程重启后能从中断处续传。

本模块负责的是**编排与状态**，不负责真正的抓取（那是 `collector`）。
它是 HTTP 层唯一的入口，也是「任务现在到底在干什么」的唯一权威。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `controller/TaskController` | Controller | 任务 CRUD + 5 个动作端点（start/pause/resume/cancel/retry） |
| `controller/RunController` | Controller | 运行记录列表 / 详情 / 日志 |
| `service/TaskService` | Service 接口 | 状态机契约（14 个方法） |
| `service/impl/TaskServiceImpl` | Service 实现 | **状态机的全部规则都在这里**（530 行） |
| `TaskRunner` | 组件（`@Async`） | 采集线程的入口：调 `CollectLoop`，写**终态** |
| `TaskRegistry` | 组件（内存态） | 采集权抢占表：一个目标同时只能有一个运行 |
| `TaskHandle` | 内存对象 | 单个运行的控制句柄（暂停 / 恢复 / 取消），实现 `CollectControl` |
| `InterruptedTaskDetector` | `ApplicationRunner` | 启动时把遗留的 `RUNNING`/`PAUSED` 标成 `INTERRUPTED` |
| `repository/TaskRepository` | Repository | 任务 / 运行 / 日志三张集合的 Mongo 访问 |
| `entity/{CollectTask,TaskRun,TaskLog}` | Entity | 三个 `@Document` |
| `req/{TaskCreateRequest,TaskUpdateRequest}` | req | 接收前端请求体 |

**几个容易忘的实现细节**：

- **`TaskProperties` 的四个默认值**（`config/TaskProperties.java`，对应 `bookcollector.task.*`）：
  | 字段 | 默认 | 含义 |
  |---|---|---|
  | `maxConcurrentRuns` | **1** | 并发闸门。调大之前先想清楚「接口限速是全局的」 |
  | `queueCapacity` | 16 | 线程池队列容量，满了直接拒绝（不阻塞 HTTP 线程） |
  | `runListLimit` | 50 | 运行记录列表默认返回条数 |
  | `logListLimit` | 500 | 运行日志列表默认返回条数 |

- **`TaskRegistry` 的 key 只在一处拼**：`keyOf(targetType, targetId)` → `"targetType:targetId"`。
  不要在各处手写字符串拼接。`active` 是 `ConcurrentHashMap<String, TaskHandle>`，
  抢占用 `putIfAbsent`（冲突时把「谁在占着」写进报错信息）。
- **`TaskRegistry.cancelAllOnShutdown()` 监听 `ContextClosedEvent`，不是 `@PreDestroy`。**
  为什么：暂停中的采集线程**阻塞**在 `awaitIfPaused()` 里不会自己退出；`@PreDestroy`
  在「停线程池」之后才执行，那时已经晚了，每次重启都要白等 `awaitTerminationSeconds`。
- **`TaskHandle` 的暂停用 `ReentrantLock` + `Condition`**（不是 `synchronized/wait`）——
  需要「可被打断的等待」；`paused` / `canceled` 是 `volatile`（写方在锁内，读方在锁外）。
- **`TaskRunner.run()` 的 `@Async(AsyncConfig.COLLECT_EXECUTOR)`**：靠的是
  `TaskService(Impl)` 持有的是**代理 bean**（不是自调用），所以注解生效。
- **`TaskRunner` 自己生成 traceId 并 `MDC.put` / `MDC.remove`**（key = `TraceIdFilter.TRACE_ID_KEY`）。
  `@Async` 线程**不继承**调用方的 MDC，不 put 的话采集线程日志就没有 traceId；
  **必须 remove**，否则线程池复用会让下一个任务带着上一个任务的 traceId（串味）。
- **`decideStatus` 的顺序不能反：先判 `isCanceled()` → 再 `isFailed()` → 否则 `SUCCESS`。**
  为什么：取消的实现方式是让 `CollectLoop` 抛 `CollectCanceledException` 并置 `canceled=true`，
  此时 `errorMsg` 是 `null`，**不先判取消就会误判成 SUCCESS**。
- **启动期三个 runner 的 `@Order`**（都在 `HIGHEST_PRECEDENCE` 附近，顺序有语义）：
  `MongoIndexInitializer` = `HIGHEST_PRECEDENCE`（先建索引）→
  `SeedRunner` = `+10`（再播种字典）→ `InterruptedTaskDetector` = `+20`（最后清理假死任务）。

## 3. 调用关系（图谱）

```
HTTP 线程                                    采集线程（collectExecutor）
─────────                                    ─────────────────────────
TaskController / RunController
      │  (只做转发)
      ▼
TaskService(Impl) ──┬──► TaskRepository ──► collect_tasks / runs / logs
                    │
                    ├──► CursorStore ─────► collect_cursors   （读起始游标）
                    │
                    ├──► TaskRegistry ────► 采集权（内存）
                    │         ▲
                    │         │ acquire / release
                    │         │
                    └──► TaskRunner.run(task, run, handle)  ─── 提交到线程池
                              │  @Async("collectExecutor")
                              ▼
                         CollectLoop ──► WereadClient ──► 微信读书
                              │              │
                              │              └──► ApiRequestRepository ──► api_requests
                              ├──► BookWriter ──► BookRepository ──► books
                              ├──► ProgressReporter ──► runs / logs   （进度快照）
                              └──► handle.awaitIfPaused() / isCanceled()
                                        │
                                        ▼
                              TaskRunner 的 finally：
                                写终态（setTaskStatus，无条件）
                                registry.release(key)   ← 🔴 漏了目标就永远起不来
```

**线程边界**：`TaskService(Impl)` 全部跑在 HTTP 线程上；`TaskRunner.run()` 及以下全在
采集线程上。两个线程共享的只有 Mongo 文档 + `TaskRegistry` 里的 `TaskHandle`。

## 4. 数据集合与索引

| 集合 | 用途 | 索引 |
|---|---|---|
| `collect_tasks` | 任务定义 | `uk_target (targetType, targetId)` **唯一** · `idx_status` · `idx_createdAt` |
| `collect_task_runs` | 每次执行 | `idx_taskId` · `idx_startedAt` |
| `collect_task_logs` | 关键事件 | `idx_runId` |

> ⚠️ `uk_target` **不是可选优化**：`collect_cursors` 的主键是 `(targetType, targetId)`，
> 即「游标是目标的属性」。允许两个任务采同一目标 → 它们共享一个游标 →
> A 采到第 100 页后 B 从第 100 页开始而不是从 0，**界面上看不出任何异常**。
> 所以「想换参数就改这个任务，不要建第二个」。

## 5. 对外接口

| 方法 | 路由 | 说明 |
|---|---|---|
| GET | `/api/tasks` | 列表，按创建时间倒序 |
| POST | `/api/tasks` | 新建（`PENDING`） |
| GET | `/api/tasks/{id}` | 详情 |
| PUT | `/api/tasks/{id}` | 编辑（**active 状态拒绝**） |
| DELETE | `/api/tasks/{id}` | 删除（**active 拒绝**；级联删 runs + logs，**不删游标**） |
| POST | `/api/tasks/{id}/start` | `PENDING`/`INTERRUPTED` → `RUNNING`，**从游标续传** |
| POST | `/api/tasks/{id}/pause` | `RUNNING` → `PAUSED` |
| POST | `/api/tasks/{id}/resume` | `PAUSED` → `RUNNING` |
| POST | `/api/tasks/{id}/cancel` | 非终态 → `CANCELED`，游标处保留断点 |
| POST | `/api/tasks/{id}/retry` | 终态 → 再跑一次，从当前游标续传 |
| GET | `/api/runs` | 运行记录分页（`taskId` / `status` 可筛） |
| GET | `/api/runs/{id}` | 运行详情（含进度快照） |
| GET | `/api/runs/{id}/logs` | 运行日志（正序，默认上限 500） |

**状态机**（`common.enums.TaskStatus`）：

```
PENDING ──start──► RUNNING ──pause──► PAUSED
                     │  ▲                │
                     │  └────resume──────┘
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     SUCCESS      FAILED      CANCELED        ← 终态（isTerminal）
JVM 重启：RUNNING / PAUSED → INTERRUPTED（不是终态，可 start/resume）
```

## 6. 不变量与铁律 ← 改这个模块前必读

1. **状态写入分工不能乱。**

   | 谁 | 写什么 | 怎么写 |
   |---|---|---|
   | `TaskService(Impl)`（HTTP 线程） | 中间态 `RUNNING`/`PAUSED`/`CANCELED` | **必须 CAS**（`casTaskStatus`） |
   | `TaskRunner`（采集线程） | 终态 `SUCCESS`/`FAILED`/`CANCELED` | **无条件覆盖**（`setTaskStatus`） |

   为什么：`TaskRunner` 若也走 CAS，运行期间用户点过暂停（状态变 `PAUSED`）终态就写不进去，
   **任务永远卡在 PAUSED**。反过来 `TaskService` 若也写终态，就和采集线程抢。

2. **采集权必须在 `finally` 里释放。** `TaskRunner.run()` 的 `finally` 有 `registry.release(key)`。
   为什么：漏掉一次，那个目标**永远无法再启动**。
   ⚠️ 写测试时注意：`@MockBean TaskRunner` 不会执行 `finally`，会留下占用的 handle，
   导致后续 `start` 被闸门拦下 —— **那是 mock 的产物，不是产品 bug**。

3. **续传的权威依据是 `collect_cursors`，不是 `TaskRun.currentCursor`。**
   - `CollectCursor.maxIndex` = 「下次从哪开始」（**状态，唯一权威**）
   - `TaskRun.currentCursor` = 「这次跑到哪了」（进度快照，给界面看）

   为什么：写恢复逻辑时**只改 run 的字段是没用的**，必须推进游标。

3.1 **`TaskRun` 上的两个图书计数不是一个东西（2026-10-08 拆开）。**

   | 字段 | 含义 | 谁写 |
   |---|---|---|
   | `booksSaved` | 写入/更新**总数**（upsert 计数，含重复更新的老书） | `ProgressReporter.onPage` 每页覆盖 |
   | `booksInserted` | 其中**新增**数（库里原本没有这个 `bookId`） | 同上 |

   → **更新数 = `booksSaved - booksInserted`**。榜单类目标一次会把整期（200 本）重写一遍，
   其中绝大多数是老书，只看 `booksSaved` 会严重高估「这次采回来多少新书」。
   数据源是 `book.dto.UpsertStat`（来自 `BulkWriteResult` 的 `getUpserts().size()`，
   **零额外查询**），经 `CollectResult.booksInserted` 上来。

   ⚠️ `ProgressReporter.onPage` 的签名是
   `onPage(runId, pagesDone, booksSaved, booksInserted, cursor, totalCount)` ——
   **两个计数是相邻参数**，加参数时别插错位置（`CollectLoop` 是唯一调用点）。

   ⚠️ 2026-10-08 之前的历史 run 没有 `booksInserted`，页面会显示 `-`（不是 0）。

4. **暂停是阻塞，不是抛异常。** `TaskHandle.awaitIfPaused()` 用 `Condition.await()`。
   为什么：抛异常会把 `CollectLoop` 的局部变量全丢，无法原地恢复（会重采一页）。

5. **`cancel()` 必须同时解除暂停。** 否则暂停中的任务永远等不到 `awaitIfPaused` 返回。

6. **启动永远从游标续传，不 reset。** 要「从头重采」应先重置游标（`PUT /api/cursors`）。

7. **并发闸门在 `bookcollector.task.max-concurrent-runs`（默认 1），不在线程池上。**
   为什么：`ThreadPoolExecutor` 是「先塞队列、队列满才开新线程」，core=1 + 有界队列的实际行为
   就是「最多 1 个在跑」。而接口限速是全局的，并发跑两个任务 = 请求频率翻倍，有被上游限流风险。

8. **关停唤醒用 `ContextClosedEvent`，不用 `@PreDestroy`。**
   为什么：Spring 关闭顺序是「发事件 → 停线程池 → destroyBeans」，`@PreDestroy` 太晚，会白等
   `awaitTerminationSeconds`。

9. **编辑与删除的边界**：`active`（`RUNNING`/`PAUSED`）时**都拒绝**。
   为什么：一次运行的参数在 `launch()` 时就固化成 `CollectCommand` 了，运行中改 `maxPages`
   不影响这次运行，但界面已经变了 —— 用户会以为改生效了。「改了不生效」比「不让改」更困惑。

10. **删除任务不删游标。** 游标是「目标」的属性。删任务保留游标 ⇒
    「删掉重建同名任务」会从原位置继续 —— 这通常正是用户想要的。

11. **`targetType` / `targetId` 不可改。** 它们是游标的归属键。
    用 `TaskUpdateRequest` **字段缺失**让「不能改」在类型层面成立，而不是靠运行时 if 拦。

## 7. 依赖与耦合

- **依赖**：`collector`（`ProgressReporter` / `CollectLoop` / `CollectControl`）、
  `cursor.repository.CursorStore`、`config.TaskProperties`、`common.enums.{TaskStatus,TargetType}`。
- **被依赖**：`collector.ProgressReporter` 反过来写 `collect_task_logs` / `collect_task_runs`
  → **`task ↔ collector` 是一个已知的环**（设计层面耦合，不是包结构问题，本轮不解决）。
- `stats` 依赖 `task.TaskRegistry` 读「有几个任务在跑」。

## 8. 测试与验收

| 测试 | 覆盖 |
|---|---|
| `TaskOrchestrationTest`（14 用例，单测） | 状态机全部准入条件、并发闸门、中断清理、cancel 解除暂停 |
| `TaskControlIT`（集成） | 真跑采集 + pause/resume/cancel 的端到端行为 |
| `CollectRetryFailureIT`（集成） | 失败路径：接口 500 / 404 / 断网的重试次数与耗时 |

```bash
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=TaskOrchestrationTest
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=TaskControlIT
```

> `*IT` **不在** `mvn test` 的默认扫描范围，必须显式 `-Dtest=`。

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 「取消」是两次写且不互相等待 → 有约 0.5 秒的不一致窗口

- **现象**：任务标签已显示「已取消」，运行记录还显示「运行中」。
- **根因**：`TaskService(Impl).cancel` 立刻 CAS 置 `CANCELED` 并返回（**不等**采集线程收尾，
  日志里那句「等待采集线程收尾」只是描述意图），而 `collect_task_runs.status` 要等采集线程
  退出（在途那页跑完）才写。S7 实测：`16:31:17.590` 任务置 CANCELED →
  `16:31:18.137` 线程退出、run 写 CANCELED。
- **修法**：**这是设计使然，不是缺陷**。⚠️ 写验收断言时**不能**踩在这个窗口里 ——
  正确写法是「轮询等它收敛 → 刷新取基线 → 隔几秒再刷比对」，不要「点完确认立刻断言」。

### 9.2 `PAUSED` 但没有对应线程 → 按中断处理

- **现象**：任务状态 `PAUSED`，但 `TaskRegistry` 里找不到 handle。
- **根因**：上次进程异常退出留下的假死记录（`InterruptedTaskDetector` 只在启动那一刻能确定）。
- **修法**：`resume` 里已兜底 —— 打 warn 后新开一次运行（游标还在，重采一页也是幂等的）。
  同理 `pause` 遇到这种情况会报「任务没有真正在运行，请用取消清理后重试」。

### 9.3 假死记录会让 run 永远停在 `RUNNING`

- **现象**：任务状态说在跑，内存里没线程，run 一直 `RUNNING`。
- **根因**：`cancel` 的「有线程」分支由 `TaskRunner` 写 run 终态；没有线程时没人写。
- **修法**：`cancel` 里对「假死」分支自己收尾（`progress.finish(..., CANCELED, ...)`）。
  **不要删这段**。

### 9.4 启动过程中任何一步失败都必须回滚

- **现象**：状态 `RUNNING` 但没人在跑。
- **根因**：`launch()` 是 5 步（闸门 → 建 run → 抢占目标 → CAS 状态 → 提交线程池），
  中间失败若直接抛出，前面已做的事就留成了假死记录。
- **修法**：`launch()` 每个失败分支都 `registry.release` + `failRun(run, ...)`。
  新增步骤时**必须照做**。

### 9.5 `TaskControlIT` 的「暂停后 pagesDone 不增长」**不能**写成严格相等

- **现象**：`TaskControlIT.fullLifecycle` **偶发**假红 ——
  `暂停期间 pagesDone 不应增长 ==> expected: <5> but was: <6>`。
  2026-09-23 实测：`-Dtest='*IT'` 全量跑时红了一次，单独复跑 3 次全绿。
- **根因**：`pause()` 是**发信号**，不是立刻掐断。若暂停那一刻正好有 1 页在途，
  它会把请求发完、页解析完、`pagesDone` 加 1 才停 —— 这是**正确行为**，不是没停住。
  更隐蔽的是：那一页的 `api_requests` 记录在**发请求时**就已经写入，
  所以 audit 的增量可能是 **0**，而 `pagesDone` 仍然是 **+1**。
  → 只查 audit 会漏判，只查 `pagesDone` 严格相等则会**偶发假红**。
- **修法**：两条断言都留 **1** 的容差（`<= 1`）。
  真正的「停住」由 audit 那条保证：限速约 1 req/s，没停住的话 3.5 秒会多出 3~4 条。
  **不要为了「更严谨」把它收紧成严格相等** —— 那是把竞态重新写回测试里。

### 9.6 IT 清夹具时**别漏 `api_requests`** —— 会留下「孤儿审计」

- **现象**：界面上「请求审计」页冒出一批红底行，`targetId` 是 `it-retry-target` ——
  一个字典里**根本不存在**的目标；「只看失败」恒有数据，看着像真有故障。
  2026-09-23 实测攒了 **27 条**（11 超时 + 8×404 + 8×500）。
- **根因**：`CollectRetryFailureIT` 打的是**本地假服务**（`127.0.0.1` 上的 `HttpServer`），
  每次请求都会经 `ApiRequestRepository` 落一条审计。而它的 `clearTarget()` 清了
  TaskLog / CollectTask / TaskRun，**独独没清 `ApiRequest`** → 留下连 targetId 都不存在的孤儿审计。
- **修法**：`clearTarget()` 里补一句按 `targetId` 删 `ApiRequest`。
- ⚠️ **但「按 targetId 整片删」只对测试专用目标才安全**：`it-retry-target` 永远不会有
  用户真采的数据，随便删。`TaskControlIT` 用的是**真目标**（`300000` 文学），
  **不能**照抄这个写法 —— 那会把用户真采的历史一起抹掉。
  它真打真接口留下的审计行属于**合法历史**，留在库里是对的
  （`api_requests` 本就是「只插不改、写入量大」的账本，见 `audit/AGENTS.md` 不变量 4）。
- 附带澄清：`audit/AGENTS.md` 不变量 4 的「只有查询、没有删除」约束的是**产品接口层**；
  IT 用 `MongoTemplate` 清自己的夹具，正是它自己说的「要清理请直接连库操作」，并不违背。
