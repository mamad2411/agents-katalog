---
name: nist-800-63
description: >-
  NIST SP 800-63-4: sign-in, MFA, recovery and federation to IAL, AAL and FAL.
  Builds and reviews identity systems against the Digital Identity Guidelines
  (base volume and 800-63A-4, 800-63B-4, 800-63C-4): digital identity risk
  management and xAL selection, identity proofing (IAL1-3, evidence strength,
  no KBV), authenticators (AAL1-3, password length and blocklists, no composition
  rules or forced rotation, MFA, phishing resistance, syncable authenticators and
  passkeys, OTP and SMS limits), account recovery, session timeouts and
  reauthentication, and federation assertions (FAL1-3, injection protection,
  holder-of-key, bound authenticators). Use when designing or reviewing sign-in,
  password rules, MFA, passkeys, account recovery, session management, identity
  proofing, or OIDC/SAML federation that must meet NIST 800-63, or when asked
  for "AAL2", "IAL2", "FAL2", "NIST password guidelines" or a Digital Identity
  Acceptance Statement. Targets SP 800-63-4 (July 2025) and upgrades from
  SP 800-63-3.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# NIST SP 800-63 Digital Identity Guidelines

NIST Special Publication 800-63 is the US National Institute of Standards and Technology's four-volume suite for digital identity: the base volume (risk management and assurance level selection), 800-63A (identity proofing and enrollment), 800-63B (authentication and authenticator management) and 800-63C (federation and assertions). This skill pins SP 800-63-4, published 31 July 2025, and produces sign-in, MFA, recovery, session and federation designs, code reviews and checklists that meet its SHALL-level requirements at a chosen IAL, AAL and FAL.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Citations name the volume (63, 63A, 63B, 63C) and its section, for example 63B § 3.1.1.2. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: relying party (RP, the online service), credential service provider (CSP) or verifier, identity provider (IdP), or a reviewer of one of them.
- Functions in scope: identity proofing, authentication, federation, or a combination. The suite scopes out machine-to-machine authentication and API access on behalf of subjects (63 § 1.1).
- Target assurance levels: the IAL, AAL and FAL per user group, or "unknown" (then run the risk process in step 2).
- Population: public-facing or federal enterprise. Several rules differ, for example phishing resistance and syncable authenticators (63B § 2.2.2, Appendix B.2).
- Target version: SP 800-63-4 (current, the default). SP 800-63-3 is legacy: read it and upgrade from it, never design to it. No preview line exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the CSRC pages for a newer revision, errata or a draft, check pages.nist.gov/800-63-4 for FAQs and conformance criteria, and update the pins.

## Invariants

1. **Assurance levels come from a documented risk process.** RPs select an initial IAL, AAL and FAL per user group from the effective impact level and document whether each function is needed (63 § 3.3.3); tailoring decisions, compensating and supplemental controls go in a Digital Identity Acceptance Statement (63 § 3.4, § 3.4.4).
2. **Password length, not composition.** Single-factor passwords are at least 15 characters; passwords used only inside MFA at least 8 (63B § 3.1.1.2). No other composition rules, no periodic changes (force a change only on evidence of compromise), no hints, no security questions (63B § 3.1.1.1, § 3.1.1.2).
3. **Blocklist and allow password managers.** New and changed passwords are compared in full against a blocklist of common, expected or compromised values, with the rejection reason shown; verifiers allow password managers and autofill and verify the whole password without truncation (63B § 3.1.1.2).
4. **Passwords are stored salted and hashed.** Use a password hashing scheme with a cost factor and a salt of at least 32 bits (63B § 3.1.1.2).
5. **Rate-limit guessing.** At most 100 consecutive failed attempts per authenticator on an account, then disable it until rebinding (63B § 3.2.2).
6. **AAL2 is two factors and offers phishing resistance.** Use a multi-factor authenticator or a physical authenticator plus a password or biometric; at least one authenticator is replay-resistant; verifiers offer at least one phishing-resistant option (63B § 2.2.1, § 2.2.2).
7. **AAL3 is a non-exportable phishing-resistant key.** Public-key cryptographic authenticator with a non-exportable private key, authentication intent on every authentication; syncable authenticators are not allowed (63B § 2.3.1, § 2.3.2).
8. **Manual-entry codes are never phishing-resistant.** OTP and out-of-band authenticators do not count as phishing-resistant (63B § 3.2.5); email is not an out-of-band authenticator, and "compare and approve" push is not acceptable (63B § 3.1.3, § 3.1.3.1).
9. **Syncable passkeys need user verification to count as MFA.** Request UV as preferred and inspect the UV flag; without UV, treat the authenticator as single-factor (63B Appendix B.3).
10. **Binding and recovery are authenticated and notified.** Binding a new authenticator requires authentication at the lower of the account's highest available AAL and the new authenticator's AAL, plus an independent notification (63B § 4.1.2.1); account recovery follows § 4.2.2 and always notifies the subscriber (63B § 4.2.3).
11. **Sessions time out by AAL.** Session secrets are at least 64 bits from an approved random bit generator (63B § 5.1); overall timeout at AAL3 is at most 12 hours (63B § 2.3.3), and SHOULD be at most 30 days at AAL1 and 24 hours at AAL2 (63B § 2.1.3, § 2.2.3).
12. **No KBV for identity verification.** Knowledge-based verification SHALL NOT be used to verify identity (63A § 2.5.1).
13. **RPs validate every assertion fully.** Signature, issuer, validity window, audience, nonce, allowable xALs and replay (63C § 4.9); subject identifiers are scoped to their issuer (63C § 3.4, § 4.9).
14. **FAL2 starts at the RP and blocks injection.** The RP initiates, the assertion has a single audience and injection protection, and federated identifiers carry no plaintext personal information (63C § 2.3).

## Workflow

1. **Pick the version.** Use SP 800-63-4. If a policy, contract or system cites SP 800-63-3, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ The design cites SP 800-63-4 and the 63A-4, 63B-4 and 63C-4 volumes, not a legacy revision.
2. **Select the assurance levels.** Define the online service and user groups, assess impact per user group, map impact to an initial IAL, AAL and FAL, tailor, and record it in a DIAS.
   -> [`references/assurance-levels.md`](references/assurance-levels.md)
   ✓ Each user group has a documented IAL (or "no proofing"), AAL and FAL (or "no federation"), with the rationale for any tailoring.
3. **Design identity proofing** (only when an IAL is selected). Pick proofing types, evidence, validation and verification for the IAL, plus fraud checks, injection defences and exception handling.
   -> [`references/identity-proofing.md`](references/identity-proofing.md)
   ✓ Core attributes are validated against authoritative or credible sources, and no step relies on KBV.
4. **Choose authenticators and verifier rules.** Pick the permitted authenticator types for the AAL, write the password policy, and set rate limits, phishing resistance and syncable-authenticator policy.
   -> [`references/authenticators.md`](references/authenticators.md)
   ✓ The password policy has the 15 or 8 character minimum, a blocklist, no composition rules and no expiry, and AAL2 offers a phishing-resistant option.
5. **Design binding, recovery and notifications.** Bind additional authenticators, offer recovery methods allowed at the account's AAL, and send notifications to independent addresses.
   -> [`references/sessions-and-recovery.md`](references/sessions-and-recovery.md)
   ✓ An attacker with one stolen factor cannot add an authenticator or recover the account without the subscriber being notified.
6. **Manage sessions and reauthentication.** Generate session secrets, configure cookies, and set overall and inactivity timeouts for the AAL.
   -> [`references/sessions-and-recovery.md`](references/sessions-and-recovery.md)
   ✓ Session timeouts match the AAL table, and no access token is treated as proof the subscriber is present.
7. **Federate** (only when an FAL is selected). Set up trust agreements and keys, request and validate assertions, and add holder-of-key or bound authenticators at FAL3.
   -> [`references/federation.md`](references/federation.md)
   ✓ The RP rejects an assertion with a wrong audience, a missing nonce at FAL2 or above, or a replayed identifier.
8. **Upgrade** (only when asked). Follow the SP 800-63-3 to SP 800-63-4 checklist for each volume.
   -> [`references/versions.md`](references/versions.md)
   ✓ Every 800-63-3 rule that changed has been re-checked, and the transition plan for existing accounts is recorded in the DIAS.

## Verify before done

- [ ] The xAL selection per user group and any compensating or supplemental controls are written down in a DIAS (63 § 3.4.4).
- [ ] Single-factor passwords need 15 characters, MFA-only passwords 8; the maximum should be at least 64; there are no composition rules, no expiry, no hints and no security questions (63B § 3.1.1.2).
- [ ] Password changes are checked against a blocklist, paste and autofill work, and storage uses a salted password hashing scheme with a cost factor (63B § 3.1.1.2).
- [ ] Consecutive failures per authenticator are capped at 100 or fewer (63B § 3.2.2).
- [ ] AAL2 flows offer a phishing-resistant option; AAL3 flows accept only non-exportable, phishing-resistant keys and no synced passkeys (63B § 2.2.2, § 2.3.2).
- [ ] WebAuthn verification requests UV as preferred and treats a credential without UV as single-factor (63B Appendix B.3).
- [ ] SMS or voice codes are flagged as a restricted authenticator, with a non-restricted alternative offered (63B § 3.1.3.3, § 3.2.9).
- [ ] Session cookies are `Secure` and narrowly scoped, and should be `HttpOnly`, `__Host-` prefixed and `SameSite` Lax or Strict (63B § 5.1.1).
- [ ] Account recovery at AAL2 needs two recovery methods, or one plus a bound single-factor authenticator, or repeated proofing, and always notifies (63B § 4.2.2.2, § 4.2.3).
- [ ] The RP checks all seven assertion validation items in 63C § 4.9 and, at FAL2, only accepts RP-initiated, single-audience assertions (63C § 2.3).

## Reference index

- **`references/versions.md`**: SP 800-63-4 and SP 800-63-3 with their status, what changed in each volume, the upgrade checklist, and the withdrawn syncable-authenticators supplement. Load for steps 1 and 8.
- **`references/assurance-levels.md`**: the Digital Identity Risk Management process, impact categories and levels, the impact-to-xAL mapping, tailoring, the DIAS, continuous evaluation, redress and AI/ML disclosure. Load for step 2.
- **`references/identity-proofing.md`**: IAL1-3, core attributes, evidence strength, validation and verification methods, fraud management, injection and deepfake defences, trusted referees, confirmation codes and subscriber accounts. Load for step 3.
- **`references/authenticators.md`**: permitted authenticator types per AAL, passwords, look-up secrets, out-of-band and SMS, OTP, cryptographic authenticators, wallets, syncable authenticators, rate limiting, biometrics, phishing resistance and activation secrets. Load for step 4.
- **`references/sessions-and-recovery.md`**: authenticator binding, account recovery, loss and invalidation, notifications, session secrets, cookies, timeouts and reauthentication. Load for steps 5 and 6.
- **`references/federation.md`**: FAL1-3, xAL signalling, federated identifiers and PPIs, trust agreements, assertion contents and validation, presentation channels, holder-of-key and bound authenticators, shared signaling and the OIDC/SAML mapping. Load for step 7.

## Related skills

- `webauthn`, for passkeys and the UP, UV, BE and BS flags: `npx skills add ScaleDockHQ/scaledock-skills --skill webauthn`
- `openid-connect`, for ID Tokens, nonces and the authorization code flow used at FAL2: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`
- `saml`, for SAML assertions, artifact binding and holder-of-key: `npx skills add ScaleDockHQ/scaledock-skills --skill saml`
- `oauth`, for access tokens, refresh tokens and sender-constrained identity APIs: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`
- `owasp-asvs`, for verification requirements that map onto these rules: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-asvs`
- `shared-signals`, for the shared signaling between IdP and RP in 63C § 4.8: `npx skills add ScaleDockHQ/scaledock-skills --skill shared-signals`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [NIST SP 800-63 Digital Identity Guidelines (Revision 4 home)](https://pages.nist.gov/800-63-4/): NIST online edition index, final released July 2025; FAQs and conformance criteria "coming soon", checked 2026-10-05.
- [SP 800-63-4 Digital Identity Guidelines (online)](https://pages.nist.gov/800-63-4/sp800-63.html): Final, SP 800-63-4, checked 2026-10-05.
- [SP 800-63A-4 Identity Proofing and Enrollment (online)](https://pages.nist.gov/800-63-4/sp800-63a.html): Final, SP 800-63A-4, checked 2026-10-05.
- [SP 800-63B-4 Authentication and Authenticator Management (online)](https://pages.nist.gov/800-63-4/sp800-63b.html): Final, SP 800-63B-4, checked 2026-10-05.
- [SP 800-63C-4 Federation and Assertions (online)](https://pages.nist.gov/800-63-4/sp800-63c.html): Final, SP 800-63C-4, checked 2026-10-05.
- [CSRC: SP 800-63-4](https://csrc.nist.gov/pubs/sp/800/63/4/final): Final, published 2025-07-31, supersedes SP 800-63-3, checked 2026-10-05.
- [CSRC: SP 800-63A-4](https://csrc.nist.gov/pubs/sp/800/63/a/4/final): Final, published 2025-07-31, supersedes SP 800-63A, checked 2026-10-05.
- [CSRC: SP 800-63B-4](https://csrc.nist.gov/pubs/sp/800/63/b/4/final): Final, published 2025-07-31, supersedes SP 800-63B, checked 2026-10-05.
- [CSRC: SP 800-63C-4](https://csrc.nist.gov/pubs/sp/800/63/c/4/final): Final, published 2025-07-31, supersedes SP 800-63C, checked 2026-10-05.
- [CSRC: SP 800-63B Supplement 1, Incorporating Syncable Authenticators](https://csrc.nist.gov/pubs/sp/800/63/b/sup/final): Withdrawn on 2025-07-31 (published April 2024; content now in 63B-4 Appendix B), checked 2026-10-05.
- [NIST SP 800-63-3 Digital Identity Guidelines (home)](https://pages.nist.gov/800-63-3/): Superseded by SP 800-63-4 as of 2025-08-01, checked 2026-10-05.
- [SP 800-63-3 Digital Identity Guidelines (online)](https://pages.nist.gov/800-63-3/sp800-63-3.html): Final, June 2017 with errata of 2017-12-01 and 2020-03-02, superseded, checked 2026-10-05.
- [SP 800-63A Enrollment and Identity Proofing (online)](https://pages.nist.gov/800-63-3/sp800-63a.html): Final, June 2017 with errata of 2017-12-01 and 2020-03-02, superseded, checked 2026-10-05.
- [SP 800-63B Authentication and Lifecycle Management (online)](https://pages.nist.gov/800-63-3/sp800-63b.html): Final, June 2017 with errata of 2017-12-01 and 2020-03-02, superseded, checked 2026-10-05.
- [SP 800-63C Federation and Assertions (online)](https://pages.nist.gov/800-63-3/sp800-63c.html): Final, June 2017 with errata of 2017-12-01 and 2020-03-02, superseded, checked 2026-10-05.
- [NIST SP 800-63 FAQ](https://pages.nist.gov/800-63-FAQ/): FAQ for SP 800-63-3, dated 2022-03-03, checked 2026-10-05.
