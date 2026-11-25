---
name: trigger-event-detection
description: When the user wants to build or improve a sales bot's ability to recognize external events that create opportunity. Also use when the user mentions "trigger events," "buying triggers," "event detection," "intent signals," or "sales triggers."
---

# Trigger Event Detection

You are an expert in building sales bots that recognize when external events create opportunity. Your goal is to help developers create systems that detect triggers like funding, hiring, leadership changes, and other signals that indicate buying readiness.

## Why Trigger Events Matter

### The Cold Outreach Problem
```
Standard outreach:
"Hi, we help companies like yours with X"
Response rate: 1-3%

Reason: No reason to respond right now.
Their situation hasn't changed.
```

### The Triggered Outreach
```
Triggered outreach:
"Congrats on the Series B! As you scale
the team, here's how we've helped similar
companies handle [challenge]."

Response rate: 10-25%

Reason: Relevant to their current moment.
```

## Trigger Categories

### Funding Events
```
What to detect:
- Seed round
- Series A, B, C, etc.
- PE/VC investment
- Debt financing
- IPO announcement

Why it matters:
- Fresh capital to spend
- Growth mandate
- Infrastructure needs
- New priorities

Message angle:
"With the new funding, you'll likely be
scaling [your solution area]. Here's how
we've helped other post-Series B companies."
```

### Leadership Changes
```
What to detect:
- New CEO/CTO/CMO/CFO
- New VP-level hires
- Key executive departures
- Board changes

Why it matters:
- New leaders make changes
- Fresh perspective on vendors
- Budget reallocation
- New initiatives

Message angle:
"Saw you joined [Company] as [Role].
New leaders often revisit [your solution area].
Happy to share what peers in your position
typically prioritize."
```

### Hiring Signals
```
What to detect:
- Job postings (specific roles)
- Hiring spree (volume)
- Specific technology in job posts
- Team expansion

Why it matters:
- Growth = investment in tools
- Specific hires = specific needs
- Scale challenges incoming

Message angle:
"Noticed you're hiring 5 SDRs. Teams that
size typically need [your solution]. Worth
a quick look?"
```

### Expansion Events
```
What to detect:
- New office opening
- Geographic expansion
- International launch
- Merger/acquisition

Why it matters:
- Growing = investing
- New locations = new systems
- M&A = consolidation opportunity

Message angle:
"Congrats on the Chicago expansion!
New offices often mean revisiting [tools].
How are you handling [challenge]?"
```

### Technology Signals
```
What to detect:
- New technology adoption
- Tool replacement announcements
- Integration launches
- Infrastructure changes

Why it matters:
- Tech change = buying mode
- Integration needs
- Modernization initiative

Message angle:
"Saw you recently adopted [tech]. Many
[tech] users pair it with [your solution]
for [benefit]. Worth exploring?"
```

### Business Events
```
What to detect:
- Product launches
- Partnership announcements
- Award wins
- Industry recognition
- Earnings reports (public)

Why it matters:
- Momentum = willingness to invest
- New initiatives = new needs
- Success = expansion mode

Message angle:
"Congrats on the product launch! Post-launch
teams often need help with [challenge].
How's that going for you?"
```

### Negative Triggers
```
What to detect:
- Competitor using their tech
- Negative reviews of competitor
- Competitor outage/issues
- Contract renewal timing

Why it matters:
- Dissatisfaction = openness
- Looking for alternatives
- Comparison shopping

Message angle:
"Heard [competitor] has been having issues.
If you're exploring options, happy to show
how we're different."
```

## Detection Implementation

### Data Sources
```python
TRIGGER_SOURCES = {
    "funding": [
        "crunchbase_api",
        "pitchbook_api",
        "news_alerts",
        "sec_filings"
    ],
    "leadership": [
        "linkedin_changes",
        "news_alerts",
        "company_announcements"
    ],
    "hiring": [
        "job_boards",
        "linkedin_jobs",
        "company_careers_page"
    ],
    "technology": [
        "builtwith",
        "wappalyzer",
        "news_alerts",
        "job_posting_tech"
    ],
    "news": [
        "google_alerts",
        "press_releases",
        "industry_publications"
    ]
}
```

### Trigger Detection Engine
```python
class TriggerDetector:
    def __init__(self, prospect):
        self.prospect = prospect
        self.detected_triggers = []

    def scan_for_triggers(self):
        triggers = []

        # Check each source
        triggers += self.check_funding_events()
        triggers += self.check_leadership_changes()
        triggers += self.check_hiring_signals()
        triggers += self.check_tech_changes()
        triggers += self.check_news_events()

        # Score and prioritize
        scored = [self.score_trigger(t) for t in triggers]
        self.detected_triggers = sorted(scored, key=lambda x: -x["score"])

        return self.detected_triggers

    def check_funding_events(self):
        triggers = []

        # Check Crunchbase
        funding = crunchbase_api.get_recent_funding(
            company=self.prospect.company_name,
            days=30
        )

        for round in funding:
            triggers.append({
                "type": "funding",
                "subtype": round.series,
                "amount": round.amount,
                "date": round.date,
                "source": "crunchbase"
            })

        return triggers

    def check_hiring_signals(self):
        triggers = []

        # Check LinkedIn jobs
        jobs = linkedin_api.get_job_postings(
            company=self.prospect.company_id,
            days=14
        )

        # Identify relevant roles
        relevant_roles = filter_relevant_roles(jobs, self.relevant_keywords)

        if len(relevant_roles) >= 3:
            triggers.append({
                "type": "hiring_spree",
                "subtype": "relevant_roles",
                "count": len(relevant_roles),
                "roles": relevant_roles[:5],
                "source": "linkedin"
            })

        return triggers

    def score_trigger(self, trigger):
        base_score = TRIGGER_BASE_SCORES.get(trigger["type"], 50)

        # Recency bonus
        days_old = (now() - trigger["date"]).days
        recency_multiplier = max(0.5, 1 - (days_old / 60))

        # Relevance bonus
        relevance = calculate_relevance(trigger, self.prospect)

        trigger["score"] = base_score * recency_multiplier * relevance
        return trigger
```

### Trigger Alert System
```python
def process_detected_trigger(trigger, prospect):
    # Create outreach opportunity
    opportunity = {
        "prospect_id": prospect.id,
        "trigger_type": trigger["type"],
        "trigger_details": trigger,
        "recommended_message": generate_trigger_message(trigger, prospect),
        "urgency": calculate_urgency(trigger),
        "suggested_timing": get_suggested_timing(trigger)
    }

    # Route based on prospect tier and trigger strength
    if prospect.icp_tier in ["tier_1", "tier_2"] and trigger["score"] >= 70:
        # High priority - alert rep
        notify_rep(prospect.owner, opportunity)
        create_task(prospect.owner, "Trigger-based outreach", due=today())

    elif trigger["score"] >= 50:
        # Medium priority - queue for bot outreach
        queue_triggered_outreach(prospect, opportunity)

    else:
        # Low priority - add to context for future
        update_prospect_context(prospect, trigger)
```

## Trigger-Based Messaging

### Message Templates by Trigger
```python
TRIGGER_MESSAGES = {
    "funding": {
        "series_a": """
Congrats on the Series A, {name}! As you scale,
teams your size typically need to think about
{pain_point}. Happy to share what we've seen
work for other post-A companies.
""",
        "series_b": """
Saw the Series B news—congrats! With growth
comes {challenge}. We've helped companies at
your stage {benefit}. Worth a quick look?
"""
    },
    "new_executive": {
        "cmo": """
{name}, congrats on the CMO role at {company}.
New marketing leaders often revisit {our_area}.
Happy to share what your peers typically
prioritize in the first 90 days.
""",
        "cto": """
Saw you joined {company} as CTO. Tech leaders
often find {pain_point} when they come in.
If that resonates, happy to chat.
"""
    },
    "hiring": {
        "sales_team": """
Noticed {company} is building out the sales
team. Teams that size often struggle with
{pain_point}. Worth exploring how we can help?
""",
        "engineering_team": """
Saw you're scaling engineering. Fast-growing
teams often need {solution_area}. Happy to
share what similar companies have done.
"""
    }
}

def generate_trigger_message(trigger, prospect):
    template = TRIGGER_MESSAGES[trigger["type"]][trigger["subtype"]]
    return template.format(
        name=prospect.first_name,
        company=prospect.company_name,
        pain_point=get_relevant_pain_point(prospect),
        challenge=get_relevant_challenge(trigger),
        benefit=get_relevant_benefit(prospect),
        our_area=get_solution_area()
    )
```

## Timing Optimization

### When to Act on Triggers
```
Funding announced:
- Act within 1-2 weeks
- Not same day (noise)
- Before spending decisions made

Executive hired:
- Act at 2-4 weeks
- After they've assessed
- Before they've decided

Hiring signals:
- Act while hiring active
- Growing = immediate need
- Position not filled yet

Technology change:
- Act within 2-4 weeks
- Implementation phase
- Integration decisions pending
```

### Trigger Decay
```python
def calculate_trigger_freshness(trigger):
    days_old = (now() - trigger["date"]).days

    DECAY_RATES = {
        "funding": 60,      # Relevant for ~60 days
        "new_executive": 90, # Relevant for ~90 days
        "hiring": 30,       # Relevant while active
        "tech_change": 45,  # Relevant for ~45 days
        "expansion": 60     # Relevant for ~60 days
    }

    decay_period = DECAY_RATES.get(trigger["type"], 45)
    freshness = max(0, 1 - (days_old / decay_period))

    return freshness
```

## Metrics

### Trigger Effectiveness
```
Track:
- Response rate by trigger type
- Conversion rate by trigger type
- Revenue from trigger-based outreach
- Time from trigger to engagement

Optimize:
- Which triggers work best?
- What messaging converts?
- What timing is optimal?
```

