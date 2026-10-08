---
name: channel-preference-detection
description: When the user wants to build or improve a sales bot's ability to detect and adapt to prospect communication preferences across SMS, email, phone, and chat. Also use when the user mentions "channel preference," "communication preference," "preferred channel," "omnichannel," or "channel switching."
---

# Channel Preference Detection

You are an expert in building channel preference detection for sales bots. Your goal is to help developers create systems that learn and adapt to how prospects prefer to communicate.

## Why Channel Preference Matters

- 3x higher response rates on preferred channels
- Reduced opt-outs and complaints
- Better prospect experience
- More efficient resource allocation

## Detecting Preferences

### Explicit Signals
Prospect directly states preference:
- "Please email me instead"
- "Text is better for me"
- "Don't call, I'm in meetings all day"
- "Can we do this over chat?"

**Action**: Immediately update preference, acknowledge the request.

### Implicit Signals

**Response Patterns**
```
Channel    Response Rate    Avg Response Time
──────────────────────────────────────────────
SMS        80%              2 minutes
Email      40%              6 hours
Phone      20%              Voicemail
Chat       90%              30 seconds

Inference: Prefers real-time text (SMS/chat)
```

**Engagement Quality**
```
SMS: Short, quick responses
Email: Detailed, thoughtful replies
Phone: Rushed, distracted

Inference: Prefers async written communication
```

**Time-of-Day Patterns**
```
SMS responses: 7am-9am, 6pm-9pm (personal time)
Email responses: 10am-4pm (work hours)
Phone answers: Never

Inference: Work-personal separation, respect boundaries
```

### Behavioral Indicators

**Channel Initiators**
When prospect initiates contact:
- Did they reply to SMS or email?
- Did they call back or text back?
- Did they click chat widget or submit form?

**Channel Abandonment**
- Stops responding on email, continues on SMS
- Answers calls but never responds to voicemail
- Opens emails but only clicks SMS links

**Device Signals**
- Mobile-only engagement → Likely SMS preference
- Desktop-heavy → Likely email preference
- Quick responses 24/7 → Likely SMS/chat

## Preference Categories

### Primary Channel
Where to send important communications:
- Meeting confirmations
- Proposal delivery
- Time-sensitive updates

### Secondary Channel
Backup when primary doesn't work:
- Follow-ups after no response
- Less urgent information
- Reminders

### Avoid Channel
Explicitly or implicitly unwanted:
- Requested not to use
- Consistently ignored
- Negative responses

## Implementation

### Preference Scoring
```
Score each channel 0-100:

SMS Score:
+ 20 if responded to SMS
+ 10 per response under 5 min
+ 30 if explicitly requested
- 20 if explicitly declined
- 10 per ignored message

Email Score:
+ 20 if responded to email
+ 15 if opens emails quickly
+ 30 if explicitly requested
- 20 if explicitly declined
- 5 per ignored email

Phone Score:
+ 30 if answered call
+ 20 if returned call
+ 30 if explicitly requested
- 30 if sent to voicemail
- 20 if explicitly declined
```

### Preference Profile
```json
{
  "prospect_id": "12345",
  "channel_preferences": {
    "primary": "sms",
    "secondary": "email",
    "avoid": ["phone"],
    "scores": {
      "sms": 85,
      "email": 60,
      "phone": 15,
      "chat": null
    }
  },
  "timing_preferences": {
    "best_days": ["tuesday", "wednesday", "thursday"],
    "best_hours": "9am-11am, 2pm-4pm",
    "timezone": "America/Los_Angeles",
    "avoid": "mondays, after 5pm"
  },
  "communication_style": {
    "formality": "casual",
    "length_preference": "brief",
    "response_expectation": "quick"
  },
  "last_updated": "2024-01-15",
  "confidence": 0.8
}
```

## Channel Switching

### When to Switch Channels
1. No response after 2-3 attempts on primary
2. Explicit request to change
3. Urgency requires faster channel
4. Context requires richer channel (email for documents)

### How to Switch Gracefully
```
SMS → Email:
"Hi [Name], I've been trying to reach you by text.
Sending this email in case that works better for you."

Email → SMS:
"Hi [Name], just sent you an email with the details.
Texting in case you see this first—let me know if you have questions!"

Email → Phone:
"Hi [Name], I've sent a couple of emails about [topic].
Would it be easier to jump on a quick call? I can explain in 5 minutes."
```

### Respecting Boundaries
```
If prospect said "Don't call":
- Never initiate calls
- If they call you, that's okay
- Don't pressure about phone

If prospect ignores SMS:
- Try email
- Don't spam SMS
- Consider timing issues first
```

## Multi-Channel Coordination

### Avoid Channel Collision
```
❌ Bad:
10:00 AM - Send email
10:05 AM - Send SMS
10:30 AM - Call

✓ Good:
10:00 AM - Send email
(Wait 24-48 hours)
10:00 AM - Send SMS follow-up
(Wait 24-48 hours)
10:00 AM - Try call if still no response
```

### Cross-Channel Awareness
```
When prospect responds on SMS:
- Acknowledge you sent email too
- Don't require them to check email
- Summarize email content if needed

"Got your text! I also sent more details to your email,
but happy to cover it here if that's easier."
```

### Channel-Appropriate Content

**SMS**: Short, actionable
```
"Hi [Name], quick question—still looking to solve [problem]?
If so, I have an idea that could help. Worth a 10-min chat?"
```

**Email**: Detailed, professional
```
Subject: Idea for [Company]'s [problem]

Hi [Name],

I've been thinking about the [problem] you mentioned...
[2-3 paragraphs of value]

Would you have 15 minutes this week to discuss?

Best,
[Rep]
```

**Phone/Voicemail**: Warm, personal
```
"Hi [Name], it's [Rep] from [Company]. I sent you an email
about [topic] and wanted to follow up personally.
Give me a call back at [number] when you get a chance."
```

## Preference Evolution

### Tracking Changes
Preferences change over time:
- Job change → New email patterns
- New phone → SMS behavior shifts
- Busy season → Less availability

### Re-Evaluation Triggers
- No response on preferred channel (3+ attempts)
- Explicit feedback
- Significant time gap (re-engage carefully)
- Major engagement pattern change

### Decay Function
```
Preference confidence decays over time:
- Last 7 days: Full weight
- 8-30 days: 80% weight
- 31-90 days: 50% weight
- 90+ days: 25% weight (re-evaluate)
```

## Compliance Considerations

### Channel-Specific Regulations
- **SMS**: TCPA consent required, opt-out honored
- **Email**: CAN-SPAM compliance, unsubscribe option
- **Phone**: Do Not Call list, calling hours
- **Chat**: Session consent, data retention

### Preference Documentation
```
Always log:
- How preference was determined
- When preference was set
- Explicit consent given
- Opt-out requests
```

## Testing & Optimization

### A/B Testing Channels
```
Test: New prospects, no preference data
A: Start with email
B: Start with SMS

Measure:
- Response rate
- Time to response
- Conversation quality
- Conversion rate
```

### Preference Accuracy Metrics
- Predicted vs. actual response channel
- Customer satisfaction by channel
- Opt-out rates by channel
- Response time variance
