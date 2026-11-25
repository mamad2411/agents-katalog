---
name: customer-escalation
description: Packages a customer escalation for engineering, product, or leadership with full context — combines customer impact, technical detail, history, and a recommended action into a complete escalation package. Make sure to use this skill whenever the user says escalate this to engineering, package this for product, this needs to go to leadership, build an escalation for [issue], the customer is threatening to churn, this bug needs eng attention, multiple customers report the same issue, or describes a customer issue that has outgrown normal support and needs cross-functional attention. Different from drafting a response TO the customer — this is for escalating WITHIN your org. Do NOT use for: routine ticket triage (use customer-support:ticket-triage), drafting a customer-facing reply (use customer-support:draft-response), or creating a knowledge base article from a resolved issue (use customer-support:kb-article). Defining characteristic: "internal escalation package, audience is engineering/product/leadership, not the customer."
---

# Customer Escalation

Packages a customer issue for internal escalation with full context for cross-functional action.

## When to use vs. adjacent support skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Internal escalation to eng/product/leadership | Drafting a reply TO the customer → `customer-support:draft-response` |
| Issue exceeds normal support scope | Routing a new ticket → `customer-support:ticket-triage` |
| Customer is threatening churn | Documenting resolution as KB article → `customer-support:kb-article` |
| Bug needs engineering investigation beyond standard | Multi-source research without escalation → `customer-support:customer-research` |

## When to actually escalate

Escalation is expensive (interrupts other teams). Use it when:

1. **Bug needs engineering investigation** beyond what support can debug
2. **Multiple customers report the same issue** — pattern indicates systemic
3. **Customer is threatening churn** explicitly (not vague frustration)
4. **Issue has sat past SLA** without resolution and standard re-escalation isn't moving it
5. **Strategic account is impacted** at material level (top-N revenue customer with ongoing degradation)
6. **Security or data integrity is involved** — never wait
7. **Regulatory/compliance issue surfaced** — legal needs to know
8. **Customer needs commitment beyond support's authority** (custom feature, exception to terms, refund above standard)

If none of these apply, don't escalate — work the standard process.

## Escalation package structure

Every escalation produced by this skill includes ALL of these sections:

```markdown
# ESCALATION: [Customer Name] — [Brief issue]

## Severity / Urgency
- **Severity:** P1 (data loss / outage) / P2 (broken workflow) / P3 (degraded but workable) / P4 (cosmetic)
- **Urgency:** Drop everything / Today / This week / Next sprint
- **Why this severity:** [Specific business impact]

## Customer Context
- **Account:** [Name, segment, ARR, contract end date]
- **Health:** [Score / churn risk / strategic importance]
- **History:** [Previous escalations, recent satisfaction signals]
- **Champion:** [Named contact, role, current sentiment]

## What's Happening (the issue)
[2-4 sentences describing the issue in customer-impact terms]

## Reproduction (if technical)
- **Environment:** [Their tier, region, integrations relevant]
- **Steps to reproduce:** [Specific, verified]
- **Expected behavior:** [What should happen]
- **Actual behavior:** [What is happening]
- **Frequency:** [Always / sometimes / specific conditions]
- **First observed:** [Date]
- **Logs / evidence:** [Links, ticket IDs, screenshots]

## Customer Impact
- **Direct impact:** [What they can't do / what's broken]
- **Quantified:** [# users affected, revenue at risk, hours lost, deadlines missed]
- **Customer's words:** [Their language, often a quote]

## Pattern (if multi-customer)
- **Other customers affected:** [Count, list with ticket IDs]
- **First reported:** [Date]
- **Trend:** [Increasing / stable / one-off]

## What Support Has Tried
- [Action 1]: [Result]
- [Action 2]: [Result]
- [Action 3]: [Result]

## Recommended Action
- **Asked of [team/owner]:** [Specific request]
- **Decision needed by:** [Date — driven by customer commitment, SLA, or escalation cadence]
- **Acceptable outcomes:** [What would resolve this — usually 2-3 options]

## Risk if Unaddressed
- [Specific risk: churn, escalation to public, regulatory exposure, contractual breach]
- [Probability: High / Medium / Low with rationale]

## Suggested Communication Plan
- **Customer update cadence:** [Daily / Twice-weekly / Weekly until resolved]
- **Internal status updates:** [Channel, frequency, owners]
- **Exec involvement trigger:** [What would warrant CEO/CRO involvement]
```

## Severity calibration

| Severity | Threshold | Examples |
|---|---|---|
| P1 | Production down / data loss / breach / strategic-account complete halt | Service outage, data corruption, security incident, top-10 customer can't operate |
| P2 | Broken critical workflow / major degradation / SLA violation imminent | Key feature broken, performance degraded 5x, integration failing |
| P3 | Degraded but workable / single-customer impact / non-critical | One feature buggy, minor performance issue, cosmetic UI bug affecting workflow |
| P4 | Cosmetic / future improvement / nice-to-have | UI polish, copy edit, low-impact friction |

## Audience-specific framing

The same escalation goes to different audiences with different framing:

### To Engineering
Lead with: reproduction, logs, technical diagnosis, suspected root cause area
Skip: ARR, churn risk (engineering doesn't optimize for that)
Add: which subsystem, what tests failed, recent deploys to check

### To Product
Lead with: customer-impact pattern, frequency across customers, feature gap surfaced
Skip: technical reproduction details
Add: roadmap impact, prioritization context, customer segments affected

### To Leadership
Lead with: customer name (if strategic), revenue at risk, public-relations risk
Skip: technical detail
Add: recommended escalation path, decision needed, exec-customer involvement option

This skill produces all three framings if asked, or one specific framing if the audience is named.

## Cybersecurity escalation patterns

For security/cybersec product issues, additional escalation paths:

### Customer reports security concern
- Escalate to: Security team + Eng + Legal (in parallel)
- Special urgency: any potential breach is automatic P1
- Documentation: chain of custody from first report
- Communication: legal counsel before public statements

### Customer fails their own audit because of you
- Escalate to: Customer Success leadership + Compliance
- Urgency: customer's audit timeline drives ours
- Need: written commitment, evidence package, timeline

### Customer security questionnaire stuck
- Escalate to: Security team + Sales (if pre-sale) or CSM (if existing)
- Less urgent unless deal is at risk
- Need: ETA from security team for completed responses

### Sub-processor change affects customer
- Escalate to: Compliance + Legal + CSM
- DPA notification clock starts (often 30 days)
- Need: customer notification draft + acknowledgment tracking

## Anti-patterns

- **Escalating without trying support resolution first** — wastes everyone's time
- **Vague impact ("customer is upset")** — quantify or it gets deprioritized
- **No ask** — escalation without specific request becomes a dump, not a decision
- **Escalating everything** — tunes others out; reserve escalation for actual escalations
- **Missing reproduction** — engineering can't act on "it doesn't work"
- **No deadline** — without a date, it sits in a queue forever
- **Single-channel escalation** — strategic accounts often need parallel escalation paths

## Output

Produces:
1. The full escalation package above
2. Audience-specific versions if multiple teams need it (eng + product + leadership)
3. Suggested communication plan
4. Customer follow-up draft (chains to `customer-support:draft-response` if customer needs an update)
5. Tracking recommendation (where to log this for visibility)
