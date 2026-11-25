---
name: customer-support-refund
description: "Handle customer refund requests following company policy. Classify request, check eligibility, draft response, and escalate when needed."
---

# Customer Support Refund Skill

Enterprise skill for handling refund requests in customer support operations.

## When To Use

Use this skill when:
- Customer asks for a refund
- Support agent needs to check refund eligibility
- Response draft is needed for refund cases
- Escalation decision is required

## Required Inputs

- Order ID
- Purchase date
- Refund reason
- Customer tier (regular/VIP)
- Product category

## Workflow

### Phase 1: Validate Request

1. Check if order ID exists
2. Verify purchase date is within policy window
3. Identify customer tier from system

### Phase 2: Check Eligibility

1. Apply refund window rules:
   - Regular customers: 30 days
   - VIP customers: 60 days
2. Check product category restrictions:
   - Promotional items: not eligible
   - Custom products: not eligible
   - Standard products: eligible if conditions met
3. Verify product condition requirements

### Phase 3: Draft Response

1. Use approved tone: professional, empathetic
2. Include policy reference
3. State decision clearly (approved/denied/escalated)
4. Provide next steps

### Phase 4: Escalation Decision

Escalate to supervisor when:
- Refund amount > 1000 CNY
- Policy exception requested
- Legal concern raised
- Customer complaint filed

## Output Format

```yaml
decision: approved | denied | escalated
refund_amount: number
reason: string
customer_response: string
internal_notes: string
escalation_reason: string (if escalated)
```

## Risk And Escalation Rules

### Permissions

- Agents can approve refunds ≤ 1000 CNY within policy
- Supervisor approval required for > 1000 CNY
- Finance approval required for > 5000 CNY

### Prohibited Actions

- Never promise refunds outside policy scope
- Never share customer privacy data
- Never offer unauthorized discounts
- Never process refunds without order verification

### Escalation Triggers

- Amount exceeds agent authority
- Customer threatens legal action
- Policy conflict or ambiguity
- VIP customer dissatisfaction

## Source Grounding

All facts must reference:
- S01: Refund Policy Document (authoritative)
- S02: Customer Service Manual
- S03: Escalation Guidelines

When policy is unclear, mark as assumption and escalate.

## Validation

Test with these scenarios:
1. Happy path: standard refund within 30 days
2. VIP edge case: 45-day window
3. Denied: promotional item refund request
4. Escalation: 2000 CNY refund request

## Failure Handling

If required data is missing:
- Ask for order ID if not provided
- Ask for purchase date if not in system
- Do not guess customer tier

If policy conflict detected:
- Flag both conflicting policies
- Escalate to supervisor
- Do not make a decision

## Evolution Notes

This skill should improve when:
- New refund cases reveal policy gaps
- Customer satisfaction scores change
- Escalation patterns emerge
- Agent feedback indicates confusion
