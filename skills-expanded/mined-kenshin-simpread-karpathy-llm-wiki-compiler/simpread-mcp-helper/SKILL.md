---
name: simpread-mcp-helper
description: Search and synthesize SimpRead unread content through the SimpRead MCP tools. Use when Codex needs to find SimpRead items by keyword, tag, or date window; filter results by creation date; fetch snapshots from localhost reading pages; and turn them into grounded reading recaps, topic briefings, timelines, or comparative summaries with per-page localhost citations.
---

# SimpRead MCP Helper Skill Guide

## Overview

Use this skill to turn SimpRead unread items into structured briefings grounded in the local snapshot pages.
Only use SimpRead MCP tools for retrieval. Do not substitute Wikipedia or web browsing when the request is specifically about the user's SimpRead library.

## Core Workflow


### Command modifiers and aliases

- `~x` is a shorthand pattern where `x` represents any single modifier letter. Any LLM receiving `~<letter>` must expand it to `::mcp:-<letter>` before processing. For example: `~r` → `::mcp:-r`, `~a` → `::mcp:-a`, `~m` → `::mcp:-m`. So `查询 星巴克 ~r` is identical to `查询 星巴克 ::mcp:-r`.
- `-r` or `-r 方案` means: keep the original task intent of `xxxx`, but in the final output **replace local snapshot links with original article URLs**.
- Here `xxxx` can be any supported request shape, such as a reading recap, a keyword briefing, a tag briefing, a history briefing, or another valid SimpRead analysis request.
- When `-r` is present, first complete the normal retrieval and analysis flow for `xxxx`, then call `get_unread_by_idx` for every cited local snapshot id and replace the final citation target with the original article URL.
- `-r` is a global output modifier, not a standalone recap mode.
- If the user says only `-r` or `-r 方案` without any base task, ask for or infer the missing base task only if the surrounding context makes it obvious; otherwise default to treating it as an original-URL conversion request for the already referenced items.

Recommended phrasing:

- `今日阅读回顾` → normal recap with local snapshot citations
- `今日阅读回顾 -r` → recap with citations replaced by original article URLs
- `查询标签 AI战争 并生成简报 -r` → tag briefing with citations replaced by original article URLs
- `查询 OpenAI 相关内容并生成简报 -r 方案` → keyword briefing with citations replaced by original article URLs
- `--kami` means: after completing the base task and any citation rewriting, render the final output as a professional HTML document using the kami long-doc template, and save to `outputs/`.
- `--kami` is a cross-environment universal modifier — it does not need `::mcp:` prefix.
- Before executing, check if kami skill is available (read `command/render.md` for the pre-check logic). If not installed, prompt the user to install.
- `--lite` means: render the final output as a lightweight HTML document using `tools/template/lite.html`, zero dependencies, saved to `outputs/`. This is the default rendering mode.
- `--lite` is a cross-environment universal modifier — it does not need `::mcp:` prefix.
- If neither `--lite` nor `--kami` is specified and a rendering modifier is implied, default to `--lite`.
- If `-r` and `--kami` or `--lite` are both present, apply `-r` first (citation rewrite), then the rendering modifier (HTML output).
- `--kami` / `--lite` do not change the retrieval scope or analytical structure — they only transform the final output format.

Recommended phrasing with `--kami`:

- `查询关键词 星巴克 并生成简报 --kami` → keyword briefing rendered as kami HTML
- `今日阅读回顾 --kami` → reading recap rendered as kami HTML
- `查询标签 AI战争 并生成简报 -r --kami` → tag briefing with citations replaced, then rendered as kami HTML

Recommended phrasing with `--lite`:

- `查询关键词 星巴克 并生成简报 --lite` → keyword briefing rendered as lite HTML
- `今日阅读回顾 --lite` → reading recap rendered as lite HTML
- `查询标签 AI战争 并生成简报 -r --lite` → tag briefing with citations replaced, then rendered as lite HTML

### Cross-Environment Command Protocol

When this skill is invoked **together with Wiki commands** (e.g., `/report`), follow these rules:

**衝突說明**：`-r` has different meanings in different environments:

| 环境 | `-r` 含义 |
|------|-----------|
| Wiki 命令 (`/command/*.md`) | `--report` (生成简报) |
| MCP 环境 (本 Skill) | 替换快照链接为原始 URL |

**混用格式**：
- `/report 星巴克 -m ::mcp:-r` → Wiki: Mermaid + MCP: replace citations
- `/report 星巴克 ::mcp:-r -m` → 同上，顺序无关
- `/report 星巴克 -m ~r` → 同上，`~r` 是 `::mcp:-r` 的缩写，效果完全相同

**`::mcp:` 前缀**：When a Wiki command uses `::mcp:` prefix before a modifier, that modifier belongs to this MCP environment.

**自动检测**：当执行 Wiki 命令时，如果检测到需要 MCP 能力（如替换快照链接），自动启用 `-r` 行为。

### 1. Choose the right MCP entry point

Pick the retrieval tool based on the user's query shape:

- `search_content` for keyword searches such as company names, people, products, or concepts.
- `search_tag` for tag-based retrieval such as `历史/少数民族` or `科技史话/AI战争`.
- `get_daily` for time windows such as `today`, `yesterday`, `week`, `last7`, `last30`.
- `get_unread_list` Strictly use this when the user asks for a specific number of unread items (e.g., "Top 5 unread") or a simple unread list without deep analysis.
- `get_unread_by_idx` for snapshot id retrieval such as `http://localhost:7026/reading/1234` `1234` is snapshot id.

### Pagination Handling

When `search_content` or `search_tag` returns paginated results (e.g., "已分为 8 页"), you MUST:

1. Call `get_unread_list` for **ALL pages** to retrieve all titles first
2. Then filter/analyze based on ALL retrieved titles
3. Only call `get_snapshot` for the filtered subset

**Do NOT skip pages** unless the user explicitly limits the scope (e.g., "only check page 1" or "第一页即可").

**Rationale**: To properly "filter within results" (在此结果中筛选), you need visibility into all titles across all pages. Relevant items may not appear on page 1, and titles that seem unrelated may actually contain relevant content (e.g., "星巴克把命运交给了一个卖卷饼的" may discuss CEO changes).

**Complete Flow**:

```
User Command: 查询关键词 星巴克 在此结果中 找出与新任 ceo 相关的内容
                        ↓
            ┌───────────────────────┐
            │   search_content      │
            │           or          │
            │     search_tag        │
            │   (keyword: 星巴克)   │
            └───────────────────────┘
                        ↓
            ┌───────────────────────┐
            │ Returns: 153 items    │
            │ 8 pages, 20 per page  │
            │ Instruction: call     │
            │ get_unread_list 8x    │
            └───────────────────────┘
                        ↓
            ┌───────────────────────┐
            │ Call get_unread_list  │
            │ page=0,1,2,3,4,5,6,7  │
            └───────────────────────┘
                        ↓
            ┌───────────────────────┐
            │ Get ALL titles list   │
            │ (title-based list)    │
            └───────────────────────┘
                        ↓
            ┌───────────────────────┐
            │ Filter CEO-related    │
            │ (search titles for   │
            │  keywords: CEO, 新任, │
            │  换帅, Brian Niccol)  │
            └───────────────────────┘
                        ↓
            ┌───────────────────────┐
            │ Call get_snapshot     │
            │ (only for filtered   │
            │  subset)             │
            └───────────────────────┘
                        ↓
            ┌───────────────────────┐
            │ Output result         │
            │ (format depends on   │
            │  whether "简报" is   │
            │  triggered)          │
            └───────────────────────┘
```

### 2. Filter aggressively before reading snapshots

The search results often include many candidates. Before calling `get_snapshot`:

- keep only items relevant to the user's exact topic
- obey explicit date limits such as `仅整理建立日期为 2026 年以内的内容`
- prefer primary topic matches over tangential mentions
- avoid duplicate or near-duplicate items unless each contributes distinct evidence

When the result set is large, select a focused subset that can support a coherent briefing instead of exhaustively opening everything.

### 3. Fetch the actual content with `get_snapshot`

Search results only provide titles, links, dates, and tags. They are not enough for analysis.
For every item you decide to use in the final briefing, call `get_snapshot` on its numeric id and read the actual content before writing.

### Link replacement rule for `-r`

When the final output contains one or more local snapshot links such as `http://localhost:7026/reading/1234` and `-r` is present:

- treat the numeric suffix after `/reading/` as the snapshot id
- call `get_unread_by_idx` with that snapshot id
- replace the citation target with the returned original article URL
- do this for every cited local snapshot link that appears in the final output
- only replace actual citation links; do not treat unrelated numbers in the body text as snapshot ids

If multiple citations appear, repeat this conversion for each cited snapshot id one by one until all final citation targets are replaced.

If the same `http://localhost:7026/reading/xxx` link appears more than once, call `get_unread_by_idx` only once for that snapshot id and reuse the returned original article URL for every repeated citation target.

### 4. Ground every conclusion in local citations

When writing, cite pages exactly in this format by default:

- `[页面标题](http://localhost:7026/reading/xxx)：说明...`

If `-r` is present, replace `http://localhost:7026/reading/xxx` with the original article URL returned by `get_unread_by_idx`, while keeping the page title and the grounded explanation.

Rules:

- remove a `简悦 | ` prefix if present in the title
- use each page in only one most-relevant section when grouping by theme
- do not cite items you did not open with `get_snapshot`
- when `-r` is present, every cited local snapshot id must be converted to its original article URL via `get_unread_by_idx` before final output
- keep conclusions traceable to one or more cited pages

### Output precedence rules

When multiple output constraints appear together, apply them in this order:

1. Preserve the base task intent of `xxxx`.
2. Preserve any explicitly requested structure such as `严格按照输出规则输出`.
3. Apply `-r` as a citation-target rewrite step, replacing local snapshot links with original article URLs via `get_unread_by_idx`.
4. Apply `--lite` or `--kami` last as an HTML rendering step, converting the final markdown output into a styled HTML file saved to `outputs/`. See `command/render.md` for the full rendering specification. Default to `--lite` if neither is specified.

This means `-r` changes the final citation targets, and `--lite` / `--kami` change the output format, but neither should change the retrieval scope or the analytical structure.

### 5. Match the output mode

Common modes:

- **阅读回顾**: organize by time-window recap and then theme
- **关键词/专题简报**: organize by key actions, strategic tensions, and future outlook
- **历史/知识型主题**: organize by timeline, lineage, phases, and structural transitions

If the user asks for `严格按照输出规则输出`, mirror their requested structure exactly. If `-r` is also present, preserve the requested structure but replace citation targets with original article URLs.

## Writing Guidance

### Reading recap

Use when the user asks for today/yesterday/week style reviews.

Recommended flow:

1. state total item count and coverage areas
2. summarize each selected page once
3. regroup into 2-4 deeper themes
4. close with a synthesis of what changed in that time window

### Briefing Trigger Protocol

When the user mentions `简报`, `生成简报`, or `输出简报`, the final output must use the full Wiki `/report` structure from `command/report.md`, even if retrieval happens in this MCP workflow.

Required sections: `核心架构图`, `关键演进/事实表`, `深度逻辑拆解`, `简报总结与行动建议`.

`-m` uses `Mermaid`; `-a` uses `ASCII`; `-r` replaces local snapshot links with original article URLs; `::mcp:-r` forces MCP link rewriting in mixed Wiki/MCP requests; `--lite` renders as lightweight HTML (default); `--kami` renders as kami HTML.

If the user asks for a time-window recap without `简报`, use the normal recap workflow; if `简报` is also requested, keep recap retrieval but use the full `/report` structure for output.

### Output Mode Selection

Based on whether the user's command contains specific keywords, choose different output formats:

| Trigger Keywords | Output Format | Format Source |
|:---|:---|:---|
| `简报`, `生成简报`, `输出简报` | Wiki `/report` structure | `command/report.md` |
| None of the above | Format rules from returned content | Output Format from `search_content` or `search_tag` |

**Examples**:

- `查询关键词 英伟达 并生成简报` → Use `/report` structure (core architecture diagram + key evolution/facts table + deep logic breakdown + briefing summary and action recommendations)
- `查询关键词 英伟达` → Use format rules from returned content
- `查询标签 星巴克` → Use format rules from returned content
- `今日阅读回顾` → Use format rules from returned content
- `今日阅读回顾 生成简报` → Use `/report` structure

**Key Differences**:

1. **With "简报" keyword**: Output a structured analysis report including visual architecture diagrams, timeline tables, deep breakdowns, and other complete sections
2. **Without "简报" keyword**: Output a lightweight summary, with format defined by the Workflow in `search_content` or `search_tag` response

### History / evolution briefing

Use when the user asks for a long historical arc.

Recommended flow:

1. identify the root lineage or earliest documented layer
2. trace major transitions in sequence
3. separate political succession from ethnogenesis when needed
4. explain not only who replaced whom, but what institutional or cultural continuity remained

## Date Filtering Rules

When the user gives a temporal constraint, enforce it before snapshot retrieval and again before writing.

Examples:

- `仅整理建立日期为 2026 年以内的内容` means include only items whose listed creation date is in 2026
- `2026 年 4 月之后` means include only items dated after 2026-04-30
- `近七日` should use `get_daily` with the relevant time window instead of ad hoc keyword search when possible

If a result list mixes valid and invalid dates, explicitly exclude the out-of-range items from analysis.

## Recommended Selection Heuristics

When too many results match:

- prioritize recency for fast-moving topics like AI companies
- prioritize canonical overview pieces plus a few high-signal supporting pieces
- include at most one or two items for each repetitive sub-angle unless the differences matter
- prefer articles with concrete facts, dates, metrics, or strategy details over vague commentary

## Reference File

For reusable patterns and exact command mapping, see `references/patterns.md`.