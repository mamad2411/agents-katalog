---
name: geo-report
description: "Client-facing GEO report generator that combines audit results into one Markdown deliverable with a GEO readiness score, findings, and an action plan in quick wins, medium-term, and strategic buckets. Use after an audit when the user wants a report to hand to a client or stakeholder."
version: 1.0.0
author: geo-seo-claude
tags: [geo, report, client-deliverable, executive-summary, action-plan]
---

# GEO client report generator

Aggregates outputs from the `geo-*` audit family into one report for business owners and marketing leaders (not developers). Technical findings translate into business impact and prioritized actions.

## How to use

1. Run (or collect existing output of) these audits:
   - `geo-platform-optimizer` → GEO-PLATFORM-OPTIMIZATION.md
   - `geo-schema` → GEO-SCHEMA-REPORT.md
   - `geo-technical` → GEO-TECHNICAL-AUDIT.md
   - `geo-content` → GEO-CONTENT-ANALYSIS.md
   - (Optional) `geo-llms-txt` → llms.txt assessment
   - (Optional) `geo-brand-mentions` → brand authority data
2. Collect all scores and findings
3. Calculate the composite GEO Readiness Score (formula below)
4. Generate the report using the 12-section template in `template.md`
5. Output: **GEO-CLIENT-REPORT.md**

---

## GEO readiness score

### Component weights

| Component | Weight | Source skill |
|---|---|---|
| AI Platform Readiness | 25% | geo-platform-optimizer |
| Content Quality & E-E-A-T | 25% | geo-content |
| Technical Foundation | 20% | geo-technical |
| Schema & Structured Data | 15% | geo-schema |
| Brand Authority & Entity Presence | 15% | geo-platform-optimizer (entity signals) |

### Formula

```
GEO Score = (Platform Score * 0.25) + (Content Score * 0.25) + (Technical Score * 0.20) + (Schema Score * 0.15) + (Brand Score * 0.15)
```

Round to the nearest integer. Cap at 100.

### Score interpretation

| Range | Label | Client-facing description |
|---|---|---|
| 85-100 | Excellent | Your site is well-positioned for AI search. Focus on maintaining and expanding your advantage. |
| 70-84 | Good | Solid foundation with clear opportunities to improve AI visibility. Targeted optimizations will yield significant results. |
| 55-69 | Moderate | Your site has gaps in AI readiness that competitors may be exploiting. A structured optimization plan will close these gaps. |
| 40-54 | Below Average | Significant barriers to AI search visibility exist. Without action, your brand risks being invisible in AI-generated answers. |
| 0-39 | Needs Attention | Critical AI readiness issues require immediate action. Your competitors are likely capturing the AI search traffic your brand should own. |

---

## Report structure

The 12-section template lives in `template.md`. Fill each section with actual audit data.

1. Executive summary (one paragraph)
2. GEO readiness score (overall + component table)
3. AI visibility dashboard (per-platform readiness)
4. AI crawler access status (robots.txt by bot)
5. Brand authority analysis (entity presence across platforms)
6. Citability analysis (top 5 most + least citable pages)
7. Technical health summary
8. Schema and structured data
9. llms.txt status
10. Prioritized action plan (Quick Wins / Medium-Term / Strategic) — bucket criteria + examples in `examples.md`
11. Competitor comparison (if URLs provided)
12. Appendix (methodology, data sources, glossary)

---

## Tone and formatting

- Markdown throughout: tables for data, bullets for recommendations, bold sparingly for key terms
- One blank line between sections; `---` separators between major sections
- All URLs absolute
- Written for business owners — confident, direct, action-oriented
- Every finding connects to a specific action
- Translate technical issues into business outcomes
- Avoid: jargon without explanation, hedging, passive voice, excessive caveats
- Use: "Your site [does/does not]...", "We recommend...", "This impacts..."
- Dollar-value framing: conservative estimates, state assumptions, never guarantee results (examples in `examples.md`)

---

## Output

**GEO-CLIENT-REPORT.md** — filled template, 3,000-6,000 words, ready to send to a client without editing, self-contained (no references to other report files).
