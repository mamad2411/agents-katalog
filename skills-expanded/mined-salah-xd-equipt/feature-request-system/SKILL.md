---
name: feature-request-system
description: "Designs feature request collection and prioritization systems with voting, tagging, and roadmap integration. Use when organizing customer input into product decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Feature Request System

## When to Use This Skill

Use this skill when you need to:
- Design a system for collecting and organizing customer feature requests
- Build a prioritization framework for evaluating requests
- Create a public or internal roadmap connected to user feedback
- Set up voting, tagging, and status workflows for feature management

**DO NOT** use this skill for bug tracking systems, customer support workflows, or product roadmap strategy. This is for the feature request collection and prioritization system specifically.

---

## Core Principle

A FEATURE REQUEST SYSTEM IS NOT A SUGGESTION BOX — IT IS A DECISION-MAKING TOOL THAT CONNECTS CUSTOMER VOICE TO PRODUCT PRIORITIES WITH TRANSPARENCY.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product type** | "What is the product?" | No default — must be provided |
| **Request volume** | "How many feature requests do you receive per month?" | Under 50 |
| **Current process** | "How do you handle feature requests today?" | Email or ad hoc |
| **Public or internal** | "Should customers see and vote on requests, or is this internal only?" | Public voting board |
| **Team size** | "Who reviews and prioritizes requests?" | Solo founder |
| **Existing tools** | "Do you use any project management tools currently?" | None specific |

**GATE: Confirm the brief before designing the system.**

---

## Phase 2: Design the System

### Collection Channels

Define where requests enter the system:

| Channel | Capture Method |
|---------|---------------|
| **In-app widget** | Feedback button → form submission |
| **Email** | Support inbox → tag and forward |
| **Support tickets** | CS team tags feature requests |
| **Social media** | Manual capture into system |
| **Sales calls** | CRM note → feature request tag |
| **Public board** | Direct user submission |

### Request Template

Every request captured with these fields:
- **Title:** Short, descriptive name
- **Description:** What the user wants and why
- **Use case:** The specific scenario driving the request
- **Requester info:** Name, plan tier, account value
- **Category:** Feature area (e.g., billing, reporting, integrations)
- **Priority score:** Calculated (see Phase 3)

### Status Workflow

```
Submitted → Under Review → Planned → In Progress → Shipped → Closed (Won't Do)
```

**GATE: Confirm system design before building the prioritization framework.**

---

## Phase 3: Prioritization Framework

### Scoring Model (RICE)

| Factor | Description | Scale |
|--------|-------------|-------|
| **Reach** | How many users will this affect? | 1-10 (% of user base) |
| **Impact** | How much will it improve their experience? | 1-3 (low/medium/high) |
| **Confidence** | How sure are we this will work? | 50-100% |
| **Effort** | How much work to build? | 1-10 (days/weeks) |

**RICE Score = (Reach x Impact x Confidence) / Effort**

### Decision Matrix

| Score Range | Action |
|-------------|--------|
| 50+ | Prioritize for next cycle |
| 20-49 | Plan for future cycle |
| 10-19 | Monitor for additional votes |
| Under 10 | Acknowledge and defer |

### Voting System Rules

- One vote per user per feature
- Allow users to add context with their vote ("I need this because...")
- Show vote counts publicly to build engagement
- High-value customers (enterprise, high MRR) can be weighted internally

---

## Phase 4: Polish

### 1. Communication Templates

**Request received:**
"Thanks for the suggestion! We have logged your request for [feature]. You can track its status and vote at [link]."

**Status update:**
"Update on your request: [feature] has moved to 'Planned' — we are targeting it for [timeframe]. We will notify you when it ships."

**Request shipped:**
"Great news — [feature] is live! You asked for it, we built it. Try it out: [link]."

**Request declined:**
"We reviewed your request for [feature] and decided not to pursue it at this time. Here is why: [brief reason]. We appreciate the feedback and encourage you to keep sharing ideas."

### 2. Roadmap Integration

- Link feature requests to roadmap items
- Show a public "what we are working on" page with 3 columns: Planned, In Progress, Shipped
- Update the board monthly at minimum
- Celebrate shipped features with "You asked, we built" messaging

### 3. Quality Checklist

```
## Feature Request System Checklist

- [ ] Collection channels defined (in-app, email, support, social)
- [ ] Request template captures title, description, use case, and requester info
- [ ] Status workflow has clear stages (Submitted → Shipped or Closed)
- [ ] Prioritization framework uses a scoring model (RICE or similar)
- [ ] Voting system allows users to support requests
- [ ] Communication templates exist for received, planned, shipped, and declined
- [ ] Public or internal roadmap is connected to the system
- [ ] Monthly review cadence is set for prioritization
- [ ] "Won't Do" requests are communicated with a reason
- [ ] System integrates with existing project management tools
```

---

## Example

**Product:** SaaS project management tool
**Volume:** 30 requests/month

**Public board categories:**
- Integrations (Slack, Zapier, etc.)
- Reporting & Analytics
- Task Management
- Mobile App
- Billing & Account

**Top request card example:**
```
## Dark Mode
Votes: 47 | Status: Planned | Category: UI/UX

"Add a dark mode option for the web app and mobile app."

Top voter comment: "I work late nights and the white interface is blinding. Even a simple dark theme would make a huge difference." — Sarah K., Growth Plan
```

---

## Anti-Patterns

- **Building everything users ask for** — popular requests are not always the right priorities. Use scoring to balance demand with strategy.
- **Black hole feedback** — collecting requests without ever updating status destroys trust. Close the loop.
- **No decline path** — never saying no means an infinite backlog. Have a "Won't Do" status with a reason.
- **Letting vote count alone decide** — a feature with 100 votes from free users may matter less than a request from your top 5 paying customers.
- **Overcomplicating the system** — a spreadsheet beats a complex tool nobody uses. Start simple.

---

## Recovery

- **Overwhelmed by request volume:** Batch-process weekly instead of daily. Group similar requests to reduce duplicates.
- **No votes on the board:** Seed it with known requests from support emails. Announce the board to existing users.
- **Conflicting requests:** Document the tradeoffs. Present both options to a small user group for tiebreaking feedback.
- **User angry about declined request:** Respond personally. Explain the reasoning and suggest a workaround if one exists.
