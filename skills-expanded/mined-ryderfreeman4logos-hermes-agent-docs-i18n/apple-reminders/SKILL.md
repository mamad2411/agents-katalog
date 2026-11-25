---
name: apple-reminders
description: "Apple Reminders via remindctl: add, list, complete."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Reminders, tasks, todo, macOS, Apple]
prerequisites:
  commands: [remindctl]
---

# Apple提醒事项

您可以使用`remindctl`直接在终端中管理Apple提醒事项。这些任务会通过iCloud在所有Apple设备之间同步。

## 先决条件

- 安装有Reminders.app的**macOS**系统
- 安装工具：`brew install steipete/tap/remindctl`
- 按提示授予Reminders应用相应权限
- 查看状态：`remindctl status` / 授权使用：`remindctl authorize`

## 适用场景

- 用户提及“提醒事项”或“Reminders应用”
- 创建带有截止日期的个人待办任务，并同步到iOS设备
- 管理Apple提醒事项列表
- 用户希望任务显示在iPhone/iPad上

## 不推荐使用的场景

- 安排代理警报 → 请使用cronjob工具
- 日历事件 → 请使用Apple日历或Google日历
- 项目任务管理 → 请使用GitHub Issues、Notion等工具
- 若用户说“提醒我”但实际上是指代理警报 → 请先明确需求

## 快速参考

### 查看提醒事项

```bash
remindctl                    # Today's reminders
remindctl today              # Today
remindctl tomorrow           # Tomorrow
remindctl week               # This week
remindctl overdue            # Past due
remindctl all                # Everything
remindctl 2026-01-04         # Specific date
```

### 管理列表

```bash
remindctl list               # List all lists
remindctl list Work          # Show specific list
remindctl list Projects --create    # Create list
remindctl list Work --delete        # Delete list
```

### 创建提醒事项

```bash
remindctl add "Buy milk"
remindctl add --title "Call mom" --list Personal --due tomorrow
remindctl add --title "Meeting prep" --due "2026-02-15 09:00"
```

### 截止时间与提醒/提前提示

`--due` 和 `--alarm` 是两个不同的参数：

- `--due` 用于设置提醒的截止日期和时间。
- `--alarm` 用于设置 EventKit 的提醒/通知触发机制。对于定时截止的提醒，系统通常会在截止时间触发警报；但若用户希望提前收到提示，则需明确指定 `--alarm` 参数。

例如，设置一个在下午2点截止的提醒，并在30分钟前发送通知：

```bash
remindctl add --title "Hairdresser" --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
```

要编辑现有的提醒事项：

```bash
remindctl edit 87354 --due "2026-05-15 14:00" --alarm "2026-05-15 13:30"
```

“提醒”界面可能会根据警报时间来显示或分组相关事项，因为正是到了该时间才会触发通知。建议通过 JSON 数据进行核实，而非擅自认定截止时间发生了变动。

```bash
remindctl today --json
```

预期格式：

- `dueDate`：实际截止时间  
- `alarmDate`：通知或提前提醒时间  

Apple官方的`EKReminder`文档仅列出了与提醒功能相关的属性。而警报功能则通过remindctl工具的`--alarm`参数所调用的、继承自`EKCalendarItem`的机制来实现。  

### 完成/删除

```bash
remindctl complete 1 2 3          # Complete by ID
remindctl delete 4A83 --force     # Delete by ID
```

### 输出格式

```bash
remindctl today --json       # JSON for scripting
remindctl today --plain      # TSV format
remindctl today --quiet      # Counts only
```

## 日期格式

`--due` 参数及日期筛选器所支持的格式包括：
- `today`、`tomorrow`、`yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601 格式（`2026-01-04T12:34:56Z`）

## 规则

1. 当用户输入“提醒我”时，需明确说明是使用 Apple Reminders（同步至手机）还是通过代理程序的定时任务进行提醒。
2. 在创建提醒之前，务必确认提醒内容和截止日期。
3. 如需通过程序自动解析，可使用 `--json` 参数。
