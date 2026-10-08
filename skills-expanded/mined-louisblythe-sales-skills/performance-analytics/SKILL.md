---
name: performance-analytics
description: When the user wants to build or improve a sales bot's ability to track conversion rates, drop-off points, and response patterns. Also use when the user mentions "bot analytics," "conversation metrics," "tracking performance," "measuring bot effectiveness," or "conversion tracking."
---

# Performance Analytics for Sales Bots

You are an expert in building analytics systems for automated sales. Your goal is to help design systems that track conversion rates, identify drop-off points, and reveal response patterns to continuously improve bot performance.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What does your bot do (qualify, book, sell)?
   - What volume of conversations do you have?
   - What analytics do you have today?

2. **Current State**
   - What metrics are you tracking?
   - Where is data flowing?
   - What insights are you missing?

3. **Goals**
   - What decisions will analytics inform?
   - What does success look like?

---

## Core Principles

### 1. Measure What Matters
- Not everything measurable matters
- Focus on actionable metrics
- Tie to business outcomes

### 2. Context is Key
- Raw numbers mislead
- Segment and compare
- Understand the why

### 3. Build for Action
- Dashboards that drive decisions
- Alerts for anomalies
- Clear improvement paths

### 4. Iterate and Learn
- Analytics should evolve
- New questions require new metrics
- Continuous improvement

---

## Key Metrics Framework

### Volume Metrics

**Conversations:**
- Total conversations started
- Conversations by channel
- Conversations by time period
- Inbound vs. outbound

**Messages:**
- Messages per conversation
- Bot messages vs. human messages
- Response rate

### Conversion Metrics

**Funnel stages:**
- Response rate
- Engagement rate
- Qualification rate
- Meeting booking rate
- Conversion rate

**By outcome:**
- Qualified leads generated
- Meetings booked
- Deals closed
- Revenue attributed

### Quality Metrics

**Conversation quality:**
- Sentiment trajectory
- Customer satisfaction score
- Human takeover rate
- Resolution rate

**Bot performance:**
- Understanding accuracy
- Response appropriateness
- Fallback rate
- Error rate

### Efficiency Metrics

**Speed:**
- Response time
- Time to qualification
- Time to booking
- Conversation duration

**Automation:**
- % conversations fully automated
- Human intervention rate
- Touches per conversion

---

## Funnel Analysis

### Building the Funnel

```
Conversation Started
        ↓
First Response Received
        ↓
Qualified (met criteria)
        ↓
Meeting Booked
        ↓
Meeting Attended
        ↓
Opportunity Created
        ↓
Deal Closed
```

### Calculating Conversion Rates

```
function calculateFunnelMetrics(period) {
  conversations = getConversations(period)

  metrics = {
    started: conversations.count(),
    responded: conversations.filter(c => c.got_response).count(),
    qualified: conversations.filter(c => c.is_qualified).count(),
    booked: conversations.filter(c => c.meeting_booked).count(),
    attended: conversations.filter(c => c.meeting_attended).count(),
    converted: conversations.filter(c => c.became_customer).count()
  }

  metrics.response_rate = metrics.responded / metrics.started
  metrics.qualification_rate = metrics.qualified / metrics.responded
  metrics.booking_rate = metrics.booked / metrics.qualified
  metrics.show_rate = metrics.attended / metrics.booked
  metrics.conversion_rate = metrics.converted / metrics.attended

  return metrics
}
```

### Identifying Drop-Off Points

```
function findDropOffPoints(funnel) {
  stages = ["started", "responded", "qualified", "booked", "attended", "converted"]
  drop_offs = []

  for (i = 0; i < stages.length - 1; i++) {
    current = funnel[stages[i]]
    next = funnel[stages[i + 1]]
    drop_rate = 1 - (next / current)

    if (drop_rate > THRESHOLD) {
      drop_offs.push({
        from: stages[i],
        to: stages[i + 1],
        drop_rate: drop_rate,
        volume_lost: current - next
      })
    }
  }

  return drop_offs.sort(by_drop_rate_desc)
}
```

---

## Conversation Analytics

### Message-Level Tracking

**Track for each message:**
- Timestamp
- Sender (bot or human)
- Content
- Intent detected
- Sentiment score
- Confidence level
- Response time

### Conversation-Level Aggregation

```
ConversationMetrics = {
  id: string,
  channel: string,
  started_at: timestamp,
  ended_at: timestamp,
  duration_seconds: number,
  message_count: number,
  bot_messages: number,
  human_messages: number,
  sentiment_start: float,
  sentiment_end: float,
  sentiment_trend: float,  // end - start
  intents_detected: [string],
  objections_raised: [string],
  qualification_score: number,
  outcome: string,  // qualified, disqualified, booked, escalated, etc.
  escalated: boolean,
  escalation_reason: string,
  fallback_count: number
}
```

### Pattern Detection

```
function findConversationPatterns(conversations) {
  patterns = {
    successful: [],
    failed: [],
    common_paths: [],
    common_objections: [],
    common_drop_points: []
  }

  // Analyze successful conversations
  successful = conversations.filter(c => c.outcome == "converted")
  patterns.successful = extractCommonPatterns(successful)

  // Analyze failed conversations
  failed = conversations.filter(c => c.outcome in ["dropped", "disqualified"])
  patterns.failed = extractCommonPatterns(failed)

  // Find where conversations diverge
  patterns.divergence_points = findDivergencePoints(successful, failed)

  return patterns
}
```

---

## Segmented Analysis

### Segmentation Dimensions

**By channel:**
- SMS vs. email vs. chat
- Inbound vs. outbound
- Paid vs. organic

**By prospect:**
- Industry
- Company size
- Role/seniority
- Geography

**By time:**
- Day of week
- Time of day
- Week over week
- Month over month

**By content:**
- First message variant
- Qualification path
- Objections encountered

### Segment Comparison

```
function compareSegments(metric, segments) {
  results = []

  for (segment in segments) {
    data = getData(segment)
    result = {
      segment: segment.name,
      value: calculate(metric, data),
      sample_size: data.count(),
      confidence: calculateConfidence(data)
    }
    results.push(result)
  }

  // Statistical comparison
  return {
    segments: results,
    best_performing: findBest(results),
    significant_differences: findSignificantDifferences(results)
  }
}
```

---

## Real-Time Monitoring

### Key Alerts

**Volume alerts:**
- Conversation volume drop
- Response rate drop
- Unusual spikes

**Quality alerts:**
- Sentiment declining
- Fallback rate increasing
- Error rate increasing

**Performance alerts:**
- Conversion rate drop
- Booking rate drop
- Escalation rate spike

### Alert Configuration

```
alerts = [
  {
    metric: "response_rate",
    condition: "drops_below",
    threshold: 0.5,
    window: "1_hour",
    severity: "high"
  },
  {
    metric: "fallback_rate",
    condition: "exceeds",
    threshold: 0.2,
    window: "4_hours",
    severity: "medium"
  },
  {
    metric: "sentiment_average",
    condition: "drops_below",
    threshold: -0.2,
    window: "1_hour",
    severity: "high"
  }
]
```

---

## Dashboard Design

### Executive Dashboard

**Key questions answered:**
- How many leads is the bot generating?
- What's our conversion rate?
- How is performance trending?

**Metrics:**
- Conversations (total, trend)
- Qualified leads (total, rate)
- Meetings booked (total, rate)
- Conversion rate (trend)
- Revenue attributed

### Operations Dashboard

**Key questions answered:**
- Where are conversations dropping off?
- What's causing escalations?
- What needs fixing?

**Metrics:**
- Funnel with drop-off rates
- Escalation rate and reasons
- Fallback rate and triggers
- Error rate and types
- Response time distribution

### Optimization Dashboard

**Key questions answered:**
- What's working best?
- What should we test?
- What can we improve?

**Metrics:**
- A/B test results
- Best performing messages
- Worst performing messages
- Segment performance comparison
- Pattern analysis

---

## Data Infrastructure

### Event Tracking

```
// Track all meaningful events
trackEvent({
  event_type: "conversation_started",
  conversation_id: "abc123",
  channel: "sms",
  timestamp: now(),
  properties: {
    source: "website_form",
    lead_score: 72
  }
})

trackEvent({
  event_type: "message_received",
  conversation_id: "abc123",
  message_id: "msg456",
  timestamp: now(),
  properties: {
    sender: "prospect",
    content: "...",
    intent: "interested",
    intent_confidence: 0.87,
    sentiment: 0.3
  }
})

trackEvent({
  event_type: "meeting_booked",
  conversation_id: "abc123",
  timestamp: now(),
  properties: {
    meeting_date: "2024-01-15",
    meeting_type: "demo",
    assigned_rep: "rep_789"
  }
})
```

### Data Pipeline

```
Events → Queue → Processing → Storage
                     ↓
              Aggregation
                     ↓
              Dashboards
                     ↓
                 Alerts
```

### Storage Schema

```
conversations:
  - id, channel, started_at, ended_at, outcome, ...

messages:
  - id, conversation_id, timestamp, sender, content, intent, sentiment, ...

events:
  - id, conversation_id, event_type, timestamp, properties

metrics_daily:
  - date, metric_name, segment, value

metrics_hourly:
  - timestamp, metric_name, segment, value
```

---

## Improvement Loop

### Weekly Review Process

1. **Review dashboards**
   - Key metrics vs. targets
   - Week over week trends
   - Anomalies and issues

2. **Analyze drop-offs**
   - Where are we losing people?
   - Why are they dropping?
   - What can we test?

3. **Review conversations**
   - Sample failed conversations
   - Sample successful conversations
   - Identify patterns

4. **Plan improvements**
   - Prioritize opportunities
   - Design tests
   - Implement changes

### Monthly Deep Dive

- Cohort analysis
- Segment performance review
- A/B test portfolio review
- Roadmap prioritization

---

## Common Mistakes

### 1. Vanity Metrics
**Problem:** Tracking things that don't matter
**Fix:** Connect every metric to business outcome

### 2. No Segmentation
**Problem:** Looking only at averages
**Fix:** Always segment to find insights

### 3. No Context
**Problem:** Numbers without meaning
**Fix:** Compare to benchmarks, trends, segments

### 4. Analysis Paralysis
**Problem:** Too much data, no action
**Fix:** Focus on actionable insights

### 5. Outdated Dashboards
**Problem:** Building once, never updating
**Fix:** Regular review and iteration

---

## Implementation Checklist

### Phase 1: Foundation
- [ ] Event tracking for all interactions
- [ ] Basic funnel metrics
- [ ] Conversion tracking
- [ ] Simple dashboard

### Phase 2: Analysis
- [ ] Segmentation capability
- [ ] Pattern detection
- [ ] Drop-off analysis
- [ ] A/B test tracking

### Phase 3: Optimization
- [ ] Real-time monitoring
- [ ] Automated alerts
- [ ] Predictive insights
- [ ] Continuous improvement loop

---

## Questions to Ask

If you need more context:
1. What analytics do you have today?
2. What decisions will analytics inform?
3. What volume of conversations do you handle?
4. What tools/infrastructure do you use?
5. Who will use these analytics?

---

## Related Skills

- **ab-message-testing**: Testing variations
- **lead-qualification-logic**: Qualification metrics
- **conversational-flow-management**: Flow optimization
- **intent-detection**: Understanding accuracy
