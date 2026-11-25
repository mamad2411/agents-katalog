---
name: refeds-profiles
description: >-
  REFEDS profiles: signal MFA, SFA, assurance (RAF), Sirtfi and entity categories in research and education identity federations. Covers REFEDS MFA Profile 2.0 (current) and 1.2, SFA Profile 1.0, Assurance Framework 2.0 and 1.0, Sirtfi 2.0 and 1.0, Research and Scholarship 1.3, and the Personalized, Pseudonymous and Anonymous Access entity categories v2. Use when an IdP, OP, SP or RP in a SAML or OIDC federation (eduGAIN, InCommon) requests or asserts https://refeds.org/profile/mfa, releases eduPersonAssurance values, or tags metadata with an entity category. Triggers: REFEDS, MFA profile, AuthnContextClassRef, acr, RAF, IAP, eduPersonAssurance, Sirtfi, R&S, entity category, eduGAIN.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# REFEDS profiles and entity categories

REFEDS (Research and Education FEDerations) profiles for federated SAML and OpenID Connect: the MFA and SFA authentication context profiles, the REFEDS Assurance Framework, the Sirtfi incident response framework and the Research and Scholarship, Personalized, Pseudonymous and Anonymous Access entity categories. The texts are the versions REFEDS deposited on Zenodo.

**Scope.** refeds.org refuses automated fetches, so the pinned texts are the copies REFEDS deposited on Zenodo. REFEDS MFA Profile 2.0 and Sirtfi 2.0 are published only on refeds.org: the lines are listed so you can name them, but their text is not pinned. MFA 2.0 keeps the 1.2 semantics as General MFA and adds a Phishing-Resistant MFA identifier; check refeds.org for that identifier before you emit it.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Identity Provider (IdP) or OpenID Provider (OP), Service Provider (SP) or Relying Party (RP), or federation registrar.
- Target version: REFEDS MFA Profile 2.0 (current); REFEDS MFA Profile 1.2 (supported); REFEDS SFA Profile 1.0 (current); REFEDS Assurance Framework 2.0 (current); REFEDS Assurance Framework 1.0 (supported); Sirtfi 2.0 (current); Sirtfi 1.0 (supported); Research and Scholarship 1.3 (current); Access entity categories v2 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 4.** "An IdP MUST NOT do so when a bypass or omission of one or more factors occurs (e.g., failing “open” for reliability of local services)."
2. **§ 4.1.** "The authentication of the user’s current session MUST use a combination of at least two of the four distinct types of factors, that is something an entity has (e.g., a hardware device containing a credential), something an entity knows (e.g., password), something an entity is (e.g., biometric), something an entity does (e.g., behavioural)."
3. **§ 4.2.** "Subsequently, the factors used MUST be independent; this includes processes to recover, replace, or add authentication factors."
4. **§ 5.2.1.** "The use of the acr_values parameter MUST NOT be used for this purpose, because it signals a non-essential or voluntary claim requirement, and cannot cause the OP to enforce the use of the Profile."
5. **§ 4.** "Authentication secrets at rest and in online transit must be cryptographically protected."
6. **§ 3.** "If a CSP is releasing any other assurance values in this framework for a Person it MUST also release: https://refeds.org/assurance"
7. **§ 5.1.1.** "A unique identifier MUST represent one and only one Person in the CSP’s system."
8. **§ 5.2.1.** "A CSP asserting an IAP value of “high” for a user MUST also assert the IAP values “medium” and “low” for that user."
9. **§ 2.1.** "[OS1] Security patches in operating system and application software are applied in a timely manner."
10. **§ 7.** "An Identity Provider that does not release all of the required elements of the R&S attribute bundle (defined in section 5), for any reason, SHALL NOT exhibit the R&S entity attribute in its metadata."
11. **§ 5.1.** "The requirement to support the REFEDS Assurance Framework implies that at least one value, 'https://refeds.org/assurance' MUST be supplied, but no others are specifically required unless the IdP deems them to be applicable."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] An IdP or OP asserts https://refeds.org/profile/mfa only when every factor was applied, and an SP or RP handles the error response.
- [ ] Every eduPersonAssurance value is sent exactly as written in RAF, including case.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `saml`, `openid-connect`, `openid-federation`, `nist-800-63`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [REFEDS Multi-Factor Authentication Profile v1.2](https://zenodo.org/records/10135577): REFEDS Final, Version 1.2, 2023-11-15, checked 2026-10-06.
- [REFEDS MFA (wiki page naming the current profile)](https://wiki.refeds.org/spaces/PRO/pages/22544394/MFA): REFEDS wiki, Page version of 2026-06-30, checked 2026-10-06.
- [Consultation: MFA Profile v2.0](https://wiki.refeds.org/spaces/CON/pages/418414593/Consultation+MFA+Profile+v2.0): REFEDS wiki, Closed consultation page summarising the 2.0 changes, checked 2026-10-06.
- [REFEDS SFA Profile v1.0](https://zenodo.org/records/5113499): REFEDS Final, Version 1.0, 2018-08-28, checked 2026-10-06.
- [REFEDS Assurance Framework v2.0](https://zenodo.org/records/10277233): REFEDS Final, Version 2.0, 2023-12-05, checked 2026-10-06.
- [Security Incident Response Trust Framework for Federated Identity (Sirtfi) v1.0](https://zenodo.org/records/1256531): REFEDS Final, Version 1.0, 2015-12-14, checked 2026-10-06.
- [Consultation: Sirtfi v2](https://wiki.refeds.org/spaces/CON/pages/100270114/Consultation+Sirtfi+v2): REFEDS wiki, Consultation page with the v1 and v2 coexistence note, checked 2026-10-06.
- [REFEDS Research and Scholarship Entity Category v1.3](https://zenodo.org/records/4700413): REFEDS Final, Version 1.3, 2016-09-16, checked 2026-10-06.
- [Personalized Access Entity Category v2](https://zenodo.org/records/7684449): REFEDS Final, Version 2, 2023-02-13, checked 2026-10-06.
- [Pseudonymous Access Entity Category v2](https://zenodo.org/records/7684488): REFEDS Final, Version 2, 2023-02-13, checked 2026-10-06.
- [REFEDS Anonymous Access Entity Category v2](https://zenodo.org/records/7816828): REFEDS Final, Version 2, 2021-03-15, checked 2026-10-06.
