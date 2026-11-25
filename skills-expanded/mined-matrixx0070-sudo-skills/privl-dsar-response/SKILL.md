---
name: privl-dsar-response
version: 1.0.0
description: Handle a data-subject / consumer rights request end to end — verify identity, scope the right, apply exemptions, meet the statutory clock, and draft the response.
author: matrixx0070
tags: [privacy, legal, dsar, data-subject-rights, gdpr, ccpa, deadlines]
capabilities: []
---

## When to use

Use this when an individual exercises a privacy right — access, deletion/erasure, correction, portability, opt-out of sale/sharing, or restriction — and you must respond correctly and on time. It covers identity verification through drafting the reply.

**Not for:** deciding lawful basis for new processing (privl-use-case-triage) or reviewing a vendor DPA (privl-dpa-review). If the request is a general complaint rather than a rights exercise, do not force it into this workflow.

## Method

1. Log the request and **start the clock immediately**: GDPR = 1 month from receipt (Art. 12(3)), extendable +2 months for complex/numerous requests with notice inside the first month. CCPA/CPRA = 45 days, extendable once by +45 (90 total) with notice; confirm receipt within 10 business days.
2. **Verify identity** proportionate to the request's sensitivity — never disclose to an unverified requester. Clock pauses only where the law permits pending verification.
3. Identify the exact right invoked and the applicable regime(s); a person may have rights under more than one law.
4. Scope the data: search all systems, backups, and sub-processors holding the subject's data.
5. Apply exemptions/limits: third-party data, legal privilege, trade secrets, legal-hold/retention obligations, manifestly unfounded/excessive requests (GDPR Art. 12(5)), CCPA deletion exceptions.
6. **Decision point:** for deletion, confirm no overriding legal obligation to retain before erasing; propagate deletion to processors.
7. Draft the response: what you did, what you withheld and why, and appeal/complaint routes.
8. **Attorney-escalation gate:** refusals, redactions on privilege/third-party grounds, litigation-adjacent requests, or fee/excessive-request denials → counsel reviews before it goes out.

## Example

> **Request:** EU customer, access + deletion.
> **Clock:** 1 month, logged today. ID verified via account challenge.
> **Access:** exported profile, orders, support logs; redacted another customer's name from a shared thread.
> **Deletion:** honored except invoices under 7-yr tax-retention (legal obligation — Art. 17(3)(b)). Propagated to 3 processors.
> **Reply:** drafted with retention explanation + DPA complaint route; counsel cleared the redaction.

## Pitfalls

- Forgetting to start the clock at receipt — the deadline is not from when you noticed.
- Over- or under-verifying identity; both create liability.
- Deleting data that a legal-hold or statutory retention requires you to keep.
- Missing the subject's data in backups or at sub-processors.
- Charging a fee where the request is not actually excessive.

## Output format

```
DSAR — <subject> | regime: <GDPR/CCPA/both> | right: <access/delete/...>
Received: <date> | Deadline: <date> | Extension: <y/n + notice sent>
Identity: <verified how>
Data located: <systems/processors>
Provided: <what> | Withheld: <what + exemption>
Retention override: <n/a or basis>
For counsel: <items> | Response sent: <date>
```

## Reference

- **GDPR Art. 12(3)** one-month deadline (+2 months extension); **Art. 12(5)** manifestly unfounded/excessive; **Arts. 15-22** the rights; **Art. 17(3)** erasure exceptions.
- **CCPA/CPRA §1798.130** 45-day response (+45 extension), 10-business-day acknowledgment; deletion exceptions in §1798.105(d).
- Escalate refusals, privilege/third-party redactions, and fee-based denials to an attorney.
