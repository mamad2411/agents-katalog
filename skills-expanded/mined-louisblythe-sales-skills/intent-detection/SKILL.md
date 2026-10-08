---
name: intent-detection
description: When the user wants to build or improve an automated sales bot's ability to recognize prospect intent—whether they're interested, objecting, asking questions, or ready to buy. Also use when the user mentions "detecting intent," "classifying responses," "understanding prospect replies," "bot understanding," or "NLP for sales."
---

# Intent Detection for Sales Bots

You are an expert in building intent detection systems for automated sales bots. Your goal is to help design systems that accurately recognize whether a prospect is interested, objecting, asking a question, or expressing other intents.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What channels does your bot operate on? (SMS, email, chat, voice)
   - What is the bot's primary goal? (qualify leads, book meetings, nurture)
   - What CRM/tools are you using?

2. **Current State**
   - Do you have an existing intent detection system?
   - What intents are you trying to detect?
   - What's your current accuracy rate?

3. **Goals**
   - What would better intent detection help you achieve?
   - Where are misclassifications causing problems?

---

## Core Principles

### 1. Intent Drives Response
- Correct intent detection enables appropriate responses
- Wrong intent = wrong response = lost opportunity
- This is the foundation of bot intelligence

### 2. Real-World Language is Messy
- People don't speak in clean categories
- Multiple intents in one message
- Context changes meaning

### 3. Confidence Thresholds Matter
- Not all classifications are equal
- Low confidence should trigger fallbacks
- When unsure, escalate or ask

### 4. Continuous Improvement
- Intent models degrade without maintenance
- New patterns emerge constantly
- Learn from misclassifications

---

## Common Sales Intents

### Positive Intents

**Interested:**
- "Tell me more"
- "That sounds interesting"
- "How does it work?"
- "Send me info"

**Ready to Buy:**
- "I'd like to move forward"
- "How do I sign up?"
- "What are the next steps?"
- "Send me a contract"

**Meeting Request:**
- "Can we schedule a call?"
- "I'm free Tuesday"
- "Let's set up a demo"
- "I'd like to discuss further"

### Negative Intents

**Not Interested:**
- "Not interested"
- "We're all set"
- "Remove me from your list"
- "No thanks"

**Opt-Out:**
- "Stop"
- "Unsubscribe"
- "Don't contact me again"
- "STOP" (SMS compliance)

**Wrong Person:**
- "I don't handle this"
- "You have the wrong number"
- "This isn't my area"
- "Try someone else"

### Neutral/Information Intents

**Question:**
- "What does it cost?"
- "How long does implementation take?"
- "Do you integrate with X?"
- "What's included?"

**Objection:**
- "It's too expensive"
- "We already have a solution"
- "Not the right time"
- "Need to talk to my boss"

**Request for Information:**
- "Send me a case study"
- "Do you have references?"
- "Can I see a demo?"
- "What industries do you work with?"

### Context-Dependent Intents

**Timing-Related:**
- "Maybe later"
- "Reach out next quarter"
- "Not now but stay in touch"
- "Check back in 3 months"

**Delegation:**
- "Talk to my colleague"
- "CC my assistant"
- "You should speak with [name]"
- "Let me introduce you to..."

---

## Building Intent Classification

### Approach 1: Rule-Based

**How it works:**
- Define keywords/phrases per intent
- Match incoming message to rules
- Simple, transparent, maintainable

**Example rules:**
```
INTERESTED:
  - contains: ["interested", "tell me more", "sounds good", "learn more"]

NOT_INTERESTED:
  - contains: ["not interested", "no thanks", "pass", "all set"]

OPT_OUT:
  - exact: ["stop", "unsubscribe", "remove"]
  - contains: ["stop texting", "stop calling", "remove me"]
```

**Pros:**
- Easy to implement and debug
- No training data needed
- Fully transparent

**Cons:**
- Misses variations
- Doesn't handle nuance
- Requires constant updating

### Approach 2: ML-Based

**How it works:**
- Train classifier on labeled examples
- Model learns patterns
- Generalizes to new variations

**Common approaches:**
- Traditional ML (Naive Bayes, SVM)
- Deep learning (BERT, transformers)
- API-based (OpenAI, Claude, etc.)

**Pros:**
- Handles variation better
- Can detect nuance
- Improves with data

**Cons:**
- Requires training data
- Less transparent
- Can have surprising failures

### Approach 3: Hybrid

**Best of both worlds:**
- Rules for clear-cut cases (opt-out, explicit interest)
- ML for nuanced cases (soft objections, implied interest)
- Confidence thresholds for escalation

**Example flow:**
```
1. Check compliance rules first (OPT_OUT keywords)
2. Check explicit intent rules
3. If no rule match, run ML classification
4. If ML confidence < threshold, flag for human review
```

---

## Intent Detection Architecture

### Message Processing Flow

```
Incoming Message
       ↓
  Preprocessing (normalize, clean)
       ↓
  Rule-Based Check (compliance, explicit)
       ↓
  ML Classification (nuanced intents)
       ↓
  Confidence Check
       ↓
  High Confidence → Automated Response
  Low Confidence → Human Review or Clarifying Question
```

### Key Components

**Preprocessor:**
- Normalize text (lowercase, remove special chars)
- Handle SMS shorthand
- Expand contractions
- Remove noise

**Rule Engine:**
- Keyword matching
- Regex patterns
- Priority ordering

**ML Classifier:**
- Feature extraction
- Intent prediction
- Confidence scoring

**Post-Processor:**
- Confidence thresholds
- Multi-intent handling
- Escalation logic

---

## Handling Complexity

### Multiple Intents

**Example message:**
"I'm interested but we don't have budget until Q2—can you send pricing info?"

**Intents present:**
- Interested
- Timing objection
- Information request

**Approach:**
- Detect all intents
- Prioritize response based on hierarchy
- Address most important/actionable intent
- Acknowledge others

### Ambiguous Messages

**Example:**
"Maybe"
"Let me think about it"
"Interesting"

**Approach:**
- Lower confidence score
- Ask clarifying question
- Or trigger follow-up sequence
- Track for pattern analysis

### Context-Dependent Intent

**Same message, different intent:**
- "What's the cost?" (after demo = buying signal)
- "What's the cost?" (first touch = information seeking)

**Approach:**
- Include conversation context in classification
- Different models/rules for different stages
- Track conversation state

---

## Confidence and Fallbacks

### Setting Confidence Thresholds

**High confidence (>0.85):**
- Automated response
- Move to next step

**Medium confidence (0.6-0.85):**
- Automated response with softer language
- Flag for review if response fails

**Low confidence (<0.6):**
- Clarifying question
- Human escalation
- Safe fallback response

### Fallback Strategies

**Clarifying question:**
"I want to make sure I understand—are you interested in learning more, or would you prefer I reach out another time?"

**Safe acknowledgment:**
"Thanks for your response! Let me get back to you with the right information."

**Human escalation:**
"Great question—let me have a team member follow up with you directly."

---

## Compliance Considerations

### Must-Detect Intents

**SMS (TCPA/ACMA):**
- STOP, UNSUBSCRIBE, CANCEL, END, QUIT
- Must detect immediately
- Must act immediately (no more messages)

**Email (CAN-SPAM/GDPR):**
- Unsubscribe requests
- Data deletion requests
- Must honor within timeframe

### Implementation

**Priority 1 rules:**
```
OPT_OUT (immediate action, no exceptions):
  - STOP
  - UNSUBSCRIBE
  - REMOVE
  - CANCEL
  - Any message containing "stop texting"
```

These rules should fire BEFORE any other processing.

---

## Testing and Improvement

### Measuring Performance

**Accuracy metrics:**
- Precision (of predicted intents, % correct)
- Recall (of actual intents, % detected)
- F1 score (balance of both)
- Confusion matrix (which intents get mixed up)

**Business metrics:**
- Response appropriateness rate
- Escalation rate
- Conversion by detected intent
- Customer satisfaction

### Building Test Sets

**Collect real examples:**
- Sample from actual conversations
- Label manually
- Include edge cases

**Test set categories:**
- Clear intent (should get right)
- Ambiguous intent (may need clarification)
- Multi-intent (detect all)
- Edge cases (unusual phrasing)

### Continuous Improvement

**Regular reviews:**
- Sample misclassifications weekly
- Identify patterns
- Update rules or retrain models

**Feedback loops:**
- Track when bot responses fail
- Correlate with intent detection
- Fix root causes

---

## Implementation Checklist

### Phase 1: Foundation
- [ ] Define intent taxonomy
- [ ] Set up compliance rules (opt-out)
- [ ] Implement basic rule matching
- [ ] Create fallback responses

### Phase 2: Enhancement
- [ ] Collect training data
- [ ] Implement ML classification
- [ ] Set confidence thresholds
- [ ] Build escalation logic

### Phase 3: Optimization
- [ ] Implement multi-intent detection
- [ ] Add context awareness
- [ ] Build feedback loop
- [ ] Monitor and improve

---

## Questions to Ask

If you need more context:
1. What channels does your bot operate on?
2. What are the most important intents to detect?
3. Do you have labeled training data?
4. What's your current accuracy?
5. Where are misclassifications causing the biggest problems?

---

## Related Skills

- **sentiment-analysis**: For understanding emotional tone
- **conversational-flow-management**: For responding appropriately
- **objection-recognition**: For detecting specific objection types
- **compliance-handling**: For regulatory requirements
