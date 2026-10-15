---
name: soke-exam
summary: 授客考试管理（考试列表/分类/考试用户成绩/详情），通过 soke-cli 查询
version: 1.0.0
description: "授客考试管理：查询考试、考试用户和成绩。查询考试列表、考试分类、考试用户成绩、考试详情。当用户需要查询考试成绩、查看考试列表、查询考试用户信息、查看考试分类时使用。"
metadata:
  requires:
    bins: ["soke-cli"]
  cliHelp: "soke-cli exam --help"
---

# 考试管理 (exam)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../soke-shared/SKILL.md`](../soke-shared/SKILL.md)，其中包含认证、配置、权限处理**

## 核心概念

- **Exam（考试）**: 考试实体，包含标题、时间范围、状态等信息，通过 `uuid` 标识
- **ExamUser（考试用户）**: 用户的考试记录，包含成绩、状态、答题时间等，通过 `target_id` 标识
- **Category（考试分类）**: 考试分类，支持层级结构，通过 `uuid` 标识
- **DeptUser（部门用户）**: 企业内的用户，通过 `dept_user_id` 标识

## 资源关系

```
Exam (考试)
├── ExamUser (考试用户记录)
│   ├── dept_user_id (用户ID)
│   ├── score (成绩)
│   ├── exam_status (考试状态)
│   └── submit_time (提交时间)
└── Category (考试分类)
```

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`soke-cli exam +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+list-exams`](#list-exams) | 列出考试列表，支持时间范围和状态筛选 |
| [`+list-exam-users`](#list-exam-users) | 列出考试用户成绩列表，支持用户筛选和时间范围 |
| [`+get-exam-user`](#get-exam-user) | 获取单个考试用户的详细成绩信息 |
| [`+list-categories`](#list-categories) | 列出考试分类 |

## 命令详解

### +list-exams

列出考试列表，支持按时间范围和状态筛选。

**命令格式**:
```bash
soke-cli exam +list-exams \
  --start-time <timestamp> \
  --end-time <timestamp> \
  [--status <status>] \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--start-time`: 开始时间（Unix时间戳，毫秒）**必需**
- `--end-time`: 结束时间（Unix时间戳，毫秒）**必需**
- `--status`: 考试状态（可选）
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `uuid`: 考试ID
- `title`: 考试标题
- `start_time`: 开始时间
- `end_time`: 结束时间
- `status`: 考试状态

**示例**:
```bash
# 查询2023年的所有考试
soke-cli exam +list-exams \
  --start-time 1672502400000 \
  --end-time 1704038400000

# 查询进行中的考试
soke-cli exam +list-exams \
  --start-time 1672502400000 \
  --end-time 1704038400000 \
  --status "进行中"
```

**权限要求**: `exam:exam:readonly`

---

### +list-exam-users

列出考试用户成绩列表，支持按用户ID和完成时间筛选。

**命令格式**:
```bash
soke-cli exam +list-exam-users \
  --exam-id <exam_id> \
  [--userid-list <user_ids>] \
  [--finish-start-time <timestamp>] \
  [--finish-end-time <timestamp>] \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--exam-id`: 考试ID **必需**
- `--userid-list`: 用户ID列表，逗号分隔，最多100个（可选）
- `--finish-start-time`: 完成开始时间（Unix时间戳，毫秒）（可选）
- `--finish-end-time`: 完成结束时间（Unix时间戳，毫秒）（可选）
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `target_id`: 考试用户记录ID
- `dept_user_id`: 部门用户ID
- `score`: 成绩
- `exam_status`: 考试状态
- `create_time`: 创建时间

**示例**:
```bash
# 查询某个考试的所有用户成绩
soke-cli exam +list-exam-users --exam-id exam123

# 查询特定用户的成绩
soke-cli exam +list-exam-users \
  --exam-id exam123 \
  --userid-list "user1,user2,user3"

# 查询某个时间段内完成的考试
soke-cli exam +list-exam-users \
  --exam-id exam123 \
  --finish-start-time 1672502400000 \
  --finish-end-time 1704038400000
```

**权限要求**: `exam:examUser:readonly`

---

### +get-exam-user

获取单个考试用户的详细成绩信息，包含答题详情。

**命令格式**:
```bash
soke-cli exam +get-exam-user \
  --exam-id <exam_id> \
  --dept-user-id <dept_user_id>
```

**参数说明**:
- `--exam-id`: 考试ID **必需**
- `--dept-user-id`: 部门用户ID **必需**

**返回字段**:
- `target_id`: 考试用户记录ID
- `target_title`: 考试标题
- `dept_user_id`: 部门用户ID
- `score`: 成绩
- `exam_status`: 考试状态
- `start_time`: 开始时间
- `submit_time`: 提交时间
- `question_count`: 题目数量
- `create_time`: 创建时间

**示例**:
```bash
# 查询张三的考试成绩
soke-cli exam +get-exam-user \
  --exam-id exam123 \
  --dept-user-id user456
```

**权限要求**: `exam:examUser:readonly`

**使用场景**:
- 当用户询问"查询某人的考试成绩"时使用
- 需要同时提供考试ID和用户ID
- 如果只知道用户名，需要先通过 `soke-cli contact +search-user` 查询用户ID

---

### +list-categories

列出考试分类，支持分页。

**命令格式**:
```bash
soke-cli exam +list-categories \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `uuid`: 分类ID
- `title`: 分类名称
- `parent_id`: 父分类ID
- `create_time`: 创建时间

**示例**:
```bash
# 查询所有考试分类
soke-cli exam +list-categories

# 分页查询
soke-cli exam +list-categories --page 1 --page-size 20
```

**权限要求**: `exam:category:readonly`

## 通用API调用

如果Shortcuts不满足需求，可以使用通用API调用：

```bash
soke-cli api <METHOD> <path> [--params <json>]
```

示例：
```bash
soke-cli api GET /exam/exam/list --params '{"start_time":"1672502400000","end_time":"1704038400000"}'
```

## 权限表

| 操作 | 所需权限 |
|------|---------|
| `+list-exams` | `exam:exam:readonly` |
| `+list-exam-users` | `exam:examUser:readonly` |
| `+get-exam-user` | `exam:examUser:readonly` |
| `+list-categories` | `exam:category:readonly` |

## 常见工作流

### 工作流1: 查询用户考试成绩

当用户询问"查询张三的考试成绩"时：

**步骤1**: 如果只知道用户名，先查询用户ID
```bash
soke-cli contact +search-user --name "张三"
```

**步骤2**: 获取考试列表，找到目标考试ID
```bash
soke-cli exam +list-exams \
  --start-time 1672502400000 \
  --end-time 1704038400000
```

**步骤3**: 查询该用户的考试成绩
```bash
soke-cli exam +get-exam-user \
  --exam-id <exam_id> \
  --dept-user-id <dept_user_id>
```

### 工作流2: 统计考试完成情况

当用户询问"统计某个考试的完成情况"时：

**步骤1**: 获取考试用户列表
```bash
soke-cli exam +list-exam-users --exam-id <exam_id>
```

**步骤2**: 分析返回的数据
- 统计 `exam_status` 字段的分布
- 计算平均分（`score` 字段）
- 统计完成人数

### 工作流3: 查询某个时间段的考试

当用户询问"查询本月的考试"时：

**步骤1**: 计算时间范围（Unix时间戳，毫秒）
```bash
# 例如：2024年1月1日 00:00:00 = 1704038400000
# 2024年1月31日 23:59:59 = 1706716799000
```

**步骤2**: 查询考试列表
```bash
soke-cli exam +list-exams \
  --start-time 1704038400000 \
  --end-time 1706716799000
```

## 注意事项

1. **时间格式**: 所有时间参数使用Unix时间戳（毫秒），不是秒
2. **分页**: 默认每页100条，最大100条，超过需要分页查询
3. **用户ID**: `dept_user_id` 是企业内的用户ID，不是用户名
4. **考试ID**: `exam-id` 和 `uuid` 是同一个字段，都表示考试ID
5. **权限**: 所有操作都需要先完成认证（`soke-cli auth login`）

## 错误处理

### 权限不足
如果遇到权限错误，参考 [`../soke-shared/SKILL.md`](../soke-shared/SKILL.md) 中的权限处理章节。

### 参数错误
使用 `--help` 查看命令参数说明：
```bash
soke-cli exam +get-exam-user --help
```

### 数据不存在
如果查询的考试或用户不存在，API会返回空数据或错误提示。
