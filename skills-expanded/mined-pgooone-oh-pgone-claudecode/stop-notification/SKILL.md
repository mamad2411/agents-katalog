---
name: stop-notification
description: Use when configuring Claude Code to play a notification sound when it finishes responding (Stop hook audio feedback)
---

# Stop 事件音频通知

在 Claude Code 完成回复时自动播放通知音或音频文件。

## 适用场景

- 长任务执行后需要声音提醒
- 离开电脑时通过声音感知 Claude 已回复完毕
- 为多会话/多项目统一配置音频反馈

## 快速配置

### Windows

在 `~/.claude/settings.json`（全局）或 `.claude/settings.json`（项目级）中添加：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -c \"(New-Object Media.SoundPlayer 'C:\\Users\\你的名字\\.claude\\notification.wav').PlaySync()\""
          }
        ]
      }
    ]
  }
}
```

> 注意：JSON 中对反斜杠需要双写（`\\`）。

### macOS

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay ~/.claude/notification.wav"
          }
        ]
      }
    ]
  }
}
```

### Linux

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "paplay ~/.claude/notification.wav"
          }
        ]
      }
    ]
  }
}
```

## 事件说明

| 事件 | 触发时机 | 推荐钩子类型 |
|------|---------|-------------|
| `Stop` | Claude 完成响应、停止输出 | command |
| `Notification` | Claude 需要用户注意时（如权限确认） | command |
| `SessionStart` | 会话开始或恢复 | command |

最常用的是 `Stop`：每次 Claude Code 输出完一整轮回答就播放音频。

## 音频来源建议

- 使用系统自带提示音（如 macOS 的 `/System/Library/Sounds/Ping.aiff`）
- 自行准备短音频文件（推荐 .wav 格式，兼容性最好）
- 生成轻量通知音（建议 1-3 秒，避免干扰）

## 常见错误

| 错误现象 | 原因 | 修复 |
|---------|------|------|
| 没有声音 | 路径错误或音频格式不支持 | 确认文件存在、使用 .wav 格式 |
| JSON 解析失败 | Windows 路径反斜杠未转义 | 双写反斜杠 `\\` |
| Hook 未触发 | 文件不在正确的 `.claude/settings.json` 位置 | 检查全局 `~/.claude/` 或项目根目录 `.claude/` |

## 验证

1. 保存 `settings.json`
2. 与 Claude Code 进行一轮完整对话
3. 完成回复时应听到通知音
4. 按 `Ctrl+O` 进入详细模式，可查看 hook 执行日志
