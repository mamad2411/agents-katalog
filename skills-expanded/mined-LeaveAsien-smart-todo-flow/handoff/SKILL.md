---
name: handoff
description: >-
  Use when capturing decisions, implicit knowledge, in-progress work, and
  references to TODO or git that would otherwise be lost between sessions.
---

# Handoff

Generate `HANDOFF.md` with the context that would be lost between the current session and the next session. Do not duplicate content already in `TODO.md`, `CHANGELOG.md`, or git history; reference those sources instead.

# Information Source

Default to **conversation context only**: what was discussed, committed, decided, and left open during the current session.

Only read external sources such as `git log`, `TODO.md`, `PLAN.md`, and `git status` when conversation context is insufficient. For example, read them when handoff is requested at the start of a session to capture prior state.

# Generating HANDOFF.md

## Sections

### 本次完成

List commit hashes only, one per line, without re-summarizing:

```markdown
## 本次完成

- f64cc21 fix(plugin): 修正安装命令路径
- c450434 docs: 安装文档更新
```

If there are uncommitted staged changes, note them as `(uncommitted)`.

### 进行中 / 未完成

List only work that is actually in progress: partially done, blocked, or represented by uncommitted changes. Do not list TODO items that have not started; they are already in `TODO.md`.

```markdown
## 进行中 / 未完成

- dev 分支 6 个 commit 未推远程，未合并 master
- git status: HANDOFF.md 未提交
```

### 待决定

This is the most important section. Capture only decisions genuinely discussed but not finalized. Do not invent hypothetical decisions or list topics that were never raised.

- Options considered and why no conclusion was reached
- Trade-offs the user is still weighing
- Questions raised but not answered

```markdown
## 待决定

- 插件发布节奏：用户想先本地验证再推远程，但完整安装流程仍待真实环境确认
```

If nothing was discussed but left open, write `无`. Never pad this section.

### 关键上下文

This is the second most important section. Capture ideas, design rationale, and decision context that informed choices but are not recorded in code or docs:

- Brainstorming ideas that were not implemented
- Why one option was chosen over another
- User preferences or constraints expressed in conversation
- Strategic thinking about project direction

```markdown
## 关键上下文

- Commit 规范选 Conventional Commits 而非自定义格式，主要为了可读性；自动 changelog/版本号工具链暂不作为当前目标
- Handoff 设计原则：引用不重复，重点写盲区；本次完成用 git hash，进行中引用 TODO 项号
```

If there is no such context, write `无`.

### 备注

Capture technical gotchas, runtime quirks, and workarounds discovered during the session. These are reference notes for future debugging, not project-direction context.

```markdown
## 备注

- PowerShell 默认编码可能影响中文输出，读取 markdown 时优先显式使用 UTF-8
```

This section is optional; omit it when there is nothing to note.

### 下一步

Provide one to three brief, actionable bullets:

```markdown
## 下一步

- 本地测试插件安装路径
- 同步安装和升级说明
```

### 上下文恢复（可选）

Omit the `上下文恢复` section by default. Include it only when the user explicitly requests a handoff with context recovery, or chooses the recovery version while reviewing the draft.

Write a brief, execution-ordered recovery path so that following them from top to bottom restores the working context: the goal, progress, design rationale, pending decisions, and next action. Do not impose a fixed item limit; use as many steps as needed, but keep every step concise.

For each step, prefer a concrete reference and state why the next session should read it:

- A specific section or item in `TODO.md`, `PLAN.md`, or `CHANGELOG.md`
- A commit or commit range
- `git status` or a focused `git diff`
- A relevant file or another section of `HANDOFF.md`

Only add a small amount of explanatory text when references cannot preserve the necessary implicit context. Do not repeat content from `本次完成`, `进行中 / 未完成`, `待决定`, `关键上下文`, or `下一步`.

The final step must tell the next session to summarize what it recovered and wait for the user's confirmation before executing any work.

```markdown
## 上下文恢复

1. Read `PLAN.md` section "Current phase" to recover the goal and scope.
2. Read `TODO.md` item 3 and `git diff -- src/state.js` to recover current progress and the unfinished implementation.
3. Read `HANDOFF.md` sections `待决定` and `关键上下文` to recover open choices and design rationale.
4. Read `HANDOFF.md` section `下一步` to identify the first action; summarize the recovered context and wait for user confirmation before executing it.
```

# User Interaction

Treat this workflow as internal instructions; do not copy it into `HANDOFF.md`.

`Ask exactly once` applies only to the one combined choice for the same unchanged draft. If the user chooses `修改草稿`, apply the requested changes, show the full modified draft, then start a new confirmation round with the menu appropriate to that revision. Write `HANDOFF.md` only after the user confirms the version currently shown.

For an ordinary handoff request:

1. Gather the minimum context needed and draft the full standard `HANDOFF.md` in the conversation without `上下文恢复`.
2. If valid, concrete recovery references exist, show a clearly labeled preview of only the optional recovery section outside the standard draft. Make clear that it is not included by default. Do not offer a vague or empty preview when no valid references exist.
3. When the recovery preview is shown, ask with one combined choice: `确认（标准版） / 确认并加恢复 / 修改草稿`.
4. If the user confirms the already previewed recovery version, use that preview. Do not show the full draft a second time.
5. Without a valid recovery preview, never offer the recovery option. Ask only: `确认（标准版） / 修改草稿`.

If the user explicitly asks for context recovery in the initial request, include `上下文恢复` in the full draft and do not present a separate optional preview. Ask with one combined choice: `确认（带恢复版） / 修改草稿`.

# Rules

- Always overwrite `HANDOFF.md`; never append, because it represents the current session state
- Keep it short and reference `TODO.md`, `CHANGELOG.md`, or git instead of repeating them
- Prioritize `待决定` and `关键上下文`; if both are empty, prompt the user to consider what the next session should know
- Add the session date and topic below the heading: `> 本次会话：YYYY-MM-DD · topic`
