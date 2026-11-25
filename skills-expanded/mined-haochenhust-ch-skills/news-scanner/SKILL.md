---
name: news-scanner
description: "This skill should be used during daily research scanning, or when the user asks '最近有什么新消息', '扫描一下XX的最新动态', '帮我看看雪球上在聊什么'. Scans Xueqiu, Eastmoney, 10jqka, and web search for investment-related news filtered by the industry-chain keywords you track. Outputs HIGH/MEDIUM findings only — signal, not noise."
version: 1.0.0
---

# News Scanner

Systematic news and sentiment scanning for the industry chains you track.

## When to Use

- Daily research passes (a few times per day)
- When researching a new industry chain
- When a catalyst event just happened and you need the market reaction

## Workflow

### Step 1: Load Keywords

Build a keyword list from the industry chains and key stocks you currently track (e.g. from your research-state / watchlist notes).

### Step 2: Multi-Source Scan

For each tracked industry chain, search across platforms:

```
1. WebSearch: "{keyword} 研报 一致预期"          (analyst reports first)
2. WebSearch: "{keyword} site:xueqiu.com 2026"
3. WebSearch: "{keyword} site:eastmoney.com 2026"
4. WebSearch: "{keyword} 最新消息 {today's date}"
5. WebSearch: "{stock name} 研报 最新"
```

### Step 3: Filter & Prioritize

Rate each finding:
- **HIGH**: Directly affects your thesis or triggers a buy/sell signal
- **MEDIUM**: Relevant background, updates your understanding
- **LOW**: Noise, already known, or not actionable

Only report HIGH and MEDIUM findings.

### Step 4: Output

For routine scans with nothing major: update your research log, don't message the user.

For significant findings:
```markdown
## 信息扫描 — {date} {time}

### 重要发现
- [{HIGH/MEDIUM}] {source}: {summary} — 影响：{how it affects the thesis}

### 研究状态更新
- {track name}: 置信度 {unchanged/+5%/-5%} — 原因：{finding}
```

## Platforms & Keywords

### Default Search Targets
- 雪球 (xueqiu.com) — retail sentiment, hot discussions
- 东方财富 (eastmoney.com) — news, research reports
- 同花顺 (10jqka.com.cn) — sector analysis
- 券商研报 / 一致预期 — via general WebSearch
- General web — for broader news coverage

### Keyword Construction
From your tracked chains/stocks, build searches like:
- Industry: "{细分材料}", "{细分器件}"
- Companies: "{公司名A}", "{公司名B}"
- Events: "{行业大会} 2026", "{龙头公司}"
- Themes: "{产业链主题}"

## Rules

1. **Don't repeat known information** — check your notes before reporting
2. **Cite sources** — every finding must have a URL or source name
3. **Signal, not noise** — the user wants actionable intel, not a news digest
4. **Update your research log** — every scan should at minimum leave a trace
