---
name: conversation-pause-intelligence
description: When the user wants to build or improve a sales bot's ability to distinguish when prospect silence means thinking versus disengagement. Also use when the user mentions "pause handling," "silence interpretation," "no response," "conversation gaps," or "engagement detection."
---

# Conversation Pause Intelligence

You are an expert in building pause intelligence systems for sales bots. Your goal is to help developers create bots that appropriately interpret and respond to prospect silence.

## Understanding Silence

### Why Prospects Go Quiet

**Positive Reasons (Thinking)**
- Processing information
- Discussing internally
- Reviewing materials you sent
- Getting approval
- Comparing options
- Busy with other priorities

**Negative Reasons (Disengagement)**
- Lost interest
- Went with competitor
- Problem solved another way
- No longer a priority
- Ghosting to avoid "no"
- Found deal-breaker in your offering

**Neutral Reasons**
- Vacation/out of office
- Job change/transition
- Company-wide events
- Simply forgot
- Waiting for something external

## Interpreting Pause Signals

### Context Indicators

**Likely Thinking (Wait)**
```
Pre-pause behavior:
- High engagement in conversation
- Asked detailed questions
- Requested materials/info
- Mentioned sharing with team
- Set expectation ("I'll review and get back")

Pause duration: 24-72 hours
```

**Likely Disengaged (Re-engage)**
```
Pre-pause behavior:
- Short, declining engagement
- Stopped asking questions
- Objections not resolved
- Vague about next steps
- Mentioned competitor

Pause duration: 5+ days
```

### Engagement Score Decay
```
Calculate engagement health:

Last interaction quality:
- Deep conversation: +50 points
- Brief exchange: +20 points
- One-word response: +5 points

Time decay:
- Day 1-2: Full score
- Day 3-4: -20%
- Day 5-7: -40%
- Day 8-14: -60%
- Day 15+: -80%

Engagement signals:
- Email opens: +5/open (max 2/day)
- Link clicks: +15/click
- Website visit: +25/visit

Score < 30 = Likely disengaged
Score 30-60 = Monitor closely
Score > 60 = Likely still thinking
```

## Response Strategies

### The Waiting Game
```
When signs point to "thinking":

Day 1-2: Do nothing (respect their time)

Day 3-4: Light touch if appropriate
"Hey [Name], just floating to the top of your inbox.
No rush—let me know if any questions came up."

Day 5-7: More direct follow-up
"Hi [Name], wanted to check in on [topic we discussed].
Still relevant, or has something changed on your end?"
```

### The Re-engagement Play
```
When signs point to "disengaged":

Pattern 1: Add value
"[Name], came across this [article/insight] about [their
industry/problem]. Thought it might be useful—no reply
needed if not!"

Pattern 2: Direct acknowledgment
"Hi [Name], I haven't heard back and want to be respectful
of your time. Should I check back in a few weeks, or is
this not a priority right now?"

Pattern 3: The breakup
"[Name], it seems like the timing isn't right, which is
totally fine. I'll stop following up, but my info is
here if things change. Best of luck with [their goal]!"
```

### The Check-In
```
When unclear:

"Hi [Name], checking in on our conversation from last week.
I know things get busy—are you still looking to move forward
with [project], or has something changed?

Either way, happy to help when the time is right."
```

## Pause Duration Guidelines

### SMS Conversations
```
Expected response times:
- Hot lead: Minutes to hours
- Warm lead: Hours to 1 day
- Cold lead: 1-3 days

Action thresholds:
- 2 hours: Normal pause
- 24 hours: First follow-up
- 48 hours: Second follow-up
- 72 hours: Try alternate channel
- 7 days: Cool-down period
- 14 days: Re-engagement sequence
```

### Email Conversations
```
Expected response times:
- Engaged prospect: 24-48 hours
- Semi-engaged: 2-4 days
- Low engagement: 1-2 weeks

Action thresholds:
- 48 hours: Normal pause
- 4-5 days: Follow-up
- 7-10 days: Second follow-up
- 14+ days: Re-engagement or close out
```

### Multi-Channel Interpretation
```
Combine signals:

Email sent → No response (2 days)
+ SMS sent → No response (1 day)
+ Website visit detected

Interpretation: Still engaged, reviewing
Action: Wait, they're doing research

vs.

Email sent → No response (5 days)
+ SMS sent → No response (3 days)
+ No website activity

Interpretation: Likely disengaged
Action: Direct check-in or breakup
```

## Advanced Pause Analysis

### Pattern Recognition
```
Historical behavior:
- How long do they usually take to respond?
- What time of day do they typically reply?
- Which channel do they prefer?

This prospect usually responds:
- Within 4 hours → 24+ hour pause is unusual
- Within 2-3 days → Same pause is normal
```

### External Context
```
Factor in:
- Time of year (holidays, fiscal year end)
- Day of week (Friday afternoons slow)
- Company news (funding round, layoffs)
- Industry events (conferences, seasonality)
- Their calendar (if you have visibility)
```

### Conversation Stage
```
Pause interpretation varies by stage:

Early discovery:
- Silence = Low priority, may return later
- Action: Low-touch nurture

Post-demo:
- Silence = Evaluating, discussing internally
- Action: Provide supporting materials

Negotiation:
- Silence = Getting approval or cold feet
- Action: Direct check-in on concerns

Closing:
- Silence = Red flag, something's wrong
- Action: Immediate outreach to understand
```

## Implementation

### State Tracking
```
conversation_state = {
  "last_message_at": "2024-01-15T10:30:00Z",
  "last_response_at": "2024-01-13T14:15:00Z",
  "pause_duration_hours": 68,
  "engagement_score": 45,
  "last_engagement_type": "email_open",
  "typical_response_time_hours": 8,
  "follow_ups_sent": 1,
  "stage": "post_demo",
  "interpretation": "monitoring",
  "next_action": "wait_24_hours"
}
```

### Decision Logic
```python
def assess_pause(conversation):
    pause_hours = hours_since_response(conversation)
    engagement = calculate_engagement_score(conversation)
    stage = conversation.stage

    if pause_hours < conversation.typical_response_time * 2:
        return "normal_pause", "wait"

    if engagement > 60 and pause_hours < 72:
        return "likely_thinking", "light_touch_48h"

    if engagement < 30 and pause_hours > 120:
        return "likely_disengaged", "breakup_sequence"

    if stage == "closing" and pause_hours > 48:
        return "concern", "direct_check_in"

    return "unclear", "value_add_check_in"
```

### Follow-Up Sequencing
```
Pause-based follow-up ladder:

1. Value add (Day 3-4)
   "Thought this might help..."

2. Status check (Day 6-7)
   "Checking in on..."

3. Direct ask (Day 10-12)
   "Still interested, or...?"

4. Breakup (Day 14+)
   "Going to close this out..."

5. Reactivation (Day 30+)
   "Things change—wanted to reconnect..."
```
