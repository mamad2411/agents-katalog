# stats 模块知识

> 包路径：`com.bookcollector.stats` · 最后更新：2026-10-12
> **本模块的核心是「统计口径」。改之前先读第 6 节。**

## 1. 这个模块是干什么的

仪表盘的 4 个指标卡 + 4 张图。全部用 MongoDB **聚合管道**算，不把文档拉到 JVM 里算。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `controller/StatsController` | Controller | 3 个端点（`/overview` / `/charts` / `/today-collected`） |
| `service/StatsService` | Service 接口 | 3 个方法 |
| `service/impl/StatsServiceImpl` | Service 实现 | 4 个指标 + 4 张图 + 今日新增明细的全部查询 |

## 3. 调用关系（图谱）

```
StatsController ──► StatsService(Impl) ──┬──► MongoTemplate（聚合 / count）
                                          │        ├─► books
                                          │        ├─► collect_tasks
                                          │        ├─► collect_cursors
                                          │        └─► api_requests
                                          ├──► TaxonomyRepository ──► taxonomy_config
                                          │        （sourceKey → name 映射）
                                          └──► TaskRegistry（内存：activeCount）
```

## 4. 数据集合与索引

| 集合 | 用途 | 依赖索引 |
|---|---|---|
| `books` | 总数、今日新增、评分分布、年份趋势、近 7 天 | `idx_firstCollectedAt`（今日/近 7 天）、`idx_newRating`（评分分布）、`idx_lastCollectedAt`（最近采集时间） |
| `taxonomy_config` | 分类/榜单总数与启用数、`sourceKey → name` 映射 | — |
| `collect_tasks` | 任务总数、运行中任务数 | `idx_status` |
| `collect_cursors` | 游标总数 | — |
| `api_requests` | 请求总数 | — |

## 5. 对外接口

| 方法 | 路由 | 返回 |
|---|---|---|
| GET | `/api/stats/overview` | `{ bookTotal, categoryTotal, taskTotal, todayCollected, categoryEnabled, rankingTotal, rankingEnabled, taskRunning, activeRuns, cursorTotal, requestTotal, last7DaysCollected, lastCollectedAt }` |
| GET | `/api/stats/charts` | `{ categoryDistribution, ratingDistribution, publishYearTrend, recentCollected }` |
| GET | `/api/stats/today-collected` | `PageResult<Book>`（分页参数 `page` / `size`，默认 1 / 20，上限 200）。2026-10-12 新增 |

**为什么拆成两个端点**：数字要先出，图表慢不该拖住数字。
（第三个端点 `today-collected` 是**按需**拉的 —— 弹窗打开才发请求，不影响这条原则。）

## 6. 不变量与铁律 ← 改这个模块前必读

1. **🔴 「今日采集数」按 `firstCollectedAt`（净新增），不按 `lastCollectedAt`。**
   为什么：`lastCollectedAt` **每次 upsert 都会刷新**，重采同一批书会让它「今天又采了一万本」，
   而实际一本都没新增。用 `firstCollectedAt` 得到的是「今天库里多了多少本之前没有的书」——
   这才是用户看到这个数字时的预期。
   **图表「近 7 天采集量」用同一个口径**，否则指标卡和图表会互相矛盾。

2. **必须用聚合管道，不要把文档拉到 JVM 里算。**
   图书量预期 1 万–5 万条，每份 46 个字段。拉回来只为数几个桶，网络传输、反序列化、GC 全白干。
   聚合在 MongoDB 里跑，回来的只有几十行。

3. **管道直接写 `Document`，不用 `Aggregation.group(...)` 链式 API。**
   为什么：`$dateToString` / `$split` / `$arrayElemAt` / `$cond` 这类「表达式」用类型化 API
   写出来**更长、更难读**，而且字段名照样靠字符串拼（该错还是会错）。
   裸 `Document` 可以整段复制到 `mongosh` 里单独调试 —— 这个可验证性值很高。
   输出用 `Document.class` 接（聚合结果是「算出来的形状」，没有实体可映射）。

4. **🔴 分布图必须补齐空桶 / 空日期。**
   管道只会返回「有数据的日子 / 有书的区间」。直接喂 ECharts 会让一张 7 天柱图只剩 3 根柱子，
   横轴变成「有数据的日子」而不是时间轴，视觉上让人以为那几天之间没有间隔。

5. **年份要 `$gte 1900 $lte 2100` 过滤。**
   库里存在 `"0000-00-00 00:00:00"` 这类「未知时间」的占位值，不过滤会出现「0000 年」的尖峰。
   取年份用 `$split` + `$arrayElemAt`，**不用 `$substrBytes`**
   （后者对短于 4 字符的字符串行为依赖版本，而库里确实有 `"2022"` 这种只有年份的脏值）。

6. **评分分桶用 `$cond` + `$floor`，不用 `$bucket`。**
   `$bucket` 的边界数组必须严格递增、且恰好等于上边界的值会落到下一个桶（1000 会掉出去），
   要额外加一个 1001 的边界才能覆盖。`$cond` 一眼就能看出「≥1000 归到最后一桶」。

7. **聚合失败不能让仪表盘整个 500。** `aggregate()` 捕获 `RuntimeException` 后
   返回空列表 + 打 error 日志 —— 页面显示 0 比报错好。

8. **🔴 分类分布按「采集目标」分，不按「平台分类」分。**
   展开 `collectSource`（形如 `["category:300000", "ranking:rising"]`）后按来源计数，
   就是「各采集目标分别贡献了多少本书」。
   为什么不用平台给的 `category`（如「精品小说-社会小说」）：那个字段取值有几百个，
   饼图会碎成一片糊；而且它反映的是**微信读书**的分类体系，不是「我这个采集器采了什么」。
   副作用：同一本书既在分类里又在榜单里会被**计两次** —— 这是对的，
   两个扇区的和会大于图书总数，因为维度是「来源贡献量」而不是「图书不重复归属」。

9. **🔴 二级分类的来源必须并到它的一级上，否则饼图会废。**
   `category:200003`（历史-历史读物）这类二级来源，要按 `parentCode` 把计数累加到
   `category:200000` 上。两个理由：① 不并的话同一个大类会被拆成十几个扇区；
   ② `DISTRIBUTION_LIMIT` 只有 30，而二级有 166 个 —— **二级会把一级整个挤出榜单**，
   图上只剩二级，恰好丢掉「我采了哪几大类」这个信息。
   实现：`categoryDistribution()` + `categoryParentMap()` / `rollUpToTopCategory()`。

10. **`categoryTotal` / `categoryEnabled` 只数一级分类**（`parentCode == null`）。
    字典里现有 188 条 CATEGORY（22 一级 + 166 二级），直接 `countByType` 会让仪表盘
    那张卡片从 22 跳到 188；而它回答的是「我采了哪几大类」。
    实现：`countTopCategories()`。**二级的数量刻意不在仪表盘展示**（用户 2026-09-29 定口径），
    要看二级清单去「分类配置」页，要看某个二级采了多少去「任务配置」按任务看。

11. **🔴 「今日新增」指标卡和它的明细列表必须共用同一个条件。**
    指标卡走 `countCollectedSince(startOfToday())`，列表走 `todayCollectedBooks(...)` ——
    两处都基于 `startOfToday()`（Asia/Shanghai 零点），所以列表的 `total` 必然等于卡片上的数字。
    **不要**把任一处改成「最近 24 小时」：那在每天零点之后就会和另一处对不上，
    而「卡片说 39 本、点开只有 12 条」比不给这个功能更糟。
    列表排序补 `_id` 兜底 —— 批量 upsert 时同一批书的 `firstCollectedAt` 是同一个时间戳，
    只按它排的话同值记录在翻页时可能重复或漏掉。**不建新表**：`books.firstCollectedAt`
    本来就是「第一次进库的时间」，另立一张表只会多一份要同步的状态。

## 7. 依赖与耦合

- **依赖**：`book.entity.Book`、`taxonomy.repository.TaxonomyRepository`、
  `cursor.entity.CollectCursor`、`audit.entity.ApiRequest`、`task.TaskRegistry`、
  `common.enums.TargetType`、`MongoTemplate`。
- **被依赖**：前端仪表盘页。
- ⚠️ 本模块是「聚合多个模块的集合」的地方，依赖面天然较广。新增指标时优先用
  `MongoTemplate` 直接查，**不要**为了复用去给别的模块的 Repository 加方法。

## 8. 测试与验收

`BookQuerySemanticsIT` 注入了 `StatsService` 并验证聚合结果（含评分分布不为全 0 的回归）。

```bash
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=BookQuerySemanticsIT
```

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 评分分布柱图全是 0

- **现象**：`ratingDistribution` 每根柱子都是 0。
- **根因**：管道里 `$match` 了 `newRatingDetail.newRating` —— 这个字段**不存在**
  （`newRatingDetail` 只有 `{good, fair, poor, recent, title}`）。
  **聚合不报错**：`$match` 匹配不到任何文档时管道正常返回空结果。
- **修法**：路径改回顶层 `newRating`。同一个坑还影响 `BookQuery.resolveSortPath()`
  和 `BookRepository.buildCriteria`，以及 `MongoIndexInitializer.idx_newRating`。
  S4 做这张图时才发现 —— 藏了整整三个阶段。

### 9.2 「今日采集数」明显偏大

- **现象**：重采了一批书，指标卡的「今日采集」暴涨，但库里没多几本。
- **根因**：用了 `lastCollectedAt`（每次 upsert 都刷新）。
- **修法**：改用 `firstCollectedAt`（铁律 1）。**两处都要改**：指标卡和「近 7 天采集量」，
  否则两个数字会互相矛盾。

### 9.3 7 天柱图只有 3 根柱子

- **现象**：近 7 天里只有 3 天有数据，图上就只画 3 根柱子，看起来那几天是连续的。
- **根因**：管道只返回「有数据的日子」。
- **修法**：在 Java 侧按 `LocalDate.now(ZONE).minusDays(i)` 补齐 7 天（铁律 4）。
