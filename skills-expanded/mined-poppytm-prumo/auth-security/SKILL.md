---
name: auth-security
description: OAuth2.1, PKCE, Argon2id password hashing, token lifecycle, session revocation, MFA, and brute-force prevention
---
# Authentication & Authorization Security

## 1. Zero Trust & Secure Authentication Flows
Implement PKCE for OAuth 2.1 authorization code flows. Mandate cryptographically random state and nonce parameters to prevent authorization injection. Reject HTTP redirects to unverified origins. Require authentication at every API boundary rather than trusting network perimeters.

## 2. Modern Password Hashing
Use Argon2id as the default password hashing algorithm (minimum memory 64MB, time cost 3, parallelism 4). For legacy compatibility, use bcrypt with work factor >= 12. Never use MD5, SHA1, or raw SHA256 for password storage. Enforce password complexity via entropy checks rather than restrictive character set rules.

## 3. Ephemeral Token Lifecycle
Keep JWT access tokens short-lived (maximum 15 minutes). Implement secure refresh token rotation where the previous refresh token is invalidated upon single use. If an invalidated refresh token is reused, treat it as token theft and immediately revoke all refresh tokens associated with that family/session.

## 4. Session Invalidation & State Revocation
Maintain a server-side session revocation denylist (e.g. Redis bloom filter or distributed cache) for rapid token invalidation. On password change or account compromise, revoke all active sessions immediately. Support global sign-out across all client devices.

## 5. Multi-Factor Authentication (MFA)
Implement TOTP (RFC 6238) with SHA-1/SHA-256 and 30-second time steps. Provide single-use cryptographically random backup codes hashed in storage. Support WebAuthn / FIDO2 passkeys for phishing-resistant authentication.

## 6. Brute Force Prevention & Adaptive Rate Limiting
Enforce progressive rate limiting using a leaky bucket algorithm on all login and password reset endpoints. Apply per-IP limits and per-account limits. Escalate with exponential delays or CAPTCHA after 5 failed attempts within 10 minutes.

## 7. Secure Account Recovery
Generate single-use, time-limited (max 30 minutes) recovery tokens using HMAC-SHA256. Send recovery links strictly to verified primary contact channels. Never reveal whether an email or username exists in recovery response messages (prevent account enumeration).

## 8. SSO & Federated Identity
Enforce strict OIDC validation: verify JWT signature, issuer (iss), audience (aud), expiration (exp), and not-before (nbf) claims. Enforce clock skew tolerance of at most 60 seconds. Require PKCE on federated broker handshakes.

## 9. Minimal Scopes & Granular Claims
Adhere to the Principle of Least Privilege: issue tokens with the minimal scopes required for the specific client operation. Validate scope claims on every protected endpoint before granting access. Separate administrative capabilities into dedicated, re-authenticated scopes.

## 10. Audit Logging & Security Event Tracing
Record structured security audit logs for all authentication events: LOGIN_SUCCESS, LOGIN_FAIL, TOKEN_ISSUED, TOKEN_REVOKED, PASSWORD_RESET_REQUEST, and MFA_FAILED. Include timestamp, actor ID, client IP, user agent, and correlation ID. Never write credentials or tokens to logs.
