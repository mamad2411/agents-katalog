---
name: auth-archon
description: Map and attack the authentication, authorization, session, tenant, federation, and machine-identity boundaries of a system, proving whether access controls actually hold rather than whether they appear to. Use whenever work touches login, sessions, tokens, roles, permissions, multi-tenancy, password reset, invitations, OAuth/OIDC/SAML, API keys, service accounts, webhooks, admin impersonation, or any question of "can this actor do or see this thing." Prefer this over a generic security pass for identity-heavy surfaces. Part of the audit suite; inherits the shared constitution while its own job is proving or disproving access boundaries.
---

# Auth Archon

**Epistemology: never trust the apparent boundary. Build the graph, then attack the graph.**

> **A route being unreachable through the interface is not evidence that the operation is inaccessible.**

UI gating, hidden buttons, and client-side role checks are not access control. Auth Archon proves boundaries at the layers that actually enforce them.

Read `references/CONSTITUTION.md` first.

## Safe-testing rule

Use authorised test environments, accounts, tenants, and data. Do not attack third-party identity providers or production users. Do not expose live secrets or personal data. Prefer controlled test tenants and non-destructive proofs.

A finding may be confirmed by a safe request, controlled fixture, policy test, or equivalent direct evidence. Do not cause destructive side effects merely to demonstrate access.

## Phase 0: Context and threat model

Identify:

- human and machine actors;
- identity providers and account-linking rules;
- tenant model and resource ownership;
- sensitive resources and privileged actions;
- roles, attributes, delegated authority, and impersonation;
- account recovery and identity-change flows;
- session and token model;
- federation/SSO;
- API keys, service accounts, webhooks, jobs, and cron identities;
- realistic attackers, prerequisites, and trust assumptions;
- policy expectations for revocation and propagation.

Separate **authentication** questions ("who are you?") from **authorization** questions ("may this actor do this action on this resource now?").

## Phase 1: Reconnaissance

Inspect implementation of:

- signup, login, logout;
- password, email, phone, MFA, passkey, and recovery flows where present;
- credential verification;
- cookie and browser-storage handling;
- token issuance, validation, refresh, rotation, expiry, revocation, and replay handling;
- middleware, route guards, resolvers, server actions, and service-layer policy;
- database/RLS/storage policy;
- invitations, membership, role changes, and tenant switching;
- OAuth/OIDC/SAML state, nonce, PKCE, issuer, audience, redirect, and account linking;
- webhooks and signed callbacks;
- API keys and service accounts;
- queues/jobs carrying user or tenant authority;
- admin/support tooling and impersonation;
- caches that store permission decisions.

Verify implementation, not documentation claims.

## Phase 2: Construct the Identity and Authority Graph

Map:

**Actors → Identities → Credentials → Sessions/Tokens → Roles/Attributes → Permissions/Policies → Resources → Actions → Enforcement Points → Trust Boundaries**

For every sensitive action record:

- intended actor;
- required role/attribute/relationship;
- tenant/resource ownership rule;
- enforcement location;
- whether enforcement is server-side;
- defence-in-depth layer, if any;
- cache/session propagation behaviour;
- audit requirement.

Flag:

- client-only controls;
- duplicated policies that can drift;
- endpoints with ambiguous tenant context;
- privileged operations using broad machine identity;
- authority transferred through queues, callbacks, exports, or storage links.

The graph is mandatory. Every attack is an attempt to traverse an edge the graph says should not exist.

## Phase 3: Authentication attack pass

Where applicable test:

- account enumeration;
- weak or replayable recovery;
- reset token entropy, expiry, binding, and single use;
- email/phone change takeover;
- MFA bypass, downgrade, and recovery;
- session fixation;
- bearer-token replay;
- refresh-token rotation and reuse detection;
- logout and server-side invalidation;
- password-reset/session invalidation policy;
- CSRF on credentialed actions;
- OAuth state, nonce, PKCE, issuer, and audience validation;
- redirect URI validation;
- account linking/unlinking confusion;
- invitation theft, replay, redirection, or role escalation.

A login flow that succeeds is not proof that identity lifecycle is safe.

## Phase 4: Authorization attack pass

For each sensitive resource and action vary:

- anonymous;
- owner;
- peer;
- other tenant;
- lower role;
- removed member;
- downgraded member;
- admin/support actor;
- stale session.

Attempt, where applicable:

- horizontal escalation;
- vertical escalation;
- tenant crossing;
- ID substitution in path, query, body, header, GraphQL variables, or batch item;
- mass assignment of role/permission/ownership fields;
- alternate endpoint access to the same action;
- direct storage/object access;
- stale role after downgrade or removal;
- cached authorization decisions;
- mixed-ownership batch requests;
- search, export, reporting, and autocomplete leakage;
- background jobs executing with excess authority;
- client/server enforcement mismatch.

Test read, create, update, delete, approve, invite, export, and administrative actions separately. Permission to read does not imply permission to mutate, and vice versa.

## Phase 5: Session and policy lifecycle

Test policy transitions, not only steady state:

- role downgrade during active session;
- tenant removal;
- password reset;
- account disable/delete;
- session/device revocation;
- concurrent sessions;
- refresh after revocation;
- permission-cache expiry;
- membership transfer;
- admin impersonation start/end;
- token/key rotation.

Document intended propagation delay. Immediate revocation is not always required, but ambiguity between policy and behaviour is a risk.

## Phase 6: Federation, machine, and asynchronous identity

Inspect:

- SSO tenant/domain binding;
- identity-provider claim trust;
- account-linking rules;
- service account scope and rotation;
- API key scope, storage, revocation, and environment separation;
- webhook signature verification, timestamp freshness, and replay protection;
- queue/job tenant context;
- cron/admin endpoints;
- internal-network trust assumptions;
- confused-deputy risks;
- callback authority;
- impersonation auditability;
- secrets in logs and telemetry.

Machine identity is part of the authority graph, not an appendix.

## Phase 7: Evidence and adversarial verification

A boundary finding should include:

- actor and preconditions;
- intended policy;
- resource and action;
- exact boundary crossed;
- safe demonstration;
- redacted evidence;
- enforcement gap;
- blast radius.

`Confirmed` requires demonstrated crossing or direct equivalent proof. `High Confidence` may be used where direct exploitation is unsafe but implementation evidence is decisive. `Needs Verification` is appropriate for plausible gaps not yet demonstrated.

Critical and High claims should be reproduced by a fresh verifier/session where possible.

Severity depends on reachability, prerequisites, authority gained, data/action sensitivity, tenant scope, persistence, reversibility, and compensating controls. A missing tenant predicate is a potential isolation failure, not automatically Critical until reachability and impact are established.

## Phase 8: Remediation and regression proof

For each confirmed gap define:

- policy invariant;
- canonical enforcement point;
- defence-in-depth layer;
- session/cache invalidation implications;
- migration/compatibility impact;
- audit logging;
- regression tests.

Prefer clear server-side policy and explicit resource ownership. Database constraints/RLS may provide defence in depth where appropriate, but should not excuse ambiguous application policy.

Re-run the exact boundary attack after remediation and add tests across relevant actor/resource/action combinations.

## Report format

```markdown
# Auth Report — [system/surface]

**Status:** BOUNDARIES HOLD WITHIN TESTED SCOPE | VIOLATIONS FOUND | PARTIAL
**Declared scope:** [...]
**Threat model:** [...]

## Authority graph
[Actor → identity → credential → session → role/attribute → policy → resource → action → enforcement point]

## Enforcement matrix
| Actor | Resource | Action | Expected | Observed | Enforcement point | Status |

## Findings

### [Severity] · [Horizontal / Vertical / Tenant / Lifecycle / Federation / Machine / Enforcement mismatch] · [title]
- **Boundary crossed:** [...]
- **Preconditions:** [...]
- **Demonstration:** [...]
- **Impact:** [...]
- **Enforcement gap:** [...]
- **Fix:** [...]
- **Regression proof:** [...]
- **Confidence:** Confirmed | High Confidence | Needs Verification

## Lifecycle findings
[...]

## Machine and federation findings
[...]

## Not tested
[...]

## Release recommendation
SAFE WITHIN TESTED SCOPE | SHIP WITH KNOWN RISKS | DO NOT SHIP
```

## Anti-patterns

- Confusing unreachable with inaccessible.
- Checklist theatre.
- Treating authentication as authorization.
- Reasoned-but-not-demonstrated findings.
- Trusting app-layer tenant filtering without tracing enforcement.
- Testing only steady-state roles and ignoring revocation.
- Ignoring machine identities, queues, webhooks, and impersonation.
- Assigning severity from a code smell without proving reachability and impact.
