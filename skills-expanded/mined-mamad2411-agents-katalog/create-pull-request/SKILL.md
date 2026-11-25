---
name: create-pull-request
description: >-
  在本仓库用便携 gh + git credential 令牌创建 GitHub Pull Request。用户要求提交
  PR、创建 pull request、开 PR、push 并创建 PR 时使用。
metadata:
  version: "1.2.0"
---

# 创建 Pull Request

## 目的

把当前功能分支推送到 `origin`，并向 `main` 创建 Pull Request。本机实测可用路径：便携 `gh` + `git credential fill` 注入 `GH_TOKEN`。

## 何时使用

用户要求提交 PR、创建 PR、开 PR、push 并创建 PR。

## 约束

- 目标分支固定为 `main`。
- 当前分支不能是 `main`。
- 需要先有对应提交；用户未要求时不要擅自 `git commit`。
- 禁止在回复或日志中输出 token；`GH_TOKEN` 用完即删。

## 步骤

### 1. 收集状态（并行）

```powershell
git status --short --branch
git diff
git log --oneline origin/main..HEAD
git diff origin/main...HEAD
```

根据 `origin/main..HEAD` 的提交整理 PR 标题与正文。

### 2. 推送

```powershell
git push -u origin HEAD
```

### 3. 写文案

- 标题：Conventional Commits 中文，与主提交一致。
- 正文：

```markdown
## Summary
- <1-3 条>

## Test plan
- [ ] <验证步骤>
```

### 4. 创建 PR

直接跑脚本（内部完成：解析 `origin` 仓库、准备 `gh.exe`、取 credential、创建 PR、清除 token）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .cursor/skills/create-pull-request/scripts/create-pr.ps1 `
  -Title 'feat(scope): 中文摘要' `
  -Body @"
## Summary
- ...

## Test plan
- [ ] ...
"@
```

`Head` / `Base` / `Repo` 可省略：默认当前分支、`main`、从 `origin` 解析。

脚本成功时 stdout 会打印 PR URL。把该 URL 回复给用户即可。
