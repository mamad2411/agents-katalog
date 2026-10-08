---
name: ab-message-testing
description: When the user wants to build or improve a sales bot's ability to automatically test message variations to optimize conversion. Also use when the user mentions "message testing," "A/B testing bots," "optimizing bot messages," "testing variations," or "message optimization."
---

# A/B Message Testing for Sales Bots

You are an expert in building automated testing systems for sales bots. Your goal is to help design systems that automatically test message variations to optimize conversion rates.

## Initial Assessment

Before providing guidance, understand:

1. **Context**
   - What volume of conversations does your bot handle?
   - What outcomes are you trying to optimize?
   - What messages are currently underperforming?

2. **Current State**
   - Are you running any tests today?
   - How do you decide what messages to send?
   - What data do you have on message performance?

3. **Goals**
   - What would better testing help you achieve?
   - What metrics matter most?

---

## Core Principles

### 1. Test Everything That Matters
- Small changes can have big impacts
- Don't assume you know what works
- Let data decide

### 2. Statistical Rigor
- Enough sample size
- Long enough duration
- Proper randomization

### 3. One Variable at a Time
- Isolate what changed
- Otherwise you don't know what worked
- Test sequentially, not simultaneously

### 4. Continuous Optimization
- Testing is ongoing
- Winners become new baseline
- Always be testing something

---

## What to Test

### Message Content

**Opening messages:**
- Greeting style
- Value proposition
- Question vs. statement
- Personalization level

**Response messages:**
- Tone and voice
- Length
- Structure
- CTAs

**Objection responses:**
- Acknowledgment style
- Reframe approach
- Proof points
- Follow-up questions

### Message Structure

**Length:**
- Short vs. detailed
- Single message vs. chunked
- Number of sentences

**Format:**
- With vs. without bullets
- With vs. without emoji
- Question at end vs. not

**Tone:**
- Formal vs. casual
- Enthusiastic vs. calm
- Direct vs. soft

### Conversation Flow

**Question order:**
- Qualification order
- Easy first vs. hard first
- Building vs. direct

**Branching:**
- Different paths
- Skip logic
- Progressive disclosure

---

## Test Architecture

### Basic A/B Test

```
Contact arrives
       ↓
  Random assignment (50/50)
       ↓
    ┌──────┴──────┐
    ↓             ↓
 Variant A    Variant B
    ↓             ↓
   Track        Track
    ↓             ↓
  Analyze results
       ↓
  Implement winner
```

### Multi-Variant Test

**When to use:**
- High volume
- Testing multiple ideas
- Want faster learning

**Structure:**
- Control: 40%
- Variant A: 20%
- Variant B: 20%
- Variant C: 20%

### Sequential Testing

**When to use:**
- Lower volume
- Need faster decisions
- Willing to accept more risk

**Structure:**
- Monitor continuously
- Stop when clear winner emerges
- Use adaptive algorithms

---

## Implementation

### Randomization

```
function assignVariant(contact_id, test_id, variants) {
  // Consistent assignment (same contact always gets same variant)
  hash = md5(contact_id + test_id)
  bucket = hash % 100

  cumulative = 0
  for (variant in variants) {
    cumulative += variant.percentage
    if (bucket < cumulative) {
      return variant.name
    }
  }
}
```

### Message Selection

```
function getMessage(context, message_key) {
  // Check for active test
  test = getActiveTest(message_key)
  if (!test) {
    return getDefaultMessage(message_key)
  }

  // Get variant assignment
  variant = assignVariant(context.contact_id, test.id, test.variants)

  // Return variant message
  return test.variants[variant].message
}
```

### Result Tracking

```
function trackResult(contact_id, test_id, variant, outcome) {
  result = {
    contact_id: contact_id,
    test_id: test_id,
    variant: variant,
    outcome: outcome,  // responded, converted, dropped, etc.
    timestamp: now()
  }
  store(result)
  updateTestStats(test_id, variant, outcome)
}
```

---

## Statistical Analysis

### Sample Size Calculation

**Inputs needed:**
- Baseline conversion rate
- Minimum detectable effect (MDE)
- Statistical significance (typically 95%)
- Statistical power (typically 80%)

**Quick reference:**

| Baseline Rate | 10% Lift | 20% Lift | 50% Lift |
|---------------|----------|----------|----------|
| 5% | 30,000/variant | 7,500/variant | 1,200/variant |
| 10% | 14,000/variant | 3,500/variant | 560/variant |
| 20% | 6,400/variant | 1,600/variant | 260/variant |

### Significance Testing

```
function isSignificant(variant_a, variant_b, confidence=0.95) {
  // Calculate z-score
  p_a = variant_a.conversions / variant_a.impressions
  p_b = variant_b.conversions / variant_b.impressions
  p_pooled = (variant_a.conversions + variant_b.conversions) /
             (variant_a.impressions + variant_b.impressions)

  se = sqrt(p_pooled * (1 - p_pooled) *
            (1/variant_a.impressions + 1/variant_b.impressions))

  z = (p_b - p_a) / se

  // Check against critical value
  z_critical = 1.96  // for 95% confidence
  return abs(z) > z_critical
}
```

### When to Call a Test

**Don't stop early:**
- Initial results are noisy
- Novelty effects exist
- Wait for full sample size

**Stop when:**
- Sample size reached
- Statistical significance achieved
- Predetermined duration elapsed

**Consider:**
- Business impact of waiting
- Cost of wrong decision
- Opportunity cost

---

## Test Management

### Test Lifecycle

**1. Hypothesis:**
Document what you're testing and why.
"We believe [change] will improve [metric] because [reason]."

**2. Design:**
- Define variants
- Set sample size and duration
- Choose metrics

**3. Launch:**
- Implement variants
- Start tracking
- Monitor for issues

**4. Analyze:**
- Wait for significance
- Check secondary metrics
- Look for segment effects

**5. Decide:**
- Implement winner
- Document learnings
- Plan next test

### Test Documentation

```
Test Name: Opening Message Greeting Style
Test ID: T-2024-001
Status: Running

Hypothesis:
A casual greeting will increase response rate because
it feels more human and less corporate.

Variants:
- Control (50%): "Hello! Thanks for reaching out..."
- Variant A (50%): "Hey there! Great to hear from you..."

Primary Metric: Response rate
Secondary Metrics: Sentiment, conversion rate
Sample Size Target: 1,000 per variant
Duration: 2 weeks or until significant

Results:
[To be completed]
```

### Test Calendar

**Always have:**
- Current test running
- Next test planned
- Backlog of ideas

**Avoid:**
- Testing too many things at once
- Overlapping tests on same messages
- Testing during anomalous periods

---

## Advanced Testing

### Multi-Armed Bandit

**Concept:**
Dynamically allocate more traffic to winning variants.

**Benefits:**
- Faster optimization
- Less regret (fewer impressions to losers)
- Continuous optimization

**Trade-off:**
- Less statistical purity
- Harder to analyze
- May miss longer-term effects

**Use when:**
- High volume
- Speed matters
- Clear conversion signal

### Personalized Testing

**Concept:**
Different messages work for different segments.

**Implementation:**
- Test within segments
- Analyze segment interactions
- Deploy segment-specific winners

**Example:**
- Message A wins for enterprise
- Message B wins for SMB
- Deploy both, targeted appropriately

### Sequential Testing

**Concept:**
Test in phases, eliminate losers early.

**Process:**
1. Test 4 variants with 25% each
2. Eliminate bottom 2
3. Test remaining 2 with 50% each
4. Implement winner

---

## Measuring Success

### Primary Metrics

**Response rate:**
% of messages that get a response

**Conversion rate:**
% that complete desired action (book meeting, qualify, etc.)

**Engagement rate:**
Continued conversation vs. drop-off

### Secondary Metrics

**Sentiment:**
Positive/negative reaction

**Conversation length:**
Engagement depth

**Time to conversion:**
Speed through funnel

### Guardrail Metrics

**Opt-out rate:**
Are we annoying people?

**Complaint rate:**
Negative feedback

**Brand perception:**
Are we hurting the brand?

---

## Common Testing Mistakes

### 1. Stopping Early
**Problem:** Calling winners before statistical significance
**Fix:** Commit to sample size before starting

### 2. Testing Too Many Variables
**Problem:** Can't isolate what caused change
**Fix:** One variable per test

### 3. No Hypothesis
**Problem:** Testing randomly, no learning
**Fix:** Document hypothesis and reasoning

### 4. Ignoring Segments
**Problem:** Average hides segment differences
**Fix:** Analyze by segment

### 5. Not Implementing Winners
**Problem:** Running tests but not acting on results
**Fix:** Have implementation plan before testing

### 6. Novelty Effects
**Problem:** New thing wins initially, then regresses
**Fix:** Run tests long enough, monitor post-implementation

---

## Test Ideas for Sales Bots

### Opening Messages

- Formal vs. casual greeting
- Question vs. statement opener
- Personalized vs. generic
- Short vs. detailed introduction

### Qualification Questions

- Direct vs. soft ask
- Single vs. multiple choice
- Order of questions
- Number of questions

### Value Propositions

- Benefit-focused vs. feature-focused
- Specific numbers vs. qualitative
- Social proof inclusion
- Customer quotes

### CTAs

- "Book a call" vs. "Learn more"
- Specific time vs. open
- Single CTA vs. options
- Urgency vs. no urgency

---

## Questions to Ask

If you need more context:
1. What conversation volume do you have for testing?
2. What messages do you suspect are underperforming?
3. What metrics are you trying to improve?
4. What testing have you done before?
5. What tools/infrastructure do you have for testing?

---

## Related Skills

- **conversational-flow-management**: What to test
- **performance-analytics**: Measuring results
- **personalization-at-scale**: Segment-specific testing
- **ab-test-setup**: General A/B testing principles
