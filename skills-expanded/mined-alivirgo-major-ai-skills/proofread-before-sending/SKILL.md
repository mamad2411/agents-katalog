---
name: proofread-before-sending
description: "Review a message for clarity, mistakes, tone, and unintended implications before sending it."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["tone-auditing", "emotional-intelligence", "communication", "email-proofreading", "subtext", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Proofread Tone & Subtext Before Sending (AI Skill)

## Overview
Because digital messages lack body language, facial cues, and vocal inflections, text is naturally subject to the **Negative Escalation Bias**: recipients consistently interpret neutral or rushed emails as cold, defensive, or hostile.

The **Tone & Perception Pre-Send Audit Protocol** uses AI to simulate how a recipient will emotionally perceive your draft, spotting hidden passive-aggression, defensive justification, or overly timid phrasing before you hit send.

---

## The 4 Perception Filters

```
┌─────────────────────────────────────────────────────────────┐
│                 The 4 Perception Filters                    │
│                                                             │
│  1. DEFENSIVENESS       ──► "As I stated in my last email..."│
│                             (Sounds petty & argumentative)  │
│  2. WEAK APOLOGIES      ──► "Sorry to bother you again..."  │
│                             (Undermines your authority)     │
│  3. PASSIVE-AGGRESSION  ──► "Per our previous discussion..." │
│                             (Creates interpersonal friction)│
│  4. AMBIGUOUS BOUNDARIES──► "Maybe we can look at this soon"│
│                             (Creates dropped deadlines)     │
└─────────────────────────────────────────────────────────────┘
```

---

## Master Tone-Audit Prompt Templates

### Pattern 1: The Emotional Subtext & Perception Audit
Use before sending high-stakes emails to clients, executives, or team members:

```markdown
Here is an email draft I wrote:
[PASTE DRAFT]

Context:
- Recipient: [e.g. An important client / My CEO / A frustrated customer]
- My Intent: [e.g. Set a firm boundary on scope without damaging the relationship]

Act as an Executive Communications Coach and audit this draft:
1. **Perception Rating**: How will this read to the recipient? (Rate: Warm / Neutral / Defensive / Hostile).
2. **Hidden Friction Points**: Identify any specific sentences that sound subtly passive-aggressive, condescending, or insecure.
3. **The Polished Version**: Provide a revised draft that is firm, respectful, and crystal-clear (under 100 words).
```

---

### Pattern 2: The "De-Escalation & Conflict Resolver"
Use when replying to an accusatory or angry email:

```markdown
Here is an angry email from a client: [PASTE CLIENT EMAIL]
Here is my initial emotional response: [PASTE YOUR RAW DRAFT]

Task:
- Strip all emotional defensiveness and counter-blame from my response.
- Acknowledge their frustration without admitting false liability.
- Focus strictly on the concrete resolution steps.
```

---

## Real-World Case Study

### Scenario: Setting Boundaries on Scope Creep

#### Raw Human Draft (Subtly Defensive)
> *"Hi John, as I already mentioned on Tuesday, that feature is completely out of the original scope we agreed on. We can't keep adding extra requests for free. If you want this, you'll have to pay an extra $3,000 and the launch will be delayed."*
> 
> ❌ *Perception: Hostile, confrontational, leaves the client feeling scolded.*

#### Tone-Audited & Polished Output
> **AI Perception Analysis**: *"The phrase 'as I already mentioned' and 'pay extra for free' reads as accusatory and creates immediate conflict."*
> 
> **Revised Version (Firm, Professional, Collaborative)**:
> *"Hi John,*
> 
> *That new feature is a great addition for v2. Because our current sprint is focused 100% on hitting our scheduled October 15th launch date, adding it now would push our timeline back by 2 weeks.*
> 
> *We have two options:*
> 1. *Keep our current Oct 15 launch on schedule, and add this feature in Sprint 2.*
> 2. *Expand the scope now with a $3,000 add-on and move launch to Oct 30.*
> 
> *Which direction works best for your team?"*

---

## Summary Best Practices
- **Never send an email written in anger**: Paste the angry draft into AI with the prompt: *"Strip the anger and leave only the boundaries and action steps."*
- **Eliminate "As per my last email"**: Replace with clear, fresh reiteration.
- **Convert friction into choices**: Don't say *"No"*; offer two clear options with their respective trade-offs.
