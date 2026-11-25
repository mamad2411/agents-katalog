---
name: okr-framework
description: "When to activate: OKRs, objectives and key results, goal setting, quarterly goals, annual goals, OKR scoring, OKR check-in, alignment"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: product
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# OKR Framework

## OKR Fundamentals

**Objective**: Qualitative, inspirational, memorable direction. Answers "where are we going?"
**Key Result**: Quantitative, measurable outcome. Answers "how will we know we got there?"
**Initiative**: The work we do to achieve Key Results (not part of OKRs themselves)

```
Objective: Make our customers wildly successful
  KR1: Increase 90-day retention from 45% to 65%
  KR2: Achieve NPS of 50+ (from current 32)
  KR3: 80% of customers complete onboarding within 7 days (from 40%)
```

## Writing Strong Objectives

### Objective Checklist
- [ ] Qualitative — no numbers in the objective itself
- [ ] Ambitious but achievable (60-70% confidence)
- [ ] Directional — could fail if ignored
- [ ] Memorable — team can recite it
- [ ] Actionable — team can influence it
- [ ] Time-boxed — for this quarter/year

### Good vs Bad Objectives
```
BAD: Improve the product
GOOD: Build the most intuitive onboarding experience in our category

BAD: Grow revenue Q3
GOOD: Establish product-led growth as our primary acquisition engine

BAD: Fix technical debt
GOOD: Build a foundation our engineering team is proud to ship on
```

### Objective Formulas
- "Become the [superlative] [thing] for [who]"
- "Establish [capability] as [strategic differentiator]"
- "Delight [persona] by [meaningful outcome]"
- "[Verb] [meaningful change] in [area]"

## Writing Strong Key Results

### KR Rules
- Always a number (% change, absolute target, ratio)
- Measures outcome, not output ("increase retention" not "ship 5 features")
- Baseline included in writing ("from X to Y")
- 3-5 KRs per objective
- Independent — achieving one doesn't auto-achieve another

### KR Formulas
```
Increase [metric] from [baseline] to [target]
Decrease [metric] from [baseline] to [target]
Achieve [metric] by [date]
Maintain [metric] above [threshold]
Reach [milestone] (binary KR — use sparingly)
```

### Good vs Bad Key Results
```
BAD: Launch new dashboard (output)
GOOD: Increase feature adoption of analytics from 20% to 45% of MAU

BAD: Improve performance
GOOD: Reduce p95 API response time from 800ms to 200ms

BAD: Get more customers
GOOD: Increase trial-to-paid conversion from 12% to 20%

BAD: Be more international
GOOD: Generate $500K ARR from EU customers (from $150K baseline)
```

## OKR Hierarchy & Alignment

```
Company OKRs (Annual + Quarterly)
│
├── Product OKRs (Quarterly) — aligned to Company OKRs
│   ├── PM Team OKRs — aligned to Product OKRs
│   └── Engineering Team OKRs — aligned to Product OKRs
│
├── Growth OKRs (Quarterly) — aligned to Company OKRs
└── Customer Success OKRs (Quarterly) — aligned to Company OKRs
```

### Alignment Check
For each team OKR, verify:
- Which company OKR does this ladder up to?
- If this KR is achieved, does it meaningfully move the parent KR?
- Are there KRs with no company alignment? (discuss: sandbox vs distraction)

## OKR Cadence

### Annual OKRs
- Set in November/December for following year
- 3-4 company objectives maximum
- Inspirational, 12-month horizon
- Reviewed quarterly, adjusted if major strategic shift

### Quarterly OKRs
```
Week 1-2 of previous quarter: Inputs
  - Previous quarter retrospective
  - Company/leadership priorities input
  - Data review (what moved? what didn't?)
  - Team capacity planning

Week 3 of previous quarter: Drafts
  - Teams draft OKRs bottom-up
  - PM reviews for alignment and ambition
  - Cross-team dependencies flagged

Week 4 of previous quarter: Finalize
  - Leadership review
  - Conflicts resolved
  - Final OKRs published by Day 1 of new quarter

Ongoing: Weekly/Bi-weekly check-ins
  - Confidence updates (not score updates — score at end)
  - Blockers surfaced
  - Initiatives adjusted based on what's working
```

## OKR Scoring

### Standard Scoring (0.0 – 1.0)
```
1.0 = 100% of target achieved
0.7 = 70% of target achieved (Google's "sweet spot" — stretch achieved)
0.4 = 40% of target achieved (below expectations)
0.0 = 0% (no progress)
```

### Scoring Philosophy
- Target score: 0.6-0.7 (not 1.0 — 1.0 means goal wasn't ambitious enough)
- 0.0-0.3: What blocked us? What did we learn?
- 0.4-0.6: Solid progress, missed stretch
- 0.7-1.0: Goal achieved; was it ambitious enough?
- > 1.0: Set a higher goal next quarter

### End-of-Quarter OKR Review Template
```markdown
## [Objective] — Score: [X.X]

### Key Results
| KR | Baseline | Target | Actual | Score |
|----|----------|--------|--------|-------|
| KR1 | 45% | 65% | 58% | 0.65 |
| KR2 | 32 | 50 | 41 | 0.45 |
| KR3 | 40% | 80% | 72% | 0.80 |

**Objective Score**: 0.63 (average of KRs)

### What Went Well
- [Specific win]
- [Specific win]

### What Didn't Work
- [Specific failure + root cause]

### What We Learned
- [Insight to inform next quarter]

### Carry Forward?
- [ ] Yes — same OKR with adjusted baseline
- [ ] No — achieved / deprioritized
- [ ] Modified — [describe change]
```

## OKR Check-In Template (Weekly/Bi-weekly)

```markdown
## Check-in: [Team] — Week [N]

| KR | Last Week | This Week | Confidence | Blockers |
|----|-----------|-----------|------------|---------|
| KR1 | 48% | 52% | 🟡 Medium | Need data infra fix |
| KR2 | 35 | 38 | 🟢 High | — |
| KR3 | 55% | 62% | 🟡 Medium | Eng bandwidth |

**Confidence Legend**: 🟢 On track | 🟡 At risk | 🔴 Off track

### This Week's Focus
- [Top 1-2 initiatives driving KRs]

### Help Needed
- [Cross-team dependency or blocker]
```

## Common OKR Mistakes

| Mistake | Fix |
|---------|-----|
| Too many OKRs (>5 objectives) | Limit to 3-4 objectives per level |
| Output KRs ("launch X feature") | Rewrite as outcomes ("increase metric Y") |
| 100% confidence in KRs | Make them more ambitious (target 60-70%) |
| OKRs disconnected from daily work | Map initiatives to KRs explicitly |
| Set-and-forget (no check-ins) | Weekly or bi-weekly confidence updates |
| Individual OKRs only | Balance team OKRs with individual |
| Copying last quarter's OKRs | Reflect on what changed and what's next |
