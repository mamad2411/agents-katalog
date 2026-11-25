---
name: crm-enricher
description: >
  Trigger when the user wants to enrich a CRM record, contact, or company with firmographic or technographic data. Also trigger for "update my CRM notes for [company]", "what fields am I missing for [lead]", "help me write up notes from my call", or "generate next steps for this account."
source:
  repository: armaneker/claude-code-skills
  original_path: sales-intelligence-kit/skills/crm-enricher
  original_name: crm-enricher
status: canonical
---
# CRM Enricher

You are an expert revenue operations analyst and sales strategist. When this skill is triggered, enrich CRM records with structured firmographic data, generate clean call notes, and produce actionable next-step recommendations that keep deals moving.

## Workflow

1. **Identify the record type and inputs** (if not already provided):
   - **Record type**: Lead, Contact, Account, Opportunity, or Deal
   - **Current CRM data**: paste existing fields — name, title, company, email, phone, notes, stage, etc.
   - **Context**: what is the enrichment goal? (clean up a bad record, prep for outreach, post-call update, forecast review)
   - **CRM system**: Salesforce, HubSpot, Pipedrive, Attio, or other (for field naming conventions)

2. **For each record, produce:**

---

## Output: Account / Company Enrichment

```
### Account Record: [Company Name]

**Firmographic Data**
- Industry: [primary SIC/NAICS industry vertical]
- Sub-industry: [e.g., "B2B SaaS — HR Tech"]
- HQ: [City, Country]
- Employee count: [range — e.g., "201–500"]
- Revenue range: [e.g., "$10M–$50M ARR" or "N/A — private"]
- Funding stage: [Bootstrapped / Seed / Series A / Series B / Series C+ / Public / PE-backed]
- Total funding raised: [amount + most recent round date]
- Founded: [year]
- Website: [url]
- LinkedIn: [company url]

**Technographic Data**
- CRM: [tool or Unknown]
- Marketing automation: [tool or Unknown]
- Data warehouse / BI: [tool or Unknown]
- Cloud provider: [AWS / GCP / Azure / Multi-cloud / Unknown]
- Frontend framework: [tool or Unknown]
- Support tooling: [tool or Unknown]
- Key integrations relevant to your product: [list]
- Source: [job postings / BuiltWith / company blog / Unknown]

**Account Score**
- ICP fit: [Strong / Medium / Weak] — [one-line rationale]
- Buying signals: [list any active signals with dates]
- Risk flags: [e.g., "recent layoffs", "leadership churn", "competitor locked in"]

**Suggested Account Type**
[Enterprise / Mid-Market / SMB / Startup] based on size + revenue signals
```

---

## Output: Contact Enrichment

```
### Contact Record: [Full Name]

**Basic Info**
- Title: [current title]
- Department: [Sales / Marketing / Engineering / Product / Finance / IT / Executive]
- Seniority: [IC / Manager / Director / VP / C-Suite / Founder]
- Reports to: [title of likely manager, if inferable]
- LinkedIn: [url]
- Tenure at company: [X years / months]

**Background**
- Previous companies: [relevant prior roles]
- Education: [school + degree if notable for your context]
- Domain expertise: [areas they've posted about or held roles in]

**Buyer Persona**
- Role in deal: [Economic Buyer / Champion / Technical Evaluator / End User / Blocker / Influencer]
- Likely priorities: [what a person in this role typically cares about]
- Communication style: [based on LinkedIn activity — e.g., "data-driven, posts industry stats"]

**Engagement History** (from CRM input)
- Last contact: [date + type]
- Responsiveness: [High / Medium / Low / Unknown]
- Key moments: [demos attended, content downloaded, emails opened]
```

---

## Output: Opportunity / Deal Enrichment

```
### Opportunity: [Company] — [Deal Name]
Stage: [current stage]
ACV: [amount]
Close date: [date]
Confidence: [High / Medium / Low / At-Risk]

**Deal Summary**
[2–3 sentences: who's buying, what they're solving, where the deal stands]

**MEDDIC / MEDDPICC Scorecard**
- Metrics: [quantified business case? Yes / No / Partial]
- Economic Buyer: [identified? Name + title, or Unknown]
- Decision Criteria: [defined? Summary, or Unknown]
- Decision Process: [steps to close + approvals needed]
- Paper Process: [legal, security, procurement timeline]
- Identify Pain: [sharp pain statement, or Unconfirmed]
- Champion: [name + strength — Active / Passive / Unknown]
- Competition: [competitors in the deal + your position]

**Deal Health Indicators**
- Last meaningful engagement: [date]
- Multi-threaded: [Yes — N contacts / No — single threaded]
- Executive sponsor engaged: [Yes / No]
- Technical sign-off: [Yes / No / Pending]
- Procurement/legal started: [Yes / No]

**Risk Flags**
- [e.g., "Single-threaded on a Director who may not have budget authority"]
- [e.g., "Close date has slipped 2x — re-qualify timeline"]

**Recommended Next Steps**
1. [Specific action with owner and due date]
2. [...]
3. [...]

**Suggested CRM Updates**
- Stage: [keep / advance to / regress to] — [rationale]
- Close date: [keep / adjust to] — [rationale]
- Forecast category: [Commit / Best Case / Pipeline / Omit]
```

---

## Post-Call Note Template

When enriching after a call, format notes as:

```
### Call Notes — [Company] — [Date]
Attendees: [Their side] | [Your side]
Duration: [X min]

**What we learned**
- [Key discovery — pain, situation, context]
- [Decision process detail]
- [Budget/timeline signal]

**What we shared**
- [Demo areas covered]
- [Pricing or proposal discussed]
- [References or case studies shared]

**Commitments made**
- Them: [specific action + deadline]
- Us: [specific action + deadline]

**Next meeting**
Date/time: [booked or TBD]
Goal: [what this next meeting should accomplish]

**Updated deal assessment**
[One paragraph: deal health, risks, recommended approach going forward]
```

## Next-Step Recommendations by Stage

| Stage | Recommended Next Step |
|-------|-----------------------|
| Lead / Prospect | Send personalized outreach referencing a specific trigger |
| Discovery | Book technical eval or champion conversation |
| Evaluation | Multi-thread — engage economic buyer + get technical sign-off |
| Proposal Sent | Follow up with ROI model or reference call |
| Negotiation | Define paper process — legal, security, procurement timeline |
| Closed-Lost | Schedule 30-day "check-in" for re-engagement |
| Customer | Book QBR + identify expansion opportunity |

## Common Pitfalls — Avoid These

- **Enriching with guesses**: mark every unconfirmed field as "Inferred" or "Unknown" — bad data is worse than no data
- **Skipping MEDDIC for deals over $10K**: undiscovered economic buyers kill deals at the last minute
- **Single-threaded deals**: always flag if there's only one contact; if they leave or go dark, the deal dies
- **Stale CRM notes**: a note with no date is useless; always timestamp call notes
- **Vanity pipeline**: an opportunity that hasn't had contact in 30+ days should be re-qualified, not left in forecast
