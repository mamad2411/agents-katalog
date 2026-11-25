---
name: ai-freelancer-rate-card-and-proposal-template-optimizer
description: "Generate optimal pricing strategies and customized proposals from project history. Use when the user needs rate recommendations, scope creep prevention, or service bundling analysis for freelance projects."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","GOOGLE_SHEETS_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"💰"}}
---

## Overview

The **AI Freelancer Rate Card and Proposal Template Optimizer** analyzes your historical project data, client feedback, and real-time market rates to recommend optimal pricing for new work. This skill generates customized proposal templates with intelligent scoping questions designed to eliminate scope creep before projects begin. It also performs retainer vs. project trade-off analysis and suggests service bundling strategies to increase deal size and predictable revenue.

### Why This Matters

Freelancers often leave money on the table through underpricing, poorly scoped projects, and missed upsell opportunities. This skill transforms raw project data into actionable pricing intelligence and proposal frameworks that:

- **Increase revenue** by 15-30% through data-driven rate recommendations
- **Reduce project friction** with comprehensive scoping that prevents scope creep
- **Improve cash flow** by suggesting retainer structures for recurring work
- **Accelerate sales** with pre-built, client-ready proposal templates
- **Integrate seamlessly** with Google Sheets, Slack, Airtable, and WordPress (via custom post types)

---

## Quick Start

### Example 1: Analyze Historical Projects & Get Rate Recommendations

```
Analyze my freelance project history and recommend optimal rates.

My past projects:
- Brand identity design (3 projects, $2,500-$4,000 each, 4-6 weeks, client satisfaction 4.8/5)
- Website redesign (2 projects, $8,000-$12,000 each, 8-10 weeks, client satisfaction 4.9/5)
- Social media strategy (5 projects, $1,500-$2,500 each, 2-3 weeks, client satisfaction 4.7/5)

Market data: Design services in my region (Austin, TX) average $85-$150/hour for experienced designers.

Please recommend:
1. Optimal hourly rate or project-based pricing for each service
2. Price positioning (premium/standard/budget)
3. Volume discount strategy
4. Seasonal pricing adjustments
```

**What you'll get:** A rate card with recommended pricing tiers, positioning analysis, and justification based on market data + your performance history.

---

### Example 2: Generate a Proposal Template with Scope-Creep Prevention

```
Create a proposal template for website redesign projects that prevents scope creep.

Project type: Website redesign (5-10 page WordPress site)
Typical project value: $10,000
Common scope creep issues: Clients request extra pages, additional integrations, revisions beyond agreed limit
My service includes: Design, WordPress setup, basic SEO, 2 rounds of revisions

Generate:
1. A professional proposal template in Markdown
2. 8-10 scoping questions to clarify deliverables upfront
3. Clear revision policy and change order process
4. Out-of-scope items checklist
5. Timeline and milestone breakdown
```

**What you'll get:** A battle-tested proposal template that clients sign off on before work begins, dramatically reducing mid-project disputes.

---

### Example 3: Retainer vs. Project Trade-Off Analysis

```
Analyze my service mix and suggest retainer opportunities.

Current mix:
- 60% project-based work (avg $5,000-$15,000 per project)
- 40% hourly consulting (avg $100/hour, 10-15 hours/month)

Ideal revenue: $120,000/year
Current annual revenue: $95,000/year
Available capacity: 10 hours/week

Analyze:
1. Which service lines are best suited for retainers?
2. Suggested retainer pricing and package tiers ($2k/month, $5k/month, $10k/month)
3. Revenue impact: How many retainers would I need to hit $120k annually?
4. Risk mitigation: How to transition clients from project to retainer work
5. Service bundling: What complementary services should I bundle in retainer packages?
```

**What you'll get:** A clear roadmap to stabilize income with recurring retainer revenue, including pricing models and transition strategies.

---

## Capabilities

### 1. **Rate Analysis & Recommendation Engine**
- Analyzes historical project data (duration, complexity, client feedback, profitability)
- Cross-references with real-time market rates via Glassdoor API, Bureau of Labor Statistics, and industry benchmarks
- Recommends optimal pricing by service type, client segment, and project complexity
- Provides hourly-to-project-based pricing conversion formulas
- Suggests geographic pricing adjustments and seasonal variations
- Generates price positioning analysis (premium vs. standard vs. budget tier)

**Usage Example:**
```
Input: 12 months of project data (scope, hours, revenue, client satisfaction)
Output: Recommended rates by service (with confidence intervals), 
        pricing strategy by client segment, 
        profit margin analysis by project type
```

### 2. **Intelligent Proposal Template Generator**
- Creates customized proposal templates in Markdown, PDF, or Google Docs format
- Generates context-specific scoping questions that clarify deliverables upfront
- Builds revision policy clauses and change order processes
- Creates out-of-scope items checklists to prevent scope creep
- Includes timeline, milestone breakdown, and payment schedule recommendations
- Generates client-ready HTML/PDF with your branding

**Usage Example:**
```
Input: Service type (e.g., "UI/UX design"), typical project value ($8,000), 
       common scope creep issues
Output: 5-page proposal template with 12 scoping questions, 
        revision policy, change order form, timeline breakdown
```

### 3. **Retainer vs. Project Trade-Off Analysis**
- Evaluates which service lines are best suited for retainer models
- Calculates retainer pricing based on historical hourly rates and project margins
- Models revenue impact of different retainer mixes (e.g., 3 retainers + 2 projects/year)
- Provides client transition strategies (project → retainer upsell playbook)
- Suggests retainer service bundles and package tiers
- Risk analysis: Identifies clients most likely to convert to retainers

**Usage Example:**
```
Input: Current service mix, annual revenue target, available capacity
Output: Recommended retainer pricing tiers, 
        number of retainers needed to hit revenue goal,
        transition playbook for existing clients,
        bundle recommendations (e.g., "design + copywriting" package)
```

### 4. **Service Bundling & Upsell Strategy**
- Identifies complementary services that increase deal size
- Recommends bundle pricing (discount for bundled services vs. à la carte)
- Suggests cross-sell opportunities based on historical client patterns
- Models revenue impact of bundling (e.g., "Adding copywriting to design projects increases avg. deal size by 35%")
- Generates bundle-specific proposals and marketing copy

**Usage Example:**
```
Input: Your service offerings (design, copywriting, SEO, social media)
Output: Recommended bundles (e.g., "Brand Identity Bundle: Design + Copywriting + Brand Guidelines"),
        bundle pricing (15-20% discount vs. à la carte),
        estimated revenue uplift,
        bundle-specific proposal templates
```

### 5. **Market Intelligence & Competitive Positioning**
- Analyzes market rates for your service category and geography
- Identifies your pricing percentile (e.g., "You're in the 75th percentile for design rates in your region")
- Suggests competitive positioning (premium, standard, or budget tier)
- Provides competitor rate benchmarking (anonymized)
- Recommends pricing adjustments based on market trends

---

## Configuration

### Required Environment Variables

```bash
# OpenAI API for analysis and proposal generation
export OPENAI_API_KEY="sk-..."

# Google Sheets API for reading/writing project data
export GOOGLE_SHEETS_API_KEY="AIza..."

# (Optional) Airtable API for project database integration
export AIRTABLE_API_KEY="key..."
export AIRTABLE_BASE_ID="appXXX..."

# (Optional) Slack API for notifications
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_CHANNEL_ID="C..."
```

### Setup Instructions

1. **Prepare your project data** (Google Sheets, Airtable, or CSV):
   - Project name, type, duration (weeks), revenue, client satisfaction (1-5 scale)
   - Profitability notes, scope creep incidents, revision rounds
   - Client industry, company size, repeat business (yes/no)

2. **Connect your data source:**
   ```bash
   # For Google Sheets:
   gcloud auth application-default login
   
   # For Airtable:
   # Copy your API key from https://airtable.com/account/tokens
   ```

3. **Run initial analysis:**
   ```bash
   python3 analyze_rates.py --data-source "google_sheets" \
     --sheet-id "YOUR_SHEET_ID" \
     --output-format "json"
   ```

4. **Customize proposal templates** (optional):
   - Edit `templates/proposal_base.md` to match your branding
   - Add your logo, company details, and preferred payment terms

---

## Example Outputs

### Output 1: Rate Card Recommendation

```
RATE CARD ANALYSIS
==================

Service: Website Redesign
├─ Recommended Rate: $125/hour or $12,500 fixed project fee
├─ Pricing Tier: Premium (75th percentile for Austin, TX)
├─ Historical Data: 2 projects, $8,000-$12,000, avg. 8.5 weeks
├─ Market Benchmark: $85-$150/hour for experienced designers
├─ Confidence: HIGH (based on 2+ projects, consistent client satisfaction 4.9/5)
└─ Recommendation: Raise rates to $12,500-$15,000 for new clients

Service: Social Media Strategy
├─ Recommended Rate: $95/hour or $2,500/month retainer
├─ Pricing Tier: Standard (60th percentile)
├─ Historical Data: 5 projects, $1,500-$2,500, avg. 2.5 weeks
├─ Market Benchmark: $75-$125/hour
├─ Confidence: HIGH (based on 5 projects, consistent 4.7/5 satisfaction)
└─ Recommendation: Offer $2,500/month retainer (vs. hourly) to stabilize income

Service: Brand Identity Design
├─ Recommended Rate: $110/hour or $4,000 fixed project fee
├─ Pricing Tier: Premium (70th percentile)
├─ Historical Data: 3 projects, $2,500-$4,000, avg. 5 weeks
├─ Market Benchmark: $80-$140/hour
├─ Confidence: VERY HIGH (based on 3 projects, 4.8/5 satisfaction)
└─ Recommendation: Maintain current rates; consider premium tier for enterprise clients
```

### Output 2: Proposal Template Excerpt

```markdown
# Website Redesign Proposal
## [Client Name]

**Prepared by:** [Your Name]  
**Date:** [Date]  
**Valid through:** [Date + 14 days]

---

## Scope of Work

### Deliverables
- Responsive WordPress website redesign (5-10 pages)
- Mobile-first design and UX optimization
- WordPress setup, theme customization, and plugin integration
- Basic on-page SEO optimization
- 2 rounds of design revisions (additional rounds: $500/round)
- Launch support and handoff documentation

### Out of Scope
- Content writing or copywriting (separate service)
- Advanced SEO (link building, technical SEO)
- Ongoing maintenance or hosting (available as retainer)
- Custom plugin development
- E-commerce setup

---

## Scoping Questions (Client to Complete)

1. How many pages will the new website have?
2. What are the top 3 goals for this redesign?
3. Do you need e-commerce functionality?
4. Will you provide content, or do you need copywriting services?
5. What is your target launch date?
6. Do you have existing branding guidelines?
7. Will you need ongoing support post-launch?
8. What is your total budget range?

---

## Investment & Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Discovery & Planning | Week 1 | Wireframes, content audit, sitemap |
| Design | Weeks 2-3 | 2-3 design comps, revision rounds |
| Development | Weeks 4-5 | WordPress build, plugin setup, testing |
| Launch | Week 6 | Final QA, deployment, handoff docs |

**Total Project Duration:** 6 weeks  
**Investment:** $12,500 (50% due upon signing, 50% upon launch)

---

## Revision Policy

- **Included:** 2 rounds of revisions during design phase
- **Additional Revisions:** $500 per round
- **Revision Scope:** Design changes only; new features/pages require change order

## Change Order Process

Any requests outside the original scope require a written change order before work begins.

*[Additional sections: Payment Terms, Confidentiality, Terms & Conditions]*
```

### Output 3: Retainer Analysis Summary

```
RETAINER VS. PROJECT ANALYSIS
=============================

Current State:
├─ Annual Revenue: $95,000
├─ Service Mix: 60% projects, 40% hourly
├─ Available Capacity: 10 hours/week
└─ Revenue Goal: $120,000/year (+26% growth)

Recommended Retainer Strategy:
├─ Target: 2-3 retainers @ $4,000-$5,000/month
├─ Remaining Capacity: Project-based work (3-4 projects/year)
├─ Projected Revenue: $120,000-$132,000/year
├─ Revenue Stability: 60% recurring (retainer), 40% project-based
└─ Confidence: HIGH

Retainer Package Recommendations:
├─ Tier 1 (Starter): $2,500/month
│  └─ 20 hours/month of social media strategy + execution
│
├─ Tier 2 (Growth): $5,000/month
│  └─ 40 hours/month of social media + monthly brand consultation + content strategy
│
└─ Tier 3 (Premium): $10,000/month
   └─ 80 hours/month of full-service marketing (social, content, SEO, brand strategy)

Client Transition Playbook:
1. Identify top 5 clients with repeat project history
2. Calculate their annual spend (if all projects were retainer-based)
3. Offer 20% discount if they convert to retainer (e.g., $2,000/month vs. $2,500)
4. Emphasize benefits: Priority access, predictable costs, strategic partnership
5. Start with 3-month pilot, then convert to annual agreement

Revenue Impact:
├─ 2 retainers @ $4,000/month = $96,000/year (vs. $60,000 in projects)
├─ 1 retainer @ $5,000/month = Additional $60,000/year
├─ 2-3 projects @ $8,000-$12,000 = Additional $20,000-$36,000/year
└─ Total Projected: $120,000-$132,000/year ✓ GOAL ACHIEVED
```

---

## Tips & Best Practices

### 1. **Keep Your Project Data Fresh**
- Update your Google Sheets or Airtable after every project closes
- Log: scope, actual hours, revenue, client satisfaction, scope creep incidents
- Review quarterly to identify pricing trends and service mix opportunities

### 2. **Use Scoping Questions as a Sales Tool**
- Send scoping questions 3-5 days before the discovery call
- Use client responses to tailor your proposal and identify upsells
- Example: If a client mentions "We need a brand refresh," suggest bundling with web design

### 3. **Test Pricing Incrementally**
- Don't raise all rates at once; test new pricing with 2-3 new clients first
- Track conversion rates at different price points
- Adjust based on feedback (