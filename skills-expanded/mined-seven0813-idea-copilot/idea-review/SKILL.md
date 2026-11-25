---
name: idea-review
description: Run a harsh external review of research idea candidates. Use after novelty checking or when the user wants PI/reviewer-style critique, prioritization, and go/no-go decisions.
argument-hint: "[idea-candidates-or-selected-idea] [--run-dir path]"
---

# Idea Review

Critically review research ideas for: **$ARGUMENTS**.

Use:

- `${IDEA_STAGE_DIR}/IDEA_CANDIDATES.md`
- `${IDEA_STAGE_DIR}/NOVELTY_REPORT.md`
- `${IDEA_STAGE_DIR}/LANDSCAPE.md`

## Output Language

All reviewer prompts, user-facing summaries, and saved artifacts must request or use **Chinese** by default. Keep official names, paper titles, benchmark names, model names, and file paths unchanged when needed. Follow `shared-references/output-language.md`.

Resolve `IDEA_STAGE_DIR` by following `shared-references/run-directory.md`.

## Reviewer Setup

Use an external reviewer backend when available. The reviewer must be independent from the executor model family when possible.

Send files or raw candidate text. Do not send a persuasive summary that hides weaknesses.

External reviewer is enabled by default. Treat `/idea-copilot` or `/idea-review` invocation as permission to send the minimized review package to the configured reviewer MCP, unless the user passed `--no-external-review` or explicitly said not to send content outside the executor. Follow `shared-references/external-review.md`.

Before any external reviewer call, write `${IDEA_STAGE_DIR}/REVIEW_PACKAGE.md`:

```markdown
# 外部评审包

## 外发范围
- 候选 idea：
- 查新结论：
- Landscape 摘要：
- 用户约束：

## 不外发内容
- 原始 PDF 全文
- notes/、papers/、literature/ 全量内容
- API key、token、隐藏配置

## 需要评审的问题
1. 哪些 idea 值得继续？
2. 哪些 idea 应该合并、暂缓或淘汰？
3. 每个 idea 最强拒稿理由是什么？
```

Also write `${IDEA_STAGE_DIR}/REVIEW_AUTHORIZATION.md`:

```markdown
# 外部评审授权记录

**默认策略**：Idea-Copilot 默认启用外部 reviewer。
**用户是否禁用外部评审**：否
**Reviewer 后端**：
**计划发送文件**：
**明确不发送**：
**时间**：
```

Review scope:

- Default: review every serious candidate in `${IDEA_STAGE_DIR}/IDEA_CANDIDATES.md`.
- If there are more than 6 serious candidates or the reviewer prompt becomes too long, review at least the top 3 plus any user-selected candidates.
- Do not review only Candidate A unless the user explicitly requested single-candidate review.
- If only one candidate is reviewed because of tool limits, state that limitation clearly in `REVIEW_REPORT.md` and mark the ranking as provisional.

Reviewer persona:

> You are a top-venue area chair and a demanding PI deciding which idea deserves one student's next 1-3 months. Be skeptical, specific, and action-oriented.

## Review Questions

Ask the reviewer:

1. Which ideas are top-venue plausible and why?
2. Which ideas are already too close to prior work?
3. What is the strongest rejection argument for each idea?
4. What minimum experiment would change your mind?
5. Which idea has the best risk-adjusted expected value?
6. What framing would make the best idea sharper?
7. What should be killed immediately?
8. Are any lower-ranked candidates more promising than the current favorite after considering novelty and feasibility?

## Scoring

Score each idea from 1-10 on:

- novelty
- importance
- mechanism clarity
- feasibility
- evidence path
- project story
- risk-adjusted priority

Then assign:

- **GO（继续细化）**：现在值得进入 refine
- **MAYBE（备选/合并）**：保留为备选或与其它 idea 合并
- **KILL（淘汰）**：除非 scope 改变，否则不再投入

## Output

Write `${IDEA_STAGE_DIR}/REVIEW_REPORT.md`:

```markdown
# Idea 评审报告

## PI 建议
- 最佳 idea：
- 备选：
- 应淘汰：
- 理由：
- 本轮评审覆盖范围：

## 评分表
| Idea | 新颖性 | 重要性 | 可行性 | 论文故事 | 总分 | 结论 |
|------|---------|------------|-------------|-------|---------|---------|

## 拒稿论点
### [Idea]
- 最强拒稿理由：
- 最小修复：
- 能改变判断的实验：

## 最终排序
1. ...
```

Also write `${IDEA_STAGE_DIR}/FINAL_IDEA_RANKING.md` with a concise ranked list for user discussion.

Also write `${IDEA_STAGE_DIR}/REVIEW_RAW.md` containing the raw external reviewer prompt and raw response when an external reviewer was used:

```markdown
# 外部评审原文

## 外部评审后端
- 工具：
- 模型：
- threadId / jobId：

## 发送给评审器的提示词
[发送给 reviewer 的原始 prompt]

## 评审器原始回复
[reviewer 原始回复，可保留英文或原文]

## 中文摘要与结论
- 评审器主要判断：
- 对排序的影响：
- 必须修正的问题：
```

## Rules

- Reviewer feedback must produce decisions, not just comments.
- Prefer killing weak ideas early.
- If all candidates are weak, recommend regenerating with a narrower landscape gap.
- External reviewer output may be invisible in the chat UI because MCP calls return through the tool layer. Preserve the raw prompt/response in `REVIEW_RAW.md` so the user can inspect it.
- If the host blocks the MCP call with an approval/security warning, do not bypass it. Mark the review as provisional, explain that the workflow defaults to external review, and ask the user to explicitly authorize sending `${IDEA_STAGE_DIR}/REVIEW_PACKAGE.md` to the chosen reviewer if they want to retry.
