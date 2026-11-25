---
name: drip-pacing-intelligence
description: When the user wants to build or improve a sales bot's ability to adjust sequence timing based on engagement signals. Also use when the user mentions "drip pacing," "sequence timing," "adaptive sequences," "engagement-based timing," or "smart cadence."
---

# Drip Pacing Intelligence

You are an expert in building intelligent sequence timing for sales automation. Your goal is to help developers create systems that dynamically adjust outreach pacing based on prospect engagement.

## Why Pacing Matters

### Static Pacing Problems
```
Fixed schedule:
Day 1 → Day 3 → Day 7 → Day 14

What happens:
- Hot prospect: Cooled off waiting 7 days
- Cold prospect: Annoyed by Day 3 message
- Busy prospect: Missed all messages during travel

Result: Lower response rates, higher opt-outs
```

### Intelligent Pacing Benefits
```
Dynamic adjustment:
- Engaged? → Accelerate
- Quiet? → Decelerate
- Signals? → Respond immediately

Result: Right message, right time, right frequency
```

## Engagement Signals

### Positive Signals (Accelerate)
```
High intent:
- Email opened (multiple times)
- Links clicked
- Attachment downloaded
- Website visited
- Content engaged with
- Partial form filled

Action: Shorten intervals, add touches
```

### Neutral Signals (Maintain)
```
Normal behavior:
- Email opened once
- No response yet
- Profile viewed (LinkedIn)
- Website bounce

Action: Stay on current pace
```

### Negative Signals (Decelerate)
```
Low engagement:
- No opens
- Unsubscribes from marketing
- Marked as spam
- Auto-reply received

Action: Lengthen intervals, reduce touches
```

## Pacing Algorithms

### Engagement Score-Based Pacing
```
Calculate engagement score (0-100):
+10: Email opened
+20: Link clicked
+30: Website visit
+40: Content downloaded
+50: Reply received
-10: Email ignored (after 48h)
-20: Unsubscribe
-50: Spam complaint

Pacing rules:
Score > 70: Next touch in 24h
Score 40-70: Next touch in 48-72h
Score 20-40: Next touch in 5-7 days
Score < 20: Pause sequence, try different approach
```

### Adaptive Interval Calculation
```python
def calculate_next_touch(prospect):
    base_interval = prospect.sequence.default_interval
    engagement = calculate_engagement_score(prospect)
    last_activity = prospect.last_engagement_at

    # Engagement multiplier
    if engagement > 70:
        multiplier = 0.5  # Half the time
    elif engagement > 40:
        multiplier = 1.0  # Normal pace
    elif engagement > 20:
        multiplier = 1.5  # Slow down
    else:
        multiplier = 2.5  # Significantly slow

    # Recency adjustment
    hours_since_activity = hours_since(last_activity)
    if hours_since_activity < 4:
        # Very recent activity—strike while hot
        return timedelta(hours=2)

    interval = base_interval * multiplier
    return interval
```

### Event-Triggered Acceleration
```
Immediate response triggers:
- Website pricing page visit → Trigger within 1 hour
- Demo video watched >50% → Follow up same day
- Competitor comparison viewed → Priority outreach
- Multiple page views in session → Real-time engagement

"I noticed you were just checking out our pricing—
any questions I can answer?"
```

## Sequence Adjustment Patterns

### The Acceleration Pattern
```
Standard sequence:
Day 1 → Day 4 → Day 8 → Day 14

Engagement detected (Day 2 email opened, link clicked):
Day 1 → [Engagement] → Day 2 (accelerated) → Day 4 → Day 8

New sequence:
Day 1 → Day 2 → Day 5 → Day 10

Message adjustment:
"I saw you checked out [content]. Wanted to follow up
while it's fresh—did that answer your questions?"
```

### The Deceleration Pattern
```
Standard sequence:
Day 1 → Day 4 → Day 8 → Day 14

No engagement detected:
Day 1 → Day 4 (no open) → Day 10 (extended) → Day 20

Message adjustment:
"I've reached out a couple times—I know inboxes get
crowded. If the timing isn't right, no worries. But
if [problem you solve] is on your radar, I'd love to
help when you're ready."
```

### The Surge Pattern
```
High engagement burst detected:
- 3 emails opened in 1 hour
- Website visit
- LinkedIn profile view

Trigger immediate outreach:
"Hey [Name], looks like you're doing some research—
perfect timing. Would a quick call be helpful, or
do you prefer I send some info?"
```

## Multi-Channel Pacing

### Channel Coordination
```
Don't pile on. Coordinate across channels:

Day 1: Email
Day 3: Email (if opened Day 1)
Day 3: LinkedIn (if no open on Day 1)
Day 6: SMS (if engagement on either)
Day 8: Call (if high engagement)

Never:
- Email + SMS + Call same day
- Multiple touches in same channel < 48h apart
```

### Channel-Specific Pacing
```
Email:
- Minimum 48h between sends
- Max 3 emails per week
- Extend if no opens

SMS:
- Minimum 3 days between sends
- Max 2 per week
- Stop if no response after 2

Phone:
- Minimum 5 days between attempts
- Max 3 per sequence
- Voicemail counts as attempt
```

## Handling Time Zones

### Optimal Send Time
```
Adjust for recipient timezone:
- Morning: 8-10am local
- Afternoon: 2-4pm local
- Never: Outside 8am-8pm local

If timezone unknown:
- Infer from area code
- Infer from email domain
- Default to safe window
```

### Weekend/Holiday Pacing
```
Pause logic:
- No outreach Saturday-Sunday
- Check for holidays
- Resume Monday morning

Adjustment:
If Day 4 falls on Saturday:
→ Move to Monday (Day 6)
→ Adjust subsequent touches proportionally
```

## Sequence Modifications

### Dynamic Sequence Selection
```
Based on engagement, switch sequences:

Low engagement (Score < 30):
→ Switch to "Break-up" sequence
→ Fewer touches, more spaced out
→ Different messaging approach

High engagement (Score > 70):
→ Switch to "Fast-track" sequence
→ More frequent touches
→ More direct CTAs
→ Add phone touches
```

### Touch Type Modification
```
Based on engagement patterns:

Opens but no clicks:
→ Make next email shorter
→ Stronger CTA
→ Single focus

Clicks but no response:
→ Add different channel
→ Address potential objection
→ Offer easier next step
```

## Implementation

### State Management
```json
{
  "prospect_id": "12345",
  "sequence_id": "enterprise_outbound",
  "current_step": 3,
  "engagement_score": 65,
  "pacing_status": "accelerated",
  "next_touch_at": "2024-01-16T10:00:00Z",
  "last_engagement": {
    "type": "email_click",
    "timestamp": "2024-01-15T14:30:00Z",
    "content": "pricing_link"
  },
  "pacing_history": [
    {"step": 1, "interval_days": 0, "actual_days": 0},
    {"step": 2, "interval_days": 3, "actual_days": 2},
    {"step": 3, "interval_days": 3, "actual_days": 2}
  ]
}
```

### Pacing Rules Engine
```python
rules = [
    {
        "condition": "email_opened_count >= 3 AND hours_since_last_open < 24",
        "action": "accelerate",
        "modifier": 0.5
    },
    {
        "condition": "no_opens AND step >= 3",
        "action": "decelerate",
        "modifier": 2.0
    },
    {
        "condition": "website_visit AND page == 'pricing'",
        "action": "immediate_touch",
        "delay_hours": 2
    },
    {
        "condition": "out_of_office_detected",
        "action": "pause",
        "resume_date": "ooo_return_date + 1"
    }
]
```

## Metrics & Optimization

### Pacing Effectiveness
```
Measure:
- Response rate by pacing tier
- Opt-out rate by pacing tier
- Time to conversion by pacing
- Engagement score trends

Compare:
- Static vs dynamic pacing
- Different pacing algorithms
- A/B test interval changes
```

### Continuous Learning
```
Track outcomes:
- Which adjustments led to responses?
- What pacing converts best?
- When do prospects disengage?

Feed back:
- Update pacing rules
- Refine engagement scoring
- Improve timing predictions
```
