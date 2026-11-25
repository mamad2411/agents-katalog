---
name: twilio-regulatory-compliance-bundles
version: 1.0.0
description: Assemble and submit Twilio Regulatory Bundles (Trust Hub) so you can buy and keep phone numbers that require country-specific End User identity and address proof.
author: matrixx0070
tags: [twilio, regulatory, trust-hub, bundles, compliance, phone-numbers]
capabilities: []
---

## When to use

Use this when you are trying to buy or provision a phone number in a country whose regulator requires identity and address documentation before the number can be assigned — Twilio blocks the purchase until an approved Regulatory Bundle is attached. Use it when a purchase fails with a "regulatory requirements not met" error, when a number is at risk of suspension for missing documents, or when you are onboarding numbers across several countries and need to know which End User type and documents each demands.

**Not for:** securing the credentials that call these APIs (see `twilio-security-api-auth`), or shaping the messaging you send once numbers are live (see `twilio-marketing-promotions-advisor` and `twilio-notifications-alerts-advisor`).

## Method

1. Identify the target country, number type (local, mobile, national, toll-free), and intended use. Regulatory requirements are keyed on all of these — a mobile number in Germany and a local number in the UK demand different proofs.
2. Look up the requirements programmatically. Query the Regulations resource to get the exact `end_user_type`, required `supporting_document` types, and address requirements for that country/number-type combination. Do not guess — requirements change per regulator.
3. Decision point: choose the End User type. If the number is for a person, use `individual`; if for a company, use `business`. This selection drives which End User Info fields and which documents Twilio will accept. Picking the wrong type forces a full resubmission.
4. Create the End User object with the required identity fields (for business: legal company name, registration number, address; for individual: full name, date of birth, address).
5. Create Supporting Documents by uploading the address proof and identity evidence (utility bill, business registration, passport/ID), then set their type to match what the Regulation demands.
6. Assemble the Regulatory Bundle: create the bundle in `draft`, attach the End User and each Supporting Document as bundle items, and reference the correct `regulation_sid`.
7. Submit the bundle for review. Its status moves `draft` → `pending-review` → `twilio-approved` (or `twilio-rejected`). Decision point: if rejected, read the rejection reason, fix the specific document or field, and resubmit — do not create a brand-new bundle.
8. Assign the approved bundle to the number at (or after) purchase via the `AddressSid`/`BundleSid` parameters, and record the bundle SID against the number for renewal.

## Example

```bash
# 1. Discover requirements for the country/number type
curl -sX GET "https://numbers.twilio.com/v2/RegulatoryCompliance/Regulations?IsoCountry=GB&NumberType=mobile" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET"

# 2. Create the End User (business)
curl -sX POST "https://numbers.twilio.com/v2/RegulatoryCompliance/EndUsers" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "FriendlyName=Acme Ltd" \
  --data-urlencode "Type=business" \
  --data-urlencode 'Attributes={"business_name":"Acme Ltd","business_registration_number":"12345678"}'

# 3. Create a Bundle in draft against the regulation
curl -sX POST "https://numbers.twilio.com/v2/RegulatoryCompliance/Bundles" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "FriendlyName=Acme GB Mobile" \
  --data-urlencode "Email=compliance@acme.com" \
  --data-urlencode "RegulationSid=RN0123..."

# 4. Attach items, then submit
curl -sX POST "https://numbers.twilio.com/v2/RegulatoryCompliance/Bundles/BU.../ItemAssignments" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "ObjectSid=IT..."   # EndUser or SupportingDocument SID

curl -sX POST "https://numbers.twilio.com/v2/RegulatoryCompliance/Bundles/BU..." \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "Status=pending-review"
```

## Pitfalls

- **Wrong End User type.** Choosing `individual` for a company (or vice versa) makes Twilio reject the whole bundle; the required documents differ. Confirm the type against the Regulation before building.
- **Address proof that does not match.** The address on the Supporting Document must match the End User address and satisfy the local-vs-national/foreign rules. A mismatch is the most common rejection cause.
- **Treating rejection as a restart.** Resubmit the same bundle after fixing the flagged item rather than creating a new one — a new bundle loses review history and slows approval.
- **Buying before approval.** Numbers in regulated countries cannot be purchased without an approved bundle attached; provisioning fails outright, it does not queue.
- **Ignoring renewal and drift.** Regulators update requirements; an approved bundle can later need refreshed documents. Track bundle SIDs per number and re-check status periodically or the number risks suspension.
- **Blurry or expired documents.** Uploads must be legible and current; expired IDs or cropped scans are rejected in review.

## Output format

```
# Regulatory Bundle: <country> / <number-type>
REGULATION: sid=<RN...> end_user_type=<individual|business>
END USER: sid=<IT...> name=<...> address=<...>
DOCUMENTS: [<type>=<DO... status>], ...
BUNDLE: sid=<BU...> status=<draft|pending-review|twilio-approved|twilio-rejected>
REJECTION (if any): <field/document> -> <reason> -> <fix>
NUMBER: <E.164> bundle=<BU...> assigned=<yes|no>
NEXT: <submit | fix+resubmit | assign to number | renewal check>
```

## Reference

- Product: Twilio Regulatory Compliance, part of Trust Hub. API base: `https://numbers.twilio.com/v2/RegulatoryCompliance/`.
- Core resources: `Regulations` (requirements per IsoCountry + NumberType), `EndUsers` (identity, `Type=individual|business`), `SupportingDocuments` (uploaded proofs), `Bundles` (container), and `ItemAssignments` (attach EndUser/Documents to a bundle).
- Bundle lifecycle status values: `draft`, `pending-review`, `in-review`, `twilio-approved`, `twilio-rejected`, and `provisionally-approved`.
- Authenticate with an API Key SID/Secret (or Account SID/Auth Token) over HTTPS Basic Auth.
- Many international local and mobile numbers, and some toll-free numbers, cannot be provisioned without an approved bundle; requirements are set by the local telecom regulator, not by Twilio, and vary by country and number type.
