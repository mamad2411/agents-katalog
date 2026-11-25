---
name: ai-solopreneur-business-model-pivot-validator
description: "Simulate 12-month financial projections for solopreneur business pivots. Tests new models against 5000+ benchmarks, identifies cash flow risks, and generates go/no-go recommendations. Use when the user needs pivot validation, revenue forecasting, or business model stress testing."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_SHEETS_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

## Overview

The **AI Solopreneur Business Model Pivot Validator** is a strategic planning skill that eliminates guesswork from business pivots. Instead of spending months building a new revenue stream only to discover fatal flaws, this skill simulates the entire 12-month financial journey in minutes.

**Why This Matters:** Solopreneurs operate with limited capital and zero margin for error. A single bad pivot decision can drain 6 months of runway. This skill benchmarks your proposed changes against anonymized data from 5,000+ comparable solopreneur businesses (service providers, SaaS founders, digital product creators, consultants) to surface hidden risks before they become expensive problems.

**What It Does:**
- Ingests your current revenue metrics, customer composition, and operating costs
- Models your proposed pivot scenario (new service line, pricing change, product launch, market shift)
- Generates 12-month financial projections with weekly granularity for the first 8 weeks
- Identifies 8+ risk categories: cash flow gaps, customer churn acceleration, margin compression, CAC payback period extension, seasonal volatility, dependency concentration, tax liability shifts, and runway depletion
- Compares your scenario against relevant peer benchmarks
- Delivers a structured go/no-go recommendation with specific de-risking actions ranked by impact

**Integrations:** Works with Google Sheets (for historical data import), Slack (for async notifications), Stripe/PayPal APIs (for real revenue data), and exports to PDF/Excel for board presentations or investor pitches.

---

## Quick Start

Try these example prompts immediately:

### Example 1: Service-to-Product Pivot
```
I'm a freelance copywriter earning $8K/month from client work (3 clients, 
60% margins). I want to launch a $47/month AI writing course. I have $15K 
in savings and need to stay profitable. My biggest fear is losing clients 
during launch. Run a pivot simulation.
```

### Example 2: Pricing Change Stress Test
```
Current state: 50 SaaS customers at $99/month, 8% monthly churn, $2K/month 
operating costs. Proposal: Raise price to $149/month, expect 15% immediate 
churn but retain 85% of existing customers. Will this improve my financial 
position? Show me the 12-month projection.
```

### Example 3: Market Expansion Validation
```
I run a local WordPress maintenance service ($4K/month, 12 clients in 
Portland, Oregon). I want to go national with a white-label reseller model. 
I'll hire a part-time sales contractor ($2K/month) and project 20 new 
clients in months 3-12. Is this viable? What are the risks?
```

---

## Capabilities

### 1. **Financial Projection Engine**
Generates week-by-week cash flow forecasts for the first 8 weeks, then monthly for months 3-12. Accounts for:
- Revenue ramp curves (conservative S-curve by default, customizable)
- Customer acquisition cost (CAC) and payback periods
- Churn modeling (baseline + pivot-induced acceleration)
- Operating expense scaling (fixed vs. variable)
- Tax liability accrual (quarterly estimated payments)
- Runway calculation with buffer warnings

**Usage Example:**
```
"I'm launching a $997 group coaching program. I have 200 email subscribers 
with a 2% conversion rate baseline. I'll spend $500/month on ads. My fixed 
costs are $3K/month. Model the cash position over 12 months assuming 
conversion improves to 3% by month 6."
```

### 2. **Risk Identification & Scoring**
Analyzes 8 critical risk dimensions and flags scenarios that exceed solopreneur safety thresholds:

| Risk Category | Threshold | Action |
|---|---|---|
| **Cash Flow Gap** | >2 weeks of negative balance | Identify cost-cutting or funding needs |
| **Churn Acceleration** | >3x baseline rate | Validate product-market fit before scaling |
| **Margin Compression** | <25% gross margin | Flag sustainability issues |
| **CAC Payback** | >6 months | Question customer lifetime value |
| **Runway Depletion** | <90 days remaining | Recommend funding or pivot delay |
| **Dependency Concentration** | >30% revenue from 1 customer | Diversification required |
| **Seasonal Volatility** | >40% month-to-month variance | Build larger cash reserves |
| **Tax Liability Shift** | >$2K quarterly swing | Plan quarterly payments |

### 3. **Peer Benchmarking**
Compares your scenario against anonymized cohorts:
- Service providers (freelancers, agencies, consultants)
- Digital product creators (courses, templates, software)
- SaaS founders (subscription products)
- Hybrid models (productized services + passive income)

Metrics compared: CAC, LTV, churn rate, gross margin, time-to-profitability, seasonal patterns.

### 4. **Go/No-Go Recommendation Engine**
Delivers a structured recommendation:
- **GO** (Green): Proceed with confidence; execute within 30 days
- **GO WITH CAUTION** (Yellow): Proceed but implement specific de-risking actions first
- **NO-GO** (Red): Delay or redesign; current scenario has unacceptable risk

Each recommendation includes:
- Top 3 de-risking actions ranked by impact
- Specific metrics to monitor weekly
- Decision gates (e.g., "Pause CAC spend if churn exceeds 12%")
- Alternative pivot designs to explore

### 5. **Scenario Comparison**
Test multiple pivot variations in a single session:
```
"Compare 3 scenarios: (A) Launch at $47/month with $1K ad spend, 
(B) Launch at $97/month with $500 ad spend, (C) Delay 60 days and 
improve product before launch. Which is least risky?"
```

---

## Configuration

### Required Environment Variables
```bash
# OpenAI API key (GPT-4 for financial modeling)
export OPENAI_API_KEY="sk-..."

# Google Sheets API (optional, for automated data import)
export GOOGLE_SHEETS_API_KEY="AIzaSy..."

# Stripe API key (optional, for real revenue data)
export STRIPE_API_KEY="sk_live_..."
```

### Setup Instructions

1. **Gather Your Current Metrics**
   - Monthly recurring revenue (MRR) or average monthly revenue
   - Number of active customers/clients
   - Monthly churn rate (% of customers lost)
   - Gross margin percentage
   - Fixed monthly operating costs
   - Current cash runway (months of operations at burn rate)

2. **Define Your Pivot Scenario**
   - What revenue stream or model are you changing?
   - What's your revenue assumption for the new stream?
   - When do you expect it to launch?
   - What new costs will it introduce?
   - What customer segments might you lose?

3. **Run the Simulation**
   - Invoke the skill with your metrics and scenario
   - Review the 12-month projection
   - Examine the risk scorecard
   - Review peer benchmarks
   - Read the go/no-go recommendation

### Optional Parameters
```
--confidence-level: "conservative" | "moderate" | "aggressive" 
  (Default: "moderate" — adjusts ramp curves and churn assumptions)

--comparison-cohort: "service-providers" | "saas-founders" | "product-creators" | "all"
  (Default: "all" — filters peer benchmarks)

--export-format: "pdf" | "excel" | "json" | "google-sheets"
  (Default: "json" — output format for downstream processing)

--decision-gates: true | false
  (Default: true — includes weekly monitoring thresholds)
```

---

## Example Outputs

### Sample Output 1: Projection Summary
```
SCENARIO: Launch $97/month group coaching program
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FINANCIAL PROJECTIONS (12 months)
Current State: $8,000/month revenue, $2,000/month costs, 6-month runway

Month 1:  Revenue $8,200  |  Costs $2,500  |  Balance $5,700
Month 2:  Revenue $8,600  |  Costs $2,500  |  Balance $6,100
Month 3:  Revenue $9,400  |  Costs $2,500  |  Balance $6,900
Month 6:  Revenue $12,100 |  Costs $3,000  |  Balance $9,100
Month 12: Revenue $16,800 |  Costs $3,200  |  Balance $13,600

RUNWAY ANALYSIS
Current: 6.2 months
After Pivot (Month 12): 9.1 months (improvement)
Minimum Runway Hit: Month 4 (5.8 months remaining) ✓ Safe

CUSTOMER METRICS
Total Customers (Month 12): 156 (vs. 140 baseline)
New Coaching Members: 8 (conservative ramp)
Churn Rate: 7.2% (vs. 6.0% baseline) ⚠ Minor acceleration
CAC Payback: 4.2 months
LTV: $1,164 (based on 12-month average lifetime)
```

### Sample Output 2: Risk Scorecard
```
RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 Cash Flow Gap: PASS
   Minimum balance: $3,200 (Month 4)
   Threshold: $2,000
   Status: 60% buffer remaining

🟡 Churn Acceleration: CAUTION
   Projected: 7.2% vs. baseline 6.0%
   Risk: Existing clients may deprioritize service during launch
   Action: Communicate pivot plans to top 3 clients 60 days early

🟢 Margin Compression: PASS
   New gross margin: 71% (vs. 75% baseline)
   Status: Acceptable given revenue growth

🟢 CAC Payback: PASS
   Payback period: 4.2 months
   Threshold: <6 months
   Status: Healthy

🟢 Runway Depletion: PASS
   Runway improves from 6.2 → 9.1 months
   Status: Positive trajectory

🟢 Dependency Concentration: PASS
   Top customer: 12% of revenue
   Threshold: <30%
   Status: Well diversified

🟢 Seasonal Volatility: PASS
   Month-to-month variance: 8%
   Threshold: <40%
   Status: Predictable

🟢 Tax Liability: PASS
   Quarterly liability increase: $800
   Status: Manageable
```

### Sample Output 3: Peer Benchmarks
```
COMPARISON TO PEER COHORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cohort: Service-to-Product Hybrids (247 comparable solopreneurs)

METRIC                  YOUR SCENARIO    PEER MEDIAN    PERCENTILE
─────────────────────────────────────────────────────────────────
CAC                     $120             $145           65th
LTV:CAC Ratio           9.7x             8.2x           72nd
Gross Margin            71%              68%            58th
Monthly Churn           7.2%             8.1%           65th
Time to Profitability   2 months         3 months       62nd
Runway at Launch        6.2 months       5.8 months     58th

INTERPRETATION:
✓ Your CAC is 17% lower than peers (excellent unit economics)
✓ Your churn is 11% better than peers (strong retention)
⚠ Your gross margin is 4% higher than peers (validate pricing power)
→ You're positioned in the 60-70th percentile for this pivot type
```

### Sample Output 4: Go/No-Go Recommendation
```
RECOMMENDATION: GO WITH CAUTION (Yellow)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RATIONALE:
This pivot improves your financial position and sits in the 65th percentile 
for comparable solopreneurs. However, the 7.2% churn rate (vs. your 6.0% 
baseline) indicates potential client distraction during launch. Your runway 
remains healthy, but you have limited margin for execution delays.

REQUIRED DE-RISKING ACTIONS (in priority order):

1. COMMUNICATE EARLY (Impact: -2% churn mitigation)
   Action: Schedule 1:1 calls with top 5 clients 60 days before launch
   Goal: Secure commitment to continued service during transition
   Timeline: Week 1-2
   Success Metric: 0 unexpected churn in months 1-3

2. VALIDATE COACHING DEMAND (Impact: +15% confidence in ramp)
   Action: Survey email list (target: 50 responses) on pricing/format
   Goal: Confirm 2%+ conversion rate assumption
   Timeline: Week 2-3
   Success Metric: ≥2% survey respondents express intent to purchase

3. SOFT LAUNCH TO WARM AUDIENCE (Impact: -$500/month ad spend)
   Action: Offer free pilot to 3-5 existing clients before paid launch
   Goal: Generate testimonials + refine curriculum
   Timeline: Week 4-6
   Success Metric: 4+ positive reviews; curriculum improvements identified

WEEKLY MONITORING THRESHOLDS:

Week 1-4:
  • Unexpected churn: If >1 client leaves, pause external marketing
  • Ad spend efficiency: If CAC >$150, reduce ad budget 25%
  • Pilot feedback: If <3 positive responses, redesign curriculum

Week 5-8:
  • Conversion rate: If <1.5%, extend soft launch 30 days
  • Runway: If drops below 5 months, reduce fixed costs immediately

DECISION GATES:

✓ PROCEED if: 
  - Churn remains <7% through month 2
  - Conversion rate hits ≥1.5% in soft launch
  - Top 3 clients confirm continued engagement

✗ PAUSE if:
  - Unexpected churn exceeds 2 clients
  - Conversion rate <1% after 100 survey responses
  - Any single customer loss >15% of revenue

ALTERNATIVE SCENARIOS TO CONSIDER:

If you want lower risk:
  → Scenario B: Launch at $147/month with lower ad spend ($500/month)
     Reduces CAC by $25 but may slow customer acquisition

If you want higher upside:
  → Scenario C: Delay 60 days, validate demand first, then launch
     Improves confidence to 85%+ but delays revenue 2 months
```

---

## Tips & Best Practices

### 1. **Validate Your Input Assumptions**
The accuracy of projections depends entirely on your input metrics. Before running a simulation:
- Pull your last 3-6 months of actual revenue data (not estimates)
- Calculate churn rate from historical customer loss, not intuition
- Get your true operating costs from accounting records
- If launching a new product, research 5+ comparable offerings for pricing benchmarks

**Bad Input:** "I think I can get 100 coaching clients in 6 months"
**Good Input:** "I have 200 warm email subscribers with 2-3% historical conversion on past offers; I'll assume 2% on coaching"

### 2. **Run Multiple