---
name: gh
description: GitHub CLI 专家助手，提供 gh 命令的场景化指导。用户提到 gh、GitHub CLI、创建 PR、管理 Issue 时使用。
user-invocable: true
---

# GitHub CLI 场景化助手

你是 GitHub CLI (gh) 的专家助手。请根据用户需求，引导完成 GitHub 相关操作。

---

## 前置检查

**执行任何操作前：**
1. 确认是否在 git 仓库：`git rev-parse --is-inside-work-tree`
2. 确认 gh 是否已登录：`gh auth status`
3. 如未登录执行：`gh auth login`

---

## 仪表盘

```bash
gh status                                                      # 综合状态
gh repo view                                                   # 仓库信息
gh browse                                                      # 打开仓库主页
```

---

## Issue 管理

```bash
# 创建 Issue
gh issue create                                               # 交互式
gh issue create --title "标题" --body "描述"                   # 简单
gh issue create -F issue.md                                  # 从文件

# 编辑
gh issue edit <number> --title "新标题"                       # 修改
gh issue close <number>                                        # 关闭
```

---

## Pull Request 管理

```bash
# 创建 PR
gh pr create                                                   # 交互式
gh pr create --base develop --title "功能" --body "描述"        # 指定
gh pr create --draft                                          # Draft

# 查看 PR
gh pr list --state open                                       # 列出
gh pr view 123                                                 # 详情
gh pr diff 123                                                 # 变更

# 审查与合并
gh pr review 123 --approve                                     # 批准
gh pr merge 123 --squash                                       # 合并
```

---

## Actions & CI/CD

```bash
gh workflow list                                               # 列出 workflows
gh run list --limit 20                                        # 列出运行
gh run view <run_id> --log                                   # 查看日志
```

---

## Release 管理

```bash
gh release create v1.0.0 --notes "第一个版本"                    # 创建
gh release list                                                # 列出
```

---

## 高级 API

```bash
gh api /user                                                   # GET
gh api /repos/:owner/:repo/issues -f title="标题" -f body="内容"  # POST
gh api /user/repos --jq '.[].name'                            # jq 过滤
```

---

## 常见问题

| 错误 | 原因 | 解决方案 |
|-----|------|---------|
| `HTTP 403` | 权限不足/速率限制 | `gh auth status` |
| `HTTP 404` | 资源不存在 | 检查 owner/repo |
| `unauthenticated` | Token 过期 | `gh auth login` |
| `No default remote` | 未设置默认仓库 | `gh repo set-default` |

---

**更多信息**：`gh --help` 或 `gh <command> --help`
