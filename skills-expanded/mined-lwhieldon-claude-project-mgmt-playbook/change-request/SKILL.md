---
name: change-request
description: Draft a formal change request document from a description of a proposed scope change, with impact assessment, assumptions, exclusions, and an approval block. Use when a scope change needs to be documented and approved. Usage - /change-request describe what is changing and why
---

# Change Request

Draft a formal change request document from a description of the proposed change. Produces a
structured document ready for client review and approval signature.

## Input

`$ARGUMENTS` describes the change: what is changing, why, and any known impact on scope, timeline,
or cost. Helpful inputs:

- Who is requesting the change (client or firm)
- Known impact: additional effort (hours or days), timeline shift, cost delta
- Optional: the original SOW for baseline context. Read it if a path is given.

If the impact figures were not provided, leave them as `[NEEDS INPUT]`. Do not estimate effort or
cost on the delivery lead's behalf; those numbers are commitments.

## Output

**Change Request**
**CR Number:** CR-[###]
**Date:** [Today's date]
**Project:** [Project name from CLAUDE.md]
**Requested By:** [Client or firm]
**Status:** Pending Approval

---

**1. Change Description**
Clear, specific description of what is changing and what is not changing. No vague language.

**2. Reason for Change**
Business or technical justification. Why is this change necessary or beneficial? If the request is
contested (the client believes it was always in scope), state both positions plainly.

**3. Impact Assessment**

| Dimension | Baseline | Revised | Delta |
|---|---|---|---|
| Scope | [Original] | [Revised] | [Added / Removed] |
| Timeline | [Original end date] | [Revised end date] | [+/- days] |
| Estimated Cost | [Original] | [Revised] | [+/- $] |

**4. Assumptions**
List assumptions underlying this change estimate.

**5. Out of Scope**
Explicitly state what this change does NOT include to prevent scope creep on the change itself.

**6. Approval**

| Role | Name | Signature | Date |
|---|---|---|---|
| Client Sponsor | | | |
| Engagement Lead | | | |
| Client PM | | | |

*Drafted with Claude Code on YYYY-MM-DD; reviewed by [NAME]*

## Example Output

**CR Number:** CR-004
**Change Description:** Add a custom inventory aging report to the data warehouse delivery. The original SOW included 12 standard reports; this adds one additional report with custom aging buckets (30/60/90/120+ days) defined by the client's finance team.

**Impact Assessment:**
| Dimension | Baseline | Revised | Delta |
|---|---|---|---|
| Scope | 12 standard reports | 13 reports (12 standard + 1 custom) | +1 custom report |
| Timeline | Jun 30, 2025 | Jul 14, 2025 | +14 days |
| Estimated Cost | $485,000 | $512,000 | +$27,000 |
