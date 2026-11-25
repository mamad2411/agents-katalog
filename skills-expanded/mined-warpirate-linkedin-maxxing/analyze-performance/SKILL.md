---
name: analyze-performance
description: |
  Use when user has been posting on LinkedIn at least 4 weeks and wants
  to know what is landing, run a quarterly content review, or diagnose
  dropping engagement. Trigger phrases include "analyze my LinkedIn
  performance," "which of my posts are working," "what should I post
  more of," "why is my engagement dropping," or when user uploads a
  LinkedIn analytics CSV.
license: MIT
---

# Analyze performance

Most LinkedIn AI tools that claim "analytics" either show the user numbers they could see in their dashboard, or generate generic advice based on the numbers without actually reading them. This skill exists to do the analysis work: read the data carefully, group posts by what they had in common, and identify which patterns the user should do more or less of.

## Why this skill exists

LinkedIn now exposes more performance data than it used to. The Creator dashboard analytics export includes impressions, unique viewers, clicks, reactions broken out by type, comments, shares, and engagement rates per post. Plus the larger LinkedIn data archive has every post's text content.

But almost nobody actually looks at this data. They glance at impression counts, get discouraged or encouraged, and keep posting. The result is that they never learn what is working. This skill exists to do the analysis the user does not do.

## When to use this skill

Trigger when:
- The user has been posting consistently for at least 4 weeks (otherwise the sample is too small)
- The user wants a quarterly content review
- The user notices engagement dropping and wants to know why
- The user is about to commit to a posting cadence and wants to make sure they are pointed at the right pillars
- The user uploaded an analytics CSV

Do NOT trigger when:
- The user wants to know about one specific post. Send to review-post.
- The user has been posting for less than 4 weeks. Tell them honestly: the sample is too small to draw conclusions. Wait.

## What you need from the user

The LinkedIn analytics export. They can get this from:
- LinkedIn Creator dashboard → Content → Export (per-post metrics)
- LinkedIn data export → larger archive (includes post text)

If the user has only post text and no analytics, the analysis is limited; tell them so and suggest they get the analytics export from the Creator dashboard (instant download, no waiting).

Useful additional inputs:
- The user's content-plan.md if plan-content has been run (so analysis can group by pillar)
- The user's voice-profile.md (less important here, but useful for noting voice-related patterns)

## How to analyze

Do not throw averages and call it analysis. Three steps:

### Step 1: Cluster the posts

Group posts by:
- **Pillar** (if plan-content was run; otherwise infer 3-5 topical clusters from the data)
- **Format** (text, carousel, video, article, image)
- **Hook type** (number, confession, contrarian claim, story, fact, change of mind)
- **Length** (short < 800 chars, medium 800-1500, long 1500+)
- **Closing pattern** (question, single sentence, list, CTA)

These clusters are where the insights live. An aggregate "your average engagement rate" tells the user almost nothing. "Your carousels with 8-12 slides get 3.5x the engagement of your text posts, but your text posts with confessional hooks beat the average of both" tells them what to do.

### Step 2: Find the patterns

For each cluster, look at:
- **Median engagement rate** (use median, not mean; outliers skew means badly)
- **Dwell-time signal** (when available; otherwise use comments + reactions as proxy)
- **Comment quality** (count of comments above a substantive threshold, not all comments equal)
- **Audience signal** (who is engaging: peers, prospects, strangers; visible in the Followers analytics)

What you are looking for: clusters that significantly outperform or underperform the user's overall median, in ways that are repeatable.

A pattern is only a pattern if:
- It shows up at least 3 times
- The effect size is meaningful (>50% above or below the median, ideally)
- It is repeatable (not a one-off post that went viral for unrelated reasons)

### Step 3: Identify the outliers

Two types matter:

- **Outperforming outliers:** posts that did far better than the user's median. What did they have in common? This is what the user should do more of.
- **Underperforming outliers:** posts that did far worse than the user's median. What did they have in common? This is what the user should drop.

Be honest about both. The job is to give the user signal, not to make every post look like a learning.

## What to output

```
# Performance analysis for [user's name or "user"]

Period analyzed: [start - end]
Posts analyzed: [N]
Median engagement rate: [N]%
Overall trajectory: [growing / flat / declining]

## What is working

### Pattern 1: [name of the pattern, e.g., "Carousels on engineering management"]
Posts in this pattern: [N]
Median engagement: [N]% (vs overall median of [N]%)
Why this is working: [one paragraph on what is specific to these posts]

### Pattern 2: ...

[2-4 strongest patterns]

## What is not working

### Pattern A: [e.g., "Posts with motivational hooks"]
Posts in this pattern: [N]
Median engagement: [N]% (vs overall median of [N]%)
Why this is likely failing: [one paragraph]

### Pattern B: ...

[1-3 weakest patterns]

## Notable outliers

### Best-performing post: [date, hook]
Why this likely worked: [analysis]

### Worst-performing post: [date, hook]
Why this likely failed: [analysis]

## Recommendations

1. [Specific, actionable. "Do more carousels on engineering management with confession-style hooks." Not "Improve your engagement."]
2. [Next]
3. [Next]
[3-5 recommendations]

## What I cannot conclude from the data

[Honest note on the limits of the analysis: small sample sizes, missing dwell time data, posts where the variable changes too much to isolate, etc.]
```

## A note on what NOT to conclude

The most dangerous outputs of content analytics are wrong patterns the user then optimizes for. Avoid:

- **Survivorship bias.** One post about a controversial topic went viral; that does not mean controversial topics work in general. Look for the pattern across multiple posts.
- **Format vs. content confusion.** "Carousels outperform text" might be true, or it might be that the user's carousel topics happen to be stronger than their text topics. Disentangle when possible.
- **Reading vanity metrics as engagement.** A post with 10,000 impressions and 12 reactions is worse than a post with 1,500 impressions and 30 substantive comments. Impressions are the easiest metric to inflate and the least meaningful.
- **Calling 4 weeks "trending."** Most claimed LinkedIn trends are sampling noise. A pattern needs to hold for 8-12 weeks before treating it as durable.
- **Recommending posting frequency increases without evidence.** "Post more" is almost never the answer unless the user is posting less than 1x/week.

## What this skill does not do

- Predict which specific future post will perform. Patterns suggest what to do more of; they do not guarantee outcomes.
- Score posts on a 1-10 scale. Composite scores hide more than they reveal.
- Generate the next post for the user. That is write-post's job. This skill identifies what to write about more of.
- Compare the user to other creators. Cross-account benchmarks require data this skill does not have, and the comparison is often misleading anyway.
- Promise specific growth from following the recommendations. Engagement is influenced by too many variables outside the user's control.
