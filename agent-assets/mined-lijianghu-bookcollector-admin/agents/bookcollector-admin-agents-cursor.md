# cursor 模块知识

> 包路径：`com.bookcollector.cursor` · 最后更新：2026-09-23
> **游标是断点续传的唯一权威。改这个模块前先读第 6 节铁律 1。**

## 1. 这个模块是干什么的

记录「每个采集目标采到哪儿了」，让任务可以中断后从原位置继续，而不是从头重采。

游标是**目标**的属性，不是任务的属性 —— `collect_cursors` 的主键是
`(targetType, targetId)`。这条定义决定了整个模块的语义（见铁律 1）。

## 2. 类清单

| 类 | 角色 | 一句话职责 |
|---|---|---|
| `controller/CursorController` | Controller | 3 个端点（列表 / 重置或指定 / 删除），**极薄转发** |
| `service/CursorService` | Service 接口 | 3 个方法 |
| `service/impl/CursorServiceImpl` | Service 实现 | 类型解析 + 校验 + 组装返回 |
| `repository/CursorStore` | Repository | `load` / `loadCursor` / `advance` / `reset` / `setCursor` / `delete` |
| `entity/CollectCursor` | Entity | `targetType` / `targetId` / `maxIndex` / `totalCollected` / `finished` / `lastRunId` |
| `req/CursorSetRequest` | req | 重置/指定请求体 |

## 3. 调用关系（图谱）

```
CursorController ──► CursorService(Impl) ──► CursorStore ──► collect_cursors
                                                  ▲
                          ┌───────────────────────┼───────────────────────┐
                          │                       │                       │
              task.TaskService.launch()     collector.CollectLoop    taxonomy 删除时
              （读起始游标 loadCursor）      （每页 advance）        （清孤儿游标 delete）
```

> `CollectLoop` 是唯一的 `advance` 调用方，`TaskService(Impl).launch` 是唯一的 `loadCursor` 调用方。

## 4. 数据集合与索引

| 集合 | 索引 | 为什么 |
|---|---|---|
| `collect_cursors` | `uk_target (targetType, targetId)` **唯一** | 一个 target 只能有一行游标，否则断点续传会读到不确定的值 |

## 5. 对外接口

| 方法 | 路由 | 说明 |
|---|---|---|
| GET | `/api/cursors` | 列表，按最近更新时间倒序 |
| PUT | `/api/cursors` | 重置 / 指定起点。`maxIndex=0` 或不传 = 重置为 0；`>0` = 从该位置继续 |
| DELETE | `/api/cursors/{id}` | 删除。删除后该目标被视为「从未采集过」，下次从 `maxIndex=0` 开始 |

`PUT` 的返回体：

```json
{
  "targetType": "CATEGORY", "targetId": "300000",
  "maxIndex": 0, "created": false, "reset": true,
  "note": "已采到的图书不会被删除；重置后再跑任务会从该位置继续（重复采到的书按 bookId 幂等更新）"
}
```

## 6. 不变量与铁律 ← 改这个模块前必读

1. **游标是「目标」的属性，不是「任务」的属性。** 这是本模块最重要的定义。
   推论：
   - 删任务**不删游标** —— 「删掉任务、重建一个同名任务」会从原位置继续，这通常正是用户想要的
   - 一个目标只能有一个任务（`collect_tasks.uk_target` 唯一索引），否则两个任务共享一个游标
     会产生**静默的意外行为**（A 采到第 100 页后 B 从第 100 页开始，界面上看不出异常）

2. **`advance` 必须在图书落库成功之后调用。**
   为什么：先推游标后落库，一旦落库失败，那批书就永久跳过了 —— 而游标已经走过，
   下次续传也不会再采到它们。

3. **`finished` 只能从 `false` 变 `true`，不允许被覆盖回去。**
   `advance` 里 `finished=true` 用 `set`，`false` 用 `setOnInsert`。
   为什么：否则一次「只采 5 页」的任务会把「已采到底」的状态抹掉。

4. **`reset` 与 `setCursor` 都要把 `totalCollected` 归零。**
   为什么：语义上「从头重采」等于「重新计数」。不归零的话第二次全量采集会把计数翻倍，
   那个数字就没意义了。

5. **`advance` 用 `Update` 而不是实体 `save()`** → `CollectCursor.updatedAt` 上的
   `@LastModifiedDate` **不会生效**，时间戳必须在 `Update` 里手工写。

6. **重置游标不会删已采到的书。** 返回值里显式带 `note` 说明这件事。
   想清库得另外调 `DELETE /api/books` —— 本接口不做这件事。

7. **运行中重置游标是「无效」的，且本模块不做拦截。**
   采集线程每采完一页就 `advance()` 一次，会覆盖手工设置的值。
   为什么不做拦截：判断「是否在跑」需要引入 `TaskRegistry` 依赖，而它对这个纯字典操作
   是多余的耦合。改为在响应里说明。正确姿势：**先取消任务 → 再重置游标 → 再启动**。

## 7. 依赖与耦合

- **依赖**：`common.enums.TargetType`、`common.{BizException,ResultBean}`。
- **被依赖**：`task`（读起始游标）、`collector`（推进游标）、`taxonomy`（删除时清孤儿游标）。
- 本模块**不依赖** `task` —— 这是刻意的（见铁律 7）。

## 8. 测试与验收

`TaskControlIT` 覆盖「重置游标 → 从 0 重采」；
`TaskOrchestrationTest` 覆盖「retry 从当前游标续传，起始游标 = 60」。

```bash
tools/mvn8.sh -f backend/pom.xml -o -B test -Dtest=TaskControlIT
```

## 9. 已知陷阱（现象 → 根因 → 修法）

### 9.1 重置了游标但任务还是从老位置继续

- **现象**：在「断点续传」页点了重置，再启动任务，它还是从第 100 页开始。
- **根因**：任务当时还在运行 —— 采集线程每采完一页就 `advance()`，把你的手工值覆盖了。
- **修法**：**先取消任务**，等它停止，再重置游标，再启动。这是设计使然，不是缺陷。

### 9.2 `@LastModifiedDate` 不生效

- **现象**：改了游标，`updatedAt` 没变。
- **根因**：`advance` / `reset` / `setCursor` 用的是 `Update`（原子更新），
  Spring Data 的审计注解只对实体 `save()` 生效。
- **修法**：在 `Update` 里手工 `.set("updatedAt", new Date())`。**不要**为此改成 `save()`
  —— 那会引入读-改-写竞态。

### 9.3 「已采到底」状态被抹掉

- **现象**：一个已经采完的分类，跑了一次「只采 5 页」的任务后，`finished` 变回 `false`。
- **根因**：`advance` 对 `finished=false` 用了 `set` 而不是 `setOnInsert`。
- **修法**：已按铁律 3 实现。改 `advance` 时**不要**动这个分支。
