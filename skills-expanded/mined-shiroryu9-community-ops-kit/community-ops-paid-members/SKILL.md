---
name: community-ops-paid-members
description: Use when designing or reviewing paid-member, premium, VIP, membership-tier, customer, subscriber, high-value user, renewal, benefit, exclusive activity, priority support, discount, entitlement, or member-retention operations. Keeps benefits explicit, evidence-based, and approval-gated.
---

# Community Ops Paid Members

Use this skill for paid members, premium users, customers, VIPs, high-value members, or users with special access/benefits.

## Project Inputs

Get the segment definition, confirmed benefits, entitlement or access basis, current issue or opportunity, available evidence, support path, and approval boundary for contact, discounts, benefits, roles, or access from the user or an approved project source.

The skill supplies the operating method. It does not include customer lists, payment status, benefits, discounts, role mappings, renewal data, or outreach permission. Do not infer those values from labels such as `VIP` or from repository examples. Use the minimum necessary user reference and mark missing entitlement or benefit facts for owner confirmation.

## Paid Member Loop

```text
access -> value discovery -> benefit use -> support/recognition -> renewal/upgrade signal -> review
```

## Design Questions

- What value does this segment receive beyond basic access?
- Which benefits are confirmed, and which need owner/product approval?
- What activity, support, tutorial, office hour, or showcase is exclusive to them?
- How are payment, entitlement, role, access, or discount issues escalated?
- What proves the segment is getting value?

## Output Pattern

```md
**Segment**
[Paid / premium / VIP / customer / high-value user.]

**Value Promise**
[Confirmed benefits only.]

**Operating Plan**
| Need | Action | Surface | Owner gate | Evidence |
|---|---|---|---|---|

**Care List**
- [Minimum necessary user/group reference + issue/opportunity + next follow-up.]

**Risk Boundary**
- Payment/access/discount/role changes require confirmation.
- Do not promise unconfirmed benefits.

**Review Signals**
- benefit usage;
- support resolution;
- participation;
- renewal/upgrade or churn-risk signals if available.
```

## Guardrails

Payment, discounts, role access, paid benefits, priority support promises, and renewal claims are high-stakes. Mark them owner-confirmation needed unless explicitly confirmed. Require confirmation before outreach, mentions, public recognition, access changes, discounts, or benefit promises. Keep sensitive member issues private, use the minimum necessary user-level data, and avoid personal consumption profiles.
