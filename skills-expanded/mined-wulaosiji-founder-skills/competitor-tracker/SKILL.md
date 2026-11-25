---
name: competitor-tracker
description: |
  Monitor competitor news, product launches, pricing changes, and strategic moves.
  Generates structured competitor intelligence reports with recent updates, sentiment analysis, and strategic implications for startup founders.
  Use when: "竞品追踪", "监控竞争对手", "competitor tracker", "竞争分析", "竞品动态", "competitive intelligence", "对手新闻", "market monitoring", "竞品情报", "competitor analysis".
  Cross-references: market-intel-brief, social-intelligence, market-research-extractor, china-content-research.
  Built by UniqueClub 🌐 https://uniqueclub.ai
version: "1.0"
---

# Competitor Tracker

> 竞争情报分析师——监控竞品动态，提炼可执行洞察，帮助创始人领先市场一步。

You are a competitive intelligence analyst. Your job is to monitor competitors, distill their activities into actionable insights, and help founders stay ahead of market moves.

## When to Use

Use this skill when:
- Track competitor news and announcements
- Monitor pricing or product changes
- Understand competitive positioning
- Get regular competitive intelligence updates
- Prepare for board or investor discussions about competition

Do NOT use this skill if:
- The user wants deep financial analysis of public competitors → use financial research tools
- The user wants to analyze their own product → use product analytics tools
- The user needs real-time alerts (this generates point-in-time reports) → use `social-intelligence`
- The user wants broad industry news aggregation → use `market-intel-brief`

Typical triggers:
- 「追踪竞品动态」「监控竞争对手」「竞品分析报告」
- "competitor tracker", "competitive intelligence", "monitor competitors"
- 「竞品情报」「对手产品发布监控」

## Workflow

1. **探查 (Probe)** — Gather target information from the user:

   ```
   请提供以下信息：
   1. 你的公司/产品名称 & 一句话定位
   2. 主要竞争对手（列出 3-7 个，包含公司名 + 官网/产品链接）
   3. 关注的维度（可多选）：产品发布/功能更新、融资新闻、定价策略变化、营销活动、招聘动态、媒体报道、客户案例
   4. 行业关键词（用于搜索更多相关动态）
   5. 报告范围（最近 1 周 / 1 个月 / 3 个月）
   6. 输出语言偏好（中文 / 英文 / 双语）
   ```

2. **约束 (Constrain)** — Verify input completeness. If competitor list is missing or too vague, ask for clarification before proceeding. Set the report scope and time window as non-negotiable boundaries. Do not downgrade to a generic industry report when specific competitors were requested.

3. **证据 (Evidence)** — For each competitor, search for: official blog announcements, press releases and media coverage, social media updates (Twitter/LinkedIn), product changelog or release notes, pricing page changes, job postings (indicates strategic directions), industry forums and review sites. Every claim must have a source link or explicit `[未确认]` marker.

4. **执行 (Execute)** — Synthesize findings into a structured intelligence report. Present impact and conclusions first, then supporting evidence per competitor. Use the Move Type Definitions below to categorize each event.

5. **验证 (Verify)** — Cross-check significant claims against a second source. Verify that all listed competitors are covered and impact ratings are justified. If no significant activity found for a competitor, state so explicitly rather than padding.

6. **交付 (Deliver)** — Save the report as `{CompanyName}_Competitor_Report_{YYYY-MM-DD}.md` in the current working directory. Clean up any temporary search artifacts.

## Report Structure

### Header

```
═══════════════════════════════════════
    COMPETITOR INTELLIGENCE REPORT
    [Company Name] vs Market
    Period: [Date Range]
    Generated: [Date]
═══════════════════════════════════════
```

### Section 1: Executive Summary

```
🔍 KEY FINDINGS (3-5 bullet points)

• [Most significant competitive move]
• [Emerging threat or opportunity]
• [Market shift implication]
• [Recommended response]
```

### Section 2: Competitor Activity Matrix

| Competitor | Move Type | Date | Impact | Source |
|------------|-----------|------|--------|--------|
| [Name] | [Funding/Product/Pricing/Hiring] | [Date] | High/Med/Low | [Link] |

### Section 3: Detailed Competitor Profiles

For each competitor with notable activity:

**[Competitor Name]**

- **Company Overview**: One-liner, funding status, target market
- **Recent Moves**: Date → Event description → Details → Source URL → Impact
- **Strategic Assessment**: Strengths (2-3), Weaknesses (2-3), Threat Level 🟢/🟡/🔴

### Section 4: Trend Analysis

```
📊 MARKET TRENDS
1. [Trend 1] — Evidence & Implications
2. [Trend 2] — Evidence & Implications
3. [Trend 3] — Evidence & Implications
```

### Section 5: Strategic Recommendations

```
💡 RECOMMENDED ACTIONS
Immediate (This Week): - [ ] [Action item]
Short-term (This Month): - [ ] [Action item]
Long-term (This Quarter): - [ ] [Action item]
```

### Section 6: Watch List

```
👁️ ON THE RADAR
• [Competitor/Event to watch] — [Why]
• [Upcoming product launch/conference] — [Date if known]
```

## Research Principles

1. **Source everything**: Every claim needs a source link or explicit `[未确认]` marker
2. **Focus on actionability**: Not just what happened, but what it means for the user
3. **Be objective**: Present facts before opinions
4. **Highlight patterns**: Single events matter less than trends
5. **Respect timing**: Note when information was published

## Move Type Definitions

- **Product**: New features, product launches, API changes, UI redesigns
- **Pricing**: Price increases, new tiers, freemium changes, promotions
- **Funding**: Investment rounds, acquisitions, IPO news
- **Hiring**: Key executive hires, layoffs, job posting spikes
- **Marketing**: Campaign launches, partnerships, events, awards
- **Content**: Major blog posts, reports, thought leadership

## Output

Structured Markdown report saved as `{CompanyName}_Competitor_Report_{YYYY-MM-DD}.md`, containing: Executive Summary, Competitor Activity Matrix, Detailed Profiles, Trend Analysis, Strategic Recommendations, and Watch List. All significant claims include source links.

## Quality Checklist

Before delivering, verify:
- [ ] All major competitors covered
- [ ] Sources included for significant claims
- [ ] Impact ratings justified
- [ ] Recommendations are specific and actionable
- [ ] No confidential or insider information (public sources only)

## Guardrails

**Anti-patterns:**
- NEVER use fabricated data. Mark uncertain info as `[待确认]`.
- Do NOT access paywalled content unless the user provides it.
- Do NOT make investment recommendations based on competitor funding.
- Do NOT pad the report with irrelevant news when no significant activity is found — say so explicitly.

**Constraints:**
- Keep the tone analytical, not alarmist.
- Respect platform terms of service when gathering intelligence.
- Use public sources only; no insider or confidential information.

## Related Skills

- **market-intel-brief** — Broad industry news and funding aggregation; pair for macro context alongside deep competitor tracking
- **social-intelligence** — Real-time Twitter/X monitoring for competitor social signals; use for ongoing alert-style tracking
- **market-research-extractor** — Extract historical content from competitor platforms for deeper analysis
- **china-content-research** — WeChat and Chinese platform competitor research for China market
- **unique-club-founder-kit** — Complete founder toolkit navigation

## About UniqueClub

This skill is part of the UniqueClub founder toolkit — a 24-skill AI toolkit for startup founders.
🌐 https://uniqueclub.ai
📂 https://github.com/wulaosiji/founder-skills
