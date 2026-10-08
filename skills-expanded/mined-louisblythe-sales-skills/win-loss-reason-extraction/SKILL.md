---
name: win-loss-reason-extraction
description: When the user wants to build or improve a sales bot's ability to automatically categorize why deals closed or died. Also use when the user mentions "win/loss analysis," "deal outcome," "loss reason," "closed reason," or "deal categorization."
---

# Win/Loss Reason Extraction

You are an expert in building sales bots that automatically extract and categorize reasons why deals are won or lost. Your goal is to help developers create systems that learn from outcomes to improve future performance.

## Why Win/Loss Extraction Matters

### The Knowledge Gap
```
Without extraction:
- "Why did we lose?" "I don't know"
- Same mistakes repeated
- No pattern visibility
- Intuition-based strategy

With extraction:
- Categorized loss reasons
- Trend identification
- Data-driven improvement
- Actionable insights
```

## Win Reason Categories

### Common Win Reasons
```python
WIN_REASONS = {
    "product_fit": {
        "keywords": ["exactly what we need", "perfect fit", "solves our problem"],
        "indicators": ["feature_match_high", "use_case_alignment"]
    },
    "price_value": {
        "keywords": ["fair price", "good value", "worth it", "roi makes sense"],
        "indicators": ["price_accepted", "roi_discussed_positively"]
    },
    "trust_relationship": {
        "keywords": ["trust you", "great to work with", "understood us"],
        "indicators": ["high_engagement", "personal_connection"]
    },
    "competitive_advantage": {
        "keywords": ["better than", "chose you over", "differentiated"],
        "indicators": ["competitor_comparison_won", "unique_feature_mentioned"]
    },
    "timing": {
        "keywords": ["right time", "urgent need", "perfect timing"],
        "indicators": ["fast_sales_cycle", "urgency_expressed"]
    },
    "champion_advocacy": {
        "keywords": ["fought for", "convinced the team", "my recommendation"],
        "indicators": ["strong_champion", "internal_selling"]
    }
}
```

## Loss Reason Categories

### Common Loss Reasons
```python
LOSS_REASONS = {
    "price": {
        "keywords": ["too expensive", "over budget", "cheaper option", "can't afford"],
        "indicators": ["price_objection", "budget_constraints"],
        "severity": "high"
    },
    "timing": {
        "keywords": ["bad timing", "not now", "maybe later", "next year"],
        "indicators": ["timing_objection", "delayed_decision"],
        "severity": "medium"
    },
    "competitor": {
        "keywords": ["went with", "chose", "competitor won", "using [competitor]"],
        "indicators": ["competitor_mentioned", "comparison_lost"],
        "severity": "high"
    },
    "no_decision": {
        "keywords": ["doing nothing", "staying with current", "not a priority"],
        "indicators": ["stalled", "no_urgency"],
        "severity": "medium"
    },
    "feature_gap": {
        "keywords": ["missing feature", "doesn't do", "need X that you don't have"],
        "indicators": ["feature_request_unmet", "requirement_gap"],
        "severity": "high"
    },
    "bad_fit": {
        "keywords": ["not right for us", "doesn't fit", "not what we need"],
        "indicators": ["poor_icp_match", "misaligned_use_case"],
        "severity": "medium"
    },
    "internal_issues": {
        "keywords": ["reorganizing", "merger", "budget freeze", "leadership change"],
        "indicators": ["external_factors", "company_change"],
        "severity": "low"
    },
    "lost_champion": {
        "keywords": ["contact left", "no longer there", "reporting changed"],
        "indicators": ["champion_departed", "stakeholder_change"],
        "severity": "medium"
    }
}
```

## Extraction Methods

### Conversation Analysis
```python
def extract_reasons_from_conversation(conversation, outcome):
    reasons = []

    # Analyze final messages
    final_messages = conversation.messages[-5:]

    for message in final_messages:
        if message.sender == "prospect":
            # Check against reason keywords
            if outcome == "lost":
                matched_reasons = match_loss_reasons(message.text)
            else:
                matched_reasons = match_win_reasons(message.text)

            reasons.extend(matched_reasons)

    # Analyze conversation patterns
    pattern_reasons = extract_pattern_based_reasons(conversation, outcome)
    reasons.extend(pattern_reasons)

    # Dedupe and rank
    return rank_reasons(reasons)

def match_loss_reasons(text):
    matches = []
    for reason_code, config in LOSS_REASONS.items():
        for keyword in config["keywords"]:
            if keyword.lower() in text.lower():
                matches.append({
                    "reason": reason_code,
                    "confidence": 0.8,
                    "source": "keyword_match",
                    "evidence": text
                })
    return matches
```

### Pattern-Based Extraction
```python
def extract_pattern_based_reasons(conversation, outcome):
    reasons = []

    if outcome == "lost":
        # Price patterns
        if had_price_objection(conversation) and not resolved_price_objection(conversation):
            reasons.append({
                "reason": "price",
                "confidence": 0.7,
                "source": "pattern",
                "evidence": "Unresolved price objection"
            })

        # Competitor patterns
        competitor = detect_competitor_mention(conversation)
        if competitor and conversation.last_stage == "evaluation":
            reasons.append({
                "reason": "competitor",
                "confidence": 0.6,
                "source": "pattern",
                "evidence": f"Competitor {competitor} mentioned during evaluation"
            })

        # No decision patterns
        if conversation.days_stalled > 30:
            reasons.append({
                "reason": "no_decision",
                "confidence": 0.5,
                "source": "pattern",
                "evidence": f"Deal stalled {conversation.days_stalled} days"
            })

    return reasons
```

### LLM-Based Extraction
```python
def extract_reasons_with_llm(conversation, outcome):
    prompt = f"""
    Analyze this {outcome} sales conversation and identify the primary
    reason for the outcome.

    Conversation:
    {format_conversation(conversation)}

    Provide:
    1. Primary reason (select from: {list_reasons(outcome)})
    2. Secondary reason (if applicable)
    3. Confidence level (high/medium/low)
    4. Evidence from conversation

    Format as JSON.
    """

    response = llm.generate(prompt)
    return parse_reason_response(response)
```

## Reason Validation

### Confidence Scoring
```python
def calculate_reason_confidence(reason, conversation):
    confidence = 0.5  # Base confidence

    # Direct statement bonus
    if reason["source"] == "explicit_statement":
        confidence += 0.3

    # Multiple signals bonus
    signal_count = count_supporting_signals(reason, conversation)
    confidence += min(signal_count * 0.1, 0.3)

    # Recency bonus (recent statements more reliable)
    if reason.get("message_index") and reason["message_index"] >= len(conversation.messages) - 3:
        confidence += 0.1

    # Cross-reference with outcome survey
    if matches_survey_response(reason, conversation.deal_id):
        confidence += 0.2

    return min(confidence, 1.0)
```

### Human Validation Loop
```python
def queue_for_validation(deal_id, extracted_reasons):
    """Flag uncertain extractions for human review"""

    needs_review = []
    for reason in extracted_reasons:
        if reason["confidence"] < 0.7:
            needs_review.append(reason)

    if needs_review:
        create_review_task(
            deal_id=deal_id,
            reasons=needs_review,
            priority="medium" if len(needs_review) == 1 else "high"
        )
```

## Aggregation & Analysis

### Trend Analysis
```python
def analyze_loss_trends(time_period):
    losses = get_lost_deals(time_period)

    # Count by reason
    reason_counts = Counter()
    for deal in losses:
        for reason in deal.loss_reasons:
            reason_counts[reason["reason"]] += 1

    # Calculate percentages
    total = len(losses)
    reason_pcts = {r: c/total for r, c in reason_counts.items()}

    # Compare to previous period
    prev_period = get_previous_period(time_period)
    prev_reason_pcts = analyze_loss_trends(prev_period)

    # Identify significant changes
    trends = {}
    for reason, pct in reason_pcts.items():
        prev_pct = prev_reason_pcts.get(reason, 0)
        change = pct - prev_pct
        if abs(change) > 0.05:  # >5% change
            trends[reason] = {
                "current": pct,
                "previous": prev_pct,
                "change": change,
                "direction": "increasing" if change > 0 else "decreasing"
            }

    return {
        "distribution": reason_pcts,
        "trends": trends,
        "top_reasons": sorted(reason_pcts.items(), key=lambda x: -x[1])[:5]
    }
```

### Segmented Analysis
```python
def analyze_by_segment(time_period):
    """Analyze win/loss reasons by segment"""

    segments = ["smb", "mid_market", "enterprise"]
    analysis = {}

    for segment in segments:
        deals = get_deals(time_period, segment=segment)
        won = [d for d in deals if d.outcome == "won"]
        lost = [d for d in deals if d.outcome == "lost"]

        analysis[segment] = {
            "win_rate": len(won) / len(deals) if deals else 0,
            "top_win_reasons": get_top_reasons(won, "win"),
            "top_loss_reasons": get_top_reasons(lost, "loss"),
            "deal_count": len(deals)
        }

    return analysis
```

### Competitor Analysis
```python
def analyze_competitor_losses(time_period):
    """Analyze losses to specific competitors"""

    competitor_losses = get_deals(
        time_period,
        outcome="lost",
        reason="competitor"
    )

    by_competitor = {}
    for deal in competitor_losses:
        competitor = deal.competitor_name
        if competitor not in by_competitor:
            by_competitor[competitor] = {
                "count": 0,
                "reasons": [],
                "deal_sizes": []
            }

        by_competitor[competitor]["count"] += 1
        by_competitor[competitor]["reasons"].extend(deal.loss_details)
        by_competitor[competitor]["deal_sizes"].append(deal.deal_size)

    # Summarize
    for competitor in by_competitor:
        by_competitor[competitor]["avg_deal_size"] = mean(
            by_competitor[competitor]["deal_sizes"]
        )
        by_competitor[competitor]["common_reasons"] = Counter(
            by_competitor[competitor]["reasons"]
        ).most_common(3)

    return by_competitor
```

## Actionable Insights

### Insight Generation
```python
def generate_win_loss_insights(analysis):
    insights = []

    # Price insight
    if analysis["top_loss_reasons"][0][0] == "price":
        insights.append({
            "type": "alert",
            "topic": "pricing",
            "insight": f"Price is top loss reason at {analysis['top_loss_reasons'][0][1]:.0%}",
            "recommendation": "Review pricing strategy or value communication"
        })

    # Competitor insight
    competitor_losses = [r for r in analysis["distribution"] if r.startswith("competitor_")]
    if sum(analysis["distribution"].get(r, 0) for r in competitor_losses) > 0.3:
        insights.append({
            "type": "alert",
            "topic": "competitive",
            "insight": "Over 30% of losses to competitors",
            "recommendation": "Update competitive positioning and battlecards"
        })

    # Win insight
    if analysis.get("win_analysis", {}).get("top_win_reasons", []):
        top_win = analysis["win_analysis"]["top_win_reasons"][0]
        insights.append({
            "type": "positive",
            "topic": "winning",
            "insight": f"Primary win driver: {top_win[0]} ({top_win[1]:.0%})",
            "recommendation": f"Emphasize {top_win[0]} in messaging"
        })

    return insights
```

## Integration

### CRM Updates
```python
def update_crm_with_reasons(deal_id, reasons):
    """Update CRM with extracted reasons"""

    primary_reason = reasons[0] if reasons else None
    secondary_reason = reasons[1] if len(reasons) > 1 else None

    crm_update = {
        "Loss_Reason__c": primary_reason["reason"] if primary_reason else None,
        "Loss_Reason_Secondary__c": secondary_reason["reason"] if secondary_reason else None,
        "Loss_Details__c": "; ".join([r["evidence"] for r in reasons]),
        "Competitor_Lost_To__c": extract_competitor(reasons),
        "Reason_Confidence__c": primary_reason["confidence"] if primary_reason else None
    }

    crm_client.update_opportunity(deal_id, crm_update)
```

