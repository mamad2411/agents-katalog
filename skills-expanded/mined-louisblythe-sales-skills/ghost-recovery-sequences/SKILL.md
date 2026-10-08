---
name: ghost-recovery-sequences
description: When the user wants to build or improve a sales bot's ability to recover prospects who stopped responding mid-conversation. Also use when the user mentions "ghost recovery," "unresponsive prospects," "conversation dropoff," "re-engagement sequences," or "dead conversation revival."
---

# Ghost Recovery Sequences

You are an expert in building sales bots that recover prospects who stopped responding mid-conversation. Your goal is to help developers create systems with specific flows for re-engaging ghosted conversations.

## Why Ghost Recovery Matters

### The Ghost Problem
```
Active conversation:
Day 1: Prospect engaged, asks questions
Day 2: Great call scheduled
Day 3: No response to confirmation
Day 4-14: Silence

Without recovery:
→ Lead goes cold
→ Opportunity lost
→ Competitor may win

With recovery:
→ Thoughtful re-engagement
→ 10-20% revival rate
→ Deals saved
```

### Ghost vs Dead
```
Ghost (recoverable):
- Was engaged, went silent
- No explicit "no"
- Life/work got busy
- Timing shifted
- Still might buy

Dead (not recoverable):
- Explicitly said no
- Went with competitor
- Company went away
- Contact left company
- Opted out

Different treatment needed.
```

## Ghost Detection

### Identifying Ghosts
```python
def detect_ghost(prospect, conversation):
    # Must have had engagement
    if conversation.message_count < 2:
        return False  # Never really engaged

    # Must have recent activity
    if conversation.last_prospect_message:
        days_silent = (now() - conversation.last_prospect_message).days

        # Was in active stage
        if conversation.stage in ["discovery", "demo_scheduled", "proposal"]:
            if days_silent >= 3:
                return True

        # Was in earlier stage
        if conversation.stage in ["awareness", "interest"]:
            if days_silent >= 7:
                return True

    return False

def get_ghost_severity(days_silent, stage):
    if stage in ["demo_scheduled", "proposal"]:
        # More serious - were close to decision
        if days_silent < 5:
            return "mild"
        elif days_silent < 10:
            return "moderate"
        else:
            return "severe"
    else:
        # Earlier stage, expected to be slower
        if days_silent < 10:
            return "mild"
        elif days_silent < 21:
            return "moderate"
        else:
            return "severe"
```

### Ghost Signals
```
Signs prospect is ghosting:
- Read receipts but no reply
- Opened email, no response
- Missed scheduled call
- "I'll get back to you" then silence
- Shorter and shorter responses before silence
- LinkedIn views but no reply

Signs NOT ghosting:
- Out of office auto-reply
- Told you they'd be busy
- Holiday period
- Known company event
```

## Recovery Sequences

### Mild Ghost (3-7 days)
```
Day 3-5: Soft check-in

"Hey [Name], wanted to make sure my last message
didn't get lost in the shuffle. [Brief value add].
Let me know if you have any questions."

Day 7: Value-first nudge

"Thought you might find this useful: [relevant
content/insight]. Happy to chat when you have time."

Short, helpful, no pressure.
```

### Moderate Ghost (7-14 days)
```
Day 7-10: Direct acknowledgment

"Hi [Name], it's been a few days since we connected.
I know things get busy—wanted to check if [your
original topic] is still on your radar, or if
priorities have shifted."

Day 12-14: Pattern break

"[Name], I'll keep this short: Are you still
interested in [solving X], or should I close
this out for now? Either way is fine—just want
to respect your time."

More direct, gives them an out.
```

### Severe Ghost (14+ days)
```
Day 14-21: Break-up attempt

"Hi [Name], I haven't heard back and want to
be respectful of your inbox. I'm going to assume
the timing isn't right and close this out.

If things change, I'm always here. Best of luck
with [their challenge]."

Day 30+: Long-term revival (see conversation-resurrection)

Different context, different approach.
```

## Stage-Specific Recovery

### Post-Demo Ghost
```
Demo happened, then silence:

Day 2:
"Thanks again for your time on [demo day].
Any questions that came up after our conversation?"

Day 5:
"Checking in—was there anything from the demo
that didn't quite hit the mark? Happy to address
any concerns."

Day 10:
"I know you're evaluating options. Is there
anything I can provide to help with your decision?
Or if you've decided to go another direction,
I'd appreciate knowing so I can update my notes."

Focus on addressing unstated concerns.
```

### Post-Proposal Ghost
```
Proposal sent, then silence:

Day 3:
"Wanted to make sure you received the proposal.
Any questions on pricing or terms?"

Day 7:
"Hi [Name], following up on the proposal from
[date]. If anything needs adjustment to fit your
requirements, I'm happy to discuss."

Day 14:
"I sense the timing may not be right. If budget
or scope needs to change, I'm flexible. If you've
moved in a different direction, I understand—just
let me know so I can update my records."

Focus on removing deal blockers.
```

### Pre-Meeting Ghost
```
Meeting scheduled but not confirmed:

Day before:
"Looking forward to tomorrow at [time]. Does
that still work for you?"

Day of (2 hours before):
"Just confirming our call at [time] today.
If something's come up, we can reschedule."

After no-show:
"Looks like we missed each other. No worries—
let me know when you're free to reconnect."

Don't guilt them. Make it easy to reschedule.
```

## Message Frameworks

### The Pattern Break
```
Standard messages get ignored. Break the pattern:

"[Name], this might sound crazy, but I'm cleaning
out my pipeline and need to know: thumbs up or
thumbs down on [your solution]?"

"Quick poll: Should I (A) follow up next month,
(B) send more info, or (C) leave you alone forever?"

Pattern breaks get attention.
```

### The Honest Approach
```
Transparent about the situation:

"I've sent a few messages without hearing back.
I don't want to be annoying, but I also don't
want to give up if you're just busy. Quick
question: is this worth continuing?"

Honesty can prompt response.
```

### The Value Hook
```
Lead with something useful:

"Saw this article about [their industry challenge]
and thought of our conversation. [Link]

If [your solution] is still relevant, happy to
reconnect. If not, at least hopefully this helps."

Give before asking.
```

### The Third-Party Approach
```
Mention others in similar situation:

"I was just helping [similar company] with
[same challenge]. They found [insight].

Made me think of your situation—worth a
quick call to see if it applies?"

Social proof + relevance.
```

## Channel Strategy

### Multi-Channel Recovery
```
If email ghosts:
- Try LinkedIn message
- Try SMS (if opted in)
- Try different email (different angle)

Don't just repeat—vary the approach:

Email: Formal, detailed
LinkedIn: Personal, conversational
SMS: Brief, direct
```

### Channel Sequence
```
Day 3: Email (soft check-in)
Day 7: LinkedIn (different angle)
Day 10: Email (break-up attempt)
Day 14: SMS (if permitted, very brief)
Day 21: Final email (close out)

Don't bombard—spread across channels thoughtfully.
```

## Recovery Triggers

### Engagement-Based Triggers
```
Restart recovery when:
- Ghost opens your email
- Ghost visits your website
- Ghost views your LinkedIn
- Ghost engages on social

Response:
"Noticed you were checking out [content]. Any
questions I can answer while it's fresh?"

Strike when they're re-engaging.
```

### External Triggers
```
Restart recovery when:
- Company raises funding
- New executive hired
- Company in news
- Competitor mentioned
- Their pain point in news

"Saw the news about [trigger]. Given what you
mentioned about [challenge], thought it might
be worth reconnecting."

New context = new conversation.
```

## Ghost Prevention

### Reduce Ghosting in First Place
```
Before they ghost:
- Set clear next steps
- Confirm commitment verbally
- Send calendar invites
- Establish communication expectations

"Before we hang up, let's lock in a time for
our next call. What works?"

Specific commitments reduce ghosting.
```

### Early Warning Detection
```
Signs someone might ghost:
- Response times increasing
- Responses getting shorter
- Enthusiasm decreasing
- Missed one small commitment

Intervene early:
"I notice you're super busy—should we slow
things down or find a better time?"
```

## Metrics

### Ghost Recovery Metrics
```
Track:
- Ghost identification rate
- Recovery sequence start rate
- Response rate per recovery stage
- Ultimate conversion of recovered ghosts
- Channel effectiveness for recovery

Benchmark:
- 10-20% recovery rate is good
- >30% means sequences are working well
```

### Ghost Analysis
```
Understand why ghosts happen:
- At what stage do most ghost?
- What precedes ghosting?
- Which personas ghost most?
- Which products/prices correlate?

Use to prevent, not just recover.
```

## Implementation

### Ghost Recovery State
```json
{
  "prospect_id": "12345",
  "ghost_status": {
    "is_ghost": true,
    "severity": "moderate",
    "days_silent": 10,
    "last_stage": "demo_completed",
    "recovery_sequence": "post_demo_recovery",
    "recovery_step": 2,
    "recovery_touches": 2,
    "last_recovery_attempt": "2024-01-18",
    "engagement_since_ghost": []
  }
}
```

### Recovery Flow
```python
def process_ghost(prospect):
    ghost_status = detect_ghost_status(prospect)

    if not ghost_status.is_ghost:
        return None

    # Check for recent engagement
    if has_recent_engagement(prospect):
        return create_engagement_response(prospect)

    # Check if recovery in progress
    if ghost_status.recovery_sequence:
        next_step = get_next_recovery_step(ghost_status)
        if next_step.is_due:
            return execute_recovery_step(prospect, next_step)

    # Start new recovery
    else:
        sequence = select_recovery_sequence(ghost_status)
        return start_recovery(prospect, sequence)
```

