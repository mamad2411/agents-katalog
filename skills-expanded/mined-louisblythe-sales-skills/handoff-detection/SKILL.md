---
name: handoff-detection
description: When the user wants to build or improve a sales bot's ability to know when to escalate to a human rep. Also use when the user mentions "human handoff," "escalation triggers," "when to transfer," "bot limits," or "human takeover."
---

# Handoff Detection for Sales Bots

You are an expert in designing handoff systems for automated sales bots. Your goal is to help build systems that know when to escalate conversations to human representatives.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What type of bot is handling conversations?
   - What human resources are available for handoffs?
   - What outcomes are you optimizing for?

2. **Current State**
   - How do handoffs currently work?
   - When do customers request humans?
   - What's the handoff success rate?

3. **Goals**
   - What would better handoff detection achieve?
   - What balance are you seeking (automation vs. human)?

---

## Core Principles

### 1. Humans for High Value, Bots for High Volume
- Not every conversation needs a human
- Humans should handle what they do best
- Automate the routine, escalate the complex

### 2. Detect Before They Ask
- Don't wait for frustration
- Recognize signals early
- Proactive handoff > reactive handoff

### 3. Smooth Handoffs Preserve Trust
- Context must transfer
- Customer shouldn't repeat themselves
- Make the human look good

### 4. Learn from Handoffs
- Every handoff is feedback
- Could this have been automated?
- Should this always escalate?

---

## Handoff Triggers

### Explicit Requests

**Clear signals:**
- "Let me talk to a human"
- "Can I speak with someone?"
- "Get me a real person"
- "Transfer me to an agent"
- "I want to talk to a human"

**Implementation:**
- High priority trigger
- Immediate escalation
- Acknowledge the request

**Response:**
"Of course! Let me connect you with someone on our team. Just a moment..."

### Sentiment Triggers

**Negative sentiment signals:**
- ALL CAPS messages
- Profanity
- Escalating frustration
- Repeated complaints

**Threshold approach:**
- Track sentiment over conversation
- Escalate if sentiment drops below threshold
- Escalate if trend is consistently negative

**Response:**
"I can see this is frustrating. Let me get you to someone who can help directly."

### Complexity Triggers

**Complex situations:**
- Technical questions beyond training
- Multi-part problems
- Custom requirements
- Legal or compliance questions
- Pricing negotiations

**Detection:**
- Keywords indicating complexity
- Long messages with multiple issues
- Questions that match "escalate" patterns

### Failure Triggers

**Bot limitations:**
- Unable to understand intent (2+ times)
- Unable to answer question
- Wrong response detected
- Conversation going in circles

**Implementation:**
```
if (clarification_attempts >= 2) {
  escalate("I want to make sure you get the right help.
            Let me connect you with a team member.")
}
```

### Value-Based Triggers

**High-value situations:**
- Large deal size
- Enterprise company
- Urgent timeline
- Competitive situation

**Implementation:**
- Lead score threshold
- Company size threshold
- Explicit high-intent signals
- Strategic account flags

---

## Handoff Detection System

### Rule-Based Detection

**Keyword triggers:**
```
HUMAN_REQUEST:
  - "talk to human"
  - "real person"
  - "agent"
  - "representative"
  - "speak to someone"

FRUSTRATION:
  - "this is ridiculous"
  - "waste of time"
  - "doesn't help"
  - profanity_list
```

**Threshold triggers:**
```
if (messages_without_resolution > 5) → escalate
if (sentiment_score < -0.5) → escalate
if (repeated_question_count >= 2) → escalate
```

### ML-Based Detection

**Features:**
- Message content
- Sentiment scores
- Conversation length
- Response patterns
- User history

**Output:**
- Probability of needing human
- Recommended action
- Urgency level

### Hybrid Approach

**Immediate escalation (rules):**
- Explicit human request
- Severe frustration
- Compliance/legal triggers

**Scored escalation (ML):**
- Accumulating signals
- Predicted dissatisfaction
- Complexity estimation

---

## Handoff Process

### Pre-Handoff

**Acknowledge:**
"I want to make sure you get the best help. Let me connect you with a team member."

**Set expectations:**
"They'll be with you shortly. In the meantime, is there anything else I can note for them?"

**Collect info:**
- Ensure contact information
- Confirm best way to reach
- Note urgency

### Context Transfer

**What to pass:**
- Full conversation transcript
- Customer information
- Detected intent
- Sentiment summary
- Any answers already provided
- Why escalation occurred

**Format:**
```
HANDOFF SUMMARY
Customer: Sarah Johnson, Acme Corp
Channel: Chat → Phone requested
Escalation reason: Complex pricing question

Key points:
- Looking for enterprise pricing
- Has 500+ employees
- Evaluating 3 vendors
- Decision timeline: 2 weeks

Sentiment: Neutral → slightly frustrated at response speed
Questions answered: Product features, basic pricing
Unanswered: Volume discounts, custom integrations
```

### Post-Handoff

**Confirmation:**
"I've sent your information to [Agent name]. They'll be reaching out within [timeframe]."

**If synchronous handoff:**
"[Agent name] is joining now. I've shared our conversation so far."

**Follow-up:**
Track handoff resolution and outcome.

---

## Handoff Routing

### Routing Factors

**Skill-based:**
- Technical questions → Technical rep
- Pricing questions → Sales rep
- Complaints → Support specialist
- Enterprise → Account executive

**Load-based:**
- Available agents
- Queue length
- Estimated wait time

**Relationship-based:**
- Existing account owner
- Previous agent preference
- Geographic alignment

### Routing Logic

```
function routeHandoff(context) {
  // Priority 1: Existing relationship
  if (context.assigned_rep && context.assigned_rep.available) {
    return context.assigned_rep
  }

  // Priority 2: Skill match
  let skill_queue = getSkillQueue(context.escalation_type)
  let available_agents = skill_queue.filter(a => a.available)

  // Priority 3: Load balancing
  if (available_agents.length > 0) {
    return available_agents.sort(by_queue_length)[0]
  }

  // Fallback: Callback queue
  return "callback_queue"
}
```

---

## Handling Unavailability

### No Agents Available

**Response:**
"I don't have anyone available right now, but I want to make sure you get help. Can I have someone call/email you within [timeframe]?"

**Collect:**
- Contact information
- Best time to reach
- Brief summary of need

**Follow-up:**
- Immediate email confirmation
- Ensure callback happens
- Track resolution

### After Hours

**Response:**
"Our team is currently offline (we're available [hours]). Can I have someone reach out first thing tomorrow, or is there something I can help with now?"

**Options:**
- Self-service resources
- FAQ answers
- Callback scheduling
- Emergency escalation (if applicable)

---

## Measuring Handoff Performance

### Key Metrics

**Volume:**
- Handoff rate (% of conversations)
- Handoffs per day/week
- Handoff by trigger type

**Quality:**
- Customer satisfaction post-handoff
- Resolution rate after handoff
- Repeat contact rate

**Efficiency:**
- Time to handoff
- Context transfer completeness
- Agent prep time

### Analyzing Handoffs

**Questions to ask:**
- Which triggers fire most often?
- Are handoffs resolved successfully?
- Could some handoffs be automated?
- Are we escalating too much or too little?

**Improvement loop:**
1. Review handoff transcripts
2. Identify patterns
3. Improve bot to handle more
4. Refine escalation triggers
5. Train humans on common issues

---

## Common Handoff Mistakes

### 1. Escalating Too Late
**Problem:** Customer already frustrated
**Fix:** Detect earlier, lower thresholds

### 2. Escalating Too Early
**Problem:** Overwhelming human team
**Fix:** Improve bot capabilities, raise thresholds carefully

### 3. Poor Context Transfer
**Problem:** Customer repeats themselves
**Fix:** Transfer full conversation, summarize key points

### 4. No Acknowledgment
**Problem:** Customer unsure what's happening
**Fix:** Clear communication about handoff process

### 5. No Follow-Through
**Problem:** Handoff falls through the cracks
**Fix:** Queue management, tracking, accountability

---

## Implementation Checklist

### Phase 1: Basic Handoff
- [ ] Explicit human request detection
- [ ] Basic routing to available agent
- [ ] Conversation transcript transfer
- [ ] Confirmation message

### Phase 2: Smart Handoff
- [ ] Sentiment-based triggers
- [ ] Complexity detection
- [ ] Skill-based routing
- [ ] Context summarization

### Phase 3: Optimized Handoff
- [ ] ML-based prediction
- [ ] Value-based prioritization
- [ ] Performance analytics
- [ ] Continuous improvement loop

---

## Questions to Ask

If you need more context:
1. What triggers handoffs to humans today?
2. What human resources are available for handoffs?
3. What's your current handoff rate?
4. How do customers react to handoffs?
5. What information do humans need to take over effectively?

---

## Related Skills

- **sentiment-analysis**: For detecting frustration
- **intent-detection**: For identifying complex requests
- **conversational-flow-management**: For smooth transitions
- **compliance-handling**: For required escalations
