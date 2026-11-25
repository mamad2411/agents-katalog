---
name: prospect-fatigue-detection
description: When the user wants to build or improve a sales bot's ability to recognize over-contacted prospects. Also use when the user mentions "prospect fatigue," "over-contact detection," "outreach fatigue," "contact frequency," or "backing off."
---

# Prospect Fatigue Detection

You are an expert in building sales bots that recognize when prospects are being over-contacted. Your goal is to help developers create systems that detect fatigue signals and automatically back off before damaging the relationship.

## Why Fatigue Detection Matters

### The Over-Contact Problem
```
Typical aggressive sequence:
Day 1: Email
Day 2: LinkedIn request
Day 3: Follow-up email
Day 4: SMS
Day 5: Call attempt
Day 7: Another email
Day 10: "Just checking in"

Prospect experience:
→ Annoyed
→ Unsubscribes
→ Marks as spam
→ Tells colleagues to avoid you
→ Relationship burned forever
```

### With Fatigue Detection
```
Smart sequence with fatigue awareness:
Day 1: Email (no open → wait)
Day 4: Follow-up (opened, no reply → gentle nudge)
Day 8: LinkedIn (different channel, lower pressure)
Day 15: Break-up email

Meanwhile:
- Track engagement signals
- Detect declining interest
- Back off automatically
- Preserve future opportunity
```

## Fatigue Signals

### Explicit Signals
```
Direct fatigue indicators:
- "Stop emailing me"
- "Take me off your list"
- "Too many messages"
- "You're being pushy"
- Unsubscribe click
- Spam report
- Block/mute

Action: Immediate stop. Flag for review.
```

### Behavioral Signals
```
Implicit fatigue indicators:

Email:
- Declining open rates (opened first 2, ignoring rest)
- No opens after 3+ emails
- Opens but immediate delete (short dwell time)
- Opens but never clicks/replies

SMS:
- Read receipts but no response (3+)
- Shorter and shorter responses
- Response time getting longer
- Single word replies ("ok", "fine", "sure")

Call:
- Sent to voicemail repeatedly
- Shorter call durations
- "I'm busy" responses
- Canceling scheduled calls
```

### Engagement Decay Patterns
```
Pattern: Decreasing engagement

Touch 1: Opened, clicked, replied "interested"
Touch 2: Opened, no click, no reply
Touch 3: Opened after 2 days, no action
Touch 4: No open
Touch 5: No open

Decay detected. Back off.
```

### Sentiment Signals
```
Language indicating fatigue:

- "I told you I'd reach out when ready"
- "I appreciate the follow-up, but..."
- "I've been busy" (repeated)
- "I'll let you know"
- Increasingly curt responses
- Longer response times
- Missing pleasantries that were previously present
```

## Fatigue Scoring

### Fatigue Score Calculation
```python
def calculate_fatigue_score(prospect):
    score = 0  # 0-100, higher = more fatigued

    # Touch frequency
    touches_7d = count_touches(prospect, days=7)
    if touches_7d > 5:
        score += 30
    elif touches_7d > 3:
        score += 15

    # Engagement decay
    engagement_trend = calculate_engagement_trend(prospect)
    if engagement_trend < -0.5:  # Declining
        score += 25
    elif engagement_trend < -0.2:
        score += 10

    # Non-response streak
    no_response_count = count_consecutive_no_responses(prospect)
    score += min(no_response_count * 10, 30)

    # Explicit signals
    if has_unsubscribe_attempt(prospect):
        score += 50
    if has_negative_sentiment_response(prospect):
        score += 20

    # Response quality decline
    if response_length_declining(prospect):
        score += 10
    if response_time_increasing(prospect):
        score += 10

    return min(score, 100)

def get_fatigue_action(score):
    if score >= 70:
        return "stop_all_outreach"
    elif score >= 50:
        return "pause_and_review"
    elif score >= 30:
        return "reduce_frequency"
    else:
        return "continue_normal"
```

### Fatigue Thresholds by Channel
```
Channel-specific limits:

Email:
- Max 3 emails/week
- Stop after 5 unanswered
- 48h minimum between sends

SMS:
- Max 2 SMS/week
- Stop after 3 unanswered
- 72h minimum between sends

Phone:
- Max 2 attempts/week
- Stop after 3 no-answers
- Leave max 2 voicemails total

LinkedIn:
- Max 1 message/week
- Stop after 2 unanswered
- Don't spam with connection requests
```

## Automatic Back-Off

### Back-Off Rules
```python
BACKOFF_RULES = {
    "fatigue_30_50": {
        "action": "extend_intervals",
        "multiplier": 1.5,  # 50% longer between touches
        "message": "softer_tone"
    },
    "fatigue_50_70": {
        "action": "pause_sequence",
        "duration_days": 14,
        "resume_trigger": "prospect_engagement"
    },
    "fatigue_70_plus": {
        "action": "stop_sequence",
        "move_to": "long_term_nurture",
        "human_review": True
    }
}

def apply_backoff(prospect, fatigue_score):
    if fatigue_score >= 70:
        stop_all_outreach(prospect)
        add_to_nurture_pool(prospect, review_in_days=90)
        alert_human(prospect, "high_fatigue")

    elif fatigue_score >= 50:
        pause_sequence(prospect, days=14)
        set_resume_trigger(prospect, "any_engagement")

    elif fatigue_score >= 30:
        extend_sequence_intervals(prospect, multiplier=1.5)
        switch_to_softer_messaging(prospect)
```

### Graceful Exit Messages
```
When backing off, communicate gracefully:

High fatigue (stopping):
"I don't want to clog your inbox—I'll step back.
If [problem you solve] becomes a priority, I'm
here. Otherwise, wishing you all the best."

Medium fatigue (pausing):
"I can tell the timing isn't right. I'll check
back in a few weeks. In the meantime, feel free
to reach out if anything changes."

Low fatigue (slowing down):
"I know you're busy—I'll space out my follow-ups.
Just didn't want this to fall through the cracks
if it's still relevant."
```

## Cross-Channel Coordination

### Unified Fatigue View
```
Track fatigue across ALL channels:

Prospect: Jane Smith
Email fatigue: 45
SMS fatigue: 20
Phone fatigue: 60
LinkedIn fatigue: 10
Overall fatigue: 52 (weighted average)

Don't:
- Over-email while SMS seems fine
- Call repeatedly when email is ignored
- Pile on across channels

Do:
- Maintain single fatigue score
- Coordinate channel selection
- Back off universally when needed
```

### Channel Switching Strategy
```
When one channel fatigues:

Email fatigue high, others low:
→ Try LinkedIn or SMS
→ But don't just shift the volume
→ One message, different channel, see response

All channels fatigued:
→ Stop all outreach
→ Wait for prospect to re-engage
→ Or trigger-based revival later
```

## Prevention

### Sequence Design Best Practices
```
Design sequences to prevent fatigue:

1. Start slow, escalate if engagement
   - Day 1: Email
   - Day 4: Email (if opened)
   - Day 7: LinkedIn (if engaged)

2. Built-in stopping points
   - After 3 no-responses: pause
   - After explicit disinterest: stop

3. Value-first cadence
   - Not every touch is an "ask"
   - Share content, insights, value
   - Ask for meeting only 30% of touches

4. Respect weekends and off-hours
   - No outreach outside business hours
   - No weekend messages
```

### Personalization Reduces Fatigue
```
Generic outreach fatigues faster:

Fatiguing:
"Just following up on my previous email..."
"Wanted to check in..."
"Circling back..."

Less fatiguing:
"Saw your company just [specific event]—thought
this might be relevant now."
"Given what you mentioned about [specific detail],
here's something that might help."

Personalized = feels like value, not spam.
```

## Recovery

### Reviving Fatigued Prospects
```
After cooling-off period:

Requirements:
- At least 60-90 days of silence
- New hook (trigger event, new feature, etc.)
- Different approach than before

Message:
"It's been a while since we connected. I deliberately
gave you space, but [new relevant thing] made me
think this might be worth a fresh look.

If the answer is still no, I'll respect that.
But if circumstances have changed, I'm here."
```

### Re-Permission Approach
```
Ask before resuming:

"I know I reached out a lot earlier this year.
Before I continue, wanted to check: is it worth
staying in touch, or would you prefer I move on?

Either answer is fine—just want to respect
your preferences."

This can reactivate interested prospects while
honoring those who want out.
```

## Metrics

### Fatigue Metrics to Track
```
Monitor:
- Average fatigue score across pipeline
- Fatigue-triggered pause rate
- Opt-out rate by fatigue score
- Conversion rate by fatigue score

Healthy patterns:
- <20% of prospects in "high fatigue" zone
- Opt-out rate <2% of touched prospects
- Declining fatigue scores over sequence lifespan
```

### Sequence Performance by Fatigue
```
Compare:

Aggressive sequence:
- 12 touches in 21 days
- 5% meeting rate
- 8% opt-out rate
- 40% high-fatigue rate

Measured sequence:
- 6 touches in 21 days
- 4% meeting rate
- 2% opt-out rate
- 15% high-fatigue rate

Less aggressive = similar results + less damage
```

## Edge Cases

### High-Value Prospects
```
For enterprise/strategic prospects:

- Lower fatigue thresholds (more cautious)
- Human review before any outreach
- Quality over quantity
- Personalization required

Burning an enterprise prospect = major loss.
```

### Existing Customers
```
For current customers:

- Even lower tolerance for fatigue
- Coordinate with CS team on contact
- Don't sales-spam existing relationships
- Account-level contact tracking

Customer fatigue = churn risk.
```

### Inbound vs Outbound
```
Adjust expectations:

Inbound (they reached out):
- Higher tolerance for follow-up
- They expect to hear from you
- But still don't overdo it

Outbound (you reached out):
- Lower tolerance
- They didn't ask for this
- Earn the right to continue
```

