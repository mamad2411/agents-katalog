---
name: tech-stack-recommendation
description: "Recommends tech stacks for specific business types with tool selection rationale, costs, and implementation order. Use when building your business software foundation."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Tech Stack Recommendation

## When to Use This Skill

Use this skill when you need to:
- Select a complete technology stack for a new business or project
- Recommend tools across multiple business functions (communication, finance, marketing, etc.)
- Design a phased implementation plan for adopting multiple tools
- Balance cost, capability, and simplicity for a solopreneur or small team

**DO NOT** use this skill for evaluating a single tool (use saas-evaluation), auditing an existing stack (use tool-stack-audit), or enterprise IT architecture. This is for small business tech stack design.

---

## Core Principle

THE BEST TECH STACK IS THE SMALLEST ONE THAT COVERS YOUR NEEDS — EVERY ADDITIONAL TOOL ADDS COST, COMPLEXITY, AND MAINTENANCE. START WITH THE ESSENTIALS AND ADD ONLY WHEN A REAL PROBLEM DEMANDS IT.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What kind of business? Service, product, SaaS, e-commerce, content?" | No default — must be provided |
| **Business stage** | "Pre-launch, launched, or scaling?" | Launched, under $100K revenue |
| **Team size** | "How many people need to use these tools?" | Solo (1 person) |
| **Monthly budget** | "What is your total budget for all software tools?" | Under $200/month |
| **Current tools** | "What tools do you already use and want to keep?" | Google Workspace or none |
| **Priority needs** | "What business functions need tools most urgently?" | No default — rank top 3 |

**GATE: Confirm the brief before designing the stack.**

---

## Phase 2: Map Business Functions

### Function Inventory

For the business type, identify which functions need tools:

| Function | Priority | Status |
|----------|----------|--------|
| **Communication** (email, messaging) | Essential | |
| **Website** (hosting, CMS) | Essential | |
| **Finance** (invoicing, bookkeeping, banking) | Essential | |
| **CRM / Contacts** | High | |
| **Project Management** | High | |
| **Marketing** (email, social, ads) | High | |
| **Content Creation** (design, writing, video) | Medium | |
| **Analytics** (web, business) | Medium | |
| **File Storage** (documents, assets) | Medium | |
| **Scheduling** (calendar, appointments) | Medium | |
| **Legal** (contracts, compliance) | Low | |
| **AI Tools** (writing, automation, research) | Medium | |

Mark each as: Needed Now / Needed Soon / Not Yet / Not Applicable

**GATE: Confirm which functions to address before recommending tools.**

---

## Phase 3: Recommend

### Stack Recommendation Format

For each function, recommend one primary tool:

```
## Recommended Tech Stack

### Communication
**Tool:** [Name] — $[X]/month
**Why:** [One sentence rationale]
**Alternative:** [Runner-up if budget or needs differ]

### Website
**Tool:** [Name] — $[X]/month
**Why:** [One sentence rationale]
**Alternative:** [Runner-up]

[Repeat for each function...]
```

### Stack Archetypes

**The Bootstrap Stack (under $50/month):**
- Google Workspace ($7/month) — email, docs, storage
- Carrd or WordPress ($0-12/month) — website
- Wave or Stripe ($0) — invoicing and payments
- Notion ($0-10/month) — CRM, project management, docs
- Canva Free ($0) — design
- Mailchimp Free ($0) — email marketing
- Claude Free ($0) — AI writing and research

**The Growth Stack ($100-200/month):**
- Google Workspace ($14/month) — email, storage
- WordPress + hosting ($20-30/month) — website
- QuickBooks ($30/month) — accounting
- Notion or ClickUp ($10-15/month) — project management
- ConvertKit ($29/month) — email marketing
- Canva Pro ($13/month) — design
- Claude Pro ($20/month) — AI
- Calendly ($0-8/month) — scheduling
- Zapier ($20/month) — automation

### Cost Summary

```
## Monthly Cost Summary

| Function | Tool | Cost |
|----------|------|------|
| Communication | [Tool] | $[X] |
| Website | [Tool] | $[X] |
| Finance | [Tool] | $[X] |
| CRM / PM | [Tool] | $[X] |
| Marketing | [Tool] | $[X] |
| Design | [Tool] | $[X] |
| AI | [Tool] | $[X] |
| **Total** | | **$[X]/month** |
| **Annual** | | **$[X]/year** |
```

---

## Phase 4: Polish

### 1. Implementation Order

Sequence tool adoption to avoid overwhelm:

| Phase | Timeline | Tools to Set Up | Why First |
|-------|----------|----------------|-----------|
| Week 1 | Essential | Email, website, invoicing | Revenue-enabling |
| Week 2 | Operations | Project management, file storage | Workflow foundation |
| Week 3 | Growth | Email marketing, CRM | Customer relationships |
| Week 4 | Optimization | Design, AI, automation | Efficiency gains |

### 2. Integration Map

Show how recommended tools connect:

```
[Website] → leads → [Email Marketing] → nurtures → [CRM]
[CRM] → projects → [Project Management] → invoices → [Finance]
[Automation] connects [all tools] via triggers and actions
```

### 3. Quality Checklist

```
## Tech Stack Checklist

- [ ] All priority business functions have a recommended tool
- [ ] Each tool has a clear rationale (not just "it is popular")
- [ ] Total monthly cost is within budget
- [ ] Alternatives provided for key tools (in case of preference)
- [ ] Implementation is phased over 4 weeks (not all at once)
- [ ] Integration points between tools are identified
- [ ] Free tiers and trials are leveraged where possible
- [ ] Stack avoids redundancy (no two tools for the same job)
- [ ] Data portability checked (can you export and leave each tool?)
- [ ] Annual cost calculated for budget planning
```

---

## Example

**Business:** Freelance copywriter, just launched, $100/month budget

```
## Recommended Stack — $87/month

| Function | Tool | Cost |
|----------|------|------|
| Email + Docs | Google Workspace | $7 |
| Website | Carrd | $9 |
| Invoicing | Stripe Invoicing | $0 (per-transaction fees) |
| CRM + PM | Notion | $10 |
| Email Marketing | MailerLite | $0 (free up to 1K subscribers) |
| Design | Canva Pro | $13 |
| AI Writing | Claude Pro | $20 |
| Scheduling | Calendly | $0 (free tier) |
| Contracts | HelloSign | $15 |
| Automation | Zapier | $20 |
| **Total** | | **$94/month** |
```

**Implementation order:** Week 1: Google Workspace, Carrd, Stripe. Week 2: Notion, Calendly. Week 3: MailerLite, HelloSign. Week 4: Canva, Claude, Zapier.

---

## Anti-Patterns

- **Enterprise tools for solo businesses** — Salesforce for a one-person business is like using a firehose to water a houseplant.
- **Adopting everything at once** — setup fatigue is real. Phase the implementation over 4 weeks minimum.
- **Choosing tools your friends use** — tool selection should match YOUR business needs, not someone else's.
- **Ignoring free tiers** — many tools offer generous free plans. Use them until you outgrow them.
- **Building instead of buying** — unless your business IS software, buy the tool. Your time is better spent on clients and revenue.

---

## Recovery

- **Budget too tight for recommendations:** Start with free tiers only. Google Workspace, Notion Free, Canva Free, and Mailchimp Free cover 80% of needs at $0.
- **User is overwhelmed by options:** Pick ONE archetype (Bootstrap or Growth) and implement it as-is. Customize later.
- **A recommended tool does not fit after trying it:** Swap with the alternative. Most tools in the same category are interchangeable.
- **User already has tools they want to keep:** Build the stack around their keepers. Fill gaps only.
