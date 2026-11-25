---
name: churn-signal-identification
description: "Identify behavioral, usage, and contextual signals that predict a customer is about to leave — before they cancel. Build an early warning system, not a postmortem. Use when churn is too high, building health scores, or designing proactive retention interventions."
---

# Churn Signal Identification

Spot the warning signs before customers leave, not after.

## How to use

- `/churn-signal-identification` Apply churn signal constraints to this conversation.
- `/churn-signal-identification <product>` Build a churn early warning system for the described product.

## Constraints

### The Churn Timeline
Churn has phases. Interventions MUST happen in the early invisible phase, not the decision phase.
- Invisible phase (weeks/months before): subtle behavior changes, slight usage dips
- Consideration phase (days/weeks before): evaluating alternatives, asking about exports
- Decision phase (days before): customer has decided. Usually too late.
- Action phase: cancel, don't renew, stop paying

### Signal Categories
MUST monitor all six categories:

1. Usage decay: login frequency drops, core action frequency drops, session duration decreases, feature breadth narrows
2. Engagement decay: stopped opening emails, unsubscribed from updates, support tickets drop to zero (gave up, not satisfied)
3. Team decay: active users on account decreasing, champion goes inactive, no new users added
4. Integration decay: disconnected integrations, reduced API calls, stopped syncing
5. Financial signals: downgraded plan, reduced seats, disputed invoice, asked about cancellation terms
6. Competitive signals: asked about data export, mentioned competitor in support, viewed comparison pages

### Signal Weighting
- MUST assign high/medium/low weight to each signal based on historical correlation with churn
- Champion going inactive = critical. Always investigate.
- Support ticket about export = high. Often means they're evaluating alternatives.
- Email open rate drop = low. Only meaningful as part of a pattern.
- NEVER treat a single low-weight signal as actionable. Look for clusters.

### Health Scoring
- Green: active usage, growing engagement. No action needed.
- Yellow: some decay signals. Trigger a check-in.
- Orange: multiple decay signals, clear downward trend. Proactive intervention.
- Red: major signals firing, usage near zero. Escalate to retention or senior contact.

### Intervention Matching
- Usage decay → re-engagement (personalized outreach, highlight unused features)
- Champion inactive → relationship (reach out directly, connect with replacement)
- Downgrade → value demonstration (ROI review, plan optimization)
- Export/cancellation inquiry → retention (understand the concern, don't hard-sell)
- Competitive signals → positioning (share differentiation, address specific gaps)
- MUST match intervention to signal. Generic "we miss you" emails make things worse.

### Anti-Patterns
- Only measuring churn at cancellation — that's measuring failure, not preventing it
- Treating all churn the same (free user vs. enterprise are different problems)
- Bombarding disengaged users with emails and calls — this accelerates churn
- Ignoring involuntary churn (failed payments) which is fixable with dunning
