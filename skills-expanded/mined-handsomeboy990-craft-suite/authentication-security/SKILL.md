---
name: authentication-security
description: Builds and audits how a system establishes who a user is: password storage and policy, login flow and its rate limits, credential recovery, multi-factor, token issuance and lifetime, account enumeration, and the difference between authentication and authorization. Covers the flows attackers target first. Use when building or reviewing login, signup, password reset, session issuance or any identity establishment.
license: MIT
metadata:
  category: secure-development
  version: 1.0.0
  depends_on: [security-core]
  outputs: [auth-findings, auth-design, credential-policy, applied-fixes]
---

# Authentication Security

Authentication establishes who a user is. Everything else in a system trusts
that answer, which is why the login, the reset and the token flows are the first
things an attacker probes. This skill builds those flows correctly and audits
the ones that exist.

Authentication is not authorization. This skill answers who you are.
`authorization-design` answers what you may do. Confusing them produces a system
that checks the door and leaves every room unlocked.

## 1. Password storage

If passwords are stored, they are stored one way only.

```
algorithm   a memory-hard password hash: argon2id, scrypt, or bcrypt
            never a general hash (SHA-256, MD5), never encryption, never plaintext
parameters  tuned so a single hash costs meaningful time on current hardware,
            reviewed as hardware improves
salt        unique per password, stored with the hash; the algorithm handles it
pepper      optional, from the secret store, never in the database
verify      constant-time comparison; the library does this, do not hand-roll it
```

A password reset re-hashes. A hash found using a general-purpose algorithm is a
critical finding, because the whole credential table is one leak from cracked.

## 2. The login flow

```
rate limit      per account and per source, so credential stuffing is not free;
                a lockout or a backoff, with the tradeoff against denial of service
                considered and decided
no enumeration  the same response and timing whether the account exists or not;
                "invalid email or password", never "no such user"
generic errors  the login never reveals which half was wrong
timing          the not-found path does the same work as the found path, so
                response time does not leak account existence
credential check   against the stored hash, constant-time, always
```

## 3. Multi-factor

```
when        for any account whose compromise is expensive; always offerable,
            enforced where the assets justify it
factor      TOTP or a hardware key over SMS, which is interceptable; SMS is
            better than nothing and worse than an authenticator
recovery    backup codes, generated once, stored hashed, shown once
enrolment   re-authenticate before enabling or disabling a factor
verify      the second factor is checked server side, on every login, not
            skippable by replaying a "remember me" that predates it
```

## 4. Credential recovery

The reset flow is a second authentication path, and it is attacked as one.

```
token       single-use, time-limited, high-entropy, tied to the account, stored
            hashed; invalidated on use and on a new request
delivery    to the registered channel only; the reset link is the credential
no enumeration   the flow says "if that account exists, a link was sent",
            the same for every input
post-reset  every existing session and token for the account is invalidated
rate limit  the request endpoint is limited, so it is not a spam or timing oracle
```

## 5. Token issuance and lifetime

```
issue       a token that identifies the session, verifiable server side
lifetime    short for access, longer for refresh; both revocable
storage     the client stores it where script cannot read it when possible;
            an HttpOnly cookie over a token in local storage for a web app
revocation  logout, password change and reset invalidate tokens server side;
            a token whose only expiry is its own clock cannot be revoked
contents    a token carries identity, never a secret and never a trusted role
            the client could read and the server re-trusts
```

## 6. What authentication must never do

```
never   store or log a password, a reset token or a session token in plaintext
never   return whether an account exists, at login, signup or reset
never   trust a client-supplied identity, role or "isAdmin" field
never   accept a token the server cannot revoke
never   use a general-purpose hash for a password
never   roll a custom crypto primitive where a vetted library exists
never   let the reset flow skip the invalidation of existing sessions
```

## 7. Prohibitions

- Never conflate authentication with authorization; this skill only establishes
  identity, and it never grants a capability.
- Never leak account existence through response text, status or timing.
- Never store a credential recoverable to plaintext.
- Never issue a token that cannot be revoked before its expiry.
- Never implement the crypto by hand when a maintained library exists.
- Never leave existing sessions alive after a password reset.

## 8. Protocol

1. Establish whether this is a build or an audit, and the scope.
2. Verify password storage: algorithm, parameters, salting, comparison.
3. Walk the login flow: rate limit, enumeration, generic errors, timing.
4. Check recovery: token properties, delivery, enumeration, post-reset
   invalidation.
5. Check multi-factor: factor strength, server-side verification, recovery.
6. Check tokens: lifetime, storage, revocation, contents.
7. Rank every finding on the `security-core` scale; fix what code fixes and
   verify each fix with its reproduction.
8. Hand rotation and infrastructure actions to the manual list.

## 9. Auto-critique

Score from 0 to 5: password storage uses a vetted memory-hard hash, login is
rate-limited and non-enumerable in text and timing, recovery is single-use and
invalidates sessions, multi-factor is verified server side, tokens are revocable
and stored safely, authentication is kept distinct from authorization, every fix
verified.

Threshold: no axis below 3, average at least 4. A general-purpose password hash,
an enumerable login, or an unrevocable token is a critical finding and caps the
score until fixed.

## 10. Interfaces

- Upstream: `security-core`, `security-architecture` for how identity
  propagates, `authentication-security` implements the establishment.
- Downstream: `session-security` owns the session lifecycle after login,
  `authorization-design` owns what the authenticated identity may do,
  `security-audit` verifies these controls in the code.
- Lateral: `secrets-management` for the pepper and signing keys,
  `input-validation` for the credential inputs, `data-privacy` for the personal
  data in an account.
