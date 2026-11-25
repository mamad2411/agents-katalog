---
name: ai-b2b-intent-data-translator-and-account-scoring-customizer
description: "Normalize B2B intent signals from 6sense, Clearbit, ZoomInfo, LinkedIn and apply custom scoring logic to identify in-market accounts. Use when the user needs account prioritization, competitive intelligence, or daily sales briefings."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "INTENT_DATA_API_KEY",
          "CLEARBIT_API_KEY",
          "ZOOMINFO_API_KEY",
          "LINKEDIN_API_KEY",
          "SLACK_WEBHOOK_URL"
        ],
        "bins": ["python3", "curl"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "🎯"
    }
  }
---

## Overview

The **AI B2B Intent Data Translator and Account Scoring Customizer** solves the critical sales intelligence gap: multiple intent platforms show you the same 50 companies, but you don't know which ones are actually in-market for *your* solution versus your competitors.

This skill connects to your raw intent data sources (6sense, Clearbit, ZoomInfo, LinkedIn Sales Navigator) and normalizes conflicting signals into a unified scoring engine. You define custom weightings for your industry vertical—what matters for SaaS vs. manufacturing vs. financial services—and the skill automatically identifies which accounts to prioritize, why they're in-market, and what competitor threats exist.

**Why this matters:**
- Intent data platforms often disagree on company urgency (signal fragmentation)
- Generic scoring ignores your specific solution fit
- Sales teams waste time on low-intent accounts
- Daily briefings get lost in noise without personalization

**Integrations included:**
- 6sense (intent signals, firmographics)
- Clearbit (enrichment, technographics)
- ZoomInfo (contact data, buying committee)
- LinkedIn Sales Navigator (engagement signals, decision-maker activity)
- Slack (daily briefing delivery)
- Google Sheets (account tracking, historical scoring)

---

## Quick Start

### Example 1: Daily Priority Account Briefing

```
"Generate my daily intent briefing for accounts in the marketing automation 
space with $10M-$100M revenue. Prioritize by competitor threat (HubSpot, 
Marketo adoption signals) and buying committee activity. Send to Slack."
```

Expected output: Ranked list of 10-15 accounts with intent signals, buying committee changes, and recommended outreach angles.

### Example 2: Custom Scoring for Your Vertical

```
"Create a custom scoring model for enterprise security solutions. Weight 
these signals: 50% security tool searches, 30% recent CISO hires, 15% 
compliance audit signals, 5% budget mentions. Apply to my ZoomInfo and 
6sense data. Show me accounts scoring 80+."
```

Expected output: Normalized scoring rules + top 25 accounts with component scores.

### Example 3: Competitive Win/Loss Analysis

```
"Analyze accounts showing high intent for Salesforce CRM alternatives. 
Identify which are evaluating us vs. Pipedrive vs. Monday.com based on 
LinkedIn engagement, content consumption, and demo requests. Flag accounts 
we're losing."
```

Expected output: Competitive positioning matrix with account names, likelihood scores, and recommended counter-intelligence tactics.

### Example 4: Buying Committee Mapping

```
"For my top 50 intent accounts, pull all decision-makers from LinkedIn 
and ZoomInfo. Show job title changes in the last 90 days. Highlight new 
CFO/CTO hires. Create outreach sequences by role."
```

Expected output: Buying committee roster with engagement history and role-specific talking points.

---

## Capabilities

### 1. Multi-Source Intent Normalization
Ingests raw intent signals from 6sense, Clearbit, ZoomInfo, and LinkedIn, then normalizes conflicting data:
- **6sense:** Buying stage, intent keywords, account engagement trends
- **Clearbit:** Company tech stack, funding events, headcount changes
- **ZoomInfo:** Contact accuracy scores, org charts, recent hires
- **LinkedIn:** Profile views, content engagement, job changes

Outputs a unified signal confidence score (0-100) for each account.

### 2. Custom Vertical Scoring Engine
Define weighted scoring rules specific to your industry:
- Create custom signal categories (e.g., "security urgency," "budget availability")
- Assign weights based on your historical win data
- Apply decay functions (older signals matter less)
- A/B test scoring models against closed-won accounts
- Track which signals correlate with actual deals

### 3. Competitive Threat Detection
Identifies which accounts are evaluating competitors:
- Monitors competitor mention frequency in intent data
- Tracks competitor content consumption and demo attendance
- Flags accounts showing "competitor replacement" signals
- Suggests counter-positioning talking points

### 4. Buying Committee Intelligence
Extracts and tracks decision-maker activity:
- Maps org hierarchy from ZoomInfo + LinkedIn
- Identifies new executive hires (VP, C-suite)
- Tracks job title changes (promotion = buying authority shift)
- Shows engagement history per role
- Recommends outreach sequence by decision-maker type

### 5. Daily Briefing Automation
Generates prioritized account lists and delivers via Slack:
- Top 10-20 accounts by intent score (customizable threshold)
- New accounts entering "active buying stage"
- Accounts at risk of competitor win
- Buying committee changes
- Recommended next actions per account

### 6. Historical Scoring & Win Rate Analysis
Tracks scoring accuracy over time:
- Compares historical scores to closed deals
- Calculates ROI per intent signal type
- Identifies which signals predict fastest sales cycles
- Recommends signal reweighting based on performance

---

## Configuration

### Required Environment Variables

```bash
# Intent data sources
export INTENT_DATA_API_KEY="your_6sense_api_key"
export CLEARBIT_API_KEY="your_clearbit_api_key"
export ZOOMINFO_API_KEY="your_zoominfo_api_key"
export LINKEDIN_API_KEY="your_linkedin_sales_nav_api_key"

# Delivery & storage
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"
export GOOGLE_SHEETS_API_KEY="your_google_sheets_api_key"
export AIRTABLE_API_KEY="your_airtable_api_key"  # optional

# Skill configuration
export INTENT_BRIEFING_TIME="08:00"  # UTC time for daily briefing
export MIN_INTENT_SCORE="65"  # Only show accounts scoring 65+
export VERTICAL="saas"  # or "manufacturing", "financial_services", etc.
```

### Setup Instructions

1. **Connect your data sources:**
   - 6sense: Generate API token in Admin > Integrations
   - Clearbit: Create API key at clearbit.co/credentials
   - ZoomInfo: Request API access from your account manager
   - LinkedIn: Enable Sales Navigator API access

2. **Define your scoring model:**
   ```
   "Create a scoring config for [YOUR VERTICAL]. 
   Here are our top 10 closed-won accounts and the signals 
   that predicted them: [paste data]. Optimize weights."
   ```

3. **Set up Slack delivery:**
   - Create a Slack webhook in your workspace
   - Test with: `"Send a test briefing to Slack"`

4. **Initialize historical tracking:**
   - Connect Google Sheets or Airtable for score history
   - Skill will auto-log scores daily for win-rate analysis

---

## Example Outputs

### Daily Briefing (Slack Format)

```
🎯 ACCOUNT INTENT BRIEFING — Feb 14, 2025

TOP 5 PRIORITY ACCOUNTS:
1. TechCorp Inc. (Score: 94/100)
   • Intent: Active CRM search (6sense), 3 tool trials (Clearbit)
   • Threat: HubSpot demo attended Feb 12
   • Action: Call Sarah Chen (new VP Sales) — she follows us on LinkedIn
   
2. DataFlow Systems (Score: 89/100)
   • Intent: "data integration" search spike, new CTO hire
   • Threat: Low — no competitor signals
   • Action: Send CTO onboarding content, schedule 1:1

3. SecureBank Ltd. (Score: 87/100)
   • Intent: Security audit signals, compliance tool searches
   • Threat: Gartner Magic Quadrant review in progress
   • Action: Position as audit-ready, emphasize compliance reports

[... 2 more accounts ...]

NEW ENTRANTS (Entered "Active Buying" stage):
• FinanceFlow Corp — just hired 2 data engineers
• CloudScale Industries — searching for "scalable infrastructure"

AT-RISK ACCOUNTS (High intent but competitor engaged):
• OldVendor Corp — showing Salesforce competitor signals
```

### Scoring Model Example

```json
{
  "vertical": "saas_security",
  "signals": {
    "security_tool_searches": {
      "weight": 0.35,
      "decay_days": 30,
      "keywords": ["endpoint protection", "SIEM", "threat detection"]
    },
    "ciso_hire": {
      "weight": 0.25,
      "decay_days": 90,
      "source": "zoominfo"
    },
    "compliance_audit": {
      "weight": 0.20,
      "decay_days": 60,
      "indicators": ["SOC 2", "ISO 27001", "audit"]
    },
    "budget_mention": {
      "weight": 0.15,
      "decay_days": 45,
      "sources": ["earnings_calls", "6sense"]
    },
    "competitor_replacement": {
      "weight": -0.05,
      "decay_days": 0,
      "note": "Penalize if showing competitor engagement"
    }
  },
  "min_threshold": 65,
  "accuracy_vs_closed_deals": 0.78
}
```

### Buying Committee Report

```
ACCOUNT: TechCorp Inc.
Org Size: 850 employees | Industry: Software

DECISION-MAKERS:
┌─ Sarah Chen (VP Sales) — NEW HIRE (30 days)
│  LinkedIn: Follows your company, viewed 2 posts
│  Engagement: High (recent job change = buying authority)
│  Recommended angle: Sales efficiency, quota attainment
│
├─ Marcus Rodriguez (CTO) — 18 months tenure
│  LinkedIn: Engaged with your technical content
│  Engagement: Medium (technical buyer, secondary influence)
│  Recommended angle: Integration, API flexibility
│
└─ Jennifer Park (CFO) — Budget holder
   LinkedIn: No recent activity
   Engagement: Low (needs indirect outreach via Sarah)
   Recommended angle: ROI, cost savings vs. current tool

SUGGESTED OUTREACH SEQUENCE:
1. Sarah (primary) — 1:1 call on sales efficiency
2. Marcus (technical) — Product demo, integration deep-dive
3. Jennifer (CFO) — Business case, ROI comparison
```

---

## Tips & Best Practices

### 1. Calibrate Your Scoring Model with Historical Data
Don't guess at weights. Analyze your last 20 closed deals:
- Which intent signals appeared earliest?
- Which predicted shortest sales cycles?
- What threshold separates real opportunities from noise?

**Action:** Run "Analyze my last 20 closed-won accounts and optimize signal weights."

### 2. Combine Intent with Fit
High intent + low fit = wasted effort. Always cross-reference:
- Company size, industry, tech stack (Clearbit)
- Your ICP criteria
- Existing customer overlap (to avoid churn risk)

**Action:** "Score accounts only if they match our ICP: $50M-$500M revenue, SaaS, US-based, no existing customer overlap."

### 3. Prioritize Buying Committee Changes
New executives = new buying authority. Monitor:
- VP/C-suite hires in relevant departments
- Job title promotions
- LinkedIn profile updates

**Action:** "Alert me whenever a new VP or C-level hire appears at my top 50 accounts."

### 4. Use Competitive Signals as Timing Indicators
Competitor engagement ≠ you lose. Use it to:
- Time your outreach (call before they decide)
- Prepare counter-positioning
- Identify what you do better

**Action:** "For accounts showing Salesforce engagement, send me HubSpot comparison content."

### 5. Track Score Accuracy Over Time
Your scoring model will drift. Monthly:
- Compare scores to actual deal velocity
- Recalibrate weights based on recent wins
- Deprecate signals that don't predict deals

**Action:** "Generate a monthly scoring accuracy report. Show which signals predicted fastest closes."

### 6. Automate Outreach Sequencing
Don't manually decide who to call. Let the skill recommend:
- Which account to call first (highest intent + fit)
- Which buying committee member to target (role-based)
- What talking point to lead with (intent signal-based)

---

## Safety & Guardrails

### What This Skill Will NOT Do

**1. Violate Data Privacy Regulations**
- Will NOT export PII without explicit consent
- Will NOT use data for purposes outside agreed integrations
- Will NOT share account lists with third parties
- Complies with GDPR, CCPA, HIPAA where applicable

**2. Make Hiring or Discrimination Decisions**
- Will NOT use personal attributes (age, gender, race, religion) in scoring
- Will NOT filter accounts based on protected characteristics
- Will NOT make employment decisions

**3. Guarantee Conversion or ROI**
- Intent signals are probabilistic, not deterministic
- High intent ≠ guaranteed deal
- Skill provides recommendations; humans make final decisions

**4. Replace Human Judgment**
- Scoring is guidance, not law
- Sales reps should override scores when warranted
- Relationship and context matter more than signals

**5. Bypass Security or Compliance**
- Will NOT access accounts without proper API authentication
- Will NOT store credentials in plaintext
- Will NOT ignore your company's data governance policies

### Limitations

- **Data freshness:** Intent signals lag 1-7 days depending on source
- **Coverage gaps:** Smaller companies (<$5M) have sparse intent data
- **Accuracy variance:** Scoring accuracy ranges 65-85% depending on vertical
- **Integration dependencies:** Skill requires at least 2 data sources (1 intent + 1 enrichment)
- **Cost:** Running multiple data source queries incurs API costs (~$500-2000/month depending on account volume)

### Recommended Safeguards

1. **Audit scoring quarterly** against closed-lost accounts
2. **Train sales team** on how to interpret scores (not as gospel)
3. **Monitor for bias** in signal weights (e.g., don't over-weight company size)
4. **Set data retention policies** (e.g., delete scores after 90 days)
5. **Use with other tools** (pipeline, CRM, customer success data) for holistic view

---

## Troubleshooting

### Common Issues & Solutions

**Q: My daily briefing shows the same 20 accounts every day. Where's the new data?**

A: Intent data sources update on different schedules (6sense = 24h, LinkedIn = real-time). Try:
- `"Show me accounts that entered 'active buying stage' in the last 7 days"`
- Increase your `MIN_INTENT_SCORE` threshold to surface different accounts
- Expand your vertical/industry filters to see broader market activity

**Q: My scoring model shows 40% accuracy. How do I improve it?**

A: Your weights are misaligned with your actual sales motion. Debug with:
```
"Analyze my last 30 closed-won and closed-lost deals. 
For each, show what the old scoring model predicted vs. actual outcome. 
Identify which signals I'm over/under-weighting."
```

Then adjust weights and re-run against historical data.

**Q: I'm getting duplicate accounts across data sources. How do I deduplicate?**

A: The skill auto-deduplicates using company domain matching. If you still see duplicates:
- Check for company name variations ("Acme Inc." vs. "Acme Incorporated")
- Verify API keys are connected to the same workspace (not test vs. prod)
- Run: `"Deduplicate my account list using domain + company registry matching"`

**Q: Slack briefing isn't arriving at 8 AM. What's wrong?**

A: Check:
1. `SLACK_WEBHOOK_URL` is valid (