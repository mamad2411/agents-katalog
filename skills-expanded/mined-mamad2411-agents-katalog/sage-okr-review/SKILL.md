---
name: sage-okr-review
description: "Review and track OKRs progress. Use when user says 'OKR review', 'OKR progress', 'update OKRs', 'define quarterly OKRs', or any reference to objectives, key results, or quarterly goals."
---

# OKR Review — Goal Tracking

Skill to review, update, or define quarterly company OKRs.

**Always respond in English.**

## Workflow

### If OKRs already exist (update)

1. Read the most recent OKRs file from `workspace/strategy/okrs/`
2. For each Key Result, fetch updated data:
   - Financial metrics → `/int-stripe` (MRR, subscriptions)
   - Product metrics → `/int-linear-review` (issues, deliveries)
   - Community metrics → read reports in `workspace/community/reports/`
   - GitHub metrics → read reports in `workspace/projects/github-reviews/`
3. Calculate progress for each KR (0-100%)
4. Classify: 🟢 on track (>70%) | 🟡 at risk (40-70%) | 🔴 off track (<40%)
5. Update the OKRs file with new data
6. Present summary

### If OKRs do not exist (definition)

1. Interview the user about the quarter's priorities
2. Propose 3-4 Objectives with 3-4 Key Results each
3. Each KR must be: measurable, with baseline and target, with deadline
4. Save to `workspace/strategy/okrs/[C] YYYY-QX-okrs.md`

## OKR file format

```markdown
# OKRs — Q{X} {YYYY}

> Status: {in definition | active | in review | closed}
> Period: {start date} → {end date}
> Last updated: {YYYY-MM-DD}

## O1: {Objetivo 1}

| KR | Baseline | Target | Atual | Progresso | Status |
|----|----------|--------|-------|-----------|--------|
| {KR1} | {valor} | {valor} | {valor} | {X%} | 🟢/🟡/🔴 |
| {KR2} | {valor} | {valor} | {valor} | {X%} | 🟢/🟡/🔴 |

**Notes:** {relevant context}

## O2: {Objetivo 2}
...
```

## Rules
- KRs should be numbers, not activities ("increase MRR to R$15k" not "work on MRR")
- Baseline required — without a baseline, progress cannot be measured
- Do not fabricate data — if the number is unavailable, mark as "pending"
- Maximum 4 Objectives per quarter — focus > ambition
