---
name: codex
description: "Delegate coding to OpenAI Codex CLI (features, PRs)."
version: 1.0.1
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

通过 Hermes 终端将编码任务委托给 [Codex](https://github.com/openai/codex)。Codex 是 OpenAI 开发的自主编码智能体 CLI 工具。

## 适用场景

- 开发新功能
- 代码重构
- PR 审核
- 批量修复问题

使用前需准备 Codex CLI 及对应的 Git 仓库。

## 先决条件

- 已安装 Codex：`npm install -g @openai/codex`
- 已配置 OpenAI 认证信息：可以是 `OPENAI_API_KEY`，也可以是通过 Codex CLI 登录流程获得的 Codex OAuth 凭据
- **必须在 Git 仓库内运行**——Codex 不支持在仓库外部运行
- 在终端调用时需添加 `pty=true` 参数——因为 Codex 是一个交互式终端应用

对于 Hermes 本身，若设置 `model.provider: openai-codex`，则会在执行 `hermes auth add openai-codex` 后使用 `~/.hermes/auth.json` 中存储的 Hermes 管理的 Codex OAuth 凭据。而对于独立的 Codex CLI，有效的 CLI OAuth 会存储在 `~/.codex/auth.json` 文件中；因此，仅凭缺失 `OPENAI_API_KEY` 无法判定 Codex 认证存在问题。

## 单次任务处理

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

用于初步开发（Codex 需要一个 Git 仓库）：
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## 后台模式（长时间任务）

```
# Start in background with PTY
terminal(command="codex exec --sandbox workspace-write 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor progress
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks a question
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

## 主要标志参数

| 标志参数 | 效果 |
|----------|------|
| `exec "prompt"` | 单次执行，完成后立即退出 |
| `--sandbox workspace-write` (`-s`) | 启用沙箱机制，但自动批准工作区内的文件修改（推荐的自动构建模式） |
| `--dangerously-bypass-approvals-and-sandbox` | 关闭沙箱与审批流程（速度最快，风险最高；`--yolo` 仍可作为隐藏别名使用） |
| `--sandbox danger-full-access` | 关闭 Codex 沙箱机制；当主机服务上下文破坏了隔离层时十分有用 |

> **已废弃**：`--full-auto` 参数仍然可用，但实时 CLI 会提示建议改用 `--sandbox workspace-write`。

## Hermes Gateway 的注意事项

当从 Hermes gateway 或服务上下文调用 Codex CLI 时（例如由 Telegram 驱动的智能体会话），即便相同的命令在用户的交互式 shell 中可以正常运行，Codex 的 `workspace-write` 沙箱机制仍可能失效。典型的错误表现为隔离层/用户命名空间相关的问题，如 `setting up uid map: Permission denied` 或 `loopback: Failed RTM_NEWADDR: Operation not permitted`。

在这种情况下，建议优先使用：

```
codex exec --sandbox danger-full-access "<task>"
```

不妨采用进程隔离作为安全防护层：明确指定`workdir`，在启动前确保Git状态整洁，缩小任务提示范围，通过`git diff`进行审查，执行有针对性的测试，并在对重大变更进行提交之前，由人工或智能代理进行最终确认。

## PR审查

为确保审查安全，请将代码克隆到临时目录中：

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## 利用工作树并行处理问题修复

```
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --sandbox workspace-write exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --sandbox workspace-write exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## 批量代码审查

```
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review multiple PRs in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# Post results
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## 规则

1. **始终使用 `pty=true`** — Codex 是一款交互式终端应用，若没有伪终端（PTY）则会挂起。
2. **需要 Git 仓库** — Codex 无法在非 Git 目录下运行。如需临时创建环境，可使用 `mktemp -d && git init` 命令。
3. **一次性任务请使用 `exec`** — 使用 `codex exec "prompt"` 可让命令正常运行并立即退出。
4. **构建时使用 `--sandbox workspace-write`** — 该选项会自动批准在沙箱环境中的更改（此功能已不再推荐使用 `--full-auto`）。
5. **长时间任务请在后台运行** — 使用 `background=true` 参数，并通过 `process` 工具进行监控。
6. **避免干扰** — 通过 `poll`/`log` 功能进行监控，对长时间运行的任务保持耐心。
7. **并行运行也是可行的** — 如需批量处理任务，可同时启动多个 Codex 进程。
