# collector 模块知识

> 包路径：`com.bookcollector.collector` · 最后更新：2026-10-08
> **本模块是「和微信读书接口打交道」的全部代码。改 `collector/` 前先读第 6、9 节。**

## 1. 这个模块是干什么的

按「目标（分类 / 榜单）+ 起始位置」分页抓取微信读书的图书列表，解析成 `Book`，
按 `bookId` 幂等 upsert 进 `books`，并把每一页请求落进 `api_requests` 供事后排查。

它**不知道**「任务」这个概念 —— 它只接收一个 `CollectCommand`（目标 + 起始游标 + 最大页数），
跑完返回 `CollectResult`。任务的启停、暂停、取消是通过注入的 `CollectControl` 接口反向控制的。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `CollectLoop` | 主循环 | **核心**：翻页 → 限速 → 重试 → 解析 → 落库 → 上报，322 行 |
| `WereadClient` | HTTP 客户端 | 拼 URL + 发请求，返回**不抛异常**的 `WereadRawResponse` |
| `BookParser` | 解析器 | 微信读书 JSON → `Book`（46 字段并集 + 清洗） |
| `BookWriter` | 落库 | 分批（500/批）调 `BookRepository.upsertMany` |
| `SimpleRateLimiter` | 限速器 | 令牌桶，≥1 秒/页 |
| `ProgressReporter` | 进度上报 | 写 `collect_task_runs` / `collect_task_logs` |
| `WereadHeaderInterceptor` | 拦截器 | 给每个请求注入自定义 Header（UA 等） |
| `WereadProbe` | `CommandLineRunner` | 手工探针，**默认关闭**，排查接口时临时打开 |
| `CollectControl` | 接口 | 暂停 / 取消的**回调契约**（由 `task.TaskHandle` 实现） |
| `CollectProgressListener` | 接口 | **逐页进度回调**（纯内存旁路，定时刷新用；见 3.1） |
| `CollectCanceledException` | 异常 | 取消信号，沿循环向上抛 |
| `dto/CollectCommand` | 入参 | 一次采集的全部参数（目标、游标、页数上限、进度回调） |
| `dto/CollectResult` | 出参 | 页数、保存数、**新增数**、最终游标、错误信息 |
| `dto/WereadPage` | 中间态 | 一页的解析结果（books + hasMore + searchIdx 列表） |
| `dto/WereadRawResponse` | 中间态 | 原始响应 + 状态码 + 失败原因（**措辞的唯一来源**） |

**几个容易忘的实现细节**：

- `WereadHeaderInterceptor` 注入 **6 个** Header；其中 `Accept-Encoding` **刻意去掉 `br`**，只留
  `gzip, deflate` —— Java 的 `HttpClient` 不认 brotli，留着会让响应解不开。
- `SimpleRateLimiter` **不是 Spring bean**，由 `CollectLoop` 自己 `new`（它是有状态的，
  每个循环一个实例，注册成单例反而会串）。
- `CollectCanceledException` **覆写 `fillInStackTrace()` 返回 `this`** —— 取消是控制流，
  不是故障，不需要栈；采集循环里会抛很多次，省下建栈的开销。
- `ProgressReporter` 上报失败**静默降级**（只打 warn）：进度是旁路，不该让采集失败。
  ⚠️ `onPage` 的签名是
  `onPage(runId, pagesDone, booksSaved, booksInserted, cursor, totalCount)` ——
  **两个图书计数是相邻参数**，改签名时别插错位置（`CollectLoop` 是唯一调用点）。
- `BookWriter.BATCH_SIZE = 500`，分片调 `BookRepository.upsertMany`。
  ⚠️ 它返回的是 `book.dto.UpsertStat`（**更新数 / 新增数**），不是单个 int ——
  见 3.1。
- `WereadProbe` 是 `CommandLineRunner`，只在 `probe` profile 下启用，**默认关闭**。

## 3. 调用关系（图谱）

```
task.TaskRunner（采集线程）
      │  CollectCommand + CollectControl
      ▼
  CollectLoop.run(cmd)  ◄── 唯一入口
      │
      ├─► WereadClient.buildUrl(type, targetId, maxIndex)
      ├─► WereadClient.fetchRaw(...) ──► wereadRestTemplate ──► 微信读书
      │        │                              ▲
      │        │                              └── WereadHeaderInterceptor（注入 Header）
      │        └─► WereadRawResponse { statusCode, body, error }
      │
      ├─► ApiRequestRepository.record(...) ──► api_requests   （成功失败都记）
      ├─► BookParser.parseAll(nodes) ──► List<Book>
      ├─► BookWriter.upsertAll(books, sourceKey) ──► BookRepository.upsertMany ──► books
      │        └─► 返回 UpsertStat { 更新数, 新增数 }
      ├─► ProgressReporter.onPage(...) ──► collect_task_runs / collect_task_logs
      ├─► CollectProgressListener.onProgress(...)   （cmd 带回调时；纯内存，不落库）
      ├─► SimpleRateLimiter.acquire()      （≥1 秒/页）
      └─► CollectControl.awaitIfPaused() / checkPoint()   （暂停阻塞、取消抛异常）
```

**入参出参都不含 Spring 上下文**：`CollectLoop` 不依赖 `TaskService` / `TaskRegistry`，
只认 `CollectControl` 接口 —— 所以它可以被单测直接 new 出来跑。

### 3.1 🔴 两条进度通道别混（2026-10-08 加）

| | `ProgressReporter` | `CollectProgressListener` |
|---|---|---|
| 落地 | 写 Mongo（`collect_task_runs` / `collect_task_logs`） | **纯内存**，调用方自己消费 |
| 谁用 | 真实采集任务（有 `runId`） | **定时刷新**（`runId=null`，没有任务实体） |
| 怎么触发 | `CollectLoop` 里无条件调（内部对 `runId=null` 静默降级） | 只在 `cmd.getProgressListener() != null` 时调 |
| 抛异常 | 内部自己吞 | `CollectLoop` 兜 `RuntimeException` + 记 warn |

**为什么不能只用 `ProgressReporter`**：定时刷新没有 `runId`，它的所有方法都是空转，
页面上就变成「黑盒等待」（用户 2026-10-08 的原话）。

**为什么回调是「逐页」而不是「逐本」**：一页 20 本、页间隔 ≥1 秒，
逐本回调会让采集线程多跑 20 倍的无用功，而进度粒度上没有区别。

**回调触发点**：只在**真正写入了一页**之后（`CollectLoop` 第 8 步）——
空页 / 请求失败的那一页不触发，因为那页没有任何写入。

**新增 / 更新是怎么分开的**：`BulkWriteResult` 本来就同时给了
`getMatchedCount()`（命中已有文档 = 更新）和 `getUpserts().size()`（真正插入 = 新增），
原先只是相加后把区分丢掉了。**没有多做任何一次查询**。

## 4. 数据集合与索引

| 集合 | 读/写 | 依赖索引 |
|---|---|---|
| `books` | 写（upsert） | `uk_bookId` **唯一** —— 幂等 upsert 的**正确性依赖**，不是性能优化 |
| `api_requests` | 写（只插） | `idx_createdAt` · `idx_runId` |
| `collect_task_runs` | 写（进度） | `idx_taskId` · `idx_startedAt` |
| `collect_task_logs` | 写（日志） | `idx_runId` |

> 本模块**不读**任何集合做业务判断（除了 `BookRepository.upsertMany` 内部的 upsert）。

## 5. 对外接口

本模块**不暴露 HTTP 端点**。对外契约是三个 Java 接口：

```java
// 入口
CollectResult CollectLoop.run(CollectCommand cmd);

// 反向控制（由 task.TaskHandle 实现）
interface CollectControl {
    boolean isCanceled();
    void awaitIfPaused() throws InterruptedException;
    default void checkPoint() throws InterruptedException;   // 取消则抛 CollectCanceledException
}

// HTTP 客户端
WereadRawResponse WereadClient.fetchRaw(TargetType type, String targetId, int maxIndex);
```

## 6. 不变量与铁律 ← 改这个模块前必读

1. **`books` 是「历史累计的并集」，不是「当前榜单快照」。**
   微信读书分类列表按 `readingCount` 排序，**并列时 tie-break 不稳定** ——
   实测「文学」前 100 名在**几分钟内**就会换掉一两本，而且是来回抖的。
   - 秒级（同一轮内）：**完全稳定**，同范围两次请求 `bookId` 集合一模一样
   - 分钟级（跨轮）：**会漂移**，边界上有书进出

   推论：**不要**拿 `books` 总数跟接口 `totalCount` 对账；跨较长时间重采同一范围总数 ±N
   **不是 bug**；幂等的准确表述是「**对同一份响应 upsert 幂等**」，不是「集合总数恒定」。
   **永不删除**：掉出榜单的书几分钟后还会回来，按「以最新榜单为准」删数据会被反复删建。

2. **`RestTemplate` 的错误处理器必须保持「不抛异常」。**
   Spring 默认的 `DefaultResponseErrorHandler` 在 4xx/5xx 上抛异常，
   异常被 `fetchRaw` 的 catch 包成 `error` 且 `statusCode` 写成 `-1`。两个后果**都是静默的**：
   状态码丢了（审计页把 500 显示成 `-1`）、「4xx 不重试」变成死代码（白等退避 1s+3s）。
   修法是 `RestTemplateConfig.RawResponseErrorHandler`（`hasError()` 恒 `false`）。
   **不要改回默认处理器。** 详见第 9.1 节。

3. **失败原因的措辞一律走 `WereadRawResponse.describeFailure()`。**
   采集日志、run 的 `errorMsg`、审计的 `errorMsg` 三处共用一份 ——
   用户在「任务失败原因」和「请求审计」里看到的必须是同一句话。

4. **限速 ≥1 秒/页，是全局的。** 并发跑两个任务 = 请求频率翻倍，有被上游限流风险。
   所以并发闸门设成 1（见 `task` 模块铁律 7）。

5. **不吞中断。** `CollectControl.awaitIfPaused()` 声明 `throws InterruptedException`，
   不要 try-catch 掉。吞掉的后果是循环带着中断标志继续跑，
   后面的 `sleep` / 限速器立刻抛异常 → 表现成「任务莫名失败」。

6. **`searchIdx` 在列表项的**外层**，不在 `bookInfo` 里。**
   分页游标 `maxIndex` = **本页最后一条的 `searchIdx`**（从 1 开始），不是页码。

7. **`newRating` 是 0~1000 的推荐值，原样存**（913 = 91.3%），展示层自己除 10。
   🔴 字段路径是**顶层** `newRating`，不是 `newRatingDetail.newRating`（后者不存在）。

## 7. 依赖与耦合

- **依赖**：`book`（`Book` / `BookRepository`）、`audit.repository.ApiRequestRepository`、
  `task.entity.{TaskRun,TaskLog}`（经 `ProgressReporter`）、`config.WereadProperties`、
  `common.enums.TargetType`。
- **被依赖**：`task.TaskRunner` / `TaskService(Impl)`。
- **已知的环（设计层面耦合，本轮不解决）**：
  - `collector ↔ task`：进度上报写任务集合，任务执行调采集引擎
  - `collector ↔ audit`：审计要记原始响应，采集要写审计
  - `collector ↔ config`：`WereadProperties` 与 `WereadHeaderInterceptor` 互相引用

## 8. 测试与验收

| 测试 | 覆盖 |
|---|---|
| `BookParserTest`（单测，离线） | 解析 + `cleanValue` 清洗 |
| `S2PageStabilityIT` | **幂等性基石**：同范围两次请求 `bookId` 集合一致、upsert 不重复插入 |
| `CollectEngineIT` | 真打接口跑通一轮采集 |
| `CollectRetryFailureIT` | 失败路径：接口 500 / 404 / 断网的重试次数与耗时（假服务） |

```bash
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=BookParserTest
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=S2PageStabilityIT
```

> 🔴 **不要删 `S2PageStabilityIT`** —— 整个幂等性都建立在它之上。

**给「对端异常」写测试的范式**（`CollectRetryFailureIT`）：用 JDK 自带的
`com.sun.net.httpserver.HttpServer` 起一个假微信读书，通过 `@DynamicPropertySource`
把 `bookcollector.weread.base-url` 指过去：

```java
@DynamicPropertySource
static void pointWereadAtFakeServer(DynamicPropertyRegistry registry) {
    registry.add("bookcollector.weread.base-url",
            () -> "http://127.0.0.1:" + FAKE_PORT + "/web/bookListInCategory");
}
```

好处是**能精确数出服务端收到了几次请求** —— 这是断言「重试了几次」唯一诚实的办法。
「断网」场景就把假服务 `stop(0)`，此时数不出来，用「总耗时 ≥ 退避合计（4s）」反证。
**不要 mock 掉 `WereadClient`** —— 那就变成「测自己写的 mock」了。

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 状态码被静默吞掉（S7 实测）

- **现象**：审计页把一次 HTTP 500 显示成 `statusCode = -1`，失败原因写成
  「网络异常 InternalServerError」，看起来像网线掉了。更隐蔽的是接口 404 也会重试 3 次。
- **根因**：`RestTemplate` 的 `DefaultResponseErrorHandler` 在 4xx/5xx 上抛异常，
  异常在 `WereadClient.fetchRaw` 的 catch 里被包成 `error`，`statusCode` 落成 `-1`；
  而 `isRetryable()` 的第一条判据是 `error != null` → 抛异常必然让 `error != null`。
- **修法**：`RestTemplateConfig.RawResponseErrorHandler`（`hasError()` 恒返回 `false`），
  让状态码原样交回 `CollectLoop` 决策。实测效果：

  | 用例 | 修复前 | 修复后 |
  |---|---|---|
  | 接口 500 | 重试 3 次，`errorMsg` =「网络异常 InternalServerError」 | 重试 3 次，`errorMsg` =「**第 1 页采集失败：HTTP 500**」 |
  | 接口 404 | **重试 3 次**，耗时 **4036ms** | **只打 1 次**，耗时 **8ms** |
  | 断网 | 重试 3 次，网络异常 | 不变 |

  > 🔴 **只有真打 HTTP 才能发现这个**：`CollectEngineIT` / `TaskControlIT` 打的都是正常的 200，
  > 类型检查和单测一个都照不出来。

### 9.2 一个分类最多 500 本（25 页），`maxPages` 设大了也没用

- **现象**：把 `maxPages` 设成 60，任务却在第 26 页正常结束。
- **根因**：🔴 S7 实测：`maxIndex=480` 是最后一页，`maxIndex>=500` 返回 36 字节的
  `{"books":[],"hasMore":0}`。文学 / 精品小说 / 计算机 / 童书全一样。
  榜单更短：`rising` 只有 39 本 / 2 页。
- **修法**：**这是接口事实，不是 bug**。一个分类任务最多 25 页 ≈ 29 秒跑完。
  做时间预算时不要引用「单采完约 45 分钟」那个已被推翻的估算（方案文档 R23 已修正）。

### 9.3 `totalCount` 不是进度分母

- **现象**：接口报「文学共 54086 本」，但翻到第 25 页就没了。
- **根因**：`totalCount` 是「该分类共 N 本」，**不代表能翻完**。
- **修法**：进度用「已跑页数 / `maxPages`」，不要用 `totalCount`。

### 9.4 `publishTime` 存在 `"0000-00-00 00:00:00"` 这类脏值

- **现象**：年份趋势图上出现一个「0000 年」的尖峰。
- **根因**：库里有「未知时间」的占位值。
- **修法**：聚合时用 `$gte 1900 $lte 2100` 过滤（在 `stats` 模块），
  取年份用 `$split` + `$arrayElemAt` 而不是 `$substrBytes`（后者对短于 4 字符的字符串行为依赖版本）。

### 9.5 🔴 榜单漂移会让相邻两页**重叠**（或留空洞）—— `maxIndex` 分页的固有性质

- **现象**：连走 5 页（每页 20 本），按 `bookId` 去重后只有 **99** 本而不是 100。
  `S2PageStabilityIT` 就是踩在这上面红的。
- **根因**：分页是 **`maxIndex`（searchIdx 偏移）式**的 —— 第 N 页用「上一页最后一条的
  `searchIdx`」当游标。而榜单是**可变列表**：两次请求之间（本项目实测间隔仅约 1 秒）
  若有书进出，位置整体平移，边界处就会**重叠**（同一本出现在相邻两页 → 去重后少 1）
  或**空洞**（一本被跳过）。
  **这是偏移式分页在可变列表上的固有性质，客户端无法消除**（除非上游给稳定快照/游标）。
- **怎么确认是这个原因**（而不是解析丢了书）——两个数字一对照就定性：
  1. `api_requests.resultCount` 每页都是 **20**（= `WereadPage.size()`，**原始节点数**，未解析）
  2. 日志里**没有** `解析第 N 条（searchIdx=…）失败` 的 WARN
  ⇒ 100 次解析全成功，却只有 99 个不同 `bookId` ⇒ **必定是跨页重复**，不是解析问题。
  （若 `resultCount` 某页 < 20，才是上游真的少给；若出现解析 WARN，才是解析器的问题。）
- **修法**：**产品行为是对的，不要改采集逻辑** —— 见铁律 1：`books` 是「历史累计的并集」，
  重复的 `bookId` upsert 天然幂等，空洞也只是「这本这次没采到」。
  ⚠️ 但**不要写「5 页恰好 100 本」这种断言** —— 那等于要求上游榜单在两次请求之间不变。
  正确的验收写法：**每页 20 条 + `searchIdx` 全程严格递增 + 两次走的 `bookId` 集合允许少量对称差**。

> ✅ **2026-09-23 已按此修好**：`S2PageStabilityIT` 已重写为断言**与榜单内容无关的分页不变量** ——
> 每页 20 条原始节点 / 20 本解析成功、`searchIdx` 全程严格递增、从 1 开始、
> 覆盖到 `100 ± MAX_DRIFT`（`MAX_DRIFT = 5`，够松到容忍漂移、又紧到能抓住游标失效）。
> 方法名也从 `twoConsecutiveWalksAreIdentical` 改为 `twoConsecutiveWalksAreStable`
> —— 一个容忍差异的测试不该叫 "AreIdentical"。

