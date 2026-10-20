---
name: authn-authz
description: >
  Authentication and authorization for platform services and agents — proving who is calling, and
  deciding what they may do. Carries: the OIDC/OAuth 2.1 flows that are still allowed and the
  grants that aren't, the complete JWT validation checklist (alg pinning, iss/aud/exp, JWKS
  rotation), why an id_token is not an API credential, server-side per-object authorization and the
  IDOR/tenant-bleed bugs a valid token doesn't prevent, workload identity (k8s projected tokens,
  IRSA/Workload Identity, SPIFFE SVIDs, CI OIDC federation), mTLS, k8s RBAC subjects, and scoped
  token exchange for agent delegated authority. Load when adding a login, issuing or validating a
  token, granting a permission, securing service-to-service traffic, or giving an agent authority to
  act for a user. Triggers: authentication, authorization, authn, authz, OAuth, OIDC, JWT, token
  validation, JWKS, PKCE, refresh token, mTLS, service account, RBAC, IRSA, workload identity,
  SPIFFE, SSO, MFA, API key, session, IDOR, multi-tenant isolation, on-behalf-of, impersonation.
  The musts are `policy/identity-and-access.md`; secret storage is `secrets-management`.
---

# authn-authz — a valid token answers one question, and it isn't the important one

> On-demand: load this when identity or permission is the question. The non-negotiable rules are
> canon at `.claude/memory/policy/identity-and-access.md` (`I1`–`I9`). Where secrets are *stored* is
> `secrets-management`; cluster RBAC *objects* are `kubernetes`; what an agent may do with the
> authority it's given is `agent-security`.

## When this applies

Adding a login. Issuing or validating a token. Granting a permission. Securing service-to-service
traffic. Letting an agent act for a user.

## The distinction that organises everything

**Authentication** = who is calling. **Authorization** = what they may do.

Almost every real-world API security bug lives in the second one, on the far side of a perfectly
validated token: IDOR, missing object-level checks, tenant bleed, "the UI doesn't show that button."
A team that says "we use OAuth" has answered the easy half.

And the two identity populations need different mechanisms — applying assurance levels to a service
account, or attestation to a person, is a category error:

| | Humans | Workloads |
|---|---|---|
| Prove identity by | Phishing-resistant MFA via an IdP | Platform attestation — what the workload *is* |
| Credential lifetime | Session | Minutes to hours, auto-rotated |
| Failure mode | Phishing, reuse | Long-lived secret in a repo or image |
| Canon | `I2` | `I3` |

## Human authentication — OAuth 2.1 / OIDC

**Use your IdP. Do not build authentication.** Password storage, MFA enrolment, recovery flows,
session management, and account-takeover defence are each a project.

The flow, and only this flow: **authorization code + PKCE**, for every client type including
confidential ones.

Forbidden, and why (canon `I5`):

| Removed | Because |
|---|---|
| Implicit grant | Tokens in URL fragments leak via history, referrer, logs |
| Password grant (ROPC) | The client handles the user's password |
| Wildcard redirect URIs | Open redirect → token theft. Exact string match only |
| Bearer tokens in query strings | They land in access logs |

**`id_token` ≠ `access_token`.** The `id_token` tells *your client* who signed in. The `access_token`
is what you send to an API. Sending an `id_token` as an API credential is a common and serious
mistake — it's audienced to the client, so any service accepting it accepts tokens minted for a
different purpose.

## JWT validation — the complete checklist (`I6`)

Partial validation is the norm; every omission below is a published vulnerability class.

```python
claims = jwt.decode(
    token,
    key=jwks_client.get_signing_key_from_jwt(token).key,
    algorithms=["RS256"],          # PIN IT. Never read alg from the token header.
    issuer=EXPECTED_ISSUER,        # exact match
    audience=THIS_SERVICE,         # this service must be in aud
    options={"require": ["exp", "iat", "iss", "aud"], "verify_exp": True},
    leeway=30,                     # minimal clock skew
)
```

- **Reject `alg: none`** and never let the token choose its own algorithm — the classic confusion
  attack is an RS256 verifier handed an HS256 token signed with the public key.
- **`aud` is not optional.** Without it, a token minted for *any* service in your IdP works on
  *every* service. This is the most common real-world JWT failure.
- **Rotate JWKS**, cache with a TTL, and refresh on unknown `kid` — with a rate limit, or an
  attacker forces you to hammer the IdP.
- **Validate `nonce`** on OIDC authentication flows.
- **Short lifetimes over revocation lists.** Revocation is hard; expiry is free. If you need instant
  revocation, you need introspection or very short tokens — decide which, don't assume.

## Authorization — the half that actually breaks

`I4`: decided **server-side, on every request, against the specific object.**

```python
# Wrong — the token proves identity, then the id is trusted
doc = db.get_document(request.json["document_id"])

# Right — the check is against this principal and this object
doc = db.get_document(request.json["document_id"])
require_permission(principal=ctx.principal, action="read", resource=doc)  # raises 404/403
```

- **Client-supplied ids, roles, and tenant claims are inputs to the check, never its result.**
- **Filter in the query, not after.** `WHERE tenant_id = :ctx_tenant` — not fetch-then-filter, which
  leaks through timing, counts, and any code path that forgets the filter.
- **Return 404, not 403**, for objects the caller may not know exist — a 403 confirms existence.
- **Deny by default.** New endpoints are unauthorized until explicitly permitted; a middleware that
  requires an explicit decorator, and fails closed when it's missing, catches the endpoint someone
  forgot.
- Model choice: RBAC for coarse roles, ABAC/ReBAC when permission depends on the relationship
  between principal and object (which is most real systems).

## Workload identity (`I3`) — no static credentials

In preference order:

| Mechanism | Use when |
|---|---|
| **SPIFFE/SPIRE SVIDs** | You run SPIRE; the most general answer (`policy/frameworks/spiffe-spire.md`) |
| **k8s projected ServiceAccount tokens** | In-cluster, with an explicit `audience` and a short `expirationSeconds` |
| **Cloud workload identity** — IRSA (EKS), Workload Identity (GKE) | Reaching cloud APIs. The pod's service account maps to a cloud role; no keys anywhere |
| **CI OIDC federation** | The pipeline reaching cloud or a registry. **Replaces long-lived cloud keys entirely** (`C6`) |

```yaml
# Projected token with an audience — not the legacy auto-mounted one
volumes:
  - name: api-token
    projected:
      sources:
        - serviceAccountToken:
            path: token
            audience: internal-api      # the receiving service validates this
            expirationSeconds: 3600
```

Long-lived API keys and static cloud access keys are prohibited for service-to-service auth. If an
external integration forces one, that's a decision-log entry with a compensating control and a review
date.

## Service-to-service (`I7`)

mTLS, with the peer's **verified identity** as the authorization input — not its IP, not its
namespace, not "it's inside the cluster." Network reachability is not permission; this rule and
`platform-security.md` `P5` (default-deny) are two halves of one control.

## Agents acting for users (`I8`)

The concrete answer to OWASP `ASI03`. When an agent acts for a principal:

1. The agent authenticates as **itself** (`ai-security.md` `AI6`) — its own identity, its own
   credential.
2. It obtains a **narrowed, short-lived** token for the specific action, via token exchange
   (RFC 8693) or equivalent.
3. Effective permission = **intersection** of the agent's own identity and the delegated scope.
4. The delegation **expires with the task**, and the action is attributable to *both* the agent and
   the principal.

**Never hand an agent the user's own token.** It then *is* that user — for this task, for every
subsequent task, and for whoever hijacks it — and nothing downstream can tell the difference.

## Gotchas

- **Authenticating the gateway, authorizing nowhere.** Edge auth plus trusting internal calls means
  one SSRF is full compromise.
- **`aud` unvalidated** — covered above, and worth repeating because it's the one that ships.
- **Roles from the token, permissions never re-checked.** A token issued before a permission was
  revoked keeps working until it expires; that's the argument for short lifetimes.
- **API keys as the "simple" option.** They're long-lived bearer credentials with no audience, no
  expiry, and no rotation story — every property `I3` and `I5` exist to prevent.
- **Testing authorization only as an admin.** The bugs are in what a *low-privilege* user can reach.
  Test cross-tenant explicitly; it's the check that finds real vulnerabilities.
