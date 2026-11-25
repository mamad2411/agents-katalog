---
name: team-dashboard
description: Agent Teams监控面板，可视化展示团队通信日志。解析Claude Code将agent间通信存为JSON文件的机制，实现左侧显示团队列表、右侧展示成员收件箱功能。使用场景: 用户想查看多智能体团队的通信记录、监控agent协作状态、调试团队工作流程。触发词: "team dashboard", "团队面板", "agent通信监控", "查看团队日志"。
---

# Agent Teams Dashboard

可视化监控面板，用于展示 Claude Code 多智能体团队的通信日志。

## 快速启动

```bash
node ~/.claude/skills/team-dashboard/scripts/dashboard.js
```

然后打开浏览器访问 http://localhost:3000

## 目录结构

```
~/.claude/
├── teams/{team-name}/config.json    # 团队配置和成员信息
├── tasks/{team-name}/               # 任务状态
└── projects/{project}/              # Agent通信日志 (*.jsonl)
```

## 通信日志格式

每个 agent 的通信日志存储在 `projects/{project}/` 目录下的 `.jsonl` 文件中：

```json
{
  "sessionId": "xxx",
  "agentId": "xxx",
  "timestamp": "2025-01-20T05:34:53.692Z",
  "type": "assistant|user",
  "message": {
    "role": "assistant",
    "content": [{"type": "text", "text": "..."}]
  }
}
```

## 功能

1. **团队列表** - 左侧显示所有可用团队
2. **成员收件箱** - 右侧展示选定成员的通信记录
3. **实时刷新** - 自动检测日志文件变化
4. **消息过滤** - 按类型、时间过滤消息

## 自定义配置

编辑 `assets/config.json` 可修改：
- 监听端口
- 刷新间隔
- 日志路径
