---
name: conversation-branching
description: When the user wants to build or improve a sales bot's ability to dynamically choose conversation paths based on prospect responses rather than following rigid scripts. Also use when the user mentions "dynamic conversations," "branching logic," "conversation flows," "adaptive scripts," or "conditional responses."
---

# Conversation Branching

You are an expert in building dynamic conversation systems for sales bots. Your goal is to help developers create bots that adapt their approach based on prospect responses rather than following rigid, linear scripts.

## Why Branching Matters

Rigid scripts feel robotic:
```
Bot: "What's your budget?"
Prospect: "We're more concerned about timeline right now."
Bot: "Great! And what's your timeline?"  ← Ignored their signal
```

Dynamic branching feels human:
```
Bot: "What's your budget?"
Prospect: "We're more concerned about timeline right now."
Bot: "Timeline is definitely important. When are you hoping to have
      a solution in place?"  ← Followed their lead
```

## Branching Architecture

### Decision Points
```
Every prospect response creates a decision point:

[Prospect Message]
      │
      ▼
┌─────────────────┐
│ Classify Intent │
└────────┬────────┘
         │
    ┌────┴────┬────────┬─────────┐
    ▼         ▼        ▼         ▼
[Answer]  [Question] [Objection] [Off-topic]
    │         │        │         │
    ▼         ▼        ▼         ▼
[Next Q]  [Address]  [Handle]  [Redirect]
```

### Branch Types

**Conditional Branches**
Based on specific criteria:
- IF budget > $50k → Enterprise path
- IF timeline < 30 days → Urgency path
- IF competitor mentioned → Competitive path

**Sentiment Branches**
Based on emotional signals:
- IF positive/enthusiastic → Accelerate
- IF skeptical/hesitant → Build trust
- IF frustrated/annoyed → De-escalate

**Intent Branches**
Based on what prospect wants:
- IF seeking information → Educate
- IF ready to buy → Close
- IF just browsing → Nurture

## Building Branch Logic

### Response Classification
```
Input: "I'm not sure we have budget for this"

Classifications:
- Topic: Budget
- Sentiment: Uncertain (not negative)
- Objection type: Budget concern
- Buying stage: Early consideration
- Required branch: Budget objection handling

Available branches:
1. Explore budget flexibility
2. Discuss ROI/value
3. Offer smaller starting point
4. Qualify out gracefully
```

### Branch Conditions
```yaml
branch: budget_objection
conditions:
  - contains: ["budget", "expensive", "cost", "afford", "price"]
  - sentiment: [negative, uncertain]
  - not_contains: ["what's the price", "how much"]  # That's a question, not objection

responses:
  - if: budget_mentioned_before == false
    then: explore_budget
  - if: budget_amount < threshold
    then: offer_alternative
  - if: sentiment == "firm_no"
    then: graceful_exit
  - default: value_justification
```

### Priority Handling
When multiple branches match:
```
Priority order:
1. Safety/compliance (always first)
2. Explicit requests ("call me back")
3. Objections (must address)
4. Questions (should answer)
5. Conversation flow (can wait)

Example:
Prospect: "This sounds expensive, and can you email me info?"

Matches:
- Budget objection (priority 3)
- Email request (priority 2)

Handle request first:
"Absolutely, I'll email you detailed info. Before I do—
when you say expensive, is that compared to your current
solution or your budget?"
```

## Common Branch Patterns

### The Qualification Fork
```
"Are you the decision maker?"

Branch A: "Yes"
→ Continue qualification
→ Ask about timeline, budget, needs

Branch B: "No, I need to involve my boss"
→ Identify decision maker
→ Offer to include them
→ Arm champion with info

Branch C: "It's a committee decision"
→ Map the buying committee
→ Understand each stakeholder
→ Plan multi-thread approach
```

### The Objection Tree
```
"It's too expensive"

Branch A: Budget doesn't exist
→ "Sounds like budget is tight. Is this a priority
   that could get funding if the ROI was clear?"

Branch B: Budget exists, price too high
→ "I hear you. Can you share what you were expecting?
   I want to see if we can find a solution that fits."

Branch C: Comparing to competitor
→ "Compared to [competitor]? Let me share why
   customers choose us despite the price difference."

Branch D: Not seeing value
→ "I may not have explained the value well.
   What would this need to do to be worth $X?"
```

### The Timeline Fork
```
"When are you looking to implement?"

Branch A: "ASAP"
→ Accelerate process
→ Identify blockers
→ Offer expedited path

Branch B: "Next quarter"
→ Normal cadence
→ Build relationship
→ Schedule appropriately

Branch C: "Just exploring"
→ Nurture mode
→ Provide value/education
→ Stay in touch loosely

Branch D: "Not sure"
→ Help define timeline
→ Uncover driving events
→ Create urgency if appropriate
```

## Implementing Branches

### State Machine Approach
```
States:
- INITIAL_CONTACT
- NEEDS_DISCOVERY
- QUALIFICATION
- DEMO_SCHEDULING
- OBJECTION_HANDLING
- NEGOTIATION
- CLOSING
- NURTURE

Transitions:
NEEDS_DISCOVERY + positive_response → QUALIFICATION
QUALIFICATION + objection → OBJECTION_HANDLING
OBJECTION_HANDLING + resolved → QUALIFICATION
QUALIFICATION + ready_signal → DEMO_SCHEDULING
Any_State + "not interested" → NURTURE
```

### Decision Tree Structure
```python
def decide_branch(message, context):
    # Check for explicit requests first
    if contains_meeting_request(message):
        return "schedule_meeting"

    if contains_question(message):
        return handle_question(message, context)

    if contains_objection(message):
        objection_type = classify_objection(message)
        return f"handle_{objection_type}_objection"

    if is_positive_response(message):
        return advance_conversation(context.current_stage)

    if is_negative_response(message):
        return "address_concerns"

    # Default: continue current path
    return context.next_planned_step
```

### Fallback Handling
```
When no branch matches:
1. Acknowledge the response
2. Gently redirect to main path
3. Or ask clarifying question

"I appreciate you sharing that. To make sure I'm helpful—
what's the main thing you're hoping to solve right now?"
```

## Branch Testing

### Coverage Testing
Ensure all branches are reachable:
- Map every possible path
- Test edge cases
- Verify dead ends don't exist

### Path Analysis
```
Successful conversations:
- Average branches taken: 8
- Most common path: A→B→D→F→H
- Drop-off points: Branch C (objection handling)

Optimize:
- Improve Branch C handling
- Reduce unnecessary branches
- Smooth common path
```

### A/B Testing Branches
```
Test different responses at same branch point:

Branch: Timeline discovery

A: "When are you looking to make a decision?"
B: "What's driving your timeline?"
C: "Is there a specific event you're working toward?"

Measure: Response quality, conversation advancement
```

## Advanced Branching

### Parallel Paths
Handle multiple threads simultaneously:
```
Prospect: "What's the price, and does it integrate with Salesforce?"

Branch: Both questions need answers

Response:
"Great questions—let me address both.

For integration: Yes, we have native Salesforce integration
that syncs in real-time.

For pricing: It depends on team size. Roughly how many
people would be using it?"
```

### Branch Memory
Remember why you're on a branch:
```
Context: Entered budget_objection branch

After handling:
- Don't re-ask budget question
- Reference the concern was addressed
- Check if resolved before proceeding

"Now that we've talked through the ROI—does that
help with the budget concern you mentioned?"
```

### Adaptive Difficulty
Adjust questioning based on engagement:
```
High engagement → Ask harder qualifying questions
Low engagement → Simplify, be more direct
Expert prospect → Skip basics
Novice prospect → Educate more
```
