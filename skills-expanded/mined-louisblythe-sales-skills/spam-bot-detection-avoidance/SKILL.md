---
name: spam-bot-detection-avoidance
description: When the user wants to build or improve a sales bot's ability to write and send messages in patterns that don't trigger carrier or email spam filters. Also use when the user mentions "deliverability," "spam filters," "avoiding spam," "email deliverability," "carrier filtering," or "message delivery."
---

# Spam/Bot Detection Avoidance

You are an expert in message deliverability for sales automation. Your goal is to help developers create systems that maintain high deliverability while scaling outreach.

## Understanding Filtering Systems

### Email Spam Filters
```
What they look for:
- Known spam patterns/phrases
- Sender reputation
- Engagement rates
- Authentication (SPF, DKIM, DMARC)
- Link/image ratios
- HTML quality
- Sending volume patterns
```

### SMS/Carrier Filtering
```
What triggers filtering:
- Message velocity (too many too fast)
- Identical messages to many recipients
- URL shorteners
- Known spam keywords
- Unregistered sender IDs
- Pattern recognition
- Complaint rates
```

## Email Deliverability

### Content Best Practices
```
DO:
- Write like a human (not a template)
- Use plain text or minimal HTML
- Personalize genuinely
- Include clear sender identity
- Balance text/link ratio
- Use full URLs (not shortened)
- Include unsubscribe option

DON'T:
- Use ALL CAPS
- Multiple exclamation marks!!!
- Spam trigger words excessively
- Image-heavy emails
- Attach files in cold outreach
- Use misleading subject lines
- Hide unsubscribe
```

### Spam Trigger Words
```
High risk (avoid):
- FREE, FREE!!!
- Act now, Limited time
- Congratulations, You've won
- 100% guaranteed
- No obligation
- Click here, Click below
- Urgent, Important

Moderate risk (use sparingly):
- Discount, Sale, Deal
- Buy, Order, Purchase
- Cash, Money, Income
- Amazing, Incredible
- Opportunity
```

### Subject Line Guidelines
```
Good:
- "Question about [Company]'s [process]"
- "Following up on [topic]"
- "[Name], quick thought"
- "Idea for [specific challenge]"

Bad:
- "URGENT: Open immediately"
- "You won't believe this offer"
- "Re: Your inquiry" (when no prior contact)
- "[NAME] - TIME SENSITIVE!!!"
```

### Sending Patterns
```
Warm-up new domains:
Week 1: 20-50 emails/day
Week 2: 50-100 emails/day
Week 3: 100-200 emails/day
Week 4+: Gradually increase

Maintain:
- Consistent daily volume
- No sudden spikes
- Send during business hours
- Mix of recipients (not all cold)
```

### Technical Setup
```
Required:
- SPF record configured
- DKIM signing enabled
- DMARC policy set
- Custom tracking domain
- Dedicated IP (for volume)

Monitor:
- Bounce rates (<2% target)
- Spam complaints (<0.1%)
- Open rates (benchmark)
- Blacklist status
```

## SMS Deliverability

### Number Registration
```
For business SMS:
- Register 10DLC (US)
- Get proper throughput
- Complete carrier registration
- Maintain good standing

For high volume:
- Use toll-free numbers
- Consider short codes
- Register with carriers
```

### Content Guidelines
```
DO:
- Identify yourself clearly
- Keep messages concise
- Use natural language
- Vary message content
- Include opt-out method
- Respect quiet hours

DON'T:
- Send identical messages en masse
- Use URL shorteners (bit.ly, etc.)
- Include loan/financial offers
- Send late night (after 9pm)
- Spam emoji 🎉🔥💰
- Use ALL CAPS
```

### Velocity Management
```
Per number limits:
- New numbers: 1-2 msgs/minute
- Established: 3-5 msgs/minute
- Short codes: Higher volume

Spacing:
- Add random delays (15-60 sec)
- Don't send in bursts
- Spread across time windows
```

### Carrier-Specific Patterns
```
Carriers filter differently:

AT&T:
- Strict on URL shorteners
- Watches for duplicate content
- Reviews high-volume senders

T-Mobile:
- Aggressive pattern matching
- Requires registration
- Monitors complaint rates

Verizon:
- URL verification
- Content filtering
- Volume thresholds
```

## Message Variation Strategies

### Template Spinning
```
Instead of one message to 1000 people:

Template with variations:
"Hi [First_Name],

[Opener_Variation]

[Value_Prop_Variation]

[CTA_Variation]

[Signature_Variation]"

Combinations create hundreds of unique messages.
```

### Variable Elements
```
Openers:
- "I noticed [Company] is [observation]."
- "Saw that [Company] recently [event]."
- "Your [role] caught my attention because..."
- "Quick question about [topic]..."

Value props:
- "We help [similar companies] [outcome]."
- "Most [role]s struggle with [problem]. We fix that."
- "Thought of you when [trigger]."

CTAs:
- "Worth a quick chat?"
- "Open to learning more?"
- "Would it make sense to connect?"
- "Interested in seeing how it works?"
```

### Natural Variation
```
Add human elements:
- Minor typos (occasionally, subtly)
- Varying punctuation
- Different greetings (Hi/Hey/Hello)
- Varying sign-offs
- Different spacing patterns
- Time-of-day references
```

## Engagement Best Practices

### Maintain Positive Signals
```
Email:
- High open rates (aim 20%+)
- Low bounce rates (<2%)
- Few spam reports (<0.1%)
- Replies (good engagement signal)

SMS:
- Response rate
- Low opt-out rate
- No carrier complaints
- Engaged conversations
```

### Handle Negative Signals
```
Immediately:
- Remove hard bounces
- Honor opt-outs
- Stop messaging non-responders
- Reduce volume if metrics drop

Proactively:
- Clean lists regularly
- Verify emails before sending
- Validate phone numbers
- Remove disengaged contacts
```

## Compliance Integration

### Required Elements
```
Email:
- Physical address
- Unsubscribe link
- Company identification
- Honest subject lines

SMS:
- Business identification
- Opt-out instructions (STOP)
- Consent documentation
- Time restrictions
```

### Consent Management
```
Track:
- How consent was obtained
- When consent was given
- What they consented to
- Opt-out requests

Respect:
- Opt-out immediately (<24 hours)
- Don't re-add opted-out contacts
- Segment by consent type
- Honor channel preferences
```

## Monitoring & Recovery

### Key Metrics to Track
```
Email:
- Delivery rate (>95% target)
- Inbox placement rate
- Bounce rate (<2%)
- Spam complaint rate (<0.1%)
- Blacklist status

SMS:
- Delivery rate (>97% target)
- Carrier filtering rate
- Opt-out rate
- Response rate
```

### Recovery from Issues
```
If deliverability drops:

1. Stop sending immediately
2. Identify the cause
3. Fix the issue
4. Clean your list
5. Warm up again slowly
6. Monitor closely

If blacklisted:
1. Identify which blacklist
2. Determine the cause
3. Fix underlying issue
4. Request delisting
5. Prevent recurrence
```
