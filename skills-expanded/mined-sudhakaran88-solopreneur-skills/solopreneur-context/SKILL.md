---
name: solopreneur-context
description: When the user wants to set up or update their solopreneur context document — a one-time profile of their business that all other skills reference automatically. Use when the user says "set up my context," "tell you about my business," "save my business info," "update my profile," or when starting a new session and other skills ask for context. Stores info as .agents/solopreneur-context.md. Built for solo founders, solopreneurs, and one-person businesses.
metadata:
  version: 1.0.0
  author: Sudhakar
  license: MIT
---

# Solopreneur Context Setup

You are helping a solopreneur or solo founder build their business context document. This is a one-time setup that gets saved to `.agents/solopreneur-context.md` — once created, every other skill in this collection reads it automatically, so they never have to repeat the same information.

Think of it as your AI's briefing document. Build it once, benefit every time.

## If Context Already Exists

First check if `.agents/solopreneur-context.md` already exists. If it does:
- Show the user what's currently saved
- Ask: "Want to update anything, or does this look good?"
- Only overwrite if they confirm changes

## Gather the Business Profile

Walk through this questionnaire. Keep it conversational — don't dump all questions at once. Group them naturally.

### Group 1: The Basics
1. **Business name** — what's the company called?
2. **What do you do?** — one sentence: "I [verb] for [customer type]"
3. **How do you make money?** — services, products, SaaS, agency, freelance, digital products?
4. **Location** — where are you based? Do you serve local, national, or global clients?

### Group 2: Your Customer
5. **Who is your ideal customer?** — be specific: "SaaS founders with 1-10 employees raising Series A" beats "small businesses"
6. **What problem do you solve for them?**
7. **What outcome do they get?** — be concrete: "launch in 6 weeks" beats "better website"

### Group 3: Your Business Stage
8. **Revenue stage** — just started, £1-10K MRR, £10-50K MRR, £50K+ MRR?
9. **Solo or small team?** — just you, VA, subcontractors?
10. **Biggest growth challenge right now?** — finding clients, converting leads, building product, content, time?

### Group 4: Marketing & Sales
11. **How do you currently get clients?** — referrals, LinkedIn, SEO, paid ads, cold outreach?
12. **Main offer** — what's your flagship product or service and its price?
13. **Website URL** — if you have one

### Group 5: Tools & Workflows
14. **Key tools you use** — CRM, email platform, project management, communication?
15. **Anything you're actively building or launching?**

---

## Output: The Context Document

Write the answers to `.agents/solopreneur-context.md` in this format:

```markdown
# Solopreneur Context
*Last updated: [date]*

## Business Overview
- **Name:** [business name]
- **Type:** [agency / SaaS / freelance / product / etc.]
- **What we do:** [one sentence]
- **Location:** [city/country + geographic reach]
- **Website:** [URL]

## Ideal Customer Profile (ICP)
- **Who:** [specific description]
- **Problem they have:** [specific pain point]
- **Outcome we deliver:** [specific result]
- **Typical deal value:** [if known]

## Business Stage
- **Revenue:** [stage or approximate MRR/ARR]
- **Team:** [solo / VA / contractors]
- **Growth focus:** [what matters most right now]

## Current Marketing
- **How clients find us:** [channels]
- **Content platforms:** [blog / LinkedIn / Twitter / etc.]
- **Primary offer:** [name, description, price]

## Tools
- **CRM:** [tool name or none]
- **Email:** [platform]
- **Project management:** [tool]
- **Other key tools:** [list]

## Active Priorities
- [Thing 1 being worked on now]
- [Thing 2]
- [Thing 3]

## Business Context Notes
[Any additional context that would help AI tools give better advice]
```

---

After saving, confirm to the user:

> "Your context is saved to `.agents/solopreneur-context.md`. Every skill in this collection will now read this automatically — no need to repeat your business details. You can update it any time by saying 'update my context.'"

---

## Related Skills

- `product-marketing-context` — the marketing-specific version of this context (for more detailed positioning work)
- All skills in this collection read this context automatically

*Generated using the solopreneur-context skill from Solopreneur Skills*
