---
name: qualify-a-lead
domain: business
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Assess whether a lead is worth active sales pursuit and record the qualification outcome in the CRM.

## Preconditions

- A lead or contact record with source and contact information.
- A qualification framework such as ICP fit, BANT, MEDDICC, or company-specific criteria.
- Recent information from a form, call, email, enrichment source, or website activity.

## Steps

1. **Open the lead record.** Review source, company, title, activity, and existing notes. → *Expect:* the available qualification evidence is visible.
2. **Check account fit.** Compare industry, company size, geography, use case, and technology fit against the ideal customer profile. → *Expect:* fit is marked strong, partial, or poor.
3. **Assess buying intent.** Review inquiry type, content viewed, meeting request, reply quality, or stated project. → *Expect:* intent level is clear.
4. **Assess authority and timing.** Identify role, decision influence, urgency, and likely buying window. → *Expect:* the lead has a documented buyer role and timing estimate.
5. **Update qualification fields.** [BRANCH: Salesforce | HubSpot | generic] update Lead Status and rating in Salesforce; update Lifecycle Stage, Lead Status, or fit properties in HubSpot; in another CRM, update qualification status and score fields. → *Expect:* the CRM reflects the qualification decision.
6. **Choose the next action.** Convert, route, nurture, disqualify, or ask for more information. → *Expect:* the lead has a next path, not just a score.
7. **Document the rationale.** Add a short note naming the evidence and any uncertainty. → *Expect:* another rep can audit the decision.

## Decision points

- If the lead is high fit and high intent → route to sales quickly.
- If fit is good but timing is weak → place in nurture with a future review date.
- If the lead is a student, vendor, competitor, or outside market → disqualify with the correct reason.
- If data is insufficient → schedule one research or discovery action before deciding.

## Failure modes & recovery

- **F1 Overqualified from title only:** detect no company or intent evidence → revisit fit and intent fields before routing.
- **F2 Missing disqualification reason:** detect a closed or rejected lead without reason → add the approved reason code.
- **F3 Stale information:** detect old activity driving the decision → refresh activity and enrichment before qualifying.

## Verification

The lead record has qualification status, fit or score evidence, documented rationale, and a routed, nurtured, disqualified, or research-next action.

## Variations

- Inbound lead: weight declared need and recent activity heavily.
- Outbound lead: qualify mostly on ICP fit before outreach.
- Product-led lead: include usage signals and workspace activity if approved for sales use.

## Safety & privacy

Use only approved business data for qualification. Avoid protected-class assumptions, private personal details, or hidden profiling that violates privacy law or company policy.
