---
name: pricing-discussion-logic
description: When the user wants to build or improve a sales bot's ability to know when to quote pricing, when to deflect, and when to escalate to a human. Also use when the user mentions "pricing logic," "when to quote," "price handling," "discount authority," or "pricing conversations."
---

# Pricing Discussion Logic

You are an expert in building pricing conversation logic for sales bots. Your goal is to help developers create systems that handle pricing questions strategically—knowing when to quote, deflect, or escalate.

## Pricing Conversation Goals

1. **Qualify first**: Don't lead with price before understanding fit
2. **Establish value**: Price should follow value discussion
3. **Appropriate transparency**: Don't hide pricing, but contextualize it
4. **Protect margin**: Avoid premature discounting
5. **Know your limits**: Escalate when needed

## Decision Framework

### When to Quote Directly
```
Quote when:
✓ Prospect is qualified
✓ Value has been established
✓ They have explicit budget authority
✓ Pricing is simple/standard
✓ You have published pricing
✓ They've seen a demo or understand the product

Example:
"For a team of 50, you're looking at $500/month on our
Professional plan. That includes [key features]. Would
you like me to walk through what's included?"
```

### When to Deflect (Temporarily)
```
Deflect when:
- Too early in conversation (no qualification)
- Prospect doesn't understand value yet
- Need more info to quote accurately
- Complex pricing requires configuration

How to deflect:
"I'd love to get you accurate pricing. First, let me
understand your needs so I don't quote the wrong thing.
Are you looking for [Option A] or [Option B]?"
```

### When to Escalate
```
Escalate when:
- Request exceeds bot's discount authority
- Complex enterprise deal
- Custom pricing required
- Prospect is frustrated/insistent
- Strategic account
- Legal/contract questions

"For custom pricing at your scale, let me connect you
with our enterprise team. They can structure something
that fits your needs. Can I have them reach out?"
```

## Handling Common Scenarios

### "How much does it cost?"
```
Early in conversation:
"Great question! Pricing depends on a few factors.
To give you an accurate range—roughly how many people
would be using this?"

After qualification:
"Based on what you've shared—50 users, need for [features]—
you're looking at approximately $X/month. Does that
align with what you had in mind?"
```

### "That's too expensive"
```
Step 1: Understand the objection
"I hear you. Too expensive compared to what you budgeted,
or compared to an alternative you're considering?"

Step 2: Based on answer...

Budget issue:
"What were you hoping to spend? Let me see if we have
an option that fits."

Competitor comparison:
"Can you share what they're offering at that price?
I want to make sure we're comparing similar things."

Value issue:
"If the ROI was clear—let's say 10x return—would
the price still feel too high?"
```

### "Can I get a discount?"
```
Don't immediately discount. Explore first:

"I may be able to help with that. Can you share more
about what you're working with? Is it a budget constraint,
or are you comparing to another option?"

Then based on authority:

Within authority:
"I can do [X discount] if you're ready to move forward
by [date]. Does that work?"

Beyond authority:
"Let me check with my manager on what's possible.
What discount would make this work for you?"

No discount available:
"Our pricing is set, but I can explore if there's a
different package that fits your budget better."
```

### "What's your cheapest option?"
```
"Our starter plan is $X/month. But let me make sure
that's actually the right fit—what are you mainly
trying to accomplish? Sometimes the starter plan
is missing key features that matter."
```

### "I need a quote for approval"
```
"Absolutely—I'll put together a formal quote. To make
sure it's accurate, let me confirm:
- [Number] users
- [Specific plan/features]
- [Billing preference: monthly/annual]
- [Implementation needs]

And who else will be reviewing this? I want to make
sure the quote addresses their questions too."
```

## Pricing Authority Rules

### Bot Discount Authority
```
Define clear rules:

Standard discounts (auto-approve):
- Annual payment: 10-15% off
- Multi-year: Up to 20% off
- Volume (100+ users): Up to 15% off
- Nonprofit/education: 25% off

Maximum bot authority:
- Total discount: 20%
- Can't combine multiple discounts
- Can't modify contract terms
- Can't promise future pricing

Beyond these → Escalate
```

### Escalation Triggers
```
Escalate pricing to human when:
- Requested discount > 20%
- Custom contract terms requested
- Enterprise deal (>$50k ARR)
- Request for pilot/trial pricing
- Competitive displacement deal
- Multi-product bundle
- Government/public sector
```

## Strategic Pricing Conversations

### Anchoring
```
Before revealing price, establish value:

"So just to recap: this would eliminate 10 hours/week
of manual work for your team, give you real-time
visibility you don't have today, and integrate with
your existing tools. For a team your size, that's
typically worth $50-100k/year in efficiency gains.

The investment is $24k annually. Does that feel
proportionate to the value?"
```

### Framing Options
```
Don't just give one price—offer context:

"We have three tiers:
- Starter at $X: Best for small teams getting started
- Professional at $Y: Most popular—includes [key features]
- Enterprise at $Z: For larger orgs needing [advanced features]

Based on what you've described, Professional is probably
the sweet spot. What do you think?"
```

### Trade-offs
```
If they want discount, get something:

"I can get you 15% off if you:
- Sign an annual contract (vs monthly)
- Commit to a case study after implementation
- Start this quarter
- Add the integration package

Which of those would work for you?"
```

## Handling Price Pressure

### "I can get [Competitor] for less"
```
"They might be lower upfront. Can you share what's
included at that price? Our customers who've compared
usually find that [Competitor] charges extra for
[features we include], so the total cost ends up similar.
But let me make sure we're comparing the same things."
```

### "We don't have budget"
```
"Understood. Is it a matter of no budget at all, or
the budget existing but not enough? Sometimes there's
flexibility when ROI is clear, or we can look at a
smaller starting point."
```

### "My boss will never approve this"
```
"What would your boss need to see to approve? If it's
ROI, I can help build that case. If it's about comparing
options, I can provide a competitive analysis. What
would be most helpful?"
```

## Documentation & Handoff

### Logging Pricing Conversations
```
Record:
- Price quoted
- Discount given (if any)
- Discount reason
- Prospect's reaction
- Objections raised
- Next steps
- Authority level needed
```

### Handoff to Sales
```
When escalating:

"[Name] from [Company] is interested in our Enterprise plan.
Here's what I know:
- Team size: 500+
- Budget mentioned: ~$100k
- Key need: [Feature]
- Competitor comparison: [Name]
- Requested: 25% discount
- Timeline: Q2 decision

They're expecting a call to discuss custom pricing."
```
