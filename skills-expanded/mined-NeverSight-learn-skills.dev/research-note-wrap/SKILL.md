---
name: research-note-wrap
description: Use when the user wants to summarize research or analysis into a readable Obsidian markdown note, such as 总结调研, 输出结论, 总结分析, 输出笔记, 调研纪要, 分析纪要, 会话结论, or when asking to summarize today's sessions about a topic. Use for current-session summaries by default, and for cross-session topic summaries when the user mentions 今天会话 or gives a topic scope.
---

# research-note-wrap

## Overview

Summarize the current session, or today's related sessions for a given topic, into an Obsidian Markdown note that is easy to review later. Prioritize core problems, comparative analysis, and clear conclusions over code detail or process narration.

## Core Rules

- Write in Simplified Chinese by default.
- Prioritize logical conclusions over coding details.
- Do not produce a chronological 流水账.
- Use tables first when comparing multiple problems, hypotheses, conclusions, impacts, or next actions.
- After the tables, provide a short `关键结论` section.
- Only include code-level details when they are truly necessary to support the conclusion.
- If you mention a file, function, method, or code path, explain in Chinese:
  - what it does
  - why it matters
  - how it supports the conclusion
- Default to writing the note file after confirmation; do not stop at chat-only output unless the user explicitly asks not to write a file.

## Scope Decision

### Default scope

If the user says things like:
- 总结调研
- 输出结论
- 总结分析
- 输出笔记
- 调研纪要
- 分析纪要
- 会话结论

Then summarize the **current session only**.

### Cross-session scope

If the user says things like:
- 总结今天会话关于 xx 的分析
- 汇总今天关于 xx 的调研
- 总结今天相关会话中的 xx 问题

Then collect **today's related sessions** about the given topic and synthesize them into one note.

If the user explicitly provides another time range, follow that range. Otherwise, `近期` defaults to **当天**.

## Output Location Decision

Before writing the file:

1. Check whether the current project's `AGENTS.md` explicitly defines a default output directory for research / analysis summary notes.
2. If `AGENTS.md` already defines it, follow that path directly.
3. If it does not define a path, ask the user for the output directory the first time.
4. Once the user gives a path, use it for the current task. Suggest adding it to `AGENTS.md` if this is a recurring workflow.

## Confirmation Workflow

Do not write the file immediately after the first draft. Use this confirmation sequence:

### Step 1: Draft the main problems

Extract and compress the discussion into a high-density problem summary. Prefer a table like this:

```md
## 问题对比表
| 问题 | 现象/信号 | 核心判断 | 当前结论 | 影响 |
|---|---|---|---|---|
| 问题 A | ... | ... | ... | ... |
```

Then ask the user to confirm whether these are the right **主要问题**.

### Step 2: Draft the conclusions

After the user confirms the problem framing, present the conclusions. Prefer a compact table first, then a short conclusion block:

```md
## 结论对比表
| 主题 | 结论 | 依据 | 风险/边界 |
|---|---|---|---|
| xx | ... | ... | ... |

## 关键结论
1. ...
2. ...
3. ...
```

Then ask the user to confirm whether these are the right **结论**.

### Step 3: Write the note file

Only after both confirmations:
- finalize title
- finalize file path
- write the markdown file
- report the saved path back to the user

## Output Structure

Use this structure by default. Keep it concise and dense.

```md
---
title: <标题>
date: <YYYY-MM-DD>
project: <项目名或路径>
tags: [research, summary]
source: <current-session | today-topic-synthesis>
---

# <标题>

## 问题对比表
| 问题 | 现象/信号 | 核心判断 | 当前结论 | 影响 |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## 结论对比表
| 主题 | 结论 | 依据 | 风险/边界 |
|---|---|---|---|
| ... | ... | ... | ... |

## 关键结论
1. ...
2. ...
3. ...

## 必要实现位点（仅在真的重要时）
| 位点 | 逻辑/作用 | 为什么关键 |
|---|---|---|
| `path:line` / `symbol` | 它负责什么 | 它如何支撑结论 |

## 未决项 / 后续建议
| 项目 | 说明 |
|---|---|
| ... | ... |
```

## File Naming

Default filename format:

```text
YYYY-MM-DD-<topic>.md
```

Examples:
- `2026-03-30-dsa-sidecar-pinned-ref.md`
- `2026-03-30-hqchart-data-contract.md`
- `2026-03-30-session-research.md`

If the topic is unclear, use a short neutral fallback such as `session-research`.

## Follow-up Research After Initial Output

If the user says things like:
- 再调研 xx 输出到文件中去
- 补充分析 xx 并写入笔记

Then:

1. Reuse the current note file by default.
2. Add a new section such as:

```md
## 追加专题：xx
```

3. Only create a new file if the user explicitly asks for a separate note.

## Writing Guidance

### Good
- Compress repeated discussion into one row or one conclusion.
- Prefer contrast and synthesis.
- Keep wording human-readable and Chinese-first.
- Explain technical references in plain Chinese.

### Avoid
- Long process transcripts
- Tool chatter
- Repeating the same conclusion in multiple bullets
- Dumping file paths or function names without explanation
- Overusing multi-level bullet lists when a table is clearer

## Final Checklist

Before writing the file, verify:

- The scope is correct: current session or today's related sessions.
- The output path follows `AGENTS.md`, or has been explicitly confirmed with the user.
- The user has confirmed both:
  - 主要问题
  - 核心结论
- Tables carry the dense comparison content.
- `关键结论` appears after the tables.
- Code-level references, if any, are explained in Chinese.
- The filename matches `YYYY-MM-DD-topic.md`.


