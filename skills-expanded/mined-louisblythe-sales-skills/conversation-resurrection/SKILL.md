---
name: conversation-resurrection
description: When the user wants to build or improve a sales bot's ability to re-engage dead threads weeks or months later. Also use when the user mentions "conversation resurrection," "dead lead revival," "re-engagement," "cold thread revival," or "dormant prospect outreach."
---

# Conversation Resurrection

You are an expert in building sales bots that intelligently revive stalled conversations. Your goal is to help developers create systems that re-engage prospects with contextually relevant hooks long after initial contact went cold.

## Why Resurrection Matters

### The Dormant Opportunity
```
Reality of sales pipelines:
- 80% of leads don't convert on first sequence
- Average prospect needs 8-12 touches
- Timing is often wrong, not interest
- Circumstances change over months

Dead doesn't mean dead forever.
```

### The Resurrection Advantage
```
Well-timed revival:
- Lower competition (others gave up)
- Circumstances may have changed
- New budget cycles, new priorities
- Previous awareness reduces friction

"Hey, we talked 6 months ago about X.
Given [relevant trigger], thought it might
be worth reconnecting."
```

## Resurrection Triggers

### Time-Based Triggers
```
Calendar milestones:
- 30 days since last contact (warm revival)
- 90 days since last contact (quarterly check-in)
- 6 months (new budget cycle potential)
- 12 months (annual review, new year)
- Anniversary of their signup/trial

"It's been a few months since we connected.
A lot can change in a quarter—wanted to
check if [problem] is still on your radar."
```

### Event-Based Triggers
```
External signals:
- Company funding announcement
- New executive hire
- Expansion news
- Competitor mention in news
- Industry regulation change
- Product launch from them

"Congrats on the Series B! When we talked
in March, scaling was a future concern.
Guessing it's more urgent now?"
```

### Behavioral Triggers
```
Re-engagement signals:
- Visited website again
- Opened old email
- Downloaded new content
- Engaged on social media
- Colleague from company engaged

"Noticed you were back on our site—timing
might be better now than when we last talked?"
```

### Internal Triggers
```
Your side changes:
- New feature launched (addresses their objection)
- Price change (if they had budget concerns)
- New case study (their industry/size)
- Integration added (their tech stack)

"When we talked in Q2, you mentioned needing
[feature]. Just launched it—thought you'd
want to know."
```

## Context Retention

### What to Remember
```
From original conversation:
- Their stated pain points
- Objections raised
- Why they went cold
- Key stakeholders mentioned
- Timeline they shared
- Budget context

Store structured:
{
  "prospect_id": "12345",
  "last_contact": "2024-01-15",
  "conversation_summary": "Interested but budget locked until Q2",
  "pain_points": ["manual reporting", "Salesforce integration"],
  "objections": ["timing", "budget"],
  "dormant_reason": "asked to reconnect after Q1",
  "revival_hooks": ["Q2 budget", "reporting feature"]
}
```

### Context Application
```
Generic revival (bad):
"Hi! Just checking in to see if you're
still interested in our product."

Contextual revival (good):
"Hi Sarah—when we talked in January, you
mentioned budget was locked until Q2 and
reporting was your biggest pain. Now that
we're in Q2 and you're probably planning,
is it worth a fresh look?"

Reference their specific situation.
```

## Revival Message Frameworks

### The "Relevant Update" Framework
```
Structure:
1. Reference previous conversation
2. Share relevant update
3. Connect to their stated need
4. Low-pressure ask

Example:
"Hi [Name], we spoke in [month] about
[their pain point]. Since then, we've
[relevant update that addresses their need].

Given what you shared about [specific detail],
thought it might be worth a quick look.
Worth 15 minutes to see what's changed?"
```

### The "Trigger Event" Framework
```
Structure:
1. Acknowledge the event
2. Connect to previous conversation
3. Explain relevance
4. Offer value

Example:
"Saw the news about [company event]—congrats!

When we talked earlier this year, [scaling/growth]
was on the horizon. Guessing that's more
front-and-center now?

Happy to share how [similar company] handled
this same transition if it would help."
```

### The "Value-First" Framework
```
Structure:
1. Lead with something useful
2. Reference past conversation
3. Soft reconnection

Example:
"[Name], just published a guide on [topic
related to their pain]. Given our conversation
about [their challenge], thought you might
find it useful: [link]

If things have changed since [month], happy
to catch up. If not, no worries—hope the
guide helps either way."
```

### The "Honest Check-In" Framework
```
Structure:
1. Direct acknowledgment of time passed
2. Respect their previous position
3. Simple question

Example:
"Hi [Name]—it's been [time] since we talked.
You mentioned [reason for pause].

Curious if anything's changed, or if this
is still not the right time. Either way,
wanted to keep the door open."

Low pressure, high respect.
```

## Timing Intelligence

### Optimal Revival Windows
```
By dormant reason:

"Timing not right":
→ Revival at 60-90 days
→ Begin of new quarter
→ After fiscal year change

"Budget locked":
→ Revival at budget cycle start
→ Q1 for calendar-year companies
→ Ask when their fiscal year starts

"Using competitor":
→ Revival at 6-12 months
→ Contract renewal period
→ If competitor news is negative

"Not a priority":
→ Revival if trigger event occurs
→ Otherwise 6-month check-in
→ Lead with new value/content
```

### Day/Time for Revival
```
Best practices:
- Tuesday-Thursday (avoid Monday chaos, Friday checkout)
- Mid-morning (9-11am local)
- Mid-week of month (avoid beginning/end crunches)

Avoid:
- Holiday weeks
- Major industry events
- Their known busy periods (if logged)
```

## Sequence Design

### Revival Sequence Structure
```
Touch 1 (Day 0): Contextual reconnection
→ Reference past conversation + new hook
→ Low-pressure, value-focused

Touch 2 (Day 5): Value add
→ Share relevant content/insight
→ No direct ask

Touch 3 (Day 12): Direct ask
→ Specific meeting request
→ Easy yes/no

Touch 4 (Day 20): Break-up
→ Close the loop
→ Leave door open

Shorter than initial outreach—they know you.
```

### Multi-Channel Revival
```
Coordinate across channels:

Day 0: Email (primary revival message)
Day 3: LinkedIn (if no response, different angle)
Day 7: Email follow-up
Day 14: SMS (if opted in, brief check-in)
Day 21: Final email (break-up)

Don't use all channels at once—escalate gradually.
```

## Handling Responses

### Positive Response
```
"Actually, yeah, timing is better now."

Response:
"Great to hear! A lot's probably changed
since [month]. Would love to hear what's
shifted on your end and show you what's
new on ours.

Does [specific time] work this week?"

Move quickly—they're re-engaged.
```

### Neutral Response
```
"Things are still pretty busy, but maybe soon."

Response:
"Totally understand—appreciate you letting me know.
I'll check back in [timeframe they suggest or 4-6 weeks].

In the meantime, if anything changes or a question
comes up, just reply here."

Set expectation, stay helpful.
```

### Negative Response
```
"We went with another solution."

Response:
"Thanks for letting me know—appreciate the closure.
How's it working out?

If things change or you ever want a second opinion,
I'm around. Best of luck with [competitor]."

Graceful, leaves door open for future.
```

### No Response
```
After full revival sequence with no response:

- Mark as "revival attempted"
- Set next revival for 6+ months out
- Don't over-contact
- Watch for re-engagement signals

Some prospects need multiple revival attempts
over years before converting.
```

## Metrics

### Revival Performance
```
Track:
- Revival response rate vs initial outreach
- Response rate by dormant period length
- Conversion rate from revival to meeting
- Win rate from resurrected opportunities

Benchmarks:
- Revival response rate: 5-15% (lower than fresh leads)
- But often higher quality (pre-qualified)
```

### Optimization Signals
```
Look for:
- Which revival triggers perform best?
- Which dormant reasons respond best?
- Optimal time between initial and revival?
- Which message frameworks convert?

Use to refine:
- Trigger selection
- Timing rules
- Message templates
- Sequence length
```

## Edge Cases

### Multiple Revivals
```
Second revival attempt:
- At least 6 months after first revival
- New hook required (not same message)
- Consider different channel
- Lower expectations

Third+ revival:
- Annual check-in only
- Trigger-based only
- Don't harass
```

### Company Changes
```
Prospect changed companies:
→ Research new role
→ If relevant, reach out at new company
→ "Saw you moved to [company]. If [problem]
   is relevant there too, happy to reconnect."

New contact at same company:
→ Fresh start with new person
→ May reference previous conversation if helpful
→ "I spoke with [previous contact] last year..."
```

### Objection Changes
```
Original objection no longer valid:

They said: "Too expensive"
Now: You have new pricing tier

Revival: "When we talked, pricing was the sticking
point. We've since introduced a [tier] that might
fit better. Worth a fresh look?"

Address the specific blocker.
```

