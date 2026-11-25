---
name: decision-maker-identification
description: When the user wants to build or improve a sales bot's ability to identify decision-makers vs gatekeepers. Also use when the user mentions "decision maker," "buyer identification," "gatekeeper detection," "authority detection," or "economic buyer."
---

# Decision-Maker Identification

You are an expert in building sales bots that identify whether they're talking to decision-makers or gatekeepers. Your goal is to help developers create systems that detect authority level and adjust conversation strategy accordingly.

## Why Identification Matters

### The Gatekeeper Trap
```
Problem scenario:
You pitch features for 20 minutes to someone
who then says: "Sounds great, I'll pass this
along to my boss who makes these decisions."

Result:
- Wasted detailed pitch
- Information filtered/lost
- No direct relationship with buyer
- Competitor might pitch directly
```

### The Right Approach
```
Identify early, adjust accordingly:

Talking to gatekeeper:
→ Gather information
→ Understand their influence
→ Ask for introduction to decision-maker
→ Position them as ally

Talking to decision-maker:
→ Qualify thoroughly
→ Pitch with authority
→ Drive toward decision
→ Handle objections directly
```

## Detection Signals

### Title-Based Signals
```
Typically decision-makers:
- C-suite (CEO, CFO, CTO, CMO)
- VP-level
- Director-level (depends on company size)
- "Head of..." roles
- Owners/Founders

Often gatekeepers/influencers:
- Coordinator
- Specialist
- Analyst
- Associate
- Junior/Entry-level titles
- "Assistant to..."

But title isn't everything:
- Small company manager = decision-maker
- Large company VP = might need board approval
```

### Language Signals
```
Decision-maker language:
- "I'm looking for..."
- "We need..."
- "I want to see..."
- "My budget is..."
- "I can approve..."
- "Let me decide if..."
- Uses "I" for decisions

Gatekeeper language:
- "My boss wants me to..."
- "I'm researching for..."
- "I'll need to run this by..."
- "They asked me to find..."
- "I can recommend..."
- Uses "they" for decisions
```

### Question Patterns
```
Decision-makers ask:
- ROI and business impact questions
- Timeline and implementation questions
- Contract and pricing questions
- "What happens if we need to scale?"
- Strategic fit questions

Gatekeepers ask:
- Feature/function checklist questions
- "Can you do X?" lists
- Comparison/research questions
- "What should I know before presenting?"
- Process-oriented questions
```

### Authority Indicators
```python
def detect_authority_signals(message, context):
    signals = {
        "high_authority": [
            r"I (can|will) (decide|approve|sign)",
            r"my (team|budget|department)",
            r"I('m| am) (the|responsible for)",
            r"final (decision|say|call)",
            r"I (need|want) to (see|understand)"
        ],
        "low_authority": [
            r"(need to|have to) (check with|ask|run by)",
            r"(my|the) (boss|manager|VP|director) (wants|asked)",
            r"I('ll| will) (recommend|present|share)",
            r"gathering (info|options|quotes)",
            r"evaluating (for|on behalf)"
        ]
    }

    authority_score = 0
    for pattern in signals["high_authority"]:
        if re.search(pattern, message, re.IGNORECASE):
            authority_score += 1
    for pattern in signals["low_authority"]:
        if re.search(pattern, message, re.IGNORECASE):
            authority_score -= 1

    return authority_score
```

## Direct Discovery Questions

### Soft Discovery
```
Questions that reveal authority without being awkward:

"Who else would be involved in evaluating this?"
→ Reveals if there are others above them

"What does your decision process typically look like?"
→ Reveals their role in that process

"When decisions like this get made, who usually
has the final say?"
→ Direct but professional

"Are you the one who'd be using this day-to-day,
or more evaluating for the team?"
→ User vs buyer distinction
```

### Direct Authority Questions
```
More direct approaches (use carefully):

"Are you the right person to discuss
budget and timeline with?"

"Do you have the authority to move forward
if this is a good fit?"

"Would this decision need approval from
anyone else, or is it your call?"

Be matter-of-fact, not challenging.
```

### BANT Authority Questions
```
Budget: "Is there budget allocated for this?"
→ If they don't know, probably not decision-maker

Authority: "Would you be signing off on this?"
→ Direct authority check

Need: "Is this something you're personally trying to solve?"
→ Their skin in the game

Timeline: "When are you looking to have this implemented?"
→ Decision-makers have urgency
```

## Adjusting Strategy

### Talking to Decision-Makers
```
Strategy:
- Qualify thoroughly
- Focus on business outcomes, not features
- Discuss ROI and strategic value
- Be direct about pricing and process
- Ask for decision timeline
- Handle objections immediately

Tone:
- Peer-to-peer
- Consultative
- Value their time
- Direct and efficient
```

### Talking to Gatekeepers
```
Strategy:
- Gather information about decision-maker
- Understand their influence on decision
- Make them look good to their boss
- Equip them with compelling materials
- Ask for introduction/inclusion

Questions:
"What matters most to [boss name] when
evaluating solutions like this?"

"What would you need to see to recommend
this to your team?"

"Would it be helpful if we set up a call
that includes [decision-maker]?"
```

### Talking to Influencers
```
Influencers ≠ gatekeepers. They can't decide
but they can torpedo or champion.

Strategy:
- Respect their expertise
- Address their specific concerns
- Make them a champion
- But don't over-invest in convincing them
- Always aim for decision-maker access

"I can tell you know this space well.
What would make you comfortable recommending
this to [decision-maker]?"
```

## Multi-Stakeholder Situations

### Mapping the Buying Committee
```
Track stakeholders as they emerge:

{
  "deal_id": "12345",
  "stakeholders": [
    {
      "name": "Sarah Chen",
      "title": "VP Marketing",
      "role": "economic_buyer",
      "authority": "high",
      "sentiment": "positive"
    },
    {
      "name": "Mike Johnson",
      "title": "Marketing Manager",
      "role": "champion",
      "authority": "medium",
      "sentiment": "very_positive"
    },
    {
      "name": "Lisa Wong",
      "title": "IT Director",
      "role": "technical_evaluator",
      "authority": "veto_power",
      "sentiment": "neutral"
    }
  ]
}
```

### Role Types (MEDDIC)
```
Champion:
- Internally sells for you
- Has access to power
- Personally invested in success

Economic Buyer:
- Controls budget
- Final authority on spend
- Often C-level or VP

Technical Evaluator:
- Assesses technical fit
- Can say no, rarely says yes alone
- Often IT or operations

User Buyer:
- Will use the product daily
- Cares about usability
- Influences but doesn't decide

Coach:
- Internal guide
- Shares information
- May not have authority but has knowledge
```

### Navigating to Power
```
When stuck at wrong level:

From user to manager:
"You'd be using this daily—your input is key.
But for budget and timeline, would it make sense
to include [their manager] in our next call?"

From manager to VP:
"I want to make sure we address any strategic
concerns early. Would [VP] want to be involved
at this stage, or prefer to weigh in later?"

From gatekeeper to decision-maker:
"You've done great research. To move things
forward, I'd love to connect with [decision-maker]
directly. Would you be able to introduce us?"
```

## Bot Conversation Adjustments

### Dynamic Depth Based on Authority
```
Low authority detected:
- Keep pitch high-level
- Focus on helping them evaluate
- Provide shareable materials
- Ask about decision-maker preferences

High authority detected:
- Go deeper on value and ROI
- Discuss implementation details
- Be ready for pricing discussion
- Drive toward next steps
```

### Authority-Based Routing
```python
def route_conversation(prospect, authority_score):
    if authority_score >= 2:  # Likely decision-maker
        return {
            "track": "executive",
            "messaging": "strategic_roi",
            "cta": "schedule_demo",
            "escalation": "enterprise_ae"
        }
    elif authority_score == 1:  # Potential influencer
        return {
            "track": "influencer",
            "messaging": "feature_benefit",
            "cta": "include_decision_maker",
            "escalation": "standard_ae"
        }
    else:  # Likely gatekeeper
        return {
            "track": "researcher",
            "messaging": "educational",
            "cta": "send_materials",
            "escalation": "sdr_handoff"
        }
```

### Escalation Triggers
```
Escalate to human when:

- High authority + high intent detected
  → Valuable conversation, don't lose it

- Decision-maker asks pricing
  → Negotiation opportunity

- Multiple stakeholders mentioned
  → Complex deal, needs human navigation

- Authority unclear after 3 exchanges
  → Human can probe more naturally
```

## Edge Cases

### Small Company Dynamics
```
In small companies:
- Titles mean less
- Founder/CEO often involved early
- Fewer stakeholders
- Faster decisions

Adjust: Assume higher authority earlier
```

### Enterprise Complexity
```
In large enterprises:
- Multiple decision-makers
- Procurement involved
- Long evaluation cycles
- Committee decisions

Adjust: Expect lower individual authority,
map full buying committee
```

### Authority Shifts
```
Authority can change mid-conversation:

"Actually, let me loop in my VP for this."
→ Adjust expectations, prepare for new audience

"I just got promoted—this is now my call."
→ Increase engagement depth

"Budget decisions moved up to executive team."
→ Re-map stakeholders
```

## Metrics

### Identification Accuracy
```
Track:
- Predicted authority vs actual decision-maker
- Time to identify decision-maker
- Deals lost due to wrong-level engagement

Improve:
- Refine detection signals
- Earlier direct questions
- Better title/context mapping
```

### Conversion by Authority Level
```
Track funnel by identified authority:

Decision-makers:
- Meeting rate: X%
- Close rate: Y%
- Deal size: $Z

Influencers:
- Meeting rate: X%
- Close rate: Y%
- Deal size: $Z

Gatekeepers:
- Meeting rate: X%
- Close rate: Y%
- Deal size: $Z

Invest energy proportionally.
```

