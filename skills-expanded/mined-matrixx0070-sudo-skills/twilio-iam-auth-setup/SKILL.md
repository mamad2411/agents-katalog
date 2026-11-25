---
name: twilio-iam-auth-setup
version: 1.0.0
description: Set up secure Twilio authentication with API Keys, least-privilege access, secret storage, and safe Auth Token rotation.
author: matrixx0070
tags: [twilio, iam, api-keys, auth-token, secrets, security]
capabilities: []
---

## When to use

Use this when you are wiring an application to the Twilio REST API and need credentials that are safe to deploy — not the raw Auth Token pasted into code. Reach for it when standing up a new environment (dev/staging/prod), when a leaked credential must be revoked, or when a scheduled rotation is due. Use it any time "how do we authenticate to Twilio without risking the master key" is the open question.

**Not for:** federating multiple accounts under one identity plane with SSO — that is `twilio-organizations-setup`. Not for choosing a sender type or provisioning phone numbers — that is `twilio-numbers-senders`. This skill is purely about credentials and their lifecycle.

## Method

1. Inventory what authenticates today: every service, its credential, and whether it uses the raw Auth Token. Decision point: any code holding the Auth Token directly is a rotation hazard — plan to move it to an API Key.
2. Create an **API Key** per service/environment in the Console or via the API. Choose **Standard** for normal REST access; reserve **Main** keys (which can manage other keys) for tooling that provisions keys. Capture the **SID** (`SK...`) and the **Secret** — the secret is shown once.
3. Store secrets in a manager (Vault, AWS/GCP Secrets Manager, Doppler), never in git, never in client-side code. Inject via environment variables at runtime.
4. Separate environments: distinct API Keys (and ideally distinct subaccounts) for dev/staging/prod so a compromised dev key cannot touch prod traffic.
5. Authenticate REST calls as `Account SID` (or subaccount SID) as username and the **API Key Secret** as password — HTTP Basic. Decision point: for subaccount resources, use the subaccount SID, not the API Key SID, as the account context.
6. Enable **Public Key Client Validation** for high-assurance callers: upload your RSA public key, sign requests, and Twilio verifies the signature — eliminating a shared secret over the wire.
7. Rotate on a schedule and on any suspected leak. For API Keys: create the new key, deploy it, then delete the old key. For the **Auth Token**: use the **secondary Auth Token** — promote secondary to primary, update consumers, then regenerate the secondary.
8. Validate inbound Twilio webhooks separately by checking the **X-Twilio-Signature** header (HMAC-SHA1 over the URL + params, keyed by your Auth Token) — this is verification, not outbound auth.

## Example

```javascript
// REST auth via API Key: username = Account SID, password = API Key SECRET.
const twilio = require('twilio');
const client = twilio(process.env.TWILIO_API_KEY_SID, process.env.TWILIO_API_KEY_SECRET, {
  accountSid: process.env.TWILIO_ACCOUNT_SID, // AC... (or subaccount AC...)
});

// Create an API Key programmatically (requires a Main key or Auth Token).
const key = await client.newKeys.create({ friendlyName: 'prod-sms-sender' });
console.log(key.sid /* SK... */, key.secret /* shown ONCE — store now */);
```

```bash
# Validate an inbound webhook signature (HMAC-SHA1, base64) before trusting it.
# Twilio computes: base64(HMAC-SHA1(AuthToken, fullURL + sortedPOSTparams))
# Compare against the X-Twilio-Signature request header.
```

## Pitfalls

- **Auth Token in application code.** The Auth Token can do everything and is painful to rotate. Use per-service API Keys so revoking one key doesn't break the whole account.
- **Secret captured too late.** The API Key Secret is displayed exactly once at creation. If you didn't store it, you must delete and recreate the key.
- **Rotating the Auth Token with no secondary.** Regenerating the primary Auth Token instantly breaks every consumer. Promote the **secondary** token first, migrate, then regenerate.
- **Skipping webhook signature validation.** Without X-Twilio-Signature checks, anyone can POST forged callbacks to your endpoint. Validate every inbound request keyed by the Auth Token.
- **One key across all environments.** A leaked dev key then reaches prod. Isolate keys (and subaccounts) per environment.
- **Signature URL mismatch.** Behind a proxy/load balancer the reconstructed URL must match exactly what Twilio called (scheme, host, path, query) or HMAC verification fails.

## Output format

```
# Twilio Auth Setup
ACCOUNT_SID: AC********************************
API KEYS:
- SK******************************** | env=<dev|staging|prod> | type=<Standard|Main> | service=<name>
SECRET STORAGE: <Vault|AWS SM|Doppler|...>
PUBLIC KEY CLIENT VALIDATION: <on/off>
AUTH TOKEN ROTATION: primary=<set> secondary=<set> next_rotation=<date>
WEBHOOK VALIDATION: X-Twilio-Signature=<enforced/not>
```

## Reference

- **Account SID** = `AC...`; **API Key SID** = `SK...`. REST Basic auth: username = Account/Subaccount SID, password = API Key **Secret** (secret shown once at creation).
- **API Key types:** *Standard* (access resources) and *Main* (also create/manage other API Keys). Prefer Standard for app services.
- **Auth Token rotation** uses a **primary + secondary** token pair so you can migrate consumers with zero downtime before regenerating.
- **Public Key Client Validation** replaces the shared secret with request signing using your uploaded RSA public key — strongest option for sensitive integrations.
- **Webhook authenticity:** Twilio signs inbound requests with **X-Twilio-Signature**, an **HMAC-SHA1** (base64-encoded) of the full request URL plus alphabetically-sorted POST parameters, keyed by your **Auth Token**. The `twilio` SDK exposes `validateRequest()` / `webhook()` middleware for this.
- Never commit secrets; inject via environment variables and rotate on any suspected exposure (e.g., a token that hit CI/pm2 logs).
