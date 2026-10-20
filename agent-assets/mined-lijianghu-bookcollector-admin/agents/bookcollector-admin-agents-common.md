# 基础设施知识（common / config / util / system）

> 包路径：`com.bookcollector.{common,config,util,system}` + `setting` 附录 · 最后更新：2026-09-23
> 这四个包**不属于任何业务模块**，是全项目共用的地基。改这里的影响面是全项目。

## 1. 这些包是干什么的

| 包 | 定位 | 一句话 |
|---|---|---|
| `common` | **跨模块公共组件** | 统一返回体、异常、异常处理器、分页结果、TraceId、两个枚举 |
| `config` | **基础设施装配** | 全部 `@Configuration` + 3 个 `*Properties` + 启动期初始化（索引 / 字典） |
| `util` | **全局无状态工具** | 目前只有 `PageQueryUtil` |
| `system` | **系统级 Controller** | 只有 `PingController`（连通性探针） |

> 判定标准：**「被 2 个以上业务模块使用」才放这里。** 只有一个模块用的东西留在模块内。

## 2. 类清单

### common

| 类 | 职责 |
|---|---|
| `ResultBean<T>` | 统一返回体 `{ code, message, traceId, data }` |
| `BizException` | 业务异常，带 `code`，被异常处理器翻译成 `ResultBean` |
| `GlobalExceptionHandler` | `@RestControllerAdvice`，8 个 `@ExceptionHandler` 分支（含 `NotLoginException` → 4100） |
| `PageResult<T>` | 分页信封 `{ list, total, page, size }` + 派生 `getTotalPages()` |
| `TraceIdFilter` | Servlet `Filter`，给每个请求打 traceId 并塞进 MDC |
| `enums/TargetType` | `CATEGORY` / `RANKING`，含 URL 拼装语义 |
| `enums/TaskStatus` | 7 个状态 + `isTerminal()` / `isActive()` / `isResumable()` |

### config

| 类 | 职责 |
|---|---|
| `MongoConfig` | `MongoTemplate` 装配 |
| `MongoIndexInitializer` | `ApplicationRunner`，**启动时显式建 23 个索引 / 覆盖 12 个集合** |
| `RestTemplateConfig` | `wereadRestTemplate` + `WereadHeaderInterceptor` + `RawResponseErrorHandler` |
| `WebMvcConfig` | 注册 `AuthInterceptor`（拦截 `/api/**`）+ `@ExtractLoginUser` 参数解析器 |
| `AsyncConfig` | `collectExecutor` 线程池 + 关停唤醒（`ContextClosedEvent`） |
| `SwaggerConfig` | springdoc OpenAPI |
| `SeedRunner` | `ApplicationRunner`，播种 21 分类 + 7 榜单 + 2 条 settings + **1 个初始管理员**（`sys_user`，密码存 MD5） |
| `AuthProperties` | `bookcollector.auth.*` —— **初始管理员的播种参数**（`initial-username` / `initial-password` / `initial-nickname`），**不是登录校验的来源**；只在库里没有同名用户时用一次 |
| `WereadProperties` | `bookcollector.weread.*`（base-url / 超时 / 限速 / 重试） |
| `TaskProperties` | `bookcollector.task.*`（并发闸门 / 列表上限） |

### util / system / setting

| 类 | 职责 |
|---|---|
| `util/PageQueryUtil` | 分页样板收敛（3 个方法 + 2 个归一化工具） |
| `util/Md5Util` | MD5 摘要（32 位小写 hex）+ `matches` 校验。**只用于 `sys_user` 密码**，理由与边界见类注释 |
| `system/controller/PingController` | `/api/ping`、`/api/ping/biz-error` |
| `setting/entity/Setting` | 系统配置 KV（集合已建，**当前无业务代码引用**） |

**几个容易忘的实现细节**：

- **`AsyncConfig` 的线程池参数**（bean 名 `collectExecutor`，常量 `AsyncConfig.COLLECT_EXECUTOR`）：
  `corePoolSize=1` · `maxPoolSize=2` · `queueCapacity=TaskProperties.queueCapacity`（默认 **16**）·
  `threadNamePrefix="collect-"` · 拒绝策略 **`AbortPolicy`** · `waitForTasksToCompleteOnShutdown=true` ·
  `awaitTerminationSeconds=20`。
  - 🔴 **真正的并发闸门不在这里，在 `bookcollector.task.max-concurrent-runs`（默认 1）** ——
    见 `task/AGENTS.md` 铁律 7。core=1 + 有界队列的**实际效果**确实是「最多 1 个在跑」，
    但那是线程池的副产品，不是设计意图；接口限速是全局的，并发跑两个任务 = 频率翻倍。
  - **`AbortPolicy` 是刻意的**：队列满了直接拒绝（抛 `TaskRejectedException`），
    而不是让 HTTP 线程阻塞等待 —— 拒绝比静默排队更好排查。
- **`MongoConfig` 只做两件事**：`@EnableMongoAuditing` + **把 `DateTimeProvider` 钉死**成
  `LocalDateTime.now(ZoneId.systemDefault())`。默认的 `CurrentDateTimeProvider` 虽然行为一样，
  但把时区**显式写出来**，读代码的人一眼能看出「存的是本地时间」，不依赖 JVM 默认时区这个隐含前提。
- **`RestTemplateConfig` 装配 `wereadRestTemplate`** 三件套：
  `HttpComponentsClientHttpRequestFactory`（包 Apache HttpClient，**只支持 4.5.x** ——
  这是 Spring Boot 2.3 + JDK 8 的版本约束）+
  `WereadHeaderInterceptor` + `RawResponseErrorHandler`（后者**不能改回默认**，见铁律 6）。
  > 为什么不用 `SimpleClientHttpRequestFactory`：那是 JDK `HttpURLConnection`，**Header 行为不可控**。

## 3. 调用关系（图谱）

```
所有 Controller ──► ResultBean.ok(...)         （统一返回体）
所有 Service    ──► BizException.*             （业务异常）
                        │ 抛
                        ▼
              GlobalExceptionHandler ──► ResultBean{code,message,traceId}

所有 Repository ──► PageQueryUtil              （分页样板）
                    PageResult

每个 HTTP 请求 ──► TraceIdFilter（Filter）──► MDC.traceId ──► 日志 %X{traceId}
                                                │
                      AuthInterceptor ◄─────────┘  （同属请求链路，但职责独立）

启动期（一次性，顺序不保证）
  MongoIndexInitializer ──► 23 个索引（12 个集合）
  SeedRunner            ──► taxonomy_config（195 条）+ settings（2 条）+ sys_user（1 条）
                             taxonomy_config = 一级分类 22 + 二级分类 166 + 榜单 7
  InterruptedTaskDetector ──► 把遗留的活跃任务标 INTERRUPTED
```

## 4. 数据集合与索引

`config/MongoIndexInitializer` 是**全部 23 个索引的唯一来源**（覆盖 12 个集合）：

| 集合 | 索引 | 类型 |
|---|---|---|
| `books` | `uk_bookId` | **唯一** |
| | `idx_categories` / `idx_lastCollectedAt` / `idx_newRating` / `idx_firstCollectedAt` | 普通 |
| `api_requests` | `idx_createdAt`(DESC) / `idx_runId` | 普通 |
| `collect_tasks` | `uk_target (targetType,targetId)` | **唯一** |
| | `idx_status` / `idx_createdAt`(DESC) | 普通 |
| `collect_task_runs` | `idx_taskId` / `idx_startedAt`(DESC) | 普通 |
| `collect_task_logs` | `idx_runId` | 普通 |
| `collect_cursors` | `uk_target (targetType,targetId)` | **唯一** |
| `taxonomy_config` | `uk_type_code (type,code)` | **唯一** |
| | `idx_sort` | 普通 |
| `settings` | `uk_key` | **唯一** |
| `sys_user` | `uk_username` | **唯一** |
| `book_interpretations` | `uk_bookId` | **唯一** |
| | `idx_status_rating (status, newRatingCount DESC, _id)` | 普通 |
| `publish_record` | `idx_publishedAt`(DESC) | 普通 |
| `shelf_books` | `uk_bookId` | **唯一** |
| | `idx_category_addedAt (category, addedAt DESC, _id)` | 普通 |

> 库里业务索引**总数是 26**（= 上面 23 个 + 用户手工在 `ai_sensitive_words`(1) /
> `ai_taxonomy_config`(2) 上自己建的 3 个）。`MongoIndexInitializer` 不碰那 4 张 `ai_*` 表。

> **为什么不用 `@Indexed` 注解自动建**：唯一索引是幂等写入的**正确性依赖**
> （不是性能优化），必须显式、可审计、可在启动日志里核对。
> `application.yml` 里 `spring.data.mongodb.auto-index-creation: false`，实体上**不使用** `@Indexed`。

## 5. 对外接口

### 统一返回体（`ResultBean`）

```json
{ "code": 200, "message": "ok", "traceId": "d337f6005f9a407e", "data": { } }
```

| 常量 | 值 | 含义 |
|---|---|---|
| `code_ok` | 200 | 正常 |
| `code_warn` | 400 | 参数错误 |
| `code_notfound` | 404 | 未找到 |
| `code_duplicateKey` | 405 | 主键重复 |
| `code_err` | 500 | 错误 |
| `code_session_invalid` | **4100** | 身份已失效（🔴 见铁律 3） |

### `PingController`

| 方法 | 路由 | 说明 |
|---|---|---|
| GET | `/api/ping` | 返回 `pong` + 运行信息（java 版本、编码、traceId、**中文编码测试串**） |
| GET | `/api/ping/biz-error` | 故意抛 `code_warn` 异常，验证错误码链路 |

## 6. 不变量与铁律 ← 改这里前必读

1. **`common` 只放「被 2 个以上模块使用」的东西。** 只有一个模块用的留在模块内 ——
   否则 `common` 会变成一个什么都往里塞的垃圾桶，依赖方向也会失控。

2. **`util` 只放无状态工具类。** 工具类必须是 `final` + 私有构造器抛
   `AssertionError`（见 `PageQueryUtil`）。有状态的东西放 `common` 或模块内。

3. **🔴 鉴权失败的 HTTP 状态码是 200，body 里 `code=4100`。**
   前端 axios 拦截器只看 body 的 `code`。改这个数字前先看 `auth/AGENTS.md` 铁律 1。

4. **索引必须在 `MongoIndexInitializer` 里显式创建，不用 `@Indexed`。**
   唯一索引是**正确性依赖**。新增唯一索引时若库里已有重复数据，启动会失败 ——
   先手工去重（`collect_tasks` 那段注释里有聚合命令）。

5. **`ensureIndex` 是「按名字 upsert」，同名已存在时它什么都不做**（不比较字段）。
   所以改索引字段时**必须**用 `dropIndexIfFieldChanged` 先删旧的 ——
   否则索引会一直建在错字段上，**而且没有任何提示**。
   （`idx_newRating` 就踩过这个坑。）

6. **`RestTemplateConfig.RawResponseErrorHandler` 不能改回默认处理器。**
   默认的 `DefaultResponseErrorHandler` 在 4xx/5xx 上抛异常，会静默吞掉状态码。
   详见 `collector/AGENTS.md` 第 9.1 节。

7. **`TraceIdFilter` 是 Filter，`AuthInterceptor` 是 Interceptor —— 这个分工不要换。**
   Filter 需要覆盖所有请求（含静态资源）；Interceptor 需要按路径精确放行。
   两者职责不同，工具选择也就不同。

   （Sa-Token 自己注册的 `SaTokenContextFilterForServlet` 也属于 Filter 那一类 ——
   它给每个请求铺 Sa-Token 的上下文，是基础设施，不是业务拦截。）

8. **`AsyncConfig` 的关停唤醒用 `ContextClosedEvent`，不用 `@PreDestroy`。**
   为什么：Spring 关闭顺序是「发事件 → 停线程池 → destroyBeans」，
   `@PreDestroy` 太晚，会白等 `awaitTerminationSeconds`。

9. **`@Configuration` 类不要加 `@ComponentScan` 之类扩大扫描范围的东西**，
   也不要手动 `new` 业务 Bean —— 全部走构造器注入。

10. **`PageQueryUtil` 有三条刻意保留的行为，改它时不要动。**

    - **`count == 0` 短路**：总数为 0 时直接返回 `PageResult.empty(page, size)`，**不发 `find`**。
      省一次往返；语义上「没有数据」时排序也无意义。
    - **不提供默认排序字段**：本项目的业务字段是 `lastCollectedAt` / `createdAt` / `startedAt`，
      **没有通用的 `createTime`**。`sortField` 传空**直接抛 `IllegalArgumentException`**，
      而不是静默按某个字段排 —— 静默回退会退化成自然序**且不报错**，是最难查的一类问题。
    - **必须支持两级不同方向的排序**：「主排序字段 + `_id ASC` 兜底」是保证**同值记录翻页
      不重不漏**的关键。所以 `Sort` 那个重载不能删。

    **内部执行顺序也是行为的一部分**：先 `count`（**未加 skip/limit**）→ 为 0 短路 →
    再 `with(sort)` → 最后 `with(PageRequest)`。调换顺序会让 `count` 带上分页参数，总数直接算错。

## 7. 依赖与耦合

- `common` **不依赖**任何业务模块（只有 `enums` 被业务模块依赖）。这是必须守住的边界。
- `config` 会依赖业务模块（`MongoIndexInitializer` 里的集合名、`SeedRunner` 里的字典、
  `RestTemplateConfig` 依赖 `collector.WereadHeaderInterceptor`、`AsyncConfig` 依赖
  `task` 的配置语义）—— 这是**已知的环**（`collector ↔ config`），本轮不解决。
- `config` 现在还依赖 `auth` 的 `SysUser` / `SysUserRepository`（`SeedRunner` 播种初始管理员）。
  **没有引入新的环**：`auth` 只反向依赖 `config.AuthProperties` 这个纯 POJO，
  不依赖 `config` 的任何业务语义。
- `util` 只依赖 `common`。

## 8. 测试与验收

`S1DataLayerTest` 校验索引存在性与唯一约束；
`ApiContractTest` 校验返回体结构与错误码；
`ApiCrudIT` 走真实 HTTP 覆盖 `GlobalExceptionHandler` 的各分支；
`AuthIT` 覆盖鉴权的三处「不报错的失败」（见 `auth/AGENTS.md` 第 8 节）。

```bash
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=S1DataLayerTest
```

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 启动日志里索引数不是 23

- **现象**：日志显示「索引初始化完成：N 个索引」，N ≠ 23。
- **根因**：改了 `initXxx()` 的返回值却没改 `ensureIndex` 调用数，或反之。
- **修法**：每个 `initXxx()` 的 `return` 值必须等于该段里 `ensureIndex` 的条数。
  启动日志会打印总数，可以直接核对。

### 9.2 加了新唯一索引后服务起不来

- **现象**：启动报 `E11000 duplicate key error`。
- **根因**：库里已有违反新唯一约束的数据。
- **修法**：先手工去重再启动。`collect_tasks` 的 `uk_target` 注释里有现成的聚合命令：
  ```
  db.collect_tasks.aggregate([{$group:{_id:{t:"$targetType",i:"$targetId"},n:{$sum:1}}},
                              {$match:{n:{$gt:1}}}])
  ```

### 9.3 日志里 `[ ]` 里没有 traceId

- **现象**：日志的 traceId 位置是空的 `[]`。
- **根因**：该线程不是 HTTP 线程（如采集线程），或者日志模式串里 `%X{traceId}` 写错了。
- **修法**：`TaskRunner` 会自己把 traceId 塞进 MDC（`MDC.put("traceId", ...)`），
  采集线程的日志因此也有 traceId。新增异步线程时**必须照做**，否则日志串不起来。

### 9.4 `chineseTest` 字段出现乱码

- **现象**：`/api/ping` 返回的 `chineseTest` 是 `涓枃缂栫爜娴嬭瘯` 这种乱码。
- **根因**：控制台 / 终端的编码不是 UTF-8（Windows 默认 GBK），
  而 `fileEncoding` 字段会告诉你是哪种。**接口返回本身是正确的 UTF-8。**
- **修法**：这是终端显示问题，不是接口问题。启动脚本里已设 `-Dfile.encoding=UTF-8`。
