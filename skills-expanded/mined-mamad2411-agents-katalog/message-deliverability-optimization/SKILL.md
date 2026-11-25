---
name: message-deliverability-optimization
description: When the user wants to build or improve a sales bot's ability to manage sender reputation and ensure messages get delivered. Also use when the user mentions "deliverability," "spam prevention," "sender reputation," "email warmup," or "domain reputation."
---

# Message Deliverability Optimization

You are an expert in building sales bots that maintain high deliverability through sender reputation management. Your goal is to help developers create systems that rotate numbers, warm domains, and manage reputation to ensure messages reach prospects.

## Why Deliverability Matters

### The Hidden Problem
```
You think:
- 1000 emails sent
- 50 opens (5% open rate)
- "Low engagement, need better copy"

Reality:
- 1000 emails sent
- 400 landed in inbox
- 600 went to spam
- 50 opens (12.5% of delivered)

Your copy might be fine. Deliverability is broken.
```

## Email Deliverability

### Domain Reputation Management
```python
class DomainManager:
    def __init__(self, domain):
        self.domain = domain
        self.reputation_score = 100
        self.daily_send_limit = self.calculate_limit()
        self.sent_today = 0

    def calculate_limit(self):
        """Dynamic limit based on reputation"""
        base_limit = 200  # New domain

        # Increase with age and reputation
        if self.domain_age_days > 90:
            base_limit += 100
        if self.reputation_score > 90:
            base_limit *= 2
        elif self.reputation_score < 70:
            base_limit *= 0.5

        return int(base_limit)

    def can_send(self):
        if self.sent_today >= self.daily_send_limit:
            return False
        if self.reputation_score < 50:
            return False  # Domain is burned
        return True

    def record_send(self, result):
        self.sent_today += 1

        # Update reputation based on results
        if result.get("bounced"):
            self.reputation_score -= 2
        if result.get("spam_complaint"):
            self.reputation_score -= 10
        if result.get("opened"):
            self.reputation_score += 0.1
        if result.get("replied"):
            self.reputation_score += 0.5
```

### Domain Warming
```python
def warm_new_domain(domain, target_volume):
    """Gradually increase sending volume for new domain"""

    warming_schedule = [
        {"day": 1, "sends": 20, "target": "engaged_list"},
        {"day": 2, "sends": 30, "target": "engaged_list"},
        {"day": 3, "sends": 50, "target": "engaged_list"},
        {"day": 4, "sends": 75, "target": "engaged_list"},
        {"day": 5, "sends": 100, "target": "mixed_list"},
        {"day": 6, "sends": 150, "target": "mixed_list"},
        {"day": 7, "sends": 200, "target": "mixed_list"},
        # Continue gradually...
    ]

    for day_config in warming_schedule:
        schedule_warming_sends(
            domain=domain,
            count=day_config["sends"],
            list_type=day_config["target"]
        )

    # Monitor during warmup
    monitor_warmup_metrics(domain)
```

### Domain Rotation
```python
class DomainRotator:
    def __init__(self, domains):
        self.domains = domains
        self.domain_managers = {d: DomainManager(d) for d in domains}

    def select_domain(self, prospect):
        available = [
            d for d in self.domains
            if self.domain_managers[d].can_send()
        ]

        if not available:
            return None

        # Select based on rotation strategy
        if self.strategy == "round_robin":
            return self.round_robin(available)
        elif self.strategy == "reputation_weighted":
            return self.reputation_weighted(available)
        elif self.strategy == "recipient_matched":
            return self.match_to_recipient(available, prospect)

    def reputation_weighted(self, available):
        """Prefer domains with better reputation"""
        weights = [
            self.domain_managers[d].reputation_score
            for d in available
        ]
        total = sum(weights)
        probs = [w/total for w in weights]
        return random.choices(available, probs)[0]
```

## SMS Deliverability

### Number Rotation
```python
class SMSNumberManager:
    def __init__(self):
        self.numbers = []
        self.daily_limits = {}
        self.carrier_scores = {}

    def add_number(self, number, carrier=None):
        self.numbers.append({
            "number": number,
            "carrier": carrier,
            "reputation": 100,
            "daily_sent": 0,
            "daily_limit": 200,  # Start conservative
            "status": "active"
        })

    def select_number(self, recipient_number):
        available = [n for n in self.numbers if self.can_send(n)]

        if not available:
            return None

        # Consider carrier matching
        recipient_carrier = lookup_carrier(recipient_number)
        matching_carrier = [
            n for n in available
            if n["carrier"] == recipient_carrier
        ]

        if matching_carrier:
            return self.select_best(matching_carrier)

        return self.select_best(available)

    def select_best(self, numbers):
        """Select number with best reputation and capacity"""
        return max(numbers, key=lambda n: (
            n["reputation"],
            n["daily_limit"] - n["daily_sent"]
        ))

    def report_issue(self, number, issue_type):
        for n in self.numbers:
            if n["number"] == number:
                if issue_type == "undelivered":
                    n["reputation"] -= 5
                elif issue_type == "blocked":
                    n["reputation"] -= 20
                    if n["reputation"] < 50:
                        n["status"] = "burned"
                elif issue_type == "carrier_block":
                    n["status"] = "carrier_blocked"
```

### SMS Compliance
```python
def ensure_sms_compliance(message, recipient):
    issues = []

    # Check opt-in status
    if not has_sms_consent(recipient):
        issues.append("no_consent")

    # Check time (TCPA)
    recipient_time = get_local_time(recipient)
    if not (8 <= recipient_time.hour <= 21):
        issues.append("outside_hours")

    # Check content
    if contains_blocked_keywords(message):
        issues.append("blocked_content")

    # Check rate limits
    recent_sms = count_recent_sms(recipient, hours=24)
    if recent_sms >= MAX_SMS_PER_DAY:
        issues.append("rate_limit_exceeded")

    return issues
```

## Content Optimization

### Spam Filter Avoidance
```python
def check_spam_triggers(content):
    triggers = []

    # Known spam words
    spam_words = [
        "free", "guarantee", "urgent", "act now",
        "limited time", "winner", "congratulations"
    ]
    for word in spam_words:
        if word.lower() in content.lower():
            triggers.append({"type": "spam_word", "word": word})

    # Excessive caps
    caps_ratio = sum(1 for c in content if c.isupper()) / len(content)
    if caps_ratio > 0.3:
        triggers.append({"type": "excessive_caps", "ratio": caps_ratio})

    # Excessive punctuation
    if content.count('!') > 2 or content.count('?') > 3:
        triggers.append({"type": "excessive_punctuation"})

    # Link analysis
    links = extract_links(content)
    for link in links:
        if is_shortened_url(link):
            triggers.append({"type": "shortened_url", "url": link})
        if is_suspicious_domain(link):
            triggers.append({"type": "suspicious_domain", "url": link})

    return triggers

def optimize_for_deliverability(content):
    triggers = check_spam_triggers(content)

    if triggers:
        # Suggest modifications
        suggestions = []
        for trigger in triggers:
            if trigger["type"] == "spam_word":
                suggestions.append(f"Replace '{trigger['word']}' with alternative")
            elif trigger["type"] == "shortened_url":
                suggestions.append(f"Use full URL instead of shortened")

        return {
            "original": content,
            "triggers": triggers,
            "suggestions": suggestions,
            "optimized": auto_optimize(content, triggers)
        }

    return {"original": content, "triggers": [], "optimized": content}
```

### Personalization for Deliverability
```python
def personalize_for_deliverability(template, prospect):
    """Personalization helps deliverability"""

    personalized = template

    # Replace placeholders
    personalized = personalized.replace("{first_name}", prospect.first_name)
    personalized = personalized.replace("{company}", prospect.company)

    # Add unique elements
    personalized = add_unique_element(personalized, prospect)

    # Vary sentence structure
    personalized = apply_sentence_variations(personalized)

    return personalized

def add_unique_element(content, prospect):
    """Add something unique to avoid template detection"""
    options = [
        f"I noticed {prospect.company}'s work on {prospect.recent_news}",
        f"Your {prospect.role} perspective would be valuable",
        f"Given {prospect.company}'s focus on {prospect.industry_vertical}",
    ]

    # Select based on available data
    for option in options:
        if all(placeholder in option for placeholder in extract_placeholders(option)):
            return content + "\n\n" + option

    return content
```

## Monitoring & Metrics

### Deliverability Metrics
```python
def calculate_deliverability_metrics(time_period):
    sends = get_sends(time_period)

    metrics = {
        "total_sent": len(sends),
        "delivered": len([s for s in sends if s.delivered]),
        "bounced": len([s for s in sends if s.bounced]),
        "spam_complaints": len([s for s in sends if s.spam_complaint]),
        "delivery_rate": calculate_rate(sends, "delivered"),
        "bounce_rate": calculate_rate(sends, "bounced"),
        "complaint_rate": calculate_rate(sends, "spam_complaint"),
        "inbox_placement": estimate_inbox_placement(sends)
    }

    # By domain
    metrics["by_domain"] = {}
    for domain in get_domains():
        domain_sends = [s for s in sends if s.domain == domain]
        metrics["by_domain"][domain] = {
            "delivery_rate": calculate_rate(domain_sends, "delivered"),
            "bounce_rate": calculate_rate(domain_sends, "bounced"),
            "reputation_score": get_domain_reputation(domain)
        }

    return metrics
```

### Alerting
```python
DELIVERABILITY_ALERTS = [
    {
        "name": "high_bounce_rate",
        "condition": lambda m: m["bounce_rate"] > 0.05,
        "action": "pause_sending"
    },
    {
        "name": "spam_complaints",
        "condition": lambda m: m["complaint_rate"] > 0.001,
        "action": "review_content"
    },
    {
        "name": "domain_reputation_drop",
        "condition": lambda m: any(d["reputation_score"] < 70 for d in m["by_domain"].values()),
        "action": "rotate_domains"
    }
]
```

## Recovery

### Reputation Recovery
```python
def recover_domain_reputation(domain):
    """Steps to recover a damaged domain"""

    # 1. Pause sending
    pause_domain(domain)

    # 2. Analyze issues
    issues = analyze_domain_issues(domain)

    # 3. Clean email list
    remove_hard_bounces(domain)
    remove_complainers(domain)

    # 4. Start slow recovery
    recovery_schedule = [
        {"day": 1, "sends": 10, "target": "most_engaged"},
        {"day": 2, "sends": 20, "target": "most_engaged"},
        {"day": 3, "sends": 30, "target": "highly_engaged"},
        # Gradually increase
    ]

    # 5. Monitor closely
    enable_enhanced_monitoring(domain)

    return schedule_recovery(domain, recovery_schedule)
```

