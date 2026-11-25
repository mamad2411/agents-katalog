---
name: opencode
description: "Delegate coding to OpenCode CLI (features, PR review)."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, OpenCode, Autonomous, Refactoring, Code-Review]
    related_skills: [claude-code, codex, hermes-agent]
---

# OpenCode CLI

[OpenCode](https://opencode.ai) 是由 Hermes 终端/进程工具所调度的自主编程工具。它是一款与具体提供方无关的开源 AI 编程智能体，同时支持 TUI 和 CLI 模式。

## 适用场景

- 用户明确要求使用 OpenCode
- 需要外部编程智能体来实现、重构或审查代码
- 需要能够进行长时间运行并随时检查进度的编程会话
- 希望在独立的工作目录/工作树中并行执行任务

## 先决条件

- 已安装 OpenCode：`npm i -g opencode-ai@latest` 或 `brew install anomalyco/tap/opencode`
- 已完成身份认证：执行 `opencode auth login`，或设置相关提供方环境变量（如 OPENROUTER_API_KEY 等）
- 验证配置：执行 `opencode auth list` 后应至少显示一个可用提供方
- 用于处理代码任务的 Git 仓库（推荐）
- 如需交互式 TUI 体验，请设置 `pty=true`

## 二进制版本问题（重要）

不同的Shell环境可能会加载不同的 OpenCode 二进制文件。如果您的终端与Hermes之间的行为存在差异，请检查：

```
terminal(command="which -a opencode")
terminal(command="opencode --version")
```

如有需要，可指定明确的二进制文件路径：

```
terminal(command="$HOME/.opencode/bin/opencode run '...'", workdir="~/project", pty=true)
```

## 单次任务

对于有边界且非交互式的任务，请使用 `opencode run` 命令：

```
terminal(command="opencode run 'Add retry logic to API calls and update tests'", workdir="~/project")
```

使用 `-f` 选项附加上下文文件：

```
terminal(command="opencode run 'Review this config for security issues' -f config.yaml -f .env.example", workdir="~/project")
```

使用 `--thinking` 参数即可展示模型的思维过程：

```
terminal(command="opencode run 'Debug why tests fail in CI' --thinking", workdir="~/project")
```

强制使用特定模型：

```
terminal(command="opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4", workdir="~/project")
```

## 交互式会话（后台模式）

对于需要多次交互才能完成的迭代性任务，可在后台启动 TUI：

```
terminal(command="opencode", workdir="~/project", background=true, pty=true)
# Returns session_id

# Send a prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow and add tests")

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send follow-up input
process(action="submit", session_id="<id>", data="Now add error handling for token expiry")

# Exit cleanly — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# Or just kill the process
process(action="kill", session_id="<id>")
```

**重要提示：** 请勿使用 `/exit` 命令——该命令并非有效的 OpenCode 命令，反而会弹出代理选择器对话框。如需退出，请使用 Ctrl+C (`\x03`) 或 `process(action="kill")`。

### TUI 键绑定

| 键 | 操作 |
|-----|------|
| `Enter` | 提交消息（如需可按两次） |
| `Tab` | 在不同代理（构建/规划）之间切换 |
| `Ctrl+P` | 打开命令面板 |
| `Ctrl+X L` | 切换会话 |
| `Ctrl+X M` | 切换模型 |
| `Ctrl+X N` | 新建会话 |
| `Ctrl+X E` | 打开编辑器 |
| `Ctrl+C` | 退出 OpenCode |

### 恢复会话

退出后，OpenCode 会显示会话 ID。可通过以下方式恢复会话：

```
terminal(command="opencode -c", workdir="~/project", background=true, pty=true)  # Continue last session
terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true)  # Specific session
```

## 常用参数

| 参数 | 用途 |
|------|-----|
| `run 'prompt'` | 单次执行后立即退出 |
| `--continue` / `-c` | 继续上一次的 OpenCode 会话 |
| `--session <id>` / `-s` | 继续特定的会话 |
| `--agent <name>` | 选择 OpenCode 智能体（build 或 plan） |
| `--model provider/model` | 强制指定模型 |
| `--format json` | 生成机器可读的输出/事件 |
| `--file <path>` / `-f` | 将文件附加到消息中 |
| `--thinking` | 显示模型的思考过程 |
| `--variant <level>` | 设置推理强度（高、最大、最低） |
| `--title <name>` | 为会话命名 |
| `--attach <url>` | 连接到正在运行的 opencode 服务器 |

## 操作步骤

1. 验证工具是否准备就绪：
   - `terminal(command="opencode --version")`
   - `terminal(command="opencode auth list")`
2. 对于有限步骤的任务，使用 `opencode run '...'`（无需伪终端）。
3. 对于需要迭代处理的任务，以 `background=true, pty=true` 参数启动 `opencode`。
4. 使用 `process(action="poll"|"log")` 监控长时间运行的任务。
5. 若 OpenCode 请求输入，通过 `process(action="submit", ...)` 进行响应。
6. 通过 `process(action="write", data="\x03")` 或 `process(action="kill")` 退出程序。
7. 向用户总结文件更改情况、测试结果及后续步骤。

## PR 审核工作流程

OpenCode 内置了 PR 相关命令：

```
terminal(command="opencode pr 42", workdir="~/project", pty=true)
```

或可在独立的临时克隆版本中进行查看，以实现隔离：

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review this PR vs main. Report bugs, security risks, test gaps, and style issues.' -f $(git diff origin/main --name-only | head -20 | tr '\n' ' ')", pty=true)
```

## 并行工作模式

通过使用独立的工作目录/工作树来避免冲突：

```
terminal(command="opencode run 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="opencode run 'Add parser regression tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

## 会话与成本管理

列出历史会话：

```
terminal(command="opencode session list")
```

查看令牌使用情况与费用：

```
terminal(command="opencode stats")
terminal(command="opencode stats --days 7 --models anthropic/claude-sonnet-4")
```

## 常见问题

- 交互式 `opencode`（TUI）会话需要设置 `pty=true`。而 `opencode run` 命令则无需该参数。
- `/exit` 不是有效命令——它只会打开代理选择器。如需退出 TUI，请使用 Ctrl+C。
- PATH 路径配置错误可能导致加载错误的 OpenCode 可执行文件或模型配置。
- 若发现 OpenCode 卡住，建议在终止进程前先查看日志：
  - `process(action="log", session_id="<id>")`
- 应避免在多个并行运行的 OpenCode 会话之间共享同一个工作目录。
- 在 TUI 环境中，可能需要按两次 Enter 才能提交内容（一次用于确认输入文本，一次用于发送）。

## 验证

冒烟测试：

```
terminal(command="opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'")
```

成功标准：  
- 输出结果中包含 `OPENCODE_SMOKE_OK`  
- 命令执行过程中无提供方或模型相关错误  
- 对于代码处理任务：预期文件已修改且测试通过  

## 规则  

1. 对于一次性自动化任务，优先使用 `opencode run` —— 它更为简单，且无需伪终端。  
2. 仅当需要迭代处理时才使用交互式后台模式。  
3. OpenCode 会话的范围始终应限制在单个仓库/工作目录内。  
4. 对于耗时较长的任务，需通过 `process` 日志提供进度更新。  
5. 需汇报具体的执行结果（如文件修改情况、测试结果及剩余风险）。  
6. 应使用 Ctrl+C 或 kill 命令结束交互式会话，严禁使用 `/exit`。
