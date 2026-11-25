---
name: commit-with-prompts
description: |
  Saves user prompts from the current Claude Code session to version control when making git commits.
  MUST be used whenever the user asks to commit, create a commit, or any commit-related action —
  including "commit", "提交", "提交代码", "git commit", "/commit", or any variation.
  Augments the normal commit workflow by preserving the prompts that drove code changes,
  treating prompts as source code. Use this skill even if the user doesn't explicitly mention
  prompts — it runs automatically as part of every commit.
---

# Commit with Prompts

Prompts are source code. They capture the intent, reasoning, and decisions behind every code change. This skill preserves them alongside the code they produced, creating a traceable history of human-AI collaboration in version control.

## Workflow

When the user asks to commit, execute these steps. The ordering matters because the prompt file depends on knowing the commit message, so you must draft the commit message before creating the prompt file.

### Step 1: Collect Prompt Units

Review the current conversation and collect **prompt units**. Each prompt unit consists of:

1. **User prompt** (required) — the user's original message
2. **Context question** (optional) — if the user's message is an answer to a question you asked (e.g., choosing from options, answering a clarification question), include your original question text so the answer makes sense in isolation
3. **Plan** (optional) — if your response to that prompt included a plan (from plan mode or a structured implementation plan presented for user approval), capture the plan content
4. **Insight** (optional) — if your response to that prompt included a `★ Insight` section, capture its content
5. **Affected files** (optional) — the files you created, modified, or deleted in response to that prompt

**Scope rules:**
- **First commit in session**: collect from the start of the conversation
- **Subsequent commits**: collect only what came **after** the previous prompt save in this session

**What to include**: requirements, instructions, questions, clarifications, corrections, feedback, and design decisions — anything substantive that provides context for why the code changed.

**What to skip**: trivial confirmations and bare commit commands. Examples: "yes", "ok", "y", "continue", "好的", "确认", "commit", "commit this", "提交", "提交代码". These carry no design intent. When in doubt, include it.

If there are **no substantive prompts** to save (every message since the last save was trivial), skip prompt file creation entirely and proceed with a normal commit.

### Step 2: Draft the Commit Message

Follow the standard commit workflow to analyze the staged/unstaged changes and draft a commit message. Do everything you normally would — `git status`, `git diff`, review recent commit style — **but do not run `git commit` yet**. You need the commit message first so it can be embedded in the prompt record file.

### Step 3: Create the Prompt Record File

Now that you have both the prompts and the commit message, create the record file.

**Directory**: `prompts/` at the project root. Create it if it doesn't exist.

**Filename**: `YYYY-MM-DD_<branch>_<summary>.md`

- `YYYY-MM-DD` — today's date (day precision only)
- `<branch>` — current git branch name (replace `/` with `-`, e.g. `feature/auth` → `feature-auth`)
- `<summary>` — a short slug derived from the commit message: lowercase, spaces and special characters replaced with `-`, truncated to ~50 characters

If a file with the same name already exists, append `-2`, `-3`, etc.

**Example filenames:**
```
2026-03-04_main_feat-add-user-auth.md
2026-03-04_feature-auth_fix-token-expiry.md
2026-03-05_main_refactor-api-endpoints.md
```

**File content** — use this template:

```markdown
# Prompt Record

- Date: YYYY-MM-DD HH:MM
- Branch: <branch-name>
- Commit: <full commit message>

---

### 1. <short summary of this prompt>

<user prompt text>

> **Plan**
> <plan content from your plan mode response or structured implementation plan, if any>

> **Insight**
> <insight content from your ★ Insight response, if any>

**Files:** `path/to/file1.py`, `path/to/file2.js`

### 2. <short summary of this prompt>

> **Q:** <the question you asked that this prompt is answering>

<user's answer>

**Files:** `path/to/file3.py`

### 3. <short summary of this prompt>

<user prompt text — a standalone instruction, no Q: needed>
```

**Formatting rules:**
- Each prompt unit is numbered sequentially, with a short summary after the number (e.g., `### 1. Add workspace to gitignore`). The summary should be a concise phrase (not a full sentence) capturing what the user asked or decided in that prompt.
- Preserve user prompt text faithfully — do not summarize, edit, or reformat the user's words
- The **Q:** block provides context when the user's message is a response to a question you asked (e.g., choosing from options, answering a clarification). Use blockquote format (`> **Q:**`). Include the essential question text — you may condense multi-option questions to just the question line and the chosen option. If the user's message is a standalone instruction (not answering a question), omit the Q: block entirely.
- The **Plan** block uses blockquote format (`>`). Only include it if your response to that prompt contained a plan — either from plan mode (EnterPlanMode/ExitPlanMode) or a structured implementation plan presented for user approval. Preserve the plan content faithfully, including key steps, decisions, and rationale. If there was no plan, omit the block entirely.
- The **Insight** block uses blockquote format (`>`). Only include it if your response to that prompt contained a `★ Insight` section. Copy the insight content faithfully. If there was no insight, omit the block entirely.
- The **Files** line lists all files you created, modified, or deleted in response to that prompt, formatted as inline code. If a prompt didn't result in any file changes (e.g., a clarification question), omit the Files line.

### Step 4: Stage, Commit, and Report

1. Stage the prompt file: `git add prompts/<filename>`
2. Stage the code changes (as you normally would)
3. Create the commit with the message drafted in Step 2. The prompt file and code changes go into the **same commit**.
4. After the commit succeeds, output a summary to the console:

```
Prompt record: prompts/<filename>
  <N> prompts | Topics: <comma-separated list of key topics covered>
```

The topics summary should be a brief list of the main subjects discussed in the prompts (e.g., "user authentication, JWT tokens, logout endpoint").

## Edge Cases

- **Commit fails** (e.g., pre-commit hook): the prompt file is already staged — it will be included automatically when the user retries. Do not create a duplicate.
- **Filename collision**: append `-2`, `-3`, etc. to the summary slug
- **Very long prompts**: preserve full text — do not truncate. Long prompts often contain the most valuable context.
- **Non-ASCII branch names**: transliterate or replace non-ASCII characters with `-` in the filename

