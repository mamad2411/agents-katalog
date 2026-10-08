---
name: conversation-compliance-auditing
description: When the user wants to build or improve a sales bot's ability to ensure conversations meet regulatory and company standards. Also use when the user mentions "compliance auditing," "regulatory compliance," "conversation audit," "policy compliance," or "legal review."
---

# Conversation Compliance Auditing

You are an expert in building sales bots that automatically audit conversations for compliance with regulations and company policies. Your goal is to help developers create systems that catch violations before they become problems.

## Why Compliance Auditing Matters

### The Risk Reality
```
Without auditing:
- TCPA violation: $500-$1500 per message
- GDPR fine: Up to €20 million
- CAN-SPAM violation: $46,517 per email
- FTC deceptive practice: Millions in fines

One bad conversation can cost more than
a year of revenue.
```

### With Automated Auditing
```
Every conversation checked for:
- Regulatory compliance (TCPA, GDPR, CAN-SPAM)
- Company policy adherence
- Promise accuracy
- Disclosure requirements

Violations flagged before they're sent.
Patterns identified for training.
```

## Compliance Rules Engine

### Rule Definition
```python
class ComplianceRule:
    def __init__(self, rule_id, name, category, severity):
        self.rule_id = rule_id
        self.name = name
        self.category = category  # regulatory, policy, ethical
        self.severity = severity  # critical, high, medium, low
        self.checks = []

    def add_check(self, check_function, description):
        self.checks.append({
            "function": check_function,
            "description": description
        })

    def evaluate(self, message, context):
        violations = []
        for check in self.checks:
            result = check["function"](message, context)
            if not result["passed"]:
                violations.append({
                    "rule_id": self.rule_id,
                    "rule_name": self.name,
                    "check": check["description"],
                    "severity": self.severity,
                    "details": result.get("details"),
                    "evidence": result.get("evidence")
                })
        return violations
```

### TCPA Compliance Rules
```python
def create_tcpa_rules():
    rules = []

    # Time restrictions
    time_rule = ComplianceRule(
        "TCPA-001", "Calling Hours", "regulatory", "critical"
    )
    time_rule.add_check(
        check_calling_hours,
        "Messages must be sent between 8am-9pm recipient local time"
    )
    rules.append(time_rule)

    # Consent verification
    consent_rule = ComplianceRule(
        "TCPA-002", "Prior Express Consent", "regulatory", "critical"
    )
    consent_rule.add_check(
        check_sms_consent,
        "SMS requires prior express written consent"
    )
    consent_rule.add_check(
        check_call_consent,
        "Calls require prior express consent for marketing"
    )
    rules.append(consent_rule)

    # Opt-out honoring
    optout_rule = ComplianceRule(
        "TCPA-003", "Opt-Out Compliance", "regulatory", "critical"
    )
    optout_rule.add_check(
        check_optout_honored,
        "Must honor opt-out requests immediately"
    )
    rules.append(optout_rule)

    return rules

def check_calling_hours(message, context):
    recipient_time = get_recipient_local_time(context.recipient)
    hour = recipient_time.hour

    if hour < 8 or hour >= 21:
        return {
            "passed": False,
            "details": f"Message scheduled for {recipient_time.strftime('%I:%M %p')} recipient time",
            "evidence": f"Recipient timezone: {context.recipient.timezone}"
        }
    return {"passed": True}
```

### CAN-SPAM Compliance
```python
def create_canspam_rules():
    rules = []

    # Accurate headers
    header_rule = ComplianceRule(
        "CAN-SPAM-001", "Accurate Header Information", "regulatory", "critical"
    )
    header_rule.add_check(
        check_from_address,
        "From address must accurately identify sender"
    )
    header_rule.add_check(
        check_subject_line,
        "Subject line must not be deceptive"
    )
    rules.append(header_rule)

    # Ad identification
    ad_rule = ComplianceRule(
        "CAN-SPAM-002", "Advertisement Disclosure", "regulatory", "high"
    )
    ad_rule.add_check(
        check_ad_disclosure,
        "Commercial messages must be identifiable as advertisements"
    )
    rules.append(ad_rule)

    # Physical address
    address_rule = ComplianceRule(
        "CAN-SPAM-003", "Physical Address Required", "regulatory", "high"
    )
    address_rule.add_check(
        check_physical_address,
        "Must include valid physical postal address"
    )
    rules.append(address_rule)

    # Opt-out mechanism
    optout_rule = ComplianceRule(
        "CAN-SPAM-004", "Opt-Out Mechanism", "regulatory", "critical"
    )
    optout_rule.add_check(
        check_unsubscribe_link,
        "Must include clear opt-out mechanism"
    )
    rules.append(optout_rule)

    return rules
```

### Company Policy Rules
```python
def create_policy_rules(company_config):
    rules = []

    # Pricing claims
    pricing_rule = ComplianceRule(
        "POLICY-001", "Accurate Pricing", "policy", "high"
    )
    pricing_rule.add_check(
        lambda m, c: check_pricing_accuracy(m, c, company_config),
        "Pricing claims must match current price list"
    )
    rules.append(pricing_rule)

    # Feature claims
    feature_rule = ComplianceRule(
        "POLICY-002", "Accurate Feature Claims", "policy", "high"
    )
    feature_rule.add_check(
        lambda m, c: check_feature_accuracy(m, c, company_config),
        "Feature claims must match product capabilities"
    )
    rules.append(feature_rule)

    # Competitor mentions
    competitor_rule = ComplianceRule(
        "POLICY-003", "Competitor References", "policy", "medium"
    )
    competitor_rule.add_check(
        check_competitor_claims,
        "Competitor claims must be verifiable"
    )
    rules.append(competitor_rule)

    # Promise restrictions
    promise_rule = ComplianceRule(
        "POLICY-004", "Unauthorized Promises", "policy", "high"
    )
    promise_rule.add_check(
        check_unauthorized_promises,
        "Cannot make commitments outside approval matrix"
    )
    rules.append(promise_rule)

    return rules
```

## Audit Engine

### Real-Time Auditing
```python
class ConversationAuditor:
    def __init__(self):
        self.rules = []
        self.rules.extend(create_tcpa_rules())
        self.rules.extend(create_canspam_rules())
        self.rules.extend(create_gdpr_rules())
        self.rules.extend(create_policy_rules(get_company_config()))

    def audit_message(self, message, context):
        """Audit a single message before sending"""

        all_violations = []

        for rule in self.rules:
            violations = rule.evaluate(message, context)
            all_violations.extend(violations)

        # Categorize by severity
        critical = [v for v in all_violations if v["severity"] == "critical"]
        high = [v for v in all_violations if v["severity"] == "high"]

        result = {
            "passed": len(critical) == 0,
            "violations": all_violations,
            "critical_count": len(critical),
            "high_count": len(high),
            "can_send": len(critical) == 0 and len(high) == 0,
            "requires_review": len(high) > 0
        }

        if not result["passed"]:
            log_compliance_violation(message, result)

        return result

    def audit_conversation(self, conversation):
        """Audit entire conversation for patterns"""

        conversation_violations = []
        for message in conversation.messages:
            if message.sender == "bot":
                result = self.audit_message(message, conversation)
                if result["violations"]:
                    conversation_violations.append({
                        "message_id": message.id,
                        "violations": result["violations"]
                    })

        return {
            "conversation_id": conversation.id,
            "total_violations": sum(len(v["violations"]) for v in conversation_violations),
            "messages_with_violations": len(conversation_violations),
            "details": conversation_violations
        }
```

### Content Checks
```python
def check_deceptive_claims(message, context):
    """Check for potentially deceptive content"""

    deceptive_patterns = [
        r"guarantee[d]?\s+(results|success|roi)",
        r"100%\s+(success|effective|guaranteed)",
        r"risk[- ]free",
        r"no\s+obligation",  # May need context
        r"limited\s+time\s+only",  # If false
        r"act\s+now\s+or\s+miss\s+out"  # Artificial urgency
    ]

    violations = []
    for pattern in deceptive_patterns:
        if re.search(pattern, message.text, re.IGNORECASE):
            violations.append({
                "type": "potentially_deceptive",
                "pattern": pattern,
                "match": re.search(pattern, message.text, re.IGNORECASE).group()
            })

    return {
        "passed": len(violations) == 0,
        "details": violations,
        "evidence": message.text
    }

def check_unauthorized_promises(message, context):
    """Check for promises that require approval"""

    promise_patterns = [
        (r"(we('ll| will)|I('ll| will))\s+waive", "fee_waiver"),
        (r"(discount|reduce|lower)\s+(the\s+)?price\s+by", "discount"),
        (r"(extend|lengthen)\s+(the\s+)?(trial|pilot)", "trial_extension"),
        (r"(custom|bespoke|tailored)\s+(feature|development)", "custom_dev"),
        (r"guaranteed?\s+(uptime|availability|sla)", "sla_guarantee")
    ]

    violations = []
    for pattern, promise_type in promise_patterns:
        if re.search(pattern, message.text, re.IGNORECASE):
            if not is_authorized(context.sender, promise_type):
                violations.append({
                    "type": "unauthorized_promise",
                    "promise_type": promise_type,
                    "requires_approval_from": get_approval_authority(promise_type)
                })

    return {
        "passed": len(violations) == 0,
        "details": violations
    }
```

## Audit Reporting

### Violation Reports
```python
def generate_compliance_report(time_period):
    """Generate compliance audit report"""

    violations = get_violations(time_period)

    report = {
        "period": time_period,
        "summary": {
            "total_messages_audited": count_audited_messages(time_period),
            "total_violations": len(violations),
            "violation_rate": len(violations) / count_audited_messages(time_period),
            "by_severity": count_by_severity(violations),
            "by_category": count_by_category(violations),
            "by_rule": count_by_rule(violations)
        },
        "trends": {
            "vs_previous_period": compare_to_previous(violations, time_period),
            "weekly_trend": calculate_weekly_trend(time_period)
        },
        "top_violations": get_top_violations(violations, n=10),
        "recommendations": generate_recommendations(violations)
    }

    return report

def generate_recommendations(violations):
    """Generate actionable recommendations from violations"""

    recommendations = []

    # Group violations by rule
    by_rule = defaultdict(list)
    for v in violations:
        by_rule[v["rule_id"]].append(v)

    for rule_id, rule_violations in by_rule.items():
        if len(rule_violations) > 10:  # Significant pattern
            recommendations.append({
                "priority": "high",
                "rule": rule_id,
                "issue": f"{len(rule_violations)} violations of {rule_id}",
                "action": get_remediation_action(rule_id),
                "impact": estimate_risk_impact(rule_violations)
            })

    return sorted(recommendations, key=lambda r: r["priority"])
```

### Audit Trail
```python
def log_compliance_event(event_type, message, result, context):
    """Maintain audit trail for compliance"""

    audit_record = {
        "event_id": generate_uuid(),
        "timestamp": datetime.now(UTC),
        "event_type": event_type,
        "message_id": message.id,
        "conversation_id": context.conversation_id,
        "sender": context.sender,
        "recipient": context.recipient.id,
        "audit_result": {
            "passed": result["passed"],
            "violations": result["violations"],
            "action_taken": result.get("action_taken")
        },
        "message_hash": hash_message(message),  # For verification
        "metadata": {
            "bot_version": get_bot_version(),
            "rules_version": get_rules_version(),
            "channel": context.channel
        }
    }

    # Store with immutability guarantees
    compliance_log.insert(audit_record)

    return audit_record["event_id"]
```

## Remediation

### Auto-Remediation
```python
def remediate_violation(message, violation):
    """Attempt automatic remediation of violations"""

    remediation_handlers = {
        "CAN-SPAM-003": add_physical_address,
        "CAN-SPAM-004": add_unsubscribe_link,
        "POLICY-001": correct_pricing,
        "POLICY-002": remove_inaccurate_claim
    }

    if violation["rule_id"] in remediation_handlers:
        handler = remediation_handlers[violation["rule_id"]]
        remediated = handler(message, violation)
        return {
            "remediated": True,
            "original": message.text,
            "corrected": remediated.text,
            "changes": diff_messages(message, remediated)
        }

    return {
        "remediated": False,
        "reason": "No auto-remediation available",
        "requires": "manual_review"
    }
```

## Metrics

### Compliance KPIs
```
Track:
- Violation rate (per 1000 messages)
- Critical violations (should be 0)
- Time to remediation
- Audit coverage (% of messages audited)
- False positive rate

Alert thresholds:
- Any critical violation: Immediate
- >1% violation rate: Same day
- Increasing trend: Weekly review
```

