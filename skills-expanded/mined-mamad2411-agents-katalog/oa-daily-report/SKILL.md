---
name: oa-daily-report
description: OA 系统日报定时提醒工具，每天定时提醒填写日报（Windows 版本）
---

# OA 日报定时提醒工具（Windows 版）

每天定时提醒填写 OA 日报，并在提醒时自动打开日报填写页面。

## 快速开始

```powershell
cd skills/oa-daily-report/scripts

# 设置每日提醒（每天 17:30）
.\setup_reminder.ps1

# 查看提醒是否设置成功
schtasks /Query /TN "OA-Daily-Report-Reminder"

# 取消提醒
.\remove_reminder.ps1
```

> **注意**: 首次运行需要以**管理员身份**执行 PowerShell

## 系统要求

- Windows 10 或 Windows 11
- PowerShell 5.1 或更高版本
- 管理员权限（用于创建任务计划）

## 工作原理

1. **定时触发**: 使用 Windows 任务计划程序，每天 17:30 自动执行提醒脚本
2. **发送通知**: 显示系统气泡通知提醒填写日报
3. **自动打开**: 通知显示的同时自动打开浏览器进入日报填写页面
4. **页面地址**: https://oa.luckyxp.cn/pcc_web/#/daily-edit/create

## 脚本说明

### daily_reminder.ps1

定时提醒脚本，由任务计划程序调用。

- 发送系统气泡通知提醒填写日报
- 自动打开默认浏览器进入 OA 日报页面
- 参数可自定义：
  - `-Url`: 日报页面 URL
  - `-Title`: 通知标题
  - `-Message`: 通知内容
  - `-DisplayTime`: 通知显示时长（毫秒）

### setup_reminder.ps1

注册每日定时任务。

- 设置每天 17:30 执行提醒（可自定义时间）
- 使用 Windows 任务计划程序
- 自动检测任务是否已存在

参数：
- `-Time`: 提醒时间（默认 17:30，24小时制）
- `-TaskName`: 任务名称（默认 OA-Daily-Report-Reminder）

### remove_reminder.ps1

取消每日定时任务。

- 移除已设置的定时任务
- 完全清除提醒配置
- 自动检测任务是否存在

## 使用方法

### 设置每日提醒

```powershell
# 以管理员身份运行 PowerShell
cd skills/oa-daily-report/scripts
.\setup_reminder.ps1
```

输出示例：

```
========================================
   OA 日报提醒定时任务注册
========================================

检查文件... OK
检查现有任务... 无
正在创建任务计划...
  任务名称: OA-Daily-Report-Reminder
  执行时间: 每天 17:30
  执行脚本: C:\...\daily_reminder.ps1

========================================
  ✅ 定时任务创建成功！
========================================

任务详情:
  - 任务名称: OA-Daily-Report-Reminder
  - 执行时间: 每天 17:30
```

### 验证提醒设置

```powershell
schtasks /Query /TN "OA-Daily-Report-Reminder"
```

### 自定义提醒时间

```powershell
# 设置每天 18:00 提醒
.\setup_reminder.ps1 -Time "18:00"
```

### 取消提醒

```powershell
.\remove_reminder.ps1
```

### 手动触发提醒

```powershell
.\daily_reminder.ps1
```

会立即发送一条系统通知，并自动打开日报页面。

## 注意事项

- **管理员权限**: 创建和删除任务计划需要管理员权限
- **提醒时间**: 默认 17:30，可自定义
- **浏览器**: 使用系统默认浏览器打开日报页面
- **通知**: 显示气泡通知的同时自动打开浏览器

## 故障排除

### 提示"拒绝访问"

需要以管理员身份运行 PowerShell：
1. 右键点击 PowerShell 图标
2. 选择"以管理员身份运行"

### 通知没有显示

1. 检查系统通知设置是否启用
2. 检查是否被安全软件拦截

### 浏览器没有自动打开

1. 检查默认浏览器设置
2. 手动点击通知中的链接

## 技术参考

- 通知方式: Windows Forms NotifyIcon（气泡通知）
- 定时任务: Windows 任务计划程序 (schtasks)
- 打开浏览器: Start-Process cmdlet
