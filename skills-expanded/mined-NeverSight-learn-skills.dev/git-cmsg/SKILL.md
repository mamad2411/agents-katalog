---
name: git-cmsg
version: 0.1.42
description: Use when generating Git commit messages, writing commit messages, committing code, or when the user mentions commit、提交、commit message、提交信息. Automatically stages all changes by default, uses LLM to judge if new files should be committed, generates Conventional Commits format messages in Chinese.
allowed-tools: AskUserQuestion, Bash
---

# Git Commit Message Generator

Automatically stage all changes, let LLM judge if new files are safe to commit, then generate Conventional Commits format commit messages in Chinese.

## When to Use

- User wants to commit code changes
- User asks to generate a commit message
- User mentions "提交", "commit", "commit message"

## Conventional Commits Specification

Format:

```
<type>(<scope>): <subject>

<body>

BREAKING CHANGE: <description>
Closes #<issue>
Co-authored-by: {model_name} <{model_email}>
```

**All text must be in Chinese** except type, scope, and special tokens (BREAKING CHANGE, Closes).

## Types

| Type | Chinese | When |
|------|---------|------|
| feat | 新增功能 | New feature |
| fix | 修复缺陷 | Bug fix |
| docs | 文档变更 | Documentation only |
| style | 代码格式 | Formatting, whitespace, semicolons (no logic change) |
| refactor | 重构 | Neither new feature nor bug fix |
| perf | 性能优化 | Performance improvement |
| test | 测试相关 | Adding or fixing tests |
| chore | 构建/工具/依赖 | Build, tools, dependencies |
| ci | CI/CD 配置 | CI/CD configuration |
| revert | 回退提交 | Reverting a commit |
| build | 构建系统 | Build system or external dependencies |

## Rules

1. **Auto-stage all changes first.** Run `git add .` to automatically stage all modified and untracked files. Do NOT ask user to `git add` manually.
2. **LLM judges new file safety.** For every untracked/new file, intelligently determine if it's safe to commit. Consider: filename, file extension, likely content, and purpose.
3. **If all files are safe, proceed automatically.** No need to stop for confirmation on file safety if LLM determines all files are appropriate to commit.
4. **Analyze staged changes.** Run `git diff --cached` to understand what changed. Never guess.
5. **Determine type from changes, not from user description.** If user says "update" but the change adds a feature, use `feat`.
6. **Scope is optional but recommended.** Infer from changed file paths (package name, module name, directory). Use one scope per commit.
7. **Subject line:** Chinese, imperative mood, no period, under 50 chars. Concise summary of WHAT and WHY, not HOW.
8. **Body:** Chinese, explain WHY the change was made. Use numbered list for multiple changes. One change per line.
9. **Do NOT include HOW details** (implementation specifics) in the message.
10. **Commit but do NOT push.** Run `git commit` only. Never `git push`.
11. **必须等待用户确认。** 生成 commit message 后，展示给用户并等待明确同意。用户未回复前禁止执行 `git commit`。如果用户提出修改意见，按意见调整后再次展示确认。
12. **Use the current agent's question tool.** Claude Code should use `AskUserQuestion`. Codex should use `request_user_input` when that tool is listed, available, and permitted in the current mode. If no structured question tool is available or the tool call fails, ask the same question in plain text and wait for the user's reply.

## Decision UI

For every user decision in this skill, use this order:

1. **Claude Code:** use `AskUserQuestion` with the listed `question`, `header`, and `options`.
2. **Codex:** use `request_user_input` with one question object. Include `header`, a stable snake_case `id`, `question`, and 2-3 options. Put the recommended option first and suffix its label with `(Recommended)`.
3. **Fallback:** if the current agent does not expose either structured question tool, or the tool is unavailable, not permitted, or fails, ask the same options as plain text. Do not continue until the user clearly chooses an option.

Never invent a tool name that is not available in the current runtime.

## Pre-commit File Check

**Auto-stage first:** Always run `git add .` at the start to stage all changes automatically.

### LLM File Safety Judgment

For every new/untracked file being staged, use LLM intelligence to judge if it should be committed:

**Judgment Criteria:**
1. **File type:** Is this a source code file, config file, documentation, or binary/blob?
2. **File name:** Does the name suggest it contains secrets, credentials, or temporary data?
3. **Project context:** Does this file belong in the repository based on the project's language/framework?
4. **Common sense:** Would most developers commit this file in a similar project?

**Automatic Action Rules:**
- ✅ **Safe to commit:** Source code (`.go`, `.py`, `.js`, `.ts`, `.java`, etc.), config files (`.json`, `.yaml`, `.yml`, `.toml`), documentation (`.md`, `.txt`), tests, assets that are clearly part of the project. **Proceed automatically, no need to ask.**
- ⚠️ **Ask user:** Large binary files, files with suspicious extensions, files that look like they might contain secrets, or files whose purpose is unclear.
- ❌ **Auto-remove:** Files matching the known bad patterns below. Auto-unstage these and inform user.

### Known Bad Patterns (Auto-remove)

Auto-unstage files matching these without asking:

| Category | Patterns |
|----------|----------|
| IDE/Editor | `.idea/`, `.vscode/`, `*.swp`, `*.swo`, `*~`, `.DS_Store` |
| Build output | `*.o`, `*.a`, `*.so`, `*.exe`, `*.dll`, `*.pyc`, `__pycache__/`, `*.class`, `*.jar`, `*.war`, `dist/`, `build/`, `out/`, `target/` |
| Dependencies | `node_modules/`, `vendor/`, `venv/`, `.venv/` |
| Secrets/Credentials | `.env`, `*.pem`, `*.key`, `*.p12`, `credentials.*`, `*.secret`, `id_rsa*` |
| Log/Temp | `*.log`, `*.tmp`, `*.bak`, `*.cache`, `.cache/` |
| OS files | `Thumbs.db`, `Desktop.ini`, `.DS_Store` |

### Workflow

```
1. git add . → Auto-stage ALL changes (modified + untracked files)
2. git diff --cached --name-only → Get staged file list
3. Check for known bad patterns → Auto-unstage them, inform user
4. For remaining new files → LLM safety judgment
   a. If all judged safe → Proceed automatically (no user prompt)
   b. If uncertain/suspicious → Use Decision UI to confirm
5. If patterns suggest missing .gitignore:
   - Check if .gitignore exists and already covers these patterns
   - If not covered, propose .gitignore additions
   - Use Decision UI to ask: whether to create/update .gitignore
6. Proceed with commit message generation
```

### .gitignore Handling

- If `.gitignore` does not exist in the repo root, offer to create one with appropriate patterns for the project's language/framework.
- If `.gitignore` exists but misses patterns for the flagged files, propose appending the missing patterns.
- Never modify `.gitignore` without user confirmation.
- If user confirms `.gitignore` update, stage the `.gitignore` change and include it in the same commit with type `chore`.

## Workflow

```
1. git add .                        → Auto-stage ALL changes (no need to ask user to git add)
2. git diff --cached --stat         → Overview of changes
3. git diff --cached --name-only    → Staged file list
4. Pre-commit file check:
   a. Auto-unstage known bad patterns and inform user
   b. LLM safety judgment on new files
   c. If all safe → proceed automatically
   d. If uncertain → stop for user confirmation
5. git diff --cached                → Detailed diff (after any file removals)
6. Analyze: type + scope + subject + body
7. Add Co-authored-by trailer (fallback chain: model → client → omit):
   a. **Detect model name** (priority order, highest first):
      1. **Claude Code system prompt** - look for exact line: "You are powered by the model <model_name>"
      2. `~/.trae/traecli.yaml` → `model.name` field
      3. `$ANTHROPIC_MODEL` environment variable
      4. Self-identify from system prompt metadata
   b. **CRITICAL**: If system prompt says "ark-code-latest", use that EXACTLY. Do NOT translate to Claude 4.7 or any other model name"
   c. **Infer provider** from model name prefix (see Provider Mapping below)
   d. **If no prefix match**, infer provider from `$ANTHROPIC_BASE_URL` domain (see Base URL Fallback below)
   e. **If still unresolved**, omit the Co-authored-by line entirely — never use "Unknown"
   f. Format: `Co-authored-by: {model_name} ({provider}) <noreply@{provider_domain}>`

   Provider Mapping:
   | Prefix/Keyword        | Provider         | Domain              |
   |-----------------------|------------------|---------------------|
   | ark-*                 | ByteDance (ARK)  | volcesengine.com    |
   | glm-*, GLM-*          | Zhipu AI         | zhipuai.cn          |
   | claude-*, Claude*     | Anthropic        | anthropic.com       |
   | gpt-*, o1-*, o3-*     | OpenAI           | openai.com          |
   | deepseek-*            | DeepSeek         | deepseek.com        |
   | qwen-*, Qwen*         | Alibaba Cloud    | alibabacloud.com    |
   | doubao-*              | ByteDance        | bytedance.com       |
   | llama-*, Llama*       | Meta             | meta.com            |
   | gemini-*, Gemini*     | Google           | google.com          |
   | mistral-*, Mistral*   | Mistral AI       | mistral.ai          |

   Base URL Fallback:
   | Domain Pattern         | Provider         |
   |------------------------|------------------|
   | volces.com / ark.*     | ByteDance (ARK)  |
   | anthropic.com          | Anthropic        |
   | openai.com             | OpenAI           |
   | deepseek.com           | DeepSeek         |
8. ⚠️ MUST STOP: 使用 Decision UI 展示生成的 commit message 并等待用户确认
   - question: "生成的提交信息是否符合要求？\n\n提交信息预览：\n```\n{commit_message}\n```"
   - header: "提交信息确认"
   - id: "commit_message_action"
   - options: [
       { label: "提交并推送", description: "使用此提交信息进行提交并直接 push 到远程仓库" },
       { label: "确认提交", description: "使用此提交信息进行提交" },
       { label: "重新生成", description: "重新分析代码变更并生成新的提交信息" },
       { label: "取消操作", description: "取消当前提交操作" }
     ]
9. git commit -m "<message>"       → Execute commit (only after user confirms)
10. If user chose "提交并推送": git push  → Execute push (only after commit is successful)
11. Show git log -1 --oneline       → Confirm result
```

## Subject Examples

Good:
- `feat(user): 新增用户注册接口`
- `fix(cache): 修复缓存过期时间未生效的问题`
- `refactor(handler): 优化指标打点逻辑并调整handleBinlogMessage参数`
- `perf(query): 减少数据库查询次数`
- `chore(deps): 升级Gin框架至v1.9.0`

Bad:
- `feat(user): 新增了一个用户注册的接口功能` (too verbose)
- `fix: fix bug` (no scope, no detail)
- `update code` (not Conventional Commits)
- `feat(user): add user register API` (not Chinese)

## Body Examples

Good:
```
refactor(handler): 优化指标打点逻辑并调整handleBinlogMessage参数

1. 重构emitCounter函数，移除固定name参数，内置指标名并通过tagkv传递维度信息
2. 调整handleBinlogMessage签名，新增topic参数用于传递binlog主题
3. 统一所有指标打点的标签格式，补充binlog主题、失败原因等维度信息
4. 调整日志和指标打点的关联逻辑，移除重复的指标调用

Co-authored-by: GLM-5.1 (Zhipu AI) <noreply@zhipuai.cn>
```

Bad:
```
fix: 修复了一些问题

- 改了代码
- 修了bug
```
(vague, no real information)


## Edge Cases

- **No changes at all:** If `git add .` results in empty staging area, inform user there are no changes to commit.
- **Mixed types in one commit:** Pick the most significant type. If a refactor also fixes a bug, use `fix` if the bug fix is the primary intent, `refactor` if the restructuring is the primary intent.
- **Multiple scopes:** Use the most affected scope, or omit scope if no single scope dominates.
- **Breaking changes:** Always add `BREAKING CHANGE:` footer in body.
- **Auto-removed files:** After auto-unstaging known bad files, if no files remain to commit, inform user.
