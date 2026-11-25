---
name: propensity-scoring-realtime
description: When the user wants to build or improve a sales bot's ability to update lead scores dynamically during conversations. Also use when the user mentions "real-time scoring," "dynamic lead scoring," "propensity scoring," "live scoring," or "conversation scoring."
---

# Propensity Scoring in Real-Time

You are an expert in building sales bots that dynamically update lead scores as conversations progress. Your goal is to help developers create systems that re-evaluate prospect quality with every interaction.

## Why Real-Time Scoring Matters

### Static Scoring Limitations
```
Traditional lead scoring:
- Scored once at creation
- Based on firmographics only
- Doesn't reflect engagement
- Score stale by first conversation

Lead created at score 75 (based on company size).
Three weeks later, still 75, even after:
- Ignored 5 emails
- Bounced from website
- Never responded

Should be much lower.
```

### Real-Time Scoring
```
Dynamic scoring:
- Updates with every signal
- Reflects actual engagement
- Predicts current likelihood
- Enables smart prioritization

Lead starts at 75.
After engagement signals:
- Opened 3 emails: +10
- Clicked pricing: +15
- Asked about timeline: +20
- Mentioned budget: +25

New score: 145 (high priority)
```

## Scoring Components

### Firmographic Baseline
```
Starting score based on fit:

Company size:
- <10 employees: +10
- 10-50: +20
- 51-200: +30
- 201-1000: +40
- 1000+: +50

Industry fit:
- Ideal industry: +30
- Good fit: +20
- Neutral: +10
- Poor fit: 0

Title/Role:
- Decision maker: +30
- Influencer: +20
- User: +10
- Unknown: +5
```

### Engagement Signals
```
Real-time adjustments:

Email engagement:
- Opened: +5 per open
- Clicked: +10 per click
- Replied: +25
- Positive reply: +40

Website behavior:
- Page visit: +3
- Pricing page: +15
- Demo page: +20
- Multiple pages: +5 per page
- Return visit: +10

Content engagement:
- Downloaded: +15
- Video watched: +10 per 25% completion
- Webinar registered: +20
- Webinar attended: +35
```

### Conversation Signals
```
From bot conversations:

Questions asked:
- Feature question: +5
- Pricing question: +20
- Timeline question: +25
- Implementation: +20
- Competitor mention: +15

Buying signals:
- "We need": +15
- "When can we": +20
- "Who else uses": +10
- "What's the process": +25
- Budget mentioned: +30

Objection signals:
- Price objection: -5 (but engaged)
- Timing objection: -10
- "Not interested": -30
- Unsubscribe request: -50
```

## Real-Time Implementation

### Score Calculation Engine
```python
class PropensityScorer:
    def __init__(self, prospect):
        self.prospect = prospect
        self.base_score = self.calculate_base_score()
        self.engagement_score = 0
        self.conversation_score = 0
        self.decay_factor = 0

    def calculate_base_score(self):
        score = 0
        score += COMPANY_SIZE_SCORES.get(self.prospect.company_size_bucket, 10)
        score += INDUSTRY_SCORES.get(self.prospect.industry, 10)
        score += TITLE_SCORES.get(self.prospect.title_level, 5)
        return score

    def update_on_event(self, event):
        """Called in real-time when events occur"""

        # Get score delta for event type
        delta = EVENT_SCORES.get(event.type, 0)

        # Apply context multipliers
        if event.recency < timedelta(hours=1):
            delta *= 1.5  # Recent activity bonus
        if event.context.get("high_intent_page"):
            delta *= 1.3

        # Update appropriate component
        if event.category == "engagement":
            self.engagement_score += delta
        elif event.category == "conversation":
            self.conversation_score += delta

        # Apply decay to old scores
        self.apply_decay()

        # Emit score update event
        self.emit_score_change()

    def get_current_score(self):
        return (
            self.base_score +
            self.engagement_score +
            self.conversation_score -
            self.decay_factor
        )

    def get_score_tier(self):
        score = self.get_current_score()
        if score >= 100:
            return "hot"
        elif score >= 60:
            return "warm"
        elif score >= 30:
            return "cool"
        else:
            return "cold"
```

### Event Processing Pipeline
```python
class ScoreEventProcessor:
    def __init__(self):
        self.scorers = {}

    def process_event(self, event):
        prospect_id = event.prospect_id

        # Get or create scorer
        if prospect_id not in self.scorers:
            prospect = load_prospect(prospect_id)
            self.scorers[prospect_id] = PropensityScorer(prospect)

        scorer = self.scorers[prospect_id]

        # Update score
        old_score = scorer.get_current_score()
        scorer.update_on_event(event)
        new_score = scorer.get_current_score()

        # Check for tier changes
        old_tier = get_tier(old_score)
        new_tier = get_tier(new_score)

        if new_tier != old_tier:
            self.handle_tier_change(prospect_id, old_tier, new_tier)

        # Persist score
        update_prospect_score(prospect_id, new_score, new_tier)

        return {
            "prospect_id": prospect_id,
            "old_score": old_score,
            "new_score": new_score,
            "tier_change": new_tier != old_tier
        }

    def handle_tier_change(self, prospect_id, old_tier, new_tier):
        if new_tier == "hot" and old_tier != "hot":
            # Alert rep
            notify_rep(prospect_id, "Lead became hot")
            # Accelerate sequence
            accelerate_outreach(prospect_id)

        elif new_tier == "cold" and old_tier != "cold":
            # Slow down outreach
            decelerate_outreach(prospect_id)
```

### Conversation Score Updates
```python
def update_score_from_message(conversation_id, message):
    """Update score based on conversation content"""

    prospect_id = get_prospect_id(conversation_id)
    scorer = get_scorer(prospect_id)

    # Analyze message for signals
    signals = analyze_message_signals(message)

    for signal in signals:
        event = ConversationEvent(
            type=signal.type,
            category="conversation",
            value=signal.value,
            context=signal.context
        )
        scorer.update_on_event(event)

    return scorer.get_current_score()

def analyze_message_signals(message):
    signals = []

    # Buying signals
    buying_patterns = [
        (r"what('s| is) the (price|cost|pricing)", "pricing_question", 20),
        (r"when can we (start|begin|implement)", "timeline_question", 25),
        (r"(we need|we're looking for)", "stated_need", 15),
        (r"who else (uses|is using)", "social_proof_request", 10),
        (r"(budget|allocated|set aside)", "budget_mention", 30)
    ]

    for pattern, signal_type, value in buying_patterns:
        if re.search(pattern, message.lower()):
            signals.append(Signal(type=signal_type, value=value))

    # Negative signals
    negative_patterns = [
        (r"not interested", "not_interested", -30),
        (r"stop (emailing|contacting)", "opt_out_request", -50),
        (r"too expensive", "price_objection", -5),
        (r"maybe (later|next year)", "timing_objection", -10)
    ]

    for pattern, signal_type, value in negative_patterns:
        if re.search(pattern, message.lower()):
            signals.append(Signal(type=signal_type, value=value))

    return signals
```

## Score Decay

### Time-Based Decay
```python
def calculate_decay(last_activity, base_decay_rate=0.02):
    """Score decays over time without activity"""

    days_since_activity = (now() - last_activity).days

    # No decay for recent activity
    if days_since_activity < 7:
        return 0

    # Gradual decay
    decay = (days_since_activity - 7) * base_decay_rate

    # Cap decay
    return min(decay, 0.5)  # Max 50% decay
```

### Engagement Decay
```python
def decay_engagement_score(scorer):
    """Recent engagement matters more"""

    events = scorer.get_engagement_events()
    decayed_score = 0

    for event in events:
        age_days = (now() - event.timestamp).days

        if age_days < 7:
            weight = 1.0
        elif age_days < 30:
            weight = 0.7
        elif age_days < 90:
            weight = 0.4
        else:
            weight = 0.1

        decayed_score += event.score_delta * weight

    return decayed_score
```

## Score-Based Actions

### Routing by Score
```python
def route_prospect(prospect):
    score = prospect.current_score
    tier = prospect.score_tier

    if tier == "hot":
        return {
            "queue": "immediate_follow_up",
            "assignee": "senior_ae",
            "urgency": "high",
            "action": "call_within_1_hour"
        }
    elif tier == "warm":
        return {
            "queue": "standard_follow_up",
            "assignee": "sdr",
            "urgency": "medium",
            "action": "email_within_24_hours"
        }
    elif tier == "cool":
        return {
            "queue": "nurture_sequence",
            "assignee": "bot",
            "urgency": "low",
            "action": "automated_nurture"
        }
    else:  # cold
        return {
            "queue": "re_engagement",
            "assignee": "bot",
            "urgency": "lowest",
            "action": "monthly_check_in"
        }
```

### Dynamic Sequence Adjustment
```python
def adjust_sequence_for_score(prospect, sequence):
    score = prospect.current_score

    if score >= 100:
        # High intent - accelerate
        return modify_sequence(sequence,
            interval_multiplier=0.5,  # Faster
            add_phone_touches=True,
            urgency_messaging=True
        )
    elif score >= 60:
        # Warm - standard pace
        return sequence
    elif score >= 30:
        # Cool - slow down
        return modify_sequence(sequence,
            interval_multiplier=1.5,  # Slower
            value_focused_messaging=True
        )
    else:
        # Cold - minimal contact
        return modify_sequence(sequence,
            interval_multiplier=3.0,  # Much slower
            re_engagement_messaging=True
        )
```

## Visualization & Reporting

### Score Timeline
```python
def get_score_timeline(prospect_id, days=30):
    """Visualize score changes over time"""

    events = get_score_events(prospect_id, days=days)

    timeline = []
    running_score = get_initial_score(prospect_id, days)

    for event in events:
        running_score += event.delta
        timeline.append({
            "timestamp": event.timestamp,
            "score": running_score,
            "event": event.type,
            "delta": event.delta
        })

    return timeline

# Output for charting:
# [
#   {"timestamp": "2024-01-01", "score": 50, "event": "created", "delta": 50},
#   {"timestamp": "2024-01-05", "score": 65, "event": "email_opened", "delta": 15},
#   {"timestamp": "2024-01-06", "score": 90, "event": "pricing_question", "delta": 25},
#   ...
# ]
```

### Score Distribution Report
```python
def generate_score_report():
    all_prospects = get_all_active_prospects()

    return {
        "distribution": {
            "hot": len([p for p in all_prospects if p.tier == "hot"]),
            "warm": len([p for p in all_prospects if p.tier == "warm"]),
            "cool": len([p for p in all_prospects if p.tier == "cool"]),
            "cold": len([p for p in all_prospects if p.tier == "cold"])
        },
        "average_score": mean([p.score for p in all_prospects]),
        "score_changes_today": count_tier_changes(today()),
        "top_movers": get_biggest_score_increases(limit=10),
        "at_risk": get_biggest_score_decreases(limit=10)
    }
```

## Model Calibration

### Score Validation
```python
def validate_score_model():
    """Check if scores predict outcomes"""

    # Get closed deals
    won = get_closed_won_last_90_days()
    lost = get_closed_lost_last_90_days()

    # Analyze scores at various stages
    won_scores_at_qualification = [d.score_at_stage("qualified") for d in won]
    lost_scores_at_qualification = [d.score_at_stage("qualified") for d in lost]

    # Scores should differentiate winners from losers
    avg_won = mean(won_scores_at_qualification)
    avg_lost = mean(lost_scores_at_qualification)

    if avg_won <= avg_lost:
        alert("Score model not predictive - won deals don't score higher")

    # Check tier conversion rates
    for tier in ["hot", "warm", "cool", "cold"]:
        conversion = conversion_rate_by_tier(tier)
        expected = EXPECTED_CONVERSION_BY_TIER[tier]
        if abs(conversion - expected) > 0.1:
            alert(f"Tier {tier} conversion {conversion} differs from expected {expected}")
```

