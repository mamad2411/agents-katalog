---
name: time-off-request
description: |
  Drafts an approval-ready time-off or leave request with policy compliance
  checks, coverage plan, and handover notes — or evaluates an incoming request
  from a manager's perspective. Use when the user says "draft a time-off
  request", "write a vacation request to my manager", "help me request PTO",
  "I need to take leave next month", or "review this time-off request from my
  report". For the individual request transaction, not policy authoring
  (employee-handbook-builder).
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="time-off-request")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session. Pay particular attention to:
- Organisation-specific leave policies, accrual rules, and blackout periods
- User's role (requestor vs. approving manager)
- Historical leave patterns and any prior approval/denial context
- Team coverage norms and minimum staffing thresholds

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Role in this request**: Are you submitting a time-off request or reviewing/approving one?
- **Leave type**: PTO, sick leave, bereavement, parental leave, unpaid leave, sabbatical, jury duty, floating holiday, or other
- **Date range**: Start date, end date, and whether partial days are involved
- **Coverage context**: Team size, critical deliverables or deadlines during the requested period, and any pre-arranged coverage
- **Organisational constraints**: Known blackout periods, peak seasons, or concurrent approved absences on the team
- **Urgency**: Is this a planned request or an emergency/retroactive submission?

If FutureProof context already contains the user's company leave policy, team roster, or accrual balances, confirm these rather than re-asking.

## Step 3: Validate Policy Compliance

Conduct a rigorous compliance check against applicable leave policy:

1. **Accrual & Balance Verification** — Does the requestor have sufficient accrued hours/days for the requested leave type? Flag if the request would result in a negative balance or require advance borrowing against future accruals.
2. **Notice Period Compliance** — Does the submission meet the organisation's minimum advance notice requirement (e.g., 14 days for planned PTO, 2 hours for unplanned sick leave)?
3. **Blackout Period Check** — Does the requested window overlap with any defined blackout periods (fiscal close, product launches, annual planning cycles)?
4. **Consecutive Day Threshold** — Does the request exceed the maximum consecutive days permitted without escalated approval (e.g., requests exceeding 10 business days requiring VP-level sign-off)?
5. **Concurrent Absence Conflict** — Are other team members already approved for overlapping dates, and would this request breach minimum staffing ratios?
6. **Eligibility Verification** — Has the requestor met tenure or probationary requirements for the specific leave type (e.g., sabbatical eligibility after 5 years)?

Apply any user-specific `instructions` from FutureProof context — for example, if the organisation uses a specific HRIS (Workday, BambooHR, ADP), tailor field references and workflow steps accordingly.

## Step 4: Assess Coverage & Operational Impact

Perform a coverage impact analysis at consulting-grade rigour:

1. **Critical Path Mapping** — Identify deliverables, meetings, and decision gates that fall within the leave window. Classify each as deferrable, delegable, or at-risk.
2. **Delegation Matrix** — For each non-deferrable responsibility, recommend a specific backup assignee based on skill match, current workload, and availability. Produce a RACI-style handover outline.
3. **Client/Stakeholder Exposure** — Flag any external commitments (client presentations, vendor deadlines, regulatory filings) and recommend pre-leave communication actions.
4. **Cumulative Team Impact Score** — Rate the operational risk on a 1–5 scale:
   - **1 — Negligible**: Full coverage exists, no critical path items
   - **2 — Low**: Minor delegation required, no external exposure
   - **3 — Moderate**: Meaningful delegation needed, manageable with planning
   - **4 — High**: Critical path items at risk, requires mitigation plan
   - **5 — Severe**: Approval contingent on material risk mitigation

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce the following structured deliverables:

### A. Time-Off Request Document
A polished, submission-ready request formatted for the user's HRIS or email-based approval workflow:
- **Requestor name & department**
- **Leave type & dates** (including total business days and hours)
- **Remaining balance** after approval (if known)
- **Coverage plan summary** (who covers what)
- **Approver & routing** (direct manager, skip-level if escalation required)

### B. Policy Compliance Summary
| Compliance Dimension | Status | Notes |
|---|---|---|
| Accrual Balance | ✅ / ⚠️ / ❌ | Specific finding |
| Notice Period | ✅ / ⚠️ / ❌ | Specific finding |
| Blackout Period | ✅ / ⚠️ / ❌ | Specific finding |
| Consecutive Day Limit | ✅ / ⚠️ / ❌ | Specific finding |
| Concurrent Absence | ✅ / ⚠️ / ❌ | Specific finding |
| Eligibility | ✅ / ⚠️ / ❌ | Specific finding |

### C. Coverage & Handover Plan
- **Delegation matrix**: Task → Backup owner → Briefing date
- **Pre-leave actions checklist**: Communications to send, documents to share, access to grant
- **Operational Impact Score**: 1–5 with justification
- **Risk mitigation recommendations**: Specific actions to reduce score by at least one level

### D. Manager Recommendation (if user is the approver)
- **Approve / Approve with conditions / Defer / Deny** recommendation with rationale
- **Conditions** (if applicable): e.g., "Approve contingent on completing Q3 forecast draft before departure"

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="time-off-request", experiment={
  hypothesis: "Providing a pre-populated delegation matrix with the initial request reduces manager approval turnaround time",
  variants: ["control: standard request without delegation plan", "variant: request bundled with delegation matrix and coverage score"],
  measurement: "Average time from submission to final approval across next 15 requests",
  expected_impact: "40% reduction in approval cycle time and 25% fewer back-and-forth clarification messages"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="time-off-request",
  query="Best practices for leave management automation, coverage planning frameworks, and 2024 trends in PTO policy design including unlimited PTO governance structures",
  reason="Ensure compliance checks reflect current regulatory changes (state/provincial leave mandates) and that coverage planning aligns with modern hybrid/remote workforce patterns"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="time-off-request", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```