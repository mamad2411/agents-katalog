---
name: renthub-commit
description: 在用户要求 commit、生成 commit message、提交代码或暂存区提交时使用。
targets:
  - '*'
---
# 提交规范（renthub-commit）

## 概述

按 RentHub Conventional Commits 起草**中文**提交说明；用户确认后再 `git commit`。

## 输出（强制）

- **起草阶段**：只输出 commit message 原文（含可选 body），无前言、无解释、无列表、无署名。
- **提交成功后**：只输出一行 `<hash> <message 首行>`。
- **禁止**：改动摘要、规则复述、`git push` 提醒、AI 署名。

## 流程

1. `git status`、`git diff --staged`、`git diff`
2. 多目的则拆分暂存，逐个起草
3. 生成 message（见下），**调用 AskQuestion** 让用户选择：
   - 接受并提交
   - 接受，不提交
   - 需要修改
   - 提问
4. 仅当用户选择「接受并提交」时执行 `git commit`

## Message 格式

```text
<type>(<scope>): <subject>

<body 可选>
```

- `type`：`feat|fix|refactor|chore|docs|test|style`
- `subject`：**中文**，动词开头、简洁
- `body`：**中文**，只写「为什么」，不重复 diff

PowerShell 多行：

```powershell
git commit -m "type(scope): subject`n`nbody"
```

## 速查

| 项 | 要求 |
|----|------|
| 粒度 | 一目的一 commit |
| subject | 中文、动词、具体 |
| body | 可选，只解释原因 |
| 自动 commit | 禁止（须 AskQuestion 确认） |

## 常见错误

| 错误 | 修法 |
|------|------|
| description/规则当输出 | 只输出 message |
| 未确认就 commit | 先 AskQuestion |
| subject 空泛（「更新代码」） | 写清做了什么 |
| body 复述 diff | 只写动机 |
