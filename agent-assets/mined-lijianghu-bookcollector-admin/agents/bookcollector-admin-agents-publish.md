# publish 模块知识

> 包路径：`com.bookcollector.publish` · 最后更新：2026-10-09
> **这是「内容产出侧」，和前面所有「把数据采回来」的模块性质不同。**
> 改之前先读第 6 节铁律 1、2、10。

## 1. 这个模块是干什么的

从候选清单里挑**一本**高质量图书 → 让 AI 写一篇解读 → 存成本地 Markdown → 发到语雀。

```
book_interpretations(PENDING)  ──挑一本──►  AiClient(DeepSeek/OpenAI 兼容)
        ▲                                        │
        │                                        ▼
        └──── 写终态 ◄── 语雀 ◄── 本地 docs/*.md ◄┘
```

支持 **cron 定时**和**手动「立即生成并发布」**两条入口，**一次只做一本**
（用户 2026-10-09 明确：「每次一本书」—— 所以这里没有「批次」概念，
想连续做多本就让 cron 密一点，或多点几次）。

### 🔴 它与「采集」侧的关系：**没有关系**

本模块**不依赖** `collector` / `task` / `refresh`，也不碰任何采集游标。
唯一的交集是：候选清单里的书是**从 `books` 集合快照过来的**（初始化那一步读一次）。
所以定时刷新与定时发布同时跑**不会互相抢锁**，只会抢网络 —— 默认 cron 已刻意错开。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `PublishProperties` | 配置 | `bookcollector.publish.*`（超时 / token 上限 / 输出目录 / 语雀坐标 / 评级白名单）。**不含任何密钥** |
| `PublishScheduler` | 定时触发器 | `SchedulingConfigurer` + 动态 `Trigger`（每次触发前重读 cron） |
| `client/AiClient` | HTTP 客户端 | 走 **OpenAI 兼容协议**（`POST {baseUrl}/chat/completions`）。**不是 DeepSeek 专用** —— 2026-10-09 从 `DeepSeekClient` 改名 |
| `client/YuqueClient` | HTTP 客户端 | 语雀 OpenAPI：建文档 + 挂目录节点 |
| `controller/PublishController` | Controller | 7 个端点，极薄转发 |
| `dto/AiCompletion` | DTO | 一次生成的返回：正文 + token 用量 + model |
| `dto/YuqueDoc` | DTO | 语雀文档：id / url / title |
| `entity/Interpretation` | Entity | **候选清单 + 解读记录**（`book_interpretations`）。本模块最核心的实体 |
| `entity/PublishStatus` | 枚举 | `PENDING` / `GENERATING` / `PUBLISHED` / `FAILED`。**单条记录**的状态 |
| `entity/PublishJob` | Entity | 单例调度配置（`ai_publish_job`，`_id` 固定 `"default"`）+ 最近一次执行结果 |
| `entity/AiModel` | Entity | 用户手工维护（`ai_model`），**程序只读**。含 `apiKey` |
| `entity/AiYuqueToken` | Entity | 用户手工维护（`ai_yuque_token`），**程序只读**。含 `token` |
| `entity/AiTaxonomyItem` | Entity | 用户手工维护（`ai_taxonomy_config`），**程序只读**。分类白名单 |
| `entity/SensitiveWord` | Entity | 用户手工维护（`ai_sensitive_words`），**程序只读** |
| `repository/InterpretationRepository` | Repository | 候选初始化（原始 BSON 快照 upsert）+ 挑书 + 状态流转 + 分页 |
| `repository/PublishJobRepository` | Repository | 单例文档 `loadOrCreate` / `saveConfig` / `markRunning` / `markFinished` |
| `repository/AiConfigRepository` | Repository | 读那三张配置表。**🔴 这个类里永远不许出现 key / token 的内容** |
| `repository/SensitiveWordRepository` | Repository | 按**词长降序**取启用中的词表 |
| `prompt/InterpretationPrompt` | 模板 | 提示词（system + user）。**只负责「告诉模型怎么写」，不做校验**（见铁律 2） |
| `service/PublishService` | Service 接口 | `getJob` / `currentCron` / `pageInterpretations` / `updateConfig` / `initializeCandidates` / `clearCandidates` / `trigger` / `runScheduled` / `resetToPending` |
| `service/impl/PublishServiceImpl` | Service 实现 | **本模块的核心**：编排 + 两个独立线程池 + 两个 `AtomicBoolean` 互斥 + 内存进度快照 |
| `req/PublishConfigRequest` | req | 改配置请求体（两字段都可选，`null` = 不改） |
| `vo/PublishJobVO` | VO | 页面全量数据（配置 + 脱敏的模型信息 + 两条任务的进度 + 各状态计数） |
| `vo/InterpretationVO` | VO | 列表行。**刻意不声明** `content` / `rawContent` —— 大字段不进列表接口 |

## 3. 调用关系（图谱）

```
PublishController ──► PublishService(Impl) ──┬──► InterpretationRepository ──► book_interpretations
                                             ├──► PublishJobRepository ─────► ai_publish_job
                                             ├──► AiConfigRepository ───────► ai_model / ai_yuque_token / ai_taxonomy_config（只读）
                                             ├──► SensitiveWordRepository ──► ai_sensitive_words（只读）
                                             ├──► client.AiClient ──────────► POST {baseUrl}/chat/completions
                                             ├──► client.YuqueClient ───────► 语雀 OpenAPI（建文档 + 挂目录）
                                             └──► 本地文件系统 ─────────────► {outputDir}/{yyyy-MM-dd}_《书名》.md

PublishScheduler ──► PublishService.currentCron() / runScheduled()
        （Spring 默认单线程调度器，与 RefreshScheduler 共用；Trigger 在注册时同步调用一次）
```

**两个专用线程池**（`initExecutor` / `genExecutor`，各自单线程）：
不共用是有意的 —— 共用一个池的话，用户点「生成」会被排在几十秒的初始化后面，
页面显示「已提交」却迟迟不动。见铁律 3。

## 4. 数据集合与索引

| 集合 | 谁写 | 索引 |
|---|---|---|
| `book_interpretations` | 本模块读写 | `_id_` · **`uk_bookId`（唯一）** · `idx_status_rating` |
| `ai_publish_job` | 本模块读写 | 无（靠固定 `_id="default"` 强制单例） |
| `ai_model` / `ai_yuque_token` / `ai_taxonomy_config` / `ai_sensitive_words` | **用户手工维护，程序只读** | 无 |

**`uk_bookId` 是正确性依赖，不是性能优化**：初始化候选走的是「按 `bookId` upsert」，
没有这个唯一索引，重复初始化或并发初始化会插出两条同一本书的记录。

**`idx_status_rating`** = `status ASC` + `newRatingCount DESC` + `_id ASC`，
一条索引同时服务两个查询：挑书（`status=PENDING` 按评价人数降序）
和按状态计数/筛选（最左前缀就是 `status`，所以没有单独的 `idx_status`）。

**挑书是「两段式 + 池内随机」**（`InterpretationRepository.pickOnePending()`，2026-10-09 用户指定）：
按上面的排序取前 **100** 条、**只投影 `_id`**（投影字段全在 `idx_status_rating` 里，
靠索引出结果、**不必回表**）→ `Collections.shuffle()` 打乱 → 取一条 → 按 `_id` 点查拿整条。
→ 排序只决定**谁进池子**，**不决定谁先被解读**：否则最高分那本一旦卡住
（反复失败 / 被重置回 `PENDING`），每次都会先撞上它、挡住后面全部。
⚠️ 随机范围是**池内**，不是全库（要全库均匀随机得用聚合 `$sample`）。

**🔴 `MongoIndexInitializer` 刻意只碰 `book_interpretations` 这一张。**
给那 4 张用户手工维护的表补唯一索引（比如 `ai_sensitive_words.word`）看着无害，
实际上**一旦库里已有重复值，`ensureIndex` 会抛异常把应用拦在启动之外**；
而那几张都是几十条以内的小集合，本来也不需要索引。
（`ai_publish_job` 也没有建索引，它靠首次写入 `loadOrCreate()` 的 `save` 存在。）

## 5. 对外接口

| 方法 | 路由 | 说明 |
|---|---|---|
| GET | `/api/publish/job` | 页面全量数据：cron / enabled / 下次触发时间 / 分类白名单 / 模型与语雀配置（**脱敏**）/ 两条任务的进度 / 各状态条数 |
| PUT | `/api/publish/job` | 改 cron / enabled（都可选）。cron 非法 → `code=400`。**改完立即生效，不用重启** |
| POST | `/api/publish/candidates/init` | 初始化候选。**提交即返回**，进度看 GET job |
| POST | `/api/publish/candidates/clear` | 只删「待解读」，不碰已发布 / 失败 / 生成中 |
| GET | `/api/publish/interpretations` | 清单分页。`status` 留空 = 全部。**返回不含正文** |
| POST | `/api/publish/interpretations/{bookId}/reset` | 重置为「待解读」 |
| POST | `/api/publish/trigger` | 生成并发布一本。**提交即返回**；已有任务在跑 → `code=400` |

鉴权由 `config.WebMvcConfig` 统一拦截 `/api/**` 覆盖，本模块不用声明。
Swagger 标签：`@Tag(name = "10. AI 书籍解读")`。

前端页面：`frontend/src/views/publish/config/index.vue`（路由 `/publish/config`，菜单「发布配置」，
**2 秒轮询** `GET /job`）；发布记录页 `frontend/src/views/publish/record/index.vue`
（路由 `/publish/record`，菜单「发布记录」）；接口封装 `frontend/src/api/publish.ts`
（原 `api/ai.ts`）。

## 6. 不变量与铁律 ← 改这个模块前必读

1. **`book_interpretations` 是「候选清单 + 解读记录」的唯一载体，不拆表。**
   （用户 2026-10-09 拍板，此前评估过「另建一张已解读表 + 列表关联」，结论是**不划算**：
   分页 / 状态筛选 / 4 个计数 + total / 挑书会**全部变成跨集合**，
   `$unionWith` 之后排序走不了索引，每页都要重算。）
   ⚠️ 代价：`status = PUBLISHED` **既表示「本系统发布的」也表示「外部已解读的」**，
   两者无法区分（列表里「语雀」「完成时间」列为空的就是外部来的）。
   要区分得加 `source` 字段，**用户明确不采纳**。

2. **🔴 模型产出不做任何校验**（用户 2026-10-09 拍板）：
   **「AI 输出什么，就把什么输出到语雀即可。」**
   历史上这里有过一个 `validate()`，先用 `firstLine.contains(author)` 卡作者名 ——
   那是**拿出版元数据当人名做字面比对**（`author` 形如 `[法]安托万·德·圣埃克苏佩里著`），
   全库 4533 条里有 **1040 条（≈23%）** 带 `[` / `著编译绘` / `/`，会随机把生成卡死
   （《小王子》是第一条受害者）；后来连「有 H1 + 8 个 H2 齐全」也一并去掉了。
   **不要把它加回来。** `InterpretationPrompt` 只负责写提示词。

3. **一次执行只做一本，两类操作都是「提交即返回」。**
   `trigger()` / `initializeCandidates()` 只把任务丢进线程池就返回，
   前端靠轮询 `getJob()` 跟进。生成一本要 30~120 秒，同步等会让页面卡在请求里、
   还容易被浏览器/网关超时掐断（用户 2026-10-09 明确要求「异步，并可以看到进度」）。
   **两个专用线程池不共用**：共用一个池时，点「生成」会排在几十秒的初始化后面。

4. **互斥的唯一权威是内存里的 `AtomicBoolean`，不是 DB。**
   `initRunning` / `genRunning`。DB 里的 `GENERATING` 只是**快照**，进程被杀就是假的。
   ⚠️ **启动时不做自动清理**（用户明确要求）→ 残留的 `GENERATING` 靠页面上的
   「重置为待解读」手工捞回。

5. **`Trigger.nextExecutionTime()` 绝对不能返回 `null`。**
   同 `refresh/AGENTS.md` 铁律 5：`ReschedulingRunnable` 拿到 null 就不再重排，
   这个定时任务**永久死掉**，而页面上看不出任何异常。
   → **未启用也要照常算出下一次**；算不出（如「2 月 30 日」）退回
   `PublishJob.DEFAULT_CRON`，「要不要真跑」交给 `runScheduled()` 运行时判断。

6. **两个 `SchedulingConfigurer` 共用 Spring 默认的「单线程」调度器。**
   所以 `runScheduled()` 必须「丢线程池后**立刻**返回」，不能就地跑一本
   —— 否则会把它之后 `RefreshScheduler` 的 `nextExecutionTime()` 一起推迟，
   表现为「定时刷新莫名其妙晚了几分钟触发」。

7. **`Interpretation` 的写入走 `Document` 原始 BSON 快照，不走实体序列化。**
   初始化是「快照 `books` 的**所有**字段，除了 `_class`」—— 用实体序列化的话，
   实体没声明的字段会丢，`books` 将来加字段也不会自动跟随。
   所以：`stream(..., Document.class, "books")` → `remove("_class")` → 加状态字段
   → `$setOnInsert` 批量 upsert。
   ⚠️ 推论：`@CreatedDate` / `@LastModifiedDate` 在这张表上**不生效**
   （那两个注解只在 `mongoTemplate.save(entity)` 时生效）。

8. **`$setOnInsert` 里不写 `_id`。**
   按 MongoDB 官方文档的标准写法：`_id` 放进**查询等值条件**
   （`{bookId: X, _id: Y}` + `$setOnInsert: {...}`），插入时由查询条件带进去。
   两种写法的结果文档完全一样，但这个是官方有示例背书的。
   `$setOnInsert` 同时带来「已有 bookId 一律跳过」的语义 —— 所以初始化**可以反复点**。

9. **`ai_model` 用 `enable`（无 d），`ai_taxonomy_config` 用 `enabled`（有 d）。**
   两张表不一样，抄错了会静默读不到配置。`ai_yuque_token` **两个都没有**（它按 `sort` 取第一条）。

10. **🔴 敏感信息零外泄（用户 2026-10-09 语气最重的一条）。**
    `ai_model.apiKey` / `ai_yuque_token.token` **绝不许**进日志、注释、接口返回。
    必须打印时只打**长度**或前缀。实体上加了 `@ToString.Exclude`
    —— `@Data` 生成的 `toString()` 会把所有字段带出来。
    所有对外的错误信息都过一遍 `AiClient.scrub(text, apiKey)` 兜底。

11. **敏感词必须按词长降序替换**（`SensitiveWordRepository.listEnabledByLengthDesc()`）。
    先替短词会造出半截词：把「极权」替成「绝对权力」之后，原文里的「极权主义」
    就变成了「绝对权力主义」—— 原本想整体替换的「极权主义」再也匹配不到。
    Mongo 不支持按值长度排序，所以是拉回内存排。

12. **本地文件名 = `日期_《书名》.md`，同名**覆盖**。**
    书名里的 Windows 非法字符（`\ / : * ? " < > |`）换成下划线
    —— 微信读书的书名里冒号、斜杠并不罕见，不处理会直接抛 `InvalidPathException`。
    同名覆盖是有意的：同一天对同一本书重新生成，本来就该是「重来一遍」。

## 7. 依赖与耦合

- **依赖**：`common`（`BizException` / `ResultBean` / `PageResult`）、
  `config`（`MongoIndexInitializer` 建 `book_interpretations` 的索引）、
  `util`（`PageQueryUtil`）。HTTP 客户端用 **Apache HttpClient 4.5.x**（`httpclient`，Boot 管理）。
- **不依赖**：`collector` / `task` / `refresh` / `cursor` / `stats` —— 与采集侧完全解耦。
- **被依赖**：无（没有任何模块依赖本模块）。
- **外部依赖**：AI 服务（OpenAI 兼容协议）、语雀 OpenAPI、本地文件系统。
- **改 `pom.xml` 时注意**：`spring-boot:run` 的 `jvmArguments` 里注入了
  `-DPUBLISH_DIR=${project.basedir}/../docs`，`application.yml` 用
  `${PUBLISH_DIR:../docs}` 兜底。删掉它 → 落盘会落到 `backend/docs/`
  （因为 fork 出的 JVM 工作目录是 `backend/`），**不会报错**。

## 8. 测试与验收

本模块**没有**单元测试（项目约定：不写单测）。手工验收：

1. 重启后端 → 「发布配置」页应显示 `cron=0 0 4 * * ?`、`enabled=false`、
   分类白名单、模型配置（**只显示 name / model / baseUrl，不显示 apiKey**）
2. 点「初始化候选」→ 立刻返回，出现进度并开始轮询；跑完清单条数应等于
   「分类白名单 ∩ 5 档评级 ∩ 评价人数 > 500」的书数
3. **再点一次**「初始化候选」→ 新增应为 **0**（`$setOnInsert` + `uk_bookId` 保证幂等）
4. 点「立即生成并发布」→ 立刻返回；30~120 秒后状态变「已发布」，
   `docs/` 下出现 `日期_《书名》.md`，语雀「书籍解读」目录出现同名文档
5. 验收关键点：**清单里那本书的「语雀」列有链接、「完成时间」有值**
   （外部标记进来的那些这两列为空 —— 见铁律 1）
6. 反例验收：点「立即生成并发布」后**再点一次** → 应返回 `code=400`
7. 反例验收：把 `ai_model` 的 `enable` 改成 `false` → 应报
   「没有可用的 AI 模型，请先在 ai_model 表里配置一行 enable=true 的记录」

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 「生成的内容不符合模板要求：一级标题里没有包含作者名「[法]…著」」

- **现象**：挑到某本书后生成失败，报上面这句，重试换个书可能又好了。
- **根因**：`validate()` 拿 `books.author` 做字面 `contains`，而那个字段是**出版元数据**
  （带 `[国籍]` 前缀和 `著/编/译` 后缀），模型自然不会逐字复现。见铁律 2。
- **修法**：✅ 2026-10-09 已彻底移除校验。**不要加回来。**

### 9.2 失败之后，单条记录上看不到任何失败痕迹

- **现象**：任务记录里明明写着「处理失败：…」，但清单里那条是「待解读」、没有失败原因。
- **根因**：两个原因叠加 ——
  ① 失败历史只写在 `ai_publish_job.lastRunMessage`（单例），单条记录只有 `errorMsg`；
  ② 在页面上点过「重置为待解读」会 `set status=PENDING, errorMsg=null`
     （`resetToPending` 的设计如此），把 `FAILED` 的痕迹抹掉，只留下 `finishedAt`。
- **修法**：查问题时**同时看 `ai_publish_job`**（`lastRunStatus` / `lastRunMessage`），
  只看 `book_interpretations` 会以为「什么都没发生」。
  ✅ 2026-10-09 起，失败时也会把模型原文写进 `rawContent`（**不进列表 VO，要用 pymongo 直连查**）。

### 9.3 页面永远显示「生成中」，重启也不消失

- **现象**：进程被杀（`stop-backend.cmd` 用的是 `taskkill /F`）后，那条记录卡在 `GENERATING`。
- **根因**：来不及写终态，DB 里留下快照，而内存里没有任务在跑。
- **修法**：**这是设计**（用户明确要求启动时**不做**自动清理）。
  在页面上点该行的「重置为待解读」捞回队列。

### 9.4 「手动执行完之后端就退出了」—— 其实是错觉

- **现象**：手动跑完一次，发现日志停在那一刻，以为应用退出了。
- **根因**：前端是**条件轮询**（只有 `genRunning` / `initRunning` 还是 true 才排下一次），
  生成结束后就停止轮询；而 `getJob()` 是全应用**唯一高频写日志**的地方。
  → **空闲的应用本来就不写日志**，日志停住 ≠ 进程死了。
- **修法**：判断进程是否还活着看**端口**（8080 是否在听），别看日志最后一行。
  应用**没有**任何「我要退出了」的记录（`addShutdownHook` 未加），所以
  「自己退出」和「被强杀」目前**无法从日志区分** —— 待办项。

### 9.5 后端挂掉后，页面每 2 秒弹一条「请求异常：HTTP 500」

- **现象**：后端不在时，页面不停弹 500，而且停不下来。
- **根因**：`views/publish/config/index.vue` 的 `load()` 在 catch 里什么都不做，
  `job.value` 保留旧值 → `running` 仍是 true → `schedulePoll()` 永远排下一次。
  （500 本身是 Vite proxy 在后端不可达时回的，是症状不是病因。）
- **修法**：⏸️ **未修**（用户 2026-10-09 说「其他非致命问题先忽略」）。
  建议方案：连续失败 N 次就停止轮询并提示。

### 9.6 不能复用 `wereadRestTemplate`

- **现象**：图省事复用现成的 `RestTemplate` bean → 报错信息读不出来 / 请求被截断 / 泄漏 Header。
- **根因**：那个 bean 上有三样东西不能带过来 ——
  ① 挂着 `WereadHeaderInterceptor`，会给**每个**请求注入微信读书的自定义 Header 和 `Cookie`
  （发给 AI 服务属于无谓的信息外泄）；
  ② 超时是「微信读书」的读数，生成一篇要 30~120 秒，用它**必然被截断**；
  ③ 错误处理器是包级私有（`RawResponseErrorHandler`），跨包拿不到。
- **修法**：`AiClient` 自己建一个 `RestTemplate`
  （`HttpComponentsClientHttpRequestFactory` + `NoThrowErrorHandler`）。
  ⚠️ 必须显式 `setSocketTimeout(readTimeout)` —— `RestTemplate` 默认**无限等**，
  对端不回时生成线程会永远挂着，页面永远显示「生成中」。
  `YuqueClient` 复用了 `AiClient.NoThrowErrorHandler`（同包，不需要 import）。
