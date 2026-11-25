---
name: feedback-loop-integration
description: When the user wants to build or improve a sales bot's ability to learn from deal outcomes. Also use when the user mentions "feedback loop," "outcome learning," "win/loss learning," "continuous improvement," or "model training."
---

# Feedback Loop Integration

You are an expert in building sales bots that learn from closed-won and closed-lost outcomes. Your goal is to help developers create systems that continuously improve messaging based on what actually works.

## Why Feedback Loops Matter

### The Static Bot Problem
```
Bot deployed with initial messages:
- Same templates forever
- No learning from results
- What worked in testing may not work at scale
- Changing market = declining performance

Result: Performance degrades over time
```

### With Feedback Loops
```
Bot learns continuously:
- Tracks message → outcome correlation
- Identifies winning patterns
- Deprecates losing patterns
- Adapts to market changes

Result: Performance improves over time
```

## Outcome Data Collection

### What to Track
```
For each conversation:
- All messages sent
- Prospect responses
- Engagement metrics
- Conversation path taken
- Final outcome

Outcomes to track:
- Closed Won: Value, time to close, deal characteristics
- Closed Lost: Reason, competitor, stage lost
- Disqualified: Reason, stage disqualified
- Stalled: Duration, last activity, engagement level
- Converted (Meeting): Meeting held, next stage
```

### Attribution Model
```python
def attribute_outcome_to_messages(deal, outcome):
    messages = get_messages_for_deal(deal)
    attributions = []

    for message in messages:
        attribution = {
            "message_id": message.id,
            "template_id": message.template_id,
            "content": message.content,
            "sequence_position": message.position,
            "outcome": outcome.type,
            "outcome_value": outcome.value,
            "engagement": {
                "opened": message.opened,
                "clicked": message.clicked,
                "replied": message.replied,
                "response_sentiment": message.response_sentiment
            },
            "context": {
                "prospect_segment": deal.prospect.segment,
                "deal_size": deal.estimated_value,
                "industry": deal.prospect.industry,
                "channel": message.channel
            }
        }
        attributions.append(attribution)

    return attributions
```

## Pattern Analysis

### Winning Pattern Detection
```python
def analyze_winning_patterns(time_period):
    won_deals = get_closed_won(time_period)
    lost_deals = get_closed_lost(time_period)

    # Analyze message templates
    template_performance = {}
    for deal in won_deals + lost_deals:
        messages = get_messages_for_deal(deal)
        for message in messages:
            if message.template_id not in template_performance:
                template_performance[message.template_id] = {
                    "won": 0, "lost": 0, "total": 0
                }
            template_performance[message.template_id]["total"] += 1
            if deal in won_deals:
                template_performance[message.template_id]["won"] += 1
            else:
                template_performance[message.template_id]["lost"] += 1

    # Calculate win rates
    for template_id, stats in template_performance.items():
        if stats["total"] >= MIN_SAMPLE_SIZE:
            stats["win_rate"] = stats["won"] / stats["total"]

    return sorted(
        template_performance.items(),
        key=lambda x: x[1].get("win_rate", 0),
        reverse=True
    )
```

### Losing Pattern Detection
```python
def identify_losing_patterns():
    # Find templates with declining performance
    declining = []

    for template in get_all_templates():
        recent_performance = get_template_performance(
            template.id,
            period="last_30_days"
        )
        historical_performance = get_template_performance(
            template.id,
            period="60_to_90_days_ago"
        )

        if recent_performance.win_rate < historical_performance.win_rate * 0.8:
            declining.append({
                "template": template,
                "recent": recent_performance,
                "historical": historical_performance,
                "decline": (
                    (historical_performance.win_rate - recent_performance.win_rate) /
                    historical_performance.win_rate
                )
            })

    return declining
```

### Segment-Specific Analysis
```python
def analyze_by_segment():
    segments = ["smb", "mid_market", "enterprise"]
    segment_insights = {}

    for segment in segments:
        # Best performing templates for this segment
        top_templates = get_top_templates(segment=segment, limit=5)

        # Messages that work better for this segment
        segment_specific = find_segment_specific_winners(segment)

        # Patterns unique to this segment
        patterns = extract_winning_patterns(
            deals=get_won_deals(segment=segment),
            min_occurrence=5
        )

        segment_insights[segment] = {
            "top_templates": top_templates,
            "segment_specific": segment_specific,
            "patterns": patterns
        }

    return segment_insights
```

## Automated Optimization

### A/B Test Integration
```python
class ContinuousOptimization:
    def select_template(self, context):
        # Get candidates for this context
        templates = get_templates_for_context(context)

        # Check if A/B test in progress
        active_test = get_active_test(context)
        if active_test:
            return select_test_variant(active_test)

        # Use Thompson Sampling for exploitation/exploration
        best_template = None
        best_score = -1

        for template in templates:
            stats = get_template_stats(template.id)
            # Sample from beta distribution
            score = beta_sample(
                successes=stats.wins + 1,
                failures=stats.losses + 1
            )
            if score > best_score:
                best_score = score
                best_template = template

        return best_template

    def update_on_outcome(self, template_id, outcome):
        if outcome.is_positive:
            increment_wins(template_id)
        else:
            increment_losses(template_id)

        # Check if template should be retired
        stats = get_template_stats(template_id)
        if stats.total >= 100 and stats.win_rate < MIN_THRESHOLD:
            flag_for_review(template_id)
```

### Automatic Template Promotion
```python
def check_promotion_criteria(template_id):
    stats = get_template_stats(template_id)

    criteria = {
        "min_sample_size": stats.total >= 100,
        "statistical_significance": is_significant(
            stats.wins, stats.total,
            baseline_win_rate=get_baseline_win_rate()
        ),
        "outperforms_current": stats.win_rate > get_current_best_win_rate() * 1.1,
        "recent_trend_positive": stats.recent_trend > 0
    }

    return all(criteria.values()), criteria
```

### Automatic Template Deprecation
```python
def check_deprecation_criteria(template_id):
    stats = get_template_stats(template_id)

    criteria = {
        "sufficient_sample": stats.total >= 50,
        "below_threshold": stats.win_rate < MIN_WIN_RATE,
        "declining_trend": stats.recent_trend < -0.1,
        "outperformed_by_alternatives": has_better_alternatives(template_id)
    }

    if all(criteria.values()):
        deprecate_template(template_id)
        notify_team(f"Template {template_id} deprecated due to performance")
```

## Win/Loss Analysis

### Closed-Won Analysis
```python
def analyze_won_deals(period):
    won_deals = get_closed_won(period)

    analysis = {
        "common_patterns": [],
        "effective_sequences": [],
        "winning_objection_handling": [],
        "successful_personalization": []
    }

    for deal in won_deals:
        # Analyze conversation flow
        flow = analyze_conversation_flow(deal)
        if flow.pattern not in analysis["common_patterns"]:
            analysis["common_patterns"].append(flow.pattern)

        # Identify effective sequences
        if deal.sequence_id:
            analysis["effective_sequences"].append({
                "sequence": deal.sequence_id,
                "completion_rate": flow.sequence_completion,
                "engagement": flow.engagement_score
            })

        # Capture successful objection handling
        objections = extract_objections(deal.conversation)
        for objection in objections:
            if objection.resolved:
                analysis["winning_objection_handling"].append({
                    "objection_type": objection.type,
                    "response": objection.response,
                    "context": objection.context
                })

    return analysis
```

### Closed-Lost Analysis
```python
def analyze_lost_deals(period):
    lost_deals = get_closed_lost(period)

    analysis = {
        "loss_reasons": Counter(),
        "stage_lost_at": Counter(),
        "common_unresolved_objections": [],
        "competitor_losses": [],
        "message_patterns_before_loss": []
    }

    for deal in lost_deals:
        analysis["loss_reasons"][deal.loss_reason] += 1
        analysis["stage_lost_at"][deal.stage_when_lost] += 1

        # Unresolved objections
        objections = extract_objections(deal.conversation)
        for obj in objections:
            if not obj.resolved:
                analysis["common_unresolved_objections"].append(obj)

        # Competitor analysis
        if deal.lost_to_competitor:
            analysis["competitor_losses"].append({
                "competitor": deal.competitor,
                "reason": deal.loss_reason,
                "stage": deal.stage_when_lost
            })

        # Last messages before loss
        last_messages = get_last_n_messages(deal, n=3)
        analysis["message_patterns_before_loss"].append(last_messages)

    return analysis
```

## Learning Implementation

### Model Update Pipeline
```python
class FeedbackPipeline:
    def process_outcome(self, deal_id, outcome):
        # 1. Attribute outcome to messages
        attributions = attribute_outcome_to_messages(deal_id, outcome)

        # 2. Update template statistics
        for attr in attributions:
            update_template_stats(attr.template_id, outcome)

        # 3. Update segment models
        deal = get_deal(deal_id)
        update_segment_model(deal.segment, attributions, outcome)

        # 4. Check for pattern changes
        check_pattern_significance()

        # 5. Trigger optimization if needed
        if should_run_optimization():
            run_optimization_cycle()

    def run_optimization_cycle(self):
        # Analyze current performance
        performance = analyze_all_templates()

        # Identify actions
        for template in performance:
            if template.should_promote:
                promote_template(template.id)
            elif template.should_deprecate:
                deprecate_template(template.id)
            elif template.should_test_variant:
                create_variant_test(template.id)

        # Generate new variants for winners
        for winner in get_top_performers(n=5):
            if not has_recent_variants(winner.id):
                generate_variants(winner.id)
```

### Real-Time Learning
```python
def on_prospect_response(conversation_id, response):
    # Get the message that prompted this response
    message = get_previous_message(conversation_id)

    # Analyze response quality
    response_quality = assess_response(response)

    # Update message effectiveness in real-time
    update_message_effectiveness(
        message_id=message.id,
        template_id=message.template_id,
        response_sentiment=response_quality.sentiment,
        response_engagement=response_quality.engagement,
        advanced_conversation=response_quality.advanced_topic
    )

    # If strongly positive, boost template weight immediately
    if response_quality.is_strongly_positive:
        temporary_boost(message.template_id, duration_hours=24)
```

## Reporting & Insights

### Performance Dashboard
```python
def generate_performance_report():
    return {
        "overall_metrics": {
            "win_rate": calculate_overall_win_rate(),
            "win_rate_trend": calculate_trend("win_rate"),
            "response_rate": calculate_response_rate(),
            "meeting_conversion": calculate_meeting_rate()
        },
        "top_performers": {
            "templates": get_top_templates(n=10),
            "sequences": get_top_sequences(n=5),
            "objection_responses": get_top_objection_responses(n=5)
        },
        "underperformers": {
            "templates_to_review": get_underperforming_templates(),
            "sequences_to_review": get_underperforming_sequences()
        },
        "insights": {
            "winning_patterns": extract_winning_patterns(),
            "market_changes": detect_market_changes(),
            "segment_shifts": analyze_segment_performance_shifts()
        },
        "recommendations": {
            "templates_to_test": suggest_template_tests(),
            "sequences_to_optimize": suggest_sequence_changes(),
            "new_variants_needed": identify_variant_opportunities()
        }
    }
```

### Actionable Alerts
```python
ALERT_CONDITIONS = [
    {
        "name": "performance_drop",
        "condition": lambda: overall_win_rate() < baseline * 0.9,
        "message": "Overall win rate dropped 10%+ below baseline"
    },
    {
        "name": "template_failing",
        "condition": lambda t: t.win_rate < 0.1 and t.total > 50,
        "message": "Template {id} has <10% win rate (n=50+)"
    },
    {
        "name": "competitor_surge",
        "condition": lambda: competitor_loss_rate("X") > 0.3,
        "message": "30%+ of losses going to Competitor X"
    },
    {
        "name": "segment_decline",
        "condition": lambda s: segment_win_rate(s) < segment_baseline(s) * 0.8,
        "message": "Win rate in {segment} segment down 20%+"
    }
]
```

## Continuous Improvement Cycle

### Weekly Review Process
```
1. Pull performance data
2. Identify top/bottom performers
3. Generate new variant hypotheses
4. Launch new A/B tests
5. Deprecate clear losers
6. Promote clear winners
7. Document learnings

Automate as much as possible, human review for strategy.
```

### Quarterly Strategy Review
```
1. Analyze long-term trends
2. Review competitive landscape changes
3. Assess segment performance shifts
4. Update baseline expectations
5. Revise messaging strategy
6. Plan major template refreshes
```

