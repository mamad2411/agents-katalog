# TickTick MCP Skill

> 滴答清单（TickTick）任务管理 MCP 插件完整使用指南
> 适用于 OpenClaw 智能体通过 MCPorter 调用

---

## 1. 概述

TickTick MCP 提供 20 个工具，覆盖项目管理、任务 CRUD、智能过滤、批量操作和 GTD 工作流。连接的是**滴答清单国内版**（dida365.com）。

### 核心概念

- **Project（项目/清单）**：任务的容器，每个任务必须属于一个项目。分为两种类型：
  - `TASK`（任务清单）：包含可操作的待办任务
  - `NOTE`（笔记清单）：包含笔记内容，任务过滤工具会自动跳过
- **Task（任务）**：基本工作单元，包含标题、内容、日期、优先级等。状态分为 Active（活跃）和 Completed（已完成）
- **Subtask（子任务）**：附属于父任务的子项，必须在同一项目内
- **Inbox（收集箱）**：特殊项目，需通过环境变量 `TICKTICK_INBOX_ID` 配置
- **Closed/Archived（已归档）**：清单可被归档，归档后默认不在列表和过滤中显示
- **Priority（优先级）**：`0`=无, `1`=低, `3`=中, `5`=高（注意：不是 0-5 连续的）

### 日期格式

所有日期参数统一使用 ISO 格式，带时区偏移：

```
YYYY-MM-DDThh:mm:ss+0000
```

示例：
- `2025-03-09T10:00:00+0800` （北京时间上午10点）
- `2025-03-09T02:00:00+0000` （UTC 时间）
- `2025-03-09T00:00:00+0800` （全天任务推荐格式，配合 `is_all_day=True`）

**关键规则**：
- 时区偏移用 `+0800` 格式（无冒号），系统会自动标准化
- `+08:00`、`Z`、无时区 均可接受，系统自动转换
- 全天任务（如生日、截止日）应设置 `is_all_day=True` 以避免时区漂移

---

## 2. 工具清单

### 2.1 项目管理

| 工具 | 用途 | 必填参数 | 可选参数 |
|------|------|---------|---------|
| `get_projects` | 获取所有项目列表 | 无 | `kind`("TASK"/"NOTE"), `include_closed`(bool) |
| `get_project` | 获取单个项目详情 | `project_id` | 无 |
| `create_project` | 创建新项目 | `name` | `color`(hex), `view_mode`(list/kanban/timeline) |
| `delete_project` | 删除项目 | `project_id` | 无 |

### 2.2 任务 CRUD

| 工具 | 用途 | 必填参数 | 可选参数 |
|------|------|---------|---------|
| `get_task` | 获取单个任务详情 | `project_id`, `task_id` | 无 |
| `get_project_tasks` | 获取项目内所有任务 | `project_id` | `include_completed`(bool) |
| `get_inbox_tasks` | 获取收集箱任务 | 无 | 无 |
| `create_task` | 创建任务 | `title`, `project_id` | `content`, `start_date`, `due_date`, `priority`, `is_all_day` |
| `update_task` | 更新任务 | `task_id`, `project_id` | `title`, `content`, `start_date`, `due_date`, `priority` |
| `complete_task` | 标记任务完成 | `project_id`, `task_id` | 无 |
| `delete_task` | 删除任务 | `project_id`, `task_id` | 无 |
| `create_subtask` | 创建子任务 | `subtask_title`, `parent_task_id`, `project_id` | `content`, `priority` |
| `batch_create_tasks` | 批量创建任务 | `tasks`(列表) | 无 |

### 2.3 智能查询与过滤

| 工具 | 用途 | 参数 |
|------|------|------|
| `get_all_tasks` | 获取所有活跃任务 | 无 |
| `get_tasks_by_priority` | 按优先级筛选 | `priority_id`(0/1/3/5) |
| `get_tasks_due_today` | 今日到期任务 | 无 |
| `get_tasks_due_tomorrow` | 明日到期任务 | 无 |
| `get_tasks_due_in_days` | N天后到期任务 | `days`(非负整数) |
| `get_tasks_due_this_week` | 本周到期任务（7天内） | 无 |
| `get_overdue_tasks` | 逾期任务 | 无 |
| `search_tasks` | 按关键词搜索 | `search_term`(字符串) |

### 2.4 GTD 工作流

| 工具 | 用途 | 筛选逻辑 |
|------|------|---------|
| `get_engaged_tasks` | 当前应专注的任务 | 高优先级(5) OR 今日到期 OR 已逾期 |
| `get_next_tasks` | 下一步要做的任务 | 中优先级(3) OR 明日到期 |

---

## 3. 使用模式与最佳实践

### 3.1 标准工作流：先查项目，再操作任务

**几乎所有任务操作都需要 `project_id`**。正确流程：

1. 调用 `get_projects` 获取项目列表及其 ID
2. 用获得的 `project_id` 进行后续操作

```
# 错误：凭空编造 project_id
create_task(title="买菜", project_id="abc123")  ❌

# 正确：先查询
get_projects()  →  得到 "生活" 项目 ID: "648283d6..."
create_task(title="买菜", project_id="648283d6...")  ✅
```

### 3.2 创建任务的完整示例

```python
# 基础任务
create_task(
    title="完成周报",
    project_id="648283d6e4b073fe87ff544d"
)

# 带日期和优先级的任务
create_task(
    title="提交论文初稿",
    project_id="34534f07bd597ab16cabfdbd",
    content="包含第三章和第四章的修改",
    due_date="2025-03-15T23:59:00+0800",
    priority=5,
    is_all_day=False
)

# 全天任务（如截止日、纪念日）
create_task(
    title="报名截止",
    project_id="648283d6e4b073fe87ff544d",
    due_date="2025-04-01T00:00:00+0800",
    is_all_day=True
)
```

### 3.3 批量创建任务

`batch_create_tasks` 接收一个任务列表，所有任务先验证后再创建：

```python
batch_create_tasks(tasks=[
    {
        "title": "阅读第1章",
        "project_id": "648283d6...",
        "priority": 3,
        "due_date": "2025-03-10T18:00:00+0800"
    },
    {
        "title": "阅读第2章",
        "project_id": "648283d6...",
        "priority": 1,
        "due_date": "2025-03-11T18:00:00+0800"
    },
    {
        "title": "撰写读书笔记",
        "project_id": "648283d6...",
        "priority": 5,
        "due_date": "2025-03-12T18:00:00+0800",
        "content": "包含关键概念总结"
    }
])
```

每个任务字典的字段：
- **必填**：`title`, `project_id`
- **可选**：`content`, `start_date`, `due_date`, `priority`

### 3.4 子任务

子任务必须与父任务在**同一个项目**中：

```python
# 先创建父任务
create_task(title="准备考试", project_id="64772a08...")
# → 返回 task_id: "69ae24b9..."

# 再创建子任务
create_subtask(
    subtask_title="复习第一单元",
    parent_task_id="69ae24b9...",
    project_id="64772a08..."
)
```

### 3.5 更新与完成任务

更新任务时 `task_id` 和 `project_id` 都是必填的，只传需要修改的字段：

```python
# 仅修改优先级
update_task(task_id="69ae24b9...", project_id="64772a08...", priority=5)

# 修改标题和截止日期
update_task(
    task_id="69ae24b9...",
    project_id="64772a08...",
    title="新标题",
    due_date="2025-03-20T18:00:00+0800"
)

# 标记完成
complete_task(project_id="64772a08...", task_id="69ae24b9...")
```

### 3.6 每日回顾推荐流程

```
1. get_overdue_tasks()          → 查看逾期任务，决定是否重新安排
2. get_tasks_due_today()        → 确认今日待办
3. get_engaged_tasks()          → 获取需要立即关注的任务（高优先级+今日+逾期）
4. get_next_tasks()             → 查看明天和中优先级任务，提前规划
5. get_tasks_due_this_week()    → 本周全局视图
```

---

## 4. 错误处理

### 4.1 常见错误与应对

| 错误信息 | 原因 | 处理方式 |
|---------|------|---------|
| `Failed to initialize TickTick client` | API 凭证无效或过期 | Token 已过期，需要管理员重新认证 |
| `Error fetching projects: 401` | access_token 过期 | 系统会自动用 refresh_token 刷新，通常无需干预 |
| `Inbox ID not configured` | 未设置 TICKTICK_INBOX_ID | 需在 .env 中配置收集箱 ID |
| `Invalid priority` | 使用了不合法的优先级值 | 只能用 0, 1, 3, 5 |
| `Invalid start_date format` | 日期格式错误 | 使用 `YYYY-MM-DDThh:mm:ss+0800` 格式 |
| `Validation errors found` | 批量创建中某些任务数据无效 | 检查每个任务的 title 和 project_id 是否存在 |

### 4.2 返回值包含 "error" 的处理

所有工具返回纯文本字符串。如果包含 "Error" 或 "Failed" 开头的内容，表示操作失败。应向用户说明失败原因并建议重试或修正参数。

### 4.3 项目/任务 ID 不存在

API 会返回 404 错误。应对方式：
1. 重新调用 `get_projects` 获取最新项目列表
2. 用 `get_project_tasks` 获取项目内任务列表
3. 用正确的 ID 重试操作

---

## 5. 重要限制与注意事项

### 5.1 API 限制
- 所有查询类工具会**自动跳过已归档项目和 NOTE 类清单**（只搜索 TASK 类活跃清单）
- `get_projects()` 默认隐藏已归档清单，传 `include_closed=True` 显示全部
- `get_projects(kind="TASK")` 只返回任务清单，`kind="NOTE"` 只返回笔记清单
- `search_tasks` 搜索范围：任务标题、内容、子任务标题（大小写不敏感，精确子串匹配）
- `get_project_tasks` 默认只返回活跃任务，传 `include_completed=True` 可包含已完成任务
- 批量创建任务是**顺序逐个创建**，不是原子操作——部分成功部分失败是可能的

### 5.2 优先级映射（非连续）
```
0 = None（无优先级）
1 = Low（低）
3 = Medium（中）     ← 注意跳过了 2
5 = High（高）       ← 注意跳过了 4
```
用户说"高优先级"就用 5，"中等"用 3，"低"用 1。不要使用 2 或 4。

### 5.3 日期与时区
- 用户所在时区为 **UTC+8（北京时间）**
- 创建任务时日期应使用 `+0800` 偏移
- 全天任务（生日、截止日等）务必设置 `is_all_day=True`
- 系统内部以 UTC 比较日期，"今日"/"逾期"判断基于 UTC 日期

### 5.4 收集箱（Inbox）
- `get_inbox_tasks` 需要预先配置 `TICKTICK_INBOX_ID` 环境变量
- 如果未配置，该工具会返回提示信息而非报错
- 其他工具（如 `get_all_tasks`）在配置了 Inbox ID 后会自动包含收集箱

### 5.5 项目类型（Kind）与归档（Closed）
- 每个项目有 `kind` 属性：`TASK`（任务清单）或 `NOTE`（笔记清单）
- 项目可以被归档（`closed=True`），归档后默认不显示
- 所有任务过滤工具（today/overdue/week/search 等）**默认只扫描未归档的 TASK 类清单**
- `format_project` 输出中会显示 `Kind: Task List` 或 `Kind: Note List`

---

## 6. 用户当前项目列表

以下为该账号中已有的项目（供快速引用）：

| 项目名 | Project ID | 类型 | 状态 |
|--------|-----------|------|------|
| Inbox（收集箱） | `inbox1020192021` | TASK | 活跃 |
| 😇考研事 | `64772a0894ee7fcde42af8d4` | TASK | 已归档 |
| 🥰放眼未来 | `648283d6e4b073fe87ff544d` | TASK | 已归档 |
| ✨100个基本 | `6496519ae4b09fb677468caa` | NOTE | 已归档 |
| 网站 | `655765ede4b0343e44552e24` | TASK | 已归档 |
| 毕业论文 | `34534f07bd597ab16cabfdbd` | TASK | 已归档 |

> 注意：项目列表可能随时间变化，如需最新数据请调用 `get_projects`

---

## 7. 场景示例

### 场景 A：用户说"帮我在毕业论文项目下添加一个高优先级任务，下周五截止"

```
1. 从已知项目表中找到 毕业论文 → project_id = "34534f07bd597ab16cabfdbd"
2. 计算下周五的日期
3. 调用：
   create_task(
       title="用户描述的任务标题",
       project_id="34534f07bd597ab16cabfdbd",
       due_date="2025-03-14T23:59:00+0800",
       priority=5
   )
```

### 场景 B：用户说"我今天有什么要做的？"

```
1. get_tasks_due_today()    → 今日到期任务
2. get_overdue_tasks()      → 逾期未完成任务
3. 合并结果汇报给用户，按优先级排序呈现
```

### 场景 C：用户说"把考研相关任务全部拉出来看看"

```
1. get_project_tasks(project_id="64772a0894ee7fcde42af8d4")
   → 获取 😇考研事 项目下所有活跃任务
2. 如果用户想看已完成的：
   get_project_tasks(project_id="64772a0894ee7fcde42af8d4", include_completed=True)
```

### 场景 D：用户说"搜索所有包含'论文'的任务"

```
search_tasks(search_term="论文")
→ 在所有项目的标题、内容、子任务中搜索
```

### 场景 E：用户说"帮我创建一个新项目叫'英语学习'，然后加三个任务"

```
1. create_project(name="英语学习")
   → 获得新项目的 project_id
2. batch_create_tasks(tasks=[
       {"title": "背单词 Day1", "project_id": "<新ID>", "priority": 1},
       {"title": "听力练习", "project_id": "<新ID>", "priority": 3},
       {"title": "写作训练", "project_id": "<新ID>", "priority": 3}
   ])
```

### 场景 F：用户说"完成了'提交初稿'这个任务"

```
1. 如果不知道 task_id，先搜索：search_tasks(search_term="提交初稿")
2. 从结果中获取 project_id 和 task_id
3. complete_task(project_id="...", task_id="...")
```

---

## 8. 决策树：如何选择正确的工具

```
用户想要...
├─ 查看项目/清单
│  ├─ 全部活跃项目 → get_projects()
│  ├─ 只看任务清单 → get_projects(kind="TASK")
│  ├─ 只看笔记清单 → get_projects(kind="NOTE")
│  ├─ 含已归档 → get_projects(include_closed=True)
│  └─ 单个项目详情 → get_project(project_id)
├─ 查看任务
│  ├─ 全部任务 → get_all_tasks
│  ├─ 某项目的任务 → get_project_tasks(project_id)
│  ├─ 含已完成任务 → get_project_tasks(project_id, include_completed=True)
│  ├─ 收集箱任务 → get_inbox_tasks
│  ├─ 按优先级 → get_tasks_by_priority(priority_id)
│  ├─ 今日到期 → get_tasks_due_today
│  ├─ 明日到期 → get_tasks_due_tomorrow
│  ├─ N天后到期 → get_tasks_due_in_days(days)
│  ├─ 本周到期 → get_tasks_due_this_week
│  ├─ 已逾期 → get_overdue_tasks
│  ├─ 搜索关键词 → search_tasks(search_term)
│  ├─ 需要立即关注 → get_engaged_tasks
│  └─ 下一步规划 → get_next_tasks
├─ 创建
│  ├─ 单个任务 → create_task
│  ├─ 多个任务 → batch_create_tasks
│  ├─ 子任务 → create_subtask
│  └─ 新项目 → create_project
├─ 修改
│  ├─ 更新任务属性 → update_task
│  └─ 标记完成 → complete_task
└─ 删除
   ├─ 删除任务 → delete_task
   └─ 删除项目 → delete_project
```
