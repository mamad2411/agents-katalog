---
name: twilio-lookup-phone-intelligence
version: 1.0.0
description: Enrich and risk-score a phone number with the Twilio Lookup API v2 — line type, caller name, SIM-swap, call forwarding, identity match, and reassigned number.
author: matrixx0070
tags: [twilio, lookup, phone, fraud, e164, intelligence]
capabilities: []
---

## When to use

Use this when you have a phone number and need to know something about it before acting: is it real and reachable, is it mobile or VoIP, has the SIM been swapped recently, is it forwarded, does the name match the account, was it reassigned to a new owner. Reach for it to screen signups, cut fraud, validate numbers before sending OTP, or reduce failed message delivery.

**Not for:** sending or checking OTP codes — use twilio-verify-send-otp. Not for deciding which verification strategy to adopt — use twilio-identity-verification-advisor. Lookup returns *intelligence*, not a verification decision by itself.

## Method

1. **Normalize to E.164.** Lookup v2 keys on the E.164 number in the path (`+14155551234`). Decision point: if you only have a national number, pass `CountryCode` so Twilio can format it, but prefer sending E.164 you already validated.
2. **Do a free format check first.** A bare `GET /v2/PhoneNumbers/{E.164}` with no data packages returns validity and formatting at no per-lookup data cost — use it to reject obviously malformed input cheaply.
3. **Select only the packages you need.** Each requested `Fields` package (line_type_intelligence, caller_name, sim_swap, call_forwarding, identity_match, reassigned_number) is billed separately. Request the minimum.
4. **Call Lookup** with `?Fields=line_type_intelligence,sim_swap` (comma-separated). Decision point: caller_name (CNAM) is US-only — don't request it for non-US numbers.
5. **Read `valid` first.** If `valid` is false, stop — the number is unusable; skip downstream sends.
6. **Interpret line type.** `mobile` → OTP SMS OK; `landline` → SMS will fail, use voice; `voip`/`nonFixedVoip` → elevated fraud risk, consider stronger factors.
7. **Score risk signals.** Recent sim_swap or active unconditional call_forwarding on an account-recovery flow is a red flag — block or step up. identity_match returns match scores against name/address/DOB you supply (some packages require end-user consent).
8. **Emit an action**, not just data: proceed, block, or escalate, with the deciding signals cited.

## Example

```bash
# Free validation + format
curl "https://lookups.twilio.com/v2/PhoneNumbers/+14155551234" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"

# Enriched: line type + SIM swap + caller name (US)
curl "https://lookups.twilio.com/v2/PhoneNumbers/+14155551234?Fields=line_type_intelligence,sim_swap,caller_name" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

```json
{
  "valid": true,
  "phone_number": "+14155551234",
  "country_code": "US",
  "line_type_intelligence": { "type": "mobile", "carrier_name": "T-Mobile USA" },
  "sim_swap": { "last_sim_swap": { "swapped_period": "PT48H", "swapped_in_period": true } },
  "caller_name": { "caller_name": "JANE DOE", "caller_type": "CONSUMER" }
}
```

```javascript
const info = await client.lookups.v2
  .phoneNumbers('+14155551234')
  .fetch({ fields: 'line_type_intelligence,sim_swap' });
if (!info.valid) reject();
if (info.lineTypeIntelligence.type === 'landline') useVoiceChannel();
```

## Pitfalls

- **Non-E.164 input gives garbage or errors.** Always format to E.164 (with `CountryCode` when needed) before calling — Lookup v2 keys on it in the URL path.
- **Every data package bills separately.** Requesting all `Fields` blindly multiplies cost. Start with the free format check, then add only the packages the decision needs.
- **caller_name (CNAM) is US-only.** Requesting it for international numbers returns nothing useful and can error — gate it on `country_code == US`.
- **Data can be null.** Carrier/CNAM/SIM-swap data is not universally available; treat missing fields as "unknown," never as "clean."
- **sim_swap and call_forwarding carry consent obligations** in some regions and packages; identity_match compares against PII you supply. Confirm you have a lawful basis before requesting them.
- **Lookup is a signal, not a verdict.** A `mobile` line still needs OTP/SNA to prove the user controls it — don't skip verification because Lookup "looked fine."

## Output format

```
LOOKUP RESULT
  number: <E.164>
  valid: <true|false>
  line_type: <mobile|landline|voip|nonFixedVoip|unknown>
  carrier: <name|unknown>
  caller_name: <CNAM|n/a (non-US)>
  sim_swap: <swapped_in_period true/false + window | unknown>
  call_forwarding: <active/none | unknown>
  identity_match: <score | n/a>
  risk: <low|medium|high>
  action: <proceed | block | step-up>
  deciding_signals: <list>
```

## Reference

- **Product:** Twilio Lookup API v2. Host `lookups.twilio.com`. Endpoint `GET /v2/PhoneNumbers/{E.164}`; enrich with `?Fields=<comma-separated packages>`; optional `CountryCode` for national-format input.
- **Data packages:** `line_type_intelligence` (mobile/landline/voip/nonFixedVoip + carrier), `caller_name` (CNAM, **US only**, consumer/business), `sim_swap` (recent SIM change window, carrier-sourced), `call_forwarding` (unconditional forwarding status), `identity_match` (score name/address/DOB against carrier records), `reassigned_number` (whether a number was disconnected/reassigned since a date — key for account recovery misdelivery).
- **Formatting:** E.164 = `+` + country code + subscriber number, digits only, no spaces or punctuation (max 15 digits). The base format/validation lookup (no `Fields`) is free.
- **Billing:** the base validation call is free; each data package is billed per successful lookup. Request the minimum set.
- **Auth:** HTTP Basic — Account SID + Auth Token, or API Key SID + Secret. Server-side only.
- **Compliance:** SIM-swap, call-forwarding, and identity_match involve carrier/consumer data subject to regional privacy law (GDPR, US state privacy laws) and, in some jurisdictions/packages, require end-user consent. Ensure a lawful basis before requesting risk/identity packages.
