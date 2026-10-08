---
name: conversation-quality-scoring
description: When the user wants to build or improve a sales bot's ability to rate conversation quality. Also use when the user mentions "conversation scoring," "quality scoring," "exchange rating," "conversation metrics," or "performance scoring."
---

# Conversation Quality Scoring

You are an expert in building sales bots that rate conversation quality to identify top performers. Your goal is to help developers create systems that score conversations to find what works and coach improvement.

## Why Quality Scoring Matters

### The Blind Spot Problem
```
Without quality scoring:
- All conversations treated equal
- Don't know what "good" looks like
- Can't identify best practices
- No basis for improvement

Rep A: 10% conversion
Rep B: 15% conversion
Bot C: 12% conversion
Why? Unknown.
```

### With Quality Scoring
```
Quality-aware system:
- Score each conversation dimension
- Identify high-quality patterns
- Spot areas for improvement
- Benchmark and compare

Rep A: Score 65 (weak on discovery)
Rep B: Score 82 (strong qualification)
Bot C: Score 71 (needs better objection handling)
Now we know where to focus.
```

## Scoring Dimensions

### Engagement Quality
```python
def score_engagement(conversation):
    score = 0

    # Response rate
    response_rate = calculate_response_rate(conversation)
    if response_rate >= 0.8:
        score += 30
    elif response_rate >= 0.5:
        score += 20
    elif response_rate >= 0.3:
        score += 10

    # Response depth
    avg_response_length = calculate_avg_response_length(conversation)
    if avg_response_length > 50:
        score += 20
    elif avg_response_length > 25:
        score += 10

    # Response sentiment
    sentiment_trend = analyze_sentiment_trend(conversation)
    if sentiment_trend > 0:
        score += 20
    elif sentiment_trend == 0:
        score += 10

    # Engagement velocity
    avg_response_time = calculate_avg_response_time(conversation)
    if avg_response_time < timedelta(hours=4):
        score += 15

    return min(score, 100)
```

### Discovery Quality
```python
def score_discovery(conversation):
    score = 0

    # Information gathered
    info_gathered = {
        "pain_points": 25,
        "budget": 20,
        "timeline": 20,
        "decision_process": 15,
        "stakeholders": 15,
        "current_solution": 10
    }

    for info_type, points in info_gathered.items():
        if has_gathered_info(conversation, info_type):
            score += points

    # Question quality
    questions = extract_questions(conversation, sender="bot")
    open_questions = [q for q in questions if is_open_ended(q)]
    if len(open_questions) >= 3:
        score += 15

    # Follow-up depth
    follow_ups = count_follow_up_questions(conversation)
    score += min(follow_ups * 5, 20)

    return min(score, 100)
```

### Value Communication
```python
def score_value_communication(conversation):
    score = 0

    # Value propositions delivered
    value_props = extract_value_propositions(conversation)
    if len(value_props) >= 2:
        score += 25

    # Personalization
    personalization_level = assess_personalization(conversation)
    score += personalization_level * 25

    # Relevance to stated needs
    needs = extract_stated_needs(conversation)
    solutions = extract_solutions_offered(conversation)
    alignment = calculate_need_solution_alignment(needs, solutions)
    score += alignment * 30

    # Social proof used
    if has_relevant_social_proof(conversation):
        score += 15

    return min(score, 100)
```

### Objection Handling Quality
```python
def score_objection_handling(conversation):
    objections = extract_objections(conversation)

    if not objections:
        return None  # No objections to score

    score = 0
    for objection in objections:
        # Was it acknowledged?
        if objection.acknowledged:
            score += 10

        # Was it addressed?
        if objection.addressed:
            score += 20

        # Was the response appropriate?
        response_quality = assess_response_quality(objection.response)
        score += response_quality * 15

        # Was it resolved?
        if objection.resolved:
            score += 15

    # Average across objections
    avg_score = score / len(objections)
    return min(avg_score, 100)
```

### Progression Quality
```python
def score_progression(conversation):
    score = 0

    # Stage advancement
    if advanced_stage(conversation):
        score += 30

    # Commitments obtained
    commitments = extract_commitments(conversation)
    score += len(commitments) * 10

    # Clear next steps
    if has_clear_next_step(conversation):
        score += 25

    # Meeting scheduled
    if meeting_scheduled(conversation):
        score += 25

    # Forward momentum
    momentum = assess_momentum(conversation)
    score += momentum * 20

    return min(score, 100)
```

## Aggregate Scoring

### Weighted Total Score
```python
def calculate_total_quality_score(conversation):
    weights = {
        "engagement": 0.20,
        "discovery": 0.25,
        "value_communication": 0.20,
        "objection_handling": 0.15,
        "progression": 0.20
    }

    scores = {
        "engagement": score_engagement(conversation),
        "discovery": score_discovery(conversation),
        "value_communication": score_value_communication(conversation),
        "objection_handling": score_objection_handling(conversation),
        "progression": score_progression(conversation)
    }

    # Handle None (e.g., no objections)
    active_weights = {}
    for dimension, score in scores.items():
        if score is not None:
            active_weights[dimension] = weights[dimension]

    # Normalize weights
    weight_sum = sum(active_weights.values())
    normalized_weights = {k: v/weight_sum for k, v in active_weights.items()}

    # Calculate weighted total
    total = sum(
        scores[d] * normalized_weights[d]
        for d in normalized_weights
        if scores[d] is not None
    )

    return {
        "total_score": total,
        "dimension_scores": scores,
        "weights_used": normalized_weights
    }
```

### Score Interpretation
```python
def interpret_score(score_result):
    total = score_result["total_score"]

    if total >= 85:
        tier = "excellent"
        description = "High-quality conversation with strong execution"
    elif total >= 70:
        tier = "good"
        description = "Solid conversation with room for improvement"
    elif total >= 55:
        tier = "average"
        description = "Adequate but missing opportunities"
    elif total >= 40:
        tier = "below_average"
        description = "Several areas need attention"
    else:
        tier = "poor"
        description = "Significant improvement needed"

    # Find weakest dimension
    weak_dimensions = [
        d for d, s in score_result["dimension_scores"].items()
        if s is not None and s < 50
    ]

    # Find strongest dimension
    strong_dimensions = [
        d for d, s in score_result["dimension_scores"].items()
        if s is not None and s >= 80
    ]

    return {
        "tier": tier,
        "description": description,
        "weakest": weak_dimensions,
        "strongest": strong_dimensions,
        "recommendation": generate_improvement_recommendation(score_result)
    }
```

## Comparative Analysis

### Benchmarking
```python
def benchmark_conversation(conversation, comparison_group):
    """Compare conversation to peers"""

    my_score = calculate_total_quality_score(conversation)

    # Get comparison group scores
    peer_scores = [
        calculate_total_quality_score(c)
        for c in comparison_group
    ]

    peer_totals = [s["total_score"] for s in peer_scores]

    return {
        "my_score": my_score["total_score"],
        "percentile": calculate_percentile(my_score["total_score"], peer_totals),
        "peer_average": mean(peer_totals),
        "peer_top_10": percentile(peer_totals, 90),
        "gap_to_average": my_score["total_score"] - mean(peer_totals),
        "gap_to_top": percentile(peer_totals, 90) - my_score["total_score"]
    }
```

### Rep/Bot Comparison
```python
def compare_performers(performer_ids, time_period):
    """Compare quality scores across reps or bots"""

    results = {}
    for performer_id in performer_ids:
        conversations = get_conversations(performer_id, time_period)
        scores = [calculate_total_quality_score(c) for c in conversations]

        results[performer_id] = {
            "avg_total": mean([s["total_score"] for s in scores]),
            "avg_by_dimension": {
                d: mean([s["dimension_scores"][d] for s in scores if s["dimension_scores"][d]])
                for d in ["engagement", "discovery", "value_communication", "objection_handling", "progression"]
            },
            "conversation_count": len(conversations),
            "trend": calculate_score_trend(scores)
        }

    return results
```

## Quality Improvement

### Coaching Recommendations
```python
def generate_coaching_insights(performer_id, time_period):
    scores = get_performer_scores(performer_id, time_period)

    insights = []

    # Find consistently weak dimensions
    dimension_avgs = calculate_dimension_averages(scores)
    for dimension, avg in dimension_avgs.items():
        if avg < 60:
            insights.append({
                "type": "weakness",
                "dimension": dimension,
                "score": avg,
                "recommendation": get_dimension_recommendation(dimension),
                "examples": get_high_score_examples(dimension)
            })

    # Find declining dimensions
    for dimension in dimension_avgs:
        trend = calculate_dimension_trend(scores, dimension)
        if trend < -0.1:  # Declining
            insights.append({
                "type": "declining",
                "dimension": dimension,
                "trend": trend,
                "recommendation": f"Focus on {dimension} - scores declining"
            })

    return insights
```

### Automated Feedback
```python
def provide_conversation_feedback(conversation):
    score = calculate_total_quality_score(conversation)
    interpretation = interpret_score(score)

    feedback = {
        "overall": f"Score: {score['total_score']:.0f}/100 ({interpretation['tier']})",
        "strengths": [],
        "improvements": []
    }

    for dimension, dim_score in score["dimension_scores"].items():
        if dim_score and dim_score >= 75:
            feedback["strengths"].append(
                f"Strong {dimension} (score: {dim_score:.0f})"
            )
        elif dim_score and dim_score < 55:
            feedback["improvements"].append({
                "dimension": dimension,
                "score": dim_score,
                "tip": get_improvement_tip(dimension, conversation)
            })

    return feedback
```

## Implementation

### Real-Time Scoring
```python
class ConversationScorer:
    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
        self.running_score = {}

    def update_score(self, new_message):
        """Update score after each message"""

        conversation = get_conversation(self.conversation_id)

        # Recalculate dimensions that could have changed
        self.running_score = calculate_total_quality_score(conversation)

        # Alert if significant change
        if self.score_dropped_significantly():
            alert_quality_drop(self.conversation_id, self.running_score)

        return self.running_score
```

## Metrics

### Quality Correlation
```
Track:
- Correlation between quality score and conversion
- Correlation between dimensions and outcomes
- Which dimensions matter most?

Validate:
- Do high-scoring conversations convert better?
- Which scores predict success?
```

