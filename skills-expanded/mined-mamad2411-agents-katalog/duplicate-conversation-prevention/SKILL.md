---
name: duplicate-conversation-prevention
description: When the user wants to build or improve a sales bot's ability to prevent contacting the same prospect through multiple channels simultaneously. Also use when the user mentions "duplicate prevention," "contact deduplication," "conversation collision," "multi-channel overlap," or "prospect fatigue prevention."
---

# Duplicate Conversation Prevention

You are an expert in building systems that prevent sales bots from overwhelming prospects with simultaneous outreach. Your goal is to help developers create intelligent coordination that avoids duplicate contacts while maximizing coverage.

## Why This Matters

### The Collision Problem
```
Without coordination:
- Email sequence sends Day 3 message
- SMS bot triggers engagement sequence
- LinkedIn bot sends connection request
- Phone system queues callback

All happen within same 2-hour window.

Result: Prospect annoyed, opt-out, reputation damage
```

### With Duplicate Prevention
```
Coordinated outreach:
- Email sends → All other channels pause 24h
- Response detected → Route to single channel
- Engagement spike → Consolidate to winning channel

Result: Coherent experience, higher conversion
```

## Duplicate Detection Layers

### Layer 1: Identity Resolution
```
Match prospects across channels:

Primary keys:
- Email address (normalized)
- Phone number (E.164 format)
- LinkedIn URL/ID

Secondary matching:
- Name + Company combination
- Domain + first name
- Phone area code + name

Fuzzy matching:
- "John Smith" vs "J. Smith"
- "john@company.com" vs "jsmith@company.com"
- "+1 (555) 123-4567" vs "5551234567"
```

### Layer 2: Channel Coordination
```
Track active conversations:

{
  "prospect_id": "unified_12345",
  "active_channels": ["email", "sms"],
  "last_touch": {
    "email": "2024-01-15T10:00:00Z",
    "sms": "2024-01-14T14:30:00Z"
  },
  "status": "awaiting_response",
  "cooldown_until": "2024-01-16T10:00:00Z"
}

Before any outreach:
1. Check if prospect in active conversation
2. Check cooldown period
3. Verify channel not recently used
4. Confirm no pending touches queued
```

### Layer 3: Sequence Awareness
```
Track sequence membership:

Prospect enrolled in:
- "Enterprise Outbound" email sequence (Step 3)
- "Demo Follow-up" SMS sequence (Step 1)

Conflict detection:
- Same prospect, multiple sequences
- Overlapping timing
- Conflicting messages

Resolution:
- Priority rules (demo > cold outreach)
- Pause lower priority sequence
- Merge into single coordinated flow
```

## Coordination Strategies

### Channel Lockout
```
When outreach occurs on Channel A:
→ Lock other channels for X hours

Lockout rules:
Email sent → 24h lockout on SMS, phone
SMS sent → 48h lockout on email, phone
Call made → 72h lockout on all automated
Response received → All automated paused

This prevents pile-on effect.
```

### Primary Channel Assignment
```
Assign each prospect a primary channel:

Based on:
- Response history (responded to email? = email primary)
- Preference stated ("text me" = SMS primary)
- Engagement data (opens email, ignores SMS)
- Industry norms (enterprise = email, SMB = phone)

Once assigned:
- 80% of touches on primary
- Other channels for variety/re-engagement only
```

### Conversation State Machine
```
States:
- COLD: No active outreach
- ACTIVE: Sequence in progress
- ENGAGED: Response received
- MEETING_SET: Appointment booked
- PAUSED: Manual hold
- OPTED_OUT: Do not contact

Transitions control outreach:
COLD → ACTIVE: Start sequence
ACTIVE → Can receive next touch
ENGAGED → All automated stops, human takes over
MEETING_SET → Only reminders allowed
PAUSED → No outreach
OPTED_OUT → No outreach ever
```

## Implementation Patterns

### Centralized Queue
```python
class OutreachQueue:
    def can_send(self, prospect_id, channel):
        # Check unified contact record
        prospect = get_unified_prospect(prospect_id)

        # Already in active conversation?
        if prospect.conversation_state == "ENGAGED":
            return False

        # Channel in cooldown?
        if is_channel_locked(prospect_id, channel):
            return False

        # Too many recent touches?
        recent = count_touches_last_48h(prospect_id)
        if recent >= MAX_TOUCHES_48H:
            return False

        # Pending touch in queue?
        if has_pending_touch(prospect_id):
            return False

        return True

    def record_touch(self, prospect_id, channel, message_type):
        # Log the touch
        log_touch(prospect_id, channel, message_type)

        # Lock other channels
        apply_lockout(prospect_id, channel)

        # Update conversation state
        update_state(prospect_id, "ACTIVE")
```

### Distributed Locking
```
For multi-system coordination:

Before send:
1. Acquire lock: prospect_id + channel
2. Check cooldowns
3. Send message
4. Record touch
5. Apply lockouts
6. Release lock

Lock timeout: 30 seconds
Prevents race conditions between systems
```

### Event-Driven Coordination
```
Publish events to message bus:

Events:
- touch.sent: {prospect_id, channel, timestamp}
- response.received: {prospect_id, channel}
- meeting.booked: {prospect_id}
- opt_out.recorded: {prospect_id}

All systems subscribe and react:
- Email system pauses on touch.sent from SMS
- All systems stop on response.received
- Reminders only on meeting.booked
```

## Deduplication Rules

### Contact Normalization
```python
def normalize_contact(contact):
    # Email
    email = contact.email.lower().strip()
    email = remove_plus_addressing(email)  # john+test@... → john@...

    # Phone
    phone = digits_only(contact.phone)
    phone = to_e164(phone, contact.country)  # +15551234567

    # Name
    name = contact.name.strip().title()

    return NormalizedContact(email, phone, name)
```

### Merge Strategy
```
When duplicates found:

Same email, different phones:
→ Merge records
→ Add both phones to contact
→ Use most recent as primary

Same phone, different emails:
→ Verify not different people
→ If same person, merge
→ Use business email as primary

Name + Company match only:
→ Flag for review
→ Don't auto-merge
→ Treat as potentially same person
```

### Conflict Resolution
```
When same prospect in multiple sequences:

Priority order:
1. Active deal sequences (highest)
2. Response follow-up sequences
3. Re-engagement sequences
4. Cold outreach sequences (lowest)

Action:
- Pause lower priority sequences
- Continue highest priority only
- Resume others after completion/exit
```

## Cross-Channel Coordination

### Channel Handoff
```
When prospect responds on different channel:

Email sequence active, SMS response received:
1. Pause email sequence
2. Route SMS to conversation
3. Mark email as "response on other channel"
4. Continue on SMS only

Don't:
- Send next email anyway
- Ask same question on email
- Ignore the SMS response
```

### Unified Inbox
```
All responses flow to single view:

- Email replies
- SMS responses
- LinkedIn messages
- Call notes

Rep sees full picture:
- Chronological timeline
- All channels merged
- Single response thread
- No confusion about where to reply
```

## Edge Cases

### Legitimate Multi-Channel
```
Sometimes multiple touches are OK:

Meeting reminder:
- Email confirmation (day before)
- SMS reminder (1 hour before)
→ Both expected, not duplicates

Different stakeholders:
- Email to champion
- Call to economic buyer
→ Different people, both needed

Sequential escalation:
- Email → no response 5 days
- SMS → "Did you see my email?"
→ Intentional, coordinated
```

### Handling Shared Inboxes
```
Multiple people, one email:

sales@company.com
info@company.com

Detection:
- Generic prefix
- Multiple responders
- Different signatures

Strategy:
- Track individual responders separately
- Company-level coordination
- Don't assume single contact
```

### Organizational Awareness
```
Multiple contacts at same company:

Coordinate across prospects:
- Don't email CEO and CFO same day
- Space out touches within org
- Track company-level activity

Rules:
- Max 2 people/company/day
- 48h between same-department contacts
- Share positive signals across contacts
```

## Metrics

### Collision Rate
```
Track:
- Duplicate touches sent (failure)
- Touches blocked by coordination (success)
- Near-misses (within 4h window)

Target: <1% collision rate

Alert when:
- Same prospect, 2+ channels, <24h apart
- Same prospect, same channel, <48h apart
```

### Opt-Out Attribution
```
When opt-out occurs:

Check:
- Touches in last 7 days
- Channels used
- Frequency

Flag if:
- 3+ touches in 48h preceded opt-out
- Multiple channels same day
- Volume spike before opt-out

Use for rule refinement.
```

## System Design

### Architecture
```
┌─────────────┐     ┌─────────────┐
│ Email Bot   │────▶│             │
├─────────────┤     │  Unified    │
│ SMS Bot     │────▶│  Outreach   │
├─────────────┤     │  Controller │
│ Phone Bot   │────▶│             │
├─────────────┤     └──────┬──────┘
│ LinkedIn    │────▶       │
└─────────────┘            ▼
                    ┌─────────────┐
                    │  Prospect   │
                    │  Database   │
                    └─────────────┘

All outreach routes through controller.
Controller enforces coordination rules.
```

### State Storage
```json
{
  "prospect_id": "unified_12345",
  "identities": {
    "email": "john@company.com",
    "phone": "+15551234567",
    "linkedin": "linkedin.com/in/johnsmith"
  },
  "conversation_state": "ACTIVE",
  "primary_channel": "email",
  "active_sequences": ["enterprise_outbound"],
  "last_touches": {
    "email": {"at": "2024-01-15T10:00:00Z", "type": "sequence_step_3"},
    "sms": {"at": "2024-01-10T14:00:00Z", "type": "intro"}
  },
  "lockouts": {
    "sms": "2024-01-16T10:00:00Z",
    "phone": "2024-01-16T10:00:00Z"
  },
  "touch_count_7d": 4
}
```

