---
name: auth-design
description: "Design or review how a system proves who a caller is and keeps that proof safe: whether to build identity at all, authorization code with PKCE per client type (the implicit and password grants are removed, not discouraged), exact-string redirect URI matching, state, nonce and PKCE, session id rotation on every privilege change, refresh token rotation with reuse detection, JWT algorithm, audience and issuer validation, password hashing and phishing-resistant MFA. Use whenever someone is designing or reviewing login, signup, SSO, logout or session handling, or asks \"should we use JWTs or sessions\", \"adding google login\", \"is our refresh token flow safe\", or \"how should we hash passwords\". Not for rotating a leaked credential (secret-rotation), reviewing who holds which grant (access-review), a diff security review (security-review), or endpoint shape and status codes (api-design)."
allowed-tools: "Read, Grep, Glob, Write, Edit, Bash(curl:*), Bash(jq:*), Bash(openssl:*), Bash(git:*)"
---

# Auth Design

A good authentication design is one where the worst outcome of a stolen artefact is bounded and short, and where every claim the application trusts was verified against a key the application chose.

Authentication is the part of a system where ordinary engineering judgement produces confidently wrong answers, because the defaults read as reasonable and the failures are silent. A token that is decoded but not verified works perfectly in every test. A session identifier that survives login works perfectly for every user who is not being attacked. A redirect URI matched by prefix works for every deployment except the one the attacker registers. None of these show up as a bug report; they show up as an account takeover, months later, discovered by somebody else. The other half of the difficulty is that the good answers are mostly *not yours to write* — the flows, the key handling and the rate limiting have been specified, attacked and revised for fifteen years, and the version you write this quarter starts at the beginning of that. So this skill spends its first gate on whether to build at all, and the rest on the decisions that remain even when you integrate.

This is design and verification work. Everything below describes how to build a system and how to test your own; none of it is tooling for getting into somebody else's.

## Scope

Use for: deciding whether to build or buy identity; choosing an OAuth 2.0 or OpenID Connect flow for a given client; designing login, signup, logout, SSO and step-up authentication; session and cookie design; access and refresh token handling, lifetimes and revocation; JWT validation rules; password storage and credential policy where you own the credential; multi-factor choice and account recovery; enumeration, throttling and lockout; reviewing any of the above before it ships.

Do not use for: rotating, revoking or containing a credential that already exists or has leaked, which is `secret-rotation`; reviewing who or what currently holds which grant and reducing it toward least privilege, which is `access-review`; a general security pass over a diff, which is `security-review`; the shape of an HTTP interface and its status codes, which is `api-design` — that skill maps 401 and 403, this one decides what makes a request authenticated in the first place. Use `authorization-design` to decide what an authenticated caller may do and where that decision is enforced.

## Hard gates

1. **Do not write the protocol.** Use an identity provider or a maintained library for issuance and validation. Writing your own token format, your own password hash, or your own OAuth server is the decision that produces the findings in every section below.
2. **Authorization code with PKCE, for every client type.** OAuth 2.1 omits both the implicit grant and the resource owner password credentials grant; RFC 9700 forbids the second outright and advises against the first — see step 2 for the exact strengths, which are worth quoting correctly.
3. **Redirect URIs are compared as exact strings.** No wildcards, no prefixes, no suffix checks.
4. **Rotate the session identifier on every privilege change, starting with login.** Session fixation is otherwise a two-step attack with no exotic prerequisites.
5. **Verify before you read.** A JWT's claims mean nothing until the signature is verified with a key you selected and an algorithm you allowlisted, and the `aud` and `iss` claims are checked. Decoding is not verification, and most libraries offer both.
6. **Every long-lived artefact is revocable, or short.** A stateless token cannot be withdrawn, so its lifetime *is* your revocation latency. Pick one property and design for it rather than assuming both.

## Workflow

### 1. Decide whether this should be your code at all

Answer this before anything else, and the honest answer is usually no.

| Situation | Build or integrate |
| --- | --- |
| A product that needs users to log in | Integrate. A hosted identity provider, or your framework's maintained authentication package with its defaults intact. |
| Enterprise customers asking for SAML or OIDC SSO | Integrate. The long tail of identity provider quirks is the entire cost here, and it is somebody's whole product. |
| Machine-to-machine inside one cloud account | Neither. Use workload identity federation and issue no credential at all. |
| You need a claim or a flow the provider does not support | Integrate, and add the claim at the edge. Wanting one custom claim is not a reason to own issuance. |
| Identity is the product you sell | Build, with a specialist, and expect it to be a permanent team rather than a project. |
| Air-gapped, or a jurisdiction that forbids the hosted options | Build on a maintained open-source server you operate — Keycloak-class — rather than on a library and a plan. |
| "We only need a login page" | Integrate. This is the sentence that precedes every hand-rolled session bug in this document. |

The arguments against integrating are usually cost, lock-in and a dislike of the dependency. Cost is real at scale and arrives as a monthly-active-user pricing cliff, so model it at your projected user count rather than today's. Lock-in is also real, and it has one concrete test that decides it: **ask the vendor, in writing and before signing, whether you can export password hashes and the user directory, and in what format.** A provider that will export bcrypt hashes leaves you a migration path; one that will only offer a "lazy migration" proxy has your user base. The dependency argument is the weak one — the dependency exists either way, and the alternative is a dependency on your own unmaintained code.

If you are building, read `references/credentials-and-recovery.md` before writing any of it, and treat every subsequent step here as a specification rather than a review checklist.

### 2. Choose the flow from the client type, not from taste

There is one default and a small number of genuine exceptions. The decision is made by what kind of client this is, and nothing else.

| Client | Flow | Notes |
| --- | --- | --- |
| Server-side web application | Authorization code with PKCE, confidential client | Tokens stay on the server. The browser gets a session cookie, never a token. |
| Single-page application | Authorization code with PKCE, public client | Better still, put a backend-for-frontend in front and give the browser a cookie. See step 3. |
| Native or mobile application | Authorization code with PKCE, in the system browser | `ASWebAuthenticationSession` or Custom Tabs. An embedded webview breaks SSO and passkeys, and the host application can read what is typed into it. RFC 8252, OAuth 2.0 for Native Apps (October 2017), is explicit about this. |
| Machine-to-machine | Client credentials | Prefer `private_key_jwt` or mutual TLS (RFC 8705, February 2020) over a shared client secret, and workload identity over both. |
| Television, console, CLI, device with no keyboard | Device authorization grant, RFC 8628 (August 2019) | The user authenticates on a second device; the first polls. |
| A first-party mobile app where "the login form should be ours" | Authorization code with PKCE anyway | The design pressure to take the password directly is where the password grant keeps being reinvented. |

Two flows are out of the current specification, and it is worth knowing exactly how strongly each is ruled out, because a design review will ask.

**The implicit grant** returned the access token in the URL fragment, which put it in browser history, in referrer headers under some conditions, and in anything that logged the URL, with no client authentication and no binding between the request and the response. It existed because cross-origin requests to the token endpoint were once impractical; that reason disappeared, and the exposure did not. **The resource owner password credentials grant** requires the application to handle the user's actual password, which defeats federation, prevents the identity provider from applying its own risk signals or MFA, and trains users that typing their identity provider password into a third-party form is normal. RFC 9700, the OAuth 2.0 Security Best Current Practice, grades the two differently and the difference is worth quoting correctly: §2.4 says the password grant MUST NOT be used, while §2.1.2 says clients SHOULD NOT use the implicit grant, with a narrow conditional exception. The OAuth 2.1 draft then omits both from the specification entirely. The recommendation is the same either way — do not propose either — but a design review is not the place to overstate a SHOULD NOT as a MUST NOT. Treat a design that proposes either as a defect with a named replacement, not a trade-off to weigh.

`references/flows-and-tokens.md` has the per-client detail, the parameters of a correct authorization request, and what to check when integrating with a specific provider.

### 3. Get the authorization request and the callback right

Three parameters do three different jobs. They are frequently described as redundant, and they are not.

| Parameter | Defends against | What it does not do |
| --- | --- | --- |
| `state` | Cross-site request forgery on the callback: an attacker causing the victim's browser to complete an authorization the victim did not begin, which ends with the victim logged into the attacker's account and typing real data into it. | Nothing about the code itself. A stolen code is unaffected. |
| `nonce` (OpenID Connect) | Replay of an ID token: it binds the token the identity provider issues to this specific authentication request, so a token captured elsewhere fails validation here. | Nothing about the access token or the code exchange. |
| PKCE, RFC 7636 (September 2015) | Interception or injection of the authorization code: the code is useless without the `code_verifier` held by the client instance that started the flow. | It carries no application state, and it binds to the client instance rather than to the user's browser session. |

Keep all three. PKCE does not replace `state` because the two bind different things — PKCE binds the code to a client instance, `state` binds the callback to the browser session that started it, and `state` is also where the return-to path lives. PKCE does not replace `nonce` because PKCE protects the exchange and `nonce` protects the token's freshness. Generate `state` and `nonce` as unguessable values, store them server-side or in the browser session, compare on return, and consume them once. A `state` value that is generated and never checked on return is the common version of this bug, and it looks identical from the outside to one that works.

Where the client talks to more than one identity provider, also validate the `iss` parameter on the authorization response (RFC 9207, March 2022), which is what stops a mix-up between providers.

**Redirect URIs are matched by exact string comparison.** RFC 9700 requires it. The exceptions are narrow and specified: a native application's loopback redirect may vary in port (RFC 8252), because the operating system assigns it.

What goes wrong otherwise:

- **Wildcard subdomains.** `https://*.example.com/callback` is only as strong as the weakest host in the zone, including the marketing site, an abandoned staging host, and anything pointing at a deprovisioned bucket that somebody else can claim.
- **Prefix matching.** `https://app.example.com/callback` registered as a prefix also accepts `https://app.example.com/callback.attacker.com` under a naive string check, and accepts path traversal or an appended path on any host that serves user content at a subpath.
- **A registered URI that is itself an open redirector.** Exact matching is satisfied, the provider is content, and the code is forwarded onward by your own application. Audit the registered endpoints for redirect behaviour, not only the registration list.
- **Preview deployments.** This is the real reason teams reach for wildcards. Register each preview host, or route previews through one stable callback host that redirects internally using a value bound to `state`.

Each of these ends the same way: an authorization code delivered to somewhere the attacker reads. PKCE limits the damage because the code cannot be redeemed without the verifier; do not use that as a reason to relax the matching, because the two controls fail in different circumstances.

### 4. Decide where the session actually lives

This is the "JWTs or sessions" question, and it has a default.

For a browser-facing application, **hold the tokens on the server and give the browser an opaque cookie-based session.** The reasons are concrete: a cookie can be `HttpOnly`, so script cannot read it; a server-side session is revocable in one write, so logout and "sign out everywhere" and incident response all work; and the browser never holds a bearer artefact that is useful somewhere else. For a single-page application this means a backend-for-frontend, which is a small proxy, not an architecture.

Choose a stateless token for browser-facing sessions only when you can say what you have bought and what it costs. The purchase is one fewer lookup per request; the cost is that the session cannot be revoked before it expires, and that the token has to be stored somewhere script can reach.

| | Server-side session, cookie | Stateless token in the browser |
| --- | --- | --- |
| Revocation | Immediate, one record | Not possible before expiry |
| Exposure to script injection | Cookie unreadable with `HttpOnly` | Readable in `localStorage`; in memory it survives less but is still reachable |
| Horizontal scale | Needs a shared session store | None needed |
| Logout everywhere | A query and a delete | A deny list, which is a session store with extra steps |

Service-to-service calls are the case where a self-contained token genuinely pays, because the verifier has no session store and no shared database, and lifetimes are minutes.

Step 5 and `references/sessions-and-cookies.md` cover the cookie decisions in detail; read that reference when writing the cookie code or diagnosing a cross-site behaviour.

### 5. Session handling

**Rotate the session identifier at every change of privilege.** That means on login, on step-up or re-authentication, on assuming another identity in an impersonation feature, and on dropping back out of it. The reason is session fixation: if an identifier issued before authentication is still valid after it, anyone who can cause the victim's browser to hold a known identifier — a link carrying one, an application that accepts a session id from a query parameter, a script on a sibling subdomain that can set the cookie — is holding an authenticated session the moment the victim logs in. Rotation costs one line and removes the class.

**Invalidate server-side on logout, on password change and on MFA changes.** Clearing the cookie logs out a cooperative browser; it does nothing to a copy. On a password change, terminate every other session for that user, because "my account was accessed" is exactly the moment the other sessions matter.

**Cookie attributes, and what each one is actually for:**

| Attribute | Why |
| --- | --- |
| `Secure` | Keeps the cookie off plaintext HTTP. Without it, one downgraded request — a hardcoded link, a captive portal, an old bookmark — sends the session in the clear. |
| `HttpOnly` | Script cannot read the value. This limits *theft* under cross-site scripting; it does not stop injected script from making authenticated requests with the cookie attached, so it reduces the blast radius rather than removing it. |
| `SameSite=Lax` | The cookie is withheld from cross-site subresource requests and cross-site form posts, which removes most classic cross-site request forgery. It is sent on top-level GET navigation, so a state-changing GET is still reachable cross-site — which is one more reason state changes are not GETs. |
| `SameSite=Strict` | Withheld even on inbound top-level navigation, so a user following a link from anywhere else arrives logged out. Correct for an administrative console, usually wrong for a consumer product. |
| `SameSite=None` | Requires `Secure`, and means you have a genuine cross-site need. Say what it is in a comment, because it is also what an accidental third-party embed produces. |
| `__Host-` prefix | The browser refuses the cookie unless it is `Secure`, has no `Domain` attribute and has `Path=/`. This is what stops a sibling or compromised subdomain from setting a cookie your application will accept. |
| No `Domain` attribute | Setting `Domain=example.com` shares the session with every subdomain, including the ones you do not control tightly. Host-only is the default and the right one. |

The important limit: **`SameSite` is scoped to the site, not the origin.** `evil.internal.example.com` is same-site with `app.example.com`, so a compromised or user-controlled subdomain sits inside the protection. `SameSite` is a strong default, not a replacement for anti-forgery tokens on state-changing requests where subdomains are numerous or not all yours.

Set an idle timeout and an absolute timeout; the idle one bounds an unattended browser, the absolute one bounds a stolen cookie. Keep a listable session record per user with device and last-seen metadata, because "sign out other devices" is the control a user reaches for during their own incident, and it is also how support answers "was that me". Record the IP and user agent for review, but do not hard-bind the session to them — mobile networks change address mid-session, and the support load buys almost nothing.

### 6. Tokens

**Refresh token rotation with reuse detection.** Every refresh returns a new refresh token and invalidates the old one. If a previously used token is presented again, the identity provider revokes the entire token family for that grant and forces re-authentication. RFC 9700 requires rotation or sender-constraining for public clients.

What matters is what a detection event *means*. Reuse means two parties hold the same refresh token: one is the legitimate client and one is not, and you cannot tell which is presenting it. That is why the response is to kill the family rather than to reject the request — rejecting only the replay leaves whichever party won the race in possession of a live chain. Expect a low rate of false positives from genuine races (a client that retried through a dropped response, two tabs refreshing at once), and handle them with a short grace window on the immediately preceding token rather than by weakening the rule. A reuse event is a security signal worth alerting on, not a log line.

Sender-constraining is the stronger option where you can take it: DPoP (RFC 9449, September 2023) or mutual-TLS-bound tokens (RFC 8705) make a stolen token useless without the corresponding key, which is the only thing that defends against a token exfiltrated wholesale.

**Lifetimes.** These are engineering judgement rather than standards, and the logic is that an access token's lifetime is your revocation latency:

| Artefact | Starting point | The argument |
| --- | --- | --- |
| Access token | 5 to 15 minutes | Long enough to avoid a refresh on every request; short enough that a revoked grant stops working within a coffee break. |
| ID token | Minutes, consumed once at sign-in | It is a statement about an authentication event, not a session. |
| Refresh token, confidential client | Days to weeks, with an absolute cap | Rotation plus reuse detection is what makes this safe. |
| Refresh token, public client | Hours to days, rotated every time | The client cannot keep a secret, so bound the window instead. |
| Browser session cookie | Idle 30 minutes to a few hours; absolute 8 to 24 hours | Tune on what the account can do, not on what feels convenient. |
| Anything touching money or administration | Shorter, plus step-up re-authentication at the action | Re-authenticate at the dangerous operation rather than shortening every session to suit it. |

**Where a JWT's claims can be trusted.** A JWT is trustworthy exactly to the extent that you verified it. The validation is a list, and skipping any line makes the rest decorative:

- **Verify the signature with a key you chose.** Fetch the issuer's JWKS from its discovery document, cache it, select by `kid` from your cached set, and re-fetch on an unknown `kid` with a rate limit. Never fetch a key from a URL carried inside the token.
- **Allowlist the algorithm in your own code.** Pass the expected algorithm to the library rather than letting the token's `alg` header select the verification path. The two classic failures both live here: `alg: none`, where a library treats the token as unsigned and returns the claims, and algorithm confusion, where a token minted with `HS256` is verified against an RSA public key that the verifier treats as an HMAC secret — and that public key is, by design, published. RFC 8725, JSON Web Token Best Current Practices (February 2020), is the primary source for both.
- **Check `iss` against the exact expected issuer, and `aud` against this service's identifier.** Without the audience check, a token minted for another service — or another tenant of the same identity provider — verifies perfectly. This is the validation most often missing in code that "works".
- **Check `exp`, and `nbf` if present, with a small clock skew allowance** of a minute or so, not fifteen.
- **Check the token type where the profile defines one.** RFC 9068 (October 2021) gives access tokens `typ: at+jwt`, which is what stops an ID token being presented as an access token.
- **Do not use an ID token as an access token.** The ID token's audience is your client, not your API. Accepting it at a resource server is audience confusion with an ordinary-looking cause.

**Revocation is the whole lifetime argument.** A self-contained token is valid until it expires because verification touches nothing but a public key. Your options are: keep access tokens short and revoke the refresh token (the default, and the reason for the five-to-fifteen-minute figure); introspect at the edge (RFC 7662), which restores revocation and re-introduces the lookup you were avoiding; or keep a deny list of revoked identifiers at the gateway, which is a session store you have promised yourself is small. Choose deliberately and write the chosen revocation latency into the design, because someone will eventually ask how fast a compromised account can be cut off and the answer needs to be a number.

### 7. Credentials you own

Skip this entire step if an identity provider holds the passwords. If you own them, `references/credentials-and-recovery.md` has the parameters and the citations; the rules that belong in the design document are these.

**Hashing.** Argon2id is the first choice, with scrypt, bcrypt and PBKDF2 as the acceptable alternatives in that order, each with parameters chosen against your own hardware and rechecked yearly. RFC 9106 (September 2021) gives Argon2's recommended configurations; the OWASP Password Storage Cheat Sheet gives current minimums for all four and is revised more often than any RFC, so read the revision date on the page. Two details cause real incidents: bcrypt truncates its input beyond 72 bytes, so a long passphrase is silently shortened, and any fast hash — SHA-256, salted or not, single-pass — is a design defect rather than a weak choice.

**Policy.** Reject a candidate password by checking it against a breach corpus and a list of context-specific terms, rather than by demanding a symbol and a digit. NIST SP 800-63B sets this out in its memorized-secret section: a minimum length, a check against known-compromised values, and no composition rules and no periodic expiry, because both produce predictable mutations of one remembered password. Revision 4 is the current one; the specifics above were checked against Revision 3 (June 2017, with the March 2020 errata), so read the figures out of Revision 4 before quoting one.

**Multi-factor, and the distinction that decides the choice.** Two categories, and the line between them is phishing resistance, not strength:

| Factor | Resists guessing | Resists phishing | Why |
| --- | --- | --- | --- |
| Passkeys and security keys (W3C WebAuthn Level 2, Recommendation, 8 April 2021) | Yes | Yes | The credential is scoped to the relying party identifier and the signature covers the origin, so a look-alike domain cannot obtain a usable assertion. There is no code for a user to read out. |
| Smartcard or certificate-based authentication | Yes | Yes | Same property: the secret never leaves the device and is bound to the verifier. |
| TOTP (RFC 6238, May 2011) | Yes | No | The user reads a code off a screen and types it somewhere. A real-time relay collects and replays it inside the validity window. |
| Push approval, including number matching | Yes | No | Number matching fixes fatigue-based approval, not relaying. The user is still approving whatever asked. |
| SMS or email one-time codes | Partly | No | Also exposed to number-porting and to whoever holds the mailbox. NIST SP 800-63B Revision 3 treats public-telephone-network delivery as restricted, requiring a documented risk assessment. |

This is why the distinction decides the choice rather than informing it: credential phishing at scale uses a relay that sits between the user and the real site, and every factor in the "no" column passes straight through it. For administrators and anything holding customer data, require a phishing-resistant factor. Elsewhere, take a second factor of any kind over none, and plan the migration to passkeys.

**Recovery is the real strength of the whole design.** An account protected by a security key and recoverable by an emailed link is protected by that mailbox. Decide deliberately what the recovery path is, hold it to the standard of the strongest factor it can reset, and enrol a second factor at registration so recovery is not the first thing a locked-out user reaches for. Re-authentication requirements and the recovery design are in the reference file.

### 8. Enumeration, throttling and lockout

**Enumeration.** Keep the response identical for "no such account" and "wrong password" — same status, same body, same timing, which means performing the hash comparison against a dummy value when the account does not exist rather than returning early. Password reset always answers "if that address has an account, a link is on its way". Registration is the surface that cannot be fully closed, because "that email is already registered" is information the user genuinely needs; bound it with rate limiting and by completing the signal only after email confirmation.

**Throttling over lockout.** Lockout after a fixed number of failures converts a list of usernames into a denial-of-service tool: an attacker with a leaked email list locks out your entire user base and your support queue becomes the incident. Throttle instead — exponential backoff per account, a separate control per source address, and a global rate that recognises a credential-stuffing pattern spread thin across thousands of accounts, which is the shape that per-account counters miss. NIST SP 800-63B Revision 3 caps consecutive failed attempts at 100 and requires an effective throttling mechanism rather than a permanent lock. Where a lock is genuinely required, make it short and self-clearing, with a path back in that does not require a human.

### 9. Verify it against your own service

Design review is not enough; run these against your own system in a test environment.

- The session identifier before login differs from the one after. Compare the two cookies.
- A `state` or `nonce` mismatch on the callback fails closed. Change one character and confirm the request is rejected rather than logged.
- The authorization code cannot be redeemed twice, and a code from one client instance cannot be redeemed with another's verifier.
- A token signed with `alg: none`, and a token signed with HMAC using the issuer's public key as the secret, are both rejected. Every library has a test hook for producing these.
- A token minted for a different audience or issuer is rejected by every resource server, including the internal ones.
- Replaying a rotated refresh token revokes the family, and the event reaches your alerting.
- Logout invalidates server-side: keep the cookie, replay the request, confirm it fails.
- Every registered redirect URI is exact, and none of the registered endpoints performs an onward redirect from a query parameter.

## Output format

```markdown
## Decision: build or integrate
[which, and the reason. If building, what made integration impossible.]

## Clients and flows
[each client type, the flow chosen, and whether it is confidential or public.]

## Authorization request
[PKCE, state, nonce, issuer validation. Registered redirect URIs, exact.]

## Session
[where it lives, cookie attributes and why each, rotation points, idle and absolute timeouts.]

## Tokens
[types, lifetimes, rotation and reuse detection, sender-constraining if any.]

## Validation rules
[the algorithm allowlist, key source, aud and iss values, clock skew.]

## Revocation
[the mechanism, and the latency it gives in seconds or minutes.]

## Credentials and factors
[hashing algorithm and parameters if owned; factors offered; which are phishing-resistant; who is required to use one.]

## Recovery
[the path, and the strongest factor it can reset.]

## Abuse controls
[throttling shape, enumeration handling, what alerts and to whom.]

## Residual risk
[what is deliberately accepted, with the reason and an owner.]
```

## Anti-patterns

**Decoding a JWT instead of verifying it.** The library offers both and the names differ by a word. The decoded version works in every test, in staging and in production, and fails only against a forged token — which is to say, it fails only when it matters. Pass the expected algorithm and audience explicitly on every call.

**Letting the token's `alg` header choose the verification path.** It is the attacker's field. `alg: none` returns claims from an unsigned token, and switching an RS256 verifier to HMAC lets a published public key be used as a signing secret. Allowlist the algorithm in your code.

**Verifying the signature and skipping `aud` and `iss`.** The token is genuine, correctly signed and intended for somebody else — another service, another tenant of the same provider. Nothing in the verification fails, and the request is authorised as whoever the token says.

**Storing an access token in `localStorage` and calling it stateless authentication.** Any injected script reads it, it cannot be revoked before expiry, and it is a bearer artefact usable from anywhere. A cookie session with `HttpOnly` removes the first problem and a server-side record removes the second.

**Prefix-matching redirect URIs so preview deployments work.** It is the plausible reason, and it accepts hosts you do not own. Register each preview host, or route them through one stable callback.

**Reusing the session identifier after login.** Session fixation needs only an identifier the victim's browser holds before authentication and keeps after it. The code looks fine, the tests pass, and the attack takes two steps.

**Rolling your own password hash.** Salted SHA-256, or a secret pepper in place of a work factor. The defect is speed: the attacker with the dump has better hardware than you, and the only lever is making each guess expensive.

**Using the ID token as an API access token.** Its audience is your client. Accepting it at a resource server means any client issued a token by the same provider is now a valid caller of your API.

**Trusting an `email` claim without `email_verified`.** Linking accounts by email address lets anyone who can register that address at any federated provider log into an existing account. Link on the provider's subject identifier, and treat matching an email to an existing account as a step that requires proof.

**Lockout after five failures.** With a list of usernames, an attacker locks out every account you have, and the outage is indistinguishable from an attack on your infrastructure. Exponential backoff and stuffing detection fail more gracefully.

**Different responses for "unknown user" and "wrong password".** Frequently it is only the timing — an early return that skips the hash comparison. It converts a credential-stuffing list into a validated account list, which is the input to every subsequent attack.

**An embedded webview for the identity provider's login page in a mobile app.** It breaks single sign-on, cannot use platform passkeys, and asks the user to type provider credentials into a form the host application can read — which is also exactly what a malicious application does, so it trains the wrong instinct.

**Deferring MFA for administrators.** Administrative accounts are the ones worth phishing, and they are the smallest population to enrol. If MFA ships in one place first, it is here.

## Reference files

- `references/flows-and-tokens.md` — read when choosing or integrating a flow, or writing token validation: the full parameter list for a correct authorization request, per-client-type detail, redirect URI registration patterns including preview environments, refresh rotation and reuse detection handling, the JWT validation checklist in order, key rotation and JWKS caching, and the revocation options with their costs.
- `references/sessions-and-cookies.md` — read when writing session or cookie code, designing logout, or diagnosing a cross-site cookie behaviour: the session lifecycle and every rotation point, the cookie attribute matrix with browser caveats, the backend-for-frontend pattern, idle and absolute timeout selection, "sign out everywhere", and where `SameSite` does not reach.
- `references/credentials-and-recovery.md` — read when you own the credential rather than delegating it: password hashing algorithms with current parameters and their primary sources, the breach-corpus check, what to do about an existing weak hash, multi-factor enrolment and step-up, account recovery design, and the throttling and enumeration details.
