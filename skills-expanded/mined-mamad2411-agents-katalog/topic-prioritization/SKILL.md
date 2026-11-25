---
name: topic-prioritization
description: Correlate pending topic briefs from News Researcher with actual traffic data from the analytics digest. Produce a ranked topic queue that EIC uses to assign next writing work.
---

# Topic Prioritization

The News Researcher generates topic briefs based on what's trending. Topic prioritization answers the harder question: what topics will actually convert for ArtStroy's audience given our existing traffic patterns?

## When to Run

- After `analytics-digest` completes and posts its weekly report (label: `ready-for-topic-prioritization`)
- When EIC requests a ranking of pending topic briefs
- When the backlog of pending topic briefs exceeds 5 (to prevent queue bloat)

## Inputs

**1. Pending topic briefs** — Issues with label `topic-brief` and status `pending-eic-review`:
- Extract: title, category, scoring dimensions (Relevance, Timeliness, Uniqueness) from the brief
- Note any brief older than 14 days — may have lost timeliness value

**2. Latest analytics digest** — most recent comment containing "Analytics Digest" on the root company issue:
- Top 5 articles by visitors
- Category breakdown (pentesting / programming / technology-qa)
- Referrer mix
- Signals section

**3. Content gaps** — scan `src/content/articles/` for:
- Most recent article per category (recency balance)
- Any pillar with no article in 30+ days (gap signal)

## Scoring: Traffic-Weighted Priority

For each pending topic brief, compute a **Priority Score (0–20)**:

| Factor | Weight | How to score |
|---|---|---|
| Original topic score (from brief) | 1× | Direct from brief (max 15) |
| Category traffic lift | +0 to +3 | +3 if category is #1 this week; +2 if #2; +1 if #3 |
| Referrer alignment | +0 to +2 | +2 if topic matches a high-referrer source (e.g., if HN is top referrer and topic came from HN digest) |
| Content gap bonus | +0 to +2 | +2 if this category has had no article in 30+ days; +1 if 14–30 days |
| Timeliness decay | −0 to −3 | −1 per week since brief was created (max −3) |

**Threshold to advance:** Priority Score ≥ 14/20 → recommend to EIC for immediate assignment.

## Output Format

Post as a comment on the current analytics or weekly-review issue:

```markdown
## Topic Priority Queue — {YYYY-MM-DD}

Based on traffic digest (week of {date}) and {N} pending topic briefs.

### Recommended for Immediate Assignment (Score ≥ 14)

| Rank | Brief | Category | Score | Key reason |
|---|---|---|---|---|
| 1 | [{brief title}](#{issue-link}) | pentesting | 17/20 | Category is top traffic driver this week; brief is 3 days old (max timeliness) |
| 2 | [{brief title}](#{issue-link}) | programming | 15/20 | 45-day gap in programming category |
...

### Queued (Score 10–13) — Hold for next cycle

| Rank | Brief | Category | Score | Notes |
|---|---|---|---|---|
...

### Deprioritized (Score < 10) — Reconsider or archive

| Brief | Score | Reason |
|---|---|---|
| {title} | 7/20 | Timeliness expired; topic well-covered by top-ranked existing article |
...

### Category Health

| Category | Last article | Days since | Status |
|---|---|---|---|
| Pentesting | {slug} | {N} days | 🟢 / 🟡 / 🔴 |
| Programming | {slug} | {N} days | |
| Technology/QA | {slug} | {N} days | |

🟢 <14 days · 🟡 14–30 days · 🔴 >30 days

---
*Scoring: Original brief score (max 15) + traffic lift (+3) + referrer alignment (+2) + content gap (+2) − timeliness decay (−3). Max 20.*
```

## Handoff

After posting, assign the top-ranked brief issue to EIC and add label `next-article`. EIC then creates the Writer's issue referencing the brief.

Brief issues with Score < 10 should be flagged for the News Researcher: "This brief has decayed below threshold — consider refreshing with updated sources or archive."

## Invariants

- Never advance a brief older than 30 days without EIC explicit confirmation (topic may be stale)
- Category gap is a real editorial signal — a 30-day silence in pentesting while running a security-focused blog is a problem, not just a data point
- One `next-article` label at a time in the queue per category (prevents Writer bottleneck)
