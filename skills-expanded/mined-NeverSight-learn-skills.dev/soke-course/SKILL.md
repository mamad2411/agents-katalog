---
name: soke-course
summary: 授客课程管理（课程列表/分类/课程详情/学习记录），通过 soke-cli 查询
version: 1.0.0
description: "授客课程管理：查询课程、课程分类、课程详情、学习记录。查询课程列表、课程分类、课程用户学习记录、课件列表、人脸识别记录。当用户需要查询课程信息、查看课程列表、查询学习记录、查看课程分类时使用。"
metadata:
  requires:
    bins: ["soke-cli"]
  cliHelp: "soke-cli course --help"
---

# 课程管理 (course)

**CRITICAL — 开始前 MUST 先用 Read 工具读取 [`../soke-shared/SKILL.md`](../soke-shared/SKILL.md)，其中包含认证、配置、权限处理**

## 核心概念

- **Course（课程）**: 课程实体，包含标题、分类、讲师、学时等信息，通过 `uuid` 标识
- **CourseUser（课程用户）**: 用户的课程学习记录，包含学习进度、完成状态、学习时长等，通过 `target_id` 标识
- **Category（课程分类）**: 课程分类，支持层级结构，通过 `uuid` 标识
- **Lesson（课件）**: 课程下的课件，包含视频、音频、文章、文档等类型
- **LessonLearn（课件学习记录）**: 用户的课件学习记录
- **LessonFace（人脸识别记录）**: 课件学习过程中的人脸识别记录

## 资源关系

```
Course (课程)
├── Category (课程分类)
├── Lesson (课件)
│   ├── LessonLearn (课件学习记录)
│   └── LessonFace (人脸识别记录)
└── CourseUser (课程用户学习记录)
    ├── dept_user_id (用户ID)
    ├── study_progress (学习进度)
    ├── finish_status (完成状态)
    └── study_duration (学习时长)
```

## Shortcuts（推荐优先使用）

Shortcut 是对常用操作的高级封装（`soke-cli course +<verb> [flags]`）。有 Shortcut 的操作优先使用。

| Shortcut | 说明 |
|----------|------|
| [`+list-courses`](#list-courses) | 列出课程列表，支持时间范围、分类和状态筛选 |
| [`+get-course`](#get-course) | 获取单个课程的详细信息 |
| [`+list-categories`](#list-categories) | 列出课程分类 |
| [`+list-lessons`](#list-lessons) | 列出课程下的课件列表 |
| [`+list-course-users`](#list-course-users) | 列出课程用户学习记录列表 |
| [`+get-course-user`](#get-course-user) | 获取单个用户的课程学习详情 |
| [`+list-lesson-learns`](#list-lesson-learns) | 列出课件学习记录 |
| [`+list-lesson-faces`](#list-lesson-faces) | 列出课件人脸识别记录 |

## 命令详解

### +list-courses

列出课程列表，支持按时间范围、分类和状态筛选。

**命令格式**:
```bash
soke-cli course +list-courses \
  --start-time <timestamp> \
  --end-time <timestamp> \
  [--category-id <category_id>] \
  [--is-in <0|1>] \
  [--status <0|1|2>] \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--start-time`: 课程创建开始时间（Unix时间戳，毫秒）**必需**
- `--end-time`: 课程创建结束时间（Unix时间戳，毫秒）**必需**（起始与结束时间差不超365天）
- `--category-id`: 课程分类ID（可选）
- `--is-in`: 课程来源（可选）
  - `0`: 采购课
  - `1`: 自建课
- `--status`: 课程状态（可选）
  - `0`: 未发布
  - `1`: 已发布
  - `2`: 已关闭
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `uuid`: 课程ID
- `title`: 课程标题
- `category_id`: 课程分类ID
- `certificate_id`: 关联证书ID
- `lector_id`: 关联讲师ID
- `study_type`: 学习模式（1=自由式, 2=解锁式）
- `credit`: 学分数量
- `point`: 积分数量
- `status`: 课程发布状态（-1=删除, 0=未发布, 1=已发布, 2=关闭）
- `lesson_num`: 课件数量
- `total_length`: 学时长度（单位：秒）
- `description`: 课程描述
- `pc_url`: PC端跳转链接
- `mobile_url`: 移动端跳转链接
- `create_time`: 创建时间
- `update_time`: 更新时间
- `create_dept_user_id`: 创建人ID
- `create_dept_user_name`: 创建人姓名

**示例**:
```bash
# 查询2024年的所有课程
soke-cli course +list-courses \
  --start-time 1704038400000 \
  --end-time 1735660799000

# 查询已发布的自建课
soke-cli course +list-courses \
  --start-time 1704038400000 \
  --end-time 1735660799000 \
  --is-in 1 \
  --status 1

# 查询特定分类的课程
soke-cli course +list-courses \
  --start-time 1704038400000 \
  --end-time 1735660799000 \
  --category-id "category123"
```

**权限要求**: `course:course:readonly`

---

### +get-course

获取单个课程的详细信息。

**命令格式**:
```bash
soke-cli course +get-course --uuid <course_id>
```

**参数说明**:
- `--uuid`: 课程ID **必需**

**返回字段**:
与 `+list-courses` 返回字段相同，但返回单个课程的完整详情。

**示例**:
```bash
# 查询指定课程详情
soke-cli course +get-course --uuid "course123"
```

**权限要求**: `course:course:readonly`

---

### +list-categories

列出课程分类，支持分页。

**命令格式**:
```bash
soke-cli course +list-categories \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `uuid`: 分类ID
- `title`: 分类标题
- `parent_id`: 分类父ID
- `create_time`: 创建时间

**示例**:
```bash
# 查询所有课程分类
soke-cli course +list-categories

# 分页查询
soke-cli course +list-categories --page 1 --page-size 50
```

**权限要求**: `course:category:readonly`

---

### +list-lessons

列出课程下的课件列表。

**命令格式**:
```bash
soke-cli course +list-lessons \
  --course-id <course_id> \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--course-id`: 课程ID **必需**
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `uuid`: 课件ID
- `title`: 课件标题
- `type`: 课件类型（video=视频, audio=音频, article=文章, document=文档）
- `media_id`: 关联素材库ID
- `duration`: 课件时长（单位：秒）
- `sort`: 排序号
- `status`: 状态（-1=删除, 0=未发布, 1=发布）
- `create_time`: 创建时间

**示例**:
```bash
# 查询课程的所有课件
soke-cli course +list-lessons --course-id "course123"
```

**权限要求**: `course:lesson:readonly`

---

### +list-course-users

列出课程用户学习记录列表，支持按用户ID和完成时间筛选。

**命令格式**:
```bash
soke-cli course +list-course-users \
  --course-id <course_id> \
  [--userid-list <user_ids>] \
  [--finish-start-time <timestamp>] \
  [--finish-end-time <timestamp>] \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--course-id`: 课程ID **必需**
- `--userid-list`: 用户ID列表，逗号分隔，最多100个（可选）
- `--finish-start-time`: 完成开始时间（Unix时间戳，毫秒）（可选）
- `--finish-end-time`: 完成结束时间（Unix时间戳，毫秒）（可选）
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `target_id`: 课程用户记录ID
- `dept_user_id`: 部门用户ID
- `dept_user_name`: 用户姓名
- `study_progress`: 学习进度（百分比）
- `finish_status`: 完成状态（0=未完成, 1=已完成）
- `study_duration`: 学习时长（单位：秒）
- `create_time`: 创建时间
- `update_time`: 更新时间

**示例**:
```bash
# 查询某个课程的所有用户学习记录
soke-cli course +list-course-users --course-id "course123"

# 查询特定用户的学习记录
soke-cli course +list-course-users \
  --course-id "course123" \
  --userid-list "user1,user2,user3"

# 查询某个时间段内完成的学习记录
soke-cli course +list-course-users \
  --course-id "course123" \
  --finish-start-time 1704038400000 \
  --finish-end-time 1735660799000
```

**权限要求**: `course:courseUser:readonly`

---

### +get-course-user

获取单个用户的课程学习详情。

**命令格式**:
```bash
soke-cli course +get-course-user \
  --course-id <course_id> \
  --dept-user-id <dept_user_id>
```

**参数说明**:
- `--course-id`: 课程ID **必需**
- `--dept-user-id`: 部门用户ID **必需**

**返回字段**:
与 `+list-course-users` 返回字段相同，但返回单个用户的完整学习详情。

**示例**:
```bash
# 查询张三的课程学习记录
soke-cli course +get-course-user \
  --course-id "course123" \
  --dept-user-id "user456"
```

**权限要求**: `course:courseUser:readonly`

**使用场景**:
- 当用户询问"查询某人的课程学习情况"时使用
- 需要同时提供课程ID和用户ID
- 如果只知道用户名，需要先通过 `soke-cli contact +search-user` 查询用户ID

---

### +list-lesson-learns

列出课件学习记录，支持按用户ID和时间范围筛选。

**命令格式**:
```bash
soke-cli course +list-lesson-learns \
  --lesson-id <lesson_id> \
  [--userid-list <user_ids>] \
  [--start-time <timestamp>] \
  [--end-time <timestamp>] \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--lesson-id`: 课件ID **必需**
- `--userid-list`: 用户ID列表，逗号分隔，最多100个（可选）
- `--start-time`: 学习开始时间（Unix时间戳，毫秒）（可选）
- `--end-time`: 学习结束时间（Unix时间戳，毫秒）（可选）
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `uuid`: 学习记录ID
- `dept_user_id`: 部门用户ID
- `dept_user_name`: 用户姓名
- `study_duration`: 学习时长（单位：秒）
- `finish_status`: 完成状态（0=未完成, 1=已完成）
- `create_time`: 创建时间
- `update_time`: 更新时间

**示例**:
```bash
# 查询某个课件的所有学习记录
soke-cli course +list-lesson-learns --lesson-id "lesson123"

# 查询特定用户的课件学习记录
soke-cli course +list-lesson-learns \
  --lesson-id "lesson123" \
  --userid-list "user1,user2"
```

**权限要求**: `course:lessonLearn:readonly`

---

### +list-lesson-faces

列出课件人脸识别记录，支持按用户ID和时间范围筛选。

**命令格式**:
```bash
soke-cli course +list-lesson-faces \
  --lesson-id <lesson_id> \
  [--userid-list <user_ids>] \
  [--start-time <timestamp>] \
  [--end-time <timestamp>] \
  [--page <page>] \
  [--page-size <size>]
```

**参数说明**:
- `--lesson-id`: 课件ID **必需**
- `--userid-list`: 用户ID列表，逗号分隔，最多100个（可选）
- `--start-time`: 识别开始时间（Unix时间戳，毫秒）（可选）
- `--end-time`: 识别结束时间（Unix时间戳，毫秒）（可选）
- `--page`: 页码，从1开始（默认: 1）
- `--page-size`: 每页数量，最大100（默认: 100）

**返回字段**:
- `uuid`: 识别记录ID
- `dept_user_id`: 部门用户ID
- `dept_user_name`: 用户姓名
- `face_status`: 识别状态（0=未识别, 1=识别成功, 2=识别失败）
- `face_time`: 识别时间
- `create_time`: 创建时间

**示例**:
```bash
# 查询某个课件的所有人脸识别记录
soke-cli course +list-lesson-faces --lesson-id "lesson123"

# 查询特定用户的人脸识别记录
soke-cli course +list-lesson-faces \
  --lesson-id "lesson123" \
  --userid-list "user1,user2"
```

**权限要求**: `course:lessonFace:readonly`

---

## 常见工作流

### 工作流1: 查询用户的课程学习情况

当用户询问"查询张三的课程学习情况"时：

**步骤1**: 如果只知道用户名，先查询用户ID
```bash
soke-cli contact +search-user --name "张三"
```

**步骤2**: 获取课程列表，找到目标课程ID
```bash
soke-cli course +list-courses \
  --start-time 1704038400000 \
  --end-time 1735660799000
```

**步骤3**: 查询该用户的课程学习记录
```bash
soke-cli course +get-course-user \
  --course-id <course_id> \
  --dept-user-id <dept_user_id>
```

### 工作流2: 统计课程学习完成情况

当用户询问"统计某个课程的学习完成情况"时：

**步骤1**: 获取课程用户学习记录列表
```bash
soke-cli course +list-course-users --course-id <course_id>
```

**步骤2**: 分析返回的数据
- 统计 `finish_status` 字段的分布
- 计算平均学习进度（`study_progress` 字段）
- 统计完成人数和未完成人数
- 计算平均学习时长（`study_duration` 字段）

### 工作流3: 查询某个时间段的课程

当用户询问"查询本月的课程"时：

**步骤1**: 计算时间范围（Unix时间戳，毫秒）
```bash
# 例如：2024年1月1日 00:00:00 = 1704038400000
# 2024年1月31日 23:59:59 = 1706716799000
```

**步骤2**: 查询课程列表
```bash
soke-cli course +list-courses \
  --start-time 1704038400000 \
  --end-time 1706716799000
```

### 工作流4: 查询课程的课件学习详情

当用户询问"查询某个课程的课件学习情况"时：

**步骤1**: 获取课程的课件列表
```bash
soke-cli course +list-lessons --course-id <course_id>
```

**步骤2**: 查询每个课件的学习记录
```bash
soke-cli course +list-lesson-learns --lesson-id <lesson_id>
```

**步骤3**: （可选）查询课件的人脸识别记录
```bash
soke-cli course +list-lesson-faces --lesson-id <lesson_id>
```

## 注意事项

1. **时间格式**: 所有时间参数使用Unix时间戳（毫秒），不是秒
2. **时间范围限制**: `+list-courses` 的起始与结束时间差不能超过365天
3. **分页**: 默认每页100条，最大100条，超过需要分页查询
4. **用户ID**: `dept_user_id` 是企业内的用户ID，不是用户名
5. **课程ID**: `course-id` 和 `uuid` 是同一个字段，都表示课程ID
6. **权限**: 所有操作都需要先完成认证（`soke-cli auth login`）
7. **课程状态**: 
   - `-1`: 删除
   - `0`: 未发布
   - `1`: 已发布
   - `2`: 关闭
8. **学习模式**:
   - `1`: 自由式（可以任意顺序学习）
   - `2`: 解锁式（必须按顺序学习）

## 错误处理

### 权限不足
如果遇到权限错误，参考 [`../soke-shared/SKILL.md`](../soke-shared/SKILL.md) 中的权限处理章节。

### 参数错误
使用 `--help` 查看命令参数说明：
```bash
soke-cli course +list-courses --help
```

### 数据不存在
如果查询的课程或用户不存在，API会返回空数据或错误提示。

### 时间范围超限
如果 `+list-courses` 的时间范围超过365天，API会返回错误，需要缩小时间范围。

## API 接口映射

| Shortcut | API 路径 | HTTP 方法 |
|----------|----------|-----------|
| `+list-courses` | `/course/course/list` | GET |
| `+get-course` | `/course/course/info` | GET |
| `+list-categories` | `/course/category/list` | GET |
| `+list-lessons` | `/course/lesson/list` | GET |
| `+list-course-users` | `/course/courseUser/list` | GET |
| `+get-course-user` | `/course/courseUser/info` | GET |
| `+list-lesson-learns` | `/course/lessonLearn/list` | GET |
| `+list-lesson-faces` | `/course/lessonFace/list` | GET |
