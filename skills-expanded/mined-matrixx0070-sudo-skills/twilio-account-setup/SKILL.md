---
name: twilio-account-setup
version: 1.0.0
description: Stand up a Twilio account from scratch — credentials, verified caller ID, buying a number, subaccounts, geo permissions, trial-to-upgrade, and billing basics.
author: matrixx0070
tags: [twilio, setup, onboarding, phone-numbers, billing, credentials]
capabilities: []
---

## When to use

Use this when you're getting a Twilio project off the ground: creating the account, finding your Account SID and Auth Token, provisioning a phone number, isolating environments with subaccounts, unlocking international destinations, or understanding what a trial account can and can't do before you go live. Reach for it whenever the blocker is "the account/number isn't set up yet," not the messaging or call logic.

**Not for:** sending OTP (twilio-verify-send-otp), number intelligence (twilio-lookup-phone-intelligence), IVR/messaging flows (twilio-studio-flows), or agent routing (twilio-taskrouter-routing). This skill gets you to the point where those can run.

## Method

1. **Create the account and locate credentials.** After signup, the Console home shows the **Account SID** (`AC...`) and the **Auth Token**. These authenticate every API call. Decision point: for production, immediately create an API Key (SID `SK...` + Secret) so you can rotate/revoke without changing the Auth Token, and treat the Auth Token as break-glass.
2. **Understand trial constraints.** A trial account has a small credit, can only send messages/calls to **verified** numbers, and prepends a trial watermark. Decision point: if you need to reach arbitrary numbers or remove the watermark, upgrade (add a payment method) before further setup.
3. **Verify a caller ID / recipient.** On trial, add and verify each destination or outbound caller ID via Verified Caller IDs (a code confirms control). Skip once upgraded (except when using a personal number as caller ID).
4. **Set geographic permissions.** Enable the countries/regions you'll message or call under Messaging/Voice Geo Permissions. Decision point: leave high-risk destinations disabled to limit toll fraud exposure.
5. **Buy a phone number.** Search available numbers by country, area code, and capability (SMS/MMS/Voice/Fax), then purchase. Decision point: match capabilities to use case (SMS-only vs voice), and for US A2P messaging plan for 10DLC brand/campaign registration.
6. **Structure with subaccounts.** For multi-tenant or env separation (dev/stage/prod, or per-customer), create Subaccounts under the main (parent) account — each has its own SID/Auth Token and isolated usage/billing, while the parent consolidates billing.
7. **Configure billing and alerts.** Add a payment method, set auto-recharge, and configure Usage Triggers / billing alerts so spend doesn't surprise you.
8. **Secure and verify.** Store credentials in secrets (never in client code or git), enable 2FA on the Console login, then confirm setup by sending one message/call from the new number.

## Example

```bash
# Verify credentials work: fetch your account
curl "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID.json" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"

# Search available US numbers with SMS + Voice in area code 415
curl "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/AvailablePhoneNumbers/US/Local.json?AreaCode=415&SmsEnabled=true&VoiceEnabled=true" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"

# Buy a specific number
curl -X POST "https://api.twilio.com/2010-04-01/Accounts/$TWILIO_ACCOUNT_SID/IncomingPhoneNumbers.json" \
  --data-urlencode "PhoneNumber=+14155550123" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"

# Create a subaccount for an isolated environment
curl -X POST "https://api.twilio.com/2010-04-01/Accounts.json" \
  --data-urlencode "FriendlyName=prod-tenant-acme" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

```javascript
// Prefer an API Key over the Auth Token for app auth
const client = require('twilio')(apiKeySid, apiKeySecret, { accountSid });
```

## Pitfalls

- **Shipping the Auth Token.** Never embed the Auth Token (or Account SID as a secret) in client-side or committed code. Use API Keys for apps and rotate them; keep the Auth Token as break-glass.
- **Trial "silent" failures.** On trial you can only reach verified numbers and messages carry a watermark — a send to an unverified number fails. Upgrade or verify the destination first.
- **Geo permissions off by default for many regions.** International sends/calls fail until you enable the destination country. Enable only what you need to limit toll fraud.
- **Buying the wrong number capability.** An SMS-only number can't take voice, and US A2P messaging needs 10DLC brand + campaign registration — provision and register for the actual use case.
- **Subaccount credential confusion.** Each subaccount has its own SID + Auth Token; calling with the parent's credentials against a subaccount resource fails or misroutes. Use the correct SID per environment.
- **No billing guardrails.** Without auto-recharge and Usage Triggers, you either run dry mid-campaign or overspend on fraud. Set both.

## Output format

```
TWILIO ACCOUNT SETUP
  account_sid: AC******** (stored in secrets)
  auth: <API Key SK... in use | Auth Token break-glass>
  status: <trial | upgraded>
  verified_caller_ids: <list, if trial>
  geo_permissions: <enabled countries>
  numbers:
    - <E.164> caps:<SMS/MMS/Voice> a2p_registered:<yes/no>
  subaccounts: <friendly names / SIDs, if any>
  billing: <payment method set, auto-recharge, usage triggers>
  verified_live: <test send/call succeeded? yes/no>
```

## Reference

- **Credentials:** **Account SID** (`AC...`) + **Auth Token** are the master credential pair, shown on the Console dashboard. **API Keys** (`SK...` SID + Secret) are the recommended app credential — scoped, rotatable, revocable without disturbing the Auth Token. Auth is HTTP Basic (`SID:secret`).
- **Trial vs upgraded:** trial = limited promo credit, sends only to Verified Caller IDs, trial watermark on messages, some features gated. Upgrading = add a payment method; removes verified-only restriction and watermark, unlocks number purchasing at scale.
- **Verified Caller IDs:** on trial you verify each outbound caller ID / destination via a confirmation code; also used to register a personal number as an outbound caller ID.
- **Phone numbers:** search `AvailablePhoneNumbers/{Country}/Local|Mobile|TollFree` by area code and capability; purchase creates an `IncomingPhoneNumbers` resource. Number types and regulatory requirements (address/bundle for some countries) vary by geography.
- **Subaccounts:** child `Accounts` under the parent for isolation (per-tenant / per-environment); each has its own SID + Auth Token, isolated usage and API scope, with consolidated billing at the parent. Common pattern for multi-tenant apps.
- **Geo permissions:** Messaging and Voice Geo Permissions in the Console gate which countries you can reach — a primary toll-fraud control.
- **Compliance to plan for:** US A2P 10DLC brand + campaign registration for application-to-person SMS on long codes; TCPA consent and STOP/HELP opt-out handling; number regulatory bundles for certain countries. Enable 2FA on the Console and store all secrets outside source control.
