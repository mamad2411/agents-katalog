---
name: github
description: "GitHub via gh CLI: PRs, issues, reviews, repos, auth."
version: 2.0.0
author: Ben Barclay (benbarclay), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, gh, git, pull-requests, issues, code-review, repos, auth, ci]
    category: software-development
    related_skills: [codebase-inspection, requesting-code-review]
---

# GitHub

可通过 `gh` CLI 对 GitHub 进行端到端操作（必要时会提供 REST 接口作为备选）：包括身份认证、问题管理、Pull Request 全生命周期处理、问题转推至 Pull Request、代码审查以及仓库管理。该功能整合了之前的六项独立功能；每项工作流程都在对应的参考文档中有完整说明——在开始执行某项工作流程之前，请务必先阅读相应的参考文档，下方的内容仅起到导航作用。

## 导航指南

| 任务 | 首先阅读的文档 |
|---|---|
| 身份认证问题 / 新设备使用 / 令牌或 SSH 配置 / gh 登录 | `references/auth.md` |
| 创建、分类、标记、分配及关闭问题 | `references/issues.md` |
| 创建分支、提交代码、发起 Pull Request、监控 CI 流水线、合并代码 | `references/pr-workflow.md` |
| 将问题转化为经过验证的 Pull Request（完整处理流程） | `references/issue-to-pr.md` |
| 审查他人的 Pull Request：代码差异对比、内联评论及审核结论 | `references/code-review.md` |
| 克隆/创建/复制仓库、配置远程仓库及发布版本 | `references/repo-management.md` |

辅助资源包括：`scripts/gh-env.sh` 和 `scripts/git-credential-token.py`（用于身份认证辅助操作）、`templates/` 目录中的 Pull Request 正文模板、错误报告模板及功能需求模板，以及 `references/ci-troubleshooting.md`、`references/conventional-commits.md`、`references/github-api-cheatsheet.md`、`references(review-output-template.md)` 等文档。

## 核心规范（适用于所有工作流程）

- 每个会话执行一次预检操作：使用 `gh auth status`；如果检测失败，请首先查看 `references/auth.md`。
- 尽量优先使用 `gh` 命令而非原始 REST 接口；仅在没有对应命令的接口时才使用 `gh api`（相关列表见操作指南）。
- 未经亲自检查 `gh pr checks`，切勿宣称 CI 测试已通过；未核实 `state,mergedAt` 状态，也切勿声称代码已合并。
- 写作前请先查看完整上下文：使用 `gh issue view --comments` / `gh pr view --comments`——决策信息存在于讨论帖中，而非标题里。
- 创建任何内容之前，请先检查是否存在重复项：使用 `gh pr list --search` / `gh issue list --search`。

## 验证方式

- 工作流自身的参考文件会定义该任务的完成标准。
- 通用原则：所有关于远程状态（CI 测试、代码合并、版本发布、问题状态等）的判断，都必须基于最新的 `gh` 命令查询结果，绝不能依赖内存中的旧数据。
