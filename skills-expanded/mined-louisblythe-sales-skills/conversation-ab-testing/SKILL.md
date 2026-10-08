---
name: conversation-ab-testing
description: When the user wants to build or improve a sales bot's ability to test individual message variants. Also use when the user mentions "message testing," "A/B testing messages," "variant testing," "message optimization," or "reply testing."
---

# Conversation A/B Testing at the Message Level

You are an expert in building sales bots that test individual message variants within conversations. Your goal is to help developers create systems that optimize not just sequences, but individual replies for maximum effectiveness.

## Why Message-Level Testing Matters

### Sequence-Level Limitations
```
Testing whole sequences:
- Email 1 + Email 2 + Email 3 = Sequence A
- Need hundreds of sends per variant
- Slow to reach significance
- Don't know which message made the difference

Sequence A: 5% reply rate
Sequence B: 7% reply rate
Which message drove the improvement? Unknown.
```

### Message-Level Testing
```
Testing individual messages:
- Test Email 1 variants across all sequences
- Reach significance faster
- Know exactly what works
- Compound improvements

Email 1A: 15% open, 2% reply
Email 1B: 18% open, 3% reply
Clear winner, immediately usable.
```

## Test Types

### Subject Line Tests
```
Test variants:
A: "Quick question about [Company]"
B: "[Name], question about [pain point]"
C: "Saw your post on [topic]"

Metrics:
- Open rate (primary)
- Reply rate (secondary)
- Spam rate (guardrail)

Sample size: 50-100 per variant minimum
```

### Opening Line Tests
```
Test variants:
A: "I noticed [Company] just [event]..."
B: "Fellow [industry] professional here..."
C: "Not sure if this is relevant, but..."

Metrics:
- Reply rate (primary)
- Positive vs negative replies
- Conversation continuation
```

### CTA Tests
```
Test variants:
A: "Worth a 15-minute call?"
B: "Open to learning more?"
C: "What's the best way to continue this?"
D: "Reply with 'yes' if interested"

Metrics:
- Reply rate
- Meeting conversion
- Quality of responses
```

### Tone/Style Tests
```
Test variants:
A: Formal professional
B: Casual conversational
C: Direct and brief
D: Storytelling approach

Metrics:
- Engagement rate
- Sentiment of responses
- Conversion to meeting
```

## Implementation

### Test Architecture
```python
class MessageABTest:
    def __init__(self, test_config):
        self.test_id = generate_id()
        self.variants = test_config.variants
        self.metrics = test_config.metrics
        self.traffic_split = test_config.split  # e.g., [0.5, 0.5]
        self.min_sample = test_config.min_sample
        self.status = "running"
        self.results = {v.id: {"sent": 0, "results": {}} for v in self.variants}

    def select_variant(self, context):
        if self.should_use_winner():
            return self.get_winner()

        # Random assignment with traffic split
        rand = random.random()
        cumulative = 0
        for i, split in enumerate(self.traffic_split):
            cumulative += split
            if rand < cumulative:
                return self.variants[i]

    def record_result(self, variant_id, metric, value):
        self.results[variant_id]["results"].setdefault(metric, []).append(value)
        self.results[variant_id]["sent"] += 1
        self.check_significance()

    def check_significance(self):
        if all(v["sent"] >= self.min_sample for v in self.results.values()):
            winner = self.calculate_winner()
            if winner and winner["confidence"] >= 0.95:
                self.status = "completed"
                self.winner = winner
```

### Variant Selection Logic
```python
def select_message_variant(message_type, context):
    # Find active tests for this message type
    active_tests = get_active_tests(message_type)

    if not active_tests:
        return get_default_message(message_type, context)

    # Select test (if multiple, pick highest priority)
    test = select_test(active_tests, context)

    # Get variant assignment
    variant = test.select_variant(context)

    # Log assignment for tracking
    log_test_assignment(
        test_id=test.test_id,
        variant_id=variant.id,
        context_id=context.conversation_id
    )

    return variant.content
```

### Result Tracking
```python
def track_message_result(message_id, event):
    # Get test assignment
    assignment = get_test_assignment(message_id)
    if not assignment:
        return

    test = get_test(assignment.test_id)

    # Map event to metric
    metric_map = {
        "opened": "open_rate",
        "clicked": "click_rate",
        "replied": "reply_rate",
        "meeting_booked": "conversion_rate",
        "positive_reply": "positive_sentiment_rate"
    }

    metric = metric_map.get(event.type)
    if metric:
        test.record_result(
            variant_id=assignment.variant_id,
            metric=metric,
            value=event.value
        )
```

## Statistical Analysis

### Sample Size Calculation
```python
def calculate_sample_size(baseline_rate, min_detectable_effect, power=0.8, alpha=0.05):
    """
    baseline_rate: Current conversion rate (e.g., 0.02 for 2%)
    min_detectable_effect: Minimum relative improvement to detect (e.g., 0.2 for 20%)
    """
    from scipy import stats

    p1 = baseline_rate
    p2 = baseline_rate * (1 + min_detectable_effect)
    effect_size = abs(p2 - p1) / ((p1 * (1-p1) + p2 * (1-p2)) / 2) ** 0.5

    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)

    n = 2 * ((z_alpha + z_beta) / effect_size) ** 2
    return int(n)

# Example:
# Baseline: 2% reply rate
# Want to detect 25% relative improvement (2% → 2.5%)
# Need ~3,200 sends per variant
```

### Significance Testing
```python
def test_significance(variant_a_results, variant_b_results, metric):
    from scipy import stats

    a_successes = sum(variant_a_results[metric])
    a_trials = len(variant_a_results[metric])
    b_successes = sum(variant_b_results[metric])
    b_trials = len(variant_b_results[metric])

    # Chi-square test for proportions
    contingency = [
        [a_successes, a_trials - a_successes],
        [b_successes, b_trials - b_successes]
    ]

    chi2, p_value, dof, expected = stats.chi2_contingency(contingency)

    return {
        "variant_a_rate": a_successes / a_trials,
        "variant_b_rate": b_successes / b_trials,
        "p_value": p_value,
        "significant": p_value < 0.05,
        "winner": "A" if a_successes/a_trials > b_successes/b_trials else "B"
    }
```

### Multi-Armed Bandit
```python
class ThompsonSampling:
    """
    Balances exploration vs exploitation during testing.
    Automatically shifts traffic to winning variants.
    """
    def __init__(self, variants):
        self.variants = variants
        self.successes = {v: 1 for v in variants}  # Prior
        self.failures = {v: 1 for v in variants}   # Prior

    def select_variant(self):
        samples = {}
        for variant in self.variants:
            # Sample from beta distribution
            samples[variant] = random.betavariate(
                self.successes[variant],
                self.failures[variant]
            )
        return max(samples, key=samples.get)

    def update(self, variant, success):
        if success:
            self.successes[variant] += 1
        else:
            self.failures[variant] += 1
```

## Test Management

### Test Lifecycle
```
1. Hypothesis: "Personalized subject lines increase open rates"
2. Design: Create variants A and B
3. Configure: Set metrics, sample size, traffic split
4. Launch: Begin test
5. Monitor: Track interim results
6. Analyze: Check for significance
7. Conclude: Declare winner or inconclusive
8. Deploy: Roll out winner, archive loser
```

### Concurrent Test Management
```python
def can_run_test(new_test, active_tests):
    """Prevent test interference"""

    for test in active_tests:
        # Same message position = conflict
        if test.message_position == new_test.message_position:
            return False, "Conflict with existing test at same position"

        # Same audience segment = potential conflict
        if overlaps(test.audience, new_test.audience) > 0.5:
            return False, "Audience overlap >50% with active test"

    return True, None

def prioritize_tests(tests, context):
    """When multiple tests could apply, pick one"""

    eligible = [t for t in tests if t.matches_context(context)]

    if not eligible:
        return None

    # Priority: Lower sample progress = higher priority (needs more data)
    return min(eligible, key=lambda t: t.sample_progress)
```

## Metrics & Reporting

### Test Dashboard
```python
def generate_test_report(test_id):
    test = get_test(test_id)

    return {
        "test_info": {
            "id": test.test_id,
            "hypothesis": test.hypothesis,
            "start_date": test.started_at,
            "status": test.status
        },
        "variants": [
            {
                "id": v.id,
                "description": v.description,
                "sent": test.results[v.id]["sent"],
                "metrics": calculate_metrics(test.results[v.id])
            }
            for v in test.variants
        ],
        "significance": {
            "is_significant": test.is_significant,
            "p_value": test.p_value,
            "confidence": test.confidence,
            "winner": test.winner
        },
        "recommendation": generate_recommendation(test)
    }
```

### Automated Insights
```python
def generate_insights(completed_tests):
    insights = []

    # Pattern detection across tests
    personalization_tests = [t for t in completed_tests if "personalization" in t.tags]
    if personalization_tests:
        personalized_wins = sum(1 for t in personalization_tests if t.personalized_won)
        insights.append({
            "insight": f"Personalization won {personalized_wins}/{len(personalization_tests)} tests",
            "recommendation": "Prioritize personalization in messages"
        })

    # Identify winning patterns
    winning_variants = [t.winning_variant for t in completed_tests]
    common_patterns = extract_common_patterns(winning_variants)
    for pattern in common_patterns:
        insights.append({
            "insight": f"Pattern '{pattern}' appears in {pattern.frequency}% of winners",
            "recommendation": f"Include '{pattern}' in message templates"
        })

    return insights
```

## Best Practices

### Test Design
```
1. One variable at a time
   - Don't test subject + body + CTA together
   - Isolate the variable

2. Meaningful differences
   - Don't test "Hi" vs "Hello"
   - Test different approaches

3. Representative samples
   - Random assignment
   - Avoid segment bias

4. Sufficient sample size
   - Calculate before starting
   - Wait for significance
```

### Common Pitfalls
```
Avoid:
- Peeking and stopping early
- Running too many tests at once
- Testing tiny differences
- Ignoring secondary metrics
- Not accounting for seasonality

Do:
- Pre-register hypothesis
- Set sample size in advance
- Consider all relevant metrics
- Account for time-based factors
```

