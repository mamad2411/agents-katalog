---
name: dedupe-crm-contacts
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 20min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Identify and merge duplicate CRM contact records while preserving the best data, history, and associations.

## Preconditions

- CRM permission to merge or edit contacts.
- Duplicate candidates identified by email, name, phone, company, or CRM duplicate tool.
- Understanding of the CRM's merge behavior.

## Steps

1. **Open duplicate candidates.** [BRANCH: Salesforce | HubSpot | generic] use matching rules or duplicate jobs in Salesforce; use Manage duplicates in HubSpot; in another CRM, open the duplicate detection tool or search results. → *Expect:* possible duplicate contact records are visible.
2. **Confirm they are the same person.** Compare email, phone, company, title, location, activity, and source. → *Expect:* duplicates are confirmed or rejected.
3. **Choose the primary record.** Select the record with the best owner, activity history, consent status, and system associations. → *Expect:* one record is identified as the survivor.
4. **Review field values.** Choose the most accurate values for email, phone, title, company, lifecycle stage, owner, and consent fields. → *Expect:* important data will not be overwritten accidentally.
5. **Merge records.** Use the CRM merge action and confirm the selected primary and retained values. → *Expect:* one contact record remains after the merge.
6. **Check associations and activity.** Verify account, deals, tickets, campaigns, tasks, emails, and meetings carried over. → *Expect:* history and relationships are intact.
7. **Add a cleanup note if useful.** Note the merge reason when the CRM timeline does not show it clearly. → *Expect:* future users understand why the duplicate disappeared.

## Decision points

- If records may be different people at the same company → do not merge; add differentiating fields instead.
- If consent fields conflict → preserve the most restrictive valid consent state unless policy says otherwise.
- If one record is synced from another system → check integration rules before merging.

## Failure modes & recovery

- **F1 False duplicate:** detect different emails, roles, or activity patterns for two people → cancel merge and mark as not duplicate.
- **F2 Data overwritten:** detect wrong value retained after merge → restore from field history or the losing record preview if available.
- **F3 Association lost:** detect missing deal or account link → manually reassociate the surviving contact.

## Verification

Only one contact record remains for the person, with correct key fields, preserved consent state, and expected activities and associations.

## Variations

- Bulk dedupe: export or review samples first and merge in small batches.
- Salesforce person accounts: confirm account/contact merge behavior before proceeding.
- HubSpot duplicates: review property-level choices in the merge wizard.

## Safety & privacy

Merging contacts can combine personal data and consent states. Preserve opt-outs, avoid exposing data across accounts, and follow CRM retention and audit policies.
