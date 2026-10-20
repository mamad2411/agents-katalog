# readinglist 模块知识

> 包路径：`com.bookcollector.readinglist` · 创建：2026-10-12
> **本模块与 `shelf`（藏书阁）是并列的两个「叶子」，互不 import、互不查询对方。**

## 1. 这个模块是干什么的

「藏书阁 → 阅读清单」页 —— **想读 / 在读 / 已读** 的阅读计划，以及
**图书库 / 精选图书 / 我的藏书 / 阅读清单 四个列表页**的「加入阅读清单 / 移除 / 改状态」。

数据是自己的集合 `reading_list`（**快照式**）。

### 与 `shelf` 的关系（本模块最容易搞错的地方）

| | `shelf`（藏书阁） | `readinglist`（本模块） |
|---|---|---|
| 回答的问题 | 我**收藏**了什么 | 我**打算读**什么、读到哪了 |
| 集合 | `shelf_books` | `reading_list` |
| 状态 | 无（在就是收藏） | `WANT_TO_READ` / `READING` / `FINISHED` |
| 加入前提 | 书在 `books` 里 | 书在 `books` 里（**不要求已收藏**） |

🔴 **两个维度不可互相推导，也不许互相影响**：
- 收藏了一本 ≠ 想读；想读一本 ≠ 收藏。
- **移除一个不影响另一个** —— 从藏书阁移除，阅读清单里那条保留；反之亦然。
- 后端层面：本模块的 Service **一行都不碰** `shelf_books`；`ShelfServiceImpl` 也不碰 `reading_list`。
- 前端层面：四个页面**并发**调 `/api/shelf/status` 与 `/api/reading-list/status` 两个接口，
  各自维护状态，不互相推导。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `controller/ReadingListController` | Controller | 6 个端点（分页 / 计数 / 加入 / 移除 / 改状态 / 批量查状态） |
| `service/ReadingListService` | Service 接口 | 6 个方法 |
| `service/impl/ReadingListServiceImpl` | Service 实现 | 参数归一化 + 状态校验 + 加入时取快照 |
| `repository/ReadingListRepository` | Repository | `reading_list` 读写 + 从 `books` 取快照 |
| `entity/ReadingListItem` | 实体 | 集合 `reading_list`：9 个快照字段 + `status` + `addedAt` + `statusUpdatedAt` |
| `entity/ReadingStatus` | 枚举 | 三态 + `label`；`parse()` 严格（入参校验）/ `of()` 宽松（展示） |
| `vo/ReadingListBookVO` | VO | 对外投影（9 字段 + 状态三件套，**不吐 `_id` / `addedAt`**） |
| `vo/ReadingListStatusVO` | VO | `{bookId, status}`（批量查状态的返回项） |
| `vo/ReadingListSummaryVO` | VO | 各状态计数（Tab 角标） |
| `req/ReadingListAddRequest` | 请求体 | `{bookId, status?}` |
| `req/ReadingListStatusRequest` | 请求体 | `{bookIds}` |
| `req/ReadingListStatusUpdateRequest` | 请求体 | `{status}` |

## 3. 调用关系（图谱）

```
ReadingListController ──► ReadingListService(Impl) ──► ReadingListRepository ──┬──► reading_list（读写）
                                                                               └──► books（**只读**：取 9 字段快照）

前端：views/shelf/reading/index.vue（阅读清单页）
      views/book/index.vue · views/book/featured/index.vue · views/shelf/index.vue（三处的操作列）
      ──► api/readingList.ts ──► composables/useBookActions.ts（统一动作）
```

## 4. 数据集合与索引

| 集合 | 用途 | 依赖索引 |
|---|---|---|
| `reading_list` | 阅读清单自己的表（快照） | `uk_bookId`（**唯一**，幂等加入的正确性依赖）、`idx_status_updated (status, statusUpdatedAt DESC)` |
| `books` | 加入时按 `bookId` 取 9 字段快照（**只读**） | `uk_bookId` |

索引在 `config.MongoIndexInitializer.initReadingList()` 里建（**2 个**），
它同时是 `reading_list` 集合的**唯一建表入口**（在不存在的集合上建索引会把集合建出来）。

## 5. 对外接口

| 方法 | 路由 | 返回 |
|---|---|---|
| GET | `/api/reading-list/books?status&category&title&author&page&size` | `PageResult<ReadingListBookVO>`（默认 `size=30`，上限 200） |
| GET | `/api/reading-list/summary` | `{wantToRead, reading, finished, total}` |
| POST | `/api/reading-list/books` | `Boolean`（`true`=新加入；`false`=本来就在） |
| DELETE | `/api/reading-list/books/{bookId}` | `Boolean`（`true`=确实删了；`false`=本来就不在） |
| PUT | `/api/reading-list/books/{bookId}/status` | `Boolean`（`true`=现在处于目标状态；`false`=不在清单里） |
| POST | `/api/reading-list/status` | `[{bookId, status}]`（只含已在清单里的） |

> ⚠️ 与 `shelf` 的 `POST /status` 返回 `Set<String>` 不同，这里返回 `[{bookId, status}]` ——
> 四个页面既要判「在不在」，也要显示**当前状态**，只回一个 ID 集合只能答前半句。

## 6. 不变量与铁律 ← 改这个模块前必读

1. **🔴 字段是「快照」不是「引用」。**
   书名 / 作者 / 封面 / 分类 / 评分 / 简介都是**加入阅读清单那一刻**的值。
   图书库后来改了或删了，都**不该**改写这里。代价：图书库删掉一本书后，清单里**仍会留着它**。

2. **🔴 加入必须 `snapshot.setId(null)`。**
   `readBookSnapshot()` 用 `findOne(query, ReadingListItem.class, "books")` 读，读回来的对象
   **带着 books 的 `_id`**。不清掉就直接 `insert`，插进去的是同一个 `_id`。
   见 `ReadingListServiceImpl.add()`（与 `shelf` 的坑完全同源）。

3. **🔴 状态校验「严格入参、宽松展示」。**
   - 入参（`add` 的 status、`updateStatus` 的 status）走 `ReadingStatus.parse()`，
     非法值 **抛 `BizException.warn`（code=400）**，**不静默降级** ——
     用户点「标记为已读」失败时若被悄悄改成「想读」，比报错更让人困惑。
   - 展示（`toVO` 里的 `statusLabel`）走 `ReadingStatus.of()`，认不出的旧值当「想读」，不让列表挂掉。

4. **🔴 列表排序 `statusUpdatedAt DESC` → `_id DESC`。**
   主序「最近操作的先看」；后一级只为**确定性** —— 分页的正确性依赖排序是个全序，
   否则同一时间戳的书在翻页时会重复 / 漏（同 `shelf` 铁律 3）。

5. **`updateStatus` 用 `matchedCount` 而不是 `modifiedCount`。**
   目标状态与当前相同时 MongoDB 的 `modifiedCount` 是 0，但「这本书现在确实处于目标状态」
   仍然成立。用 `matchedCount` 才能把「幂等地设成同一个值」（1）和「这本书根本不在清单里」（0）
   区分开。

6. **`category` 是「一级-二级」拼串**（如 `文学-散文杂著`），一级 = 第一个 `-` 之前。
   匹配用 `^\Q文学\E(-|$)`：前缀匹配 + 也接受裸值 + `Pattern.quote` 转义
   （类目名是用户输入，不转义的话 `.*` 能查出全表）。

7. **本模块不依赖任何业务模块（单向叶子）。**
   从 `books` 取快照时，`BOOKS_COLLECTION = "books"` 是**字符串常量**，
   **不 import `book` 模块的实体**。反向也守住：「这本书是否在阅读清单」**不由图书库接口返回**，
   而是前端拉完列表后带当前页 `bookId` 调 `POST /api/reading-list/status` 问一次。

8. **不存正文**（`content` / `rawContent`）。清单只用来「看」与「标记进度」。

9. **参数归一化在 Service 层**：`topCategoryOf()`（截到一级）、`normalizePage()`（`>=1`）、
   `normalizeSize()`（默认 30 / 上限 200）、`resolveStatus()`（校验 + 默认值）。

## 7. 依赖与耦合

- **依赖**：`MongoTemplate`、`common.BizException` / `common.PageResult`、`util.RegexUtil`、Lombok。
  **不 import 任何业务模块的类**（含 `shelf`）。
- **被依赖**：前端 `api/readingList.ts` + `composables/useBookActions.ts`，
  页面 `views/shelf/reading/`、`views/book/`、`views/book/featured/`、`views/shelf/`。
- ⚠️ 前端**不要**把两个维度合并成一个「已读/已收藏」的派生状态 —— 那正是需求明确禁止的。

## 8. 测试与验收

**无模块专属测试**（按用户硬规则 4：不写单测）。验收走前端手工：

- 阅读清单页：4 个状态 Tab（全部/想读/在读/已读）+ 角标正确 / 下滑加载 / 改状态后刷新仍保持
- 图书库：对一本**未收藏**的书点「加入阅读清单」→ 成功；再点「加入藏书」→ 两边各有一条
- 从「我的藏书」移除该书 → 阅读清单里那条**仍在**；反向同理
- 后端编译：`cd backend && ../tools/mvn8.sh -o -B clean test-compile`

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 加入报 `E11000` / 第二次加不进

- **根因**：`readBookSnapshot()` 读回来的对象带着 books 的 `_id`，没清就 insert。
- **修法**：`snapshot.setId(null)`（铁律 2）。并发下由 `catch (DuplicateKeyException)` 兜底
  → 视为「已存在」返回 `false`，**不报错**。

### 9.2 点「标记为已读」没生效，反而变成「想读」

- **根因**：入参用了宽松解析（`ReadingStatus.of()`），非法值被静默降级成默认值。
- **修法**：入参走 `parse()` + 抛 `BizException.warn`（铁律 3）。

### 9.3 改成相同状态时接口返回 false

- **根因**：用了 `modifiedCount`（MongoDB 认为「没修改」时为 0）。
- **修法**：改用 `matchedCount`（铁律 5）。

### 9.4 翻页重复 / 漏书

- **根因**：排序不是全序（只按 `statusUpdatedAt` 排，同一毫秒的书顺序不稳定）。
- **修法**：排序补 `_id DESC`（铁律 4）。
