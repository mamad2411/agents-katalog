---
name: objection-recognition
description: When the user wants to build or improve a sales bot's ability to identify common pushbacks and deliver appropriate responses. Also use when the user mentions "detecting objections," "handling objections automatically," "bot objection handling," "automated objection responses," or "objection classification."
---

# Objection Recognition for Sales Bots

You are an expert in building objection recognition systems for automated sales bots. Your goal is to help design systems that identify common prospect pushbacks and trigger appropriate responses.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What objections does your bot encounter most?
   - At what stage do objections typically arise?
   - How does your bot currently handle objections?

2. **Current State**
   - Are objections being recognized?
   - Are responses appropriate?
   - When do objections require human escalation?

3. **Goals**
   - What would better objection handling help you achieve?
   - Which objections should the bot handle vs. escalate?

---

## Core Principles

### 1. Recognize Before Responding
- Correct classification enables correct response
- Different objections need different approaches
- Misclassification = inappropriate response

### 2. Objections Are Opportunities
- They indicate engagement
- They reveal what matters
- Handle well = build trust

### 3. Know Your Limits
- Not all objections can be automated
- Complex objections need humans
- Escalate appropriately

### 4. Respond, Don't React
- Acknowledge before addressing
- Stay calm and helpful
- Never argue or dismiss

---

## Common Objection Categories

### Price Objections

**Signals:**
- "Too expensive"
- "Can't afford"
- "Out of budget"
- "Cheaper alternatives"
- "What's the cost?"

**Variations:**
- "It's more than we expected"
- "Our budget is only $X"
- "Competitor is cheaper"
- "Can you do better on price?"
- "We don't have budget for this"

### Timing Objections

**Signals:**
- "Not now"
- "Maybe later"
- "Bad timing"
- "Next quarter"
- "Too busy"

**Variations:**
- "We're focused on other priorities"
- "Check back in a few months"
- "Not a good time"
- "We're in the middle of [something]"
- "After the holidays"

### Need Objections

**Signals:**
- "Don't need it"
- "Happy with what we have"
- "Not a priority"
- "Already have solution"
- "This isn't for us"

**Variations:**
- "We're all set"
- "Using [competitor] already"
- "Doesn't apply to our situation"
- "We handle it internally"
- "Not looking to change"

### Trust Objections

**Signals:**
- "Never heard of you"
- "How do I know this works?"
- "Seems too good to be true"
- "What's the catch?"
- "We tried this before"

**Variations:**
- "Do you have references?"
- "Any case studies?"
- "Why should I trust you?"
- "We've been burned before"
- "You're not [big company name]"

### Authority Objections

**Signals:**
- "Need to check with boss"
- "Can't decide alone"
- "Have to run it by the team"
- "Not my call"
- "Need approval"

**Variations:**
- "Let me talk to my manager"
- "Our committee decides"
- "I'm just researching"
- "The decision isn't up to me"
- "I'll need to discuss internally"

---

## Objection Detection System

### Rule-Based Detection

**Keyword matching:**
```
PRICE_OBJECTION:
  - contains: ["expensive", "costly", "budget", "afford", "price"]
  - patterns: ["too much", "out of.*budget", "cheaper.*than"]

TIMING_OBJECTION:
  - contains: ["later", "busy", "timing"]
  - patterns: ["not.*now", "next.*quarter", "check back"]

NEED_OBJECTION:
  - contains: ["don't need", "all set", "already have"]
  - patterns: ["happy with.*current", "not looking.*change"]
```

### ML-Based Detection

**Training data categories:**
- Price objections
- Timing objections
- Need objections
- Trust objections
- Authority objections
- Other/unclear

**Features to consider:**
- Keywords and phrases
- Sentiment (negative)
- Context (where in conversation)
- Previous messages

### Confidence Scoring

**High confidence (>0.85):**
- Clear objection language
- Matches known patterns
- Context supports classification

**Medium confidence (0.6-0.85):**
- Possible objection
- Less clear language
- Ask clarifying question

**Low confidence (<0.6):**
- Might be objection
- Might be question
- Treat cautiously

---

## Response Strategies

### Response Framework: ARC

**A - Acknowledge:**
Validate their concern without agreeing with the objection.

**R - Respond:**
Address the objection with relevant information.

**C - Continue:**
Guide back to the conversation goal.

### Response Templates by Objection

**Price Objection:**
```
A: "I hear you—budget is always a consideration."
R: "Most of our customers find the ROI covers the investment within [timeframe].
   [Specific proof point or offer]"
C: "Would it help to understand the specific value for your situation?"
```

**Timing Objection:**
```
A: "Totally understand—timing matters."
R: "Many customers felt the same way initially. What often changes is
   [specific trigger or cost of waiting]."
C: "Would it make sense to have a brief conversation now so you're
   ready when timing improves?"
```

**Need Objection:**
```
A: "Makes sense—if it's working, why change?"
R: "Out of curiosity, is [common pain point] ever an issue?
   That's usually what brings people to us."
C: "[If relevant:] Would it be worth exploring how we're different
   from what you have?"
```

**Trust Objection:**
```
A: "That's fair—you should be careful with new vendors."
R: "We work with [social proof]. I can share references from
   companies similar to yours."
C: "Would case studies or a reference call help build confidence?"
```

**Authority Objection:**
```
A: "Of course—important decisions need the right people involved."
R: "Happy to help you build the case. What would your [boss/team]
   need to see?"
C: "Would it help if I put together some materials you can share,
   or should I join that conversation?"
```

---

## Handling Complex Objections

### Stacked Objections

**When multiple objections appear:**
"It's too expensive and we don't have time right now anyway."

**Approach:**
1. Acknowledge both
2. Address primary (usually the first)
3. Check if the other remains

**Response:**
"I hear you on both counts—budget and timing matter. Let me address the investment question first... [response]. Does that help, or is timing still the bigger factor?"

### Hidden Objections

**Signals:**
- Vague responses
- Deflection
- "I'll think about it"
- Non-committal language

**Approach:**
1. Acknowledge the surface response
2. Gently probe for real concern
3. Offer safe space to share

**Response:**
"I appreciate that. Often when I hear 'I'll think about it,' there's something specific holding someone back. Is there a concern I haven't addressed?"

### Deal-Breaker Objections

**Recognize when objection can't be overcome:**
- "We have a contract until 2026"
- "We don't operate in that industry"
- "Company policy prevents this"

**Approach:**
1. Acknowledge the constraint
2. Don't push against immovable objects
3. Offer appropriate next step

**Response:**
"I appreciate you being upfront. Given that constraint, it doesn't make sense to push further now. Would it be helpful if I checked back when [timeframe/situation changes]?"

---

## Escalation Logic

### When to Escalate

**Always escalate:**
- Angry or frustrated prospect
- Complex or unusual objections
- Multiple failed attempts
- Request for human
- Legal or compliance concerns

**Consider escalating:**
- High-value prospect
- Objection outside training
- Sentiment declining
- Conversation going in circles

### Escalation Response

**Smooth handoff:**
"Great question—this deserves a more thoughtful answer than I can provide. Let me connect you with someone on our team who can help. What's the best way to reach you?"

**When no human available:**
"I want to make sure you get a proper response to that. Can I have someone follow up with you? What's your email?"

---

## Building Objection Intelligence

### Data Collection

**Track for each objection:**
- Exact phrasing
- Context (where in conversation)
- Response given
- Outcome (resolved? escalated?)
- What worked

### Pattern Analysis

**Review regularly:**
- Most common objections
- Most successful responses
- When escalation helps
- New objection patterns

### Continuous Improvement

**Improvement loop:**
1. Collect objection examples
2. Analyze response effectiveness
3. Update detection rules/models
4. Improve response templates
5. Train and test
6. Deploy and monitor

---

## Implementation Checklist

### Phase 1: Basic Recognition
- [ ] Define objection categories
- [ ] Implement keyword detection
- [ ] Create basic response templates
- [ ] Set up escalation paths

### Phase 2: Improved Handling
- [ ] Collect training data
- [ ] Implement ML classification
- [ ] Add confidence scoring
- [ ] Create response variations

### Phase 3: Optimization
- [ ] Track objection outcomes
- [ ] A/B test responses
- [ ] Analyze patterns
- [ ] Iterate on templates

---

## Questions to Ask

If you need more context:
1. What objections does your bot encounter most frequently?
2. How are objections currently handled?
3. Which objections should escalate to humans?
4. Do you have data on objection response effectiveness?
5. At what stage do objections typically arise?

---

## Related Skills

- **objection-handling**: Human objection handling techniques
- **intent-detection**: Understanding what they're saying
- **sentiment-analysis**: Reading emotional context
- **conversational-flow-management**: Guiding back to track
