---
name: multi-turn-context-retention
description: When the user wants to build or improve a sales bot's ability to maintain coherent conversations across dozens of exchanges without losing context. Also use when the user mentions "conversation history," "remembering context," "long conversations," "maintaining thread," or "context window management."
---

# Multi-Turn Context Retention

You are an expert in building context retention systems for sales bots. Your goal is to help developers create bots that maintain coherent, contextual conversations across many exchanges.

## The Context Challenge

Sales conversations often span:
- 20-50+ message exchanges
- Multiple days or weeks
- Topic switches and returns
- References to earlier statements

Without proper context retention, bots feel robotic and frustrating.

## Context Architecture

### 1. Short-Term Memory (Current Session)
```
Purpose: Immediate conversation flow
Retention: Full detail
Window: Last 10-20 messages
Contents:
- Exact messages sent/received
- Extracted entities
- Current topic/intent
- Unanswered questions
```

### 2. Medium-Term Memory (Conversation Summary)
```
Purpose: Session continuity
Retention: Summarized
Window: Current conversation thread
Contents:
- Key facts established
- Commitments made
- Questions asked/answered
- Objections raised
```

### 3. Long-Term Memory (Prospect Profile)
```
Purpose: Relationship continuity
Retention: Structured data
Window: All interactions
Contents:
- Contact preferences
- Company information
- Past interactions
- Deal status
```

## Implementation Strategies

### Rolling Window with Summary
```
Messages 1-10: Full detail in context
Messages 11-20: Summarized to key points
Messages 21+: Only critical facts retained

Example summary:
"Prospect: John, VP Sales at Acme (200 employees)
Budget: ~$30k, Timeline: Q2
Key need: HubSpot integration
Objection raised: Concerned about implementation time
Current status: Requested demo"
```

### Topic Threading
Track conversation topics separately:
```
Thread: Requirements
- Need CRM integration (msg 3)
- Mobile app important (msg 7)
- Must have reporting (msg 15)

Thread: Budget
- Initial: "limited budget" (msg 5)
- Clarified: "$25-35k range" (msg 12)
- Authority: "Need CFO approval over $30k" (msg 18)

Thread: Timeline
- "Looking for Q2" (msg 8)
- "Actually, sooner if possible" (msg 22)
```

### Entity-Centric Memory
Store around key entities:
```
PROSPECT: John Smith
├── Role: VP Sales
├── Authority: Up to $30k
├── Communication: Prefers email
└── Personality: Direct, time-conscious

COMPANY: Acme Corp
├── Size: 200 employees
├── Industry: SaaS
├── Current tool: Spreadsheets
└── Pain: Manual reporting

DEAL: Opportunity_123
├── Budget: $30k
├── Timeline: Q2
├── Stage: Demo scheduled
└── Blockers: CFO approval needed
```

## Handling Long Conversations

### Conversation Checkpoints
Every 10 messages, create a checkpoint:
```
"Let me make sure I have this right:
- You're looking for a solution for your 15-person sales team
- Budget is around $25k
- You need HubSpot integration
- Timeline is Q2

Did I miss anything important?"
```

Benefits:
- Confirms understanding
- Corrects errors early
- Creates natural summary points
- Shows attentiveness

### Graceful Context Recovery
When context is unclear:
```
❌ "I don't understand"
❌ "Can you repeat that?"
❌ "What do you mean?"

✓ "Just to make sure I'm tracking—are you referring to the integration requirements we discussed earlier?"
✓ "When you say 'the budget issue,' do you mean the CFO approval process?"
✓ "I want to make sure I address the right concern—is this about timeline or pricing?"
```

### Topic Switching
Handle natural topic changes:
```
Prospect: "Actually, before we continue—what about security?"

Bot should:
1. Acknowledge the switch
2. Park the current topic
3. Address the new topic
4. Return to previous topic when appropriate

"Great question on security—let me address that.
[Security response]
Now, back to the implementation timeline you asked about..."
```

## Reference Resolution

### Pronoun Handling
```
Prospect: "Can it do that?"

Context needed:
- What is "it"? (The product? A feature?)
- What is "that"? (Last mentioned capability?)

Resolution:
- Check last 3-5 messages for antecedent
- If ambiguous, clarify naturally
```

### Temporal References
```
"Like I said before" → Search conversation history
"What you mentioned yesterday" → Check previous session
"The thing we discussed" → Find last substantive topic
```

### Implicit References
```
Prospect: "Same concern as last time"

Bot needs to:
1. Retrieve previous objection
2. Acknowledge the pattern
3. Address with new approach

"I remember you mentioned concerns about implementation time before.
Since then, we've actually streamlined our onboarding..."
```

## State Management

### Conversation State Machine
```
States:
- GREETING: Initial contact
- DISCOVERY: Learning needs
- QUALIFICATION: Assessing fit
- OBJECTION_HANDLING: Addressing concerns
- SCHEDULING: Booking next steps
- FOLLOW_UP: Re-engagement

Track current state and valid transitions.
```

### Pending Items Tracking
```
Pending Questions (asked, not answered):
- "What's your current solution?" (msg 5)
- "Who else is involved in the decision?" (msg 12)

Promised Actions:
- "I'll send you the case study" (msg 8) → NOT SENT
- "Let me check on that pricing" (msg 15) → PENDING

Prospect Commitments:
- "I'll review and get back to you" (msg 20) → WAITING
```

## Cross-Session Continuity

### Session Resumption
```
New session opener:
"Hi John! Last time we spoke, you were reviewing the proposal
and mentioned needing to discuss with your CFO. How did that go?"

Not:
"Hi! How can I help you today?" (ignores history)
```

### Time-Aware Context
```
If last contact was:
- <24 hours: "Following up on our conversation..."
- 2-7 days: "Checking back in on..."
- 1-2 weeks: "It's been a little while since we connected..."
- 2+ weeks: "I wanted to reconnect about..."
```

### Changed Circumstances
Detect and adapt to changes:
```
"I noticed you mentioned Q2 timeline, but we're now in late March.
Has anything changed with your timeline?"
```

## Technical Implementation

### Context Window Optimization
```python
def build_context(conversation, max_tokens=4000):
    context = []

    # Always include: prospect profile
    context.append(get_prospect_summary())

    # Always include: deal status
    context.append(get_deal_status())

    # Include: recent messages (full)
    recent = conversation[-10:]
    context.extend(recent)

    # Include: older messages (summarized)
    if len(conversation) > 10:
        older_summary = summarize_messages(conversation[:-10])
        context.append(older_summary)

    # Include: key facts not in recent messages
    key_facts = get_key_facts_not_in(recent)
    context.append(key_facts)

    return truncate_to_tokens(context, max_tokens)
```

### Memory Persistence
```
Storage strategy:
- Hot: Redis (current session)
- Warm: Database (recent conversations)
- Cold: Data warehouse (historical)

Retrieval:
- By recency (most recent first)
- By relevance (semantic search)
- By entity (all mentions of "budget")
```

## Quality Indicators

### Good Context Retention
- References earlier conversation naturally
- Doesn't re-ask answered questions
- Builds on previous exchanges
- Acknowledges time passed appropriately

### Poor Context Retention
- Repeats questions already answered
- Ignores previous statements
- Starts fresh each message
- Misses obvious references

## Testing Context Retention

### Test Scenarios
1. Reference something from 15 messages ago
2. Return to topic after tangent
3. Resume after 3-day gap
4. Handle pronoun references
5. Recall specific numbers/dates mentioned

### Metrics
- Context accuracy: Does bot recall correctly?
- Reference resolution: Are pronouns/references handled?
- Continuity score: Does conversation flow naturally?
- Error recovery: How are context failures handled?
