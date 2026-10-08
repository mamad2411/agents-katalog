---
name: sentiment-trend-tracking
description: When the user wants to build or improve a sales bot's ability to monitor sentiment over time. Also use when the user mentions "sentiment trends," "tone tracking," "campaign sentiment," "aggregate sentiment," or "sentiment monitoring."
---

# Sentiment Trend Tracking

You are an expert in building sales bots that monitor whether overall campaign tone is improving or degrading. Your goal is to help developers create systems that track sentiment trends across conversations to identify systemic issues.

## Why Trend Tracking Matters

### The Slow Decline Problem
```
Individual conversations look fine.
Aggregate tells a different story:

Week 1: Average sentiment 0.65
Week 2: Average sentiment 0.60
Week 3: Average sentiment 0.52
Week 4: Average sentiment 0.45

Something's wrong that individual
conversation review wouldn't catch.
```

### With Trend Tracking
```
Alert: "Campaign sentiment declined 25%
over 4 weeks. Top drivers:
- Message fatigue (same template)
- Increased competitor mentions
- Pricing complaints up 40%"

Early warning enables correction.
```

## Sentiment Measurement

### Per-Message Sentiment
```python
def analyze_message_sentiment(message):
    # Use NLP model for sentiment
    sentiment_result = sentiment_model.analyze(message.text)

    return {
        "message_id": message.id,
        "timestamp": message.timestamp,
        "sentiment_score": sentiment_result.score,  # -1 to 1
        "sentiment_label": sentiment_result.label,  # negative/neutral/positive
        "confidence": sentiment_result.confidence,
        "aspects": extract_aspect_sentiments(message)
    }

def extract_aspect_sentiments(message):
    """Break down sentiment by topic"""
    aspects = {}

    topics = ["pricing", "product", "support", "timeline", "competitor"]
    for topic in topics:
        if mentions_topic(message.text, topic):
            aspects[topic] = analyze_topic_sentiment(message.text, topic)

    return aspects
```

### Conversation Sentiment
```python
def calculate_conversation_sentiment(conversation):
    message_sentiments = [
        analyze_message_sentiment(m)
        for m in conversation.messages
        if m.sender == "prospect"
    ]

    if not message_sentiments:
        return None

    return {
        "conversation_id": conversation.id,
        "average_sentiment": mean([m["sentiment_score"] for m in message_sentiments]),
        "sentiment_trend": calculate_trend(message_sentiments),
        "starting_sentiment": message_sentiments[0]["sentiment_score"],
        "ending_sentiment": message_sentiments[-1]["sentiment_score"],
        "delta": message_sentiments[-1]["sentiment_score"] - message_sentiments[0]["sentiment_score"],
        "message_count": len(message_sentiments),
        "aspect_sentiments": aggregate_aspects(message_sentiments)
    }
```

## Trend Calculation

### Time Series Analysis
```python
def calculate_sentiment_trend(time_period, granularity="day"):
    """Calculate sentiment trend over time"""

    conversations = get_conversations(time_period)

    # Group by time bucket
    buckets = defaultdict(list)
    for conv in conversations:
        bucket = get_time_bucket(conv.timestamp, granularity)
        sentiment = calculate_conversation_sentiment(conv)
        if sentiment:
            buckets[bucket].append(sentiment["average_sentiment"])

    # Calculate average per bucket
    trend_data = []
    for bucket in sorted(buckets.keys()):
        trend_data.append({
            "period": bucket,
            "average_sentiment": mean(buckets[bucket]),
            "conversation_count": len(buckets[bucket]),
            "std_dev": stdev(buckets[bucket]) if len(buckets[bucket]) > 1 else 0
        })

    # Calculate trend direction
    if len(trend_data) >= 2:
        sentiments = [d["average_sentiment"] for d in trend_data]
        trend_direction = calculate_trend_direction(sentiments)
        trend_strength = calculate_trend_strength(sentiments)
    else:
        trend_direction = "insufficient_data"
        trend_strength = 0

    return {
        "data": trend_data,
        "direction": trend_direction,  # improving, declining, stable
        "strength": trend_strength,    # 0-1
        "period": time_period,
        "granularity": granularity
    }

def calculate_trend_direction(values):
    if len(values) < 2:
        return "insufficient_data"

    # Simple linear regression
    slope = calculate_slope(values)

    if slope > 0.02:
        return "improving"
    elif slope < -0.02:
        return "declining"
    else:
        return "stable"
```

### Segment-Level Trends
```python
def calculate_segment_trends(time_period):
    """Compare trends across segments"""

    segments = ["smb", "mid_market", "enterprise", "inbound", "outbound"]
    segment_trends = {}

    for segment in segments:
        conversations = get_conversations(time_period, segment=segment)
        trend = calculate_sentiment_trend_from_conversations(conversations)
        segment_trends[segment] = trend

    # Compare segments
    comparison = {
        "segment_trends": segment_trends,
        "best_performing": max(segment_trends, key=lambda s: segment_trends[s]["average"]),
        "worst_performing": min(segment_trends, key=lambda s: segment_trends[s]["average"]),
        "most_improved": max(segment_trends, key=lambda s: segment_trends[s].get("change", 0)),
        "most_declined": min(segment_trends, key=lambda s: segment_trends[s].get("change", 0))
    }

    return comparison
```

## Anomaly Detection

### Statistical Anomaly Detection
```python
def detect_sentiment_anomalies(trend_data, sensitivity=2):
    """Detect unusual sentiment changes"""

    anomalies = []

    # Calculate rolling statistics
    window_size = 7  # days
    for i, point in enumerate(trend_data):
        if i < window_size:
            continue

        window = trend_data[i-window_size:i]
        window_values = [d["average_sentiment"] for d in window]

        rolling_mean = mean(window_values)
        rolling_std = stdev(window_values) if len(window_values) > 1 else 0.1

        # Check if current point is anomalous
        z_score = (point["average_sentiment"] - rolling_mean) / rolling_std if rolling_std > 0 else 0

        if abs(z_score) > sensitivity:
            anomalies.append({
                "period": point["period"],
                "value": point["average_sentiment"],
                "expected": rolling_mean,
                "z_score": z_score,
                "type": "positive_anomaly" if z_score > 0 else "negative_anomaly"
            })

    return anomalies
```

### Pattern-Based Detection
```python
def detect_sentiment_patterns(trend_data):
    """Detect concerning patterns"""

    patterns = []

    # Consecutive decline
    consecutive_decline = 0
    for i in range(1, len(trend_data)):
        if trend_data[i]["average_sentiment"] < trend_data[i-1]["average_sentiment"]:
            consecutive_decline += 1
        else:
            consecutive_decline = 0

        if consecutive_decline >= 3:
            patterns.append({
                "type": "consecutive_decline",
                "duration": consecutive_decline,
                "severity": "high" if consecutive_decline >= 5 else "medium"
            })

    # Sudden drop
    for i in range(1, len(trend_data)):
        change = trend_data[i]["average_sentiment"] - trend_data[i-1]["average_sentiment"]
        if change < -0.15:
            patterns.append({
                "type": "sudden_drop",
                "period": trend_data[i]["period"],
                "magnitude": abs(change),
                "severity": "high"
            })

    # Volatility spike
    recent_volatility = calculate_volatility(trend_data[-7:])
    historical_volatility = calculate_volatility(trend_data[:-7])
    if recent_volatility > historical_volatility * 2:
        patterns.append({
            "type": "volatility_spike",
            "recent": recent_volatility,
            "historical": historical_volatility,
            "severity": "medium"
        })

    return patterns
```

## Root Cause Analysis

### Correlation Analysis
```python
def analyze_sentiment_drivers(time_period):
    """Identify what's driving sentiment changes"""

    conversations = get_conversations(time_period)

    drivers = {
        "template_correlation": {},
        "segment_correlation": {},
        "topic_correlation": {},
        "rep_correlation": {}
    }

    # Analyze by template
    by_template = defaultdict(list)
    for conv in conversations:
        template_id = conv.template_id
        sentiment = calculate_conversation_sentiment(conv)
        if sentiment:
            by_template[template_id].append(sentiment["average_sentiment"])

    for template_id, sentiments in by_template.items():
        drivers["template_correlation"][template_id] = {
            "avg_sentiment": mean(sentiments),
            "count": len(sentiments)
        }

    # Identify lowest performing templates
    drivers["worst_templates"] = sorted(
        drivers["template_correlation"].items(),
        key=lambda x: x[1]["avg_sentiment"]
    )[:5]

    return drivers
```

### Topic Sentiment Analysis
```python
def analyze_topic_sentiments(time_period):
    """Track sentiment by topic over time"""

    topics = ["pricing", "features", "support", "implementation", "competitor"]
    topic_trends = {}

    for topic in topics:
        conversations = get_conversations_mentioning(topic, time_period)
        sentiments = []

        for conv in conversations:
            topic_sentiment = extract_topic_sentiment(conv, topic)
            if topic_sentiment:
                sentiments.append({
                    "date": conv.timestamp,
                    "sentiment": topic_sentiment
                })

        if sentiments:
            topic_trends[topic] = {
                "average": mean([s["sentiment"] for s in sentiments]),
                "trend": calculate_trend_direction([s["sentiment"] for s in sentiments]),
                "count": len(sentiments)
            }

    return topic_trends
```

## Alerting

### Trend Alerts
```python
def configure_sentiment_alerts():
    return [
        {
            "name": "declining_trend",
            "condition": lambda t: t["direction"] == "declining" and t["strength"] > 0.3,
            "message": "Sentiment showing significant decline",
            "severity": "high"
        },
        {
            "name": "sudden_drop",
            "condition": lambda t: any(a["type"] == "sudden_drop" for a in t.get("anomalies", [])),
            "message": "Sudden sentiment drop detected",
            "severity": "high"
        },
        {
            "name": "segment_divergence",
            "condition": lambda t: segment_divergence(t) > 0.2,
            "message": "Significant sentiment divergence between segments",
            "severity": "medium"
        },
        {
            "name": "template_outlier",
            "condition": lambda t: has_template_outlier(t),
            "message": "Template with significantly lower sentiment",
            "severity": "medium"
        }
    ]

def check_and_alert(trend_analysis):
    for alert_config in configured_alerts:
        if alert_config["condition"](trend_analysis):
            send_alert(
                name=alert_config["name"],
                message=alert_config["message"],
                severity=alert_config["severity"],
                data=trend_analysis
            )
```

## Visualization

### Trend Dashboard
```python
def generate_sentiment_dashboard(time_period):
    return {
        "overall_trend": calculate_sentiment_trend(time_period),
        "segment_comparison": calculate_segment_trends(time_period),
        "anomalies": detect_sentiment_anomalies(trend_data),
        "patterns": detect_sentiment_patterns(trend_data),
        "drivers": analyze_sentiment_drivers(time_period),
        "topic_breakdown": analyze_topic_sentiments(time_period),
        "alerts": get_active_alerts(),
        "recommendations": generate_recommendations()
    }
```

## Metrics

### Trend Health Metrics
```
Track:
- 7-day sentiment average
- 30-day sentiment trend
- Segment sentiment variance
- Template sentiment variance
- Topic sentiment breakdown

Alert thresholds:
- >10% decline over 7 days
- >20% decline over 30 days
- >0.3 variance between segments
```

