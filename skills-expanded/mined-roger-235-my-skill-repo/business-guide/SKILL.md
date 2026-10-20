---
name: business-guide
description: "Routes business and management requests to the appropriate skill. Covers C-suite advisory, marketing, product management, finance, compliance, project management, and business growth."
metadata:
  category: business
  version: "1.0"
---

## Purpose
Route business and management queries to the correct specialist skill.

## Trigger

Apply when user asks about:
- "business strategy", "company strategy", "startup advice", "founder decisions"
- "marketing campaign", "SEO", "content strategy", "go-to-market"
- "financial model", "fundraising", "investor deck", "SaaS metrics"
- "product roadmap", "product strategy", "PRD", "user research"
- "compliance", "GDPR", "ISO audit", "regulatory affairs"
- "project management", "Jira", "sprint planning", "portfolio management"
- "revenue operations", "sales strategy", "customer success"

Do NOT trigger for:
- Software development tasks — use `dev-guide`
- Data analysis or modeling — use `data-guide`
- General writing or editing — use `writing-guide`

## Prerequisites
- None

## Steps

1. **Identify the business domain** — determine which of the 7 subcategories (C-Suite, Marketing, Product, Finance, Compliance, Project Management, Growth) best matches the request
2. **Match to Routing Table** — find the most specific skill in the matching subcategory
3. **Recommend the skill** — name the skill and explain in one sentence why it fits; if the goal spans multiple skills, show the full chain from `## Skill Chains`

## Output Format

File path: none (routing recommendation printed to user)

```
## Recommended: <subcategory>/<skill-name>

**Why:** <one sentence matching the request to the skill's purpose>

**Next step:** Run `/<skill-name>` or ask Claude to apply it.

*(Optional)* **Chain:** `skill-a` → `skill-b` → `skill-c`
```

## Routing Table

7 subcategories (C-Suite 28, Marketing 43, Product 13, Finance 2, Compliance 12, Project Management 6, Growth 4): [ref/routing-table.md](ref/routing-table.md)

## Skill Chains
- Business launch: `product/product-discovery` → `product/product-strategist` → `marketing/launch-strategy` → `marketing/content-strategy`
- Fundraising: `c-suite/ceo-advisor` → `c-suite/board-deck-builder` → `finance/financial-analyst`
- Compliance program: `compliance/risk-management-specialist` → appropriate ISO/FDA skill → `compliance/quality-documentation-manager`
- Marketing funnel: `marketing/marketing-strategy-pmm` → `marketing/content-strategy` → `marketing/paid-ads` → `marketing/page-cro`

## Rules
### Must
- Route to the most specific skill available
- Explain what the routed skill does before invoking it
- Suggest skill chains when the request spans multiple domains

### Never
- Perform work directly — always route
- Invoke multiple specialist skills simultaneously without user confirmation

## Examples

### Good Example

User: "Help me prepare for my board meeting"

```
## Recommended: c-suite/board-deck-builder

**Why:** Structures board updates with financial summary, OKR status, and key decisions in investor-ready deck format.

**Next step:** Run `/board-deck-builder` or ask Claude to apply it.
```

### Bad Example

User: "Help me with marketing"

Claude immediately starts writing ad copy and social posts without asking what type of marketing help is needed or routing to the appropriate skill.

> Why this is bad: "Marketing" spans 43+ skills (SEO, paid ads, copy, strategy, CRO, analytics). Starting to produce content without routing skips domain triage, uses the wrong skill for the job, and ignores the Routing Table entirely.
