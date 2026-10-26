---
name: cron-task
description: 定时任务助手。当用户用自然语言描述定时需求时触发，例如："明天早上9点用nb2画图发到XX群"、"每天8点提醒我喝水"、"30分钟后提醒我开会"、"每周一早上发早报"、"查看/取消定时任务"。将自然语言解析为精确调度参数，通过内置 scheduler 工具创建任务。
homepage: https://github.com/Lingyuzhou111/dow-ipad-859
metadata:
  emoji: ⏰
---

# 定时任务（cron-task）

将用户的自然语言定时需求转换为精确的 scheduler 工具调用。

---

## 触发条件

- 用户说"X点"、"X分钟后"、"明天/后天"、"每天/每周/每月"等时间词
- 用户要求在特定时间执行某项操作（画图、发消息、搜索新闻等）
- 用户查询、取消、暂停已有定时任务

---

## 核心原则

> **必须实质性调用 scheduler 工具**：严禁只凭口头回复（如"已安排"、"已清空"）而不调用工具。若是文字回复，任务根本不会真正生效！
> **直接使用内置 `scheduler` 工具**：无需调用任何外部脚本，实际执行完全交由自带 scheduler 即可。
> 本 skill 仅提供解析规范，不提供任何其它外置工具类。
---

## 时间解析规范

### 相对时间/特定日期 → `once` + 绝对时间
**重要**：除非用户明确说"每天"，否则"今日/今天"、"今晚"、"明天"均视为**一次性任务**。

| 用户说 | schedule_type | schedule_value (ISO 格式) |
|---|---|---|
| 30分钟后 | once | +30m |
| 今晚 20:00 | once | `2026-03-09T20:00:00` (今日日期) |
| 今日 15:00 | once | `2026-03-09T15:00:00` (今日日期) |
| 明天 09:00 | once | `2026-03-10T09:00:00` (次日日期) |

> **计算 ISO 时间**：必须根据当前时间 {当前时间} 准确计算 YYYY-MM-DD。**严禁**将"今日"识别为 cron 的 `* * *`（那会变成每天执行）。

### 周期性任务 → `cron` 表达式
仅当用户明确要求"每天"、"每周"、"工作日"等重复周期时使用。

| 用户说 | schedule_type | schedule_value（cron） |
|---|---|---|
| 每天早上8点 | cron | `0 8 * * *` |
| 每周一早上9点 | cron | `0 9 * * 1` |

### 固定间隔 → `interval` + 秒数

| 用户说 | schedule_type | schedule_value |
|---|---|---|
| 每隔30分钟 | interval | 1800 |
| 每隔1小时 | interval | 3600 |
| 每隔2小时 | interval | 7200 |

---

## 任务类型选择

### 固定消息（message）
用于直接发送固定文本，不需要 AI 二次处理：
- "每天早上8点发'早安'"
- "30分钟后提醒我喝水"

```
scheduler(
  action="create",
  name="早安问候",
  message="早安！",
  schedule_type="cron",
  schedule_value="0 8 * * *"
)
```

### AI 任务（ai_task）
用于需要 Agent 在执行时动态完成的复杂指令：
- "明天早上9点用 nb2 画图工具画一只可爱的小猫发到 Bot与AI绘画交流群"
- "每天早上7点搜索今日新闻并整理摘要发到群里"

```
scheduler(
  action="create",
  name="定时画图",
  ai_task="使用 nb2 画图工具画一只可爱的小猫，完成后发送图片到 Bot与AI绘画交流群",
  schedule_type="once",
  schedule_value="2026-03-10T09:00:00"
)
```

> ⚠️ **ai_task 描述要完整清晰**：包含要使用的工具名、内容描述、发送目标，确保 Agent 执行时无歧义。

---

## 任务管理操作

### 查看所有任务
```
scheduler(action="list")
```

### 查看单个任务详情
```
scheduler(action="get", task_id="任务ID")
```

### 删除特定任务
```
scheduler(action="delete", task_id="任务ID")
```

### 清空/删除全部任务
若用户要求"清空"、"删除全部定时任务"，直接使用：
```
scheduler(action="clear")
```

### 暂停/恢复任务
```
scheduler(action="disable", task_id="任务ID")
scheduler(action="enable", task_id="任务ID")
```

---

## 完整示例

**用户：** "明天早上9点 使用nb2 画图工具画一只可爱的小猫发到 Bot与AI绘画交流群"

解析步骤：
1. 时间：明天 09:00 → 计算 ISO 时间（当前日期 +1 天，时间设为 09:00:00）
2. 类型：一次性 → `once`
3. 内容：含工具调用和发送目标 → `ai_task`

调用：
```
scheduler(
  action="create",
  name="明天画猫发群",
  ai_task="使用 nb2 画图工具画一只可爱的小猫，完成后将图片发送到 Bot与AI绘画交流群",
  schedule_type="once",
  schedule_value="2026-03-10T09:00:00"
)
```

**用户：** "每周一早上7点搜索今日新闻发到群里"

调用：
```
scheduler(
  action="create",
  name="每周一早报",
  ai_task="搜索今日重要新闻，整理成简洁摘要，发送到当前群聊",
  schedule_type="cron",
  schedule_value="0 7 * * 1"
)
```

**用户：** "30分钟后提醒我喝水"

调用：
```
scheduler(
  action="create",
  name="喝水提醒",
  message="⏰ 提醒：该喝水了！",
  schedule_type="once",
  schedule_value="+30m"
)
```

---

## 注意事项

- **当前时间至关重要**：务必基于实际当前时间计算"今日"、"明天"的精确 ISO 日期。**除非有"每天"关键字，否则一律使用 `once`。**
- **目标群路由**：若用户指定了发到某个群（如"Bot测试群"），你**必须**在 `ai_task` 或 `message` 字符串中保留"发到Bot测试群"或"发送到Bot测试群"字样。后端会自动解析该名称并精准路由。
- **ai_task 描述要完整**：包含要使用的工具名、具体操作和发送目标，确保 Agent 独立执行时有足够上下文。
- **cron 表达式**：采用标准 5 段格式 `分 时 日 月 周`。
