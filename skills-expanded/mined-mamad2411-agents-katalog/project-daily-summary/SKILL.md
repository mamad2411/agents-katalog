---
name: project-daily-summary
description: Use when the user wants a same-day Codex work summary grouped by project folder or repository, combining today's Codex sessions, extracted plans, completed items, commits, and uncommitted changes, or says 项目日报, 日报, 今日工作总结, 按项目总结今天, 总结今天所有 Codex 会话, 总结今天会话+提交+未提交改动.
---

# project-daily-summary

Summarize today's Codex work by project. Use global Codex session transcripts as the primary evidence source, then enrich with git commits and uncommitted changes. Prioritize plans and final outcomes over process chatter.

## Core Rule

Do not produce a chronological 流水账.
Do not summarize reasoning noise.
Always summarize by **project** and then by **major workstream**.

## Source Priority

1. `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
2. `~/.codex/history.jsonl`
3. `<project>/.specstory/history/` if it exists
4. `git log`, `git status --short`, `git diff --stat`

## Important Environment Assumption

In this Codex environment, session transcripts are primarily stored under:

```text
~/.codex/sessions/YYYY/MM/DD/
```

Do **not** assume each project stores its own sessions under `<project>/.codex/sessions/`.

Map sessions back to projects using:

- `session_meta.payload.cwd`
- then normalize with `git -C <cwd> rev-parse --show-toplevel`
- if git root cannot be resolved, fall back to `cwd`

## Scope

### Default scope

Summarize **all projects** that appear in today's Codex sessions.

### If the user provides folders

Summarize only those folders or repositories.

## Workflow

### Step 1: Determine today's local date

Use the local machine date, not UTC.

Build the session directory path:

```text
~/.codex/sessions/YYYY/MM/DD/
```

If the directory does not exist, report that no Codex sessions were found for today and stop.

### Step 2: Load today's session transcripts

Read all:

```text
rollout-*.jsonl
```

For each session, extract from the first `session_meta` line:

- session id
- cwd
- branch
- commit hash
- repository url
- whether it is a subagent session
- parent thread id if present

### Step 3: Group by project

For each session:

1. Try:
   ```bash
   git -C <cwd> rev-parse --show-toplevel
   ```
2. If that fails, use `cwd` as the project key.

Output one section per project, not one section per raw session.

### Step 4: Handle subagents correctly

Many sessions may be spawned subagents. Do not list each child session as a separate user-facing item.

Use this policy:

- Main sessions are the primary narrative units.
- Subagent sessions are supporting evidence only.
- If a same-day parent session exists, merge the subagent into the parent workstream.
- If the parent session is missing, keep the subagent as orphan evidence and merge it into the nearest matching project workstream instead of listing it standalone.

### Step 5: Extract structured signals from each session

#### Goal

Prefer the first meaningful `user_message`.

Rewrite it into one short Chinese objective sentence.

#### Plan

Prefer the **last** `update_plan` call in the session.

Summarize it into:

- 已完成
- 进行中
- 待处理

Keep only high-level plan items.

#### Completion

Prefer the final `agent_message` where:

- `phase == final_answer`

If present, extract sections such as:

- `STATUS`
- `CHANGED_FILES`
- `TESTS_RUN`
- `NOTES`

Convert them into concise outcome statements.

#### Fallback when no final answer exists

If no final answer exists, fall back to:

- latest plan state
- changed files if detectable
- git evidence
- latest meaningful assistant message

### Step 6: Ignore process noise

Ignore by default:

- reasoning items
- token counts
- most system and developer prompt content
- most intermediate tool chatter
- repeated subagent scaffolding

Keep only:

- user goal
- extracted plan
- final outcome
- changed files
- tests run
- risks or blockers

### Step 7: Merge sessions into major workstreams

Within each project, merge multiple sessions into a few major workstreams.

Use these signals:

- same branch or worktree
- same or similar user goal
- overlapping changed files
- same plan file
- same parent thread chain
- same feature, bug, review, or skill topic

Target **1 to 5 workstreams per project**, not dozens of tiny entries.

### Step 8: Add git evidence

For each project, run:

```bash
git -C <repo> log --since="YYYY-MM-DD 00:00" --until="YYYY-MM-DD 23:59" --pretty=format:"%h %s"
git -C <repo> status --short
git -C <repo> diff --stat
```

Use this to produce:

- 今日 commits
- 当前未提交改动

Do not claim commits came from Codex unless the session evidence supports that inference.

### Step 9: Optional SpecStory supplementation

If `<project>/.specstory/history/` exists, use it only as a supplementary source.

Do not let SpecStory override Codex transcript evidence when they conflict.

### Step 10: Optional closeout appendix

If the user also wants a **same-day all-repo closeout appendix** in addition to the daily summary, you may optionally invoke `worktree-closeout`.

Use it only as an additive supplement:

- `project-daily-summary` remains the primary same-day, by-project report
- `worktree-closeout` is optional and only for the appendix view
- use this only for **same-day all-repo** closeout appendix scenarios
- if the user wants a standalone closeout scan, or a repo-scoped closeout scan, use `worktree-closeout` directly instead of this skill
- if the user did not ask for the appendix, skip this step

When used, append the result as one extra appendix, for example:

```md
## 附录：Closeout / 未收口 Worktree / 分支收口状态
- 扫描范围：当天所有 repos
- 需优先收口的 repo / branch / worktree：
- 建议后续动作 / artifact 路径：
```

Do not replace the main daily summary structure with the closeout appendix.

## Output Format

```md
# Codex Project Daily Summary
日期：YYYY-MM-DD

## 总览
- 项目数：
- 会话数：
- 主要推进：
- 今日仍未收尾：

## 项目：<repo-or-folder>
- 分支 / 仓库：
- 今日 Codex 目标：
- 今日计划提炼：
- 今日完成事项：
- 今日 commits：
- 当前未提交改动：
- 风险 / 未完成项：
- 建议下一步：

## 项目：<repo-or-folder>
...

## 跨项目总结
- 今天最重要的推进
- 重复出现的问题
- 明天最值得先做的 1-3 件事

## 附录：Closeout / 未收口 Worktree / 分支收口状态（可选）
- 仅当用户额外要求当天所有 repo 的 closeout / worktree / 分支收口状态时添加
- 可附 `worktree-closeout` 的摘要、优先级、artifact 路径
```

## Writing Rules

- Write in Chinese.
- Group by project first.
- Lead with results, not process.
- Distinguish clearly between:
  - 会话计划
  - 已完成事项
  - 已提交内容
  - 未提交改动
- Do not repeat subagent outputs separately if already merged.
- If evidence is missing, say so explicitly.
- If a project has no git repository, say that commit and uncommitted sections are unavailable.


## Default Save Location

For public distribution, do **not** hardcode a personal sync folder.

Use this policy instead:

1. If the current project's `AGENTS.md` defines a daily-summary output directory, follow it.
2. Otherwise, ask the user for the output directory the first time.
3. Use a configurable filename pattern such as:

```text
YYYY-MM-DD-project-daily.md
```

If the user does not explicitly override the path or filename, use this location and naming convention automatically.

If the user explicitly says not to save the report, skip file creation and return the summary in chat only.
## Trigger Phrases

- 项目日报
- 日报
- 今日工作总结
- 按项目总结今天
- 总结今天所有 Codex 会话
- 总结今天会话+提交+未提交改动
- codex project daily summary





