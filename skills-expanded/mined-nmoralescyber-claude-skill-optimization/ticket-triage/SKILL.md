---
name: ticket-triage
description: Triages and prioritizes an inbound support ticket — assigns category, P1-P4 priority, product area, routing recommendation, and a suggested initial response. Use when a NEW ticket or customer message arrives and has not yet been classified, when deciding which team should own it, or when checking whether it is a duplicate or known issue. Defers to customer-support:customer-research when the ticket cannot be priority-assigned without investigation first, customer-support:customer-escalation when the ticket is already known to need engineering or leadership packaging (skip triage and go straight to escalation), customer-support:draft-response when the ticket is already triaged and the user just wants the reply written, legal:legal-response for SOC 2 evidence requests / security questionnaires with contractual reps / DSARs / subpoenas, sales:draft-outreach when the message is from a non-customer prospect. The defining characteristic is "a fresh inbound that needs categorization, prioritization, and routing decisions before anyone touches it."
argument-hint: "<ticket text, customer message, or issue description>"
---

# Ticket Triage

Categorizes, prioritizes, and routes an incoming support ticket. Built for a cybersecurity product where security-incident reports get extra-strict priority and routing rules.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| A fresh ticket needs category + priority + routing | Ticket is already triaged and you just need the reply -> `customer-support:draft-response` |
| You can decide priority from the ticket text + quick context | You need investigation across CRM/Slack/docs before you can even classify -> `customer-support:customer-research` first, then return here |
| Routing might land on Tier 1/2, eng, product, or legal | Issue is clearly a P1 needing eng/leadership packaging now -> skip triage, go to `customer-support:customer-escalation` |
| Customer is an existing account or active free-trial | Sender is a cold prospect / sales-context inquiry -> `sales:draft-outreach` |
| The ticket is operational | The ticket is a SOC 2 evidence request, security questionnaire with contractual reps, DSAR, or subpoena -> `legal:legal-response` |

## Workflow

### 1. Parse the issue
Extract: core problem, symptoms, customer context (account, plan, history), urgency signals (blocked? prod? users affected?), emotional state.

### 2. Categorize and prioritize
Assign primary + optional secondary category, P1-P4 priority, product area.

### 3. Check duplicates / known issues
Search support platform, knowledge base, project tracker. Apply duplicate detection rules below.

### 4. Determine routing
Use routing rules below. Pick the team or sibling skill that should own it next.

### 5. Generate triage output

```
## Triage: [one-line issue summary]

**Category:** [Primary] / [Secondary if applicable]
**Priority:** [P1-P4] — [brief justification]
**Product area:** [Area/team]

### Issue Summary
[2-3 sentences]

### Key Details
- **Customer:** [Name/account, plan, tenure]
- **Impact:** [Who/what affected]
- **Workaround:** [Available / Not / Unknown]
- **Related tickets:** [Links]
- **Known issue:** [Yes-link / No / Checking]

### Routing Recommendation
**Route to:** [Team / queue / sibling skill]
**Why:** [Brief reasoning]

### Suggested Initial Response
[Draft first reply using auto-response template by category]

### Internal Notes
- [Reproduction hints, escalation triggers, things checked already]
```

### 6. Offer next steps
- "Draft the full response now? -> `customer-support:draft-response`"
- "Need more context first? -> `customer-support:customer-research`"
- "Should I package this for eng? -> `customer-support:customer-escalation`"
- "This looks like a legal/compliance question — route to `legal:legal-response`?"

---

## Category Taxonomy

| Category | Description | Signal Words |
|---|---|---|
| **Bug** | Product behaving incorrectly | error, broken, crash, not working, failing |
| **How-to** | Guidance on using the product | how do I, where is, configure, help with |
| **Feature request** | Capability that doesn't exist | wish I could, any plans to, requesting |
| **Billing** | Payment, subscription, invoice | charge, invoice, refund, upgrade |
| **Account** | Access, permissions, settings | login, password, SSO, locked out |
| **Integration** | Third-party tools / APIs | API, webhook, OAuth, sync |
| **Security — incident** | Active or suspected security event affecting THIS customer | unauthorized access, suspicious login, data exposed, breach, ransomware |
| **Security — question** | Compliance/security question, no active incident | SOC 2, ISO, pen-test report, sub-processor list |
| **Data** | Quality, migration, import/export | missing data, export, duplicates |
| **Performance** | Speed, reliability, availability | slow, timeout, down, degraded |

### Category rules
- "It used to work" = **Bug**.
- "I want it different" = **Feature request**.
- "How do I" = **How-to**.
- Cannot log in due to a bug = **Bug** (root cause beats symptom).
- Customer reports active unauthorized access on their tenant = **Security — incident** (auto-P1, see below).
- Customer asks for SOC 2 report or wants the security questionnaire filled out = **Security — question**, route to `legal:legal-response` (NOT to internal security team unless legal kicks back).

## Priority Framework

### P1 — Critical (1 hr response, updates every 1-2 hr)
- Customer cannot use product at all
- Data loss / corruption / exposure
- **Any Security — incident category, by default**
- Issue worsening or expanding

### P2 — High (4 hr response, updates every 4 hr)
- Core workflow broken, partial usability
- Multiple users or key account
- Time-sensitive blocker, no workaround

### P3 — Medium (1 business day, resolution in 3)
- Feature partial, workaround exists
- Single user / small team
- Not escalating

### P4 — Low (2 business days)
- Cosmetic, feature request, general question

### Auto-bump triggers
- SLA breach already
- 3+ customers reporting same issue (pattern)
- Customer mentions exec / Twitter / churn
- Workaround stops working
- Scope expanded
- Strategic account in regulated industry (healthcare/finance/govt) -> bump one tier

## Routing Rules

| Route to | When |
|---|---|
| **Tier 1 (frontline)** | How-to, known-issue with documented fix, billing inquiries, password resets |
| **Tier 2 (senior)** | Bugs needing investigation, complex config, integration troubleshooting, account issues |
| **Engineering** | Confirmed bugs needing code fix, infrastructure, performance — package via `customer-support:customer-escalation` |
| **Product** | Feature requests with significant demand, design decisions |
| **Internal Security / CISO** | Security — incident category (always), suspected internal vulnerability, customer reporting our product was the vector |
| **Legal** (`legal:legal-response`) | SOC 2 evidence requests, security questionnaires with contractual reps, DSARs, subpoenas, regulatory inquiries, breach-notification obligations |
| **Billing / Finance** | Refund requests, contract disputes, complex billing |
| **CSM / AE** | Renewal-at-risk signal in support ticket (tag for the commercial conversation; support still owns the ticket) |

## Duplicate Detection

1. Search by symptom (similar error messages)
2. Search by customer (open tickets for same issue)
3. Search by product area (recent tickets in same feature)
4. Check known-issues list

If duplicate found: link tickets, notify customer it is tracked, add new info to existing ticket, bump priority if new report adds urgency (more customers / wider scope).

## Auto-Response Templates

### Bug
```
Thanks for reporting this — I can see how [specific impact] would be disruptive.
I have logged this as a [priority] issue and our team is investigating.
[Workaround if available.] I will update you within [SLA] with what we find.
```

### How-to
```
Great question. [Direct answer or doc link.]
Let me know if that helps or if you have follow-ups.
```

### Feature request
```
Thank you for the suggestion — I can see why [capability] would help your workflow.
I have logged it and shared with product. I cannot commit to a timeline, but your input
shapes our priorities. [Alternative if any.]
```

### Billing
```
Billing questions get prompt attention. I am reviewing your account now and
will have an answer within [timeframe].
```

### Security — incident
```
Thank you for flagging this. We treat suspected security events as P1 by default.
Our security team is investigating now and will follow up within 1 hour.
[If customer action needed: "In the meantime, please [rotate keys / disable user / etc.]."]
We will share scope and timeline as soon as we confirm.
```
(Always: route to internal CISO + CC `legal:legal-response` before customer-facing scope statements.)

### Security — question (compliance)
```
Thanks for the request. Compliance and contractual security artifacts are handled
by our legal team — I am routing this to them and they will reply within [SLA].
[If standard package exists: "We can typically share our SOC 2 Type II report under
NDA — happy to start that process now."]
```

## Triage best practices

1. Read the full ticket before categorizing — context in later messages can change the assessment.
2. Categorize by root cause, not symptom.
3. When in doubt on priority, err high — easier to de-escalate than to recover from a missed SLA.
4. Always check duplicates and known issues before routing.
5. Write internal notes that help the next person (what you checked / ruled out).
6. Flag patterns even if individual tickets are low priority.
7. For any Security — incident: do NOT promise scope or attribution in the initial response; let CISO + legal confirm first.
