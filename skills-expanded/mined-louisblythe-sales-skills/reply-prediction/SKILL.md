---
name: reply-prediction
description: When the user wants to build or improve a sales bot's ability to anticipate likely responses. Also use when the user mentions "reply prediction," "response anticipation," "conversation prediction," "next response," or "predictive replies."
---

# Reply Prediction

You are an expert in building sales bots that anticipate likely prospect responses and pre-load appropriate follow-ups. Your goal is to help developers create systems that predict responses and prepare intelligent replies in advance.

## Why Reply Prediction Matters

### The Reactive Problem
```
Traditional approach:
1. Bot sends message
2. Waits for response
3. Analyzes response
4. Generates reply
5. Sends reply

Time to reply: Seconds to minutes
Quality: Variable, sometimes off-target
```

### Predictive Approach
```
Predictive approach:
1. Bot sends message
2. Predicts likely responses
3. Pre-generates replies for each
4. Response arrives
5. Matches to prediction
6. Sends pre-optimized reply

Time to reply: Near-instant
Quality: Pre-reviewed, consistent
```

## Prediction Categories

### Response Type Predictions
```
For any given message, predict likelihood of:

Positive responses:
- "Yes, I'm interested"
- "Tell me more"
- "Let's schedule a call"

Neutral responses:
- "What exactly do you do?"
- "How is this different from X?"
- "I need to check with my team"

Negative responses:
- "Not interested"
- "We already have a solution"
- "Bad timing"

No response:
- Probability of no reply
```

### Content Predictions
```
Predict specific content:

Questions likely to be asked:
- Pricing questions
- Feature questions
- Comparison questions
- Implementation questions

Objections likely to be raised:
- Budget concerns
- Timing concerns
- Authority concerns
- Competitor mentions

Information likely to be shared:
- Company details
- Pain point specifics
- Timeline information
```

## Prediction Implementation

### Probability Model
```python
class ReplyPredictor:
    def __init__(self, model):
        self.model = model
        self.predictions = {}

    def predict_responses(self, context):
        """Generate probability distribution of likely responses"""

        features = extract_features(context)

        predictions = {
            "positive_interest": 0,
            "question_pricing": 0,
            "question_features": 0,
            "question_comparison": 0,
            "objection_timing": 0,
            "objection_budget": 0,
            "objection_competitor": 0,
            "not_interested": 0,
            "no_response": 0
        }

        # Use model to predict probabilities
        probabilities = self.model.predict_proba(features)

        for response_type, prob in zip(self.model.classes_, probabilities):
            predictions[response_type] = prob

        return predictions

    def get_top_predictions(self, context, n=3):
        all_predictions = self.predict_responses(context)
        sorted_predictions = sorted(
            all_predictions.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_predictions[:n]
```

### Historical Pattern Analysis
```python
def predict_from_history(message_template, prospect_segment):
    """Predict based on historical response patterns"""

    # Get historical responses to this template
    historical = get_historical_responses(
        template_id=message_template.id,
        segment=prospect_segment
    )

    # Calculate response distribution
    response_counts = Counter([r.response_type for r in historical])
    total = len(historical)

    predictions = {}
    for response_type, count in response_counts.items():
        predictions[response_type] = count / total

    # Get common response content
    content_patterns = extract_common_content(historical)

    return {
        "type_probabilities": predictions,
        "content_patterns": content_patterns,
        "sample_size": total
    }
```

### Context-Aware Prediction
```python
def predict_with_context(context):
    """Adjust predictions based on conversation context"""

    base_predictions = predict_from_history(
        context.last_message.template,
        context.prospect.segment
    )

    # Adjust for conversation stage
    stage_adjustments = {
        "discovery": {"question_features": 0.2, "not_interested": -0.1},
        "evaluation": {"question_pricing": 0.3, "question_comparison": 0.2},
        "proposal": {"objection_budget": 0.2, "positive_interest": 0.1},
        "negotiation": {"objection_budget": 0.3, "positive_interest": 0.2}
    }

    adjustments = stage_adjustments.get(context.stage, {})
    adjusted = apply_adjustments(base_predictions, adjustments)

    # Adjust for prospect engagement
    if context.prospect.engagement_score > 70:
        adjusted["positive_interest"] *= 1.3
        adjusted["not_interested"] *= 0.5

    # Adjust for recent behavior
    if context.prospect.asked_pricing_before:
        adjusted["question_pricing"] *= 1.5

    return adjusted
```

## Pre-Generated Replies

### Reply Templates by Prediction
```python
PREDICTED_REPLY_TEMPLATES = {
    "positive_interest": {
        "replies": [
            "Great! What specifically caught your attention?",
            "Glad to hear it. Would a quick call or more info be more helpful right now?"
        ],
        "next_action": "advance_to_meeting"
    },
    "question_pricing": {
        "replies": [
            "Happy to walk through pricing. To give you accurate info, can I ask a few questions about your team size and needs?",
            "Pricing depends on a few factors. What's your team size, and what's most important to you in a solution?"
        ],
        "next_action": "qualify_then_price"
    },
    "question_comparison": {
        "replies": [
            "Good question—here's how we're different: [comparison points]. What matters most to you?",
            "We get asked that a lot. The main difference is [key differentiator]. What's driving the comparison?"
        ],
        "next_action": "understand_evaluation"
    },
    "objection_timing": {
        "replies": [
            "Totally understand—when would be a better time to revisit this?",
            "Makes sense. If I check back in [timeframe], would that work better?"
        ],
        "next_action": "schedule_future_outreach"
    },
    "not_interested": {
        "replies": [
            "No problem. Mind if I ask what's not a fit? Helps me know if I should reach out again in the future.",
            "Understood. If anything changes, feel free to reach out. Best of luck!"
        ],
        "next_action": "disqualify_or_nurture"
    }
}
```

### Dynamic Reply Selection
```python
def select_preloaded_reply(actual_response, predictions, context):
    """Match actual response to predictions and select reply"""

    # Classify actual response
    response_type = classify_response(actual_response)

    # Check if we predicted this
    if response_type in predictions and predictions[response_type] > 0.1:
        # Use preloaded reply
        template = PREDICTED_REPLY_TEMPLATES.get(response_type)
        if template:
            reply = select_best_reply(template["replies"], context)
            return {
                "reply": reply,
                "source": "predicted",
                "confidence": predictions[response_type]
            }

    # Fall back to real-time generation
    return {
        "reply": generate_reply_realtime(actual_response, context),
        "source": "generated",
        "confidence": None
    }
```

## Prediction Caching

### Pre-Computation
```python
def precompute_replies(conversation):
    """Precompute replies before response arrives"""

    # Get predictions
    predictions = predict_responses(conversation.context)
    top_predictions = get_top_predictions(predictions, n=5)

    # Generate and cache replies
    cached_replies = {}
    for response_type, probability in top_predictions:
        if probability > 0.05:  # Only cache if >5% probability
            template = PREDICTED_REPLY_TEMPLATES.get(response_type)
            if template:
                reply = personalize_reply(
                    template["replies"],
                    conversation.prospect
                )
                cached_replies[response_type] = {
                    "reply": reply,
                    "probability": probability,
                    "generated_at": datetime.now()
                }

    # Store in cache
    cache_key = f"replies:{conversation.id}"
    cache.set(cache_key, cached_replies, ttl=3600)

    return cached_replies
```

### Cache Retrieval
```python
def get_reply_for_response(conversation_id, actual_response):
    """Retrieve cached reply if available"""

    cache_key = f"replies:{conversation_id}"
    cached = cache.get(cache_key)

    if not cached:
        return None

    # Match response to cached predictions
    response_type = classify_response(actual_response)

    if response_type in cached:
        return cached[response_type]

    return None
```

## Learning & Improvement

### Prediction Accuracy Tracking
```python
def track_prediction_accuracy(conversation_id, predicted, actual):
    """Track how accurate predictions were"""

    log_prediction_result(
        conversation_id=conversation_id,
        predicted_type=max(predicted, key=predicted.get),
        predicted_probability=max(predicted.values()),
        actual_type=actual,
        correct=actual == max(predicted, key=predicted.get)
    )

    # Update model if enough data
    if should_retrain_model():
        retrain_prediction_model()
```

### Feedback Loop
```python
def improve_predictions(results):
    """Use outcomes to improve prediction model"""

    for result in results:
        # Was predicted reply effective?
        if result["source"] == "predicted":
            effectiveness = measure_reply_effectiveness(result)

            if effectiveness < THRESHOLD:
                # Flag reply for review
                flag_for_review(
                    response_type=result["response_type"],
                    reply=result["reply"],
                    effectiveness=effectiveness
                )

    # Aggregate learnings
    improvement_suggestions = analyze_prediction_patterns(results)
    return improvement_suggestions
```

## Metrics

### Prediction Quality
```
Track:
- Prediction accuracy (did we predict right type?)
- Reply match rate (how often was cached reply used?)
- Response time improvement
- Reply effectiveness by source (predicted vs generated)

Optimize:
- Which responses are predictable?
- Where do we need better predictions?
- Which templates perform best?
```

