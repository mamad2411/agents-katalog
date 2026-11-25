---
name: ai-refund-fraud-and-abuse-pattern-detector
description: "Analyze refund requests and chargebacks against behavioral profiles to identify fraud patterns, assign risk scores, and recommend approval/denial/escalation. Use when the user needs chargeback protection, refund abuse prevention, or fraud detection for e-commerce."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","BUSINESS_DATA_SOURCE"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🛡️"}}
---

## Overview

The **AI Refund Fraud and Abuse Pattern Detector** protects solopreneurs, agencies, and small e-commerce businesses from systematic refund abuse and chargeback losses by automatically analyzing refund requests, returns, and dispute patterns against historical behavioral data.

This skill examines:
- **Serial returner detection** — identifies customers with abnormally high return rates
- **Geographic anomalies** — flags requests from unusual locations or IP addresses
- **Payment method mismatches** — detects inconsistencies between purchase and refund methods
- **Time-of-purchase correlations** — reveals patterns like bulk purchases followed by immediate refunds
- **Device fingerprinting** — tracks suspicious device/browser combinations
- **Historical behavioral scoring** — learns from your business's specific refund data to reduce false positives

Each request receives a **fraud likelihood score (0-100)** and an actionable recommendation: **Approve**, **Deny**, or **Escalate for Manual Review**.

### Why This Matters
Refund fraud costs small businesses an average of $10,000-$50,000+ annually. Manual review is time-consuming and inconsistent. This skill automates risk assessment, integrates with WordPress, Shopify, Stripe, PayPal, and custom databases, and learns from your historical data to improve accuracy over time.

---

## Quick Start

### Example 1: Analyze a Single Refund Request
```
Analyze this refund request for fraud risk:
- Customer: john.doe@example.com
- Order ID: ORD-2024-89234
- Purchase amount: $1,250 USD
- Purchase date: 2024-01-15 14:32 UTC
- Refund request date: 2024-01-16 03:15 UTC (19 hours later)
- Product: Premium software license (digital)
- Payment method: Visa ending in 4242
- Refund method requested: Bitcoin wallet (3FZbgi2...)
- Customer IP at purchase: 203.45.67.89 (Sydney, Australia)
- Customer IP at refund request: 185.220.101.45 (Amsterdam, Netherlands)
- Customer history: 12 refunds in last 90 days, 8 different products
- Device fingerprint: New device, first time using this browser
- Previous chargeback history: 3 chargebacks in 6 months
```

**Expected Output:** Fraud score 87/100 → **DENY** (multiple red flags: geographic mismatch, payment method mismatch, serial refunder, rapid refund request, chargeback history)

### Example 2: Batch Analyze Weekly Refunds
```
Analyze these 15 refund requests from this week's data and provide a summary report with fraud scores, risk categories, and escalation recommendations:
[Import CSV with columns: customer_id, order_id, amount, days_since_purchase, payment_method, refund_method, customer_country, refund_country, device_changes, previous_refunds, chargeback_history]
```

**Expected Output:** Summary table with risk tiers, 3-5 recommendations for escalation, patterns identified across the batch

### Example 3: Train on Historical Data
```
Train the fraud detector on our historical refund data from Q4 2023:
- Dataset: 2,847 refund requests
- Ground truth labels: 156 confirmed fraud cases, 2,691 legitimate refunds
- Business context: Digital SaaS products, 30-day money-back guarantee
- Geographic markets: US (60%), EU (25%), APAC (15%)
Please calibrate the model to reduce false positives while maintaining 95%+ fraud detection rate.
```

**Expected Output:** Model performance metrics, calibration report, new baseline thresholds specific to your business

---

## Capabilities

### 1. Real-Time Fraud Scoring
Assigns a **0-100 risk score** to every refund request based on:
- Customer behavioral history (refund frequency, average time-to-refund)
- Geographic inconsistencies (purchase location vs. refund location)
- Payment method anomalies (Visa → Bitcoin, credit card → wire transfer, etc.)
- Temporal patterns (purchases at 3 AM followed by refund requests within hours)
- Device fingerprinting (new devices, unusual browsers, VPN/proxy usage)
- Chargeback history and dispute frequency
- Product category risk (high-value digital goods vs. physical items)
- Velocity checks (multiple refund requests from same customer within short timeframe)

### 2. Custom Business Learning
The skill learns from your historical data to:
- Establish baseline refund rates by product category, geography, and customer segment
- Identify your business's unique fraud patterns (not generic rules)
- Reduce false positives by calibrating thresholds to your industry and customer base
- Track model performance over time and alert when accuracy drifts

### 3. Actionable Recommendations
Three-tier decision framework:
- **APPROVE** — Low risk (score 0-35), process immediately
- **ESCALATE** — Medium risk (score 35-70), flag for manual review with priority level
- **DENY** — High risk (score 70-100), recommend rejection with reason codes

### 4. Integration Support
- **Shopify** — Direct API integration via webhooks
- **WordPress + WooCommerce** — Plugin-ready, REST API compatible
- **Stripe** — Analyze disputes and refund events in real-time
- **PayPal** — Process refund notifications and chargeback data
- **Custom databases** — CSV, JSON, or SQL import/export
- **Slack** — Post alerts for high-risk requests requiring escalation
- **Google Sheets** — Auto-populate fraud scores and recommendations

### 5. Reporting & Analytics
- Weekly/monthly fraud trend reports
- Customer risk segmentation (low, medium, high)
- False positive/negative analysis for continuous improvement
- ROI tracking (recovered revenue vs. processing costs)
- Detailed audit trails for compliance (PCI, GDPR, SOC 2)

---

## Configuration

### Required Environment Variables
```bash
export OPENAI_API_KEY="sk-..."                    # OpenAI API key for LLM analysis
export BUSINESS_DATA_SOURCE="postgresql://..."    # Database connection string
export STRIPE_API_KEY="sk_live_..."               # (Optional) Stripe integration
export SHOPIFY_API_KEY="..."                      # (Optional) Shopify integration
export SLACK_WEBHOOK_URL="https://hooks.slack..." # (Optional) Slack alerts
```

### Configuration File (config.json)
```json
{
  "fraud_detection": {
    "score_threshold_approve": 35,
    "score_threshold_escalate": 70,
    "score_threshold_deny": 85,
    "false_positive_tolerance": 0.05,
    "min_historical_samples": 100
  },
  "business_context": {
    "industry": "saas",
    "primary_market": "US",
    "average_order_value": 299.99,
    "refund_window_days": 30,
    "chargeback_history_months": 12
  },
  "integrations": {
    "shopify_enabled": true,
    "stripe_enabled": true,
    "slack_alerts": true,
    "google_sheets_export": true
  },
  "model_tuning": {
    "learning_mode": true,
    "retraining_frequency": "weekly",
    "min_confidence_score": 0.75
  }
}
```

### Setup Instructions
1. **Authenticate** — Provide OpenAI API key and database credentials
2. **Import historical data** — Upload CSV or connect database with past 6-12 months of refund records
3. **Label ground truth** — Identify which historical refunds were confirmed fraud (if available)
4. **Calibrate thresholds** — Run initial test on 100 refunds, adjust score thresholds based on your risk tolerance
5. **Enable integrations** — Connect Shopify, Stripe, Slack, or custom webhooks
6. **Monitor performance** — Review weekly accuracy metrics and false positive rates

---

## Example Outputs

### Single Refund Analysis
```json
{
  "request_id": "REF-2024-45823",
  "customer_id": "cust_789abc",
  "fraud_score": 72,
  "recommendation": "ESCALATE",
  "confidence": 0.89,
  "risk_factors": [
    {
      "factor": "Geographic mismatch",
      "weight": 0.25,
      "details": "Purchase: US (IP 203.0.113.45), Refund: Russia (IP 198.51.100.89)"
    },
    {
      "factor": "Serial refunder",
      "weight": 0.20,
      "details": "8 refunds in 90 days (avg: 0.5 per customer)"
    },
    {
      "factor": "Payment method mismatch",
      "weight": 0.18,
      "details": "Purchased with Visa, requesting refund to bank account (different name)"
    },
    {
      "factor": "Rapid refund request",
      "weight": 0.15,
      "details": "Refund requested 14 hours after purchase (avg: 8 days)"
    },
    {
      "factor": "Device fingerprint anomaly",
      "weight": 0.12,
      "details": "New device, VPN detected at refund request"
    }
  ],
  "reason_codes": ["GEO_ANOMALY", "SERIAL_REFUNDER", "PAYMENT_MISMATCH", "VELOCITY_CHECK"],
  "suggested_action": "Request additional verification (ID, proof of purchase) before approving refund",
  "historical_context": {
    "customer_refund_rate": "66.7% (8 of 12 orders)",
    "avg_time_to_refund": "4.2 days",
    "chargeback_count": 2,
    "similar_cases": 23
  }
}
```

### Weekly Batch Report
```
WEEKLY FRAUD DETECTION SUMMARY
Generated: 2024-01-22

Total Refund Requests Analyzed: 147
Fraud Score Distribution:
  - Approve (0-35): 118 requests (80.3%)
  - Escalate (35-70): 22 requests (15.0%)
  - Deny (70-100): 7 requests (4.8%)

Top Risk Factors This Week:
  1. Geographic anomalies (45 cases)
  2. Serial returners (28 cases)
  3. Payment method mismatches (19 cases)
  4. Rapid refund requests (16 cases)
  5. Device fingerprint anomalies (12 cases)

Recommended Actions:
  - ESCALATE: customer@example.com (score 68) — Geographic + serial refunder
  - ESCALATE: john.doe@test.net (score 61) — Payment mismatch + velocity
  - DENY: fraudster@suspicious.ru (score 91) — Multiple critical flags

Model Performance:
  - Accuracy: 94.2% (vs. 91.8% last week)
  - False positive rate: 3.1% (target: <5%)
  - False negative rate: 2.7% (target: <2%)
  - Estimated fraud prevented: $8,340 (based on historical conversion)
```

---

## Tips & Best Practices

### 1. Calibrate to Your Business
- Generic fraud rules don't work for all industries. A 30-day refund request is normal for e-commerce but suspicious for SaaS.
- Train the model on **at least 100 historical refund records** with ground truth labels (fraud/legitimate).
- Adjust thresholds quarterly as your business grows and refund patterns evolve.

### 2. Combine with Manual Review
- Use this skill to **prioritize** manual reviews, not replace them entirely.
- For "ESCALATE" tier requests, add a quick verification step: request ID confirmation or proof of purchase.
- Track which escalated cases you approve vs. deny to continuously improve the model.

### 3. Monitor False Positives
- A 2-3% false positive rate is acceptable; higher rates damage customer trust.
- Review rejected refunds monthly—if legitimate customers are being denied, lower your thresholds.
- Use Slack alerts to catch edge cases before they become complaints.

### 4. Protect Customer Privacy
- Hash or anonymize personally identifiable information (PII) in logs and reports.
- Store historical data securely; comply with GDPR/CCPA requirements.
- Audit logs quarterly to ensure no sensitive data is exposed.

### 5. Integrate with Accounting
- Export fraud scores to your accounting system (QuickBooks, Xero) for revenue recognition.
- Track chargeback costs and compare against refund fraud losses to justify the investment.
- Use analytics to identify which products or customer segments have highest fraud rates.

---

## Safety & Guardrails

### What This Skill Will NOT Do
- **Make final decisions** — Recommendations are advisory only; humans retain final authority over refund approvals.
- **Guarantee fraud detection** — No model is 100% accurate; sophisticated fraudsters may evade detection.
- **Access payment card data** — The skill does NOT store or process full credit card numbers (PCI-compliant).
- **Discriminate based on protected characteristics** — The model is designed to exclude geographic location as a primary factor to avoid bias against certain countries.
- **Replace legal/compliance expertise** — Consult with a lawyer regarding refund policies and chargeback regulations in your jurisdiction.

### Limitations
- **Requires historical data** — The skill needs at least 100 refund records to establish baseline patterns; new businesses may see high false positive rates initially.
- **Geographic bias** — If your historical data is skewed toward US customers, the model may over-flag international requests. Rebalance training data as you expand globally.
- **Payment method limitations** — The skill works best with structured payment data (Stripe, PayPal). Custom payment processors may require manual mapping.
- **Evolving fraud tactics** — Fraudsters adapt; retrain the model monthly to stay ahead of new patterns.

### Compliance Considerations
- **GDPR** — Ensure you have consent to store and analyze customer refund data; provide data deletion on request.
- **PCI DSS** — This skill does NOT handle raw payment card data, but ensure your data pipeline is PCI-compliant.
- **Fair Lending** — Avoid using geographic location or customer demographics as primary fraud factors; use behavioral signals instead.
- **Transparency** — If you deny a refund based on fraud detection, be prepared to explain the reason to the customer.

---

## Troubleshooting

### Q: My fraud scores seem too high. Many legitimate customers are being flagged.
**A:** Your thresholds are likely too aggressive for your business model. 
- Lower the `score_threshold_escalate` from 70 to 55.
- Retrain the model on more recent historical data (fraud patterns evolve).
- Check if geographic location is over-weighted; some legitimate international customers may be penalized.
- Review false positives weekly and adjust weights accordingly.

### Q: The skill isn't detecting fraud in cases I know are fraudulent.
**A:** Your historical training data may not include enough fraud examples.
- Ensure you've labeled at least 20-30 confirmed fraud cases in your training set.
- Add new fraud patterns manually if you discover a novel attack (e.g., "bulk purchases of gift cards followed by refund requests").
- Increase the `min_confidence_score` threshold to lower the bar for flagging suspicious activity.

### Q: Integration with Shopify isn't working.
**A:** Verify webhook configuration:
- Check that your Shopify API credentials are valid and have `read_orders` and `read_refunds` scopes.
- Ensure the webhook URL is publicly accessible and returning HTTP 200 responses.
- Check Shopify's webhook logs in your admin panel for failed deliveries.
- Test with a manual refund request to confirm the skill receives the payload.

### Q: How do I export fraud scores to my accounting system?
**A:** Use the Google Sheets integration:
- Enable `google_sheets_export` in config.json.
- The skill will auto-populate a sheet