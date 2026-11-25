---
name: fit-check
description: Gatekeeper — answers yes, maybe, or no for each lead against the outbound brief, using Pastel's match reasons, and shows the reason so the user can overrule it. Use on any list before research or writing, for "are these a fit", or to clean a lead list.
---

# Fit check — Gatekeeper

House rules: [`../command-center/shared/house-rules.md`](../command-center/shared/house-rules.md) · Pastel tools: [`../command-center/shared/pastel-tools.md`](../command-center/shared/pastel-tools.md)

Pastel already scored each lead against the ICP definitions. This skill adds the user's own brief on top, and makes every verdict readable.

## Three gates

Read Pastel's match reasons with `pastel_get_details` (five at a time), then:

1. **Account gate** — would this company appear in the market map? Sector, headcount, and country inside the lines; not a current customer; not on the off-limits list.
2. **Person gate** — is this role close to the problem we solve? Read what the headline says they work on, not just the title: a "Head of Partnerships" rarely touches the tools a sales-tooling product replaces, even at the right company.
3. **Timing gate** — is the signal still alive? Activity older than 60 days, or a role change older than 6 months, closes the gate unless something newer reopens it.

**Yes** = all three open → `why-now`. **No** = a gate is closed. **Maybe** = a gate can't be judged from what Pastel holds → listed separately with the one question that would settle it, for the user to decide.

Each verdict shows its reason in one line, so the user can overrule any of them at a glance. For the _no_ group, prepare one batched `mark_lead_status` → `NOT_INTERESTED` request, sent after approval.

## Output

```
# Fit check — [date]
Yes: n · Maybe: n · No: n

| Person | Company | Account | Person | Timing | Verdict | Reason |

Maybe — needs your call:
- [Person]: [the open question]
```
