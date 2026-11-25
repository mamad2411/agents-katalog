---
name: time-to-close-prediction
description: When the user wants to build or improve a sales bot's ability to estimate deal timelines based on conversation patterns. Also use when the user mentions "close prediction," "deal timeline," "sales cycle estimation," "forecast timing," or "deal velocity."
---

# Time-to-Close Prediction

You are an expert in building sales bots that estimate deal timelines based on conversation patterns. Your goal is to help developers create systems that predict when deals will close by analyzing engagement signals and conversation dynamics.

## Why Prediction Matters

### The Forecasting Problem
```
Traditional forecasting:
- Rep guesses: "Should close this month"
- Based on hope, not data
- Consistently wrong
- Pipeline becomes fiction

Result:
- Missed forecasts
- Bad resource planning
- Surprised leadership
```

### Predictive Forecasting
```
Data-driven prediction:
- Analyzes conversation patterns
- Compares to historical deals
- Updates in real-time
- Confidence intervals

Result:
- Accurate forecasts
- Better resource allocation
- Proactive deal management
```

## Prediction Signals

### Velocity Signals
```
How fast is the deal moving?

Accelerating indicators:
- Response times decreasing
- Meeting frequency increasing
- Stakeholders being added
- Questions becoming more specific
- Pricing discussion initiated

Decelerating indicators:
- Response times increasing
- Meetings being postponed
- Stakeholders going quiet
- Vague or generic responses
- "We'll revisit this later"
```

### Engagement Signals
```
How engaged is the prospect?

High engagement (faster close):
- Multiple stakeholders involved
- Detailed questions asked
- Proactive outreach from them
- Documentation requested
- Reference calls requested

Low engagement (slower close):
- Single contact only
- Surface-level questions
- Slow responses
- No proactive contact
- Vague interest
```

### Stage Completion Signals
```
Where are they in the journey?

Discovery completed:
+Needs articulated
+Decision process shared
+Timeline discussed
→ Expect 60-90 days to close

Evaluation in progress:
+Demo completed
+Trial/POC active
+Technical questions addressed
→ Expect 30-60 days to close

Decision pending:
+Proposal reviewed
+Pricing negotiated
+Contract discussed
→ Expect 0-30 days to close
```

### Buying Signal Density
```
Count buying signals over time:

Week 1: 2 signals
Week 2: 4 signals
Week 3: 7 signals
Week 4: 10 signals

Increasing density = approaching decision

Signals to count:
- Pricing questions
- Timeline questions
- Implementation questions
- Contract questions
- "What's the next step?"
```

## Prediction Models

### Historical Pattern Matching
```python
def predict_from_history(deal):
    # Find similar historical deals
    similar_deals = find_similar_deals(
        industry=deal.industry,
        company_size=deal.company_size,
        deal_size=deal.estimated_value,
        product=deal.product_interest
    )

    # Get their actual close times
    close_times = [d.days_to_close for d in similar_deals]

    # Current deal's stage
    stage_days = get_average_remaining_days(
        stage=deal.current_stage,
        similar_deals=similar_deals
    )

    return {
        "estimated_days": stage_days,
        "confidence": calculate_confidence(similar_deals),
        "range_low": percentile(close_times, 25),
        "range_high": percentile(close_times, 75)
    }
```

### Conversation Pattern Model
```python
def predict_from_conversation(deal):
    conversations = get_conversations(deal)

    # Extract features
    features = {
        "avg_response_time": calc_avg_response_time(conversations),
        "response_time_trend": calc_response_trend(conversations),
        "message_count": len(conversations),
        "stakeholder_count": count_stakeholders(conversations),
        "buying_signal_count": count_buying_signals(conversations),
        "objection_count": count_objections(conversations),
        "question_specificity": assess_question_depth(conversations),
        "sentiment_trend": analyze_sentiment_trend(conversations)
    }

    # Predict using trained model
    prediction = close_time_model.predict(features)

    return {
        "estimated_days": prediction,
        "confidence": close_time_model.confidence(features),
        "key_factors": get_key_factors(features)
    }
```

### Combined Prediction
```python
def predict_close_time(deal):
    # Historical comparison
    historical = predict_from_history(deal)

    # Conversation analysis
    conversation = predict_from_conversation(deal)

    # Stage-based baseline
    stage_baseline = get_stage_baseline(deal.current_stage)

    # Weighted combination
    weights = {"historical": 0.3, "conversation": 0.5, "stage": 0.2}

    predicted_days = (
        historical["estimated_days"] * weights["historical"] +
        conversation["estimated_days"] * weights["conversation"] +
        stage_baseline * weights["stage"]
    )

    # Confidence is minimum of components
    confidence = min(
        historical["confidence"],
        conversation["confidence"]
    )

    return {
        "predicted_close_date": today() + timedelta(days=predicted_days),
        "predicted_days": predicted_days,
        "confidence": confidence,
        "factors": {
            "historical_pattern": historical,
            "conversation_signals": conversation,
            "stage_baseline": stage_baseline
        }
    }
```

## Stage-Specific Predictions

### Early Stage Predictions
```
Discovery stage:
- High uncertainty
- Wide range
- Base on industry averages

Prediction:
"Based on similar companies, expect 60-120 days
to decision. Current engagement suggests
you're on the faster end."

Focus on:
- Qualifying properly
- Identifying decision process
- Understanding timeline drivers
```

### Mid Stage Predictions
```
Evaluation stage:
- Moderate uncertainty
- Can compare to historical
- Engagement signals matter

Prediction:
"Deal is moving 20% faster than average.
If current pace continues, expect close
in 35-50 days."

Focus on:
- Addressing remaining objections
- Stakeholder alignment
- Competitive positioning
```

### Late Stage Predictions
```
Negotiation/Decision stage:
- Lower uncertainty
- Clear remaining steps
- Timing more predictable

Prediction:
"Pending contract review and legal approval.
Historical similar deals close within 2 weeks
of this stage. Target: January 25-February 5."

Focus on:
- Removing blockers
- Expediting approvals
- Closing logistics
```

## Dynamic Updates

### Real-Time Prediction Updates
```
Update prediction when:
- New conversation occurs
- Meeting completed
- Stage changes
- New stakeholder added
- Objection raised/addressed
- Buying signal detected

"After today's call where CFO asked about
implementation timeline, prediction moved
from 45 days to 30 days."
```

### Prediction Alerts
```python
def check_prediction_alerts(deal):
    current = deal.current_prediction
    previous = deal.previous_prediction

    alerts = []

    # Significant acceleration
    if current.days < previous.days * 0.7:
        alerts.append({
            "type": "acceleration",
            "message": f"Deal moving faster—close date moved up {previous.days - current.days} days"
        })

    # Significant slowdown
    if current.days > previous.days * 1.3:
        alerts.append({
            "type": "slowdown",
            "message": f"Deal slowing—close date pushed out {current.days - previous.days} days"
        })

    # At risk of slipping
    if deal.target_close_date and current.predicted_close > deal.target_close_date:
        alerts.append({
            "type": "at_risk",
            "message": f"May miss target close date by {(current.predicted_close - deal.target_close_date).days} days"
        })

    return alerts
```

## Forecast Applications

### Pipeline Forecasting
```
Aggregate predictions for pipeline:

Pipeline: $1,000,000
- Deal A: $200k, 90% in Jan (weighted: $180k)
- Deal B: $300k, 60% in Jan (weighted: $180k)
- Deal C: $500k, 30% in Jan (weighted: $150k)

January forecast: $510,000

Confidence range:
- Best case: $750,000
- Expected: $510,000
- Worst case: $300,000
```

### Resource Planning
```
Use predictions for:
- Implementation team scheduling
- Customer success allocation
- Rep capacity planning
- Inventory/fulfillment

"Predicted $2M closing in Q1.
Implementation needs 3 additional engineers."
```

### Deal Coaching
```
Alert managers to at-risk deals:

"Deal ABC predicted to close 2 weeks
later than forecast. Engagement dropped.
Suggest manager review."

"Deal XYZ accelerating faster than expected.
May need to pull in implementation team
earlier."
```

## Prediction Accuracy

### Measuring Accuracy
```
Track:
- Predicted vs actual close date
- Prediction accuracy by stage
- Accuracy by deal type
- Accuracy improvement over time

Metrics:
- Mean Absolute Error (MAE)
- Prediction within 2 weeks: X%
- Prediction within 30 days: Y%
```

### Improving Predictions
```
Feedback loop:

1. Make prediction
2. Deal closes (or doesn't)
3. Compare prediction to actual
4. Update model weights
5. Refine signal importance

Over time:
- More accurate predictions
- Better signal identification
- Improved confidence calibration
```

## Implementation

### Prediction Data Model
```json
{
  "deal_id": "12345",
  "prediction": {
    "predicted_close_date": "2024-02-15",
    "predicted_days_remaining": 30,
    "confidence": 0.75,
    "range": {
      "optimistic": "2024-02-01",
      "pessimistic": "2024-03-01"
    },
    "factors": {
      "accelerating": ["buying_signals_increasing", "stakeholder_engaged"],
      "decelerating": ["response_time_slow"],
      "neutral": ["typical_stage_duration"]
    },
    "updated_at": "2024-01-15T10:00:00Z",
    "previous_prediction": "2024-02-20"
  },
  "history": [
    {
      "date": "2024-01-01",
      "predicted_close": "2024-03-01",
      "confidence": 0.5,
      "stage": "discovery"
    },
    {
      "date": "2024-01-08",
      "predicted_close": "2024-02-20",
      "confidence": 0.65,
      "stage": "evaluation"
    }
  ]
}
```

### Integration Points
```
Where to surface predictions:

CRM:
- Deal record
- Pipeline views
- Forecast reports

Bot conversations:
- Adjust urgency based on timeline
- Recommend next actions
- Alert on at-risk deals

Dashboards:
- Rep-level predictions
- Team-level forecast
- Accuracy metrics
```

## Messaging Based on Predictions

### Accelerating Deal
```
"Based on our conversations, you're moving
faster than most companies your size.
If we aim for [predicted date], here's what
we'd need to accomplish in the next 2 weeks..."
```

### Stalled Deal
```
"We had good momentum, but I sense things
have slowed. Is there something holding you
back that I can address?"
```

### At-Risk Deal
```
"You mentioned wanting this done by [target].
To hit that, we'd need to [specific actions].
Is that timeline still realistic?"
```

