---
name: using-git-worktrees
description: 在需要与当前工作区隔离的功能开发或执行实施计划前使用——创建隔离的 git worktree，支持智能目录选择和安全校验
---

# 使用 Git Worktrees

## 概述

Git worktrees 创建共享同一仓库的隔离工作区，允许同时在多个分支上工作，无需切换分支。

**核心原则：** 系统化的目录选择 + 安全校验 = 可靠的隔离。

**启动时宣告：** "我正在使用 using-git-worktrees 技能来设置隔离工作区。"

## 目录选择流程

按以下优先级依次检查：

### 1. 检查已有目录

```bash
# 按优先级检查
ls -d .worktrees 2>/dev/null     # 首选（隐藏目录）
ls -d worktrees 2>/dev/null      # 备选
```

**如果找到：** 使用该目录。如果两者都存在，优先使用 `.worktrees`。

### 2. 检查 CLAUDE.md

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

**如果指定了偏好：** 直接使用，无需询问。

### 3. 询问用户

如果没有已有目录且 CLAUDE.md 中无偏好设置：

```
未找到 worktree 目录。请问应该在哪里创建 worktrees？

1. .worktrees/（项目本地，隐藏目录）
2. ~/.config/agent/worktrees/<项目名>/（全局位置）

你更倾向哪个？
```

## 安全校验

### 项目本地目录（.worktrees 或 worktrees）

**创建 worktree 前必须验证目录已被 git 忽略：**

```bash
# 检查目录是否被忽略（支持 local、global 和 system gitignore）
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果未被忽略：**

遵循"立即修复问题"原则：

1. 在 .gitignore 中添加相应条目
2. 提交该变更
3. 继续创建 worktree

**为什么这很关键：** 防止 worktree 内容被意外提交到仓库。

### 全局目录（~/.config/agent/worktrees）

无需 .gitignore 校验——完全在项目之外。

## 创建步骤

### 1. 检测项目名称

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

### 2. 创建 Worktree

```bash
# 确定完整路径
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/agent/worktrees/*)
    path="~/.config/agent/worktrees/$project/$BRANCH_NAME"
    ;;
esac

# 创建 worktree 并新建分支
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

### 3. 运行项目初始化

自动检测并运行相应的初始化命令：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

### 4. 验证基线状态

运行测试确保 worktree 起始状态正常：

```bash
# 示例——使用项目对应的测试命令
npm test
cargo test
pytest
go test ./...
```

**如果测试失败：** 报告失败，询问是继续还是排查问题。

**如果测试通过：** 报告就绪。

### 5. 报告位置

```
Worktree 已就绪：<完整路径>
测试通过（<N> 个测试，0 个失败）
准备实施 <功能名称>
```

## 快速参考

| 场景                       | 操作                      |
| -------------------------- | ------------------------- |
| `.worktrees/` 已存在       | 使用它（校验已忽略）      |
| `worktrees/` 已存在        | 使用它（校验已忽略）      |
| 两者都存在                 | 使用 `.worktrees/`        |
| 两者都不存在               | 检查 CLAUDE.md → 询问用户 |
| 目录未被忽略               | 添加到 .gitignore + 提交  |
| 基线测试失败               | 报告失败 + 询问           |
| 无 package.json/Cargo.toml | 跳过依赖安装              |

## 常见错误

### 跳过忽略校验

- **问题：** Worktree 内容被追踪，污染 git status
- **修复：** 创建项目本地 worktree 前始终使用 `git check-ignore`

### 假定目录位置

- **问题：** 造成不一致，违反项目约定
- **修复：** 遵循优先级：已有目录 > CLAUDE.md > 询问用户

### 在测试失败时继续

- **问题：** 无法区分新引入的 bug 和原有问题
- **修复：** 报告失败，获得明确许可后再继续

### 硬编码初始化命令

- **问题：** 在使用不同工具的项目中会失败
- **修复：** 根据项目文件（package.json 等）自动检测

## 工作流示例

```
你：我正在使用 using-git-worktrees 技能来设置隔离工作区。

[检查 .worktrees/ - 已存在]
[校验忽略 - git check-ignore 确认 .worktrees/ 已被忽略]
[创建 worktree：git worktree add .worktrees/auth -b feature/auth]
[运行 npm install]
[运行 npm test - 47 个通过]

Worktree 已就绪：/Users/jesse/myproject/.worktrees/auth
测试通过（47 个测试，0 个失败）
准备实施 auth 功能
```

## 红线警告

**绝不：**

- 创建项目本地 worktree 时不校验是否已被忽略
- 跳过基线测试验证
- 在测试失败时不询问就继续
- 在不确定时假定目录位置
- 跳过 CLAUDE.md 检查

**始终：**

- 遵循目录优先级：已有目录 > CLAUDE.md > 询问用户
- 对项目本地目录校验是否已被忽略
- 自动检测并运行项目初始化
- 验证测试基线状态

## 集成

**被以下技能调用：**

- **brainstorming**（第 4 阶段）- 设计通过并进入实施时必须调用
- **subagent-driven-development** - 执行任何任务前必须调用
- **executing-plans** - 执行任何任务前必须调用
- 任何需要隔离工作区的技能

**搭配使用：**

- **finishing-a-development-branch** - 工作完成后清理时必须调用
