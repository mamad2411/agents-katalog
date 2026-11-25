---
name: idea-landscape
description: Map the literature and research landscape for idea creation. Use before brainstorming or when the user asks what has been done, what gaps exist, or where a field is moving. Supports local papers, notes, and MCP-backed web/literature search.
argument-hint: "[research-topic] [--run-dir path]"
---

# Idea Landscape

Build a detailed but idea-oriented research landscape for: **$ARGUMENTS**.

## Output Language

All user-facing text and all saved artifacts must be in **Chinese** by default. Keep official paper titles, benchmark names, model names, file paths, and commands unchanged when needed. Follow `shared-references/output-language.md`.

Resolve `IDEA_STAGE_DIR` by following `shared-references/run-directory.md`.

## Inputs

Check, in order:

1. user prompt and constraints
2. explicit `--ref`, `reference:`, or `--brief` argument if present
3. `RESEARCH_IDEA_BRIEF.md` or `RESEARCH_BRIEF.md`
4. `papers/`, `literature/`, and `notes/` in the current project
5. notes from Zotero, Obsidian, or other MCPs if available
6. web/literature MCP search if available

## Search Protocol

Use at least five query formulations:

- direct method terms
- problem-focused terms
- benchmark or dataset terms
- closest-system terms
- failure-mode terms

Prefer recent top-venue and arXiv work from the last 24 months, but include foundational work when it defines the problem.

For each source type, state how it was accessed:

- **local**: files under `papers/`, `literature/`, `notes/`, or explicit paths.
- **MCP**: Zotero, Obsidian, Semantic Scholar, arXiv, OpenAlex, Gemini, Exa, or other configured MCP tools.
- **web**: host-provided web search or browser/search tool.
- **unavailable**: source requested but no tool is available.

## Landscape Axes

Write the landscape around these axes:

- **Problem clusters**: what subproblems exist?
- **Method families**: what approaches dominate?
- **Evaluation norms**: datasets, metrics, baselines, and typical evidence.
- **Known limitations**: what papers admit they cannot do.
- **Contradictions**: where papers disagree.
- **Boundary conditions**: where methods break.
- **Changed assumptions**: what has changed recently in compute, models, tooling, data, or regulation.
- **Open gaps**: actionable holes that can become ideas.

## Output

Write `${IDEA_STAGE_DIR}/LANDSCAPE.md`:

```markdown
# 研究版图

**主题**：
**日期**：
**使用来源**：

## 总览
[8-12 bullets, including what is known, what is contested, and what changed recently]

## 输入与来源
| 来源类型 | 具体来源 | 是否可用 | 备注 |
|---------|----------|----------|------|

## 主要方向
| 方向 | 代表工作 | 核心思路 | 局限 |
|-----------|---------------------|-----------|------------|

## 关键论文/系统卡片
### [论文/系统名称]
- 解决的问题：
- 核心机制：
- 使用的数据/benchmark：
- 主要证据：
- 作者承认或可见的局限：
- 对本项目的启发：

## 机会缺口
| 缺口 | 对应失败模式 | 为什么重要 | 为什么现在可做 | 最近 prior work | 置信度 |
|-----|----------------|------------|----------------|------------------|--------|

## 检索记录
| Query | 来源 | 命中证据 | 用途 |
|-------|------|----------|------|

## 审稿人敏感风险
- [risk]

## Idea 种子
- [seed derived from a real gap]
```

## Rules

- Separate verified papers from memory-based impressions.
- If a source cannot be queried, mark it as unavailable instead of pretending coverage.
- Make the landscape detailed enough to justify idea generation. It is not a full related-work section, but it should preserve the evidence trail that led to each gap.
