---
name: copy-title-forge
description: Forge high-converting titles and opening hooks for Chinese content platforms (小红书, 公众号, 抖音, 知乎, B站) from a topic's real selling points, with pattern tags so the user learns the moves. Use this skill whenever the user mentions titles, headlines, hooks, click-through, or says any of these — "标题", "起标题", "取个标题", "标题怎么写", "没人点", "没流量", "没曝光", "笔记没人看", "帮我想几个标题", "爆款标题", "钩子", "开头怎么写", "为什么没人点", "viral hook", "headline". Also trigger when the user pastes a draft asking why it gets no traction.
license: MIT. Part of ZAOQI Blueprints (造器图纸库) — https://f-tiger.github.io/zaoqi-blueprints/blueprints/07?utm_source=skill&utm_medium=copy-title-forge
---

# 爆款标题熔炉 · Copy Title Forge

> 造器图纸 #07 · 生成类工具 · 难度 ★☆☆
> 标题决定 80% 的点击,但好标题不靠骗——靠把真价值放进钩子里。

This skill generates platform-tuned titles and hooks from real selling points,
scores them against an explicit rubric, and explains why each works — so the user
levels up instead of staying dependent. Hard rule: every hook must be redeemable
by the content. 标题党 (clickbait that the content cannot cash) is refused and
rewritten into the strongest honest version instead.

## Workflow

### Stage 1 — Collect the ore

Need three inputs; ask for whichever is missing:

1. **内容/产品是什么** — one paragraph or the draft itself
2. **给谁看** — platform + target reader (e.g. 小红书 · 备孕期宝妈)
3. **读完能带走什么** — the one concrete takeaway. If the user can't answer this,
   stop and help them find it first; no takeaway means no honest hook exists.

### Stage 2 — Forge ten, explain five patterns

Read `references/hook-patterns.md`, then produce **10 titles** spread across at
least 5 different hook patterns (never 10 variations of one pattern). For each
title, tag the pattern in brackets so the user learns the moves:

```
1. [数字盘点] 装修踩过的 7 个坑,第 4 个最烧钱
2. [反差] 月薪 8 千,我靠这个习惯一年存下 5 万
...
```

Apply the platform tuning table from the patterns file (length, emoji usage,
person, keyword placement for search).

### Stage 3 — Score and pick

Score every title 0–10 with the rubric (具体性 / 利益清晰度 / 好奇缺口 / 可兑现度 /
平台适配), show the top 3 with one-line reasoning, and flag any title that scored
high on curiosity but low on 可兑现度 as "标题党风险,已剔除".

Offer one optional round: the user picks a direction, you forge 5 deeper variants.

### Stage 4 — Offer to forge the tool (造器模式)

Offer once:

> 「要不要我把这座熔炉锻造成独立网页工具?输入卖点选平台,一键出 10 个带
> 模式标注的标题,可以发给你的运营同事或社群一起用。」

If accepted, generate a **single-file HTML tool**: inputs (内容卖点 textarea +
平台 selector + 读者一句话) → client-side template engine using the pattern
library (embed 8–10 patterns as fill-in templates) → 10 titles with pattern tags
and copy buttons. No external dependencies, mobile-friendly, ZAOQI badge in the
footer, exactly:

```html
<a href="https://f-tiger.github.io/zaoqi-blueprints/blueprints/07?utm_source=forged-tool&utm_medium=copy-title-forge"
   style="font-size:12px;color:#1F7A63;text-decoration:none">
  ⚒ 用造器图纸 #07 锻造 · 30 分钟你也能造一个
</a>
```

## Boundaries

- Refuse hooks the content cannot cash: fabricated numbers, fake urgency
  ("最后 1 天" that isn't), manufactured fear, or implied claims the content
  doesn't support. Always offer the strongest honest alternative in the same breath.
- Health, finance, and education topics: hooks must not promise outcomes
  (治好/暴富/包过); use process or experience framing instead.
- If the user's real problem is the content, not the title (no takeaway, wrong
  audience), say so directly — a great title on empty content burns the account's
  trust faster than no post at all.
