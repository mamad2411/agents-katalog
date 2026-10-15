---
name: x-monitor-manager
description: 管理X (Twitter) 博主监控配置。添加、删除、启用、禁用监控的博主，查看监控列表。
---

# X 博主监控管理器

管理 X (Twitter) 博主监控配置，支持添加、删除、启用、禁用监控的博主。

## 快速开始

**查看当前监控列表：**
```bash
python3 skills/x-monitor-manager/scripts/manage.py list
```

**添加博主：**
```bash
python3 skills/x-monitor-manager/scripts/manage.py add <username> [--max-tweets 20] [--enabled]
```

**删除博主：**
```bash
python3 skills/x-monitor-manager/scripts/manage.py remove <username>
```

**启用/禁用博主：**
```bash
python3 skills/x-monitor-manager/scripts/manage.py enable <username>
python3 skills/x-monitor-manager/scripts/manage.py disable <username>
```

## 配置文件

配置文件位置：`config/x-monitor.json`

```json
{
  "global": {
    "request_delay_min": 30,
    "request_delay_max": 90,
    "retry_backoff_seconds": 60,
    "data_dir": "./x_monitor_data"
  },
  "monitors": [
    {
      "username": "oran_ge",
      "enabled": true,
      "max_tweets": 20
    }
  ]
}
```

## 命令详解

### list
列出所有监控的博主及其状态。

```bash
python3 skills/x-monitor-manager/scripts/manage.py list
```

输出示例：
```
📋 当前监控的博主列表：
1. @oran_ge (enabled) - 每次检查 20 条推文
```

### add
添加新的博主到监控列表。

```bash
python3 skills/x-monitor-manager/scripts/manage.py add <username> [--max-tweets 20] [--enabled]
```

参数：
- `username`: X 用户名（不带 @）
- `--max-tweets`: 每次检查的推文数量（默认 20）
- `--enabled`: 是否启用监控（默认启用）

示例：
```bash
python3 skills/x-monitor-manager/scripts/manage.py add elonmusk --max-tweets 10
```

### remove
从监控列表中删除博主。

```bash
python3 skills/x-monitor-manager/scripts/manage.py remove <username>
```

示例：
```bash
python3 skills/x-monitor-manager/scripts/manage.py remove elonmusk
```

### enable
启用对博主的监控。

```bash
python3 skills/x-monitor-manager/scripts/manage.py enable <username>
```

### disable
禁用对博主的监控（保留在列表中但不检查）。

```bash
python3 skills/x-monitor-manager/scripts/manage.py disable <username>
```

### test
测试监控指定博主（立即运行一次检查）。

```bash
python3 skills/x-monitor-manager/scripts/manage.py test <username>
```

## 防反爬配置

在 `global` 部分可以调整防反爬参数：

- `request_delay_min`: 用户请求之间的最小延迟（秒）
- `request_delay_max`: 用户请求之间的最大延迟（秒）
- `retry_backoff_seconds`: 重试退避时间（秒）

建议值：
- 1-3 个博主：延迟 30-60 秒
- 4-6 个博主：延迟 60-120 秒
- 7+ 个博主：延迟 90-180 秒

## 使用示例

**场景1：添加多个博主**
```bash
python3 skills/x-monitor-manager/scripts/manage.py add elonmusk --max-tweets 10
python3 skills/x-monitor-manager/scripts/manage.py add naval --max-tweets 15
python3 skills/x-monitor-manager/scripts/manage.py add samaltman --max-tweets 20
```

**场景2：临时禁用某个博主**
```bash
python3 skills/x-monitor-manager/scripts/manage.py disable elonmusk
```

**场景3：测试新添加的博主**
```bash
python3 skills/x-monitor-manager/scripts/manage.py test naval
```

## 注意事项

1. **防反爬**：添加太多博主时，适当增加请求延迟
2. **初始化**：首次添加博主时，建议先运行 `test` 初始化历史记录
3. **备份**：修改配置前会自动备份到 `config/x-monitor.json.bak`

## 故障排除

**博主已存在：**
- 使用不同的用户名，或先删除再添加

**配置文件损坏：**
- 从 `config/x-monitor.json.bak` 恢复备份

**测试失败：**
- 检查用户名是否正确
- 确认 X 账号是公开的
