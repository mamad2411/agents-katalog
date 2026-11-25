---
name: commit-tag
description: |
  分析改动，生成合适的中文 git commit message 并标记代码作者（AI 或 Human）。当用户要求提交代码、commit、生成 commit message 时使用此 skill。支持 --ai/--human flag 和交互式选择。
allowed-tools:
  - Bash(git *)
  - Bash(bash *)
  - AskUserQuestion
  - Read
  - Grep
  - Glob
---

# commit-tag

分析改动，生成带有 AI/Human 标记的合适的 git commit message。

## 触发条件

当用户说以下内容时触发：
- `/commit-tag`、"提交代码"、"commit"、"帮我提交"

## Commit 流程

**Step 1：收集信息**

并行执行以下命令收集当前仓库状态：

```bash
git status
git diff --staged
git diff
git log --oneline -5
```

对 `git status` 中出现的未跟踪文件（Untracked files），读取其内容以便后续分析（大文件只读前 50 行）。

**Step 2：确定暂存范围**

并非所有改动都属于同一个 commit。按以下优先级决定暂存哪些文件：

1. **已暂存文件优先**：如果用户已经手动 `git add` 了部分文件，尊重用户的选择，只提交已暂存的内容
2. **会话上下文推断**：如果没有已暂存文件，根据当前会话中讨论和修改过的文件来判断哪些改动属于本次提交。只选择与当前任务主题相关的文件
3. **全量提交兜底**：如果无法从上下文判断（比如用户直接说"把所有改动都提交了"），才使用全量提交

当改动涉及多个不相关主题时，主动建议用户拆分为多次提交。

**Step 3：敏感文件检查**

在暂存之前，检查待提交文件中是否包含敏感文件（`.env`、`credentials.json`、`*secret*`、`*.key`、`*.pem` 等）。如果发现，警告用户并从暂存列表中排除，除非用户明确确认要包含。

**Step 4：生成 commit message**

分析待提交的改动内容，生成中文 commit message，遵循 conventional commits 格式：

```
type(scope): 简短描述

- 改动点 1
- 改动点 2
```

规则：
- type 从以下选择：feat / fix / refactor / perf / chore / ci / docs / style / test
- scope 根据改动的主要模块或目录确定；如果改动跨多个模块则省略 scope
- subject 行（第一行）控制在 50 字符以内
- body 中的改动点用简洁的短句概括，每项不超过一行

**Step 5：确定作者类型**

解析用户输入中的 flag：
- `--ai` → 标记为 AI 编写
- `--human` → 标记为人类编写
- 无 flag → 使用 AskUserQuestion 询问：

```
这次提交的代码主要由谁编写？
- AI 编写（AI 生成或 AI 辅助完成主要逻辑）
- 人类编写（人类手写，AI 仅辅助少量内容）
```

**Step 6：构造最终 commit message**

如果是 AI 编写，在 message 末尾追加 trailer：

```
type(scope): 简短描述

- 改动点 1
- 改动点 2

Co-Authored-By: AI-Agent <ai@noreply>
```

如果是人类编写，不追加 trailer。

**Step 7：执行提交**

```bash
git add <具体文件列表>
git commit -m "$(cat <<'EOF'
commit message here
EOF
)"
```

注意：
- 如果没有可提交的改动，提示用户并终止
- 使用具体文件名而非 `git add -A`，确保只提交 Step 2 确定的文件
- commit message 通过 HEREDOC 传递以保证格式正确

## 重要规则

- commit message 必须使用中文
- 如果用户明确指定了 commit message 内容，尊重用户的内容，仅追加 trailer
- AI trailer 使用 `Co-Authored-By: AI-Agent <ai@noreply>`，与 Claude 默认的 `Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>` 格式均可被统计工具识别
