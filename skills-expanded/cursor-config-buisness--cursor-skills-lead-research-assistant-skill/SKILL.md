---
name: lead-research-assistant
description: Identifies high-quality leads for your product or service by analyzing your business, searching for target companies, and providing actionable contact strategies — output as a downloadable Markdown (.md) file. Use this skill proactively whenever a user asks to find leads, build a prospect list, identify target accounts, research potential customers or partners, do sales prospecting, or find companies that match an ICP. Also trigger for phrases like "find me companies", "who should I reach out to", "build me a lead list", "who are my ideal customers", or any request to identify potential buyers, clients, or B2B partnerships. Perfect for founders, sales, business development, and marketing professionals.
---

# Lead Research Assistant

This skill identifies and qualifies potential leads for your business by analyzing your product/service, understanding your ideal customer profile, and producing a comprehensive, downloadable Markdown report with actionable outreach strategies.

**Output format**: Always a `.md` file (never docx, csv, or pptx unless the user explicitly requests otherwise).

---

## When to Use This Skill

- Finding potential customers or clients for your product/service
- Building a prospect list of companies to reach out to
- Identifying target accounts for sales outreach
- Researching companies that match your ideal customer profile (ICP)
- Preparing for business development or partnership activities
- Analyzing competitor customer bases for targeting

---

## How to Use

**Basic usage** — describe your product and target:
```
I'm building [product description]. Find me 10 companies in [location/industry] 
that would be good leads.
```

**With codebase context** — run from your product directory:
```
Look at what I'm building in this repository and identify the top 10 companies 
in [location/industry] that would benefit from this product.
```

**Advanced usage** — provide full ICP:
```
My product: [description]
Ideal customer profile:
- Industry: [industry]
- Company size: [size range]
- Location: [location]
- Pain points: [pain points]
- Technologies they use: [tech stack]

Find me 20 qualified leads with contact strategies for each.
```

---

## Instructions for Claude

When a user requests lead research, follow these steps precisely:

### Step 1 — Understand the Product/Service

- If in a code directory, analyze the codebase to understand what the product does
- Ask clarifying questions about the value proposition if not clear
- Identify key features and benefits
- Understand what problems it solves and for whom
- Note any unique differentiators or moats

### Step 2 — Define the Ideal Customer Profile (ICP)

Determine or confirm with the user:
- Target industries and sectors
- Company size ranges (headcount and/or revenue)
- Geographic preferences
- Key pain points the product addresses
- Technology requirements or stack signals
- Growth stage preferences (startup vs. enterprise vs. mid-market)
- Budget signals to look for

### Step 3 — Research and Identify Leads

Use web search to actively find companies. Look for:
- Companies matching the ICP criteria
- Signals of immediate need (job postings, tech stack, recent news/press releases)
- Growth indicators (recent funding rounds, expansion announcements, hiring sprees)
- Companies with complementary products or customer bases
- Budget indicators (public financials, funding, contract announcements)
- Evidence of the problem your product solves (e.g., GitHub repos, open issues, forum discussions)

Cast wide enough to find more candidates than requested, then filter down.

### Step 4 — Prioritize and Score

Create a **fit score (1–10)** for each lead based on:
- Alignment with ICP (industry, size, location)
- Signals of immediate need
- Budget availability and willingness to spend
- Competitive landscape (are they already using a competitor?)
- Timing indicators (recent funding, hiring, product launches)
- Accessibility (can you actually reach a decision-maker?)

Only include leads with a score ≥ 5 in the final output. Briefly note why lower-scoring candidates were excluded if relevant.

### Step 5 — Produce the Output as a Markdown File

Save the output as a `.md` file to `/mnt/user-data/outputs/lead-research-[topic]-[date].md` and present it using `present_files`.

**Use the following structure exactly:**

---

```markdown
# Lead Research Report: [Product/Service Name]
*Generated: [Date]*

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total leads researched | X |
| Leads included (score ≥ 5) | X |
| High priority (8–10) | X |
| Medium priority (5–7) | X |
| Average fit score | X.X / 10 |

**ICP Summary**: [1-2 sentence description of the ideal customer profile used]

**Top Recommendation**: [Single best lead and why in 1 sentence]

---

## Lead [N]: [Company Name]

**Website**: [URL]  
**Industry**: [Industry / Sector]  
**Size**: [Employee count range] | [Revenue range if known]  
**Location**: [HQ location]  
**Funding Stage**: [Bootstrap / Seed / Series A / B / C / Public / Unknown]  
**Priority Score**: [X / 10]  

### Why They're a Good Fit
[3–5 specific, researched reasons tied to this company's actual situation — not generic]

### Fit Score Breakdown
| Factor | Score | Reason |
|--------|-------|--------|
| ICP Alignment | X/10 | [reason] |
| Signals of Need | X/10 | [reason] |
| Budget Availability | X/10 | [reason] |
| Timing | X/10 | [reason] |
| Accessibility | X/10 | [reason] |
| **Overall** | **X/10** | |

### Target Decision Maker
**Role**: [e.g., VP of Engineering, Head of Fraud Prevention, CTO]  
**Why this role**: [1 sentence explaining why this is the right entry point]  
**LinkedIn**: [URL if findable, otherwise note "Search: [name hints]"]

### Value Proposition for This Company
[2–3 sentences — specific to their business, not generic. What problem of theirs does your product solve? What outcome should they expect?]

### Outreach Strategy
[Personalized, researched approach. Reference specific company news, pain points, tech stack, recent hires, or public statements. Suggest channel (LinkedIn DM, cold email, warm intro). Note best timing if applicable.]

### Conversation Starters
- [Specific, researched hook 1 — e.g., "I saw you recently hired 3 ML engineers — are you building internal fraud detection or evaluating external tools?"]
- [Specific hook 2]
- [Specific hook 3]

### Red Flags / Risks
- [Any reasons this lead might not convert — competitor lock-in, budget constraints, org structure, etc.]

---

[Repeat for each lead]

---

## Leads Not Included (Score < 5)

| Company | Score | Reason Excluded |
|---------|-------|-----------------|
| [Company] | X/10 | [brief reason] |

---

## Recommended Next Steps

1. **Prioritize outreach** to leads scored 8–10 first — focus here in the next 7 days
2. **Draft personalized emails** — ask me to write outreach for any specific lead
3. **CRM import** — ask me to convert this list to a CSV for import into HubSpot, Salesforce, or Notion
4. **Deeper research** — ask me to do a full company deep-dive on any top lead
5. **Monitor signals** — set Google Alerts for top companies' names + key trigger terms

---

*Report generated by Lead Research Assistant for [User/Company Name]*
```

---

### Step 6 — Offer Follow-Up Actions

After presenting the file, offer these explicitly:
- Draft personalized outreach emails for any specific lead
- Convert the lead list to a CRM-ready CSV
- Do a deeper company research dive on any top lead (triggers `company-research` skill)
- Refine the ICP and re-run the search with tighter parameters

---

## Examples

### Example 1: B2B SaaS (Data Privacy)

**User**: "I'm building a tool that masks sensitive data in AI coding assistant queries. Find potential leads."

**Output covers**: Companies using Copilot/Cursor/Codeium with sensitive data (fintech, healthcare, legal). Identifies engineering leaders. References GitHub evidence of AI tool usage. Flags compliance-heavy orgs as high-priority.

---

### Example 2: Consulting / Services

**User**: "I run a consulting practice for remote team productivity. Find 10 companies in the Bay Area that recently went remote."

**Output covers**: Companies with recent remote job postings, announced remote-first policies, distributed hiring. Identifies heads of People/HR/Operations. Personalizes conversation starters around specific remote pain signals.

---

### Example 3: Insurance / Fraud Prevention (Stamped-style)

**User**: "Find TPAs and mid-tier insurers in India that are likely to care about image fraud prevention in claims."

**Output covers**: Named Indian TPAs (Medi Assist, Paramount, MDIndia, etc.), IRDAI-regulated insurers, companies with recent fraud-related press. Targets Fraud/Claims/Tech heads. References IRDAI 2025 Fraud Monitoring Framework as context for outreach.

---

## Tips for Best Results

- Be specific about your product and its unique value — generic descriptions produce generic leads
- Provide context about your ICP if you have it already defined
- Specify constraints: industry, location, company size, tech stack
- If your product is technical, mention the underlying problem it solves (not just what it does)
- Request follow-up deep dives on promising leads for full company intelligence reports
