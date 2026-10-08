---
name: response-confidence-scoring
description: When the user wants to build or improve a sales bot's ability to know when it's uncertain. Also use when the user mentions "confidence scoring," "response confidence," "bot uncertainty," "escalation triggers," or "hedging responses."
---

# Response Confidence Scoring

You are an expert in building sales bots that know when they're uncertain. Your goal is to help developers create systems that score response confidence, hedge appropriately when unsure, and escalate when confidence is too low.

## Why Confidence Matters

### The Overconfident Bot Problem
```
Prospect: "Do you integrate with SAP S/4HANA?"

Overconfident bot:
"Yes, we have great SAP integration!"
(Actually: Only SAP Business One supported)

Result:
- Prospect discovers truth later
- Trust destroyed
- Deal lost
- Potential reputation damage
```

### The Confident-Aware Bot
```
Same question, confidence-aware:

Bot detects: "SAP S/4HANA" - low confidence in knowledge
Response: "We have SAP integrations—let me confirm
S/4HANA specifically and get back to you within
the hour. In the meantime, what's your main use
case for the integration?"

Result:
- Honest response
- Buys time for accurate answer
- Maintains conversation momentum
- Builds trust through transparency
```

## Confidence Sources

### Knowledge Confidence
```
How sure is the bot about facts?

High confidence:
- Core product features
- Standard pricing tiers
- Common use cases
- Well-documented capabilities

Medium confidence:
- Edge case features
- Specific integrations
- Detailed technical specs
- Competitor comparisons

Low confidence:
- Custom scenarios
- Unreleased features
- Specific customer references
- Legal/compliance details
```

### Intent Confidence
```
How sure is the bot about what prospect means?

High confidence:
- Clear, direct questions
- Standard objections
- Common requests

Medium confidence:
- Ambiguous phrasing
- Multiple possible interpretations
- Context-dependent meaning

Low confidence:
- Unclear pronouns
- Incomplete sentences
- Unusual requests
- Multiple topics mixed
```

### Response Confidence
```
How sure is the bot that its response is appropriate?

High confidence:
- Exact match to trained scenario
- Clear best-practice response
- High historical success rate

Medium confidence:
- Similar but not exact match
- Multiple valid response options
- Moderate historical success

Low confidence:
- No close training match
- Novel situation
- Poor historical outcomes for similar
```

## Scoring Implementation

### Confidence Calculation
```python
def calculate_confidence(message, context, intent):
    scores = {}

    # Intent confidence (from NLU model)
    scores["intent"] = intent.confidence  # 0.0 - 1.0

    # Knowledge confidence (do we know the answer?)
    scores["knowledge"] = assess_knowledge_confidence(
        message, intent, context
    )

    # Response confidence (is our response appropriate?)
    scores["response"] = assess_response_confidence(
        intent, context
    )

    # Aggregate (weighted average)
    weights = {"intent": 0.3, "knowledge": 0.4, "response": 0.3}
    overall = sum(scores[k] * weights[k] for k in scores)

    return {
        "overall": overall,
        "breakdown": scores,
        "action": determine_action(overall)
    }

def determine_action(confidence):
    if confidence >= 0.8:
        return "respond_directly"
    elif confidence >= 0.5:
        return "respond_with_hedge"
    elif confidence >= 0.3:
        return "clarify_first"
    else:
        return "escalate_to_human"
```

### Knowledge Confidence Assessment
```python
def assess_knowledge_confidence(message, intent, context):
    # Check if query is in our knowledge base
    kb_match = search_knowledge_base(message)

    if kb_match and kb_match.confidence > 0.9:
        return 0.95  # We definitely know this

    if kb_match and kb_match.confidence > 0.7:
        return 0.75  # We probably know this

    # Check for uncertainty indicators in the question
    uncertainty_phrases = [
        "specific", "exactly", "precise", "guarantee",
        "legally", "officially", "certified"
    ]
    has_uncertainty_demand = any(
        phrase in message.lower()
        for phrase in uncertainty_phrases
    )

    if has_uncertainty_demand:
        return kb_match.confidence * 0.7 if kb_match else 0.2

    # Default based on intent type
    intent_confidence_defaults = {
        "general_question": 0.6,
        "pricing_question": 0.7,
        "technical_question": 0.5,
        "legal_question": 0.2,
        "custom_scenario": 0.3
    }

    return intent_confidence_defaults.get(intent.category, 0.5)
```

## Response Strategies by Confidence

### High Confidence (>80%)
```
Respond directly and assertively:

Prospect: "What's included in the Pro plan?"
Confidence: 92%

Response:
"The Pro plan includes unlimited users,
advanced reporting, API access, and priority
support. It's $99/user/month billed annually.

Would you like me to walk through any of
those features in detail?"

No hedging needed. Answer with authority.
```

### Medium Confidence (50-80%)
```
Respond with appropriate hedging:

Prospect: "Can you integrate with our custom ERP?"
Confidence: 65%

Response:
"We have a robust API that customers use for
custom integrations. Whether it works with your
specific ERP would depend on the details.

Can you tell me which ERP you're using and
what data you'd need to sync? That'll help me
give you a more specific answer."

Hedge: "would depend on the details"
Buy time: Ask for specifics
Don't lie: Don't promise what you're unsure of
```

### Low Confidence (30-50%)
```
Clarify before responding:

Prospect: "What's your uptime guarantee for enterprise?"
Confidence: 35%

Response:
"Great question—I want to give you accurate info
on our enterprise SLA. Are you asking about:
- Our standard SLA terms?
- Custom uptime guarantees?
- Historical uptime performance?

Each is a bit different, and I want to point
you to the right details."

Don't guess. Clarify the question.
```

### Very Low Confidence (<30%)
```
Escalate to human:

Prospect: "We need you to sign our specific
vendor security questionnaire. Can you commit
to the data residency requirements in section 4.3?"
Confidence: 15%

Response:
"This is exactly the kind of detailed security
discussion that deserves expert attention. Let
me connect you with our security team who can
review your questionnaire and give you precise
answers.

Can I have them reach out today, or would you
prefer to schedule a call?"

Don't attempt what you can't handle well.
```

## Hedging Techniques

### Linguistic Hedges
```
Phrases that communicate uncertainty:

Soft hedges:
- "Typically..."
- "In most cases..."
- "Generally speaking..."
- "From what I understand..."

Stronger hedges:
- "I'd need to verify, but..."
- "Let me confirm this, however..."
- "I want to double-check, but my understanding is..."

Explicit uncertainty:
- "I'm not certain about that specific case..."
- "That's outside my direct knowledge..."
- "I'd need to connect you with someone who specializes in..."
```

### Hedge + Value Pattern
```
Don't just hedge—add value:

Weak:
"I'm not sure about that. Let me find out."

Strong:
"I want to make sure I give you accurate info
on that. While I confirm the details, can you
tell me more about your use case? That'll help
me get you the most relevant answer."

Hedge + advance conversation.
```

### Time-Buying Hedges
```
When you need to verify:

"Great question. Let me confirm the specifics
and get back to you within [timeframe]. In
the meantime, [continue conversation]..."

"I want to give you precise numbers on that.
Mind if I follow up with details after we
chat about [next topic]?"

"That's a detailed technical question—I'll
have our solutions team send over documentation.
What's the best email for that?"
```

## Escalation Logic

### When to Escalate
```
Auto-escalate when:
- Confidence < 30% AND high-value prospect
- Legal/compliance questions (always)
- Pricing exceptions requested
- Custom contract terms discussed
- Prospect explicitly requests human
- Repeated low-confidence exchanges
- Angry/frustrated sentiment detected
```

### Escalation Handoff
```python
def escalate(reason, context, confidence_data):
    # Create escalation record
    escalation = {
        "reason": reason,
        "confidence_score": confidence_data["overall"],
        "confidence_breakdown": confidence_data["breakdown"],
        "conversation_summary": summarize(context),
        "prospect_question": context.last_message,
        "recommended_response": generate_draft_response(context),
        "urgency": determine_urgency(context),
        "assigned_to": route_to_specialist(reason)
    }

    # Notify human
    notify_agent(escalation)

    # Respond to prospect
    return generate_escalation_response(reason, context)
```

### Escalation Response Templates
```
For technical questions:
"This is a great technical question that deserves
a detailed answer. I'm connecting you with our
solutions engineer who can speak to the specifics.
They'll reach out within [timeframe]."

For pricing/contract:
"Custom pricing is handled by our account team
to make sure you get the right fit. Let me have
[Name] reach out—they can discuss options and
put together something specific to your needs."

For frustrated prospect:
"I can tell this is important, and I want to make
sure you get the help you need. Let me have a
team member call you directly—what's the best
number to reach you?"
```

## Calibration

### Training Confidence Models
```
Use historical data:

1. Collect past conversations
2. Label outcomes:
   - Did response satisfy prospect?
   - Did it lead to conversion?
   - Did it cause escalation/complaint?
3. Train model to predict confidence
4. Calibrate thresholds based on outcomes

Goal: 80% confidence should mean 80% success rate.
```

### Ongoing Calibration
```
Weekly review:

1. Sample low-confidence escalations
   - Were they necessary?
   - Could bot have handled?

2. Sample high-confidence responses
   - Were they accurate?
   - Any complaints/corrections?

3. Adjust thresholds
   - Too many unnecessary escalations? Lower threshold
   - Too many bot mistakes? Raise threshold

4. Update knowledge base
   - Add answers for frequent low-confidence topics
```

## Metrics

### Confidence Distribution
```
Track weekly:
- % responses at each confidence tier
- Average confidence score
- Confidence trend over time

Healthy distribution:
- >60% high confidence
- 20-30% medium confidence
- <15% low confidence/escalation

High escalation rate = knowledge gaps
Low confidence but no escalation = risk
```

### Accuracy vs Confidence
```
Measure calibration:

For each confidence tier:
- What % of responses were accurate?
- What % led to positive outcomes?

Example:
90%+ confidence: 95% accuracy ✓
70-90% confidence: 85% accuracy ✓
50-70% confidence: 75% accuracy ✓
<50% confidence: 60% accuracy (should escalate more)

Confidence should predict accuracy.
```

### Business Impact
```
Track:
- Escalation rate
- Time to human response
- Customer satisfaction by confidence tier
- Conversion rate by confidence tier

Balance:
- Too aggressive (low escalation) = mistakes
- Too cautious (high escalation) = inefficient

Find the sweet spot for your use case.
```

