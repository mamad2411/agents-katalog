---
name: session-security
description: Owns the session lifecycle after login: how the session is represented and stored, cookie attributes, fixation and rotation, idle and absolute timeout, concurrent sessions, revocation on password change and logout, and defence against CSRF and session theft. The bridge between a correct login and a correctly protected request. Use when building or reviewing sessions, cookies, remember-me, or logout.
license: MIT
metadata:
  category: secure-development
  version: 1.0.0
  depends_on: [security-core]
  outputs: [session-findings, session-design, cookie-policy, applied-fixes]
---

# Session Security

Authentication proves who a user is once. A session carries that proof across
every subsequent request. Between the correct login and the protected
operation, the session is what an attacker steals, fixes or replays, and this
skill owns that span.

## 1. What the session is, and where it lives

```
identifier   a high-entropy, unguessable session id, or a signed token the
             server can verify and revoke
server state   for stateful sessions, the record the id points to: user,
             issued time, last-seen, expiry, revoked flag
storage        server-side session store, or a signed token whose revocation
               list the server keeps; never trust the client's copy of the
               user's role or permissions
client side    the id or token in an HttpOnly cookie, unreadable by script
```

A session whose only representation is a self-contained token with no
server-side revocation cannot be logged out before it expires. Decide
revocation before choosing the representation.

## 2. Cookie attributes

A session cookie carries a fixed set of attributes. Each closes a specific
attack.

```
HttpOnly    script cannot read it -> an XSS cannot steal the session cookie
Secure      sent over HTTPS only -> not exposed on a downgraded connection
SameSite    Lax or Strict -> the cookie is not sent on a cross-site request,
            which closes most CSRF at the transport layer
Path/Domain scoped as narrowly as the app allows -> not shared with siblings
Max-Age     bounded -> the cookie does not outlive the session it names
__Host-     prefix where applicable -> binds the cookie to the exact host
```

A session cookie missing HttpOnly or Secure is a finding. Missing SameSite
raises the CSRF requirement in section 5.

## 3. Fixation and rotation

```
on login     issue a new session id; never keep the id the user arrived with,
             which an attacker may have set (session fixation)
on privilege change   rotate the id when the user authenticates a second factor
             or elevates, so a pre-elevation id cannot ride the new privilege
never        accept a session id supplied in a URL or a request the server did
             not issue
```

## 4. Timeout and concurrency

```
idle timeout      the session expires after inactivity; the window matches the
                  asset, minutes for a bank, longer for a forum
absolute timeout  the session expires at a fixed age regardless of activity, so
                  a stolen long-lived session has a ceiling
remember-me       a separate, revocable, long-lived token, not an extended
                  session; it re-establishes a fresh session, it is not one
concurrent        decide whether multiple sessions are allowed; if the asset
                  justifies it, show them to the user and allow revoking one
```

## 5. CSRF

If the session is carried in a cookie the browser attaches automatically, a
cross-site request rides it unless defended.

```
SameSite     Lax or Strict on the session cookie closes most of it
token        a per-session or per-request anti-CSRF token on state-changing
             requests, verified server side, for defence in depth and for the
             cases SameSite does not cover
check        state-changing operations are POST/PUT/PATCH/DELETE, never GET;
             a GET must never change state, so a cross-site image cannot trigger it
origin       verify the Origin or Referer on sensitive state changes
```

An API authenticated by a bearer token in a header, not a cookie, is not
CSRF-exposed in the same way; state the auth model before deciding the defence.

## 6. Revocation

```
logout            invalidates the session server side, not only the client cookie
password change   invalidates every session for the account
password reset     the same, per authentication-security
compromise        an administrator can revoke a user's sessions
mechanism         a self-contained token needs a server-side revocation list or
                  a short lifetime, or logout is a lie
```

## 7. Prohibitions

- Never store a session id or token in a place script can read when a cookie
  with HttpOnly is possible.
- Never keep the session id a user arrived with across a login.
- Never issue a session cookie without HttpOnly and Secure.
- Never let a GET request change state.
- Never make logout a client-only action for a token the server cannot revoke.
- Never treat remember-me as an indefinitely extended session.
- Never accept a session identifier from a URL.

## 8. Protocol

1. Establish the session representation and whether the server can revoke it.
2. Set the cookie attributes: HttpOnly, Secure, SameSite, scope, Max-Age.
3. Rotate the id on login and on privilege elevation; reject supplied ids.
4. Set idle and absolute timeouts to the asset; design remember-me separately.
5. Decide the CSRF defence from the auth model: SameSite plus a token for
   cookie-based sessions.
6. Implement revocation on logout, password change, reset and by an admin.
7. Rank findings on the `security-core` scale; fix and verify each.
8. Hand any infrastructure action (a shared session store, TLS config) over.

## 9. Auto-critique

Score from 0 to 5: session id high-entropy and server-revocable, cookie carries
HttpOnly/Secure/SameSite, id rotates on login and elevation, idle and absolute
timeouts set to the asset, CSRF defended for the actual auth model, logout and
password change revoke server side, remember-me is a separate revocable token.

Threshold: no axis below 3, average at least 4. A session cookie without
HttpOnly, or a logout that does not revoke server side, caps the score until
fixed.

## 10. Interfaces

- Upstream: `security-core`, `authentication-security` issues the identity this
  skill carries, `security-architecture` for how identity propagates.
- Downstream: `authorization-design` reads the session's identity to decide
  access, `security-audit` verifies cookie attributes and revocation,
  `security-headers` sets the transport protections around it.
- Lateral: `secrets-management` for the signing key, `caching-strategy` when the
  session store is a shared cache.
