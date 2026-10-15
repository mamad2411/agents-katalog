---
name: dev-memory-read
description: 读取 dev-memory 的入口。用户要求查看/重读记忆，或 agent 需要主动查当前仓库/分支记忆时使用。只读不写。
---

# Dev Memory Read

`dev-memory-read` 是主动读取开发记忆的入口。它解决的是“我知道要查记忆，但不知道当前 repo+branch 的权威目录在哪里”。

典型触发：

- 用户说“重新读一下记忆文件”“之前让你记的 todo”“按记忆里的最新口径”
- agent 需要核对字段、文案、源资料入口、旧结论是否更新
- SessionStart 摘要被截断，只列了文件路径，需要展开细节

## Hard Rule

不要用这些方式找 dev-memory：

- `find . -path '*dev-memory*'`
- 在当前仓库里搜 `.codex` / `.agents` / `*memory*`
- 全量 `rg` `/Users/bytedance/.dev-memory` 或 `/Users/bytedance/.codex/memories`
- 手写 shell glob 拼 `branches/feature_.../*`

先跑 `dev-memory-cli read`，让 CLI 负责：

- 按当前 repo remote/path 算 repo_key
- 按当前 Git branch 算 branch_key（例如 `feature/x` → `feature__x`）
- 只在当前 repo 的 memory 目录下查
- 输出可直接 Read 的绝对路径

## Workflow

### Step 1: 定位权威文件

```bash
npx dev-memory-cli read show --repo <repo-path>
```

cwd 已在目标 repo 时：

```bash
npx dev-memory-cli read show
```

输出重点看：

- `repo_dir`
- `branch_dir`
- `branch_exists`
- `recommended_read_order`
- `existing_branches`

如果 `branch_exists=false`，不要立刻全局搜索；先看 `existing_branches` 是否有相邻分支，必要时显式传：

```bash
npx dev-memory-cli read show --branch feature/xxx
```

### Step 2: 用关键词查当前 repo 记忆

默认只查当前 branch + repo 共享层：

```bash
npx dev-memory-cli read search \
  --repo <repo-path> \
  --query "作者信息" \
  --query "头像" \
  --query "todo"
```

需要正则时显式加 `--regex`，不要把 `|` 塞进 shell 未引用参数里：

```bash
npx dev-memory-cli read search \
  --repo <repo-path> \
  --regex \
  --query "作者信息|头像|showAvatar|todo"
```

scope：

| Scope | 用途 |
|---|---|
| `current` | 默认；当前 branch + repo 共享层 |
| `branch` | 只查当前 branch |
| `repo` | 只查 repo 共享层 |
| `all-branches` | 当前 repo 的所有活跃 branch 记忆 |
| `archived` | 当前 repo 的归档 branch 记忆 |
| `all` | 当前 repo 的 repo + 活跃 branch + 归档 branch |

只有当当前 branch 没命中、而用户明确说“之前记的”可能来自旧分支时，才扩大到：

```bash
npx dev-memory-cli read search --scope all-branches --query "..."
npx dev-memory-cli read search --scope archived --query "..."
```

## Step 3: Read 命中的文件

`search` 输出 `hits[].path` 和 `line`。命中后用文件读取工具打开对应文件，不要只看搜索行就下结论；需要读命中上下文所在 section。

推荐读取优先级：

1. `progress.md`
2. `risks.md`
3. `decisions.md`
4. `glossary.md`
5. `overview.md`
6. repo 共享层 `decisions.md` / `glossary.md` / `overview.md`

## 和其他 skill 的边界

- 只读：用 `dev-memory-read`
- 写入 / 改写 / checkpoint：用 `dev-memory-capture`
- 未分类条目整理：用 `dev-memory-setup`
- 批量清理旧条目：用 `dev-memory-tidy`
- 分支收尾归档 + 上提共享层：用 `dev-memory-graduate`

`dev-memory-read` 不会创建新记忆骨架，也不会修改任何文件。
