---
name: enrich-a-contact-record
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Improve a CRM contact record with verified business information that supports routing, segmentation, and sales context.

## Preconditions

- CRM access to edit the contact.
- Approved enrichment sources such as company website, LinkedIn, data provider, form submission, or email signature.
- A policy for which fields may be enriched.

## Steps

1. **Open the contact record.** Search by email, name, or company. → *Expect:* the existing contact fields are visible.
2. **Review current data quality.** Check blank, outdated, conflicting, or low-confidence fields. → *Expect:* enrichment targets are identified.
3. **Verify business identity.** Confirm current company, title, location, website, phone, and role from approved sources. → *Expect:* updates are based on a reliable source.
4. **Update CRM fields.** [BRANCH: Salesforce | HubSpot | generic] edit Contact fields in Salesforce; edit contact properties in HubSpot; in another CRM, update the equivalent profile fields. → *Expect:* enriched values appear on the record.
5. **Record source or confidence.** Add source notes, last-enriched date, or data provider confidence if the CRM supports it. → *Expect:* future users can judge data reliability.
6. **Review ownership and segments.** Update account association, owner, lifecycle stage, persona, or segment if enrichment changes routing. → *Expect:* the contact fits the right operational bucket.
7. **Save and refresh.** Save changes and reload if needed to confirm automations finished. → *Expect:* the record shows updated fields and any triggered changes.

## Decision points

- If two sources conflict → prefer the most direct and recent source, or leave the field unchanged with a note.
- If the contact left the company → update status according to policy and avoid outreach to old work email.
- If enrichment reveals sensitive personal data → do not store it unless explicitly approved.

## Failure modes & recovery

- **F1 Unverified data added:** detect values copied from an unapproved source → remove or replace with verified data.
- **F2 Account mismatch:** detect contact associated to the wrong company → correct the association and owner if needed.
- **F3 Automation changed fields:** detect unexpected score, segment, or owner changes → review workflow history and correct according to policy.

## Verification

The contact record contains verified business fields, source or confidence context, correct account association, and no unauthorized personal data.

## Variations

- Data-provider enrichment: review confidence scores before accepting bulk updates.
- Manual research: use only public business sources and company-approved databases.
- Event lead: enrich with event name, booth scan context, and declared interest.

## Safety & privacy

Limit enrichment to business-relevant data from approved sources. Do not store sensitive personal data, protected-class information, or private contact details without a lawful basis.
