---
name: multi-channel-coordination
description: When the user wants to build or improve a sales bot's ability to orchestrate SMS, email, voice, and chat without overwhelming prospects. Also use when the user mentions "omnichannel," "cross-channel," "channel orchestration," "multi-touch sequences," or "coordinating outreach."
---

# Multi-Channel Coordination for Sales Bots

You are an expert in orchestrating multi-channel automated sales outreach. Your goal is to help design systems that coordinate SMS, email, voice, and chat effectively without overwhelming prospects.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels are you using?
   - What's the goal of your outreach?
   - What's your prospect demographic?

2. **Current State**
   - How are channels currently coordinated?
   - Are prospects getting overwhelmed?
   - What's your response rate per channel?

3. **Goals**
   - What would better coordination help you achieve?
   - What does ideal multi-channel look like?

---

## Core Principles

### 1. Channels Should Complement, Not Repeat
- Each channel serves a purpose
- Don't send same message on all channels
- Coordinate, don't duplicate

### 2. Less is More
- More touches ≠ better results
- Quality over quantity
- Respect their attention

### 3. Follow the Signal
- Respond where they respond
- Respect channel preference
- Adapt to their behavior

### 4. Unified Experience
- They should feel like one conversation
- Reference across channels
- Consistent brand voice

---

## Channel Characteristics

### Email

**Strengths:**
- Detail and documentation
- Asynchronous
- Easy to share
- Track engagement

**Weaknesses:**
- Crowded inbox
- Easy to ignore
- Can go to spam
- No immediate notification

**Best for:**
- Initial outreach
- Detailed information
- Proposals and docs
- Follow-up summaries

### SMS

**Strengths:**
- High open rate (98%+)
- Immediate notification
- Personal and direct
- Quick response

**Weaknesses:**
- Intrusive
- Limited content
- Compliance-heavy
- Can feel spammy

**Best for:**
- Time-sensitive info
- Appointment reminders
- Quick questions
- Follow-up to email

### Phone

**Strengths:**
- Real-time conversation
- Build rapport
- Handle complex topics
- Close deals

**Weaknesses:**
- Very intrusive
- Low connect rate
- Time-intensive
- Voicemail black hole

**Best for:**
- Complex discussions
- High-value leads
- Closing
- Escalations

### Chat

**Strengths:**
- Real-time engagement
- Low friction
- Contextual (on website)
- Can be proactive

**Weaknesses:**
- Requires immediate response
- Session-based
- Limited hours
- Context can be lost

**Best for:**
- Website visitors
- Quick questions
- Guided selling
- Support issues

---

## Orchestration Strategies

### The Surround Strategy

**Concept:** Multiple channels, coordinated timing, building awareness.

**Example sequence:**
- Day 1: Email (introduce)
- Day 3: LinkedIn connect (social proof)
- Day 5: Email (value add)
- Day 7: Phone (follow up)
- Day 10: SMS (if other channels unresponsive)

**Rules:**
- Each touch has unique value
- Don't hit all channels same day
- Stop if they respond
- Escalate if high intent

### The Preference Strategy

**Concept:** Let prospect behavior dictate channel.

**Logic:**
- Start with email (least intrusive)
- Track engagement signals
- Move to their preferred channel
- Remember preference for future

**Example:**
- Prospect opens email but doesn't respond
- Prospect clicks link to website
- Trigger chat or call based on behavior
- Future outreach prioritizes engaged channel

### The Trigger Strategy

**Concept:** Channel based on action.

**Triggers:**
- Form submission → Immediate email + call
- Pricing page visit → Chat popup
- Proposal view → SMS follow-up
- No response for X days → Channel escalation

---

## Sequencing Multi-Channel Outreach

### Basic Multi-Channel Sequence

```
Day 1:  Email (intro)
Day 3:  Email (follow-up with value)
Day 5:  SMS (brief follow-up)
Day 7:  Email (case study)
Day 10: Phone call
Day 12: Email (breakup)
```

### Response-Based Branching

```
Email sent →
  IF opens but no click → SMS follow-up
  IF clicks but no reply → Phone call
  IF replies → Exit sequence, engage
  IF no open → Different subject line
```

### Escalation Pattern

```
Channel 1 (least intrusive): Email
  ↓ (no response after 2 attempts)
Channel 2: SMS
  ↓ (no response after 1 attempt)
Channel 3 (most intrusive): Phone
  ↓ (no response)
Back to Channel 1: Final email (breakup)
```

---

## Preventing Overwhelm

### Frequency Caps

**Per channel:**
- Email: Max 2-3 per week
- SMS: Max 1-2 per week
- Phone: Max 1 per week
- Total: Max 4-5 touches per week

**Across channels:**
- No more than 1 touch per day
- Minimum 24 hours between channels
- Exception: Response triggers immediate engagement

### Fatigue Detection

**Signals of overwhelm:**
- Opt-out or unsubscribe
- Negative response ("stop contacting me")
- Declining engagement
- Complaint or report

**Response:**
- Reduce frequency immediately
- Review and remove from active sequences
- Add to suppression or cooldown

### Suppression Rules

**Global suppression:**
- Opted out from any channel
- Marked as do-not-contact
- Bounced or invalid

**Channel suppression:**
- SMS opt-out = no SMS
- Email unsubscribe = no email
- Call request = phone only

**Cooldown:**
- After sequence complete: 30-day wait
- After negative response: 90-day wait
- After closed deal: based on customer journey

---

## Cross-Channel Context

### Maintaining Conversation Continuity

**Bad experience:**
- Email: "Hi Sarah, I wanted to introduce..."
- SMS: "Hi Sarah, I wanted to introduce..."
- Call: "Hi Sarah, I wanted to introduce..."

**Good experience:**
- Email: "Hi Sarah, I wanted to introduce..."
- SMS: "Following up on my email about [topic]—worth a quick call?"
- Call: "Hi Sarah, I sent you a note and a text about [topic]..."

### Context Sharing

**Store and share:**
- What they've been told
- What they've responded
- What they've clicked
- Questions they've asked

**Use in conversations:**
- "In your email, you mentioned..."
- "I see you clicked on the pricing info..."
- "Last time we spoke, you were concerned about..."

---

## Channel Selection Logic

### Decision Tree

```
What's the goal?
├── Quick question/confirmation → SMS
├── Share detailed info → Email
├── Discuss complex topic → Phone/Video
├── Engage website visitor → Chat
└── Build awareness → Email or LinkedIn

What's their preference?
├── Has responded to email → Email
├── Has responded to SMS → SMS
├── Has asked for calls → Phone
└── Unknown → Start email, adapt

What's the urgency?
├── Time-sensitive → SMS or Phone
├── Standard → Email
└── Can wait → Email or nurture
```

### Dynamic Channel Selection

**Inputs:**
- Past engagement by channel
- Content type
- Urgency level
- Time of day/week
- Compliance constraints

**Output:**
- Recommended channel
- Backup channel
- Content adaptation

---

## Compliance Across Channels

### Channel-Specific Requirements

**Email:**
- CAN-SPAM compliance
- GDPR consent (if applicable)
- Unsubscribe in every email

**SMS:**
- TCPA consent
- Time-of-day restrictions
- STOP keyword required
- Message frequency limits

**Phone:**
- DNC list compliance
- Calling hour restrictions
- Disclosure requirements

**Chat:**
- Privacy policy
- Data handling
- Bot disclosure (in some jurisdictions)

### Cross-Channel Consent

**Track:**
- Consent per channel
- Date of consent
- Source of consent
- Opt-out per channel

**Respect:**
- Email opt-out ≠ SMS opt-out (but be careful)
- Be conservative
- When in doubt, don't contact

---

## Measuring Multi-Channel Effectiveness

### Per-Channel Metrics

| Metric | Email | SMS | Phone | Chat |
|--------|-------|-----|-------|------|
| Delivery rate | ✓ | ✓ | ✓ | N/A |
| Open/Answer rate | ✓ | ✓ | ✓ | N/A |
| Response rate | ✓ | ✓ | ✓ | ✓ |
| Conversion rate | ✓ | ✓ | ✓ | ✓ |
| Opt-out rate | ✓ | ✓ | ✓ | N/A |

### Cross-Channel Metrics

**Sequence metrics:**
- Overall sequence response rate
- Touch-to-conversion ratio
- Channel contribution to conversion
- Average touches to response

**Coordination metrics:**
- Cross-channel engagement
- Channel preference distribution
- Frequency complaint rate
- Multi-channel vs. single-channel performance

---

## Questions to Ask

If you need more context:
1. What channels are you currently using?
2. How many touches per prospect per week?
3. How do you currently coordinate across channels?
4. What compliance requirements apply?
5. Do you have cross-channel engagement data?

---

## Related Skills

- **timing-optimization**: When to use each channel
- **conversation-memory**: Remembering across channels
- **compliance-handling**: Channel-specific requirements
- **re-engagement-sequencing**: Multi-channel nurture
