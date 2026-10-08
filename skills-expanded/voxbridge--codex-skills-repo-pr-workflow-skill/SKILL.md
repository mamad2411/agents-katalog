---
name: repo-pr-workflow
description: 用于 VoxBridge 仓库的 spec 文档、功能开发、修复、重构、Pull Request 发起、PR 审核派发、PR 正文撰写、GitHub CLI/gh 操作和合并 main 流程。强制执行独立分支开发、origin 推送、PR 创建、审核子代理审查、修复、验证和合并规则。
---

# Repo PR Workflow

使用此技能保持 VoxBridge 的改动可审查，并避免在 `main` 上直接开发。

## 核心规则

- 不要在 `main` 上直接开发、修改、提交或合并。
- 保留用户已有的无关改动；不要用破坏性 Git 命令清理工作区。
- 一个分支只承载一个相对独立的 spec、功能、修复或重构任务。
- 创建 PR 前必须先把当前分支推送到 `origin`。
- PR 的目标分支必须是 `main`。
- PR 创建后，如当前环境具备子代理或线程工具，必须派发审核子代理。
- 审核通过、验证通过且 PR 状态满足合并条件前，不要合并。

## 任务开始

1. 检查仓库状态：

   ```bash
   git status --short --branch
   ```

2. 如果已经在独立工作分支上，且用户没有要求新分支，就继续使用当前分支。
3. 如果当前在 `main` 且工作区干净，先同步再创建分支：

   ```bash
   git fetch origin
   git switch main
   git pull --ff-only origin main
   git switch -c <type>/<short-description>
   ```

4. 如果当前在 `main` 且存在本地改动，切换分支前先停下来询问如何处理。
5. 如果在工作分支上发现本地无关改动，除非用户明确要求，不要 reset 或 stash；只编辑当前任务需要的文件。

分支名使用语义化前缀，例如：

- `spec/<name>`
- `feature/<name>`
- `fix/<name>`
- `refactor/<name>`

## 开发流程

1. 在当前工作分支完成用户要求的 spec、实现、修复或重构。
2. 优先运行聚焦验证；如果影响面较大，再运行更完整的验证。
3. 如果无法运行验证，在最终回复和 PR 正文中明确原因。
4. 只 stage 属于当前任务的文件。
5. 使用简洁的 conventional-style commit message 提交。
6. 推送当前分支：

   ```bash
   git push -u origin <branch>
   ```

## PR 发起

使用 `gh` 创建目标分支为 `main` 的 PR：

```bash
gh pr create --base main --head <branch> --title "<type>: <short description>" --body-file <body-file>
```

PR 标题应简洁、具体：

```txt
<type>: <short description>
```

示例：

```txt
feat: add realtime subtitle revision buffer
fix: correct audio chunk reconnection logic
docs: update implementation spec for ASR provider
refactor: split translation provider interface
```

PR 正文使用以下结构：

```md
## Summary

- 简要说明本次 PR 完成了什么
- 控制在 2 到 4 条要点内

## Motivation

说明为什么需要这个改动，它解决了什么问题，或对应哪一部分 spec / issue / task。

## Changes

按模块或文件职责列出主要改动，避免流水账。

## Validation

- pnpm test
- pnpm lint
- pnpm build
- 手动验证某个核心流程

如有未执行的验证，必须明确说明原因。

## Notes

补充审查者需要注意的内容，例如已知限制、后续工作、兼容性影响、风险点等。
```

如果本次 PR 关联 issue、任务或 spec，在正文中明确引用：

```md
Related: #123
Spec: docs/specs/realtime-subtitle.md
```

PR 正文必须让审查者快速判断：

- 本次改动的目标是什么
- 改了哪些核心文件或行为
- 如何验证改动有效
- 是否存在风险或后续工作

## 审核子代理

PR 创建后，如果当前环境提供子代理或线程工具，派发审核子代理。要求审核者通过 `gh` 检查：

- PR diff
- 提交记录
- 相关文件
- 验证结果
- 是否存在直接在 `main` 上开发的违规痕迹

审核必须重点检查：

- 是否符合 spec 或用户任务要求
- 是否存在行为回归
- 是否有明显 bug
- 是否缺失必要测试
- 是否引入不必要的复杂度
- 是否破坏现有架构边界
- PR 描述是否足够清楚
- 验证步骤是否真实、充分
- 是否存在直接在 `main` 分支开发的违规痕迹

审核结论必须明确给出以下三者之一：

```txt
approve
request changes
comment only
```

如果审核要求修改，必须回到原开发分支修复问题，推送更新后再次审核。

如果当前环境无法派发审核子代理，必须明确说明原因，并提供 PR URL 与已执行的验证结果。

## 合并

只有同时满足以下条件时才能合并：

- PR 已审核通过。
- 必要检查和本地验证均已通过。
- PR 处于可合并状态。
- 用户要求完成合并流程，或当前任务明确包含合并。

按照仓库设置使用 `gh pr merge`。合并后，回到最新 `main` 再开始下一个任务：

```bash
git switch main
git pull --ff-only origin main
```
