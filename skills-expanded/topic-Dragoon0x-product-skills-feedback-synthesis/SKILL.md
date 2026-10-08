---
name: feedback-synthesis
description: "Turn raw customer feedback from multiple sources into clear product insights and priorities. Covers feedback collection, pattern recognition, and separating signal from noise. Use when feedback feels overwhelming, contradictory, or when the team can't agree on what users actually want."
---

# Feedback Synthesis (Customer Empathy)

Turn messy feedback into clear priorities the team can act on.

## How to use

- `/feedback-synthesis` Apply feedback synthesis constraints to this conversation.
- `/feedback-synthesis <feedback data>` Synthesize the provided feedback into actionable insights.

## Constraints

### Collection
- MUST gather feedback from multiple channels: support tickets, sales calls, user interviews, surveys, social media, app reviews
- MUST capture the user's actual words, not just the PM's interpretation
- SHOULD tag feedback with: user segment, frequency, severity, and source
- NEVER rely on a single channel — each has its own bias
- MUST distinguish between who gave the feedback and how representative they are

### Pattern Recognition
- MUST look for themes, not individual requests. One user wanting X is anecdote. Twenty is a pattern.
- SHOULD cluster feedback by underlying problem, not by proposed solution
- MUST weight feedback by user segment relevance — feedback from your target segment matters more
- SHOULD track frequency and recency — a problem mentioned 50 times this month beats one mentioned 5 times last year
- NEVER treat loud feedback as representative. Vocal users are a minority.

### Signal vs. Noise
- Feature requests are solutions, not problems. MUST translate "I want X" into "I'm struggling with Y"
- MUST separate pain (something broken or missing) from desire (something nice to have)
- SHOULD deprioritize feedback that only applies to a segment you're not targeting
- MUST check if feedback contradicts usage data — sometimes what users say and do are different
- NEVER let one large customer's request override patterns from many smaller customers without deliberation

### Actionability
- Every synthesis MUST end with a prioritized list of insights, not just a summary
- Each insight MUST connect to a product decision: build, investigate further, or deprioritize
- SHOULD present insights to stakeholders with evidence (quotes, volume, impact)
- MUST close the loop: tell feedback sources what you did with their input
- NEVER synthesize feedback and leave it in a doc. It MUST reach roadmap discussions.

### Anti-Patterns
- The Echo Chamber: only hearing from power users who love the product
- Request-Driven Building: building exactly what users ask for instead of solving underlying problems
- Feedback Fatigue: collecting so much that none of it gets processed
- The Spreadsheet Graveyard: meticulously logging feedback that nobody reads
- Recency Bias: overweighting whatever came in this week over long-term patterns
