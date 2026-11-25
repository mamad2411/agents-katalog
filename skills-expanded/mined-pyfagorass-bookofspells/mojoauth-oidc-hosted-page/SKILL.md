---
name: mojoauth-oidc-hosted-page
description: Implement OIDC authentication using the MojoAuth Hosted Login Page — covers client configuration, user redirect, and callback token validation.
---

# Implement MojoAuth OIDC Hosted Page

This skill guides you through implementing the OIDC Authorization Code flow with MojoAuth's Hosted Login Page. MojoAuth provides passwordless authentication (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through a single hosted page — no need to build a login UI from scratch.

## 1. Prerequisites
- **Client ID**: From the MojoAuth Dashboard.
- **Client Secret**: From the MojoAuth Dashboard (store securely!).
- **Redirect URI**: Must be whitelisted in the MojoAuth Dashboard (e.g., `http://localhost:3000/callback`).
- **MojoAuth Domain**: Your application's MojoAuth domain (e.g., `https://your-app.mojoauth.com`).

## 2. Key OIDC Endpoints

All endpoints are relative to your MojoAuth domain (`https://your-app.mojoauth.com`):

| Endpoint | URL |
| :--- | :--- |
| **Discovery** | `/.well-known/openid-configuration` |
| **Authorization** | `/oauth/authorize` |
| **Token** | `/oauth2/token` |
| **UserInfo** | `/oauth/userinfo` |
| **JWKS** | `/.well-known/jwks.json` |

## 3. Implementation Steps

### Step 1: Configure OIDC Client
Initialize your OIDC client with the credentials above. Use a well-maintained OIDC library for your language. The discovery endpoint will auto-configure all URLs.

### Step 2: Redirect to MojoAuth Hosted Login Page
Construct the authorization URL and redirect the user. MojoAuth's Hosted Login Page handles all authentication methods (passwordless email, OTP, social login, passkeys).
- **Endpoint**: `/oauth/authorize`
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

## 4. Authentication Flow

```
User clicks "Sign In"
        │
        ▼
Redirect to MojoAuth Hosted Login Page
(https://your-app.mojoauth.com/oauth/authorize)
        │
        ▼
User authenticates via passwordless method
(Magic Link, OTP, Social Login, Passkeys)
        │
        ▼
MojoAuth redirects back with authorization code
        │
        ▼
Your server exchanges code for tokens
(POST /oauth2/token)
        │
        ▼
Verify ID token & create session
```

## 5. Examples
Refer to the platform-specific skill files for complete implementations:
- **Next.js**: [oidc-hosted-page-nextjs](../oidc-hosted-page-nextjs/SKILL.md)
- **Node.js**: [oidc-hosted-page-node](../oidc-hosted-page-node/SKILL.md)
- **Python**: [oidc-hosted-page-python](../oidc-hosted-page-python/SKILL.md)
- **Go**: [oidc-hosted-page-go](../oidc-hosted-page-go/SKILL.md)
- **React**: [oidc-hosted-page-react](../oidc-hosted-page-react/SKILL.md)
- **Angular**: [oidc-hosted-page-angular](../oidc-hosted-page-angular/SKILL.md)
