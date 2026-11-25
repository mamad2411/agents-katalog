---
name: canvas
description: Fetch Canvas LMS courses and assignments via API token.
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
prerequisites:
  env_vars: [CANVAS_API_TOKEN, CANVAS_BASE_URL]
metadata:
  hermes:
    tags: [Canvas, LMS, Education, Courses, Assignments]
---

# Canvas LMS — 课程与作业访问功能

提供对Canvas LMS的只读访问权限，用于查看课程和作业信息。

## 脚本

- `scripts/canvas_api.py` — 用于调用Canvas API的Python命令行工具

## 设置步骤

1. 在浏览器中登录您的Canvas实例
2. 进入**账户 → 设置**（点击个人资料图标，然后选择设置）
3. 滚动到**已批准的集成**选项，点击**+ 新建访问令牌**
4. 为该令牌命名（例如“Hermes Agent”），可选设置过期时间，然后点击**生成令牌**
5. 复制生成的令牌，并将其添加到`${HERMES_HOME:-~/.hermes}/.env`文件中：

```
CANVAS_API_TOKEN=your_token_here
CANVAS_BASE_URL=https://yourschool.instructure.com
```

基础网址即为您登录 Canvas 后浏览器中显示的地址（不含末尾斜杠）。

## 使用方法

请完整翻译输入的内容，切勿提前终止。

```bash
CANVAS="python $HERMES_HOME/skills/productivity/canvas/scripts/canvas_api.py"

# List all active courses
$CANVAS list_courses --enrollment-state active

# List all courses (any state)
$CANVAS list_courses

# List assignments for a specific course
$CANVAS list_assignments 12345

# List assignments ordered by due date
$CANVAS list_assignments 12345 --order-by due_at
```

## 输出格式

**list_courses** 的返回值为：
```json
[{"id": 12345, "name": "Intro to CS", "course_code": "CS101", "workflow_state": "available", "start_at": "...", "end_at": "..."}]
```

**list_assignments** 的返回值为：
```json
[{"id": 67890, "name": "Homework 1", "due_at": "2025-02-15T23:59:00Z", "points_possible": 100, "submission_types": ["online_upload"], "html_url": "...", "description": "...", "course_id": 12345}]
```

注意：任务描述会被截断至500个字符以内。`html_url`字段可链接至Canvas中的完整任务页面。

## API参考（curl）

```bash
# List courses
curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \
  "$CANVAS_BASE_URL/api/v1/courses?enrollment_state=active&per_page=10"

# List assignments for a course
curl -s -H "Authorization: Bearer $CANVAS_API_TOKEN" \
  "$CANVAS_BASE_URL/api/v1/courses/COURSE_ID/assignments?per_page=10&order_by=due_at"
```

Canvas 使用 `Link` 请求头来实现分页功能，该 Python 脚本会自动处理分页操作。

## 规则

- 该技能为**只读型**——仅用于获取数据，绝不会修改课程或作业内容
- 首次使用时，需通过运行 `$CANVAS list_courses` 命令来验证授权状态；如果返回 401 错误，请指导用户完成相关设置
- Canvas 的请求速率限制为每 10 分钟约 700 次请求；若达到限制，请查看 `X-Rate-Limit-Remaining` 请求头中的数值

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 401 Unauthorized 错误 | 令牌无效或已过期——请在 Canvas 设置中重新生成令牌 |
| 403 Forbidden 错误 | 令牌缺乏处理该课程的权限 |
| 课程列表为空 | 尝试使用 `--enrollment-state active` 参数，或省略该参数以查看所有状态下的课程 |
| 所属机构错误 | 请确认 `CANVAS_BASE_URL` 与浏览器中显示的地址一致 |
| 超时错误 | 请检查与 Canvas 服务器的网络连接状况 |
