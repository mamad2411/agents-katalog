---
name: draft-emails-with-placeholders
description: "Draft reusable email templates with clearly marked placeholders for names, dates, amounts, and other missing facts."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["email-templates", "placeholders", "productivity", "workflows", "client-communication", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Draft Emails with Bracketed Placeholders (AI Skill)

## Overview
Asking an AI to draft an email for a specific person often bakes in rigid, hallucinated facts (*"I enjoyed our conversation on Tuesday about the Philadelphia warehouse..."*). 

The **Modular Bracketed Placeholder Pattern** instructs the AI to generate high-conversion email templates using standardized uppercase brackets (e.g. `[CLIENT_NAME]`, `[METRIC]`, `[DATE]`). This prevents factual slip-ups and creates a permanent, reusable template you can deploy across dozens of clients in seconds.

---

## The Modular Email Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Modular Email Blueprint                     │
│                                                             │
│  [ SUBJECT ]: Compelling, specific hook with `[TOPIC]`      │
│                                                             │
│  [ SECTION 1: Context Hook ] ──► `[RECENT_EVENT]` reference │
│                                                             │
│  [ SECTION 2: Core Value ]   ──► `[METRIC / DELIVERABLE]`   │
│                                                             │
│  [ SECTION 3: Frictionless CTA]──► Exact `[DAY / TIME]` slot│
└─────────────────────────────────────────────────────────────┘
```

---

## Master Placeholder Prompt Templates

### Pattern 1: The Reusable Outreach & Follow-Up Engine

```markdown
Draft a reusable email template for [SCENARIO: e.g. Following up after an initial discovery call].

Requirements:
1. Use clear, uppercase bracketed placeholders for all dynamic variables (e.g. `[FIRST_NAME]`, `[COMPANY]`, `[PAIN_POINT]`, `[PROPOSED_DATE]`).
2. Tone: Warm, executive, and direct (under 120 words).
3. Do not invent fake client names or specific numbers.
4. Conclude with a low-friction, single-question Call to Action (CTA).
```

---

### Pattern 2: The Multi-Stage Drip Funnel Generator

```markdown
Create a 3-part email follow-up sequence for [SCENARIO: e.g. Overdue Invoice Collection].
- Email 1 (Day 1 Past Due): Friendly reminder with `[INVOICE_NUMBER]` and `[AMOUNT]`.
- Email 2 (Day 7 Past Due): Firm check-in with `[PAYMENT_LINK]`.
- Email 3 (Day 14 Past Due): Formal notice referencing `[CONTRACT_CLAUSE]` and service pause.
```

---

## Real-World Case Study

### Scenario: Client Follow-Up on Pending Contract Signature

#### Weak One-Off Prompt
> *"Write an email asking Bob to sign the contract."*
> ❌ *Result: A hyper-specific, one-time message that cannot be reused for other clients.*

#### Reusable Bracketed Template Output

> **Subject**: Next steps for `[PROJECT_NAME]` kick-off
> 
> Hi `[FIRST_NAME]`,
> 
> I hope you're having a great week.
> 
> We have our engineering team penciled in to start `[PROJECT_NAME]` on `[TARGET_START_DATE]`. 
> 
> To ensure we hit that milestone without delay, we just need the signed agreement by `[DEADLINE_DATE]`:
> 👉 **Review & Sign Agreement**: `[DOCUSIGN_LINK]`
> 
> If you have any questions or need a quick adjustment to `[SPECIFIC_TERM]`, let me know and I'll take care of it right away.
> 
> Best regards,  
> `[YOUR_NAME]`

---

## Top 5 Essential Bracket Tokens

| Token | Purpose | Example |
| :--- | :--- | :--- |
| `[FIRST_NAME]` | Recipient greeting anchor | *"Hi Sarah,"* |
| `[SPECIFIC_PAIN_POINT]` | Proves personalization | *"reducing your checkout churn"* |
| `[QUANTIFIED_BENEFIT]` | Concrete value prop | *"cut onboarding time by 35%"* |
| `[TIME_WINDOW]` | Low-friction scheduling | *"Thursday at 2 PM EST"* |
| `[ACTION_LINK]` | Direct one-click destination | `[CALENDAR_LINK]` |
