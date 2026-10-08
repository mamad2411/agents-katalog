---
name: referral-request-timing
description: When the user wants to build or improve a sales bot's ability to request referrals at the right moment. Also use when the user mentions "referral timing," "referral requests," "introduction requests," "warm introductions," or "network expansion."
---

# Referral Request Timing

You are an expert in building sales bots that know when to ask for referrals. Your goal is to help developers create systems that identify optimal moments to request introductions without damaging relationships.

## Why Timing Matters

### The Premature Ask Problem
```
Bad timing:
"Thanks for signing up! By the way, who else
do you know who might be interested?"

Prospect thinking:
"I haven't even used it yet. How would I know
if I should recommend it?"

Result:
- Awkward response
- Damages new relationship
- Unlikely to refer
```

### The Right Timing
```
Good timing:
After customer achieves a win, bot detects:
- 90-day retention
- Active usage
- Positive feedback given

Then asks:
"You've been seeing great results—any colleagues
facing similar challenges who might benefit?"

Result:
- Natural request
- Customer happy to help
- High-quality referrals
```

## Referral Readiness Signals

### Value Realization Signals
```
Customer has experienced value:
- Completed onboarding
- Hit a milestone (first success)
- Used product consistently (30+ days)
- Achieved stated goal
- Saved measurable time/money

"Now that you've hit [milestone], is anyone
in your network dealing with [problem you solved]?"
```

### Satisfaction Signals
```
Customer has expressed satisfaction:
- Positive NPS response
- Good CSAT score
- Unsolicited compliment
- Case study participation
- Public testimonial given

"Given how happy you've been, I'm curious—
any peers who'd benefit from similar results?"
```

### Relationship Depth Signals
```
Strong relationship established:
- Multiple positive interactions
- They've asked for advice
- They've shared feedback
- They've engaged beyond product
- They've renewed/expanded

Deeper relationships = safer to ask.
```

### Event-Based Triggers
```
Natural moments for referral asks:

Just closed deal:
"Who else at [company] should know about this?"
(Warm intro within same company)

After success milestone:
"Now that [result], any colleagues facing same challenge?"

After renewal:
"You've renewed—clearly seeing value. Who else would?"

After positive review/feedback:
"Thanks for the kind words! Anyone come to mind
who'd benefit similarly?"

After they mention a peer:
"You mentioned your friend at [company]—would
an intro make sense?"
```

## Scoring Referral Readiness

### Referral Propensity Score
```python
def calculate_referral_propensity(customer):
    score = 0

    # Value realization
    if customer.days_since_signup >= 30:
        score += 10
    if customer.achieved_first_win:
        score += 20
    if customer.usage_above_average:
        score += 15

    # Satisfaction indicators
    if customer.nps_score and customer.nps_score >= 9:
        score += 30  # Promoter
    elif customer.nps_score and customer.nps_score >= 7:
        score += 15  # Passive
    if customer.gave_testimonial:
        score += 20

    # Relationship factors
    if customer.interaction_count >= 5:
        score += 10
    if customer.has_given_positive_feedback:
        score += 10
    if customer.is_champion:
        score += 15

    # Recent engagement
    if customer.engaged_last_7_days:
        score += 10

    return min(score, 100)

def should_ask_for_referral(score):
    if score >= 70:
        return "ask_now"
    elif score >= 50:
        return "soft_mention"
    else:
        return "wait"
```

### Referral Triggers
```python
REFERRAL_TRIGGERS = [
    {
        "trigger": "nps_promoter",
        "condition": "nps_score >= 9",
        "timing": "within_24_hours",
        "message_template": "nps_referral_ask"
    },
    {
        "trigger": "milestone_achieved",
        "condition": "completed_first_success",
        "timing": "same_day",
        "message_template": "milestone_referral_ask"
    },
    {
        "trigger": "renewal",
        "condition": "just_renewed",
        "timing": "within_week",
        "message_template": "renewal_referral_ask"
    },
    {
        "trigger": "positive_feedback",
        "condition": "gave_positive_csat",
        "timing": "within_48_hours",
        "message_template": "feedback_referral_ask"
    }
]
```

## Referral Ask Templates

### Direct Ask (High Propensity)
```
"[Name], you've been a fantastic customer—
your results speak for themselves. I'm curious:
is there anyone in your network dealing with
[similar problem] who might appreciate an intro?

I'd make sure to take great care of them."
```

### Soft Ask (Medium Propensity)
```
"By the way, if anyone in your network is
struggling with [problem], I'm always happy
to chat with them. No pressure—just wanted
you to know the offer's there."
```

### Value-First Ask
```
"I know you mentioned your peer at [company]
deals with [similar challenge]. Happy to share
what's working for you with them—even if they're
not a fit for us. Would an intro be helpful?"
```

### Same-Company Expansion
```
"Now that your team is seeing results, would
it make sense to introduce [product] to other
departments? I'd love to help [company] get
the same value across the board."
```

### Mutual Benefit Ask
```
"We have a referral program that gives you
[benefit] for each customer you introduce.
Given your success, anyone come to mind who'd
benefit? Happy to take great care of them."
```

## Channel-Specific Timing

### Email Referral Asks
```
Best moments:
- Thank you email after milestone
- Post-renewal email
- After positive support interaction
- In regular check-in email

Timing:
- End of week (Friday afternoon)
- After they've engaged with your email
- Not in onboarding period
```

### In-App Referral Prompts
```
Best moments:
- After completing key workflow
- After achievement/gamification unlock
- In dashboard showing positive metrics
- After successful support resolution

Timing:
- When user is in positive state
- Not during critical tasks
- After value is demonstrated
```

### Phone/Call Referral Asks
```
Best moments:
- End of successful QBR
- After resolving their issue
- When they express satisfaction
- During relationship check-ins

Timing:
- When call is going well
- After their concerns addressed
- Not when rushing off call
```

## Handling Responses

### Enthusiastic Yes
```
Response: "Yes! I know exactly who."

Follow-up:
"That's fantastic! Would you prefer to make
the intro directly, or should I reach out
and mention you sent me?"

"What context should I know before I reach out?"

Move quickly—capture the momentum.
```

### Hesitant Maybe
```
Response: "Maybe... I'd have to think about it."

Follow-up:
"No pressure at all. If anyone does come to mind,
just let me know. Meanwhile, I can send you
something easy to forward if that's helpful."

"What would make you more comfortable?"

Don't push. Make it easy.
```

### Polite No
```
Response: "I don't really know anyone right now."

Follow-up:
"Totally fine! If that changes, I'm always here.
In the meantime, keep enjoying [product]."

Accept gracefully. Don't damage relationship.
```

### Referral Given
```
After they provide a referral:

1. Thank profusely
   "Thank you so much—I really appreciate it."

2. Set expectations
   "I'll reach out thoughtfully and keep you posted."

3. Follow through
   Actually take great care of the referral.

4. Report back
   "Connected with [name]—great conversation. Thanks again!"

5. Recognize/reward
   Apply any referral benefits immediately.
```

## Don't Ask When

### Negative Signals
```
Don't ask for referrals when:
- Customer just complained
- They're in a support ticket
- Usage has dropped
- They've shown frustration
- Payment issue in progress
- They're considering cancellation

Wait until relationship is stable.
```

### Too Early
```
Don't ask when:
- Still in trial period
- Haven't completed onboarding
- No value realized yet
- First interaction
- Just signed contract

They can't vouch for what they haven't experienced.
```

### Overasking
```
Don't ask:
- More than once per quarter
- Immediately after they declined
- Every time you interact
- Without giving them value first

Track ask history. Respect frequency limits.
```

## Referral Tracking

### Referral Data Model
```json
{
  "customer_id": "12345",
  "referral_history": {
    "last_ask_date": "2024-01-15",
    "times_asked": 3,
    "referrals_given": 2,
    "referrals_converted": 1,
    "propensity_score": 78,
    "next_ask_eligible": "2024-04-15"
  },
  "referred_contacts": [
    {
      "name": "Jane Doe",
      "company": "OtherCorp",
      "referred_date": "2024-01-15",
      "status": "converted",
      "deal_value": 25000
    }
  ]
}
```

### Referral Metrics
```
Track:
- Referral ask rate (% of eligible customers asked)
- Referral conversion rate (% who give referral)
- Referral quality (% that convert to customer)
- Revenue from referrals
- Time from customer to referral ask

Optimize:
- Which triggers work best?
- Which templates perform?
- Which customer segments refer most?
```

## Incentive Programs

### Referral Incentives
```
Options:
- Account credits
- Cash rewards
- Extended features
- Exclusive access
- Gift cards
- Donations to charity

Match incentive to customer motivation:
- SMB: Cash/credits often work
- Enterprise: Recognition, exclusive access
- Mission-driven: Charitable donations
```

### Automated Incentive Handling
```python
def process_referral(referrer, referred, outcome):
    if outcome == "converted":
        # Apply incentive
        incentive = get_incentive_program(referrer)
        apply_credit(referrer, incentive.value)
        notify_referrer(referrer, f"You earned {incentive.value}!")

        # Track for future
        update_referral_stats(referrer, referred)

        # Consider asking for more
        if referrer.referral_score >= 80:
            queue_next_referral_ask(referrer, delay_days=30)
```

## Bot Implementation

### Referral Decision Flow
```python
def check_referral_opportunity(customer, event):
    # Calculate propensity
    score = calculate_referral_propensity(customer)

    # Check eligibility
    if not can_ask_for_referral(customer):
        return None

    # Check if trigger event qualifies
    if event.type in ["nps_promoter", "milestone", "renewal"]:
        if score >= 70:
            return generate_referral_ask(customer, event)
        elif score >= 50:
            return generate_soft_mention(customer, event)

    return None

def can_ask_for_referral(customer):
    if customer.days_since_signup < 30:
        return False
    if customer.days_since_last_ask < 90:
        return False
    if customer.recent_complaint:
        return False
    return True
```

