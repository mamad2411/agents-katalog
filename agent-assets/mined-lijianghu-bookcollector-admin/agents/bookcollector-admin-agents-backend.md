# AGENTS.md

> **本文件是 `bookcollector-admin` 的项目级开发规范**，供 AI 编码工具（Codex / Claude Code / Cursor / WorkBuddy / Trae 等）阅读并遵循。
> 仓库内 `backend/CLAUDE.md` 与本文件**内容完全一致**，修改时必须同步更新两份。
> **各业务模块另有目录级 `AGENTS.md`**（见下方「模块索引」），写的是该模块的调用关系、
> 不变量与已知陷阱 —— 改某个模块的代码前先读它。目录级 `AGENTS.md` 由各工具自动就近加载。
> 🔴 **「AI 开发约束」一节顶部的「用户硬规则」优先级最高** —— 与本文件其余条款冲突时，一律以其为准。
> 最后更新：2026-09-23

---

# 项目概览

`bookcollector-admin` 是微信读书图书采集器的**本地单机可视化后台**，由原来的 Python CLI 脚本重构而来。

**定位与形态**

- 本机 Windows 上**单用户**运行的管理后台：按分类 / 榜单采集微信读书图书数据、落库，并提供可视化查询与运维界面。
- 前后端分离的**单体 Spring Boot 应用** + Vue 3 SPA。无 Docker、无微服务、无注册中心、无网关。
- 后端端口 `8080`；前端 dev server `5173`；MongoDB `localhost:27017/bookcollector`。

**数据流**

```
微信读书接口
   ↓  WereadClient（限速 1 页/秒 + 失败重试 + 自定义 Header）
   ↓  BookParser（接口响应 → Book 实体）
   ↓  BookRepository.upsertMany（按 bookId 幂等批量 upsert）
MongoDB（books）
   ↓  REST API（ResultBean 统一包装 + PageResult 分页）
Vue 前端（6 个业务页面）
```

**采集链路**

```
collect_tasks（任务定义）
   ↓  TaskService —— 任务状态机（启动 / 暂停 / 恢复 / 取消 / 重试，同目标互斥）
   ↓  TaskRunner —— 跑在采集专用线程池里
   ↓  CollectLoop —— 分页主循环（断点续传 + 限速 + 重试）
   ↓  逐页 BookWriter 落库 + ProgressReporter 上报进度
collect_task_runs（进度）+ collect_task_logs（日志）
```

**第一期明确不做**：定时采集、SSE 实时推送（手动刷新）、权限体系（登录用户有 `roles` 字段，但**不参与任何鉴权判断**）、数据导出、ETL 迁移、模糊搜索、Docker 部署。

---

# 模块索引

> 🔴 **改某个模块的代码前，先读该模块自己的 `AGENTS.md`** ——
> 模块级的调用关系、数据集合、不变量与铁律、已知陷阱都在那里。
> 本文件只写**跨模块**的规范。

`com.bookcollector` 下有 4 类包：**业务模块**、`common`（跨模块公共组件）、
`config`（基础设施装配）、`util`（全局工具），另有 `system`（系统级 Controller）。

| 包 | 职责 | 知识文件 |
|---|---|---|
| `book` | 图书库：分页筛选 / 详情 / 编辑 / 删除 | [`book/AGENTS.md`](src/main/java/com/bookcollector/book/AGENTS.md) |
| `taxonomy` | 采集目标字典（21 分类 + 7 榜单） | [`taxonomy/AGENTS.md`](src/main/java/com/bookcollector/taxonomy/AGENTS.md) |
| `task` | **采集任务状态机** + 运行记录 + 日志 | [`task/AGENTS.md`](src/main/java/com/bookcollector/task/AGENTS.md) |
| `cursor` | 采集游标（断点续传的唯一权威） | [`cursor/AGENTS.md`](src/main/java/com/bookcollector/cursor/AGENTS.md) |
| `audit` | 请求审计（每页一条，成功失败都记） | [`audit/AGENTS.md`](src/main/java/com/bookcollector/audit/AGENTS.md) |
| `auth` | 登录鉴权（Sa-Token + `sys_user` + MD5；`@ExtractLoginUser` 注入当前用户） | [`auth/AGENTS.md`](src/main/java/com/bookcollector/auth/AGENTS.md) |
| `stats` | 仪表盘聚合（口径最讲究） | [`stats/AGENTS.md`](src/main/java/com/bookcollector/stats/AGENTS.md) |
| `collector` | **采集引擎**：主循环 / 限速 / 重试 / 解析 / 落库 | [`collector/AGENTS.md`](src/main/java/com/bookcollector/collector/AGENTS.md) |
| `refresh` | **增量配置**：8 个目标的定期**全量重采**（cron / 手动）—— **与「采集任务」是两套东西** | [`refresh/AGENTS.md`](src/main/java/com/bookcollector/refresh/AGENTS.md) |
| `publish` | **AI 书籍解读**（内容产出侧）：挑一本候选 → AI 写解读 → 落 `docs/` → 发语雀 | [`publish/AGENTS.md`](src/main/java/com/bookcollector/publish/AGENTS.md) |
| `shelf` | **我的藏书**（原「藏书阁」页）：8 列 × 3 行网格 + 下滑加载；**快照式**存储 | [`shelf/AGENTS.md`](src/main/java/com/bookcollector/shelf/AGENTS.md) |
| `readinglist` | **阅读清单**：想读 / 在读 / 已读；**快照式**存储；与 `shelf` **并列且互不影响** | [`readinglist/AGENTS.md`](src/main/java/com/bookcollector/readinglist/AGENTS.md) |
| `common` + `config` + `util` + `system` + `setting` | 基础设施（统一返回体、异常、索引初始化、线程池、探针） | [`common/AGENTS.md`](src/main/java/com/bookcollector/common/AGENTS.md) |

**两个知识最密的模块**：`task`（状态机）与 `collector`（数据源事实）。
`stats` 的核心是统计口径，`cursor` 的核心是「游标属于目标而不是任务」。

## 数据集合

**19 个集合**（2026-10-12），**集合名与字段映射不得变更**（既有数据依赖）。
⚠️ 其中 `reading_list` 是新增的：**代码已定义，但库里尚未创建** —— 后端下次启动时由
`MongoIndexInitializer.initReadingList()` 建（在空集合上建索引会顺带把集合建出来）。

| 集合 | 实体 | 说明 |
|---|---|---|
| `books` | `book.entity.Book` | 图书（46 个业务字段 + 采集元数据） |
| `taxonomy_config` | `taxonomy.entity.TaxonomyItem` | 采集目标字典 |
| `collect_tasks` | `task.entity.CollectTask` | 采集任务定义 |
| `collect_task_runs` | `task.entity.TaskRun` | 一次运行记录（含实时进度） |
| `collect_task_logs` | `task.entity.TaskLog` | 运行日志（按 run 查看） |
| `collect_cursors` | `cursor.entity.CollectCursor` | 断点续传游标 |
| `api_requests` | `audit.entity.ApiRequest` | 请求审计记录 |
| `settings` | `setting.entity.Setting` | 系统配置 KV |
| `sys_user` | `auth.entity.SysUser` | 登录用户（**密码存 MD5 摘要，不存明文**） |
| `book_interpretations` | `publish.entity.Interpretation` | AI 解读的候选清单 + 解读记录（**不拆表**） |
| `publish_record` | `publish.entity.PublishRecord` | 每次成功发布到语雀的流水 |
| `ai_publish_job` | `publish.entity.PublishJob` | AI 发布配置 + 最近一次结果（**单例**） |
| `refresh_jobs` | `refresh.entity.RefreshJob` | 增量配置 + 最近一次结果（**单例**） |
| `shelf_books` | `shelf.entity.ShelfBook` | 我的藏书（**快照式**） |
| `reading_list` | `readinglist.entity.ReadingListItem` | 阅读清单（**快照式** + 三态 `status`） |
| `ai_model` | `publish.entity.AiModel` | AI 模型配置（**用户手工维护，程序只读**） |
| `ai_yuque_token` | `publish.entity.AiYuqueToken` | 语雀 token（**同上**） |
| `ai_taxonomy_config` | `publish.entity.AiTaxonomyItem` | AI 用的分类白名单（**同上**） |
| `ai_sensitive_words` | `publish.entity.SensitiveWord` | 敏感词表（**同上**） |

⚠️ 最后 4 张 `ai_*` 表由**用户自己建好并灌数据**，`MongoIndexInitializer` **刻意不碰**
（给它们补唯一索引看着无害，但一旦库里已有重复值，`ensureIndex` 会抛异常把应用拦在启动之外）。

**索引**：共 25 个，**全部由 `config.MongoIndexInitializer` 在启动时显式创建**。
`application.yml` 里 `spring.data.mongodb.auto-index-creation: false`，且实体上**不使用** `@Indexed`。
原因：唯一索引是幂等写入的**正确性依赖**（不是性能优化），必须显式、可审计、可在启动日志里核对。

## API 路由

统一前缀 `/api`，共 14 个 Controller / 61 个端点：

| 前缀 | Controller | 说明 |
|---|---|---|
| `/api` | `PingController` | 连通性检查 |
| `/api/auth` | `AuthController` | 登录 / 登出 / 当前用户（Sa-Token） |
| `/api/books` | `BookController` | 图书库 |
| `/api/taxonomy` | `TaxonomyController` | 分类与榜单字典 |
| `/api/tasks` | `TaskController` | 采集任务 |
| `/api/runs` | `RunController` | 运行记录 |
| `/api/cursors` | `CursorController` | 采集游标 |
| `/api/stats` | `StatsController` | 仪表盘 |
| `/api/requests` | `RequestAuditController` | 请求审计 |
| `/api/refresh` | `RefreshController` | 增量配置（8 目标全量刷新） |
| `/api/publish` | `PublishController` | AI 解读：候选清单 / 配置 / 生成并发布 |
| `/api/publish/records` | `PublishRecordController` | 发布记录 |
| `/api/shelf` | `ShelfController` | 我的藏书（8 列 × 3 行网格 + 下滑加载） |
| `/api/reading-list` | `ReadingListController` | 阅读清单（想读 / 在读 / 已读；与藏书阁互不影响） |

接口文档：`http://localhost:8080/swagger-ui.html`（springdoc，OpenAPI 3）。

## 测试

```bash
# 单元测试（离线，不联网）
mvn test

# 集成测试（会打真实微信读书接口 / 真实 MongoDB）
mvn test -Dtest=CollectEngineIT
mvn test -Dtest=TaskControlIT
mvn test -Dtest=ApiCrudIT
mvn test -Dtest=BookQuerySemanticsIT
mvn test -Dtest=CollectRetryFailureIT
```

> `*IT` 结尾的类**不在** `mvn test` 的默认扫描范围，必须显式 `-Dtest=` 运行。
> 集成测试会真实写入 MongoDB，不要与正在运行的采集任务同时执行。

> 🔴 **本节仅供用户手动执行。** 按**用户硬规则 4 / 5**，agent **不主动创建测试文件、不主动运行测试**；
> 现有测试文件（`S1DataLayerTest` 与各 `*IT`）**保持不动**。

---

# 架构模式

## 代码组织结构

**核心原则：业务模块优先 + 模块内部按职责分层。**

```
com.bookcollector/
├── BookCollectorApplication.java
│
├── {业务模块}/                    ← 第一层永远是业务模块
│   ├── AGENTS.md                  # ★ 该模块的知识图谱（改代码前先读）
│   ├── controller/                # 控制器
│   ├── service/                   # 服务接口
│   │   └── impl/                  # 服务实现类（@Service 加在这里）
│   ├── repository/                # 数据访问层
│   ├── entity/                    # MongoDB 持久化实体（@Document）
│   ├── req/                       # 接收前端请求的对象
│   ├── resp/                      # 返回前端的数据对象
│   ├── dto/                       # 模块内部数据传递对象
│   ├── constant/                  # 模块专属常量
│   └── util/                      # 模块内部可复用的工具类
│
├── common/                        # 跨模块公共组件（ResultBean / BizException / PageResult / enums）
├── config/                        # 基础设施装配（@Configuration + *Properties + 启动期初始化）
├── util/                          # 全局无状态工具（PageQueryUtil）
└── system/                        # 系统级 Controller（PingController）
```

**这是推荐的标准结构，不是强制模板。** 不要求每个业务模块都创建全部子包——没有实际用途的包不要强行创建（例如某模块没有任何模块级常量，就不建 `constant/`）。

**为什么按业务模块优先**：定位一个功能时只需要进一个目录，而不是在 `controller/`、`service/`、`dao/` 三个顶层目录之间来回跳。模块内部的修改天然收敛在一个目录内，降低改动外溢风险。

### 模块级 `AGENTS.md`（模块知识图谱）

每个业务模块根目录下有一个 `AGENTS.md`，**就近生效** —— Codex / Claude Code / Cursor
都支持读取目录级 `AGENTS.md`。它写的是「本模块非显而易见的东西」：
类清单、调用关系图谱、数据集合与索引、对外接口、**不变量与铁律**、依赖与耦合、测试、已知陷阱。

**写规则**：

1. **只写非显而易见的。** 方法名、参数列表、getter/setter 不写 —— 那些读代码就有。
2. **每条铁律带「为什么」。** 只写「不要这样做」的规则，下一个人不知道边界在哪，迟早会绕过。
3. **陷阱写全三段**：现象 → 根因 → 修法。只写「注意 XX」等于没写。
4. ~~**改代码时同步改图谱。**~~ 🔴 **已被用户硬规则 2 推翻** —— 文档同步只在**需求明确要求**时做。
   （原理由保留备查：过期的文档比没有文档更坏 —— 它会让人做出错误判断。）
5. 这些 `.md` 放在 `src/main/java` 下**不会被打包**（`maven-resources-plugin` 只处理
   `src/main/resources`，已实测确认），可以放心就近放置。

## 技术栈

以 `pom.xml` 与 `application.yml` 为唯一依据，**不要自行升级依赖或引入新框架**。

| 类别 | 组件 | 版本 | 说明 |
|---|---|---|---|
| 语言 | Java | **1.8** | `maven.compiler.source/target = 1.8` |
| 框架 | Spring Boot | **2.3.12.RELEASE** | 单体，非 Cloud |
| Web | spring-boot-starter-web | 由 Boot 管理 | Spring MVC |
| 校验 | spring-boot-starter-validation | 由 Boot 管理 | Hibernate Validator（JSR-303） |
| 数据库 | spring-boot-starter-data-mongodb | 驱动 4.0.6（由 Boot 管理） | 服务端 MongoDB **7.0.30** |
| 缓存 | spring-boot-starter-data-redis | Lettuce 5.3.x | 服务端 Redis **3.2.100**；⚠️ **当前代码零引用** |
| HTTP 客户端 | httpclient | 由 Boot 管理 | 供 `RestTemplate` 使用 |
| JSON | fastjson2 | **2.0.60** | `com.alibaba.fastjson2` |
| 接口文档 | springdoc-openapi-ui | **1.6.15** | OpenAPI 3 |
| 工具库 | hutool-all | **5.8.4** | `cn.hutool`；官方聚合包，一个坐标含全部模块 |
| 工具库 | commons-lang3 | **3.12.0** | ⚠️ 在 `properties` 里覆盖了 BOM 默认的 3.10，全项目统一 |
| 代码简化 | lombok | 由 Boot 管理 | 仅用于实体与值对象 |
| 测试 | spring-boot-starter-test | 由 Boot 管理 | JUnit 5 + AssertJ |

**配置约定**

- 所有配置写在 `src/main/resources/application.yml`，业务配置挂在前缀 `bookcollector.*` 下。
- MongoDB 用 `spring.data.mongodb.*`；**Redis 用 `spring.redis.*`**（Spring Boot 2.3 的前缀，不是 `spring.data.redis.*`）。
- 日志的**格式与滚动策略**在 `logback-spring.xml` 里定义，`application.yml` 只配级别。
  `logging.pattern.*` 与 `logging.file.name` 在本项目是**死配置**（自定义了 appender），不要写。

## 分层职责

| 层 | 位置 | 职责 | 硬约束 |
|---|---|---|---|
| **Controller** | `{模块}/controller/` | 接收 HTTP 请求、触发参数校验、调用 Service、包装 `ResultBean` 返回 | **不写业务逻辑**，**不直接操作 MongoDB** |
| **Service** | `{模块}/service/` | 业务服务**接口**，只声明方法签名 | 用 `interface` 修饰 |
| **ServiceImpl** | `{模块}/service/impl/` | 业务流程编排、事务边界、业务规则校验 | 用 `@Service` 注解；实现对应接口 |
| **Repository** | `{模块}/repository/` | 数据访问：复杂查询、聚合、可复用的 Mongo 操作 | 见下节「MongoDB 数据访问规范」 |
| **Entity** | `{模块}/entity/` | MongoDB 持久化映射（`@Document`） | 集合名与字段映射**不得变更** |
| **Req** | `{模块}/req/` | 接收前端请求的对象 | 只做字段声明 + 基础校验注解 |
| **Resp** | `{模块}/resp/` | 返回前端的数据对象 | — |
| **DTO** | `{模块}/dto/` | 业务模块**内部**的数据传递对象 | 不为了形式而创建 |

**依赖方向**：`Controller → Service(接口) → ServiceImpl → Repository → MongoTemplate`。
**禁止反向依赖**：Repository 不得依赖 Service；Entity 不得依赖任何上层。

**Service 必须拆分为接口 + 实现类。** 这是本项目明确的规范：
- `service/` 包放接口，用 `interface` 修饰，只定义方法；
- `service/impl/` 包放实现类，用 `@Service` 注解；
- Controller 只依赖接口，不依赖实现类。

> ✅ 已全量落地（2026-09-23）：7 组 Service 全部是「接口 + `impl/` 实现类」，
> Controller 只依赖接口。新增 Service 时照此执行。

## MongoDB 数据访问规范

**统一使用 `MongoTemplate`。**

**明确禁止**：
- 使用 `MongoRepository`
- 继承 `MongoRepository`
- 引入任何基于 `MongoRepository` 的数据访问实现

**Repository 的使用边界**（按复杂度判断，不为了形式机械创建）：

- 简单 CRUD、简单单条件查询，且无复用需求 → 允许在 ServiceImpl 中直接注入 `MongoTemplate`。
- 出现下列任一情况时，**必须**抽取 Repository：
  1. 查询条件复杂（多条件 `andOperator` 组合、区间、嵌套字段）；
  2. 使用聚合管道、`BulkOperations`、批量 upsert 等较重的操作；
  3. 同一套数据访问逻辑在**多个类**里重复出现。
- **铁律**：不要让同一类复杂、可复用的数据访问逻辑在多个 ServiceImpl 中重复实现。

**写法约定**：

- 动态条件用 `Criteria` + `Criteria.andOperator(...)` 组合。
  **不要**连续 `query.addCriteria(...)` —— 同一字段上叠加条件时后者会覆盖前者。
- 更新用 `Update` + `mongoTemplate.updateFirst()` / `findAndModify()`。
  **禁止**用 `save()` 做全量覆盖（有并发覆盖风险）。
- 局部更新只写调用方明确给到的字段（`Update.set(field, value)` 逐字段下发）。
  整本 `save()` 会导致「前端少传一个字段 → 该字段被写成 null」的隐式清空。
- 批量 `$in` 查询要**分片**（本项目阈值 `IN_QUERY_CHUNK = 1000`），避免 BSON 超过 16MB。
- 集合判空用 `xxx == null || xxx.isEmpty()`（本项目现有风格），不要引入新的工具类。

**集合与索引**：

- 集合名通过 `@Document(collection = "...")` 显式声明，**不得变更**。
- 字段名不做别名映射：**Mongo 字段名 == Java 字段名**（现有代码零 `@Field`）。新增字段保持同样约定。
- 索引**不在实体上声明** `@Indexed`，统一在 `config.MongoIndexInitializer` 里 `ensureIndex` 显式创建。
- 唯一索引是幂等写入的正确性依赖，不是可选优化。

## 分页查询规范

**统一使用全局分页工具类 `com.bookcollector.util.PageQueryUtil`**，不要各自手写分页逻辑，也不要在没有必要的情况下新建分页工具类。

> ✅ 该类**已落地**（2026-09-23），三处分页（`BookRepository` / `TaskRepository` / `ApiRequestQueryRepository`）已收敛。
> 实现细节见 `common/AGENTS.md` 与类自身的注释。

**分页响应结构**：沿用本项目已有的 `com.bookcollector.common.PageResult<T>`，不引入新的响应类型。

```
ResultBean.data = PageResult { list, total, page, size }
```

**分页参数命名**：现有接口用 `page` / `size`。

> ⏸️ 规范目标曾是 `pageNum` / `pageSize`，但改名属**接口契约变更**，需前后端同步，
> 收益不足。**已决定不做**（见文末待整改项 #6）。新增接口也沿用 `page` / `size`，保持一致。

**`PageQueryUtil` 的公开 API**（3 个分页/转换方法 + 2 个归一化工具）：

```java
// 单字段排序分页。sortField 必须显式给出，传空直接抛异常
// —— 本项目没有通用的 createTime 字段，静默回退会退化成自然序且不报错
public static <R> PageResult<R> getPageResult(MongoTemplate mongoTemplate,
        Integer pageNum, Integer pageSize, Criteria criteria, Class<R> clazz,
        Sort.Direction direction, String sortField);

// 显式 Sort 分页（用于「主排序 + _id 兜底」这类多字段/多方向排序）
public static <R> PageResult<R> getPageResult(MongoTemplate mongoTemplate,
        Integer pageNum, Integer pageSize, Criteria criteria, Class<R> clazz, Sort sort);

// 分页结果转换（Entity → Resp）。元素用 Hutool BeanUtil 拷，信封字段直接 setter
public static <S, T> PageResult<T> convertPageResult(PageResult<S> source, Class<T> targetClass);

// 参数归一化（全项目唯一口径）：page<1→1、size<1→20、size>200→200
public static int normalizePage(Integer pageNum);
public static int normalizeSize(Integer pageSize);
```

> ⚠️ 该类有**三条刻意保留的行为**（`count == 0` 短路 / 不提供默认排序字段 /
> 必须支持两级不同方向的排序），以及一段**不能调换的执行顺序**。改它之前先读
> `common/AGENTS.md` **铁律 10** 与 `PageQueryUtil` 自身的 javadoc。

**分页编码风格**（Controller 保持简洁，业务编排在 ServiceImpl / Repository）：

```java
// Controller —— 只接收请求、调用 Service、包装响应
@GetMapping
public ResultBean<PageResult<Book>> page(BookQuery query) {
    return ResultBean.ok(service.page(query));
}
```

```java
// Repository —— 只负责「条件怎么拼」和「按什么排」，分页样板交给 PageQueryUtil
public PageResult<Book> pageQuery(BookQuery q) {
    BookQuery query = q == null ? new BookQuery() : q;

    // 主排序字段走白名单校验（见 BookQuery#resolveSortPath），加 _id 兜底保证翻页稳定
    Sort sort = Sort.by(query.isAsc() ? Sort.Direction.ASC : Sort.Direction.DESC,
                        query.resolveSortPath())
            .and(Sort.by(Sort.Direction.ASC, "_id"));

    return PageQueryUtil.getPageResult(mongoTemplate, query.getSafePage(), query.getSafeSize(),
            buildCriteria(query), Book.class, sort);
}

// 多条件用 andOperator 组合，避免同字段叠加时被覆盖；空条件返回 new Criteria()（等价「全部」）
private Criteria buildCriteria(BookQuery q) { ... }
```

> ⚠️ **排序字段必须是白名单校验过的合法路径**，绝不能把用户传入的字符串直接拼进 Mongo 路径（注入面）。
> 参考 `BookQuery#resolveSortPath()`。字段用**字符串字面量** —— 本项目实体没有 `Fields` 常量内部类。

**提炼出的规范**：

1. Controller 保持简洁，只负责请求接收和调用 Service。
2. Service / Repository 负责业务流程编排与条件构建。
3. 使用 `MongoTemplate` + `Criteria` 构建动态查询。
4. 分页样板统一走 `PageQueryUtil`，不重复实现。
5. 复杂查询条件必须有中文注释说明「为什么这样查」。
6. 查询条件、排序、分页、结果转换四段逻辑保持清晰分隔。
7. 模糊查询若使用正则，**必须转义特殊字符**（本项目第一期约定不做模糊搜索）。
8. 不要为了形式引入过多无意义的抽象层。

**依赖**：`PageQueryUtil` 用到 `cn.hutool.core.bean.BeanUtil`（`cn.hutool:hutool-all:5.8.4`），
已在 `pom.xml` 中。**不需要**再新增依赖。

> `convertPageResult` 目前**暂无调用点**（现有接口 Entity 直出，本项目允许）。
> 保留它是因为规范要求「后续新增分页查询优先复用」。
> `org.apache.commons:commons-lang3:3.12.0` 已引入但当前无引用，保留备用。

## 请求与响应规范

**统一响应体：`com.bookcollector.common.ResultBean<T>`**

```json
{ "code": 200, "message": null, "traceId": "…", "data": { } }
```

**核心约定：HTTP 状态码恒为 `200`，业务结果看 body 里的 `code`。**
前端 axios 拦截器只判断一处 `code`，不需要同时处理 HTTP 状态码。

**错误码常量**（定义在 `ResultBean`，`BizException` 的 `code` 直接对齐）：

| 常量 | 值 | 含义 |
|---|---|---|
| `code_ok` | 200 | 正常 |
| `code_warn` | 400 | 参数错误 |
| `code_notfound` | 404 | 未找到 |
| `code_duplicateKey` | 405 | 主键重复 |
| `code_err` | 500 | 错误 |
| `code_session_invalid` | 4100 | 身份已失效，请重新登录 |

**异常处理**：

- 业务错误统一 `throw new BizException(...)`，或用快捷构造：`BizException.warn / notFound / duplicate / sessionInvalid`。
- 全局处理集中在 `common.GlobalExceptionHandler`（`@RestControllerAdvice`），覆盖：
  `BizException`、`DuplicateKeyException`、`MethodArgumentNotValidException`、`BindException`、
  `MissingServletRequestParameterException`、`HttpMessageNotReadableException`，以及兜底 `Exception`。
- **不要**在 Controller 里写 `try/catch` 兜业务异常，交给全局处理器。
- 参数校验失败时，message 必须**可读**（`GlobalExceptionHandler.describeFieldErrors` 已按字段名排序 + 限 3 条 + 类型转换失败转人话）。
- 拦截器里返回失败**不走** `GlobalExceptionHandler`（异常处理器不介入），必须自己写响应体 —— 参考 `auth.interceptor.AuthInterceptor.writeSessionInvalid`。

**`Req` / `Resp` / `DTO` 的职责与边界**：

- **Req**：接收前端请求。只做字段声明 + 基础校验注解（`@NotBlank`、`@NotNull`、`@Min` 等），**不写自定义校验方法**。
- **Resp**：返回前端的数据对象。用于收敛字段、隔离持久化结构、聚合多个来源。
- **DTO**：**模块内部**的数据传递对象。
- **不要求每个接口都创建 DTO**，也不要把 `Req → DTO → Entity → DTO → Resp` 设计成固定流水线。
  只有在确实需要承载内部业务数据、聚合多个对象、或隔离不同层数据结构时才创建。
- **避免创建字段完全相同、没有实际价值的重复对象。**

**Entity 可以直接作为响应对象。**

这是本项目**明确的约定**：`ResultBean<Book>`、`ResultBean<PageResult<Book>>` 这样的直接返回是允许的、也是当前的主流写法。
引入 `Resp` 的目的是「收敛字段 / 隔离结构」，**不是**「Entity 一律不得出现在响应里」。
判断标准是「这个接口是否有需要收敛或聚合的内容」，而不是形式上的分层完整性。

## 公共组件规范

本项目有**两个**公共层，职责不同，不要混：

| 包 | 放什么 | 判定标准 |
|---|---|---|
| `com.bookcollector.common` | **跨模块公共组件**：`ResultBean`、`BizException`、`GlobalExceptionHandler`、`PageResult`、`TraceIdFilter`、`enums/{TaskStatus,TargetType}` | **有状态**或**承载约定**的东西（返回体结构、异常语义、枚举） |
| `com.bookcollector.util` | **全局无状态工具**：`PageQueryUtil` | 纯函数、无状态、`final` + 私有构造器抛 `AssertionError` |

> ✅ **已定案**（2026-09-23，方案 D1）：`common` **保留**，不再迁往 `util`。
> 原先「把 `common` 并进 `util`」的想法已作废 —— `ResultBean` / `BizException` / `PageResult`
> 被全项目引用，改名只会产生大量无收益的改动；而且「承载约定的组件」与「无状态工具」
> 本就是两类东西，混在一个包里语义会变糊。

- **不要**将业务逻辑、业务专属常量、业务专属工具放进 `common` 或全局 `util`。
- **`{业务模块}/util`**：只放当前模块内部可复用的工具类，**禁止**将具体业务逻辑放进去。
- 判定标准是**「是否被 2 个以上业务模块使用」** —— 只有一个模块用的东西留在模块内。

## 编码规范

**命名**

- 类名：大驼峰（`BookRepository`）；包名：全小写（`collector`）。
- 方法名、字段名：小驼峰（`pageQuery`、`bookId`）。
- 常量：`static final`。新增常量用全大写下划线（如 `MAX_SIZE`、`IN_QUERY_CHUNK`）；
  `ResultBean.code_*` 为既有风格，**保持不动**。
- 请求对象：`XxxRequest`（如 `BookUpdateRequest`）；查询条件对象：`XxxQuery`（如 `BookQuery`）。

**依赖注入**

- **统一使用构造器注入**，字段声明为 `private final`。
- **禁止** `@Autowired` 字段注入（现有代码零使用）。

```java
private final BookRepository repository;

public BookService(BookRepository repository) {
    this.repository = repository;
}
```

**Lombok**

- 仅用于**实体类**与**不可变值对象**：`@Data` + `@Builder` + `@NoArgsConstructor` + `@AllArgsConstructor`。
  （现有：8 个 `entity` + `collector` 的 4 个值对象）
- 通用基础类（`ResultBean`、`PageResult`）与查询条件对象（`BookQuery`）**手写 getter/setter**，因为它们带有自定义行为（如 `getMessage()` 的兜底逻辑、`@JsonIgnore`）。

**参数校验**

- Controller 方法参数用 `@Validated`（或 `@Valid`）触发校验；请求体 DTO 字段用 JSR-303 注解。
- 跨字段校验、业务规则校验放在 **ServiceImpl 方法开头**，违规 `throw BizException`。

**日志**

- 用 SLF4J：`private static final Logger log = LoggerFactory.getLogger(Xxx.class);`
- 用占位符，不要字符串拼接：`log.info("图书已编辑：{}，修改字段 {}", bookId, sets.keySet());`
- 关键业务动作（写入、删除、状态流转、失败原因）必须有日志。
- `TraceIdFilter` 会给每个请求分配 traceId 放进 MDC 的 `"threadId"`，`ResultBean` 自动带上。
  ⚠️ `@Async` 线程**不继承 MDC**，需要在任务线程里手动 put/remove。

**时间类型**

- 业务时间字段用 `java.util.Date`（现有实体统一如此）。
- `LocalDateTime` 仅用于展示格式化（如 `PingController` 返回服务器时间）与审计时间提供者。
- ⚠️ **`publishTime` 是字符串**（定长零填充 `"yyyy-MM-dd HH:mm:ss"`），字典序等于时间序，区间筛选用字符串比较，不要解析成日期。

**注释**

- **代码注释使用中文。**
- 逻辑分段或复杂逻辑必须有注释说明**为什么**（而不是复述代码在做什么）。
- 修改原有代码时**尽量保留原注释**，除非业务逻辑确实与原来不一致。
- 类级 Javadoc 说明「这个类是干什么的、边界在哪」。

**接口文档**

- 所有对外接口必须使用 springdoc 标准注解：`@Tag`（Controller 级）、`@Operation`（方法级）、`@Parameter`（参数级）、`@Schema`（模型字段级）。
- `@Tag(name = "0X. 模块名")` —— 用两位数字前缀控制 Swagger UI 的排序。

**Controller / REST 风格**

- 查询/获取：`@GetMapping`；创建/更新/删除：`@PostMapping` + `@RequestBody`。
- 现有代码在个别资源型接口上使用了 `@PutMapping` / `@DeleteMapping`（如 `BookController`），属既有实现，保持不动。
- 路由前缀统一 `/api/{资源复数}`。

**回复语言**

- 所有回复默认使用**简体中文**。

## AI 开发约束

后续 AI 新增功能或修改代码时，**必须**遵守：

### 🔴 用户硬规则（2026-09-23 定，优先级最高）

> **本节由用户直接下发，优先级高于本文件其余全部条款。**
> 与本文件其他条款冲突时**一律以本节为准**（冲突处已在对应位置标注「已被用户硬规则 N 推翻」）。

1. **git 只读。**
   - **允许**：`git status` / `log` / `diff` / `show` / `branch` 等**只读查询**。
   - **禁止**：`add` / `commit` / `push` / `merge` / `rebase` / `reset` / `revert` /
     `cherry-pick` / `checkout` / `switch` / `stash` / `tag` / `rm` 等**一切写操作** ——
     **由用户手动执行**。
   - 为什么：提交粒度与时机的控制权归用户（见「Git 仓库与发布」一节）。

2. **只改需求明确提及的方法 / 文件。** 需求未提及的一律不改、不重构、不「顺手优化」。
   - 🔴 **这条推翻了本文件原先「改完代码要同步更新模块 `AGENTS.md`」的强制要求** ——
     文档同步只在**需求明确要求**时做。
     （受影响处：本节第 0 条、上文「模块级 `AGENTS.md` 写规则」第 4 条。）

3. **禁止大范围 grep + Edit 批量替换。** 重命名类改动**逐个文件手动改**；
   确需批量（10+ 文件）时**先说明范围并获用户同意**。

4. **不写单元测试。** 跳过测试相关任务、不创建测试文件；**无需在汇报中提示**，除非用户主动要求。
   - 约束的是 agent 的**自主行为**；用户主动要求时照做。
   - 现有测试文件（`S1DataLayerTest` 与各 `*IT`）**保持不动**。

5. **不做运行时验证。** 不启动服务、不调用接口做真实读写验证，除非用户主动要求。
   - 🔴 **这条推翻了原先「改完前端必须跑 `s5/s6-acceptance.mjs`」的要求。**
   - `tools/*.mjs` 验收脚本**保留备查**，由用户按需执行。

6. **模型能力不足时先说明，不擅自绕过。** 遇到当前模型能力不足（如不支持读图、上下文不够），
   先说明原因与建议方案，**等用户明确同意后再执行**；**不得擅自换模型或换引擎绕过**。

7. **歧义向「先问」倒。** 某条指令能否构成**写盘授权**存在疑义时，一律按**「无授权」**处理，
   先问再做；**不得把模糊之处向「可以先做」解释**。

### 通用约束

0. **🔴 动手前先读该模块的 `AGENTS.md`。** 例如改 `task/` 下任何代码前先读
   `src/main/java/com/bookcollector/task/AGENTS.md`。模块级的**不变量与铁律**和**已知陷阱**
   只写在那里，不看就会踩已经踩过的坑。
   - ⚠️ 原句末的「**改完代码要同步更新该文件**（过期的文档比没有文档更坏）」
     **已被用户硬规则 2 推翻** —— 文档同步只在需求明确要求时做。
1. **优先复用现有实现**。新增分页查询前先确认 `PageQueryUtil` 与 `PageResult`；新增公共能力前先检索 `com.bookcollector.util` 与 `common`。
2. **避免无意义的抽象**。不为「看起来更规范」而创建空接口、单实现接口、字段完全相同的 DTO。抽象必须有明确收益。
3. **避免重复造轮子**。同一套逻辑不得在多个类里各写一遍 —— 抽 Repository 或全局 util。
4. **不改动既有契约**。集合名、字段映射、接口路径、请求参数、响应结构一律保持兼容；确需变更时必须先说明影响面并获得确认。
5. **不擅自升级依赖或引入新框架**。需要新依赖时先提出并说明理由。
6. **需求与规范冲突时，先指出冲突并等待确认**，不要自行决定是否修改规范。
7. **改代码时保留原有注释**，除非逻辑确实变化。
8. **改动范围收敛**：只改需求明确提及的文件；不做「顺手优化」式的重构。（= **用户硬规则 2**）
9. **完成后说明**：改了哪些文件、为什么改、有无未完成项。

---

# 落地现状与待整改项

> 本节记录「现有代码」与「本规范目标」之间的差异。
> **最后一次包结构整理：2026-09-23（第三步已执行完毕，见 `backend/3_包结构调整方案.md`）。**

| # | 维度 | 现状 | 状态 |
|---|---|---|---|
| 1 | **Service 分层** | `service/` 接口 + `service/impl/` 实现类，共 7 组 | ✅ 已完成 |
| 2 | **模块内分层** | Controller / Service / Repository / entity / req 已归入各自子包 | ✅ 已完成 |
| 3 | **请求对象位置** | 全部在 `req/` 下（8 个类） | ✅ 已完成 |
| 4 | **公共包位置** | 顶层 `common/` **保留**（`ResultBean` 等跨模块组件）；`util/` 只放无状态工具类 | ✅ 已定案（原「迁到 util」方案作废，理由见方案 D1） |
| 5 | **分页工具** | `util/PageQueryUtil` 已建，三处分页（book / task / audit）已收敛 | ✅ 已完成 |
| 6 | **分页参数命名** | 仍为 `page` / `size` | ⏸️ **刻意不做** —— 改名是接口契约变更，需前后端同步，收益不足 |
| 7 | **`@Indexed`** | 零使用（统一在 `MongoIndexInitializer` 建 18 个） | ✅ 已符合规范 |
| 8 | **`MongoRepository`** | 零使用，全部手写 `@Repository` + `MongoTemplate` | ✅ 已符合规范 |
| 9 | **统一响应 / 异常** | `ResultBean` + `BizException` + `GlobalExceptionHandler` | ✅ 已符合规范 |
| 10 | **SpringDoc 注解** | `@Tag` / `@Operation` / `@Parameter` / `@Schema` 已全量使用 | ✅ 已符合规范 |
| 11 | **依赖注入** | 全部构造器注入，`@Autowired` 零使用 | ✅ 已符合规范 |
| 12 | **Entity 直出** | 所有接口直接返回 Entity | ✅ 允许（本项目约定） |
| 13 | **模块知识图谱** | 9 个模块各有 `AGENTS.md` | ✅ 已完成 |
| 14 | **`S2PageStabilityIT` 的断言** | 已改为断言**分页不变量**（每页 20 条 / `searchIdx` 严格递增 / 漂移容忍度 5） | ✅ 已修（见 `collector/AGENTS.md` 陷阱 9.5） |

## 已知的测试脆弱点

- **`S2PageStabilityIT`** 是唯一一条依赖**实时榜单数据**的集成测试。
  2026-09-23 曾红：断言「走 5 页恰好 100 本」，实测拿到 99。
  根因是**分页机制本身的固有性质**（不是缺陷）：分页是 `maxIndex`（searchIdx 偏移）式的，
  而榜单是**可变列表** —— 两次请求之间若有书进出，位置整体平移，
  相邻页就会**重叠**（同一本出现两次 → 去重后少 1）或**留空洞**。
  **已改为断言与内容无关的分页不变量**（每页 20 条原始节点 / 20 本解析成功、
  `searchIdx` 全程严格递增、从 1 开始、覆盖到 `100 ± 5`），方法名
  `twoConsecutiveWalksAreIdentical` → `twoConsecutiveWalksAreStable`。
  详见 `collector/AGENTS.md` 陷阱 9.5。
  > **通用教训**：对**实时数据源**断言「精确条数」几乎一定会红。要断言的是**机制不变量**
  > （每页条数、游标单调、起始位置），把数据漂移留成显式容忍度或纯观测输出。

## 已知的跨模块依赖环（不解决，仅记录）

这三组环是**设计层面的耦合，不是包结构问题**。换包不会改变它们，
也不该顺手重构（违反「改动范围收敛」）。供后续单独评估。

| 环 | 路径 | 成因 |
|---|---|---|
| `audit ↔ collector` | `audit/ApiRequestRepository` ← `collector.dto.{WereadPage,WereadRawResponse}`；`collector/CollectLoop` ← `audit.repository.ApiRequestRepository` | 审计要记录原始响应，采集要写审计 |
| `collector ↔ task` | `collector/ProgressReporter` ← `task.entity.{TaskLog,TaskRun}`；`task/{TaskRunner,TaskHandle,TaskService}` ← `collector.*` | 进度上报写任务集合，任务执行调采集引擎 |
| `collector ↔ config` | `collector/{CollectLoop,WereadClient,WereadHeaderInterceptor}` ← `config.WereadProperties`；`config/RestTemplateConfig` ← `collector.WereadHeaderInterceptor` | 配置绑定类与使用方互相引用 |
