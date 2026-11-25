---
name: git-workflow
description: "Git 工作流 — 版本控制、提交规范、分支管理、.gitignore 治理"
stage: development
type: delivery-skill
version: "1.0"
scope: platform
category: delivery
tags: [git, commit, push, pull, branch, gitignore, version-control]
---

# Git 工作流技能

## 1. 操作原则

- **用户确认机制**：在执行 `workspace_git_commit` / `workspace_git_push` / `workspace_git_pull` 前，系统会自动向用户弹出确认卡。如用户点击"取消"，工具返回"用户已取消"，应立即停止该 git 操作并告知用户，不要重试。
- **提交前读 diff**：使用 `workspace_git_diff` 查看改动，确认无误再提交
- **Commit message 规范**：格式为 `type: 描述`，type 可选：
  - `feat`: 新功能
  - `fix`: Bug 修复
  - `docs`: 文档更新
  - `refactor`: 代码重构
  - `test`: 测试相关
  - `chore`: 构建/配置变更
- **不提交敏感/临时文件**：`.env`、日志文件、IDE 配置、编译产物
- **每次提交只包含逻辑相关的改动**，避免大杂烩提交

## 2. 工作流模型

```
main/master
  └── feature/xxx (从 main 切出)
        ├── 多次 commit
        └── PR → code review → merge to main
```

- **禁止直推 main/master**：所有变更通过 feature branch + PR
- feature branch 命名：`feature/描述`、`bugfix/描述`、`hotfix/描述`
- 保持 branch 生命周期短，尽早合并

## 3. Commit 三步骤

执行提交时，**必须按顺序**：

1. `workspace_git_status` — 查看当前分支和修改文件
2. `workspace_git_diff` — 确认具体改动内容
3. `workspace_git_add` — 精确暂存需要提交的文件
4. `workspace_git_commit` — 提交（自动附加 `[Forge-Agent]` 标注）

> **示例消息**："帮我提交登录功能的实现" → 执行以上 4 步，commit message 为 `feat: 实现用户登录功能 [Forge-Agent]`

## 4. .gitignore 治理

初始化 `.gitignore` 时，根据项目类型选择模板。

**常见忽略类别**：
- **Secrets**：`.env`, `*.key`, `*.pem`, `credentials.json`
- **Build artifacts**：`build/`, `dist/`, `target/`, `*.class`, `*.jar`
- **IDE files**：`.idea/`, `.vscode/`, `*.iml`
- **OS files**：`.DS_Store`, `Thumbs.db`
- **Dependencies**：`node_modules/`, `.gradle/`
- **Logs**：`*.log`, `logs/`

**Kotlin/Spring Boot 项目模板**：
```gitignore
# Build
build/
*.jar
*.war

# IDE
.idea/
*.iml
.gradle/

# Logs
*.log
logs/

# Env
.env
*.env.local

# OS
.DS_Store
Thumbs.db
```

**Node.js/TypeScript 项目模板**：
```gitignore
# Dependencies
node_modules/

# Build
dist/
.next/
out/

# Env
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*
```

## 5. 分支命名约定

| 类型 | 格式 | 示例 |
|------|------|------|
| 新功能 | `feature/描述` | `feature/user-login` |
| Bug 修复 | `bugfix/描述` | `bugfix/fix-null-pointer` |
| 紧急修复 | `hotfix/描述` | `hotfix/security-patch` |
| 发布准备 | `release/版本` | `release/v1.2.0` |

## 6. 常用场景 SOP

### 场景 A：开发新功能
```
1. workspace_git_status     # 确认当前在 main，工作区干净
2. workspace_git_branch name="feature/xxx"   # 创建并切换到新分支
3. [编写代码...]
4. workspace_git_diff       # 查看改动
5. workspace_git_add paths=["src/..."]       # 暂存文件
6. workspace_git_commit message="feat: xxx"  # 提交
```

### 场景 B：修复 Bug
```
1. workspace_git_status
2. workspace_git_diff
3. workspace_git_add all=true
4. workspace_git_commit message="fix: 修复 xxx 问题"
```

### 场景 C：同步远程代码
```
1. workspace_git_pull rebase=true    # 拉取并 rebase
2. workspace_git_status              # 确认状态
```

### 场景 D：初始化 .gitignore
```
1. workspace_list_files              # 查看项目类型
2. workspace_write_file path=".gitignore" content=<模板内容>
3. workspace_git_add paths=[".gitignore"]
4. workspace_git_commit message="chore: 初始化 .gitignore"
```

### 场景 E：克隆远程仓库（GitHub / GitLab 通用）

> ⚠️ 克隆是网络操作。**必须先做 Pre-flight 验证，禁止直接尝试克隆**。最多尝试 2 次，失败后立即 escalate，不要穷举变体。

#### E.1 识别平台和 token 格式

| 平台 | URL 特征 | Token 格式 |
|------|---------|-----------|
| GitHub.com | `github.com` | `ghp_*`（PAT classic）/ `github_pat_*`（fine-grained） |
| GitLab.com | `gitlab.com` | `glpat-*` |
| 企业 GitLab | 自定义域名 | `glpat-*` |
| 企业 GitHub | 自定义域名（Enterprise） | `ghp_*` / `ghs_*` |

#### E.2 Pre-flight — 网络连通性（Step 1，必做）

```bash
# 提取主机名
HOST=$(echo "$REPO_URL" | sed -E 's|https?://([^/@]+@)?([^/:]+).*|\2|')

# 验证主机可达（10s 超时）
curl --max-time 10 -s -o /dev/null -w "%{http_code}" "https://$HOST" 2>&1
```

- **返回 000 / 连接被拒 / 超时** → 主机不可达。立即写入 workspace 记忆：
  ```
  [BLOCKER] $HOST not reachable from this environment (network timeout).
  Tried: curl. Do not retry clone variants.
  ```
  然后告知用户，**停止**，建议替代方案（见 E.5）。
- **返回任何 HTTP 状态码** → 主机可达，进入 Step 2。

#### E.3 Pre-flight — 认证验证（Step 2，必做）

```bash
# GitHub / GitLab 均支持：用 git ls-remote 测试认证（比 clone 快 10x）
git ls-remote --exit-code "$REPO_URL" HEAD 2>&1 | head -5
```

- **exit 128 / 401 / 403** → token 无效或权限不足。告知用户具体错误，**不要继续**。
- **exit 0** → 认证通过，进入 Step 3。

#### E.4 执行克隆

```bash
# 默认 shallow clone（加速，适合大仓库）
git clone --depth 50 "$REPO_URL" .

# 如果需要完整历史（用户明确要求时才用）
git clone "$REPO_URL" .
```

**失败重试规则**：
- 第 1 次失败（如网络抖动）→ 等待 3s，去掉 `--depth` 重试一次
- 第 2 次失败 → **停止**，生成诊断报告（见 E.5），不再尝试其他变体

#### E.5 失败后的 escalation 模板

```
克隆失败。已验证：
- 主机 $HOST：[可达/不可达]
- 认证：[通过/失败，原因：xxx]
- 尝试次数：[N]

建议替代方案：
1. 在能访问该仓库的机器上执行：git bundle create repo.bundle --all
   然后将 repo.bundle 文件传入本环境，执行：git clone repo.bundle .
2. 配置 VPN 或 SSH 隧道使本环境能访问 $HOST
3. 在本地克隆后，使用 workspace_write_file 逐文件上传关键源码
```

#### E.6 Token 安全规范（重要）

- ❌ **禁止**：将 token 硬编码进脚本或 URL：`https://glpat-xxx@gitlab.com/...`
- ✅ **推荐**：使用环境变量传递 token：
  ```bash
  # GitHub
  git clone "https://x-access-token:$GITHUB_TOKEN@github.com/org/repo.git" .
  # GitLab
  git clone "https://oauth2:$GITLAB_TOKEN@gitlab.com/org/repo.git" .
  ```
- 克隆完成后立即清理 token 引用，配置 credential 缓存替代明文存储

---

## 7. 可用 MCP 工具清单

> ⚠️ **重要**：本技能**无 scripts 目录**，禁止调用 `run_skill_script`。所有 git 操作均通过以下 MCP 工具完成。

| 工具 | 说明 |
|------|------|
| `workspace_git_status` | 查看当前分支 + 修改文件列表 |
| `workspace_git_diff` | 查看 staged + unstaged 改动 |
| `workspace_git_add` | 暂存文件（精确或全量） |
| `workspace_git_commit` | 提交暂存的改动 |
| `workspace_git_push` | 推送到远程（main/master 时给出警告） |
| `workspace_git_pull` | 拉取远程变更（默认 --rebase） |
| `workspace_git_branch` | 创建新分支或列出所有分支 |
