---
name: ai-proposal-contract-risk-auditor
description: "Analyze vendor contracts and partnership proposals to flag unfavorable terms, identify negotiation leverage, and generate counter-proposal language. Use when the user needs contract review, risk assessment, or negotiation strategy for agreements."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","ANTHROPIC_API_KEY"],"bins":["node","python3"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"⚖️"}}
---

# AI Proposal & Contract Risk Auditor with Negotiation Leverage Finder

## Overview

This skill transforms contract review from a time-consuming legal expense into an automated, intelligent process. It analyzes incoming vendor agreements, partnership proposals, client contracts, and service terms to identify hidden liabilities, unfavorable clauses, missing protections, and negotiation opportunities.

**Why This Matters:**
- A single missed clause can cost thousands in unexpected liability or lost revenue
- Solopreneurs and small agencies typically lack in-house legal review
- Industry-standard contract benchmarks exist but aren't accessible to small teams
- Negotiation leverage is often left on the table due to lack of visibility

**Key Integrations:**
- **Google Drive & Docs:** Upload contracts directly for analysis
- **Slack:** Receive risk alerts and summaries in your workspace
- **WordPress & Client Portals:** Embed contract review workflows
- **Email:** Forward contracts for automated processing and reporting
- **Notion/Airtable:** Log all contract reviews with risk scores and action items

This skill uses Claude 3.5 Sonnet and GPT-4 for deep semantic analysis, comparing your agreements against 500+ industry-standard contract templates and benchmarks to surface non-standard, risky, or missing provisions.

---

## Quick Start

Try these prompts immediately:

### Example 1: Vendor SaaS Contract Review
```
Review this vendor agreement for risk and identify negotiation leverage:

[PASTE FULL CONTRACT TEXT OR UPLOAD FILE]

Focus on:
1. Data ownership and liability caps
2. Auto-renewal and termination clauses
3. Price escalation terms
4. Indemnification obligations
```

### Example 2: Partnership Proposal Analysis
```
Analyze this partnership proposal against industry standards:

[PASTE PROPOSAL]

Flag:
- Revenue split fairness (compare to 70/30 and 80/20 industry norms)
- Intellectual property ownership
- Exclusivity restrictions
- Term length and exit clauses
- Insurance and liability requirements

Suggest 3 counter-proposal modifications with specific language.
```

### Example 3: Client Service Agreement Audit
```
I'm using this client service agreement template. Identify:

[PASTE AGREEMENT]

1. Gaps that expose me to liability
2. Payment terms that could delay cash flow
3. Scope creep risks
4. Clauses that limit my ability to work with similar clients
5. Insurance/indemnity imbalances

Provide revised language for each gap.
```

---

## Capabilities

### 1. **Comprehensive Risk Scoring**
- **Overall Risk Score** (1-100): Aggregate assessment of contract favorability
- **Category Scores:** Data & IP, Liability & Indemnity, Payment Terms, Term & Termination, Compliance & Insurance
- **Red Flags:** Automatically highlighted with severity levels (Critical, High, Medium, Low)
- **Benchmark Comparison:** Shows how your terms compare to industry standards for your business type

**Example Output:**
```
Risk Assessment Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Risk Score: 72/100 (HIGH RISK)

Category Breakdown:
├─ Data & IP Protection: 45/100 🔴 CRITICAL
├─ Liability & Indemnity: 38/100 🔴 CRITICAL
├─ Payment Terms: 68/100 🟡 MEDIUM
├─ Term & Termination: 82/100 🟢 LOW
└─ Compliance & Insurance: 55/100 🟡 MEDIUM

Critical Issues Found: 3
High-Risk Issues: 5
```

### 2. **Negotiation Leverage Identification**
- Identifies asymmetrical obligations (they get more protections than you)
- Flags market-rate deviations (e.g., payment terms worse than 60% of similar deals)
- Spots missing reciprocal protections
- Highlights one-sided termination rights
- Surfaces unusual or non-standard clauses that signal negotiation room

**Example:**
```
NEGOTIATION LEVERAGE POINT #2: Liability Cap Asymmetry
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Current Language: "Vendor's liability capped at 12 months of fees"
Industry Standard: 3-6 months for SaaS, 12 months for professional services
Your Exposure: You indemnify them for unlimited amounts

Leverage Point: Their liability cap is ABOVE market for SaaS. Propose:
"Each party's liability capped at 6 months of fees, with exception for 
data breaches (capped at 12 months) and IP indemnification (uncapped)."

This brings alignment AND protects both parties fairly.
```

### 3. **Counter-Proposal Language Generator**
- Generates specific, market-tested alternative language for problematic clauses
- Includes "soft" versions (easier to negotiate) and "strong" versions
- Provides rationale for each change
- Maintains professional tone while protecting your interests
- Includes fallback positions if vendor won't accept primary language

**Example:**
```
CLAUSE REVISION: Payment Terms
Current: "Net 90 days from invoice date"
Your Concern: Cash flow impact; industry standard is Net 30-45

SOFT COUNTER (Easier to negotiate):
"Payment due within 45 days of invoice date. Invoices issued upon 
delivery/completion of services. Late payments subject to 1.5% monthly 
interest or applicable legal rate, whichever is lower."

STRONG COUNTER (Better for you):
"Payment due within 30 days of invoice date. Early payment (15 days) 
qualifies for 2% discount. Late payments accrue interest at 1.5% 
monthly. Overdue invoices (60+ days) may result in service suspension."

FALLBACK POSITION:
"Net 45 days with automatic payment plan: 50% upon delivery, 50% upon 
completion. This is our standard for all clients."
```

### 4. **Industry Benchmark Comparison**
- Compares your contract against 500+ templates across 20+ industries
- Shows percentile ranking (e.g., "Your payment terms are in the 25th percentile—worse than 75% of comparable deals")
- Highlights non-standard clauses specific to your industry
- Provides context on why certain terms are standard in your sector

### 5. **Missing Protections Audit**
- Identifies clauses that SHOULD be present but aren't
- Examples: Force majeure, data breach notification, IP indemnification, confidentiality, limitation of liability
- Provides template language for each missing protection
- Prioritizes by relevance to your business type

### 6. **Liability & Indemnity Analysis**
- Maps who bears risk for what scenarios
- Flags asymmetrical indemnification (you indemnify them more than vice versa)
- Identifies uncapped liability exposure
- Highlights third-party liability risks
- Suggests balanced alternatives

---

## Configuration

### Environment Variables Required

```bash
# OpenAI API Key (for GPT-4 analysis)
export OPENAI_API_KEY="sk-..."

# Anthropic API Key (for Claude 3.5 Sonnet benchmarking)
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional: Slack Integration
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Optional: Google Drive Integration
export GOOGLE_DRIVE_API_KEY="..."
```

### Setup Instructions

1. **Obtain API Keys:**
   - OpenAI: Visit https://platform.openai.com/api-keys
   - Anthropic: Visit https://console.anthropic.com/

2. **Set Environment Variables:**
   ```bash
   echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
   echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Optional Integrations:**
   - For Slack alerts: Create incoming webhook at https://api.slack.com/messaging/webhooks
   - For Google Drive: Enable Google Drive API in Google Cloud Console
   - For email forwarding: Set up email-to-OpenClaw integration in your email settings

### Configuration Options

```yaml
analysis_depth: "comprehensive"  # comprehensive | standard | quick
industry_benchmark: "saas"       # saas | professional-services | manufacturing | ecommerce
risk_threshold: "high"           # critical | high | medium (alerts only above this)
output_format: "detailed"        # detailed | summary | executive
include_templates: true          # Include revised clause templates
negotiation_aggressiveness: "balanced"  # aggressive | balanced | conservative
```

---

## Example Outputs

### Sample 1: Risk Summary Report

```
CONTRACT RISK AUDIT REPORT
═══════════════════════════════════════════════════════════════
Document: Acme SaaS Vendor Agreement v2.3
Analysis Date: 2024-01-15
Overall Risk Score: 68/100 (HIGH RISK - NEGOTIATE REQUIRED)

KEY FINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 CRITICAL (Must Address):
   1. Unlimited Liability for Data Breaches (Section 8.2)
      - Vendor has no cap on damages if their system is breached
      - Industry standard: 12 months of fees maximum
      - Recommendation: Propose capped liability with carve-out for willful misconduct

   2. Auto-Renewal with 60-Day Termination Notice (Section 3.1)
      - Contract auto-renews unless you provide notice 60 days in advance
      - Creates lock-in risk; easy to miss renewal deadline
      - Recommendation: Change to 30-day notice; require email confirmation

   3. Asymmetrical IP Indemnity (Section 6.4)
      - You indemnify them for IP claims, but they don't indemnify you
      - Exposes you to legal costs if their software infringes patents
      - Recommendation: Make reciprocal with mutual indemnification

🟡 HIGH RISK (Strongly Recommended):
   4. Unilateral Price Increase Rights (Section 4.2)
      - Vendor can increase prices 20% annually without your consent
      - No cap on cumulative increases
      - Recommendation: Propose annual cap (CPI + 3%) or right to terminate if increase >10%

   5. No Data Portability Guarantee (Section 7.3)
      - Contract silent on your ability to export data if relationship ends
      - Recommendation: Add: "Upon termination, Vendor shall provide all Customer 
        data in CSV/JSON format within 30 days, at no additional cost"

NEGOTIATION LEVERAGE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Strong Position: Their liability cap (12 months) is ABOVE market average (6 months)
  → You can negotiate it DOWN without appearing unreasonable

✓ Moderate Position: 60-day termination notice is non-standard
  → Industry average is 30 days; this gives you negotiating room

✗ Weak Position: IP indemnification is one-sided in their favor
  → They likely won't accept full reciprocity; propose carve-out for third-party claims only

RECOMMENDED COUNTER-PROPOSAL PRIORITIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. MUST CHANGE: Auto-renewal notice period (Section 3.1)
2. MUST CHANGE: Data breach liability cap (Section 8.2)
3. SHOULD CHANGE: Price escalation cap (Section 4.2)
4. NICE TO HAVE: Reciprocal IP indemnity (Section 6.4)
5. NICE TO HAVE: Data portability guarantee (Section 7.3)
```

### Sample 2: Clause-by-Clause Revision

```
SECTION 8.2: LIMITATION OF LIABILITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURRENT LANGUAGE:
"Vendor shall have no liability for any claims arising from Customer's 
use of the Services. Vendor's total liability shall not exceed the fees 
paid in the 12 months preceding the claim, except for data breaches, 
which shall be unlimited."

RISK ASSESSMENT:
├─ Severity: 🔴 CRITICAL
├─ Industry Percentile: 8th (worse than 92% of comparable contracts)
├─ Exposure: Unlimited liability for data breach = catastrophic risk
└─ Negotiability: HIGH (Vendor's position is extreme)

SOFT COUNTER (Recommended First Offer):
"Each party's liability for claims arising from breach of this Agreement 
shall be limited to the fees paid in the 12 months preceding the claim, 
except for: (a) willful misconduct or gross negligence, (b) data breaches 
caused by Vendor's failure to maintain industry-standard security, which 
shall be capped at 24 months of fees, and (c) indemnification obligations 
under Section 6, which shall be uncapped. This cap applies to all claims, 
whether in contract, tort, or otherwise."

RATIONALE:
✓ Maintains their 12-month cap for routine issues
✓ Adds reasonable cap (24 months) for data breaches
✓ Includes carve-out for willful misconduct (they'll accept this)
✓ Keeps IP indemnity uncapped (standard in SaaS)
✓ Shows you've researched industry standards

STRONG COUNTER (If Vendor Pushes Back):
"Vendor's liability capped at 24 months of fees for all claims except 
willful misconduct and IP indemnification. Customer's liability capped 
at 12 months of fees. Neither party liable for indirect or consequential 
damages."

FALLBACK POSITION:
"Vendor's liability capped at 18 months of fees for data breaches caused 
by Vendor's negligence; 12 months for all other claims. Data breach 
includes failure to encrypt data at rest, unauthorized access, or failure 
to notify Customer within 24 hours of discovery."
```

---

## Tips & Best Practices

### 1. **Prioritize Your Negotiations**
Don't try to change everything. The skill ranks issues by impact and negotiability:
- **MUST CHANGE:** Issues that create existential risk (unlimited liability, one-sided termination)
- **SHOULD CHANGE:** Issues that affect cash flow or operational flexibility
- **NICE TO HAVE:** Issues that are nice but won't break the deal

Start with MUST CHANGE items; use SHOULD CHANGE as trading chips.

### 2. **Use "Soft" Counter-Proposals First**
The skill generates both soft and strong versions. Always lead with soft:
- Soft versions are easier for the vendor to accept
- They show you're reasonable and have researched industry standards
- If vendor refuses soft version, you have strong version as backup
- Saves negotiation capital for truly critical issues

### 3. **Leverage the Benchmark Data**
When negotiating, reference the percentile rankings:
- "Payment terms at 25th percentile—worse than 75% of comparable deals"
- "Liability cap at 8th percentile—this is an outlier"
- "Industry standard for our type of agreement is 30-day termination notice, not 60"

Vendors often soften when they realize their terms are