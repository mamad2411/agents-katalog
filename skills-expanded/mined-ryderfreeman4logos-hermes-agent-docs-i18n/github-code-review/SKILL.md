---
name: github-code-review
description: "Review PRs: diffs, inline comments via gh or REST."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Code-Review, Pull-Requests, Git, Quality]
    related_skills: [github-auth, github-pr-workflow]
---

# GitHub代码审查

在推送代码之前，可先对本地修改进行代码审查，或直接在GitHub上查看已提交的PR。该功能主要使用基础的`git`命令——只有在进行PR相关操作时，才需要区分使用`gh`还是`curl`命令。

## 前提条件

- 已在GitHub完成身份认证（参见`github-auth`功能）
- 处于某个git仓库中

### 设置（用于处理PR）

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if _hermes_env="${HERMES_HOME:-$HOME/.hermes}/.env"; [ -f "$_hermes_env" ] && grep -q "^GITHUB_TOKEN=" "$_hermes_env"; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" "$_hermes_env" | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

## 1. 查看本地更改（推送前）

这完全基于 `git` —— 可在任何地方使用，无需 API。

### 获取差异内容

```bash
# Staged changes (what would be committed)
git diff --staged

# All changes vs main (what a PR would contain)
git diff main...HEAD

# File names only
git diff main...HEAD --name-only

# Stat summary (insertions/deletions per file)
git diff main...HEAD --stat
```

### 审核策略

1. **首先把握整体概览：**

```bash
git diff main...HEAD --stat
git log main..HEAD --oneline
```

2. **逐个文件审查**——对发生更改的文件使用 `read_file` 函数以获取完整上下文，并通过差异对比功能查看具体修改内容：

```bash
git diff main...HEAD -- src/auth/login.py
```

3. **检查常见问题：**

```bash
# Debug statements, TODOs, console.logs left behind
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|HACK\|XXX\|debugger"

# Large files accidentally staged
git diff main...HEAD --stat | sort -t'|' -k2 -rn | head -10

# Secrets or credential patterns
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*=\|private_key"

# Merge conflict markers
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======="
```

4. **向用户提供结构化的反馈**。

### 审核输出格式

在审核本地更改时，请按照以下结构呈现审核结果：

```
## Code Review Summary

### Critical
- **src/auth.py:45** — SQL injection: user input passed directly to query.
  Suggestion: Use parameterized queries.

### Warnings
- **src/models/user.py:23** — Password stored in plaintext. Use bcrypt or argon2.
- **src/api/routes.py:112** — No rate limiting on login endpoint.

### Suggestions
- **src/utils/helpers.py:8** — Duplicates logic in `src/core/utils.py:34`. Consolidate.
- **tests/test_auth.py** — Missing edge case: expired token test.

### Looks Good
- Clean separation of concerns in the middleware layer
- Good test coverage for the happy path
```

## 2. 在 GitHub 上审查拉取请求

### 查看 PR 详情

**使用 gh 命令：**

```bash
gh pr view 123
gh pr diff 123
gh pr diff 123 --name-only
```

**使用 git + curl 方式：**

```bash
PR_NUMBER=123

# Get PR details
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "
import sys, json
pr = json.load(sys.stdin)
print(f\"Title: {pr['title']}\")
print(f\"Author: {pr['user']['login']}\")
print(f\"Branch: {pr['head']['ref']} -> {pr['base']['ref']}\")
print(f\"State: {pr['state']}\")
print(f\"Body:\n{pr['body']}\")"

# List changed files
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/files \
  | python3 -c "
import sys, json
for f in json.load(sys.stdin):
    print(f\"{f['status']:10} +{f['additions']:-4} -{f['deletions']:-4}  {f['filename']}\")"
```

### 在本地查看 Pull Request 以进行全面审查

该功能可直接使用普通的 `git` 命令——无需借助 `gh`：

```bash
# Fetch the PR branch and check it out
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Now you can use read_file, search_files, run tests, etc.

# View diff against the base branch
git diff main...pr-123
```

**使用 gh（快捷键）：**

```bash
gh pr checkout 123
```

### 在 Pull Request 上留下评论

**使用 gh 工具添加常规 PR 评论：**

```bash
gh pr comment 123 --body "Overall looks good, a few suggestions below."
```

**使用 curl 发送常规 Pull Request 评论：**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/$PR_NUMBER/comments \
  -d '{"body": "Overall looks good, a few suggestions below."}'
```

### 留下内联评审评论

**使用 gh 通过 API 添加单条内联评论：**

```bash
HEAD_SHA=$(gh pr view 123 --json headRefOid --jq '.headRefOid')

gh api repos/$OWNER/$REPO/pulls/123/comments \
  --method POST \
  -f body="This could be simplified with a list comprehension." \
  -f path="src/auth/login.py" \
  -f commit_id="$HEAD_SHA" \
  -f line=45 \
  -f side="RIGHT"
```

**使用 curl 添加单行内联注释：**

```bash
# Get the head commit SHA
HEAD_SHA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments \
  -d "{
    \"body\": \"This could be simplified with a list comprehension.\",
    \"path\": \"src/auth/login.py\",
    \"commit_id\": \"$HEAD_SHA\",
    \"line\": 45,
    \"side\": \"RIGHT\"
  }"
```

### 提交正式审核（批准/请求修改）

**通过 gh 实现：**

```bash
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."
gh pr review 123 --comment --body "Some suggestions, nothing blocking."
```

**使用 curl —— 可以以原子方式提交多条评论：**

```bash
HEAD_SHA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/reviews \
  -d "{
    \"commit_id\": \"$HEAD_SHA\",
    \"event\": \"COMMENT\",
    \"body\": \"Code review from Hermes Agent\",
    \"comments\": [
      {\"path\": \"src/auth.py\", \"line\": 45, \"body\": \"Use parameterized queries to prevent SQL injection.\"},
      {\"path\": \"src/models/user.py\", \"line\": 23, \"body\": \"Hash passwords with bcrypt before storing.\"},
      {\"path\": \"tests/test_auth.py\", \"line\": 1, \"body\": \"Add test for expired token edge case.\"}
    ]
  }"
```

事件值：`"APPROVE"`、`"REQUEST_CHANGES"`、`"COMMENT"`

`line` 字段表示文件*新版本*中的行号。对于被删除的行，请使用 `"side": "LEFT"`。

---

## 3. 审核检查清单

在进行代码审核（本地或 PR）时，需系统地检查以下内容：

### 正确性
- 代码是否实现了预期的功能？
- 是否处理了边缘情况（空输入、空值、大数据量、并发访问等）？
- 错误处理是否得当？

### 安全性
- 不存在硬编码的机密信息、凭证或 API 密钥
- 对用户输入进行了验证
- 无 SQL 注入、XSS 或路径遍历风险
- 在需要处进行了身份认证与授权检查

### 代码质量
- 变量、函数和类的命名清晰
- 不存在不必要的复杂性或过早的抽象设计
- 遵循 DRY 原则——没有应被提取出来的重复逻辑
- 函数职责单一，专注明确

### 测试
- 是否测试了新的代码路径？
- 是否覆盖了正常流程和错误场景？
- 测试用例是否易于阅读和维护？

### 性能
- 不存在 N+1 查询或不必要的循环
- 在合适的地方使用了缓存机制
- 异步代码路径中不存在阻塞操作

### 文档
- 公共 API 已有文档说明
- 难以理解的逻辑部分配有解释“为何如此设计”的注释
- 如果功能发生变更，已更新 README 文件

---

## 4. 推送前审核工作流程

当用户要求你“审核代码”或“在推送前检查”时，请按以下步骤操作：

1. `git diff main...HEAD --stat` — 查看修改范围
2. `git diff main...HEAD` — 查看完整的差异内容
3. 对每个被修改的文件，如需更多上下文信息，可使用 `read_file` 功能
4. 按照上述检查清单进行审核
5. 以结构化格式呈现审核结果（严重问题 / 警告 / 建议 / 无问题）
6. 如果发现严重问题，可主动提出在用户推送前帮其修复

---

## 5. PR 审核工作流程（端到端）

当用户要求你“审核 PR #N”、“看看这个 PR”或提供 PR 链接时，请遵循以下流程：

### 第一步：搭建环境

```bash
source "${HERMES_HOME:-$HOME/.hermes}/skills/github/github-auth/scripts/gh-env.sh"
# Or run the inline setup block from the top of this skill
```

### 第 2 步：收集 Pull Request 相关信息

在深入研究代码之前，先获取 Pull Request 的元数据、描述以及变更文件列表，以便了解其工作范围。

**使用 gh 工具时：**
```bash
gh pr view 123
gh pr diff 123 --name-only
gh pr checks 123
```

**使用 curl：**
```bash
PR_NUMBER=123

# PR details (title, author, description, branch)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER

# Changed files with line counts
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/files
```

### 第 3 步：在本地查看该 Pull Request

这样您即可完全使用 `read_file`、`search_files` 函数，同时还能运行测试。

```bash
git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER
git checkout pr-$PR_NUMBER
```

### 第4步：查看差异并了解具体变更内容

```bash
# Full diff against the base branch
git diff main...HEAD

# Or file-by-file for large PRs
git diff main...HEAD --name-only
# Then for each file:
git diff main...HEAD -- path/to/file.py
```

对于每一个被修改过的文件，建议使用 `read_file` 功能来查看该改动周围的完整代码上下文——仅通过差异对比往往无法发现那些只有结合周边代码才能识别的问题。

### 第 5 步：在本地运行自动化检查（如适用）

```bash
# Run tests if there's a test suite
python -m pytest 2>&1 | tail -20
# or: npm test, cargo test, go test ./..., etc.

# Run linter if configured
ruff check . 2>&1 | head -30
# or: eslint, clippy, etc.
```

### 第 6 步：应用审查检查表（第 3 节）

逐一检查以下各个类别：正确性、安全性、代码质量、测试、性能以及文档情况。

### 第 7 步：将审查结果发布到 GitHub

汇总您的发现，并通过内联评论的形式提交正式的审查报告。

**使用 gh 命令：**
```bash
# If no issues — approve
gh pr review $PR_NUMBER --approve --body "Reviewed by Hermes Agent. Code looks clean — good test coverage, no security concerns."

# If issues found — request changes with inline comments
gh pr review $PR_NUMBER --request-changes --body "Found a few issues — see inline comments."
```

**使用 curl — 带有多条内联注释的原子级审核：**
```bash
HEAD_SHA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

# Build the review JSON — event is APPROVE, REQUEST_CHANGES, or COMMENT
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/reviews \
  -d "{
    \"commit_id\": \"$HEAD_SHA\",
    \"event\": \"REQUEST_CHANGES\",
    \"body\": \"## Hermes Agent Review\n\nFound 2 issues, 1 suggestion. See inline comments.\",
    \"comments\": [
      {\"path\": \"src/auth.py\", \"line\": 45, \"body\": \"🔴 **Critical:** User input passed directly to SQL query — use parameterized queries.\"},
      {\"path\": \"src/models.py\", \"line\": 23, \"body\": \"⚠️ **Warning:** Password stored without hashing.\"},
      {\"path\": \"src/utils.py\", \"line\": 8, \"body\": \"💡 **Suggestion:** This duplicates logic in core/utils.py:34.\"}
    ]
  }"
```

### 第8步：还需添加总结评论

除了内联评论外，还需撰写一级总结内容，以便PR提交者能一目了然地掌握整体情况。请使用`references/review-output-template.md`中规定的审核输出格式。

**通过gh平台操作时：**
```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
## Code Review Summary

**Verdict: Changes Requested** (2 issues, 1 suggestion)

### 🔴 Critical
- **src/auth.py:45** — SQL injection vulnerability

### ⚠️ Warnings
- **src/models.py:23** — Plaintext password storage

### 💡 Suggestions
- **src/utils.py:8** — Duplicated logic, consider consolidating

### ✅ Looks Good
- Clean API design
- Good error handling in the middleware layer

---
*Reviewed by Hermes Agent*
EOF
)"
```

### 第9步：清理工作

```bash
git checkout main
git branch -D pr-$PR_NUMBER
```

### 决策选项：批准、要求修改或仅发表意见

- **批准** — 不存在任何严重或警告级别的问题，仅有轻微建议或所有方面均无问题  
- **要求修改** — 存在必须在合并前解决的严重或警告级别问题  
- **仅发表意见** — 仅提出观察结果与建议，且没有会阻碍流程的问题（在不确定或该 PR仍处于草稿阶段时使用）
