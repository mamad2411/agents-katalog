---
name: sentiment-analysis
description: "Analyzes customer sentiment from reviews, social media, and support tickets with trend tracking, theme categorization, and alert recommendations. Use for brand health monitoring."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Sentiment Analysis

## When to Use This Skill

Use this skill when you need to:
- Analyze customer sentiment from reviews, social posts, or support tickets
- Track brand perception trends over time
- Categorize feedback themes to prioritize product or service improvements
- Set up a sentiment monitoring framework for ongoing use

**DO NOT** use this skill for social media content creation, customer service response writing, or NLP model building. This is for interpreting and acting on customer sentiment data.

---

## Core Principle

SENTIMENT IS A LEADING INDICATOR — DECLINING SENTIMENT PREDICTS CHURN, NEGATIVE REVIEWS, AND REVENUE LOSS BEFORE THEY SHOW UP IN YOUR FINANCIALS.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Data sources** | "Where is the feedback? (Google reviews, App Store, social media, support tickets, surveys)" | Must be provided |
| **Volume** | "Roughly how many pieces of feedback to analyze?" | 50-200 |
| **Time period** | "What date range?" | Last 90 days |
| **Focus** | "What do you want to understand? (overall sentiment, specific product, competitor comparison)" | Overall brand sentiment |
| **Segments** | "Any segments to analyze separately? (product line, customer tier, channel)" | Overall first |
| **Existing tracking** | "Do you have any sentiment tracking in place?" | None |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Analyze

### Sentiment Scoring Framework

Classify each piece of feedback:
- **Positive** — praise, satisfaction, recommendation
- **Neutral** — factual, no strong emotion, mixed
- **Negative** — complaint, frustration, warning to others

### Theme Categorization

Tag every piece of feedback with 1-2 themes:
- Product quality, pricing, customer service, delivery/speed, usability, feature requests, competitor mentions, billing issues

### Analysis Dimensions

1. **Overall sentiment distribution** — % positive, neutral, negative
2. **Sentiment by theme** — which topics generate the most negativity?
3. **Sentiment trend** — is sentiment improving or declining over time?
4. **Volume trend** — are more people talking? (volume increase + negative sentiment = alarm)
5. **Competitive mentions** — how often do customers mention competitors and in what context?

**GATE: Present preliminary findings and confirm focus areas for the full report.**

---

## Phase 3: Build

### Deliverables

**1. Sentiment Analysis Report**
- Overall sentiment score and distribution
- Theme-by-theme sentiment breakdown
- Trend chart over the analysis period
- Top 10 representative quotes (positive and negative)
- Competitive mention summary

**2. Issue Priority Matrix**
| Theme | Sentiment | Volume | Trend | Priority |
|-------|-----------|--------|-------|----------|
| Customer service | Negative | High | Worsening | Critical |
| Product quality | Positive | High | Stable | Protect |
| Pricing | Mixed | Medium | Stable | Monitor |

**3. Alert Framework**
Define triggers for ongoing monitoring:
- Negative sentiment exceeds 30% in any week
- New negative theme appears that was not previously tracked
- Star rating drops below 4.0 on any review platform
- Competitor mentioned positively more than 10% of the time

**4. Response Playbook**
- Template responses for common negative themes
- Escalation criteria for serious complaints
- Proactive outreach triggers for at-risk customers

---

## Phase 4: Polish

### Monitoring Dashboard Spec

Recommend a simple tracking system:
- Weekly sentiment score by source
- Theme trend tracking (monthly)
- Alert log for triggered notifications

### Quarterly Sentiment Review

Template for a quarterly deep-dive comparing current sentiment to previous quarter with action plan updates.

---

## Example 1: App Store Reviews (150 reviews, SaaS mobile app)

**Finding:** 72% positive, 18% negative, 10% neutral. Top negative theme: onboarding confusion (8 mentions). Top positive: time-saving features.
**Action:** Improve onboarding flow, create tutorial videos.

## Example 2: Google Reviews (80 reviews, local service business)

**Finding:** 4.2 average stars. Negative reviews cluster around wait times (6 mentions) and billing clarity (4 mentions). Positive reviews highlight staff quality.
**Action:** Address wait time communication, simplify billing invoices.

---

## Anti-Patterns

- **Ignoring negative feedback** — 1 negative review often represents 10 silent churners. Take complaints seriously.
- **Counting stars without reading text** — a 3-star review with specific feedback is more useful than a 5-star "Great!" Read the content.
- **Analyzing once and forgetting** — sentiment shifts over time. Set up ongoing monitoring, not one-time reports.
- **Responding defensively** — negative sentiment analysis should drive improvement, not defensive PR responses.
- **Overreacting to one bad review** — look for patterns. One complaint is an anecdote; five on the same topic is a trend.

---

## Recovery

- **Very few reviews to analyze:** Supplement with support ticket data, social media comments, or direct customer interviews.
- **Overwhelmingly positive (suspicious):** Dig deeper — are reviews incentivized? Check for patterns suggesting fake reviews.
- **User takes negative feedback personally:** Reframe as a competitive advantage — you now know exactly what to fix. Competitors are guessing.
- **No ongoing monitoring resources:** Set up Google Alerts and a monthly 30-minute review habit. Low-effort monitoring beats no monitoring.
