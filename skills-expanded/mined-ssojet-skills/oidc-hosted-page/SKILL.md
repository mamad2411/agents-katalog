---
name: oidc-hosted-page
description: Implement OIDC authentication using the SSOJet Hosted Login Page — covers client configuration, user redirect, and callback token validation.
---

# Implement SSOJet OIDC Hosted Page

This skill guides you through implementing the OIDC Authorization Code flow with SSOJet's Hosted Login Page.

## 1. Prerequisites
- **Client ID**: From the SSOJet Dashboard.
- **Client Secret**: From the SSOJet Dashboard (store securely!).
- **Redirect URI**: Must be whitelisted in the SSOJet Dashboard (e.g., `http://localhost:3000/callback`).
- **SSOJet Domain**: Your organization's SSOJet domain (e.g., `https://auth.ssojet.com`).

## 2. Implementation Steps

### Step 1: Configure OIDC Client
Initialize your OIDC client with the credentials above. Use a well-maintained OIDC library for your language.

### Step 2: Redirect to Login
Construct the authorization URL and redirect the user.
- **Endpoint**: `/oauth2/authorize`
- **Params**:
  - `response_type=code`
  - `client_id=YOUR_CLIENT_ID`
  - `redirect_uri=YOUR_REDIRECT_URI`
  - `scope=openid profile email`

### Step 3: Handle Callback
On the callback route (e.g., `/callback`):
1.  Extract the `code` parameter from the query string.
2.  Exchange the code for tokens at `/oauth2/token`.
3.  Verify the `id_token` signature using the JWKS endpoint (`/.well-known/jwks.json`).

## 3. Examples
Refer to the `examples/` directory for complete implementations:
- **Node.js**: [examples/nodejs/app.js](./examples/nodejs/app.js)
- **Python**: [examples/python/app.py](./examples/python/app.py)
- **Go**: [examples/go/main.go](./examples/go/main.go)
