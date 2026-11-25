---
name: iam
description: "Covers identity architecture decisions: IAM vs PAM vs IGA scope, SAML vs OIDC/OAuth2, the phishing-resistance ladder (passkeys, FIDO2), joiner-mover-leaver, JIT and least privilege, and break-glass accounts. Use when the user asks about SSO and federation, choosing MFA, rolling out passkeys, privileged access management, access reviews and identity governance, or emergency admin accounts."
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Identity & access architecture

Identity is the control plane. Most 2024-2026 breaches are identity attacks, not
malware but phishing, token theft, MFA-fatigue, OAuth consent abuse. Design the
identity layer first; everything else (network, endpoint) is downstream of "who
is this and what may they do".

## Three disciplines: don't conflate

| Discipline | Covers                                                                                                    | Owns the question                                                  |
| ---------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **IAM**    | Authentication + authZ for the _general workforce/customers_: directory, SSO, MFA, federation, session    | "Is this the right person, and are they allowed in?"               |
| **PAM**    | _Privileged_ accounts: vaulting, secrets, session brokering/recording, credential rotation, JIT elevation | "How do admins/service accounts get power, briefly, with a trail?" |
| **IGA**    | _Governance_: lifecycle (JML), access requests/approvals, certification/recert, SoD policy, role mining   | "Who has access to what, why, and is it still justified?"          |

Decision: IAM is daily access, PAM is the high-blast-radius accounts, IGA is the
audit/lifecycle layer that proves IAM+PAM stay correct over time. You need all
three; a tool that claims "all-in-one" usually does one well.

## Federation: SAML vs OIDC/OAuth2

- **OAuth2** = _authorization_ (delegated access to APIs via tokens). It is **not**
  authentication. Using raw OAuth2 as login = the "OAuth login" anti-pattern.
- **OIDC** = identity layer _on top of_ OAuth2: adds the `id_token` (JWT). This is
  the modern default for new apps, SPAs, mobile, API-driven systems.
- **SAML 2.0** = older XML browser-SSO. Still everywhere in enterprise/legacy SaaS.

Pick OIDC for anything new, mobile, or API-centric. Tolerate SAML when the SaaS
only speaks SAML. Never hand-roll either: use the IdP's libraries; signature/
audience/replay validation is where homegrown SSO gets broken.

- OAuth2 flow rule: **authorization code + PKCE** for everything now (SPAs and
  native included). Implicit and ROPC flows are deprecated: don't use.
- SCIM is the companion to both: SAML/OIDC log users in, **SCIM provisions/
  deprovisions** them. No SCIM = orphaned accounts and slow leaver cleanup.

## Authentication strength ladder (weak -> strong)

Phishing-resistance is the dividing line, not "MFA / no MFA". The bypassable tier
all fall to a real-time reverse-proxy (Evilginx-class) that relays the OTP/push.

1. Password alone: assume compromised.
2. Password + SMS/email OTP: phishable + SIM-swap; **not** real MFA for privileged use.
3. TOTP authenticator app: phishable (relay), but no SIM-swap.
4. Push w/ number-matching: better, still social-engineerable (fatigue/relay).
5. **FIDO2 / WebAuthn passkeys** (**phishing-resistant**): private key never leaves
   the authenticator, challenge is origin-bound so a proxy can't replay it. This
   is the target state. CISA + NIST treat FIDO2/WebAuthn and PKI smartcards as the
   only phishing-resistant tier.

Decision rule: privileged + internet-facing admin = phishing-resistant only. Push
and TOTP are a transition state, not a destination.

### Passkeys: device-bound vs synced (current: verify, this is moving fast)

- **Synced passkeys** (Apple/Google/MS cloud): great UX, kill passwords for the
  workforce; private key is replicated across a consumer cloud.
- **Device-bound passkeys / hardware FIDO2 keys** (YubiKey etc.): key is hardware-
  pinned, **supports attestation** (you can cryptographically enforce approved
  authenticator models). Synced passkeys do NOT support attestation.
- Rule: synced passkeys for general workforce; **device-bound or hardware keys for
  privileged/AAL3 and regulated accounts**: NIST AAL3 requires the key stay in a
  hardware authenticator, which consumer-synced passkeys fail.
- Verify current normative text: NIST SP 800-63B-4 finalized July 2025 and now
  bakes phishing-resistance + syncable authenticators into AAL2/AAL3:
  fetch https://csrc.nist.gov/pubs/sp/800/63/b/4/final and its syncable-authenticator
  section https://pages.nist.gov/800-63-4/sp800-63b/syncable (the separate
  800-63Bsup1 supplement was withdrawn Aug 2025, superseded by 63B-4)
- Microsoft Entra "passkey profiles" (per-group device-bound vs synced policy
  via `passkeyType`) hit GA March 2026, with existing FIDO2 tenants auto-migrated;
  the enforcement lever exists now; verify tenant state before you promise it:
  https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-passkeys-fido2

Also drop legacy password theater: NIST 800-63B-4 says **no forced periodic rotation,
no composition rules**, screen against breached-password lists, allow 64+ char
passphrases + paste. If your policy still expires passwords every 90 days, it's stale.

## Lifecycle: joiner / mover / leaver (JML)

The expensive failures are **movers** (access accretes, never revoked) and
**leavers** (orphaned accounts). Automate from the HR system as source of truth.

- **Joiner**: provision from a role/birthright template via SCIM. No "copy Jane's
  access" (entitlement creep propagates).
- **Mover**: the hard one. On role change, **re-derive** entitlements and revoke
  what the new role doesn't grant. Most orgs only add, never subtract.
- **Leaver**: disable auth immediately (session + token revocation, not just a
  directory flag), then deprovision. Tie to HR termination event, same-day.
- IGA **access certification**: periodic recert catches the JML automation's misses:
  managers attest "still needed". Cross-link `load_skill control-mapping` for the
  framework ids (ISO A.5.18, NIST AC-2) this satisfies.

## Least privilege & just-in-time (JIT)

- **Standing privilege is the liability.** Replace always-on admin with JIT: request
  -> approve -> time-boxed elevation -> auto-expire. (Entra PIM, AWS IAM Identity
  Center perms sets, PAM session brokering.)
- Zero standing access for the highest tiers: admin role is empty until activated.
- **Separation of duties**: requester != approver; the person who grants access
  can't also use it unaudited.
- Service/machine identities now outnumber humans; they need the same: scoped,
  short-lived (OIDC workload federation / SPIFFE), rotated, no shared static secrets.
  Cross-link `load_skill crypto-key-management` for the secret-rotation half.

## Break-glass (emergency access)

The account that gets you back in when SSO/MFA/IdP is down. Get it right before
you need it:

- **2+ break-glass accounts**, cloud-only / not federated (so an IdP outage can't
  lock them out), excluded from Conditional Access that depends on the IdP.
- Credentials split + vaulted offline (password in a sealed/physical store, or split
  knowledge between two custodians). Phishing-resistant MFA where the platform allows.
- **High-fidelity alerting**: any break-glass sign-in pages the security team
  immediately: usage is always an incident-worthy event.
- Test quarterly; rotate after every use. An untested break-glass is a single point
  of failure dressed as a control.
