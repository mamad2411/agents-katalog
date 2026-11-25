---
name: legal-compliance-phrase-avoidance
description: When the user wants to build or improve a sales bot's ability to avoid making claims that create liability. Also use when the user mentions "compliance," "legal risk," "claim avoidance," "regulated industries," or "liability prevention."
---

# Legal and Compliance Phrase Avoidance

You are an expert in building sales bots that avoid making claims that could create liability. Your goal is to help developers create systems that communicate effectively while staying within legal boundaries, especially in regulated industries like property, finance, and healthcare.

## Why This Matters

### The Liability Problem
```
Risky bot statement:
"Our software will definitely increase your
ROI by 50% within 6 months!"

What happens:
- Customer relies on this claim
- Results don't match
- Customer demands refund/damages
- Potential false advertising claim
- Regulatory investigation

One bad claim can cost millions.
```

### Safe Communication
```
Safe alternative:
"Customers typically see significant ROI
improvements. Results vary by implementation,
but I can share case studies from companies
similar to yours."

This:
- Sets realistic expectations
- Provides evidence without guarantee
- Protects the company legally
```

## Industry-Specific Risks

### Financial Services
```
Regulated phrases to avoid:
- "Guaranteed returns"
- "Risk-free investment"
- "You will make money"
- "This is a sure thing"
- "Better than the bank"
- "Outperform the market"

Required disclaimers:
- Past performance doesn't guarantee future results
- Investment involves risk
- Consult a licensed advisor

Example transformation:
BAD: "You'll earn 10% annually"
GOOD: "Historical returns have averaged around 10%,
though past performance doesn't guarantee future results."
```

### Real Estate/Property
```
Risky claims:
- "This property will appreciate"
- "Best investment in the area"
- "Rental income guaranteed"
- "You can't lose money on property"
- "This neighborhood is safe" (discrimination risk)
- "Good schools nearby" (fair housing concerns)

Safe alternatives:
- "Properties in this area have historically appreciated"
- "Here's the rental yield data for similar properties"
- "I can share market research for this location"

Fair Housing concerns:
Never mention: race, religion, national origin,
sex, disability, familial status, or use proxies.
```

### Healthcare/Medical
```
Never claim:
- "This will cure..."
- "Guaranteed to treat..."
- "FDA approved" (unless actually approved)
- "Clinically proven" (without evidence)
- "No side effects"
- Diagnoses or medical advice

Safe language:
- "May help support..."
- "Studies suggest..."
- "Consult your healthcare provider"
- "Individual results vary"
```

### Insurance
```
Avoid:
- "Full coverage" (vague, misleading)
- "You're fully protected"
- "This covers everything"
- "Best price guaranteed"
- Advice without proper licensing

Required:
- Clear policy limitations
- Disclaimer about reading policy docs
- "Coverage depends on specific policy terms"
```

## Risky Phrase Categories

### Guarantees
```
Avoid:
- "Guaranteed"
- "100% certain"
- "Definitely will"
- "Absolutely"
- "Promise"
- "We ensure"

Instead:
- "Typically"
- "Based on our experience"
- "Customers generally see"
- "Our expectation is"
- "Designed to"
```

### Absolute Claims
```
Avoid:
- "Best in the market"
- "Number one solution"
- "Industry leading" (without proof)
- "Unbeatable"
- "Perfect for everyone"

Instead:
- "One of the top solutions"
- "Highly rated by customers"
- "Strong performer in [category]"
- "Well-suited for [specific use case]"
```

### Comparative Claims
```
Avoid:
- "Better than [competitor]"
- "Cheaper than alternatives"
- "Faster than everyone else"
- (Unless you have proof)

Instead:
- "Competitive in the market"
- "Customers often compare favorably"
- "Here's how we differ: [factual]"
```

### Future Predictions
```
Avoid:
- "Will increase revenue"
- "You'll see results in X days"
- "This will solve your problem"
- "Prices will go up"

Instead:
- "Designed to help increase"
- "Customers typically see results within"
- "Helps address this challenge"
- "Current pricing is..."
```

## Implementation

### Phrase Detection
```python
RISKY_PHRASES = {
    "high_risk": [
        r"\bguarantee[ds]?\b",
        r"\b100%\s*(certain|sure|guaranteed)\b",
        r"\bwill\s+(definitely|certainly)\b",
        r"\brisk[- ]free\b",
        r"\bno\s+risk\b",
        r"\bpromise\s+(you|that)\b",
        r"\bcure[sd]?\b",
        r"\btreat(s|ment)?\s+\w+\s+disease\b"
    ],
    "medium_risk": [
        r"\bbest\s+(in|on)\s+(the\s+)?(market|industry)\b",
        r"\bnumber\s+(one|1|#1)\b",
        r"\bindustry[- ]leading\b",
        r"\bunbeatable\b",
        r"\bwill\s+(increase|improve|grow)\b"
    ],
    "context_dependent": [
        r"\bFDA\s+approved\b",
        r"\bclinically\s+proven\b",
        r"\bAward[- ]winning\b"
    ]
}

def check_compliance(message):
    issues = []
    for risk_level, patterns in RISKY_PHRASES.items():
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                issues.append({
                    "risk_level": risk_level,
                    "pattern": pattern,
                    "match": re.search(pattern, message, re.IGNORECASE).group()
                })
    return issues
```

### Response Modification
```python
def make_compliant(response, issues):
    modified = response

    for issue in issues:
        if issue["risk_level"] == "high_risk":
            # Must modify
            modified = apply_hedge(modified, issue)
        elif issue["risk_level"] == "medium_risk":
            # Should modify
            modified = soften_claim(modified, issue)
        elif issue["risk_level"] == "context_dependent":
            # Flag for review
            flag_for_compliance_review(response, issue)

    return modified

HEDGE_REPLACEMENTS = {
    "guarantee": "designed to",
    "will definitely": "typically",
    "100% certain": "confident",
    "risk-free": "low-risk",
    "best in the market": "competitive",
    "will increase": "helps increase",
    "you will see": "customers typically see"
}
```

### Pre-Response Compliance Check
```python
def generate_response(intent, context):
    # Generate initial response
    response = generate_base_response(intent, context)

    # Check for compliance issues
    issues = check_compliance(response)

    if issues:
        # Modify to be compliant
        response = make_compliant(response, issues)

        # Log for review
        log_compliance_modification(response, issues)

    # Add required disclaimers if needed
    if requires_disclaimer(intent, context):
        response = add_disclaimer(response, context.industry)

    return response
```

## Required Disclaimers

### Financial Disclaimers
```
When discussing investments/returns:

"Past performance is not indicative of future results.
Investment involves risk. Please consult with a
licensed financial advisor."

When discussing loans:
"Rates and terms subject to credit approval.
[Company] is not a lender."
```

### Health Disclaimers
```
"This information is for educational purposes only
and is not intended as medical advice. Please consult
a healthcare professional for medical guidance."

"These statements have not been evaluated by the FDA.
This product is not intended to diagnose, treat, cure,
or prevent any disease."
```

### General Disclaimers
```
"Individual results may vary."

"[Feature] available in select plans. See terms."

"Offer subject to change. Terms and conditions apply."
```

## Safe Language Alternatives

### Results Claims
```
Risky: "You'll save $10,000"
Safe: "Customers in your situation typically save around $10,000"

Risky: "This will fix your problem"
Safe: "This is designed to address that challenge"

Risky: "Guaranteed 2x ROI"
Safe: "Customers commonly see 2x or better ROI, though results vary"
```

### Product Claims
```
Risky: "The best CRM on the market"
Safe: "A highly-rated CRM with strong customer reviews"

Risky: "100% secure"
Safe: "Enterprise-grade security with [specific certifications]"

Risky: "Works perfectly every time"
Safe: "Reliable performance with 99.9% uptime"
```

### Comparative Claims
```
Risky: "Better than Salesforce"
Safe: "Customers who switched from Salesforce often cite
[specific benefits] as their reasons"

Risky: "Cheaper than competitors"
Safe: "Competitively priced; happy to compare specific quotes"
```

## Escalation Rules

### Auto-Escalate Topics
```
Always escalate to human when:
- Legal questions asked
- Compliance requirements discussed
- Contract terms negotiated
- Specific guarantees requested
- Regulatory questions raised
- Pricing commitments requested

Response:
"That's an important question that deserves a precise
answer. Let me connect you with someone who can speak
to that specifically."
```

### Flagged Topics
```
Topics requiring extra caution:

- Price matching promises
- Service level agreements
- Performance guarantees
- Liability discussions
- Regulatory compliance
- Data handling commitments

Use pre-approved language only.
```

## Training and Validation

### Response Validation
```
Before deployment, validate:

1. All response templates reviewed by legal
2. Risky phrase detection tested
3. Industry-specific rules configured
4. Disclaimer triggers working
5. Escalation paths functional
```

### Ongoing Monitoring
```
Monitor for:
- Compliance modifications triggered
- Escalations due to compliance
- Customer complaints about claims
- Regulatory inquiries

Review:
- Weekly compliance modification logs
- Monthly pattern analysis
- Quarterly legal review of templates
```

## Metrics

### Compliance Tracking
```
Track:
- Risky phrase detection rate
- Successful modifications
- Escalation rate for compliance
- Compliance-related complaints
- Regulatory issues

Target:
- 0 compliance violations
- <5% escalation rate for compliance
- All high-risk phrases caught
```

