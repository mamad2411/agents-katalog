---
name: modopro
description: "Automate social media content moderation with real-time analysis, policy enforcement, and compliance tracking. Use when the user needs to moderate user-generated content, enforce community guidelines, or scale content review across multiple platforms."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["MODOPRO_API_KEY", "OPENAI_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🛡️"
    }
  }
---

## Overview

ModoPro is an enterprise-grade content moderation skill that automates the detection, categorization, and handling of policy-violating content across social media platforms. Instead of manually reviewing thousands of posts daily, ModoPro uses AI-powered analysis to flag inappropriate content, categorize violations, and enforce your custom community guidelines in real-time.

**Why ModoPro Matters:**
- **Scale Without Manual Labor**: Review 10,000+ posts/day without hiring moderators
- **Compliance & Legal Protection**: Maintain audit trails and policy enforcement logs
- **Platform Integration**: Works with WordPress comments, Slack channels, Twitter/X, Facebook, Instagram, TikTok, and custom APIs
- **Customizable Policies**: Define your own rules—what's inappropriate for a gaming community differs from a parenting forum
- **Real-Time Blocking**: Automatically hide, remove, or quarantine violating content before human eyes see it

ModoPro reduces moderation costs by 70-80% while improving response time from hours to seconds.

---

## Quick Start

Try these prompts immediately to see ModoPro in action:

### Example 1: Analyze a Single Post
```
Moderate this social media post using ModoPro:
"Check out this amazing deal on fake designer bags! DM for link"

Policy: Enforce against spam, counterfeit goods, and suspicious links.
```

### Example 2: Batch Moderate Comments
```
ModoPro: Analyze these 50 YouTube comments and categorize violations:
[paste comments here]

Return: violation_type, confidence_score, recommended_action, policy_reference
```

### Example 3: Create Custom Moderation Policy
```
ModoPro: Create a content moderation policy for a fitness coaching community.
Include rules for: spam, harassment, medical misinformation, and self-harm content.
Format as JSON with severity levels (low, medium, high, critical).
```

### Example 4: Real-Time Stream Moderation
```
ModoPro: Monitor this Twitch chat stream and flag violations every 30 seconds.
Integrate with Slack: Send alerts to #moderation channel for critical violations.
```

---

## Capabilities

### 1. **Automated Content Analysis & Categorization**
ModoPro analyzes text, URLs, and metadata to detect:
- **Spam & Manipulation**: Duplicate posts, link farms, engagement farming
- **Harassment & Hate Speech**: Bullying, slurs, targeted attacks (multi-language support)
- **Misinformation**: Health claims, conspiracy theories, election fraud narratives
- **Adult Content**: Explicit sexual material, adult services
- **Violence & Self-Harm**: Threats, glorification of violence, suicide/eating disorder content
- **Intellectual Property**: Piracy links, counterfeit goods, unauthorized resales
- **Phishing & Scams**: Credential harvesting, financial fraud, fake giveaways
- **Doxxing & Privacy Violations**: Personal information exposure

**Usage Example:**
```
ModoPro analyze-content
--input "Just got paid $5000 working from home! Click here: [suspicious-link.ru]"
--policy-id "default_social_media"
--confidence-threshold 0.75
```

**Output:**
```json
{
  "content_id": "post_12345",
  "violations": [
    {
      "type": "spam",
      "severity": "high",
      "confidence": 0.89,
      "reason": "Classic work-from-home spam with suspicious domain",
      "policy_reference": "SPAM_001"
    }
  ],
  "recommended_action": "hide_post",
  "priority": "medium"
}
```

### 2. **Real-Time Moderation & Blocking Protocols**
- **Auto-Hide**: Immediately hide violating content from feed (visible only to poster)
- **Auto-Remove**: Delete content permanently with notification to user
- **Quarantine**: Move to review queue for human verification
- **Rate Limiting**: Temporarily restrict user posting if violation pattern detected
- **Account Suspension**: Flag accounts with repeated critical violations
- **Webhook Integration**: Trigger actions in WordPress, Slack, Discord, or custom systems

**Usage Example:**
```
ModoPro enforce-policy
--platform "wordpress_comments"
--policy-id "parenting_forum"
--auto-action "hide_and_notify_user"
--escalate-to-human-if-confidence-below 0.85
--webhook-url "https://your-app.com/moderation-webhook"
```

### 3. **Customizable Content Policies & Guidelines**
Create policies tailored to your community:

```json
{
  "policy_id": "gaming_community",
  "name": "Gaming Community Standards",
  "rules": [
    {
      "id": "SLUR_001",
      "category": "hate_speech",
      "severity": "critical",
      "trigger_patterns": ["offensive_words_list"],
      "action": "immediate_removal",
      "user_notification": "Your post violated our code of conduct regarding respectful language"
    },
    {
      "id": "SPAM_002",
      "category": "spam",
      "severity": "high",
      "trigger_patterns": ["link_farm", "duplicate_posting"],
      "action": "hide_and_rate_limit",
      "rate_limit": "1_post_per_hour_for_24h"
    }
  ]
}
```

### 4. **Audit Trails & Compliance Logging**
Every moderation decision is logged with:
- Timestamp, content ID, policy applied, confidence score
- Action taken, moderator ID (if human-reviewed)
- Appeal status and resolution
- GDPR-compliant data retention

---

## Configuration

### Required Environment Variables
```bash
# ModoPro API credentials
export MODOPRO_API_KEY="sk_live_xxxxxx"

# OpenAI for advanced NLP analysis
export OPENAI_API_KEY="sk-xxxxx"

# Optional: Platform integrations
export WORDPRESS_API_KEY="your_key"
export SLACK_BOT_TOKEN="xoxb-xxxxx"
export TWITTER_BEARER_TOKEN="xxxxx"
```

### Setup Instructions

1. **Obtain ModoPro API Key**
   - Register at [modopro.io](https://modopro.io)
   - Generate API key in dashboard
   - Set `MODOPRO_API_KEY` environment variable

2. **Configure Your Policy**
   ```bash
   modopro policy create \
     --name "my_community" \
     --template "social_media" \
     --severity-levels "low,medium,high,critical"
   ```

3. **Connect Platforms**
   ```bash
   modopro integrate wordpress \
     --site-url "https://mysite.com" \
     --api-key "your_wordpress_key"
   
   modopro integrate slack \
     --workspace "my-workspace" \
     --token "xoxb-token"
   ```

4. **Set Moderation Actions**
   ```bash
   modopro config set \
     --auto-hide-threshold 0.85 \
     --auto-remove-threshold 0.95 \
     --escalate-threshold 0.70
   ```

---

## Example Outputs

### Single Post Analysis
```json
{
  "post_id": "fb_post_987654",
  "timestamp": "2024-01-15T14:32:00Z",
  "content": "Buy cheap meds online no prescription needed!!!",
  "analysis": {
    "violations": [
      {
        "type": "illegal_activity",
        "category": "drug_distribution",
        "severity": "critical",
        "confidence": 0.97,
        "triggered_rules": ["ILLEGAL_001", "SPAM_003"],
        "explanation": "Promoting illegal pharmaceutical sales without prescription"
      }
    ],
    "sentiment": "negative",
    "language": "en",
    "toxicity_score": 0.42
  },
  "recommended_action": "remove_immediately",
  "escalation": {
    "escalate_to_human": true,
    "priority": "urgent",
    "assigned_to": "legal_team"
  }
}
```

### Batch Moderation Report
```json
{
  "batch_id": "batch_20240115_001",
  "total_items_processed": 250,
  "processing_time_seconds": 12,
  "summary": {
    "clean_content": 198,
    "violations_detected": 52,
    "auto_hidden": 38,
    "auto_removed": 8,
    "escalated_to_human": 6
  },
  "violation_breakdown": {
    "spam": 22,
    "harassment": 15,
    "misinformation": 10,
    "adult_content": 3,
    "other": 2
  },
  "actions_taken": [
    {
      "content_id": "post_001",
      "action": "hidden",
      "reason": "spam",
      "user_notified": true
    }
  ]
}
```

### Policy Compliance Report
```json
{
  "period": "2024-01-01 to 2024-01-31",
  "policy_id": "ecommerce_marketplace",
  "metrics": {
    "total_posts_reviewed": 15000,
    "violations_caught": 342,
    "false_positive_rate": 0.03,
    "average_response_time_ms": 240,
    "human_review_escalations": 28
  },
  "top_violations": [
    {"type": "spam", "count": 156, "percentage": 45.6},
    {"type": "counterfeit_goods", "count": 89, "percentage": 26.0},
    {"type": "harassment", "count": 67, "percentage": 19.6}
  ]
}
```

---

## Tips & Best Practices

### 1. **Start Conservative, Iterate**
Begin with auto-hide (not auto-remove) to catch false positives. Monitor for 1-2 weeks, then gradually increase automation confidence thresholds.

### 2. **Customize by Community Type**
Gaming communities tolerate trash talk; parenting forums don't. Use different policies:
```bash
modopro policy apply --community-id "gaming" --strictness "low"
modopro policy apply --community-id "parenting" --strictness "high"
```

### 3. **Monitor False Positives Weekly**
Review escalated content flagged as violations but approved by humans. Adjust patterns:
```bash
modopro report false-positives --period "7d" --export-json
```

### 4. **Use Context Signals**
Combine text analysis with user behavior:
- New account + spam pattern = higher confidence
- Established user + one violation = lower action threshold
- Rapid posting = rate limit even if content is borderline

### 5. **Leverage Appeals Process**
Users can appeal moderation decisions. Use appeals data to refine policies:
```bash
modopro insights appeals --last-30-days --sort-by-overturned-rate
```

### 6. **Integrate with Moderation Tools**
Connect to:
- **Slack**: Get alerts for critical violations
- **Jira**: Auto-create tickets for human review
- **Zendesk**: Link moderation appeals to support tickets
- **Google Sheets**: Export weekly reports for leadership

---

## Safety & Guardrails

### What ModoPro Will NOT Do
- **Override Legal Jurisdiction**: ModoPro flags content; YOU decide legality based on your jurisdiction
- **Detect Images/Video**: Text-only analysis (image moderation requires separate integration)
- **Moderate Private Messages**: Designed for public content only
- **Replace Human Judgment**: Always maintain human review for critical decisions (legal, account bans)
- **Guarantee 100% Accuracy**: AI-based detection has ~3-5% false positive rate; humans must verify

### Limitations & Boundaries
- **Language Support**: English, Spanish, French, German, Chinese (Simplified/Traditional), Japanese, Korean. Other languages have reduced accuracy.
- **Latency**: Real-time processing adds 200-500ms to post publication
- **Cultural Context**: May miss sarcasm, regional slang, or context-dependent violations
- **Evolving Threats**: New slang, memes, and coded language requires policy updates every 2-4 weeks
- **Rate Limits**: Free tier: 1,000 posts/day; Pro: 100,000 posts/day

### Data Privacy & Compliance
- **GDPR**: Compliant; data deleted after 90 days unless legally required
- **CCPA**: User data not sold; audit trails available for compliance
- **HIPAA**: NOT compliant; do not use for healthcare content
- **PCI-DSS**: NOT compliant; do not analyze payment card data

### Responsible Use
- Disclose to users that automated moderation is in place
- Provide clear appeals process
- Don't use solely for political/ideological censorship
- Train human moderators on policy decisions for consistency
- Review moderation patterns quarterly for bias

---

## Troubleshooting

### Issue: High False Positive Rate (>5%)
**Diagnosis**: Confidence thresholds too aggressive

**Solution**:
```bash
# Increase auto-hide threshold from 0.80 to 0.88
modopro config set --auto-hide-threshold 0.88

# Review flagged content
modopro report false-positives --last-7d
```

### Issue: Spam Still Getting Through
**Diagnosis**: Policy rules not updated for new spam patterns

**Solution**:
```bash
# Check latest spam trends
modopro insights violations --category spam --period 7d

# Add new patterns
modopro policy rule add \
  --policy-id "default" \
  --pattern "crypto_pump_and_dump" \
  --severity high
```

### Issue: Slow Processing (>500ms latency)
**Diagnosis**: API rate limits or network congestion

**Solution**:
```bash
# Use batch processing instead of real-time
modopro batch process --input posts.json --batch-size 100

# Check API quota
modopro account quota
```

### Issue: Appeals Not Being Tracked
**Diagnosis**: Webhook not configured or failing silently

**Solution**:
```bash
# Test webhook
modopro webhook test \
  --url "https://your-app.com/moderation-webhook" \
  --verbose

# Check logs
modopro logs --component webhook --last-24h
```

### FAQ

**Q: Can ModoPro detect context? (e.g., "I hate this bug" vs. "I hate this person")**
A: Partially. ModoPro uses NLP to detect context but isn't perfect. Always pair with human review for borderline cases.

**Q: How do I handle appeals?**
A: Users can appeal via API. Create a workflow: Appeal → Human Review → Restore or Uphold. Store all decisions for audit.

**Q: Can I use ModoPro for private communities (Discord, Slack)?**
A: Yes! Set `--mode private` and adjust policies. Slack integration is built-in; Discord requires webhook setup.

**Q: What's the cost?**
A: Pricing at modopro.io. Free tier: 1,000 posts/day. Pro: $99/mo for 100K posts/day. Enterprise: Custom.

**Q: Does ModoPro work in non-English languages?**
A: Yes, with reduced accuracy (85-90% vs. 95% for English). Best for Spanish, French, German, Chinese, Japanese, Korean.

---

## Getting Help

- **Documentation**: https://docs.modopro.io
- **Support**: support@modopro.io
- **Community**: https://community.modopro.io
- **Status**: https://status.modopro.io