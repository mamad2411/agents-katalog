---
name: github-auth
description: "GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Authentication, Git, gh-cli, SSH, Setup]
    related_skills: [github-pr-workflow, github-code-review, github-issues, github-repo-management]
---

# GitHub身份验证设置

该技能用于配置身份验证机制，使智能体能够操作GitHub仓库、Pull Request、问题以及CI任务。它提供两种认证方式：

- **`git`（始终可用）** — 使用HTTPS个人访问令牌或SSH密钥
- **`gh` CLI（如已安装）** — 通过更简化的认证流程实现更丰富的GitHub API访问功能

## 检测流程

当用户要求你处理与GitHub相关的工作时，首先执行此检查：

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"

# Check if already authenticated
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**决策树：**
1. 如果 `gh auth status` 显示已认证 → 恭喜，可直接使用 `gh` 执行所有操作
2. 如果已安装 `gh` 但未认证 → 请使用下方的 “gh auth” 方法进行认证
3. 如果未安装 `gh` → 请使用下方的 “仅使用 git” 方法（无需 sudo 权限）

---

## 方法 1：仅使用 Git 进行认证（无需 gh，无需 sudo）

只要机器上安装了 `git` 即可使用此方法，无需 root 权限。

### 方案 A：通过个人访问令牌进行 HTTPS 认证（推荐）

这是最通用的方法——可在任何环境中使用，且无需配置 SSH。

**步骤 1：创建个人访问令牌**

请用户访问：**https://github.com/settings/tokens**

- 点击 “Generate new token (classic)”
- 给令牌起个名称，例如 “hermes-agent”
- 选择权限范围：
  - `repo`（完整的仓库访问权限——读取、写入、推送代码及提交 Pull Request）
  - `workflow`（触发和管理 GitHub Actions 工作流）
  - `read:org`（如需操作组织内的仓库）
- 设置有效期（默认 90 天较为合适）
- 复制该令牌——此后再也不会显示

**步骤 2：配置 git 以存储该令牌**

```bash
# Set up the credential helper to cache credentials
# "store" saves to ~/.git-credentials in plaintext (simple, persistent)
git config --global credential.helper store

# Now do a test operation that triggers auth — git will prompt for credentials
# Username: <their-github-username>
# Password: <paste the personal access token, NOT their GitHub password>
git ls-remote https://github.com/<their-username>/<any-repo>.git
```

一旦输入过凭证，它们就会被保存下来，并在后续的所有操作中重复使用。

**备选方案：缓存辅助功能（凭证仅存储在内存中，到期后会自动清除）**

```bash
# Cache in memory for 8 hours (28800 seconds) instead of saving to disk
git config --global credential.helper 'cache --timeout=28800'
```

**备选方案：直接在远程 URL 中设置令牌（针对单个仓库）**

```bash
# Embed token in the remote URL (avoids credential prompts entirely)
git remote set-url origin https://<username>:<token>@github.com/<owner>/<repo>.git
```

**步骤 3：配置 Git 身份信息**

```bash
# Required for commits — set name and email
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

**第4步：验证**

```bash
# Test push access (this should work without any prompts now)
git ls-remote https://github.com/<their-username>/<any-repo>.git

# Verify identity
git config --global user.name
git config --global user.email
```

### 方案 B：SSH 密钥认证

适用于更倾向于使用 SSH 或已配置好密钥的用户。

**步骤 1：检查现有的 SSH 密钥**

```bash
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"
```

**步骤 2：如需，请生成密钥**

```bash
# Generate an ed25519 key (modern, secure, fast)
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Display the public key for them to add to GitHub
cat ~/.ssh/id_ed25519.pub
```

请告知用户将公钥添加至以下地址：**https://github.com/settings/keys**
- 点击“新建 SSH 密钥”
- 粘贴公钥内容
- 为该密钥起一个名称，例如 “hermes-agent-<机器名称>”

**第 3 步：测试连接**

```bash
ssh -T git@github.com
# Expected: "Hi <username>! You've successfully authenticated..."
```

**第4步：配置git以使用SSH连接GitHub**

```bash
# Rewrite HTTPS GitHub URLs to SSH automatically
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

**第5步：配置Git身份信息**

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

## 方法 2：通过 gh CLI 进行身份验证

如果已安装 `gh`，它可一步完成 API 访问及 Git 凭据的处理。

### 交互式浏览器登录（桌面端）

```bash
gh auth login
# Select: GitHub.com
# Select: HTTPS
# Authenticate via browser
```

### 基于令牌的登录（无头服务器/SSH服务器）

```bash
echo "<THEIR_TOKEN>" | gh auth login --with-token

# Set up git credentials through gh
gh auth setup-git
```

### 验证

```bash
gh auth status
```

## 无需使用 gh 即可调用 GitHub API

即使没有安装 `gh`，您也可以通过结合 `curl` 与个人访问令牌来访问完整的 GitHub API。其他 GitHub 技能也正是通过这种方式实现备用方案。

### 为 API 调用设置令牌

```bash
# Option 1: Export as env var (preferred — keeps it out of commands)
export GITHUB_TOKEN="<token>"

# Then use in curl calls:
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### 从 Git 凭证中提取令牌

如果已配置 Git 凭证（通过 credential.helper 存储机制），则可从中提取令牌：

```bash
# Read from git credential store
grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'
```

### 辅助工具：检测认证方式

在任意 GitHub 工作流的开头使用此模式：

```bash
# Try gh first, fall back to git + curl
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "AUTH_METHOD=gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  echo "AUTH_METHOD=curl"
elif _hermes_env="${HERMES_HOME:-$HOME/.hermes}/.env"; [ -f "$_hermes_env" ] && grep -q "^GITHUB_TOKEN=" "$_hermes_env"; then
  export GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_hermes_env" | head -1 | cut -d= -f2 | tr -d '\n\r')
  echo "AUTH_METHOD=curl"
elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
  export GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  echo "AUTH_METHOD=curl"
else
  echo "AUTH_METHOD=none"
  echo "Need to set up authentication first"
fi
```

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| `git push` 提示需要密码 | GitHub 已禁用密码认证。请使用个人访问令牌作为密码，或切换为 SSH 认证方式 |
| `remote: Permission to X denied` | 令牌可能缺少 `repo` 权限范围——请使用包含正确权限范围的令牌重新生成 |
| `fatal: Authentication failed` | 缓存的凭据可能已过期——请运行 `git credential reject` 后重新进行认证 |
| `ssh: connect to host github.com port 22: Connection refused` | 尝试通过 HTTPS 端口使用 SSH：在 `~/.ssh/config` 文件中添加 `Host github.com`、`Port 443` 以及 `Hostname ssh.github.com` |
| 凭据无法持久保存 | 检查 `git config --global credential.helper` 的设置——该值必须为 `store` 或 `cache` |
| 拥有多个 GitHub 账户 | 可在 `~/.ssh/config` 中为每个主机别名配置不同的 SSH 密钥，或为每个仓库指定独立的凭据 URL |
| 出现 `gh: command not found` 且未使用 sudo 权限 | 请使用上述仅依赖 Git 的解决方案——无需进行任何安装操作 |
