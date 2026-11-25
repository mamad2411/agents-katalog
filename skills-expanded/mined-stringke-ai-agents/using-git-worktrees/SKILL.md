---
name: using-git-worktrees
description: 使用 git worktree 创建隔离工作空间，避免切换分支时丢失工作上下文。触发短语："worktree"、"隔离工作空间"、"隔离分支"。
allowed-tools: Read, Bash, Glob
---

# /using-git-worktrees — Git Worktree 隔离工作空间

使用 git worktree 在同一仓库中创建多个独立的工作目录，每个目录对应一个分支。

## 核心价值

- 不需要 stash 或 commit 未完成的工作就能切换任务
- 每个 worktree 是独立的文件系统目录，互不干扰
- 共享同一个 .git 仓库，不需要重新 clone

## 目录选择优先级

1. **已有 worktree**：如果目标分支的 worktree 已存在，直接使用
2. **配置路径**：如果项目或用户配置了 worktree 存放路径，使用该路径
3. **询问用户**：没有上述信息时，建议使用 `.worktrees/` 目录

## 流程

### 第一步：检查现有 worktree

```bash
git worktree list
```

如果目标分支已有 worktree，告知用户路径。

### 第二步：创建 worktree

```bash
# 基于当前分支创建新分支和 worktree
git worktree add .worktrees/{branch-name} -b {branch-name}

# 基于已有分支创建 worktree
git worktree add .worktrees/{branch-name} {branch-name}
```

### 第三步：安全验证

确认 worktree 目录被 git 忽略：

```bash
git check-ignore .worktrees/{branch-name}
```

如果未被忽略，在 `.gitignore` 中添加 `.worktrees/`。

### 第四步：项目设置

自动检测并执行项目的初始化命令：

```bash
# 检查项目类型并安装依赖
if [ -f package.json ]; then npm install; fi
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f Cargo.toml ]; then cargo build; fi
if [ -f go.mod ]; then go mod download; fi
if [ -f pom.xml ]; then mvn dependency:resolve; fi
if [ -f build.gradle ]; then ./gradlew dependencies; fi
```

### 第五步：通知用户

告知用户 worktree 的路径和切换方式：

```
Worktree 已创建：.worktrees/{branch-name}
切换到该目录：cd .worktrees/{branch-name}
```

## 清理

完成工作后（使用 /finishing-a-development-branch），清理 worktree：

```bash
git worktree remove .worktrees/{branch-name}
```

## 注意事项

- 同一个分支不能同时存在于两个 worktree 中
- worktree 中的 .git 是一个文件（指向主仓库的 .git 目录），不是目录
- 删除 worktree 目录前，先用 `git worktree remove` 清理引用
