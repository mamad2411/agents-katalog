---
name: support-response-templates
description: "Writes customer support response templates for common scenarios with tone guidelines, personalization cues, and escalation triggers."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Support Response Templates

## When to Use This Skill

Use this skill when you need to:
- Create templated responses for common customer support scenarios
- Standardize tone and quality across support interactions
- Build an escalation framework with clear trigger criteria
- Save time on repetitive support replies without sounding robotic

**DO NOT** use this skill for help center articles (use help-center-article), chatbot scripts, or complaint resolution frameworks. This is for human-sent support message templates.

---

## Core Principle

SUPPORT TEMPLATES SAVE TIME ON THE STRUCTURE SO YOU CAN SPEND TIME ON THE PERSONALIZATION — A GOOD TEMPLATE IS 70% REUSABLE AND 30% CUSTOMIZED TO THE SPECIFIC CUSTOMER.

---

## Phase 1: Scenario Audit

Identify the most common support scenarios.

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business type** | "What product or service do you support?" | No default |
| **Support channels** | "Where do customers contact you? (email, chat, social, phone)" | Email |
| **Top 10 questions** | "What are the 10 most common support requests you receive?" | No default |
| **Current templates** | "Do you have any existing templates or canned responses?" | None |
| **Tone** | "How should support replies feel? (formal, friendly, casual)" | Friendly and professional |
| **Response time goal** | "What is your target response time?" | Under 4 hours |

### Scenario Categorization

```
## Support Scenario Map

| Category | Scenario | Frequency | Complexity | Template Priority |
|----------|----------|-----------|-----------|------------------|
| Pre-sale | Pricing question | High | Low | HIGH |
| Onboarding | Setup help | High | Medium | HIGH |
| Technical | Feature not working | Medium | High | HIGH |
| Billing | Refund request | Medium | Medium | HIGH |
| General | Status check | High | Low | MEDIUM |
```

**GATE: Confirm scenario list before writing templates.**

---

## Phase 2: Write Templates

Create response templates for each priority scenario.

### Template Format

Every template follows this structure:

```
## Template: [Scenario Name]

**Use when:** [Specific trigger for using this template]
**Tone:** [Empathetic / Informative / Celebratory / Apologetic]
**Personalize:** [What to customize before sending — marked with [brackets]]

---

Subject: [Subject line]

Hi [Name],

[Body — with [personalization markers] for customization]

[Closing + next step]

[Signature]

---

**Escalation trigger:** [When NOT to use this template and escalate instead]
```

### Common Template Library

**Acknowledgment / We Are On It:**
```
Subject: Got your message — here is what happens next

Hi [Name],

Thanks for reaching out. I have received your [question/request about specific topic] and I am looking into it now.

You can expect a full response within [timeframe].

If anything changes or you have additional details to add, just reply to this email.

[Name]
```

**How-To / Instructional:**
```
Subject: Here is how to [action]

Hi [Name],

Great question! Here is how to [action]:

1. [Step 1]
2. [Step 2]
3. [Step 3]

[Screenshot or link if applicable]

If you run into any issues with these steps, let me know and I will walk you through it.

[Name]
```

**Refund/Billing Issue:**
```
Subject: Your refund has been processed

Hi [Name],

I have processed your refund of $[amount]. You should see it in your account within [3-5 business days].

[If applicable: Here is what happened and what we have done to prevent it.]

I am sorry for the inconvenience. If there is anything else I can help with, I am here.

[Name]
```

**Apology / Something Went Wrong:**
```
Subject: We dropped the ball — here is how we are fixing it

Hi [Name],

You are right — [acknowledge the specific issue]. That is not the experience you should have, and I am sorry.

Here is what I have done:
- [Action 1 — immediate fix]
- [Action 2 — prevention measure]

[Compensation if applicable: As a gesture, I have [credit/discount/extension].]

If there is anything else I can do, please let me know directly.

[Name]
```

**Positive Outcome / Celebration:**
```
Subject: Great news about your [request/issue]

Hi [Name],

Good news — [positive outcome].

[Details of what was done]

Is there anything else you need? Happy to help.

[Name]
```

**GATE: Present template library for review and customization.**

---

## Phase 3: Tone Guide

Define the voice and guardrails for all support communication.

### Tone Guidelines

```
## Support Tone Guide

**Always:**
- Use the customer's name
- Acknowledge their issue before solving it
- Be specific about timelines ("within 24 hours" not "soon")
- End with a clear next step or offer of further help

**Never:**
- Use passive voice for responsibility ("mistakes were made")
- Blame the customer ("you should have...")
- Use jargon the customer may not understand
- Send a template without personalizing the [bracketed] fields

**Escalation language:**
- "I am bringing in [Name/Role] who specializes in this" (not "I cannot help you")
- "Let me make sure the right person handles this for you" (not "That is not my department")
```

### Escalation Matrix

```
| Trigger | Escalate To | Timeframe |
|---------|------------|-----------|
| Customer mentions legal action | [Owner/Legal] | Immediately |
| Issue unresolved after 2 responses | [Senior support] | Same day |
| Refund over $[amount] | [Owner/Finance] | Same day |
| Customer threatening public review | [Owner] | Within 1 hour |
| Technical issue beyond support scope | [Technical lead] | Within 4 hours |
```

---

## Phase 4: Maintain

Keep templates current and effective.

### Template Review Schedule

- **Monthly:** Review templates for any that need updating (product changes, policy changes)
- **Quarterly:** Analyze which templates are used most and refine them
- **After any product change:** Update affected templates immediately

### Performance Tracking

```
| Metric | Target | Current |
|--------|--------|---------|
| Average response time | Under [X] hours | — |
| First-contact resolution rate | 70%+ | — |
| Customer satisfaction after support | 4.5+/5 | — |
| Template usage rate | 60%+ of responses | — |
```

---

## Anti-Patterns

- **Sending templates without personalization** — a clearly canned response feels worse than a slow personal one. Always customize.
- **Template for every edge case** — write templates for the top 80% of scenarios. Handle edge cases personally.
- **No empathy before solution** — jumping to the fix without acknowledging the frustration feels dismissive.
- **Vague timelines** — "We will get back to you soon" creates anxiety. "Within 24 hours" creates trust.
- **Same template for different severity levels** — a billing error and a data breach require very different tones.

---

## Recovery

- **Customer responds angrily to a template:** Apologize, acknowledge it felt impersonal, and respond with a fully custom message.
- **Templates are not being used:** They may be too hard to find or too rigid. Organize by scenario and encourage customization.
- **Response times are still slow despite templates:** The bottleneck may be decision-making, not writing. Pre-approve responses for common scenarios.
- **User handles all support alone:** Prioritize the 5 most common scenarios. Even 5 good templates save significant time.
- **Customer's issue does not fit any template:** Write a custom response. Log the scenario — if it happens 3+ times, create a new template.
