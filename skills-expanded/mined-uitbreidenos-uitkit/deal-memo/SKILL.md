---
name: "deal-memo"
description: "Investment deal memo: market thesis, company analysis, financial projections, risk factors, and recommendation — for VC, growth equity, and early-stage investments"
---

# Deal Memo Skill

## When to activate
- Writing a deal memo after a first or second meeting with a founder
- Synthesizing diligence findings into a structured investment recommendation
- Presenting a new deal to your partners or IC for the first time
- Building the investment thesis before IC memo — deal memo is the earlier, more exploratory document
- Preparing a VC-style deal memo for seed, Series A, or growth rounds

## When NOT to use
- Formal IC memos requiring financial model sign-off — use `/ic-memo` for that
- PE buyout analysis — deal memo format differs (use PE-specific templates)
- Public market investment theses — different format and regulatory requirements
- Preliminary deal screens — use `/deal-screening` before investing time in a memo

## Important

Deal memos contain investment recommendations based on limited diligence. Mark all unverified claims as `[UNVERIFIED]`. Financial projections are founder-provided unless stated otherwise — always disclose the source.

## Instructions

### Full deal memo prompt

```
Write a deal memo for an investment opportunity.

COMPANY:
- Name: [company name]
- Founded: [year]
- Stage: [pre-seed / seed / Series A / Series B / growth]
- Industry: [sector]
- HQ: [location]
- Team size: [X] employees

BUSINESS:
- What they do (1 sentence): [describe]
- Business model: [SaaS / marketplace / transactional / hardware / other]
- Revenue model: [subscription / usage / one-time / hybrid]
- Current traction: [ARR/GMV/revenue, growth rate, key customers]
- Product maturity: [MVP / early product / mature]

MARKET:
- TAM: $[X]B [source or [UNVERIFIED]]
- Market growth rate: [X]% [source]
- Why now: [what has changed that makes this moment the right time]
- Key tailwinds: [technology, regulatory, consumer behavior shifts]

INVESTMENT TERMS:
- Round size: $[X]M
- Our check: $[X]M
- Pre-money valuation: $[X]M
- Post-money ownership: [X]%
- Lead: [who is leading the round]
- Other investors: [co-investors, if known]

FINANCIALS (founder-provided):
- LTM revenue: $[X]M
- ARR (if SaaS): $[X]M
- YoY growth: [X]%
- Gross margin: [X]%
- Burn rate: $[X]M/month
- Runway: [X] months
- Path to profitability: [description or [UNVERIFIED]]

TEAM:
- CEO: [name, background in 1 sentence]
- CTO: [name, background]
- Other key executives: [list]
- Team strengths: [domain expertise, prior exits, technical depth]
- Team gaps: [what's missing — finance, enterprise sales, etc.]

COMPETITIVE LANDSCAPE:
- Main competitors: [list 3-5]
- Differentiation: [why this company wins]
- Defensibility: [switching costs / network effects / IP / data moat]

MY THESIS:
- Why invest: [your 2-3 sentence investment thesis]
- Why now: [timing rationale]
- Why us: [what we bring beyond capital]

Generate a structured deal memo with:
1. Company overview and what they do
2. Market opportunity and why now
3. Business model and unit economics
4. Team assessment
5. Competitive analysis and moat
6. Financial overview and key metrics
7. Investment terms and valuation
8. Risk factors (top 5)
9. Diligence checklist (what to verify before IC)
10. Preliminary recommendation
```

---

### Market thesis section

```
Write the Market Opportunity section of a deal memo.

Company: [name]
Category: [what space they're in]

Market sizing:
- TAM: $[X]B — [how calculated: top-down / bottom-up / [UNVERIFIED]]
- SAM (addressable given product scope): $[X]B
- SOM (realistic near-term capture): $[X]M

Why now (select applicable):
[ ] Technology shift: [AI / cloud / mobile / API ecosystem]
[ ] Regulatory change: [describe]
[ ] Consumer behavior shift: [describe]
[ ] Incumbent failure to adapt: [describe]
[ ] New distribution channel unlocked: [describe]

Key tailwinds: [list 3]
Key risks to market thesis: [list 2]

Write a 200-word market opportunity section that argues why this market is large, growing, and winnable — and why this is the right time to invest.
```

---

### Team assessment section

```
Write the Team section of a deal memo.

Founders:
[For each founder: Name, role, prior companies, relevant expertise, notable achievements]

Assess against these dimensions:
1. Domain expertise: do they know this space deeply?
2. Technical ability: can they build the product?
3. Commercial ability: can they sell and tell the story?
4. Prior founder experience: first time or repeat?
5. Coachability signals (from references or conversation): [any notes]
6. Team completeness: what key roles are missing?

Write a balanced team assessment — strengths and gaps. Do not over-inflate. VCs who present every team as "world-class" lose credibility.
```

---

### Unit economics and financials section

```
Write the Financial Overview and Unit Economics section.

Metrics provided by company ([UNVERIFIED] unless audited):
- ARR: $[X]M, growing [X]% YoY
- MRR: $[X]M
- Gross margin: [X]%
- CAC: $[X] ([payback period: X months])
- LTV: $[X] (LTV/CAC ratio: [X]x)
- Churn: [X]% monthly / [X]% annual gross churn
- Net revenue retention: [X]%
- Burn rate: $[X]M/month
- Current ARR per employee: $[X]K

Benchmarks for comparison (SaaS, seed to Series A):
- Good gross margin: >70%
- Good LTV/CAC: >3x
- Healthy net revenue retention: >100%
- Efficient burn: <18 months runway at current rate

Write the financial overview section. Flag any metrics that are below benchmark. Note which figures are unverified and what we need to confirm in diligence.
```

---

### Risk factors section

```
Write the Risk Factors section for this deal.

Company: [name], [stage], [industry]

Evaluate these risk categories:
1. Market risk: is the market real and large enough?
2. Product risk: can they build it / does it work at scale?
3. Team risk: founder-market fit, key person dependency
4. Competition risk: can incumbents replicate or acquire competitors?
5. Technology risk: AI disruption, API dependency, platform risk
6. Regulatory risk: any pending regulation that could change the landscape?
7. Fundraising risk: how much runway do they have and what triggers the next round?
8. Customer concentration: does one customer represent >20% of revenue?

For each risk: [Risk] | [Probability: High/Med/Low] | [Impact: High/Med/Low] | [Mitigant or open question]

Prioritise the top 5. Flag which risks need resolution before we can invest.
```

---

### Diligence checklist

```
Generate a pre-IC diligence checklist for a [stage] investment in [sector].

Based on what I know:
- Known gaps: [list anything you couldn't verify from founder conversations]
- High-risk areas: [which risks from the risk assessment need investigation]
- References needed: [customer, prior employer, investor references]

Generate a checklist covering:
[ ] Financial diligence: [what to request from the company]
[ ] Customer diligence: [which customers to call, what to ask]
[ ] Technical diligence: [code review, architecture, security]
[ ] Legal/corporate: [cap table, IP assignment, prior financing terms]
[ ] Reference calls: [founder references — prior employers, co-founders, investors]
[ ] Market diligence: [expert calls, industry reports to pull]
[ ] Competitive diligence: [conversations with people who've evaluated alternatives]
```

---

### Investment recommendation section

```
Write the Recommendation section of a deal memo.

Summary of findings:
- Investment thesis (your 2 sentences): [describe]
- Key strengths: [top 3]
- Key risks: [top 3]
- Valuation: $[X]M pre-money, [X]x ARR / revenue multiple vs. comps at [X]x
- Our proposed check: $[X]M for [X]% ownership

Recommendation options:
[ ] INVEST — proceed to IC with the following conditions: [list]
[ ] PASS — primary reason: [state clearly, not diplomatically]
[ ] INVEST WITH CONDITIONS — invest only if: [specific conditions met]
[ ] WAIT — re-evaluate at: [next milestone or date]

Write a crisp recommendation section (150 words max). State your view clearly. Avoid mealy-mouthed language. If you're passing, say why directly so the team learns from it.
```

---

### Deal memo output format

```markdown
# Deal Memo: [Company Name]
**Date:** [Date] | **Stage:** [Stage] | **Analyst:** [Name]
**Round:** $[X]M | **Our check:** $[X]M | **Post-money valuation:** $[X]M

---

## TL;DR
[3 bullet points: what they do, why the market, why we'd invest or pass]

---

## 1. Company Overview
[What they do, founded when, where, team size, stage]

## 2. Market Opportunity
[TAM/SAM/SOM, why now, tailwinds]

## 3. Business Model & Unit Economics
[Revenue model, key metrics, unit economics — with [UNVERIFIED] flags]

## 4. Team Assessment
[Strengths, gaps, founder-market fit]

## 5. Competitive Analysis
[Competitive map, differentiation, moat]

## 6. Financial Overview
[ARR, growth, burn, runway — all figures marked as founder-provided unless verified]

## 7. Investment Terms & Valuation
[Round terms, our check, ownership, valuation vs. comps]

## 8. Risk Factors
[Top 5 risks with probability, impact, and mitigant]

## 9. Diligence Required Before IC
[Checklist of what must be verified]

## 10. Recommendation
[Invest / Pass / Conditional — stated clearly with rationale]
```

## Example

**User:** I just met with the founders of a seed-stage B2B AI company that automates legal contract review. 2 co-founders — one former BigLaw attorney, one engineering lead from a major legal tech firm. $400K ARR, growing 30% MoM, 4 enterprise pilots. Raising $3M seed at $15M pre-money. 18 months runway.

**Expected output:** A full deal memo covering market (legal tech $X0B, AI disruption timing), team (excellent domain/technical fit, missing enterprise sales leader), unit economics (prompt for LTV/CAC verification), competitive landscape (Harvey, Ironclad, Kira as comps), risk factors (customer concentration in pilots, regulatory around AI in legal advice, enterprise sales GTM), and a recommendation section that either leans in or passes with clear rationale. All founder-provided financial figures marked [UNVERIFIED].

---
