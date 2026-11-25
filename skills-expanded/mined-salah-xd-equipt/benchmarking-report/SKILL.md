---
name: benchmarking-report
description: "Creates industry benchmarking reports comparing business metrics against standards and best-in-class performers. Use when evaluating where your business stands versus peers."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Benchmarking Report

## When to Use This Skill

Use this skill when you need to:
- Compare your business metrics against industry averages
- Identify performance gaps relative to best-in-class competitors
- Set realistic targets based on external benchmarks
- Create a benchmarking report for investors, board, or internal planning

**DO NOT** use this skill for competitive intelligence gathering, financial auditing, or market research. This is for comparing your metrics against known benchmarks.

---

## Core Principle

BENCHMARKS PROVIDE CONTEXT, NOT ANSWERS — A METRIC BELOW BENCHMARK IS A SIGNAL TO INVESTIGATE, NOT AUTOMATICALLY A PROBLEM TO FIX.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Industry** | "What industry are you in?" | Must be provided |
| **Business model** | "SaaS, e-commerce, services, marketplace, or other?" | Must be provided |
| **Metrics to benchmark** | "Which metrics do you want to compare? (growth rate, margins, churn, CAC, conversion)" | Core financial + growth metrics |
| **Your current numbers** | "Share your current performance for each metric." | Must be provided |
| **Company stage** | "What stage? (pre-revenue, early, growth, mature)" | Early stage |
| **Peer group** | "Any specific companies or cohort you want to benchmark against?" | Industry averages |

**GATE: Confirm brief and metrics list before proceeding.**

---

## Phase 2: Research

### Benchmark Sources

Pull benchmarks from these source types (note the source for every number):
- Industry reports (SaaS Benchmarks, Shopify reports, etc.)
- Public company filings (for mature business comparisons)
- Aggregated survey data (OpenView, ChartMogul, ProfitWell)
- Accelerator/VC published benchmarks (YC, a16z, First Round)

### Benchmark Categories

1. **Growth metrics** — revenue growth rate, customer growth, MRR expansion
2. **Unit economics** — CAC, LTV, CAC:LTV ratio, payback period
3. **Retention** — churn rate, net revenue retention, logo retention
4. **Profitability** — gross margin, operating margin, burn rate
5. **Efficiency** — revenue per employee, magic number, Rule of 40

**GATE: Present the benchmark data with sources and confirm before comparing to user's metrics.**

---

## Phase 3: Build

### Deliverables

**1. Benchmarking Scorecard**
| Metric | Your Number | Industry Median | Top Quartile | Status |
|--------|------------|----------------|--------------|--------|
| Annual growth | 40% | 25% | 80% | Above median |
| Gross margin | 65% | 70% | 85% | Below median |
| Monthly churn | 5% | 3% | 1.5% | Below median |

**2. Gap Analysis**
For each metric below median:
- How far below and what that means in dollar terms
- Likely causes based on company context
- Specific improvement strategies

**3. Strength Recognition**
For each metric above median:
- What is driving the strong performance
- How to protect and extend the advantage

**4. Target-Setting Recommendations**
- 12-month targets per metric based on realistic improvement trajectories
- Priority ranking: which gaps to close first for maximum business impact

---

## Phase 4: Polish

### Report Formatting

Present in a format appropriate for the audience:
- **Investor deck:** 2-3 slides with scorecard and narrative
- **Internal planning:** Full report with gap analysis and action plan
- **Board meeting:** Executive summary with top 3 strengths and top 3 gaps

### Update Schedule

Benchmarks shift over time. Recommend re-running the analysis:
- Annually for stable industries
- Semi-annually for fast-moving sectors
- After major business model changes

---

## Example 1: SaaS Startup (Series A stage)

**Benchmarks used:** OpenView SaaS Benchmarks, ChartMogul medians
**Key finding:** Growth rate above median but churn is 2x the benchmark — growth is masking a retention problem.

## Example 2: E-commerce Brand (2 years old, $1M revenue)

**Benchmarks used:** Shopify commerce data, industry gross margin ranges
**Key finding:** AOV above benchmark, conversion rate below — pricing is strong but site experience needs work.

---

## Anti-Patterns

- **Comparing apples to oranges** — a bootstrapped 5-person company should not benchmark against a VC-funded 200-person company. Match the peer group.
- **Using outdated benchmarks** — 2019 SaaS benchmarks do not reflect post-2020 market reality. Use the most recent data available.
- **Benchmark worship** — being below a benchmark is a signal to investigate, not a guarantee something is wrong. Context matters.
- **Ignoring your strengths** — fixating on gaps while ignoring above-benchmark performance misses the strategic picture.
- **Too many metrics** — benchmarking 30 metrics dilutes focus. Pick the 5-8 that matter most for your stage and model.

---

## Recovery

- **No benchmark data for the niche:** Use adjacent industry benchmarks and note the approximation. Something is better than nothing.
- **All metrics below benchmark:** Prioritize the 1-2 metrics with the highest revenue impact. Fix those first.
- **User disputes the benchmarks:** Discuss the source and methodology. Offer multiple sources for triangulation.
- **Benchmarks make the user feel behind:** Reframe — benchmarks show the path, not the finish line. Most companies are below median on something.
