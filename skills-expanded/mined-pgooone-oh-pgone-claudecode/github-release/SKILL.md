---
name: github-release
description: >
  自动化 GitHub 发布流程：检测工具依赖 → 暂存文件 → 提交 → 推送到远程 → 打标签 → 创建 Release。
  当用户提到"发布"、"release"、"推送到 GitHub"、"打标签"、"创建版本"、"publish"时使用此技能。
  确保使用此技能处理任何版本发布相关的需求。
---

# GitHub Release 发布流程

将代码变更发布到 GitHub 并创建 Release 的标准化流程。

## 前置条件检测

执行发布前，**必须**检测以下工具是否可用：

### 1. 检测 git

```bash
git --version
```

- 如果命令不存在或执行失败，告知用户需要安装 git，并提供安装指引
- Windows: `winget install Git.Git` 或访问 https://git-scm.com
- macOS: `brew install git`
- Linux: `sudo apt install git` 或 `sudo yum install git`

### 2. 检测 gh (GitHub CLI)

```bash
gh --version
```

- 如果命令不存在或执行失败，告知用户需要安装 GitHub CLI
- Windows: `winget install GitHub.cli`
- macOS: `brew install gh`
- Linux: 参考 https://github.com/cli/cli#installation

### 3. 检测 gh 认证状态

```bash
gh auth status
```

- 如果未认证，提示用户运行 `gh auth login` 完成认证

### 4. 确认在 git 仓库中

```bash
git rev-parse --is-inside-work-tree
```

- 如果不在 git 仓库中，提示用户先初始化或进入正确的仓库目录

**以上任一检测失败，停止流程并告知用户具体缺少什么。**

## 发布流程

按照以下步骤依次执行：

### Step 1: 查看当前状态

```bash
git status
git diff --stat
git log --oneline -5
```

向用户展示当前工作区状态、变更统计和最近提交记录，确认哪些文件需要提交。

### Step 2: 暂存文件

```bash
git add <文件路径>
```

- **不要使用 `git add .` 或 `git add -A`**，避免意外提交敏感文件（.env、credentials 等）
- 逐个指定需要提交的文件
- 暂存后运行 `git status` 确认

### Step 3: 提交

```bash
git commit -m "$(cat <<'EOF'
<版本号>: <简短描述>

- 变更点 1
- 变更点 2

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

- commit message 使用中文
- 格式：`版本号: 简短描述`
- 正文列出具体变更点

### Step 4: 推送到远程

```bash
git push origin <当前分支>
```

### Step 5: 打标签

```bash
git tag <版本号>
git push origin <版本号>
```

- 版本号格式遵循 semver（如 `v0.1.1`）
- 先确认标签不存在：`git tag -l`

### Step 6: 创建 Release

```bash
gh release create <版本号> \
  --title "<标题>" \
  --notes "$(cat <<'EOF'
## <版本号> - <副标题>

### 概述
<本次发布的简要说明>

### 变更内容
- 变更 1
- 变更 2

---
**Full Changelog**: https://github.com/<owner>/<repo>/compare/<上个版本>...<当前版本>
EOF
)"
```

## 完成确认

发布完成后，向用户报告：
- 提交的 commit hash
- 创建的标签
- Release 链接
