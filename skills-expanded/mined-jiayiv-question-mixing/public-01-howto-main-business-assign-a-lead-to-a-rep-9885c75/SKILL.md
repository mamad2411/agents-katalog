---
name: assign-a-lead-to-a-rep
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Assign a lead to the correct sales rep or queue so follow-up ownership is clear.

## Preconditions

- CRM permission to update lead owner.
- A lead that needs routing.
- Routing rules or territory guidance for owner selection.

## Steps

1. **Open the lead record.** Search by name, email, company, or lead ID. → *Expect:* the lead owner field is visible.
2. **Review routing signals.** Check region, segment, account ownership, product interest, source, and language if relevant. → *Expect:* the correct owner or queue can be determined.
3. **Check for existing account ownership.** Search matching company or domain for an active owner. → *Expect:* assignment will not bypass an existing account owner.
4. **Update the owner.** [BRANCH: Salesforce | HubSpot | generic] change Lead Owner in Salesforce; change Contact owner or Lead owner in HubSpot; in another CRM, update owner or assignee. → *Expect:* the selected rep or queue appears as owner.
5. **Set the follow-up task.** Create or transfer the next outreach task to the assigned owner. → *Expect:* the assignee has a dated action.
6. **Notify if needed.** Use CRM notification, mention, or routing workflow only when the rep will not otherwise see the assignment. → *Expect:* the owner knows the lead is assigned.

## Decision points

- If the lead belongs to an existing customer account → assign to the account owner or customer team according to policy.
- If no matching owner exists → assign to the approved inbound queue.
- If the lead is disqualified → set status and reason instead of assigning for outreach.

## Failure modes & recovery

- **F1 Territory mismatch:** detect owner conflicts with region or segment rules → reassign to the correct rep and document the correction.
- **F2 Owner updated without task:** detect ownership changed but no next action → create a follow-up task for the owner.
- **F3 Duplicate lead routed:** detect another active lead or contact for the same person → merge or coordinate ownership before outreach.

## Verification

The lead record shows the correct owner or queue, a follow-up task assigned to that owner, and no unresolved duplicate or account-owner conflict.

## Variations

- Round-robin routing: use the CRM queue or routing workflow instead of manually picking a rep.
- Named-account sales: account ownership overrides inbound lead source.
- Partner lead: route to channel owner or partner manager if required.

## Safety & privacy

Lead assignment exposes prospect data to a rep or queue. Assign only to authorized users and avoid notifying broad channels with personal contact details.
