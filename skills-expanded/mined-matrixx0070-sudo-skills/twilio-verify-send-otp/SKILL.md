---
name: twilio-verify-send-otp
version: 1.0.0
description: Send and check one-time passcodes with the Twilio Verify API v2 across SMS, voice, email, and WhatsApp, with fraud and rate-limit handling.
author: matrixx0070
tags: [twilio, verify, otp, 2fa, sms, authentication]
capabilities: []
---

## When to use

Use this when you need to send a one-time passcode and then confirm the code a user typed back — phone/email verification, two-factor login, transaction step-up, or account recovery. Use it whenever the goal is "prove the user controls this phone number or inbox right now." It wraps Twilio Verify v2 so you never store, hash, or expire codes yourself — Twilio owns the code lifecycle.

**Not for:** deciding *whether* OTP is the right factor at all, or picking between OTP, Lookup, and Silent Network Auth — that is an advisory call, use twilio-identity-verification-advisor. Not for enriching or validating a number before you send (line type, SIM-swap) — use twilio-lookup-phone-intelligence. Not for building the surrounding IVR/messaging flow — use twilio-studio-flows.

## Method

1. **Confirm a Verify Service exists.** Verify is scoped to a Service (`VAxxxxxxxx...`). Reuse the app's existing Service so friendly name, code length, and settings stay consistent. Decision point: if no Service SID is available, create one via `POST /v2/Services` with a `FriendlyName` before sending anything.
2. **Normalize the destination.** For sms/call/whatsapp the `To` must be E.164 (`+14155551234`). For email the `To` is the address and you must pass `Channel=email`. Reject anything not normalizable rather than sending to a malformed target.
3. **Pick the channel.** `sms`, `call`, `email`, or `whatsapp`. Decision point: if the user is on a landline, `sms` will fail — fall back to `call`. If email delivery is configured (SendGrid integration), `email` avoids carrier filtering.
4. **Start the verification.** `POST /v2/Services/{ServiceSid}/Verifications` with `To` and `Channel`. Twilio generates, sends, and tracks the code. Do not generate the code yourself.
5. **Handle the start response.** Status returns `pending`. Persist the `To` (or a session token), not the code — you never see it. Decision point: on HTTP 429 or `max attempts` errors, back off and surface a rate-limit message rather than retrying immediately.
6. **Collect the code from the user**, then check it: `POST /v2/Services/{ServiceSid}/VerificationCheck` with `To` and `Code`.
7. **Branch on check status.** `approved` = success, mark the factor verified. `pending` = wrong code, let the user retry (finite attempts). Decision point: after Twilio returns a 404 on check, the verification has expired (default 10 minutes) or was already consumed — start a fresh verification, do not loop.
8. **Enforce your own attempt ceiling** on top of Twilio's, and log outcomes for fraud review.

## Example

```bash
# 1. Start an SMS verification
curl -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SERVICE_SID/Verifications" \
  --data-urlencode "To=+14155551234" \
  --data-urlencode "Channel=sms" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
# -> { "sid": "VE...", "status": "pending", "channel": "sms", "valid": false }

# 2. Check the code the user entered
curl -X POST "https://verify.twilio.com/v2/Services/$VERIFY_SERVICE_SID/VerificationCheck" \
  --data-urlencode "To=+14155551234" \
  --data-urlencode "Code=123456" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
# -> { "status": "approved", "valid": true }
```

```javascript
// Node twilio SDK
const client = require('twilio')(accountSid, authToken);
await client.verify.v2.services(serviceSid)
  .verifications.create({ to: '+14155551234', channel: 'sms' });

const check = await client.verify.v2.services(serviceSid)
  .verificationChecks.create({ to: '+14155551234', code: '123456' });
if (check.status === 'approved') { /* grant */ }
```

## Pitfalls

- **Never generate or store the code.** Twilio owns generation, delivery, expiry, and attempt counting. If you find yourself saving a code, you are fighting the API — persist only the `To` and status.
- **Codes expire in ~10 minutes by default.** A check after expiry returns a 404, not `pending`. Treat 404 as "expired/consumed → restart," never as a transient error to retry.
- **A verification is single-max-attempt-scoped.** Repeated `VerificationCheck` failures burn attempts and eventually invalidate the verification; start fresh instead of hammering.
- **Rate limits and Fraud Guard bite silently.** Twilio applies per-`To` rate limits and Fraud Guard (SMS Pumping protection) may block high-risk destinations. Handle 429 and 60xxx error codes with user-facing backoff, and consider Rate Limits / Programmable Rate Limits buckets for custom throttling.
- **Landlines can't receive SMS.** Detect line type up front (twilio-lookup-phone-intelligence) or fall back to the `call` channel on delivery failure.
- **TCPA applies to the delivery SMS/call.** OTP messages are generally treated as transactional, but you still need the number to be user-provided for the purpose of authentication; do not repurpose Verify traffic for marketing.

## Output format

```
VERIFY RESULT
  channel: <sms|call|email|whatsapp>
  to: <E.164 or email>
  start_status: <pending|error>
  check_status: <approved|pending|expired|not_started>
  attempts_used: <n>/<max>
  action: <grant | retry | restart | fallback:call>
  notes: <rate-limit / fraud / delivery observations>
```

## Reference

- **Product:** Twilio Verify (API v2). Base host `verify.twilio.com`.
- **Resources:** `POST /v2/Services` (create Service, returns `VA...` SID); `POST /v2/Services/{ServiceSid}/Verifications` (start, status `pending`); `POST /v2/Services/{ServiceSid}/VerificationCheck` (verify, status `approved`/`pending`).
- **Channels:** `sms`, `call` (TTS voice), `email` (requires a configured SendGrid email integration on the Service), `whatsapp`. Also supports `sna` (Silent Network Auth) and Push/TOTP via separate flows.
- **Code lifecycle:** default code length 6 digits, default expiry 10 minutes, both configurable per Service. Twilio generates and validates — you never handle plaintext codes.
- **Auth:** HTTP Basic with Account SID as username and Auth Token as password, or a Standard/Main API Key SID + Secret. Never ship the Auth Token to a client — Verify calls are server-side only.
- **Anti-fraud:** Fraud Guard defends against SMS Pumping (artificially inflated traffic); Verify also exposes rate limits and geo-permission controls. Watch for 429 responses and 60xxx error codes.
- **Compliance:** OTP/2FA messages are transactional under the US TCPA when the number was supplied by the user for authentication; do not send marketing over the same intent. For EU/other regions honor local consent and A2P 10DLC registration requirements on the underlying US long-code/short-code sender.
