---
name: gitlink-branch
version: 1.0.0
description: "分支管理：创建、查看、删除、保护分支。当用户需要操作 GitLink 分支时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli branch --help"
---

# gitlink-branch（分支操作）

**CRITICAL — 开始前必须先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)，其中包含认证、权限处理和 API 注意事项。**
**CRITICAL — 所有 Shortcuts 在执行写入/删除操作前，务必先确认用户意图。**
**CRITICAL — GitLink 操作只能用 `gitlink-cli`。禁止用 `gh`（GitHub CLI）操作 GitLink 资源。`gh` 仅适用于 GitHub 平台。**

> **前置条件：** 先阅读 [`../gitlink-shared/SKILL.md`](../gitlink-shared/SKILL.md)

## Shortcuts

| Shortcut | 说明 | 操作类型 |
|----------|------|----------|
| `branch +list` | 列出仓库的所有分支 | Read |
| `branch +create` | 创建新分支 | ⚠️ Write Operation |
| `branch +delete` | 删除分支 | 🔴 Destructive Operation |
| `branch +protect` | 设置分支保护规则 | ⚠️ Write Operation |
| `branch +unprotect` | 移除分支保护规则 | ⚠️ Write Operation |

## 参数参考

### branch +list

| 参数 | 必填 | 说明 |
|------|------|------|
| `--owner` | 是* | 仓库所有者（可从 git remote 自动推断） |
| `--repo` | 是* | 仓库名称（可从 git remote 自动推断） |
| `--page, -p` | 否 | 页码（默认 `1`） |
| `--limit, -l` | 否 | 每页条数（默认 `20`） |
| `--format` | 否 | 输出格式：`json`/`table`/`yaml` |
| `--debug` | 否 | 启用调试输出 |

### branch +create

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name, -n` | 是 | 新分支名称 |
| `--from, -f` | 否 | 源分支或 commit（默认 `master`） |
| `--owner` | 是* | 仓库所有者（可从 git remote 自动推断） |
| `--repo` | 是* | 仓库名称（可从 git remote 自动推断） |
| `--format` | 否 | 输出格式：`json`/`table`/`yaml` |
| `--debug` | 否 | 启用调试输出 |

### branch +delete

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name, -n` | 是 | 要删除的分支名称 |
| `--owner` | 是* | 仓库所有者（可从 git remote 自动推断） |
| `--repo` | 是* | 仓库名称（可从 git remote 自动推断） |
| `--format` | 否 | 输出格式：`json`/`table`/`yaml` |
| `--debug` | 否 | 启用调试输出 |

### branch +protect

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name, -n` | 是 | 要保护的分支名称 |
| `--owner` | 是* | 仓库所有者（可从 git remote 自动推断） |
| `--repo` | 是* | 仓库名称（可从 git remote 自动推断） |
| `--format` | 否 | 输出格式：`json`/`table`/`yaml` |
| `--debug` | 否 | 启用调试输出 |

### branch +unprotect

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name, -n` | 是 | 要移除保护的分支名称 |
| `--owner` | 是* | 仓库所有者（可从 git remote 自动推断） |
| `--repo` | 是* | 仓库名称（可从 git remote 自动推断） |
| `--format` | 否 | 输出格式：`json`/`table`/`yaml` |
| `--debug` | 否 | 启用调试输出 |

> *如果在 GitLink 仓库目录下执行，`--owner` 和 `--repo` 可自动推断。

## 使用示例

```bash
# 列出当前仓库的分支
gitlink-cli branch +list

# 指定仓库并分页
gitlink-cli branch +list --owner Gitlink --repo forgeplus --page 1 --limit 10

# 输出为 JSON
gitlink-cli branch +list --format json

# 从 master 创建分支
gitlink-cli branch +create --name feature/new-feature

# 从指定分支创建
gitlink-cli branch +create --name hotfix/bug-123 --from develop

# 指定仓库创建分支
gitlink-cli branch +create --name feature/x --owner someone --repo myrepo

# 删除分支
gitlink-cli branch +delete --name feature/old-feature

# 指定仓库删除分支
gitlink-cli branch +delete --name feature/old-feature --owner someone --repo myrepo

# 保护分支
gitlink-cli branch +protect --name main

# 指定仓库保护分支
gitlink-cli branch +protect --name main --owner someone --repo myrepo

# 移除分支保护（仅简单分支名，含 / 的路径需通过 Web 操作）
gitlink-cli branch +unprotect --name main
```

## Workflow 注意事项

### branch +create（Write Operation）

> [!CAUTION]
> This is a **Write Operation** — confirm user intent.

1. 确认用户希望创建的分支名称和源分支。
2. 执行 `branch +create --name <name> --from <source>`。
3. 输出创建结果。

### branch +delete（Destructive Operation）

> [!CAUTION]
> This is a **Destructive Operation** — confirm user intent.

1. 确认用户确实希望删除该分支（此操作不可逆）。
2. 执行 `branch +delete --name <name>`。
3. 输出删除结果。

### branch +protect（Write Operation）

> [!CAUTION]
> This is a **Write Operation** — confirm user intent.

1. 确认用户希望保护的分支名称。
2. 执行 `branch +protect --name <name>`。
3. 输出设置结果。

### branch +unprotect（Write Operation）

> [!CAUTION]
> This is a **Write Operation** — confirm user intent.

1. 确认用户希望移除保护的分支名称。
2. 执行 `branch +unprotect --name <name>`。
3. 输出结果。

> **注意：** 含 `/` 的分支名（如 `feature/my-branch`）可能无法通过 CLI 解除保护（受限于 API 路由），需通过 Web 页面操作。

## References

- [gitlink-shared](../gitlink-shared/SKILL.md) — 认证、全局参数、安全规则
