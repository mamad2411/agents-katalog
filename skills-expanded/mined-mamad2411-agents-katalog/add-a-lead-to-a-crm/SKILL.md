---
name: add-a-lead-to-a-crm
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

Create a new CRM lead record with enough accurate information for follow-up and routing.

## Preconditions

- Access to the CRM with permission to create leads.
- The prospect's name, company, and at least one contact method.
- A lawful source for the lead, such as a form fill, event badge, referral, or approved prospecting list.

## Steps

1. **Open the lead creation flow.** [BRANCH: Salesforce | HubSpot | generic] in Salesforce, open Leads and select New; in HubSpot, open Contacts and select Create contact; in another CRM, open the lead or contact create form. → *Expect:* a blank lead or contact form is visible.
2. **Enter core identity fields.** Add first name, last name, company, email, phone, title, and website when available. → *Expect:* required identity fields are populated.
3. **Record the lead source.** Choose the source value that matches how the prospect entered the pipeline. → *Expect:* source is visible on the record.
4. **Add routing context.** Set owner, territory, lifecycle status, product interest, and campaign if those fields are used. → *Expect:* the lead can be assigned and reported correctly.
5. **Save the record.** Select Save or Create and wait for the CRM to load the new record page. → *Expect:* the lead record has a CRM ID or URL.
6. **Add a next action.** Create a follow-up task or sequence enrollment only if outreach is appropriate. → *Expect:* the record shows the next action and owner.

## Decision points

- If the person is already in the CRM → update the existing record instead of creating a duplicate.
- If consent or source is unclear → create the record only as allowed by policy and do not enroll in outreach.
- If the company already exists → associate the lead with the existing account or company.

## Failure modes & recovery

- **F1 Duplicate found:** detect an existing email, phone, or company match → merge or update the existing record according to CRM policy.
- **F2 Missing required field:** detect a save error on a required field → enter the best verified value or use the approved placeholder policy.
- **F3 Wrong owner:** detect the record assigned to the wrong queue or rep → update owner and note why it changed.

## Verification

The CRM contains one lead or contact record with the prospect's identity, source, owner or queue, and a visible next action if follow-up is permitted.

## Variations

- `salesforce`: Leads may convert into Accounts, Contacts, and Opportunities after qualification.
- `hubspot`: Contacts often carry lifecycle stage instead of a separate lead object.
- `generic`: Use the object's local naming convention, but preserve source, owner, and next-action fields.

## Safety & privacy

Store only business-relevant data from lawful sources. Do not add sensitive personal notes, scraped private contact data, or outreach tasks that violate consent, CAN-SPAM, GDPR, or company policy.
