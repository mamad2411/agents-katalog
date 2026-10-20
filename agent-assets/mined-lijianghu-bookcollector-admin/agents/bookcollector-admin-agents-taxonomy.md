# taxonomy 模块知识

> 包路径：`com.bookcollector.taxonomy` · 最后更新：2026-09-23

## 1. 这个模块是干什么的

维护「采集目标字典」：一级分类 21 个 + 二级分类（清单见 `config.SeedRunner` 的 `SUB_CATEGORIES`）
+ 榜单 7 个。它决定了「新建任务时下拉框里能选什么」，也是 `targetType + targetId` 的**名称来源**
（`category:300000` → 「文学」）。

🔴 **一级与二级都是合法的采集目标**：`targetId` 只是被原样拼进
`/bookListInCategory/{targetId}`（见 `collector/WereadClient#buildUrl`），传二级 ID 同样成立。
上游对**每个 ID 各自**封顶 25 页（500 本）→「历史」+「历史-历史读物」… 把可采总量放大一个量级。

字典本身在启动时由 `config.SeedRunner` 播种（只补缺失、不覆盖已有）。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `controller/TaxonomyController` | Controller | 分类与榜单各 4 个端点（共 8 个），同一套逻辑按 `type` 分派 |
| `service/TaxonomyService` | Service 接口 | 4 个方法（列表/新增/编辑/删除） |
| `service/impl/TaxonomyServiceImpl` | Service 实现 | **三条业务规则都在这里** |
| `repository/TaxonomyRepository` | Repository | 按 `type` 查、按 `type+code` 查、`maxSort` |
| `entity/TaxonomyItem` | Entity | `type` / `code` / `name` / **`parentCode`** / `enabled` / `sort` / `remark` |
| `req/TaxonomyRequest` | req | 新增/编辑共用请求体 |

## 3. 调用关系（图谱）

```
TaxonomyController ──► TaxonomyService(Impl) ──┬──► TaxonomyRepository ──► taxonomy_config
   （/categories                                │
     /rankings）                                 ├──► TaskRepository.countByTarget()
                                                 │        └─► collect_tasks（查引用）
                                                 └──► CursorStore.delete()
                                                          └─► collect_cursors（清孤儿游标）

config.SeedRunner（启动时一次）──► TaxonomyRepository ──► taxonomy_config
```

## 4. 数据集合与索引

| 集合 | 索引 | 为什么 |
|---|---|---|
| `taxonomy_config` | `uk_type_code (type, code)` **唯一** | **seed 幂等的依赖** |
| | `idx_sort` | 前端下拉框按 `sort` 排 |

## 5. 对外接口

分类与榜单是同一套逻辑，只是 `type` 固定：

| 方法 | 路由 | 说明 |
|---|---|---|
| GET | `/api/taxonomy/categories` | 列表（`enabledOnly=true` 用于新建任务下拉框） |
| POST | `/api/taxonomy/categories` | 新增 |
| PUT | `/api/taxonomy/categories/{id}` | 编辑（**不允许改 `code`**） |
| DELETE | `/api/taxonomy/categories/{id}` | 删除（**有任务引用则拒绝**） |
| GET/POST/PUT/DELETE | `/api/taxonomy/rankings[/{id}]` | 同上，`type = RANKING` |

## 6. 不变量与铁律 ← 改这个模块前必读

1. **编辑不允许改 `code`。** `code` 是采集目标的身份（`collect_tasks.targetId` 和
   `collect_cursors.targetId` 都存它）。改了之后已有任务和游标就指向一个字典里不存在的目标
   —— 任务还能跑（URL 是拼 code 的），但「新建任务」的下拉框里找不到它，
   界面上表现为「这个任务的目标名点不进去」。
   请求体里带了 `code` 且与当前值不同 → **直接报错**，不要静默忽略
   （静默忽略会让用户以为改成功了，这是最难排查的一类问题）。
   改名（`name`）无所谓 —— 它只是展示，而且是冗余快照。

2. **有任务引用则不允许删除。** 先 `TaskRepository.countByTarget(type, code)` 查引用，
   `> 0` 就拒绝并告诉用户还剩几个任务。
   为什么：删掉字典项后那个任务依然会跑，但目标在字典里查不到了 ——
   界面上会出现「新建任务时选不到它，但任务列表里它还在」。这种不一致比直接拒绝难排查得多。

3. **删除时顺带清理游标。** 只有游标、没有任务 → 允许删，并顺手 `CursorStore.delete()`，
   返回 `cursorsRemoved`。
   为什么：否则 `collect_cursors` 里会留下一条永远没有入口能看到的孤儿记录
   （「断点续传」页是按游标列表渲染的，它会出现，但点「重置」没有任何意义）。

4. **`sort` 不传时自动排到末尾**（`maxSort + 1`）。让用户自己填 `sort` 是没必要的负担，
   而默认都填 1 又会让下拉框顺序随机。

5. **seed 逻辑不在这里。** 它在 `config.SeedRunner` —— 只在启动时跑一次，
   策略是「只补缺失、不覆盖已有」，与这里「用户主动增删改」的语义不同。

6. **🔴 `parentCode` 是层级的唯一表达：`null` = 一级分类，非 null = 二级分类。**
   （2026-09-24 加入）

   - **二级分类不是另一个 `type`** —— 复用 `CATEGORY`，只用 `parentCode` 区分层级。
     理由：`type` 在下游到处被当**键**用（`CollectCommand.sourceKey()` 决定 `collectSource`
     前缀 `category:`，还被用作任务 / 游标 / 审计三张表的联合键）。新增枚举要动 9 处链路，
     而 `parentCode` 一处都不用动。**别再提「加个 SUB_CATEGORY 枚举」。**
   - **只有一级的 `code` 能当 `categoryId` 用。** 图书库的「平台分类」筛选走
     `BookQuery.categoryId`，它精确匹配 `bookInfo.categories[].categoryId`；而二级的 `code`
     是 `subCategoryId`，**是另一个字段** —— 传进去恒不匹配、**静默返回 0 条**。
     所以 `views/book/index.vue` 的 `categoryOptions` **必须只列一级**；
     同一个文件的 `targetOptions`（采集来源）则**保持全量**，二级本来就该在那里。
   - **`sort` 不保证连续，更不表达层级。** seed 是「只补缺失、不覆盖已有」，所以已有库上
     二级的 `sort` 注定排在全部一级之后（22+），插不回各自上级的后面。
     → 前端**按 `parentCode` 分组渲染**（`TaskFormDialog.vue` 的 `availableGroups`），
     不要试图靠 `sort` 排层级。
   - **`name` 统一用「一级-二级」形式**（如 `历史-历史读物`），与平台
     `bookInfo.categories[].title` / `Book.category` 的格式对齐，这样字典页、任务名、
     分类分布饼图三处口径自动一致。

## 7. 依赖与耦合

- **依赖**：`task.repository.TaskRepository`（查引用）、`cursor.repository.CursorStore`（清游标）、
  `common.enums.TargetType`。
- **被依赖**：`task`（新建任务时校验目标存在）、`stats`（读字典做 `sourceKey → name` 映射）、
  `config.SeedRunner`。
- ⚠️ `TaxonomyService` 依赖 `TaskRepository` 和 `CursorStore`，这两个都是别的模块的类 ——
  这是**已知的跨模块依赖**，本轮不重构。

## 8. 测试与验收

`S1DataLayerTest` 覆盖 `uk_type_code` 唯一索引与 seed 幂等。
`ApiCrudIT` 覆盖端到端 CRUD 契约。

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 重复添加同一目标 → `DuplicateKeyException`

- **现象**：新增一个已存在的 `(type, code)` 报错。
- **根因**：`uk_type_code` 唯一索引。
- **修法**：这是**产品缺陷之外的正常路径**（用户重复添加同一个目标）。
  `TaxonomyServiceImpl.create` 捕获 `DuplicateKeyException` 后转成
  `BizException.duplicate("该分类已存在：code=300000")`。**不要**把异常直接抛到前端。

### 9.2 库里 `type` 字段可能有历史脏数据

- **现象**：读一条 `type` 非法的记录。
- **根因**：`type` 在库里是字符串，可能有人手工改过。
- **修法**：`TaxonomyServiceImpl.parseType` 把 `IllegalArgumentException` 包成
  `BizException(code_err, "字典项的类型非法：xxx")`，报可读错误而不是 500。

### 9.3 `SeedRunner` 新增条目后要重启才生效

- **现象**：改了 `SeedRunner` 里的字典，运行中的服务看不到新条目。
- **根因**：`SeedRunner` 是 `ApplicationRunner`，只在启动时跑。
- **修法**：重启后端。它**不会**覆盖已有条目，所以改 `name` 需要走接口编辑。
