---
name: idea-novelty
description: Check novelty of research idea candidates against recent literature using local notes and MCP-backed literature/web search. Use before ranking or refining ideas.
argument-hint: "[idea-or-candidate-file] [--run-dir path]"
---

# Idea Novelty

Check whether proposed ideas are actually novel: **$ARGUMENTS**.

Use `${IDEA_STAGE_DIR}/IDEA_CANDIDATES.md` if present.

## Output Language

All user-facing text and all saved artifacts must be in **Chinese** by default. Keep official paper titles, venues, author names, DOI/arXiv IDs, benchmark names, and file paths unchanged when needed. Follow `shared-references/output-language.md`.

Resolve `IDEA_STAGE_DIR` by following `shared-references/run-directory.md`.

## Claim Extraction

For each candidate, extract 3-5 novelty-bearing claims:

- problem setting
- mechanism
- training/evaluation protocol
- claimed insight
- expected contribution

## Search Protocol

For every claim:

1. Search exact mechanism terms.
2. Search problem plus method-family terms.
3. Search benchmark/dataset plus intervention terms.
4. Search broader synonyms and older terminology.
5. Check the last 6-12 months of arXiv or available literature sources.

Use MCP literature tools when available. Acceptable sources include arXiv, Semantic Scholar, OpenAlex, Zotero, Obsidian, local PDF search, general web search, or any user-provided MCP.

## Novelty Verdicts

Use these verdicts:

- **高**：没有发现非常接近的 prior work，技术差异清晰。
- **中**：相关工作存在，但 idea 仍有可辩护的新机制、新设定或新发现。
- **低**：大概率只是增量，或已有工作已经覆盖。
- **阻断**：发现接近 prior work，可能实质上覆盖该 idea。
- **未知**：来源不可用或证据不足。

## Output

Write `${IDEA_STAGE_DIR}/NOVELTY_REPORT.md`:

```markdown
# 查新报告

## 总结
| Idea | 结论 | 分数 | 最近 prior work | 建议 |
|------|---------|-------|--------------------|----------------|

## 分 Idea 分析

### [Idea 标题]
- 已检查的核心 claim：
- 使用的检索 query：
- 最近 prior work：
- 重合点：
- 差异点：
- 新颖性风险：
- 定位建议：
- 结论：

## 被阻断或偏弱的 Idea
| Idea | 原因 |
|------|--------|
```

## Rules

- Be conservative. Months of work can be wasted by optimistic novelty.
- Do not fabricate papers, arXiv IDs, venues, or author lists.
- Mark unverified references explicitly.
- If the method is not novel but the experiment/finding could be novel, say that distinction clearly.
