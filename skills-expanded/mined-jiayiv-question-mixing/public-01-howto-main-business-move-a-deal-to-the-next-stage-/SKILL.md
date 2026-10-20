---
name: move-a-deal-to-the-next-stage
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 3min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Advance a CRM deal to the next pipeline stage only when the buyer evidence matches the stage criteria.

## Preconditions

- Access to edit the deal or opportunity.
- Current knowledge of the buyer status and agreed next step.
- A pipeline definition or sales process that explains stage exit criteria.

## Steps

1. **Open the deal.** Search for the opportunity or deal by account, contact, or deal name. → *Expect:* the current stage and deal details are visible.
2. **Check stage criteria.** Compare the deal evidence against the next stage requirement, such as qualified need, discovery complete, proposal sent, or verbal agreement. → *Expect:* there is a clear reason to move or hold the deal.
3. **Update required fields.** Enter amount, close date, next step, decision process, competitor, or probability fields required by the next stage. → *Expect:* no required-stage fields are blank.
4. **Move the stage.** [BRANCH: Salesforce | HubSpot | generic] select the next Opportunity Stage in Salesforce; drag or set Deal Stage in HubSpot; in another CRM, update the pipeline stage field. → *Expect:* the deal displays the new stage.
5. **Log the reason.** Add a brief note or activity explaining the evidence behind the stage change. → *Expect:* reviewers can see why the deal advanced.
6. **Save and confirm automation.** Save the record and review any created tasks, approvals, or notifications. → *Expect:* the CRM accepts the stage change and related workflow actions appear.

## Decision points

- If the buyer evidence is missing → keep the deal in the current stage and create a task to gather it.
- If the deal skipped a stage → confirm sales process allows skipping and document why.
- If stage movement triggers external communication → review the message before it sends.

## Failure modes & recovery

- **F1 Required field block:** detect a validation error → complete the missing field from verified deal information.
- **F2 Premature advancement:** detect stage criteria are not met → move the deal back and document the correction.
- **F3 Automation surprise:** detect unwanted tasks or emails created → pause or correct workflow items according to CRM permissions.

## Verification

The deal is in the intended next stage, required fields are complete, and the timeline contains evidence supporting the move.

## Variations

- `salesforce`: Stage changes may affect forecast category and probability.
- `hubspot`: Moving between board columns may trigger tasks, workflows, or required properties.
- `generic`: Use the local pipeline stage definitions as the authority.

## Safety & privacy

Stage changes affect forecast and management reporting. Do not inflate stage or amount to improve optics, and review any automation that could notify a customer.
