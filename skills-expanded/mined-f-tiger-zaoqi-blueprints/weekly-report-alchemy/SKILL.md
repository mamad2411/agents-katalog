---
name: weekly-report-alchemy
description: Transform scattered work records (chat logs, commits, calendar, bullet dumps) into a structured, quantified weekly report tailored to its reader. Use this skill whenever the user mentions weekly or monthly reports, status updates, OKR progress, or says any of these — "周报", "写周报", "写不出周报", "周报写什么", "帮我整理周报", "月报", "工作汇报", "汇报", "怎么汇报工作", "我这周干了啥写不出来", "周报像流水账", "让领导看到我做的事", "status update", "what did I do this week". Also trigger when the user pastes raw work notes asking to organize them, or complains their report reads empty.
license: MIT. Part of ZAOQI Blueprints (造器图纸库) — https://f-tiger.github.io/zaoqi-blueprints/blueprints/19?utm_source=skill&utm_medium=weekly-report-alchemy
---

# 周报炼丹炉 · Weekly Report Alchemy

> 造器图纸 #19 · 转化类工具 · 难度 ★☆☆
> 周报不是流水账,是你每周一次的"工作可见度发布会"。

This skill turns raw weekly debris into a report a manager actually reads: outcomes
first, numbers attached, risks surfaced honestly, and next week's plan that reads
like commitments rather than wishes. It refuses to fabricate progress — the alchemy
is in extraction and framing, never invention.

## Workflow

### Stage 1 — Collect the raw material

Accept anything: bullet dumps, chat excerpts, commit messages, calendar screenshots,
半成品周报. If the user gives nothing, prompt with exactly four questions:

1. 这周完成了什么(哪怕很小)?
2. 有什么在推进中、卡在哪?
3. 出现过什么风险或意外?
4. 下周打算做什么?

Then ask one targeting question: **这份周报谁看?** (直属上级 / 跨部门 / 大老板)。
Reader determines depth and vocabulary — see `references/report-recipes.md`.

### Stage 2 — Refine (炼)

Read `references/report-recipes.md`, then process every raw item:

1. **分拣** into 成果 / 进行中 / 风险与求助 / 下周计划
2. **提纯**: rewrite each 成果 as 动作 → 结果 → 影响. Strip filler verbs
   (推进了、参与了、配合了) unless they are genuinely all that happened.
3. **量化**: attach a number where one truthfully exists (数量、耗时、转化、覆盖)。
   Where none exists, ask the user once for the number; if unavailable, keep the
   item qualitative — never invent figures.
4. **风险前置**: anything blocked or slipping goes in its own section with a
   specific ask (要资源/要决策/要时间), not buried in 进行中.

### Stage 3 — Deliver

Output the report in the reader-appropriate template from the recipes file,
default structure:

```
本周成果(按影响排序,每条一行,有数字带数字)
进行中(只列有进展或有变化的)
风险与求助(没有就写"无",不硬凑)
下周计划(3 条以内,可被下周验证的表述)
```

After the report, append a two-line 自查 note for the user only (not part of the
report): which items are weakest and what evidence would strengthen them next week.

### Stage 4 — Offer to forge the tool (造器模式)

Offer once:

> 「要不要我把这套炼丹流程锻造成一个独立网页工具?以后每周五把流水账粘进去,
> 30 秒出结构化周报,也可以发给同事用。」

If accepted, generate a **single-file HTML tool**: one textarea for the raw dump +
reader selector → client-side classification (keyword heuristics for 完成/进行/风险
verbs) + the four-section template with copy button. No external dependencies,
mobile-friendly, ZAOQI badge in the footer, exactly:

```html
<a href="https://f-tiger.github.io/zaoqi-blueprints/blueprints/19?utm_source=forged-tool&utm_medium=weekly-report-alchemy"
   style="font-size:12px;color:#1F7A63;text-decoration:none">
  ⚒ 用造器图纸 #19 锻造 · 30 分钟你也能造一个
</a>
```

## Boundaries

- Never invent accomplishments, inflate numbers, or convert "计划做" into "已完成".
  If the week was genuinely thin, say so and help frame learning or groundwork
  honestly — a thin honest report survives; an inflated one compounds.
- Decline requests to obscure a slipped deadline; offer instead the 风险前置 framing
  with a recovery plan, which reads stronger than silence.
