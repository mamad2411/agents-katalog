---
name: platform-help-center
description: "Structures platform help centers with separate buyer/seller sections, video tutorials, and contact escalation. Use when building self-serve support for marketplace platforms."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Platform Help Center

## When to Use This Skill

Use this skill when you need to:
- Structure a help center for a marketplace with buyer and seller audiences
- Write help articles that reduce support ticket volume
- Design a contact escalation path from self-serve to human support
- Organize FAQs, tutorials, and troubleshooting guides by user type

**DO NOT** use this skill for knowledge base software selection, chatbot design, or internal documentation. This is for external-facing help center structure and content.

---

## Core Principle

A HELP CENTER EXISTS TO ANSWER QUESTIONS BEFORE THEY BECOME SUPPORT TICKETS — EVERY ARTICLE MUST BE FINDABLE IN UNDER 30 SECONDS AND ANSWERABLE IN UNDER 2 MINUTES.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Platform type** | "What does your marketplace connect?" | No default — must be provided |
| **Top support questions** | "What are the 10 most common questions from buyers and sellers?" | No default — must be provided |
| **Current support volume** | "How many support tickets per week?" | Under 50 |
| **Support channels** | "How do users currently reach support? Email, chat, phone?" | Email only |
| **Help center tool** | "What platform will host the help center?" | Notion, Zendesk, or standalone page |

**GATE: Confirm the brief before structuring the help center.**

---

## Phase 2: Structure

### Information Architecture

```
Help Center Home
├── For Buyers
│   ├── Getting Started
│   ├── Browsing and Searching
│   ├── Placing an Order
│   ├── Payments and Refunds
│   ├── Reviews and Ratings
│   └── Account and Settings
├── For Sellers
│   ├── Getting Started
│   ├── Creating Listings
│   ├── Managing Orders
│   ├── Payments and Payouts
│   ├── Reviews and Ratings
│   └── Account and Settings
├── Trust and Safety
│   ├── Our Guarantee
│   ├── Reporting a Problem
│   ├── Dispute Resolution
│   └── Community Guidelines
└── Contact Us
    ├── Submit a Request
    └── Live Chat (if available)
```

### Article Priority Matrix

Rank articles by impact:

| Priority | Criteria | Action |
|----------|----------|--------|
| P1 | Top 10 questions by ticket volume | Write first |
| P2 | Onboarding and activation questions | Write second |
| P3 | Edge cases and advanced topics | Write third |
| P4 | Nice-to-have reference content | Write as needed |

**GATE: Confirm the structure and priority list before writing articles.**

---

## Phase 3: Write

### Article Template

```
## [Article Title — phrased as a question]

**Applies to:** Buyers / Sellers / Both

[1-2 sentence answer to the question — the TL;DR.]

### Step-by-step

1. [Step with specific UI reference]
2. [Step with specific UI reference]
3. [Step with specific UI reference]

### Screenshot
[SCREENSHOT: description of what to capture]

### Common Issues
- **[Problem]:** [Solution]
- **[Problem]:** [Solution]

### Still need help?
[Contact our support team →](link)
```

### Writing Rules

- **Title is a question** — match how users think and search ("How do I get a refund?" not "Refund Policy")
- **Answer first, details second** — the first 1-2 sentences should answer the question directly
- **Step-by-step format** — use numbered lists for processes, bullets for options
- **Specific UI references** — "Click the gear icon in the top right" not "Go to settings"
- **Screenshots for every process** — placeholder notes if screenshots are not ready: `[SCREENSHOT: settings page with gear icon circled]`
- **Link to related articles** — at the bottom, suggest 2-3 related articles

### Content Types

| Type | When to Use | Format |
|------|-------------|--------|
| **How-to article** | Process questions | Numbered steps + screenshots |
| **Troubleshooting guide** | "It is not working" questions | Problem → possible causes → solutions |
| **FAQ entry** | Quick factual answers | Question + 1-3 sentence answer |
| **Video tutorial** | Complex multi-step processes | 60-120 second screencast |

---

## Phase 4: Polish

### 1. Contact Escalation Path

```
User has a question
    ↓
Search help center (self-serve)
    ↓
No answer found → Suggest related articles
    ↓
Still no answer → Contact form with category selection
    ↓
Ticket created → Auto-response with estimated reply time
    ↓
Human support responds within [X] hours
```

### 2. Help Center Metrics

```
## Help Center Metrics

- **Search success rate:** % of searches that result in an article click
- **Contact rate:** % of help center visitors who submit a ticket (lower = better)
- **Top searches with no results:** Keywords users search for that return nothing
- **Article helpfulness:** "Was this helpful?" yes/no at the bottom of each article
- **Ticket deflection rate:** % reduction in tickets after article publication
- **Time to resolution:** Average time to resolve tickets that escalate beyond self-serve
```

### 3. Quality Checklist

```
## Help Center Checklist

- [ ] Separate buyer and seller sections with clear navigation
- [ ] Top 10 questions (by ticket volume) have dedicated articles
- [ ] Every article title is phrased as a question
- [ ] Every article answers the question in the first 2 sentences
- [ ] Step-by-step articles include screenshots (or placeholders)
- [ ] Contact escalation path is clear and accessible
- [ ] Search functionality works across all articles
- [ ] "Was this helpful?" feedback is on every article
- [ ] Related articles linked at the bottom of each page
- [ ] Help center link is accessible from every page of the platform
```

---

## Example

**Platform:** Freelance services marketplace

**Buyer article:**
```
## How do I get a refund?

You can request a refund if the work delivered does not match what was agreed upon in your project brief.

### Steps to request a refund

1. Go to **My Orders** in your dashboard
2. Click on the order in question
3. Click **Request Refund** (available for 14 days after delivery)
4. Select your reason and add details
5. Click **Submit** — the seller has 48 hours to respond

### What happens next
- If the seller agrees, your refund is processed within 3-5 business days
- If the seller disagrees, our team reviews the case and decides within 5 business days

### Still need help?
[Contact support →](link) | Related: [How does buyer protection work?](link)
```

---

## Anti-Patterns

- **Single help center for both sides** — buyers and sellers have different questions and different vocabulary. Separate the sections.
- **Long articles** — if an article takes more than 2 minutes to read, split it into multiple articles.
- **No search function** — if users cannot search, they will email support instead. Search is mandatory.
- **Hiding the contact option** — self-serve is the goal, but hiding human support frustrates users who genuinely need it.
- **Stale content** — outdated screenshots and processes create more confusion than no article at all. Review quarterly.

---

## Recovery

- **No data on common questions:** Review the last 50 support emails. Group by topic. The top 10 topics are your first articles.
- **Too many articles needed at once:** Start with the top 5 questions for each side (10 total). Add 2-3 per week.
- **Users still contact support for questions that have articles:** The articles are hard to find or hard to understand. Improve search and rewrite using simpler language.
- **Help center gets no traffic:** Link to it from transactional emails, in-app tooltips, and the support auto-reply. Make it visible everywhere.
