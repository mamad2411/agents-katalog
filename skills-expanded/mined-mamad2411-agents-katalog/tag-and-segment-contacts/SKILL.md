---
name: tag-and-segment-contacts
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Apply tags or segment membership to CRM contacts so they can be filtered, routed, reported, or messaged appropriately.

## Preconditions

- CRM permission to edit contact properties, tags, lists, or segments.
- Clear segment criteria and intended use.
- Consent and suppression rules if the segment will be used for outreach.

## Steps

1. **Define the segment rule.** Write the exact inclusion and exclusion criteria, such as persona, product interest, lifecycle stage, region, or event source. → *Expect:* membership can be checked objectively.
2. **Find matching contacts.** Use CRM filters, reports, or list builder to identify contacts that meet the rule. → *Expect:* candidate contacts are visible.
3. **Review exclusions.** Remove duplicates, opt-outs, restricted accounts, wrong owners, and contacts that fail the criteria. → *Expect:* the segment contains only eligible contacts.
4. **Apply the tag or segment.** [BRANCH: Salesforce | HubSpot | generic] update a campaign, field, or list in Salesforce; create a static or active list in HubSpot; in another CRM, apply the tag, saved segment, or property. → *Expect:* selected contacts show the tag or membership.
5. **Name and document the segment.** Use a clear name and description with owner, date, source, and purpose. → *Expect:* future users understand why the segment exists.
6. **Test membership.** Open several included and excluded contacts to confirm the rule behaves correctly. → *Expect:* sample contacts match the intended logic.

## Decision points

- If membership should update automatically → use a dynamic or active list.
- If the segment is for a one-time campaign → use a static list with source documentation.
- If outreach is planned → verify consent, opt-out, and frequency caps before activation.

## Failure modes & recovery

- **F1 Overbroad segment:** detect contacts outside the intended audience → tighten filters and remove incorrect members.
- **F2 Missing exclusions:** detect opted-out or restricted contacts → add exclusion rules and rerun membership.
- **F3 Ambiguous tag name:** detect users cannot tell purpose from the tag → rename or document the segment.

## Verification

The CRM segment or tag has documented criteria, correct sample membership, required exclusions, and a clear owner or purpose.

## Variations

- Campaign segment: include campaign source, consent, and send eligibility.
- Sales routing segment: include territory, company size, and owner rules.
- Customer health segment: use product usage or renewal signals if approved.

## Safety & privacy

Segments can reveal behavior, interest, or customer status. Limit access to authorized users and apply consent, suppression, and purpose limits before using segments for outreach.
