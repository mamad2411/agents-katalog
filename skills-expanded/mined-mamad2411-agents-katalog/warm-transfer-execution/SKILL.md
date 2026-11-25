---
name: warm-transfer-execution
description: When the user wants to build or improve a sales bot's ability to seamlessly connect prospects to live reps with full context passed along. Also use when the user mentions "warm handoff," "transfer to human," "live rep handoff," "context handover," or "seamless transfer."
---

# Warm Transfer Execution

You are an expert in building seamless handoff systems for sales bots. Your goal is to help developers create transfers to human reps that feel smooth and maintain conversation momentum.

## What Makes a Transfer "Warm"

### Cold Transfer (Bad)
```
Bot: "Let me transfer you to a representative."
[Call connects]
Rep: "Hi, how can I help you?"
Prospect: "I was just talking to your chatbot about..."
Rep: "Can you start from the beginning?"
```

### Warm Transfer (Good)
```
Bot: "Sarah from our enterprise team will help you
from here. She knows you're looking at the 500-user
plan for Q2. One moment while I connect you."
[Transfer happens]
Rep: "Hi [Name]! I see you're evaluating our enterprise
plan for about 500 users. I also saw you had questions
about Salesforce integration. Let's dive in!"
```

## Transfer Triggers

### When to Transfer
```
Positive triggers (opportunity):
- High-value prospect identified
- Ready to buy signals
- Request for demo/meeting
- Complex questions needing expertise
- Enterprise-level inquiry

Necessary triggers (capability):
- Bot can't answer question
- Negotiation required
- Contract/legal discussions
- Escalation requested
- Language routing needed

Rescue triggers (risk):
- Frustrated prospect
- Repeated misunderstandings
- Sensitive situation
- VIP/strategic account
- Complaint in progress
```

### Transfer Timing
```
Good timing:
- Natural conversation break
- After collecting key information
- When they ask for human
- Before conversation degrades

Bad timing:
- Mid-sentence/thought
- Before understanding their need
- Without warning
- When no human available
```

## Context Package

### Essential Information
```
Transfer context must include:

PROSPECT INFO:
- Name
- Company
- Contact info
- Account history (if any)

CONVERSATION SUMMARY:
- How they found you
- What they asked about
- Key needs expressed
- Pain points mentioned
- Budget/timeline indicators

QUALIFICATION DATA:
- Company size
- Use case
- Decision timeline
- Budget range
- Decision maker status

SENTIMENT:
- Overall tone
- Frustration points
- Excitement points
- Specific concerns

RECOMMENDED APPROACH:
- What they respond to
- What to avoid
- Suggested next step
```

### Context Format
```json
{
  "transfer_id": "xfer_12345",
  "timestamp": "2024-01-15T14:30:00Z",
  "prospect": {
    "name": "John Smith",
    "email": "john@acme.com",
    "phone": "+1-555-123-4567",
    "company": "Acme Corp",
    "title": "VP Sales",
    "account_id": null
  },
  "conversation": {
    "channel": "web_chat",
    "duration_minutes": 12,
    "messages_exchanged": 24,
    "started_at": "2024-01-15T14:18:00Z"
  },
  "summary": {
    "entry_point": "Clicked pricing page chat widget",
    "initial_question": "Enterprise pricing for 500+ users",
    "key_needs": [
      "Salesforce integration",
      "SSO/SAML support",
      "Custom reporting"
    ],
    "pain_points": [
      "Current tool doesn't scale",
      "Poor reporting capabilities"
    ],
    "objections_raised": [
      "Concerned about migration effort"
    ],
    "objections_addressed": true
  },
  "qualification": {
    "company_size": "500+ employees",
    "use_case": "Sales team productivity",
    "timeline": "Q2 implementation",
    "budget": "Mentioned 'Enterprise budget available'",
    "decision_maker": true,
    "score": 85
  },
  "sentiment": {
    "overall": "positive",
    "frustration_level": "low",
    "buying_intent": "high",
    "notes": "Impressed by Salesforce integration depth"
  },
  "transfer_reason": "Ready for demo, enterprise deal",
  "recommended_approach": "Focus on migration support and timeline",
  "conversation_transcript": "[full transcript link or embedded]"
}
```

## Transfer Flow

### Step 1: Prepare the Prospect
```
"Based on what you're looking for, I think [Rep Name]
from our enterprise team would be perfect to help.
[He/She] specializes in [relevant expertise].

Before I connect you, is there anything else I should
let [them] know?"
```

### Step 2: Check Availability
```
[Internal check]
- Is rep available?
- What's estimated wait time?
- Who else can take it?

If available:
"Perfect—[Rep] is available now. Let me connect you."

If not available:
"[Rep] is with another customer right now. You'll be
connected in about [X] minutes. Would you prefer to
wait, or should I have [them] call you back?"
```

### Step 3: Execute Transfer
```
To prospect:
"Connecting you now. [Rep] has the full context of
our conversation—you won't need to repeat anything."

To rep:
[Push notification with context package]
"Incoming: John from Acme Corp. 500-user enterprise
opportunity. Ready for demo. Hot lead."
```

### Step 4: Confirm Handoff
```
Rep acknowledgment:
"Got it—I see the context. Taking over."

Prospect confirmation:
Rep: "Hi John! I'm Sarah from the enterprise team.
I see you're looking at our solution for your 500-person
sales team, with Salesforce integration being key.
And you're hoping to have this in place by Q2, right?"
```

## Handling Transfer Scenarios

### Immediate Transfer (Live)
```
Chat/Phone - rep available:

Bot: "Connecting you with Alex now..."
[2-3 second transition]
Rep: "Hi [Name], Alex here. I saw you were asking about
[topic]. Let me help with that!"
```

### Queued Transfer
```
Rep not immediately available:

Bot: "Our team is helping other customers right now.
You're [2nd] in queue—estimated wait is [3 minutes].

While you wait, is there anything else I can help with?
Or if you prefer, I can have someone call you back at
a specific time."

Options:
1. Wait in queue
2. Scheduled callback
3. Email follow-up
```

### Async Transfer
```
After hours or no availability:

Bot: "Our team isn't available right now, but I've
captured everything we discussed. [Rep Name] will
reach out first thing tomorrow.

Is email or phone better for you?"

Then send:
- Confirmation to prospect
- Full context to rep
- Calendar task for follow-up
```

### Failed Transfer Recovery
```
If transfer fails:

Bot: "I apologize—we're having a technical issue
connecting you. Let me take your number and have
[Rep] call you directly within [X minutes].

What's the best number to reach you?"

Then:
- Collect callback info
- Alert rep immediately
- Log the issue
- Follow up to confirm connection made
```

## Rep Enablement

### Pre-Transfer Alert
```
[Push notification to rep]

🔥 HOT TRANSFER INCOMING 🔥
Prospect: John Smith, VP Sales @ Acme Corp
Score: 85/100 (Enterprise)
Context: 500 users, Salesforce integration, Q2 timeline
Sentiment: Positive, ready for demo
Transfer reason: Qualified, requesting demo

[Accept] [Defer to colleague] [Schedule callback]
```

### Context Display
```
Rep interface should show:
- Quick summary (scannable in 10 seconds)
- Key talking points
- Things to avoid
- Full transcript (expandable)
- Prospect profile (if in CRM)
- Suggested next steps
```

### Handoff Script Assistance
```
Suggested opener:
"Hi John! I'm [Rep] from the enterprise team.
[Bot name] filled me in—sounds like you're looking
to upgrade your 500-person sales team before Q2.
I'd love to help make that happen."

Key points to address:
☐ Salesforce integration details
☐ Migration support (concern raised)
☐ Q2 timeline feasibility
☐ Next step: Demo scheduling
```

## Quality Assurance

### Transfer Metrics
```
Track:
- Transfer completion rate
- Time to rep pickup
- Prospect satisfaction post-transfer
- Conversation continuation rate
- Conversion rate of transfers
- Context utilization by reps
```

### Feedback Loop
```
After transfer:
- Did rep find context helpful?
- Was anything missing?
- Did prospect have to repeat info?
- How could handoff improve?

Use feedback to improve context package.
```
