---
name: ai-proposal-to-contract-revenue-maximizer
description: "Analyze client proposals pre-signature to identify revenue leakage, compare against historical deals and benchmarks, and recommend contract modifications. Use when the user needs to maximize deal value, negotiate better terms, or flag compliance risks."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📋"
    }
  }
---

## Overview

The **AI Proposal-to-Contract Revenue Maximizer** is a strategic sales enablement tool designed to help solopreneurs, agencies, and small businesses identify hidden revenue opportunities in client proposals before signature. This skill analyzes contracts against historical closed deals, industry benchmarks, and pricing standards to surface underpriced scope, missing upsells, unfavorable payment terms, and legal/compliance red flags.

By leveraging advanced AI analysis (OpenAI GPT-4 and Claude), this skill automatically generates ranked recommendations sorted by revenue impact—enabling you to negotiate 15-25% better deal terms without requiring expensive legal counsel. It integrates seamlessly with proposal management platforms (PandaDoc, Proposify), CRM systems (HubSpot, Pipedrive), document storage (Google Drive, Dropbox), and communication tools (Slack, email) to streamline your deal review workflow.

**Why This Matters:**
- **Revenue Leakage**: Most small teams leave 10-30% of potential deal value on the table due to rushed negotiations
- **Scope Creep Prevention**: Identifies missing service boundaries and unpriced deliverables
- **Leverage Gaps**: Flags unfavorable payment schedules, missing retainer upsells, or inadequate liability caps
- **Compliance Risk**: Catches problematic legal language before it becomes expensive to fix
- **Speed**: Automates the 2-4 hour manual contract review process into 5 minutes

---

## Quick Start

### Example 1: Basic Proposal Analysis
```
Analyze this client proposal for revenue optimization:

Client: TechCorp Inc.
Service: 3-month digital marketing campaign
Proposed Fee: $15,000 flat
Scope: Social media management, content creation, monthly reporting
Payment Terms: 50% upfront, 50% at completion
Contract Length: 3 months, no renewal clause

Our average deal size: $22,500
Industry benchmark for this service: $18,000-$25,000
Historical upsells: paid ads management (+$5,000), strategy consulting (+$3,000)

What are the top 5 revenue gaps I should negotiate?
```

### Example 2: Comparative Deal Analysis
```
Compare this proposal against our last 5 similar deals:

CURRENT PROPOSAL:
- Client: HealthPlus Co.
- Service: Website redesign + 6 months support
- Fee: $8,500
- Payment: Net 30, no deposit
- Scope: Design, dev, 3 rounds revisions, email support

HISTORICAL DEALS (last 6 months):
1. SaaS startup - $12,000 (similar scope, paid ads training included)
2. E-commerce client - $11,500 (with 12-month support retainer)
3. Agency rebrand - $9,800 (included brand strategy workshop)
4. B2B manufacturer - $10,200 (with monthly optimization calls)

Identify underpricing and missing upsells with negotiation talking points.
```

### Example 3: Legal Risk & Compliance Check
```
Flag legal and compliance risks in this contract:

Contract excerpt:
- "Client may terminate for convenience with 5 days notice"
- "Contractor assumes all liability for third-party claims"
- "Intellectual property ownership: Client retains all rights to deliverables"
- "Payment terms: Net 60, with 2% monthly late fee"
- "Indemnification clause covers all damages without cap"

Our standard terms:
- 30-day termination notice
- Liability capped at contract value
- We retain IP until final payment
- Net 30 payment terms

What are the top compliance risks and recommended changes?
```

---

## Capabilities

### 1. **Revenue Leakage Detection**
Analyzes proposals against your historical deal database to identify:
- **Underpriced Scope**: Compares current fee to past similar projects and industry benchmarks
- **Missing Service Tiers**: Recommends premium add-ons based on client profile and deal size
- **Inadequate Retainer Structures**: Flags one-time projects that should include ongoing support
- **Scope Creep Indicators**: Identifies vague deliverables that lead to unpaid work

**Usage Example:**
```
Analyze for scope creep risks:
- Deliverable: "Website optimization" (undefined)
- Deliverable: "SEO improvements as needed" (open-ended)
- Timeline: "Until client is satisfied" (no completion criteria)
```

### 2. **Comparative Deal Intelligence**
Automatically surfaces gaps by comparing against:
- Your closed deals from the last 12-24 months (filtered by service type, client size, geography)
- Industry benchmarks from public datasets and pricing databases
- Competitor pricing (where available)
- Seasonal/market adjustments

**Output Includes:**
- Price per unit/hour/project comparison
- Payment term analysis (upfront %, deposit size, net days)
- Scope breadth scoring
- Upsell penetration rates

### 3. **Smart Upsell Recommendations**
Identifies complementary services based on:
- Client industry and company size
- Current service scope
- Historical upsell success rates
- Margin analysis by service line

**Example Recommendations:**
```
For a "Website Redesign" proposal:
- Tier 1 (High-Probability): Add paid ads strategy (+$3,000, 65% close rate)
- Tier 2 (Medium-Probability): Add monthly SEO consulting (+$2,000, 42% close rate)
- Tier 3 (Low-Probability): Add brand strategy workshop (+$4,500, 28% close rate)
```

### 4. **Payment Terms Optimization**
Analyzes and recommends improvements to:
- Deposit/upfront payment percentages (industry standard: 30-50%)
- Net payment days (standard: Net 15-30, not Net 60+)
- Late payment penalties and enforcement clauses
- Retainer vs. project-based structures
- Milestone-based payment schedules for multi-phase projects

### 5. **Legal Risk Flagging**
Identifies problematic contract language including:
- **Liability Issues**: Uncapped indemnification, "Client assumes all risk" clauses
- **IP Ownership**: Unfavorable intellectual property terms
- **Termination Clauses**: Insufficient notice periods or termination for convenience language
- **Scope Boundaries**: Missing service level agreements (SLAs) or undefined deliverables
- **Compliance Gaps**: Missing insurance requirements, confidentiality provisions
- **Regulatory Risks**: Industry-specific concerns (GDPR, HIPAA, PCI-DSS)

### 6. **Negotiation Talking Points**
Generates specific, data-backed language for conversations:
```
"Based on our analysis of similar projects, the fair market rate 
for this scope is $18,500-$22,000. We can offer you $19,500 
if we move the support period to 90 days instead of 6 months."
```

### 7. **Structured Output Ranking**
All recommendations are ranked by:
- **Revenue Impact** (highest first)
- **Negotiation Difficulty** (easy wins before hard fights)
- **Risk Level** (critical legal issues flagged separately)

---

## Configuration

### Required Environment Variables
```bash
# OpenAI API access (for detailed analysis and benchmarking)
export OPENAI_API_KEY="sk-..."

# Anthropic Claude API (for legal risk analysis)
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional: For direct integrations
export HUBSPOT_API_KEY="pat-..."        # CRM integration
export SLACK_WEBHOOK_URL="https://..."   # Slack notifications
export GOOGLE_DRIVE_API_KEY="..."        # Document import
```

### Configuration Options
```yaml
analysis_mode: "comprehensive"  # or "quick" (5 min) vs "deep" (15 min)
benchmark_source: "internal"    # or "industry" or "hybrid"
risk_threshold: "medium"        # Flag only medium+ risks
output_format: "json"           # or "markdown", "pdf"
auto_slack_notify: true         # Post results to Slack channel
```

### Setup Instructions

1. **Authenticate APIs:**
   ```bash
   export OPENAI_API_KEY="your-key-here"
   export ANTHROPIC_API_KEY="your-key-here"
   ```

2. **Upload Historical Deals (Optional but Recommended):**
   - Create a CSV with past 12-24 closed deals
   - Include: client name, service type, fee, scope, payment terms, close date
   - Skill will use this for benchmarking

3. **Configure Slack Integration (Optional):**
   - Create incoming webhook in Slack workspace
   - Paste webhook URL in environment variables
   - Skill will auto-post recommendations to designated channel

4. **Connect CRM (Optional):**
   - For HubSpot: Generate API key in Settings > Private Apps
   - Skill will auto-pull proposal data and log recommendations

---

## Example Outputs

### Standard Analysis Report
```json
{
  "proposal_id": "PROP-2024-001",
  "client_name": "TechCorp Inc.",
  "analysis_date": "2024-01-15T10:30:00Z",
  "revenue_summary": {
    "proposed_fee": 15000,
    "recommended_fee": 19500,
    "potential_uplift": 4500,
    "uplift_percentage": 30,
    "confidence_score": 0.87
  },
  "recommendations": [
    {
      "rank": 1,
      "category": "pricing",
      "title": "Increase base fee to market rate",
      "description": "Current $15k is 18% below market for this scope. Industry standard: $18-22k.",
      "revenue_impact": 3500,
      "difficulty": "medium",
      "talking_point": "Based on our analysis of similar projects completed in 2023-2024, the fair market rate for this scope is $18,500-$22,000. We'd recommend $19,500.",
      "implementation": "Modify line item 'Digital Marketing Services' from $15,000 to $19,500"
    },
    {
      "rank": 2,
      "category": "upsell",
      "title": "Add paid ads management service",
      "description": "Client is not budgeting for paid advertising strategy. Historical close rate: 65% for this add-on.",
      "revenue_impact": 5000,
      "difficulty": "easy",
      "talking_point": "We typically include paid ads strategy with campaigns this size. For an additional $5,000, we can manage your Google Ads and Facebook campaigns.",
      "implementation": "Add new line item 'Paid Ads Management' at $5,000/month"
    },
    {
      "rank": 3,
      "category": "payment_terms",
      "title": "Adjust payment schedule to reduce cash flow risk",
      "description": "Current terms (50/50 at completion) are unfavorable. Recommend 50% upfront, 25% at 30 days, 25% at completion.",
      "revenue_impact": 0,
      "difficulty": "medium",
      "risk_reduction": "high",
      "talking_point": "To ensure project continuity and resource allocation, we typically require 50% upfront, with the balance split across milestones.",
      "implementation": "Modify payment schedule section"
    }
  ],
  "legal_risks": [
    {
      "severity": "high",
      "issue": "Uncapped indemnification clause",
      "current_language": "Contractor assumes all liability for third-party claims",
      "recommended_language": "Contractor liability capped at total contract value ($19,500)",
      "impact": "Protects against unlimited financial exposure"
    },
    {
      "severity": "medium",
      "issue": "Vague termination clause",
      "current_language": "Client may terminate for convenience with 5 days notice",
      "recommended_language": "Client may terminate with 30 days written notice after 30-day trial period",
      "impact": "Provides project stability and resource planning certainty"
    }
  ],
  "benchmark_analysis": {
    "your_proposal": {
      "fee": 15000,
      "scope_breadth": "medium",
      "payment_terms": "unfavorable"
    },
    "market_average": {
      "fee": 19500,
      "scope_breadth": "medium",
      "payment_terms": "standard"
    },
    "your_historical_avg": {
      "fee": 18200,
      "scope_breadth": "medium",
      "payment_terms": "standard"
    }
  }
}
```

### Slack Summary (Auto-Posted)
```
📋 Proposal Analysis Complete: TechCorp Inc.

💰 Revenue Opportunity: +$4,500 (30% uplift)
⚠️ Legal Risks: 2 issues flagged (1 high, 1 medium)
✅ Easy Wins: Paid ads upsell (+$5k, 65% close rate)

Top 3 Actions:
1. Increase base fee from $15k → $19.5k (market rate)
2. Add paid ads management (+$5k/month)
3. Fix indemnification clause (liability cap)

View full analysis: [Link to dashboard]
```

---

## Tips & Best Practices

### 1. **Prepare Your Historical Data**
- Upload your last 20-30 closed deals for more accurate benchmarking
- Include: client size, industry, service type, fee, scope, payment terms, close date
- Skill learns from your pricing patterns and upsell success rates

### 2. **Use the "Difficulty Filter"**
```
Show me only "easy" negotiation wins that I can close in one call.
(vs. showing all 15 recommendations that might overwhelm the client)
```

### 3. **Leverage Talking Points Directly**
- Copy/paste recommended language into your proposal counter-offer
- Data-backed suggestions increase negotiation success by ~40%
- Use "Based on our analysis..." framing to appear professional, not aggressive

### 4. **Focus on Upsells Before Price Increases**
- Clients often accept new services more easily than price hikes
- Recommend paid ads management before raising base fee
- Position as "value-add" rather than "we underpriced"

### 5. **Flag Legal Risks Early**
- Don't negotiate price if contract has critical legal problems
- Address indemnification, IP ownership, and termination clauses first
- Legal fixes often unlock better payment terms as goodwill gesture

### 6. **Use Industry Benchmarks Strategically**
```
"Industry average for this service is $18-22k. 
We're offering you $19.5k, which is 12% below market."
(vs. "Our price is $19.5k" — much weaker)
```

### 7. **Automate Slack Notifications**
- Set skill to post analysis summaries to your sales channel
- Team can review recommendations before client calls
- Reduces time-to-insight from hours to minutes

### 8. **Compare Against Your Own Deals First**
- If you have historical data, use "internal" benchmark mode
- Your own deals are more relevant than generic industry data
- Identifies if you're pricing inconsistently across similar clients

---

## Safety & Guardrails

### What This Skill Does NOT Do

**❌ Not a Legal Advisor**
- This skill flags legal risks but is NOT a substitute for qualified legal counsel
- For contracts >$50k or with complex IP/liability issues, consult an attorney
- Recommendations are educational; you remain responsible for final contract terms

**❌ Not a Binding Negotiation Tool**
- Suggested talking points are conversation starters, not ultimatums
- Client may reject recommendations; skill has no enforcement mechanism
- Always maintain professional, collaborative tone in negotiations

**❌ Not a Guarantee of Deal Closure**
- Skill recommends optimal terms, but market conditions vary
- Some clients have fixed budgets and won't negotiate
- Uplift percentages (15-25%) are aver