---
name: finishing-a-development-branch
description: 完成开发分支的收尾工作。四选项决策树：合并、创建 PR、保留、丢弃。触发短语："完成分支"、"合并"、"提交 PR"。
allowed-tools: Read, Bash, Glob, Grep
---

# /finishing-a-development-branch — 完成开发分支

## 流程

### 第一步：验证状态

```bash
# 当前分支
git branch --show-current

# 确认所有测试通过
# [运行项目的测试命令]

# 查看变更统计
git log main..HEAD --oneline
git diff main...HEAD --stat
```

如果有未提交的改动，先提交。如果测试未通过，先修复。

### 第二步：呈现选项

向用户呈现四个选项：

```
分支收尾选项：

1. 合并到 main — 直接合并（适合小改动、个人项目）
2. 创建 PR   — 推送并创建 Pull Request（适合团队协作）
3. 保留分支   — 暂不处理（适合未完成的工作）
4. 丢弃分支   — 删除分支和所有改动（适合废弃的实验）

请选择：
```

### 第三步：执行选择

#### 选项 1：合并到 main

```bash
git checkout main
git merge --no-ff {branch-name}
```

合并后确认测试通过。

#### 选项 2：创建 PR

```bash
git push -u origin {branch-name}
gh pr create --title "{标题}" --body "{描述}"
```

PR 描述应包含：
- 变更摘要
- 相关的 spec.md 或 plan.md 链接
- 测试计划

#### 选项 3：保留分支

告知用户分支名和恢复方式。无需操作。

#### 选项 4：丢弃分支

**此操作不可逆，执行前必须确认。**

```bash
git checkout main
git branch -D {branch-name}
```

### 第四步：清理 worktree

如果分支关联了 worktree，清理它：

```bash
git worktree remove .worktrees/{branch-name}
```

### 第五步：确认完成

```
分支 {branch-name} 已 [合并/PR 已创建/保留/丢弃]。
当前在 main 分支。
```
