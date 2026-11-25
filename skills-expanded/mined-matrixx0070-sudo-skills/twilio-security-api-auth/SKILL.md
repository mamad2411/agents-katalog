---
name: twilio-security-api-auth
version: 1.0.0
description: Secure Twilio API authentication — prefer scoped API Keys over the Auth Token, rotate credentials, isolate subaccounts, enable Public Key Client Validation, and keep secrets off the client.
author: matrixx0070
tags: [twilio, security, api-keys, auth-token, authentication, subaccounts]
capabilities: []
---

## When to use

Use this when you are wiring an application to the Twilio REST API and deciding how it authenticates, or when you are auditing existing credential usage. Use it when you need to rotate a leaked credential, separate credentials per environment or tenant, or add request signing for high-assurance calls. This covers authenticating *to* Twilio; it is the credential half of Twilio security.

**Not for:** validating that inbound webhooks genuinely came from Twilio and full transport/rate-limit hardening (see `twilio-security-hardening`), or HIPAA/BAA obligations (see `twilio-security-compliance-hipaa`).

## Method

1. Default to API Keys, not the Auth Token, for application access. The Account Auth Token is the master credential — if it leaks, everything is exposed and rotating it breaks every integration at once. API Keys are independently revocable.
2. Decision point: choose the key type. Use a **Standard** API Key for most REST calls; use a **Main** key only when you specifically need to manage other keys/subaccounts. Never mint more privilege than the app uses.
3. Create one API Key per application/environment (dev, staging, prod) so you can revoke a single blast radius without touching the others. Capture the Secret at creation — Twilio shows it exactly once.
4. Isolate tenants and environments with subaccounts. Each subaccount has its own SID/credentials and its own resources; a compromise in one does not reach another, and billing/usage stays separated.
5. Rotate on a schedule and immediately on any exposure: create the new key, deploy it, verify traffic flows on it, then delete the old key. Never rotate the Auth Token as your only credential strategy — it is a single choke point.
6. For high-assurance flows, enable Public Key Client Validation: you sign each request with your private key and upload the public key to Twilio, so Twilio verifies the request signature (`x-twilio-signature` request signing) in addition to Basic Auth. Use where credential replay is a real threat.
7. Use product OAuth where offered (some newer Twilio products and organization-level admin support OAuth 2.0 tokens) rather than long-lived static secrets.
8. Never embed Account SID + Auth Token or API secrets in client-side code, mobile apps, or public repos. Client apps should call your backend, or use short-lived Access Tokens (as with Twilio Video/Voice SDKs) minted server-side.

## Example

```bash
# Create a Standard API Key (returns the secret ONCE)
curl -sX POST "https://api.twilio.com/2010-04-01/Accounts/$ACCOUNT_SID/Keys.json" \
  -u "$ACCOUNT_SID:$AUTH_TOKEN" \
  --data-urlencode "FriendlyName=orders-service-prod"
# -> { "sid": "SK...", "secret": "shown once — store now" }

# Authenticate subsequent calls with the API Key SID + Secret, not the Auth Token
curl -sX GET "https://api.twilio.com/2010-04-01/Accounts/$ACCOUNT_SID/Messages.json?PageSize=1" \
  -u "$TWILIO_API_KEY_SID:$TWILIO_API_KEY_SECRET"

# Rotate: create new -> deploy -> verify -> delete old
curl -sX DELETE "https://api.twilio.com/2010-04-01/Accounts/$ACCOUNT_SID/Keys/$OLD_SK.json" \
  -u "$ACCOUNT_SID:$AUTH_TOKEN"
```

For SDKs, mint a short-lived Access Token server-side rather than shipping account credentials to the device.

## Pitfalls

- **Using the Auth Token as the app credential.** It is the master key; a leak exposes the whole account and rotation breaks every integration simultaneously. Use per-app API Keys.
- **One key for everything.** A single shared key means revoking it takes down all environments. One key per app/environment keeps blast radius small.
- **Losing the secret.** The API Key Secret and Auth Token full value are shown once. Capture into a secret manager at creation; you cannot retrieve them later.
- **Credentials on the client.** Account SID/Auth Token or API secrets in a mobile app or SPA are extractable. Use a backend proxy or server-minted short-lived Access Tokens.
- **No subaccount isolation for multi-tenant.** Sharing one account across tenants means one breach touches all. Use subaccounts for per-tenant SID/credentials and resource isolation.
- **Rotate-in-place with downtime.** Deleting the old key before the new one is deployed and verified causes an outage. Overlap: create, deploy, verify, then delete.

## Output format

```
# Twilio API Auth Posture: <app/env>
CREDENTIAL: type=<api-key(standard)|api-key(main)|auth-token> sid=<SK...>
SCOPE: per-app=<yes|no> per-env=<dev|staging|prod> subaccount=<AC.../none>
ROTATION: last=<date> cadence=<n days> on-exposure=documented
CLIENT-SIDE: secrets-embedded=no access-tokens=server-minted
SIGNING: public-key-client-validation=<on|off> oauth=<where available>
STORAGE: secret-manager=<ref> shown-once-captured=yes
GAPS: [...]
```

## Reference

- Auth: Twilio REST API uses HTTPS Basic Auth. Credentials are either Account SID + Auth Token, or an API Key SID (`SK...`) + Secret. The API Key SID goes in the username, secret in the password.
- API Key types: **Standard** (REST resource access, cannot manage keys/subaccounts) and **Main** (can create/manage other keys and subaccounts). Endpoint: `/2010-04-01/Accounts/{AccountSid}/Keys.json`.
- The Auth Token is the account master secret; API Keys are independently revocable and are the recommended credential for applications. Both the Auth Token and each API Key Secret are displayed only once.
- Subaccounts (`AC...`) provide isolated SIDs, credentials, resources, and billing — used for per-tenant/per-environment separation.
- Public Key Client Validation: you generate a key pair, upload the public key to Twilio, and sign requests with your private key; Twilio validates the signature in addition to credentials, mitigating credential replay.
- SDK products (Voice, Video, Conversations) authenticate devices with short-lived Access Tokens minted by your server, never with account credentials on the client. OAuth 2.0 is available for some newer products and organization-level administration.
