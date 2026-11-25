---
name: meeting-notes
description: "Take structured Markdown meeting notes during a live conversation. Cover real-time dictation from the user, data enrichment (web research, market data APIs), incremental patch-based updates, and final cleanup. Works for any topic — finance, tech, project discussion."
category: productivity
---

# Meeting Notes

> 本技能为会议笔记类技能的伞,已吸收 `live-meeting-notes`(2026-08 合并)。
> 完整原文见 `references/absorbed-*.md`。


## Overview

During a conversation, the user may dictate meeting notes — topics, data points, analysis, and strategic views — that need to be captured as a structured Markdown document. The workflow is: the user talks, the agent types and enriches.

## When to Use

- User says "接下来做会议纪要" or "我说什么你记什么"
- User dictates a series of topic points and says "记一下"
- A section of the conversation contains structured information worth persisting
- The conversation shifts between structured topics (e.g. options → bonds → IPO → market views)

## Directory Structure

```
meetings/
├── jul-06.md        ← date-named files (两位日期排序友好)
├── jul-07.md
└── ...
```

Always create files under `meetings/`. Name with the pattern `{三字母月份}-{两位日期}.md` (e.g. `jul-06.md`, `aug-01.md`).

## Workflow

### Step 1: Create the file shell

```markdown
# {Topic} — 会议纪要

日期：2026-07-06
主讲人：
参与人：
```

### Step 2: Record topics incrementally

As the user speaks, add sections with `patch`:

```markdown
## 核心观点

- {point 1}
- {point 2}

## {Topic Name}

### Sub-topic

- detail...
```

Use `patch` with unique surrounding context for each insertion. Keep file open — avoid `write_file` on the whole file mid-session (risk of overwriting concurrent additions).

### Step 3: Research enrichment

When the user references a market event, price level, or trend:
- Pull real-time/latest data from TradingView, Yahoo Finance API, or search
- Insert as a table or bullet list under the relevant section
- Do NOT fabricate data points — if search is blocked, say so and leave room for later fill

```markdown
| 周期 | 涨幅 |
|------|------|
| 年初至今 | −4.06% |
| 1年 | +24.86% |
```

### Step 4: Clean up at the end

After the user signals the session is over ("没了", "收尾"):
1. Remove any empty section headers (topics mentioned but not discussed)
2. Consolidate related short sections under a common parent
3. Ensure headers follow a consistent nesting depth
4. Optionally commit to git

### Step 5: Commit

```bash
git add meetings/{filename}.md
git commit -m "docs: add {date} meeting notes - {key topics}"
git push
```

## Data Enrichment Techniques

When the user references market data that needs real values:

**Yahoo Finance API** (for historical price data):
```bash
curl -sL -A "Mozilla/5.0" \
  "https://query1.finance.yahoo.com/v8/finance/chart/SI=F?range=6mo&interval=1d"
```

Parse the JSON `chart.result[0]` for timestamps + close/open to compute daily changes.

**TradingView** (for current prices):
Navigate to `https://www.tradingview.com/symbols/{TICKER}/` and read the price/change data from the page snapshot.

## Due Diligence Compilation

For compiling structured due diligence Q&A documents from live interview draft notes + source materials (尽调问卷/净值表/审计报告), see `references/due-diligence-compilation.md`.

This pattern extends the base meeting-notes workflow: instead of real-time dictation into `meetings/`, the user provides incremental draft updates and you sync a formal document in `docs/jul-NN-manager/`.

## Market Data / Daily Review Notes

When the user asks to record market data across multiple markets, the final document must have a logical analysis layer — not just raw data tables. The user will explicitly ask for this ("小结部分要做逻辑分析").

### Required structure for the 小结 section

1. **Global context** — macro drivers (VIX, geopolitical events, rate expectations). Reference specific news headlines.
2. **Per-market analysis** — explain what drove each region's move. Connect sub-sector divergences (e.g. "storage up while semiconductors down = rotation signal").
3. **Policy/event catalyst analysis** — when a policy event surfaces, add an impact assessment table:

   | 维度 | 影响 | 方向 |
   |------|------|------|
   | Market / sector | What changes | 利好/利空/中性 |

4. **Core conclusions** — 3-5 numbered conclusions that synthesise data + analysis + catalysts into actionable or testable claims.

### Data collection priority

1. `akshare` (`stock_zh_index_daily`, `stock_us_daily`, `stock_hk_index_daily_em`, `index_global_spot_em`) — reliable for Chinese/HK/US/KR indices and individual US stocks
2. `thsdk` — fast for A-share data but guest account limited for US/HK
3. Browser (AP News, Yahoo Finance) — for news context when search engines block bot traffic

For a worked example of this structure, see `references/market-review-structure.md`.

## Common Pitfalls

1. **Overwriting vs patching** — never `write_file` the whole file mid-session. Use `patch` with unique old_string anchors. The user keeps talking while you edit; a full write could lose concurrent dictation.
2. **Empty section headers** — when the user mentions a topic but doesn't elaborate, don't add the section header until they start dictating content. If you already added them, remove them in the final cleanup.
3. **Fabricated data** — when the user says "check this price" and search fails, say "search blocked" or "couldn't verify", leave the section with a placeholder. Never invent price levels.
4. **Too much nesting** — max 3 heading levels (`##` → `###` → `####`). Beyond that, use bullet lists.
5. **Not committing** — meeting notes should be persisted. After the session ends, commit.
6. **Mixed languages in tables** — pick one language per table. Chinese for Chinese topics, English for global market data.
7. **Personally identifiable info** — don't record third-party names the user mentions in passing (colleagues, speakers) without explicit instruction.

## Verification Checklist

- [ ] All topics the user dictated are captured
- [ ] Empty/untouched section headers removed
- [ ] Data from external sources is real (not fabricated)
- [ ] Consistent heading depth
- [ ] Committed and pushed
