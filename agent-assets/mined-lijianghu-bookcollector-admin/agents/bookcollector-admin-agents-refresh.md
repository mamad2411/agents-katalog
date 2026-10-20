# refresh 模块知识

> 包路径：`com.bookcollector.refresh` · 最后更新：2026-10-08
> **这个模块和「采集任务」是两套东西。改之前先读第 6 节铁律 1。**

## 1. 这个模块是干什么的

把 **7 个榜单 + 期刊杂志**（共 8 个目标，清单见 `RefreshTarget.ALL`）做一次**全量重采**，
支持 cron 定时触发和手动「立即执行」。

它存在的理由：这 8 个目标的数据源会**定期整体更新**（榜单按天滚动、期刊按期上新），
而普通分类（如「文学」）的历史数据基本不动、采一次就够。手工去任务配置一个个点太麻烦。

### 🔴 它和「采集任务」的区别（一张表说清）

| 维度 | 采集任务（`task` 模块） | 定时刷新（本模块） |
|---|---|---|
| 任务实体 | `CollectTask` + `TaskRun` | **都没有** |
| 执行记录 | 每次运行一条 `TaskRun`，永久保留 | `RefreshJob.lastDetails`，**只留最近一次** |
| 执行中进度 | 逐页写 `collect_task_runs`（`ProgressReporter`） | **内存快照**（`liveDetails`），逐页换引用、**不落库** |
| 增量 | `TaskRun.booksSaved` + `booksInserted`（2026-10-08 也拆开了） | `RefreshDetail.booksInserted` —— **新增 / 更新分开** |
| 游标 | 读写 —— 断点续传的权威依据 | **完全不碰**（`skipCursor=true`） |
| 页数 | 由任务的 `maxPages` 决定 | 固定 `0` = 从第 0 页跑到底 |
| 目标锁 | `task.TaskRegistry`（key `targetType:targetId`） | **同一把锁**（所以两者天然互斥） |
| 冲突行为 | 抛 `BizException`「目标「X」正在采集中」 | **中止整批**，文案见铁律 4 |
| 入口 | `/api/tasks/**` + 「任务配置」页 | `/api/refresh/**` + 「增量配置」页 |

**为什么不复用 `task.TaskRunner`**：它和任务模型是**硬绑定**的 —— 它要写
`CollectTask.status`、写 `TaskRun`，而本模块这两样都没有。为了复用去造一个「假任务」，
会把「一个目标只能有一个任务」（`collect_tasks.uk_target` 唯一索引）这个前提弄脏。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `RefreshTarget` | 常量 | 8 个目标的**固定清单**（`ALL`）。写死，页面不可改 |
| `entity/RefreshStatus` | 枚举 | 状态 + 中文 label。**批次级与目标级共用**（取值是包含关系） |
| `entity/RefreshJob` | Entity | 单例配置文档（`_id` 固定 `"default"`）+ 最近一次结果 |
| `entity/RefreshDetail` | Entity（内嵌） | 单个目标的结果，作为 `lastDetails` 数组元素；**执行中也会以 `RUNNING` 出现在内存快照里** |
| `repository/RefreshJobRepository` | Repository | `loadOrCreate` / `saveConfig` / `markRunning` / `markFinished` / `resetStaleRunning` |
| `service/RefreshService` | Service 接口 | `getJob` / `updateConfig` / `trigger` / `currentCron` / `runScheduled` |
| `service/impl/RefreshServiceImpl` | Service 实现 | 批次编排（**本模块的核心**）+ 独立线程池 + `AtomicBoolean` 互斥 + `liveDetails` 内存进度 |
| `RefreshScheduler` | 定时触发器 | `SchedulingConfigurer` + 动态 `Trigger`（每次重新读 cron） |
| `controller/RefreshController` | Controller | 3 个端点，极薄转发 |
| `req/RefreshConfigRequest` | req | 改配置请求体（两字段都可选，null = 不改） |
| `vo/RefreshJobVO` | VO | 页面全量数据（配置 + 内存态 + 目标清单 + 最近结果） |

## 3. 调用关系（图谱）

```
RefreshController ──► RefreshService(Impl) ──┬──► RefreshJobRepository ──► refresh_jobs
                                             │
                                             ├──► collector.CollectLoop.run(cmd)   ★ 直接调，不走 TaskRunner
                                             │        ├── cmd.skipCursor = true
                                             │        └── cmd.progressListener ──► 逐页回调（内存）
                                             │                 └── RefreshServiceImpl.liveDetails（AtomicReference）
                                             └──► task.TaskRegistry.acquire/release  ★ 与手动任务同一把锁

RefreshScheduler ──► RefreshService.currentCron() / runScheduled()
        （Spring 默认单线程调度器；Trigger 在注册时同步调用一次 nextExecutionTime）
```

`CollectLoop` 与 `TaskRegistry` 是**本模块对外的全部依赖**，都不改动它们的行为。
⚠️ 2026-10-08 起还多用了 `CollectCommand.progressListener`（新增字段，默认 null，
不影响其它调用方）。

## 4. 数据集合与索引

| 集合 | 索引 | 为什么 |
|---|---|---|
| `refresh_jobs` | `_id`（固定 `"default"`） | **用固定主键强制单例** —— 比「查询时 limit 1」可靠：多写一条都写不进去 |

`lastDetails` 是**内嵌数组**，不单独建集合：它永远跟着批次一起读，没有独立查询需求。

## 5. 对外接口

| 方法 | 路由 | 说明 |
|---|---|---|
| GET | `/api/refresh/job` | 页面全量数据：cron / enabled / nextFireTime / running / targets / 最近一次结果 |
| PUT | `/api/refresh/job` | 改 cron / enabled（都可选）。cron 非法 → `code=400` |
| POST | `/api/refresh/trigger` | 立即执行。**提交即返回**，前端轮询 GET 跟进 |

鉴权由 `config.WebMvcConfig` 统一拦截 `/api/**` 覆盖，本模块不用声明。

## 6. 不变量与铁律 ← 改这个模块前必读

1. **刷新任务没有断点续传，且全程不碰游标。**
   榜单每期换一批书，「从上次的位置继续翻」会**漏掉排在前面的新上榜书**。
   又因为游标是**目标**的属性（用户手工建的榜单任务也在用它），
   所以是「全程不碰」（`CollectCommand.skipCursor=true`）而**不是**「重置后再写」——
   后者会把手工任务的续传位置冲掉。
   落地方式：`CollectLoop` 的 **4 处**游标调用点（`reset` / `load` / 两处 `advance`）
   全包了 `if (!skip)`；`skip=true` 时 `maxIndex=0`、`baseCollected=0L`。

2. **批次互斥的唯一权威是 `RefreshServiceImpl.batchRunning`（`AtomicBoolean`），不是 DB。**
   DB 里的 `lastRunStatus=RUNNING` 只是**快照**，进程被杀就是假的。
   必须用 `compareAndSet` 而不是「先 get 再 set」—— 后者在「定时触发」和
   「手动点击」同时发生时会让两个批次都通过，同一批目标被采两遍。
   启动时 `@PostConstruct` 把遗留的 `RUNNING` 标成 `INTERRUPTED`（同 `InterruptedTaskDetector` 的思路）。

3. **手动触发必须用自己的线程池，不能用 `AsyncConfig.collectExecutor`。**
   后者 `core=1` + 有界队列 = 「只要有采集在跑，提交进去的刷新批次就**排队等**」。
   而它该做的是「抢不到锁就**立刻**报中止」。排队等 30 分钟再报「已中止」，
   用户早就以为它跑完了。

4. **冲突时中止整批，且已跑完的目标不回滚。**
   文案（用户 2026-10-08 逐字指定，两种中止原因共用）：
   **「定时任务被手动采集占用，已中止」**。
   不回滚是刻意的 —— 已完成的目标是幂等 upsert 的产物，数据是对的，
   回滚反而会造成「刷新了但没生效」的假象。**这个批次不是原子的。**

5. **`Trigger.nextExecutionTime()` 绝对不能返回 `null`。**
   `ReschedulingRunnable.schedule()` 拿到 null 直接 `return null`，而 `run()` 里
   `if (!currentFuture.isCancelled()) schedule();` 不会重排 → **这个定时任务永久死掉**。
   于是「先停用、再启用」会让定时刷新再也跑不起来，而页面上看不出任何异常。
   → 未启用也要照常算出下一次，「要不要真跑」交给 `runScheduled()` 在运行时判断。

6. **`nextExecutionTime()` 在注册时是同步调用的**
   （`ThreadPoolTaskScheduler.schedule` → `new ReschedulingRunnable(...).schedule()`）
   → Trigger 里读 Mongo 的代码会在**应用启动期**执行。启动期依赖 Mongo 是既有事实
   （`SeedRunner` / `InterruptedTaskDetector` 也是），但要心里有数。

7. **cron 校验只能用 `CronSequenceGenerator`，不能用 `CronExpression`。**
   本项目锁在 Boot 2.3.12 = **Spring Framework 5.2.15.RELEASE**，
   而 `org.springframework.scheduling.support.CronExpression` 是 **5.3** 才引入的
   （已用 `unzip -l` 核实 jar 里没有这个类）。
   `CronSequenceGenerator` 在 5.2 里**未**标 `@Deprecated`（已用 `javap -v` 核实），可以放心用。
   ⚠️ **升级到 Boot 2.4+ 之后必须换成 `CronExpression.parse(cron).next(...)`**，否则编译不过。

8. **`lastDetails` 只保留最近一次，且长度不一定是 8。**
   中途被占用而中止时，中止点**之后**的目标压根没跑，不会出现在数组里。
   前端表格的行数因此是可变的 —— 别写死 8 行。

   ⚠️ 而且**执行中它读的不是 DB**：`getJob()` 在 `batchRunning=true` 时返回
   `liveDetails` 里的**内存快照**（含 `status=RUNNING` 的占位项），
   批次结束后才切回 DB 里的终态。所以：
   - 别把「`lastDetails` 里有 `RUNNING`」当成脏数据 —— 那是设计
   - 别在 `doBatch` 之外去改 `liveDetails`，它是采集线程独占写的

9. **`runId` 传 `null`，不是随便编一个。**
   `collector.ProgressReporter` 对 `runId=null` 静默降级（`onPage` / `finish` 直接 return，
   `log` 只打 SLF4J 不落库），`audit.ApiRequestRepository.recordPage` 整体包了 try-catch。
   编一个假的 runId 只会往 `collect_task_logs` 里塞查不到的孤儿数据。

10. **实时进度只活在内存里，不落库（用户 2026-10-08 要求）。**
    页面 2 秒轮询一次，采集是**逐页**推进的 —— 每页写一次 Mongo 意味着一个批次最多几百次写，
    只为展示进度，不划算。做法是：
    - 每个目标开跑**前**先往 `details` 里放一条 `RUNNING` 占位（否则一个目标要跑 1~2 分钟，
      页面在它跑完之前什么都看不到 = 用户说的「黑盒等待」）
    - `CollectLoop` 每采完一页回调一次 → 造一个**全新的** `RefreshDetail` 换进快照
    - 每次发布都是 `AtomicReference.set(新列表 + 新元素)`，**绝不原地改字段** ——
      快照可能正被 HTTP 线程读着，原地改会让它读到「改了一半」的对象
    - `trigger()` / `runScheduled()` 在 CAS 成功后就 `liveDetails.set(null)`，
      免得批次真正开始前的几毫秒里页面看到**上一批**的残留明细

11. **「新增」和「更新」是两个数，别只报一个。**
    `booksSaved` 是 upsert 总数，整期榜单（200 本）会被重写一遍，其中绝大多数是老书。
    新增数来自 `BulkWriteResult.getUpserts().size()`，更新数来自 `getMatchedCount()`，
    经 `book.dto.UpsertStat` → `CollectResult.booksInserted` → `RefreshDetail.booksInserted`
    一路上来。**零额外查询**（原先就在取，只是相加后丢掉了区分）。
    ⚠️ 口径是「库里原本没有这个 `bookId`」—— 手动删过的书再采到会重新算新增。

## 7. 依赖与耦合

- **依赖**：`collector`（`CollectLoop`）、`task`（`TaskRegistry` / `TaskHandle`）、
  `config`（`TaskProperties`）、`common`（`BizException` / `ResultBean` / `TargetType`）。
- **被依赖**：无（没有任何模块依赖本模块）。
- **改 `CollectCommand` / `CollectLoop` 时注意**：本模块是 `skipCursor=true` 的**唯一**使用方。
  删掉这个字段会让刷新任务退化成「续传」，而且**不会报错** —— 只会表现为
  「某个榜单某一期少了排在前面的新书」。

## 8. 测试与验收

本模块**没有**单元测试（项目约定：不写单测）。手工验收：

1. 重启后端 → 「增量配置」页应显示 `cron=0 0 3 * * ?`、`enabled=false`、8 个目标
2. 点「立即执行」→ 立刻返回，页面出现「执行中」并开始轮询；1~2 分钟后变「成功」
3. **看得到进度**（2026-10-08 加）：执行中「最近一次执行」卡会变成**「本次执行进度」**，
   标题右边显示「已完成 N / 8 个目标，正在采「X」」；表格里正在采的那行是
   `执行中` 标签 + 实时增长的页数/本数。点「刷新进度」按钮可立刻手动拉一次
4. **看得到增量**（2026-10-08 加）：表格有「新增」列（高亮），
   「说明」列写的是「采集 N 页，新增 X 本、更新 Y 本」，
   批次汇总写的是「8 个目标全部刷新完成，新增 X 本、更新 Y 本」
5. 验收关键点：**跑完之后去「采集游标」页看，8 个目标的游标一个字节都不该变**
6. 反例验收：手工启一个「飙升榜」的采集任务 → 点「立即执行」→ 应返回
   「定时任务被手动采集占用，已中止」，且**没有**任何目标被采

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 停用之后再也起不来了

- **现象**：把「启用定时」关掉，过一阵再打开，到点了却不跑。
- **根因**：`Trigger` 在未启用时返回了 `null` → `ReschedulingRunnable` 不再重排（铁律 5）。
- **修法**：已按铁律 5 实现（未启用也照常算下一次）。改 `RefreshScheduler` 时**不要**动这个分支。

### 9.2 页面永远显示「执行中」

- **现象**：进程重启后，「增量配置」页一直显示执行中。
- **根因**：进程被杀时来不及写终态，DB 里留下 `RUNNING`，而内存里没有批次在跑。
- **修法**：`@PostConstruct` 里的 `resetStaleRunning()` 会把它标成 `INTERRUPTED`。
  如果没生效，先确认后端真的重启了（对比 class 编译时间，见 skill 的对应小节）。

### 9.3 手动任务报「任务 定时刷新」正在采集

- **现象**：手动启一个榜单任务，报错说目标正在采集中（任务 定时刷新）。
- **根因**：刷新批次正持有该目标的锁 —— 这是**正确**行为，不是 bug。
- **修法**：等它跑完（一次批次约 1~2 分钟），或在「增量配置」页确认它已结束。

### 9.4 「写入/更新」的数字远大于「新增」

- **现象**：刷新完显示「写入/更新 200 本」，但感觉没进多少新书。
- **根因**：`booksSaved` 是 **upsert 计数**，整期榜单（200 本）会被重写一遍，
  其中绝大多数是老书。**这不是 bug。**
- **修法**：✅ 2026-10-08 已修 —— 表格新增了高亮的「新增」列，
  它是从 `BulkWriteResult` 的 upserts 数直接来的（见铁律 11），
  不再需要人去仪表盘对比「今日新增」。
  ⚠️ 两个口径仍然不同：本页「新增」= **本次批次**新增；仪表盘「今日新增」= 按
  `books.firstCollectedAt` 聚合的**自然日**增量（跨批次、跨手动任务）。

### 9.5 采了但页面显示「什么都没发生」

- **现象**：直接调 `POST /api/refresh/trigger`（没打开过页面），采集跑了、书也入库了，
  但刷新页一直显示「从未执行」、明细是空的。
- **根因**：`updateFirst` 在**文档不存在时静默不生效**（matchedCount=0，不报错）。
  单例文档是靠 `loadOrCreate()` 惰性创建的，而 `trigger` 不读 GET 接口就没有这个机会。
- **修法**：`RefreshJobRepository.update(Update)` 里**先 `loadOrCreate()`** 再下发 `Update`。
  改这个私有方法时**不要**把这一步删掉。
