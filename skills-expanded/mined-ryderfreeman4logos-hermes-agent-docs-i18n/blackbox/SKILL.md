---
name: blackbox
description: Delegate coding tasks to the Blackbox AI multi-model CLI.
version: 1.0.1
author: Hermes Agent (Nous Research)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Blackbox, Multi-Agent, Judge, Multi-Model]
    related_skills: [claude-code, codex, hermes-agent]
---

# Blackbox CLI

通过 Hermes 终端将编程任务委托给 [Blackbox AI](https://www.blackbox.ai/)。Blackbox 是一款多模型编程智能体 CLI 工具，它能将任务分配给多种大型语言模型（Claude、Codex、Gemini、Blackbox Pro），并通过评估机制选出最优的实现方案。

该 CLI 工具（npm 包 `@blackbox_ai/blackbox-cli`，二进制文件 `blackbox`）基于 TypeScript 开发，属于编程智能体工具（由 Gemini CLI 分支而来），支持交互式会话、非交互式单次任务处理、检查点保存、MCP 协议以及视觉模型切换功能。

## 先决条件

- 已安装 Node.js 20 及以上版本
- 已安装 Blackbox CLI：`npm install -g @blackbox_ai/blackbox-cli`（二进制文件：`blackbox`）
- 获取来自 [app.blackbox.ai/dashboard](https://app.blackbox.ai/dashboard) 的 API 密钥
- 完成配置：运行 `blackbox configure` 并输入 API 密钥
- 在终端调用时使用 `pty=true` 参数——因为 Blackbox CLI 是一款交互式终端应用

## 单次任务处理

```
terminal(command="blackbox --prompt 'Add JWT authentication with refresh tokens to the Express API'", workdir="/path/to/project", pty=true)
```

用于快速临时处理任务：
```
terminal(command="cd $(mktemp -d) && git init && blackbox --prompt 'Build a REST API for todos with SQLite'", pty=true)
```

## 后台模式（长时间任务）

对于需要数分钟才能完成的任务，建议使用后台模式，以便随时监控任务进度：

```
# Start in background with PTY
terminal(command="blackbox --prompt 'Refactor the auth module to use OAuth 2.0'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Blackbox asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## 检查点与恢复

Blackbox CLI 内置了检查点功能，可用于暂停和恢复任务：

```
# After a task completes, Blackbox shows a checkpoint tag
# Resume with a follow-up task:
terminal(command="blackbox --resume-checkpoint 'task-abc123-2026-03-06' --prompt 'Now add rate limiting to the endpoints'", workdir="~/project", pty=true)
```

## 会话命令

在交互式会话中，可使用以下命令：

| 命令 | 功能 |
|---------|------|
| `/compress` | 缩减对话历史记录以节省令牌数 |
| `/clear` | 清除历史记录并重新开始 |
| `/stats` | 查看当前令牌使用情况 |
| `Ctrl+C` | 取消当前操作 |

## PR审查

请将代码克隆到临时目录中，以避免修改工作树：

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && blackbox --prompt 'Review this PR against main. Check for bugs, security issues, and code quality.'", pty=true)
```

## 并行处理

启动多个 Blackbox 实例以执行独立的任务：

```
terminal(command="blackbox --prompt 'Fix the login bug'", workdir="/tmp/issue-1", background=true, pty=true)
terminal(command="blackbox --prompt 'Add unit tests for auth'", workdir="/tmp/issue-2", background=true, pty=true)

# Monitor all
process(action="list")
```

## 多模型模式

Blackbox的独特功能在于通过多个模型执行同一任务并对比其输出结果。您可以通过`blackbox configure`命令来指定要使用的模型——选择多个提供方即可启用“评审员”工作流，此时CLI会评估不同模型的输出并选出最优结果。

## 主要参数

| 参数 | 效果 |
|------|------|
| `--prompt "任务内容"` (`-p`) | 非交互式单次执行模式 |
| `--resume-checkpoint "标签名"` | 从已保存的检查点继续执行 |
| `--yolo` (`-y`) | 自动批准所有操作及模型切换 |
| `--vlm-switch-mode <模式>` | 图像处理模式：`once`、`session`或`persist` |
| `-c, --checkpointing` | 启用文件编辑内容的检查点保存功能 |
| `blackbox configure` | 修改设置、提供方及模型配置 |
| `blackbox update` | 将CLI升级到最新版本 |
| `blackbox mcp` | 管理MCP服务器 |
| `blackbox extensions` | 管理CLI插件 |
| `blackbox voice <操作>` / `blackbox shortcut` | 配置语音输入功能及`b`快捷键 |

## 视觉处理支持

Blackbox能够自动识别输入内容中的图像，并切换至多模态分析模式。VLM模式包括：
- `"once"` — 仅针对当前查询切换模型
- `"session"` — 整个会话期间持续切换模型
- `"persist"` — 保持使用当前模型，不进行切换

## 字符限制

您可以通过`.blackboxcli/settings.json`文件来控制字符使用量：
```json
{
  "sessionTokenLimit": 32000
}
```

## 规则

1. **始终使用 `pty=true`** — Blackbox CLI 是一款交互式终端应用，若没有伪终端（PTY）将会卡住。
2. **使用 `workdir` 参数** — 确保智能体始终在正确的目录中运行。
3. **长时间任务请后台运行** — 使用 `background=true` 参数，并通过 `process` 工具对任务进行监控。
4. **避免干扰** — 仅通过 `poll`/`log` 方式进行监控，切勿因任务执行缓慢而强制终止会话。
5. **汇报结果** — 任务完成后，检查有哪些变化，并为用户总结相关情况。
6. **积分需付费** — Blackbox 采用积分系统；多模型模式会更快消耗积分。
7. **检查前置条件** — 在尝试委托任务之前，请确认已安装 `blackbox` CLI。
