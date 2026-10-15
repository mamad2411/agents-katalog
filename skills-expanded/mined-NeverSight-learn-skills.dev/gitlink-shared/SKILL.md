---
name: gitlink-shared
version: 1.0.0
description: "gitlink-cli 共享基础：认证登录、全局参数、错误处理、安全规则。当用户首次使用 gitlink-cli、遇到认证错误、权限不足时触发。"
metadata:
  requires:
    bins: ["gitlink-cli"]
  cliHelp: "gitlink-cli --help"
---

# gitlink-cli 共享规则

本技能指导你如何通过 gitlink-cli 操作 GitLink 平台资源。

## 认证

### 登录方式

```bash
# 方式 1：用户名密码登录（交互式）
gitlink-cli auth login

# 方式 2：粘贴已有 Token
gitlink-cli auth login --token

# 查看登录状态
gitlink-cli auth status

# 退出登录
gitlink-cli auth logout
```

### Token 说明

- GitLink Token 有效期 **7 天**，过期需重新登录
- Token 存储在 OS Keychain（macOS Keychain / Linux Secret Service / Windows Credential Manager）
- Fallback 存储：`~/.config/gitlink-cli/credentials`

### 认证错误处理

遇到 `401` 错误时：
```bash
# 引导用户重新登录
gitlink-cli auth login
```

遇到 `403` 错误时：
- 确认用户是否有对应资源的权限
- 确认 owner/repo 是否正确

## 全局参数

| 参数 | 说明 |
|------|------|
| `--owner` | 仓库所有者（可从 git remote 自动解析） |
| `--repo` | 仓库名称（可从 git remote 自动解析） |
| `--format` | 输出格式：json / table / yaml（AI 场景建议 json） |
| `--debug` | 启用调试输出 |

### 上下文自动解析

在 git 仓库目录下，`--owner` 和 `--repo` 可自动从 `git remote origin` 解析：
- HTTPS: `https://www.gitlink.org.cn/owner/repo.git`
- SSH: `git@www.gitlink.org.cn:owner/repo.git`

## 输出格式

所有命令输出遵循统一 Envelope 格式：

```json
{
  "ok": true,
  "data": { ... },
  "meta": { "page": 1, "limit": 20, "total_count": 100 }
}
```

错误格式：
```json
{
  "ok": false,
  "error": { "code": 401, "message": "请登录后再操作", "suggestion": "请先运行 gitlink-cli auth login 登录" }
}
```

**AI 场景建议**：始终使用 `--format json` 以便解析输出。

## 三层命令体系

| 层级 | 格式 | 示例 | 适用场景 |
|------|------|------|----------|
| Shortcuts | `gitlink-cli <domain> +<verb>` | `gitlink-cli repo +info` | 高频操作，推荐优先使用 |
| Raw API | `gitlink-cli api <METHOD> <PATH>` | `gitlink-cli api GET /users/me` | Shortcuts 未覆盖的接口 |

## GitLink API 注意事项

以下是实际测试中发现的 API 行为特殊性，使用时务必注意：

| 问题 | 说明 | 影响 |
|------|------|------|
| Issue 创建需要 `done_ratio` | 创建 Issue 时必须包含 `done_ratio: 0`，否则数据库报错 | `issue +create` 已内置处理 |
| Issue 更新需保留 `subject`/`description` | 任何 Issue 更新（包括只改状态）都应带上当前 `subject` 和 `description`，否则可能清空描述 | `issue +update`/`issue +close` 已内置处理，Raw API 需先 GET 再提交 |
| Release 查看需要 `version_id` | `release +view` 必须用 `version_id`（从 `release +list` 获取），不能用 tag_name | tag_name 会返回 HTML 页面 |
| Release 删除需要 `version_id` | `release +delete -i <version_id>` 正常工作 | 已验证通过 |
| 分支操作需要 `/v1/` 前缀 | 分支的 create/delete/list 端点使用 `/v1/:owner/:repo/branches` | 已内置处理 |
| Branch 删除 API 不可用 | `DELETE /v1/:owner/:repo/branches/:name` 始终返回"分支不存在" | GitLink 平台 Bug，暂时无法通过 API 删除分支 |
| Create File 需要 base64 | `POST /:owner/:repo/create_file` 的 `content` 字段必须 base64 编码 | 不编码会返回"文件已存在"错误 |
| Update File 需要 SHA | `PUT /:owner/:repo/update_file` 需要 `sha` 参数，通过 `sub_entries` 接口获取 | 见下方文件操作说明 |
| PR 合并需要 `do` 参数 | `pr +merge` 需传 `do` 字段指定合并方式（merge/rebase/squash） | `pr +merge` 已内置处理 |
| PR 列表 state 过滤 | `--state` 参数仅影响统计计数，返回列表可能包含所有状态 | 需通过 `pull_request_status` 字段客户端过滤：0=open, 1=merged, 2=closed |
| PR 创建需要代码差异 | 分支内容必须与目标分支不同，否则拒绝创建 | 需要先在分支上有实际提交 |

## 文件操作 API

通过 Raw API 在分支上创建或修改文件（PR 工作流的前置操作）：

### 创建文件

```bash
# content 必须 base64 编码
CONTENT=$(echo -n "文件内容" | base64)
gitlink-cli api POST /:owner/:repo/create_file --body '{
  "filepath": "path/to/file.md",
  "content": "<base64编码>",
  "branch": "feature-branch",
  "message": "add new file"
}'
```

### 更新文件

```bash
# Step 1: 获取文件 SHA
gitlink-cli api GET /:owner/:repo/sub_entries --query 'filepath=path/to/file.md&ref=branch-name'
# 从返回的 entries.sha 获取 SHA 值

# Step 2: 更新文件（content 必须 base64 编码）
gitlink-cli api PUT /:owner/:repo/update_file --body '{
  "filepath": "path/to/file.md",
  "content": "<base64编码>",
  "sha": "<从sub_entries获取的sha>",
  "branch": "feature-branch",
  "message": "update file"
}'
```

### 删除文件

```bash
# 需要文件 SHA
gitlink-cli api DELETE /:owner/:repo/delete_file --body '{
  "filepath": "path/to/file.md",
  "sha": "<sha>",
  "branch": "master",
  "message": "delete file"
}'
```

## 分支约定

GitLink 和 GitHub 使用不同的主分支名称：

| 平台 | 主分支 | 说明 |
|------|--------|------|
| GitHub | `main` | GitHub 默认主分支 |
| GitLink | `master` | GitLink 默认主分支 |

**自动分支映射**：

gitlink-cli 在与 GitLink 交互时会自动处理分支映射：
- 当 push 到 GitLink 时，自动将 `main` 映射到 `master`
- 当从 GitLink pull 时，自动将 `master` 映射到 `main`

**本地 Git 操作**：

如果直接使用 `git push` 命令，需要手动指定分支映射：

```bash
# 在本地 main 分支工作
git checkout main
git commit -m "feat: new feature"

# 直接 push 到 GitLink 的 master 分支
git push gitlink main:master
# 或配置 git remote 的 push refspec
git config remote.gitlink.push refs/heads/main:refs/heads/master
git push gitlink
```

**使用 gitlink-cli**：

```bash
# 在本地 main 分支工作
git checkout main
git commit -m "feat: new feature"

# Push 到 GitLink 时自动映射到 master
gitlink-cli repo +push
# 实际推送到 GitLink 的 master 分支
```

## 安全规则

- **禁止输出 Token** 到终端明文
- **写入/删除操作前必须确认用户意图**
- 危险操作（删除仓库、删除分支等）需二次确认

## ⚠️ PR 协作流程（Fork-based）

向他人仓库（非自己拥有的仓库）提交 PR 时，**必须走 Fork 流程**，禁止直接往主仓库推分支。

### 正确流程

```bash
# 1. Fork 目标仓库（在 GitLink 网页或 CLI 操作）
gitlink-cli repo +fork --owner TargetOrg --repo target-repo

# 2. Clone 自己的 Fork
git clone https://www.gitlink.org.cn/MyUser/target-repo.git
cd target-repo

# 3. 添加 upstream remote
git remote add upstream https://www.gitlink.org.cn/TargetOrg/target-repo.git

# 4. 创建分支、修改、提交
git checkout -b fix/my-change
# ... 修改文件 ...
git add -A && git commit -m "fix: my change"

# 5. Push 到自己的 Fork（不是 upstream）
git push origin fix/my-change

# 6. 从 Fork 向主仓库提 PR
gitlink-cli pr +create --owner TargetOrg --repo target-repo \
  --head MyUser:fix/my-change --base master \
  --title "fix: my change"
```

### 错误做法

- ❌ `git clone` 主仓库 → 建分支 → `git push origin` → 提 PR（直接污染主仓库）
- ❌ 即使有写权限也不要直接往主仓库推分支

### 例外

- 用户明确要求「直接 push」或「不用 Fork」时，可以直接推分支提 PR
- 除此之外，即使是仓库 admin/owner 也应走 Fork 流程

## ⛔ 工具使用边界

**GitLink 平台的操作必须通过 `gitlink-cli` 完成，不能用其他平台的 CLI 替代。**

### 核心规则

| 操作目标 | 正确工具 | 错误工具 |
|----------|----------|----------|
| GitLink 上的仓库/Issue/PR | `gitlink-cli` | `gh` / `hub` / `glab` |
| GitHub 上的仓库/Issue/PR | `gh` | `gitlink-cli` |
| GitLab 上的仓库/MR | `glab` | `gitlink-cli` / `gh` |

**判断标准：看 remote URL 或用户指定的目标平台。**
- remote 含 `gitlink.org.cn` → 用 `gitlink-cli`
- remote 含 `github.com` → 用 `gh`
- 用户明确说"推到 GitLink / 在 GitLink 上创建 PR" → 用 `gitlink-cli`

### 常见错误

当用户在 GitLink 项目中操作时：
- ❌ `gh pr create ...` → `gh` 无法操作 GitLink，会报 command not found 或指向错误平台
- ❌ `gh issue list ...` → 同上
- ✅ `gitlink-cli pr +create ...` → 正确
- ✅ `gitlink-cli issue +list ...` → 正确

> **原则：哪个平台的事，用哪个平台的工具。GitLink 的事只用 `gitlink-cli`。**

### 双平台场景

用户可能同时使用 GitLink 和 GitHub（如双向同步项目）。此时：
- 推送/PR 到 GitLink → `gitlink-cli`
- 推送/PR 到 GitHub → `gh`
- 根据用户意图和目标 remote 判断，不要混用
