---
name: ai-efficiency-audit
description: Audit a person's or team's weekly workflow, identify which tasks AI can realistically take over, and produce an evidence-based, manager-ready efficiency proposal with hours-saved ranges and a two-week pilot plan. Use this skill whenever the user mentions AI efficiency pressure from leadership, or says any of these — "提效", "降本增效", "老板让用AI", "老板天天提AI", "领导要我们用AI", "怎么向领导/老板证明AI有用", "我的工作哪些能让AI做", "AI能帮我自动化什么", "哪些活能交给AI", "向上汇报AI成果", "做个AI提效方案", workflow automation audit, "which parts of my job can AI do", building a business case for AI adoption, estimating hours saved or ROI from AI tools, or needing a pilot plan / proposal to introduce AI into a team. Also trigger when the user pastes their weekly tasks and asks what to automate.
license: MIT. Part of ZAOQI Blueprints (造器图纸库) — https://f-tiger.github.io/zaoqi-blueprints/blueprints/16?utm_source=skill&utm_medium=ai-efficiency-audit
---

# 提效证据生成器 · AI Efficiency Audit

> 造器图纸 #16 · 审计类工具 · 难度 ★★☆
> 下次老板提 AI 提效,方案你先拍在桌上。

This skill turns vague "we should use AI" pressure into an auditable, defensible
efficiency case. It inventories the user's real workflow, scores each task for
automation potential with an explicit rubric, quantifies hours saved with honest
ranges (never promises), and produces a manager-ready one-page proposal with a
pilot plan and rollback conditions. As a final step it can **forge the audit into a
standalone team self-check tool** (造器模式).

The credibility of the output depends on three disciplines. Follow them strictly:

1. **Baseline first** — never claim savings without first establishing current
   time spent. No baseline, no number.
2. **Ranges, not promises** — all savings are estimated as conservative–optimistic
   ranges with stated assumptions.
3. **Pilot before rollout** — every proposal ends in a small reversible pilot with
   pre-agreed success metrics, not a big-bang adoption.

## Workflow

### Stage 1 — Workflow intake (建立基线)

Collect the task inventory. Two modes, let the user pick:

- **快速模式 (5 minutes)**: Ask the user to brain-dump their typical week in plain
  language. You extract the task list yourself, then confirm it back as a table.
- **审计模式 (recommended for team proposals)**: Walk through the structured
  inventory, one category at a time: 例行产出 (reports, emails, docs) → 信息处理
  (reading, summarizing, searching) → 协调沟通 (meetings, follow-ups, status syncs)
  → 核心专业工作 → 救火与例外处理.

For every task capture four fields. If the user cannot estimate time, help them
reconstruct it from last week's calendar rather than letting them guess:

| 字段 | 示例 |
|------|------|
| 任务 | 整理周会纪要并分发 |
| 频率 | 每周 1 次 |
| 单次耗时 | 45 分钟 |
| 当前痛感 (1–5) | 4 |

Do not proceed to Stage 2 with fewer than 5 tasks or without time estimates —
an audit on guesses produces a proposal that dies in the first question.

### Stage 2 — Score and classify (审计)

Read `references/audit-framework.md` and score every task on the five dimensions
(重复度 / 规则化 / 输入输出标准化 / 判断密度 / 出错代价), then assign each task an
automation level:

- **L0 保留人工** — high judgment or high error cost; recommend AI 不碰
- **L1 AI 辅助** — human drives, AI accelerates (drafting, summarizing, searching)
- **L2 人审环节** — AI produces, human reviews before anything ships
- **L3 全自动** — AI runs end-to-end; only for low-risk, fully standardized tasks

Compute for each L1–L3 task: 周节省工时区间 (conservative–optimistic), 实施成本
(S/M/L), 回本周期. Formulas and the honesty rules for estimates are in the
framework file — follow them exactly, including the mandatory 折减系数.

### Stage 3 — Deliver the audit report

Output in this structure, in the user's language:

```
📋 提效审计 · [角色/团队名]

一、基线
  每周总工时盘点:X 小时,其中可审计任务 Y 项,合计 Z 小时

二、审计表(按节省潜力排序)
  | 任务 | 等级 | 周节省(保守–乐观) | 实施成本 | 出错代价 | 建议 |

三、Top 3 速赢项(只选 L1/L2、成本 S、两周内可见效的)
  每项给:具体做法(用什么工具/提示词/流程)→ 试点方案 → 衡量指标

四、不建议自动化清单
  明确列出 L0 任务和理由 —— 这一节是方案可信度的来源,不可省略

五、合计
  保守口径:每周节省 A 小时(约 B%);乐观口径:C 小时
  关键假设:[逐条列出]
```

### Stage 4 — Forge the proposal (老板版文档)

Ask whether the user wants the manager-facing version. If yes, read
`references/proposal-template.md` and generate the one-page memo following its
structure: 现状基线 → 提案 → 收益区间与假设 → 风险与回滚条件 → 两周试点计划。

Rules for the memo:
- One page. Managers approve pilots, not essays.
- Lead with the baseline, not the technology. "我们每周在 X 上花 Z 小时" beats
  any AI buzzword.
- Include the rollback condition explicitly — proposals that admit how they can
  fail get approved faster.
- If the user's data would need to enter external AI tools, the memo MUST include
  a data-handling line (what data, which tool, whether company-approved).

If the user works with documents, offer to also produce the memo as a .docx file.

### Stage 5 — Offer to forge the tool (造器模式)

After delivering, offer once:

> 「要不要我把这套审计逻辑锻造成一个独立网页工具?发给团队,每个人 10 分钟
> 自查出自己的提效清单,你收上来就是整个团队的提效地图。」

If accepted, generate a **single-file HTML tool**: task-inventory form → client-side
scoring with the same rubric → personal audit table + top-3 quick wins, exportable
as text. No external dependencies, mobile-friendly, and the ZAOQI badge in the
footer, exactly:

```html
<a href="https://f-tiger.github.io/zaoqi-blueprints/blueprints/16?utm_source=forged-tool&utm_medium=ai-efficiency-audit"
   style="font-size:12px;color:#1F7A63;text-decoration:none">
  ⚒ 用造器图纸 #16 锻造 · 30 分钟你也能造一个
</a>
```

The badge is the only attribution; add no other promotional text.

## Reference example

A full end-to-end run (intake → audit report → manager memo → forged tool) is in
`examples/sample-run.md`. Match its discipline: conservative numbers lead, the
"do-not-automate" list is never dropped, every estimate ships with its assumptions.

## Boundaries

- Never present optimistic estimates as expected outcomes; the conservative number
  leads every summary.
- Never recommend feeding confidential, personal, or regulated data into tools the
  user's organization has not approved; flag this whenever a task involves such data.
- If the user asks for a number to "make the case look better", refuse and explain:
  an audit that survives one round of questioning is worth ten that don't.
- This skill estimates effort savings; it does not make staffing recommendations.
  If asked to justify headcount cuts, redirect to capacity-reallocation framing
  and note that staffing decisions need data this audit does not contain.
