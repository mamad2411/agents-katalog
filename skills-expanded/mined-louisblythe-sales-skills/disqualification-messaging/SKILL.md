---
name: disqualification-messaging
description: When the user wants to build or improve a sales bot's ability to gracefully end conversations with poor-fit prospects. Also use when the user mentions "disqualification," "not a fit," "poor fit messaging," "declining prospects," or "graceful rejection."
---

# Disqualification Messaging

You are an expert in building sales bots that gracefully end conversations with poor-fit prospects. Your goal is to help developers create systems that disqualify without burning bridges, maintain brand reputation, and potentially open doors for referrals.

## Why Graceful Disqualification Matters

### The Bad Disqualification
```
Bot discovers prospect is too small:

"Unfortunately, you're not a fit for our
product. Good luck!"

Prospect reaction:
- Feels dismissed
- Tells others about bad experience
- Never considers you again
- No referral opportunity
```

### The Good Disqualification
```
Same situation, better approach:

"Based on what you've shared, I think our
solution might be more than you need right
now. That said, here's a resource that might
help at your stage... And if your team grows
or needs change, I'd love to reconnect."

Prospect reaction:
- Feels respected
- May refer others
- Comes back when ready
- Positive impression of brand
```

## When to Disqualify

### Budget Mismatch
```
Signals:
- Budget is <50% of your minimum
- "We have no budget" (genuinely)
- Company too small to afford
- Explicit: "Way out of our range"

Timing:
- Disqualify early (save everyone time)
- After confirming no flexibility
```

### Need Mismatch
```
Signals:
- Problem doesn't match your solution
- Use case outside your capability
- They need something you don't offer
- Would require extensive customization

Timing:
- Once confirmed they need something else
```

### Authority Mismatch
```
Signals:
- No decision-making power
- Can't get to actual buyer
- Gatekeeper stonewalling
- Research project, not buying

Timing:
- After attempts to reach decision-maker fail
```

### Timing Mismatch
```
Signals:
- Not buying for 12+ months
- "Just researching for someday"
- No trigger event on horizon
- Explicit: "Not a priority this year"

Action:
- Move to long-term nurture, not disqualify
```

### Company Fit Mismatch
```
Signals:
- Wrong industry for your product
- Wrong company size
- Wrong geography
- Regulatory/compliance barriers

Timing:
- As soon as identified
```

## Disqualification Frameworks

### The "Not Right Now" Approach
```
When timing is the issue:

"Based on what you've shared, it sounds like
[your solution] isn't the right priority for
you right now—and that's okay.

Here's what I'd suggest:
• [Free resource that helps them now]
• Check back in [timeframe] when [trigger]

If anything changes, reach out anytime."

Leaves door open, positions future outreach.
```

### The "Better Alternative" Approach
```
When you're genuinely not the best fit:

"I want to be honest with you—for what you're
trying to do, we might not be the best fit.

Have you looked at [alternative/competitor]?
They specialize in [prospect's actual need].

If your needs change to [what you do well],
I'd love to chat then."

Builds trust through honesty.
```

### The "Not Yet" Approach
```
When they'll grow into your solution:

"Right now, our solution is probably more
than you need—and I'd hate for you to
overspend.

At your stage, I'd recommend [simpler alternative].
When you hit [growth milestone], that's usually
when companies like yours upgrade to us.

Can I check back in [timeframe]?"

Respects their stage, plans for future.
```

### The "Referral Pivot" Approach
```
When disqualifying:

"While we can't help you directly, I work
with a lot of [their type of company].

If you know anyone who [ideal customer profile],
I'd love an introduction. And if your situation
changes, my door's always open."

Turns disqualification into referral opportunity.
```

## Message Templates

### Budget Disqualification
```
"Thanks for being upfront about budget.
Our solution is built for larger investments,
so I don't think we're the right fit right now.

A few alternatives that might work better
for your budget:
• [Alternative 1]
• [Alternative 2]

If budget frees up or you scale up, definitely
reach back out. Happy to help then."
```

### Size/Stage Disqualification
```
"Based on your team size, our enterprise solution
would probably be overkill (and overpriced).

At your stage, I'd recommend starting with
[appropriate alternative]. It'll serve you well.

When you hit around [threshold], that's when
our solution starts making sense. I'll keep
your info and check in when I see you growing."
```

### Need Mismatch Disqualification
```
"I appreciate you explaining what you're looking
for. To be honest, what you need isn't our
sweet spot—we're really built for [your focus].

For [their need], you might want to look at
[better-fit solution]. They do that really well.

If you ever need [what you do], I'm here."
```

### Industry/Geographic Disqualification
```
"Unfortunately, we don't currently serve
[their industry/region]. Regulatory requirements
make it challenging for us.

I'd recommend checking out [alternative that
serves their space].

We're working on expanding—if that changes,
I'll let you know."
```

## Tone Guidelines

### Do
```
✓ Be direct but kind
✓ Explain why (briefly)
✓ Offer alternatives when possible
✓ Leave door open for future
✓ Thank them for their time
✓ Ask for referrals (when appropriate)
```

### Don't
```
✗ Ghost them (just stop responding)
✗ Be vague ("It's not going to work")
✗ Make them feel bad about their situation
✗ Burn the bridge permanently
✗ Disparage their company/situation
✗ Over-explain or justify excessively
```

## Post-Disqualification Actions

### CRM Updates
```
When disqualifying:

1. Update lead status: "Disqualified"
2. Add disqualification reason
3. Set future follow-up (if applicable)
4. Add to appropriate nurture track
5. Note referral potential

Don't just delete—track for future.
```

### Nurture Tracks
```
Disqualified leads by type:

Budget DQ → "When budget opens" track
  - Quarterly check-in
  - Budget season outreach

Stage DQ → "Growth nurture" track
  - Monthly content
  - Trigger-based reactivation

Need DQ → "Different need" track
  - Relevant content
  - Product expansion alerts
```

### Referral Follow-Up
```
If disqualification went well:

Day 2-3 later:
"Thanks again for the conversation. If anyone
in your network is looking for [your solution],
I'd appreciate the intro. Happy to return
the favor!"

Warm disqualifications = referral opportunities.
```

## Automation

### Disqualification Detection
```python
def should_disqualify(prospect, qualification_data):
    reasons = []

    # Budget check
    if qualification_data.budget:
        if qualification_data.budget < MIN_DEAL_SIZE * 0.5:
            reasons.append("budget_too_low")

    # Size check
    if prospect.company_size < MIN_COMPANY_SIZE:
        reasons.append("company_too_small")

    # Industry check
    if prospect.industry in EXCLUDED_INDUSTRIES:
        reasons.append("industry_excluded")

    # Need check
    if qualification_data.needs:
        fit_score = calculate_need_fit(qualification_data.needs)
        if fit_score < 0.3:
            reasons.append("need_mismatch")

    return {
        "should_disqualify": len(reasons) > 0,
        "reasons": reasons,
        "recommended_action": get_recommended_action(reasons)
    }
```

### Message Selection
```python
def generate_disqualification_message(prospect, reasons):
    primary_reason = reasons[0]  # Main reason

    templates = {
        "budget_too_low": get_budget_dq_template(prospect),
        "company_too_small": get_size_dq_template(prospect),
        "industry_excluded": get_industry_dq_template(prospect),
        "need_mismatch": get_need_dq_template(prospect)
    }

    message = templates.get(primary_reason)

    # Add referral ask if appropriate
    if prospect.engagement_score > 0.6:
        message += "\n\n" + get_referral_ask()

    # Add future outreach offer if timing-related
    if primary_reason in ["budget_too_low", "company_too_small"]:
        message += "\n\n" + get_future_check_in_offer(prospect)

    return message
```

## Metrics

### Disqualification Quality
```
Track:
- Disqualification response rate
- Sentiment of disqualified prospects
- Referrals from disqualified prospects
- Reactivation rate (came back later)
- Brand mentions/reviews post-DQ

Measure quality of exit, not just quantity.
```

### Efficiency Metrics
```
Track:
- Time to disqualify (faster = less waste)
- Pipeline health (fewer bad fits lingering)
- Rep time saved
- Cost per disqualification

Early DQ = efficient pipeline.
```

## Edge Cases

### Persistent Poor-Fit Prospects
```
When they won't accept disqualification:

"I appreciate your interest, but I want to
be respectful of your time. We're genuinely
not able to help with what you need.

I've shared some alternatives that can.
If your situation changes significantly,
I'm happy to reassess."

Be firm but kind. Don't string them along.
```

### High-Profile Poor Fits
```
Important company, wrong fit:

- Escalate to human for handling
- More personalized disqualification
- Explore other potential within company
- Stronger referral ask

"While [specific need] isn't our strength,
I'd love to stay connected. Other teams at
[their company] might have different needs
we could help with."
```

### Competitor Customers
```
Using competitor, not switching:

"Thanks for taking the time. Since [competitor]
is working for you, it makes sense to stick
with them.

If you ever reevaluate or need a second opinion,
I'm happy to chat. Good luck with [their project]."

Leave impression for future consideration.
```

