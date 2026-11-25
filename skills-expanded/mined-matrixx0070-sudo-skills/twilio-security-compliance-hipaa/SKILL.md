---
name: twilio-security-compliance-hipaa
version: 1.0.0
description: Use Twilio for healthcare communications under HIPAA — sign the BAA, use only HIPAA-eligible products, keep PHI out of message bodies, and configure redaction and retention.
author: matrixx0070
tags: [twilio, hipaa, healthcare, phi, baa, compliance]
capabilities: []
---

## When to use

Use this when a Twilio integration will touch Protected Health Information (PHI) — patient appointment reminders, telehealth video, care-team messaging, lab-result notifications. Use it before sending anything health-related, when your organization is a Covered Entity or Business Associate, or when you must decide what may go in a message body. It defines the HIPAA obligations on top of the technical controls in the other security skills.

**Not for:** general credential security (see `twilio-security-api-auth`), webhook/transport hardening (see `twilio-security-hardening`), or transactional notification design when no PHI is involved (see `twilio-notifications-alerts-advisor`).

## Method

1. Execute a Business Associate Addendum (BAA) with Twilio *before* any PHI flows. Without a signed BAA, Twilio is not a Business Associate and no use of the platform for PHI is compliant — this is the gating step.
2. Confirm the products you use are HIPAA-eligible under the BAA. Twilio designates specific eligible products (e.g. Programmable SMS/MMS, Programmable Voice, Programmable Video, and SendGrid email under conditions); products and features not listed as eligible must not carry PHI even after the BAA.
3. Turn on the required configuration for eligibility. Some products only become HIPAA-eligible when specific settings are enabled (for example message/PII redaction, disabling certain logging, or restricting features); apply Twilio's documented HIPAA configuration for each product, do not assume defaults qualify.
4. Minimize PHI at the source: do not put PHI in the message body. Prefer content-free notifications ("You have a new message / appointment update — log in to the portal") and move the actual clinical detail behind an authenticated app or portal.
5. Decision point: if PHI must be conveyed, confirm the channel and product are eligible, the patient has been informed of the risks of unencrypted SMS/email and consented, and the minimum-necessary standard is met. If any of those fail, fall back to a content-free notification.
6. Enable message redaction and disable retention of PHI where offered — turn on body/PII redaction so PHI is not stored in Twilio logs, the console, or debugger, and set the shortest viable retention.
7. Apply the underlying security controls: TLS in transit, scoped API Keys, webhook signature validation, access controls, and audit logging (per `twilio-security-api-auth` and `twilio-security-hardening`) — HIPAA's Security Rule requires these safeguards regardless of the BAA.
8. Maintain your own compliance record: patient consent, the BAA, your product-eligibility mapping, audit logs, and an incident/breach-notification process. Twilio being a Business Associate does not discharge your Covered-Entity obligations.

## Example

Content-free (PHI-minimizing) reminder — clinical detail stays behind authenticated portal:

```bash
# GOOD: no PHI in the body; patient logs in for details
curl -sX POST "https://api.twilio.com/2010-04-01/Accounts/$ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "From=+15559876543" \
  --data-urlencode "Body=Reminder: you have an appointment tomorrow. Details/reschedule: portal.clinic.org"

# BAD (do not send): PHI in the body
# Body="Reminder: your oncology chemo infusion with Dr. Lee is at 9am"
```

Enable redaction on the Messaging Service so PHI is not retained in logs (configure per Twilio's HIPAA guidance in the console/API for the eligible product).

## Pitfalls

- **Sending PHI before the BAA is signed.** No BAA means Twilio is not a Business Associate and every PHI message is a violation. Sign it first, and note Twilio does not offer a BAA on trial accounts — you must be on a qualifying paid arrangement.
- **Assuming all Twilio products are covered.** Only designated products are HIPAA-eligible; using a non-eligible product or feature for PHI is non-compliant even with a BAA. Map each product before use.
- **PHI in the message body.** SMS and standard email are not end-to-end encrypted to the handset; diagnoses, provider specialties, or facility names in the body can themselves reveal PHI. Keep bodies content-free and move detail behind authentication.
- **Leaving redaction off / logs retaining PHI.** Default logging may store message bodies in the console and debugger. Enable redaction and minimize retention so PHI is not persisted by Twilio.
- **Skipping the eligibility configuration.** Some products are only eligible when specific settings are enabled; the BAA alone is not sufficient. Apply the documented per-product HIPAA configuration.
- **Assuming the BAA ends your obligations.** You remain the Covered Entity/Business Associate: consent, minimum-necessary, audit logging, and breach notification are still yours.

## Output format

```
# HIPAA Twilio Review: <use case>
BAA: signed=<yes|no> account=<paid/qualifying> (trial=not-eligible)
PRODUCTS: [<product> eligible=<yes|no> config-applied=<yes|no>]
PHI IN BODY: none (content-free) | justified=<consent+eligible+min-necessary>
CHANNEL: <sms|voice|video|email> encryption=TLS patient-informed=<yes|no>
REDACTION: message/PII redaction=on retention=<shortest viable>
SECURITY: tls=yes scoped-keys=yes webhook-validation=yes audit-logs=on
RECORDS: consent+baa+eligibility-map+breach-process=maintained
VERDICT: <send content-free | send PHI (justified) | block> GAPS: [...]
```

## Reference

- HIPAA basics: PHI is individually identifiable health information. Under HIPAA, a vendor that handles PHI on a Covered Entity's behalf is a Business Associate and must sign a Business Associate Agreement/Addendum (BAA). Twilio will act as a Business Associate and offers a BAA to eligible (non-trial, qualifying) customers.
- HIPAA-eligible products: Twilio designates specific products as HIPAA-eligible — commonly Programmable Messaging (SMS/MMS), Programmable Voice, Programmable Video, and Twilio SendGrid email under defined conditions. Products/features not designated eligible must not carry PHI. Always confirm the current eligibility list in Twilio's HIPAA documentation.
- Eligibility often requires configuration: enabling message/PII redaction, restricting logging/retention, or limiting features per product — the BAA is necessary but not sufficient on its own.
- PHI minimization: SMS and standard email are not encrypted to the endpoint; keep PHI out of message bodies, use content-free notifications, and place clinical detail behind an authenticated portal/app. Obtain patient consent and meet the minimum-necessary standard when PHI must be sent.
- Security Rule safeguards still apply: TLS in transit, access controls, scoped API Keys, `X-Twilio-Signature` webhook validation, and audit logging (see `twilio-security-api-auth` and `twilio-security-hardening`).
- The BAA does not transfer your Covered-Entity obligations: you retain responsibility for consent, minimum necessary, workforce access controls, audit, and breach notification.
