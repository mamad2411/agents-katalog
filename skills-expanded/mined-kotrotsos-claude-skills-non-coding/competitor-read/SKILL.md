---
name: competitor-read
description: Use this skill to produce a strategic read of a competitor based on their public signals over the last 6 to 12 months. Triggers on phrases like "competitor read on [company]", "what is [company] doing", "strategic read [company]", or when the user references a competitive analysis need. Weights job postings and product changes more heavily than press releases.
---

# Competitor Strategy Reverse-Engineer

## When to use this skill

The user needs to understand what a competitor is actually doing, building, hiring for, abandoning, and betting on. Most competitive intel relies on press releases, which is the least informative public signal a company emits. This skill pulls a broader set of signals and weights them appropriately.

## Input the user provides

- Competitor name (company)
- Optionally: the user's own positioning, to ground the comparison
- Optionally: the time window (default: last 12 months)

## What this skill does

1. Gathers public signals from the time window across multiple categories
2. Weights signals by predictive value (job postings > product launches > press releases > thought leadership)
3. Classifies signals by strategic vector
4. Produces a one-page memo in the structure below

## Signals to collect (in order of predictive value)

1. **Job postings** (most predictive of what they are building 6 months out). Pay particular attention to:
   - New role types not present 12 months ago
   - Geographic expansion in posting locations
   - Seniority level shifts (more VPs vs. more ICs)
   - Technical specializations being hired
2. **Product changes** (release notes, changelog, new product launches, pricing changes, deprecations)
3. **Executive movements** (hires, departures, role changes)
4. **Customer announcements** (named wins, case studies, logo additions)
5. **Pricing page changes** (often signals strategic shifts)
6. **Conference talks and content** (where their voice is going)
7. **Press releases** (least useful in isolation, useful as confirmation of other signals)

## Output structure

```
# Competitor Read: [Company]
*Time window: [start-end]. Signals analyzed: [count]. Confidence: [high/medium/low].*

## Headline
One sentence on what [Company] is actually doing right now.

## Strategic vectors they are betting on
1. **[Vector 1]**: evidence (which specific signals support this read)
2. **[Vector 2]**: evidence
3. **[Vector 3]**: evidence

## What they are not doing (or have quietly abandoned)
- [Abandoned vector 1]: evidence (job postings removed, product feature deprecated, etc.)
- [Abandoned vector 2]: evidence

## Leading indicators worth tracking
- [Job posting category to watch]
- [Product feature to watch for in next release]
- [Hire that would change the read]

## What this means for [User's company]
2-3 sentences on the implications. Not generic ("we should monitor this"). Specific ("their new VP of Sales is a signal they are moving up-market in Q3, which puts our mid-market positioning under pressure if they execute").

## Honest read on confidence
What is uncertain. What would resolve the uncertainty. Where the signals point in different directions.
```

## Calibration notes

- Job postings are the strongest leading indicator. A press release describes what shipped. A job posting describes what is being built 6 months out. Weight accordingly.
- Be specific about which signals support which vectors. "Their hiring suggests cloud focus" is weak. "Three new postings for AWS Solutions Architects in Q2 suggest they are building a cloud delivery capability they did not have 6 months ago" is useful.
- Acknowledge signal noise. Not every job posting is strategic. Backfills, attrition, and unrelated team growth all generate postings.
- If the company is private and signal-poor, say so explicitly. Do not invent strategic narratives from thin data.
- Do not be reflexively negative. Sometimes a competitor is genuinely executing well. Naming that is more useful than rationalizing it away.

## When NOT to use this skill

- Pre-IPO companies in stealth mode (signals will be too thin)
- Companies the user has no overlap with strategically (the analysis is academic)
- Adjacent companies that are not actually competitors (different lens needed)
