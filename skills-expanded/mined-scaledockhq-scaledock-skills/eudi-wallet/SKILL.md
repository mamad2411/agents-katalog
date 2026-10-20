---
name: eudi-wallet
description: >-
  EU Digital Identity Wallet ARF 3.0.0: build and review Wallet Units, PID and
  attestation issuers, and Relying Parties against the European Commission's
  Architecture and Reference Framework and its High-Level Requirements (HLRs).
  Use when working on the EUDI Wallet or eIDAS 2 (Regulation (EU) 2024/1183):
  Wallet Provider, Wallet Instance, WSCA/WSCD and keystores, PID Provider,
  QEAA, PuB-EAA and EAA Providers, Relying Party registration, access
  certificates and registration certificates, Trusted Lists and LoTEs, PID
  Rulebook, SD-JWT VC and ISO/IEC 18013-5 mdoc, OpenID4VCI with HAIP, Wallet
  Instance Attestation (WIA) and Key Attestation (KA), OpenID4VP over custom
  URI schemes or the W3C Digital Credentials API, ISO/IEC 18013-5 proximity and
  18013-7, Token Status List revocation, embedded disclosure policies,
  intermediaries, unlinkability, once-only and batch issuance, and pseudonyms.
  Targets ARF 3.0.0, upgrades from ARF 2.x and 1.x, and tracks the ARF main
  branch.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# EU Digital Identity Wallet (ARF)

The Architecture and Reference Framework (ARF), published by the European Commission with the European Digital Identity Cooperation Group in `eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework`, describes how EUDI Wallet Units, PID Providers, Attestation Providers and Relying Parties interoperate under Regulation (EU) 2024/1183. Its normative core is Annex 2: the High-Level Requirements (HLRs). With this skill the agent designs, builds or reviews one of those roles against ARF 3.0.0 and cites the HLR identifiers it meets.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Main-document rules cite the ARF section (§); HLRs cite their Annex 2 identifier (for example `RPA_03`). The ARF is informative: the Regulation and its implementing acts are the only legally binding requirements (§ 1.3), and the final requirements are those in the latest Annex 2 (§ 1.8). When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Wallet Provider (Wallet Unit), PID Provider, Attestation Provider (QEAA, PuB-EAA or non-qualified EAA), Relying Party, or intermediary. Registrars, Access CAs and Providers of registration certificates are out of scope except as inputs.
- Format and flow: SD-JWT VC or ISO/IEC 18013-5 mdoc; remote (custom URI or W3C Digital Credentials API, same-device or cross-device) or proximity.
- Attestation category: PID, QEAA, PuB-EAA or non-qualified EAA. It decides which trust list holds the trust anchor (§ 6.6.3.6).
- Target version: ARF 3.0.0 (current, the default). ARF 2.9.0 and ARF 1.10.0 are legacy: read them and upgrade from them, never author against them. ARF main branch is a preview (posture: track): never build from it. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, check the repository's releases for a newer tag, read its `CHANGELOG.md`, diff `hltr/high-level-requirements.csv` against the pinned tag, re-read every URL in [Sources](#sources), and update the pins.

## Invariants

1. **Two formats, both mandatory for Wallet Units.** Wallet Units support ISO/IEC 18013-5 mdoc and SD-JWT VC; W3C VCDM 2.0 is optional and only for non-qualified EAAs (§ 5.4.1; `ISSU_02`, `ARB_01`, `ARB_01a`). PID Providers issue every PID in both formats (`PID_02`).
2. **OpenID4VCI as profiled by HAIP for issuance.** Wallet Units and issuers support OpenID4VCI profiled by HAIP Sections 4 and 6, plus Technical Specification 3 for WIA and KA (`ISSU_01`, `ISSU_01a`; § 5.8).
3. **Proximity is ISO/IEC 18013-5; remote is OpenID4VP or ISO/IEC 18013-7.** Wallet Units support 18013-5 proximity, OpenID4VP with HAIP over redirects and over the Digital Credentials API, and 18013-7 Annex C over the DC API; 18013-7 Annex A is optional (§ 5.7.1; `OIA_01`, `OIA_01a`, `OIA_03b`–`OIA_03d`, `OIA_08`–`OIA_08b`).
4. **Every presentation authenticates the Relying Party with an access certificate.** In proximity and remote flows alike, the Wallet Unit authenticates the RP Instance, detects copied or replayed requests, and accepts only trust anchors from the Access CA LoTEs (§ 6.6.3.2; `RPA_01`–`RPA_04`).
5. **Every request carries one registration certificate.** It is a JWT bound to the access certificate by the same Relying Party identifier and Service identifier, and covers one intended use; the Wallet Unit warns when the request asks for attributes not in it (§ 3.19, § 6.6.3.3; `RPRC_17`, `RPRC_17a`, `RPRC_19`, `RPRC_21`).
6. **No attribute leaves the Wallet Unit without User approval.** The Wallet Unit authenticates the User first, shows the RP and Service trade names, the attributes, the intended use and privacy policy, and keeps authority over the decision; the browser and OS do not (§ 6.6.3.5; `OIA_06`, `RPA_06`–`RPA_08`, `RPA_10`).
7. **Verify against the right trust list.** PIDs and PuB-EAAs against their LoTEs, QEAAs against the Article 22 Trusted Lists, non-qualified EAAs as their Rulebook says; support both ETSI TS 119 612 and TS 119 602 (§ 6.6.3.6; `OIA_12`–`OIA_15b`).
8. **PIDs are device-bound to a WSCA/WSCD.** PID private keys are never in a plain keystore; ISO/IEC 18013-5 attestations are always device-bound, SD-JWT VC attestations should be (§ 4.3.2, § 6.6.3.8; `ISSU_17`, `ISSU_27`).
9. **WIA and KA go only to issuers.** Wallet Units present WIAs and KAs only to PID and Attestation Providers, never to Relying Parties, and send no KA for non-device-bound attestations (§ 6.5.3.4, § 6.5.3.5; `WUA_07`, `WUA_10a`, `WUA_24`).
10. **Revocable unless short-lived.** A PID, QEAA or PuB-EAA valid for more than 24 hours uses an Attestation Status List (Token Status List for SD-JWT VC) or, for mdoc only, an Attestation Revocation List; indices are random and lists are large enough for herd privacy (§ 6.6.3.7; `VCR_01`, `VCR_01b`, `VCR_11`, `VCR_11a`, `VCR_17`, `VCR_18`).
11. **Unique elements are unique and discarded.** Salts, hashes, revocation indices, device keys and signatures differ across attestations, and Relying Parties discard them once no longer needed (§ 7.4.3.5.1; `ISSU_35`, `OIA_16`). Wallet Units support once-only (method A) and limited-time (method B) attestations (`ISSU_37`).
12. **Remote responses are encrypted to the Relying Party Instance** (`OIA_09`), and cross-device DC API flows pass a proximity check (§ 4.4.3.3.3; `OIA_08g`).

## Workflow

1. **Pick the version.** Target ARF 3.0.0 and note which amended implementing acts the release aligns with.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is ARF 3.0.0, not a legacy tag or the main branch.
2. **Place the component in the trust model.** Name the role, its registration, its certificates, and the trust lists it reads or is listed in.
   -> [`references/roles-and-trust.md`](references/roles-and-trust.md)
   ✓ Every trust anchor the component uses has a named Trusted List or LoTE.
3. **Choose formats and identifiers.** Pick mdoc, SD-JWT VC or both from the PID Rulebook or the Attestation Rulebook, with the attestation type, namespace or `vct`, device binding and revocation method.
   -> [`references/credentials-and-formats.md`](references/credentials-and-formats.md)
   ✓ The Rulebook, attestation type and revocation method are written down.
4. **Build issuance.** Signed Credential Issuer metadata with access and registration certificates, Wallet Unit checks, WIA and KA validation, batch and re-issuance policy, embedded disclosure policy.
   -> [`references/issuance-and-presentation.md`](references/issuance-and-presentation.md)
   ✓ An issuer whose registration certificate lacks the attestation type is refused before the request.
5. **Build presentation.** Pick the transmission mechanism, then run Relying Party authentication, registration certificate checks, policy evaluation, User approval, and the RP-side verification steps.
   -> [`references/issuance-and-presentation.md`](references/issuance-and-presentation.md)
   ✓ A request with a broken access certificate chain is stopped, and an over-asking request triggers a warning.
6. **Review privacy.** Check unlinkability (methods A to D), discarded unique elements, WIA and KA exposure, pseudonym rules and status list herd privacy.
   -> [`references/credentials-and-formats.md`](references/credentials-and-formats.md)
   ✓ No value that is the same across presentations reaches a Relying Party unless the method allows it.
7. **Trace to HLRs.** Map each behaviour to its HLR identifier and look up the exact text in the CSV.
   -> [`references/requirements-index.md`](references/requirements-index.md)
   ✓ Every SHALL for the role is met or has a documented reason it does not apply.
8. **Upgrade** (only when asked). Follow the upgrade path from the source ARF line to 3.0.0.
   -> [`references/versions.md`](references/versions.md)
   ✓ The changed HLRs for the role are rechecked against the 3.0.0 CSV.

## Verify before done

- [ ] Each claim of conformance names an HLR identifier and the ARF 3.0.0 text matches the CSV.
- [ ] Both mdoc and SD-JWT VC work wherever the role requires both.
- [ ] Remote presentations use OpenID4VP with HAIP or ISO/IEC 18013-7, and the response is encrypted.
- [ ] Access certificate and registration certificate checks run on every request, with the identifier and Service identifier match.
- [ ] Trust anchors come from the right Trusted List or LoTE and are refreshed regularly.
- [ ] WIAs and KAs are never sent to a Relying Party.
- [ ] Revocation and unlinkability choices are documented per attestation type.
- [ ] Nothing is built from the main branch or a discussion paper.

## Reference index

- **`references/versions.md`**: ARF lines, which to use, what changed, upgrade steps and the main-branch preview. Load for steps 1 and 8.
- **`references/roles-and-trust.md`**: roles, registration, access and registration certificates, Trusted Lists and LoTEs, Wallet Unit components, WIA and KA, lifecycles and Wallet Unit revocation. Load for step 2.
- **`references/credentials-and-formats.md`**: attestation categories, mdoc and SD-JWT VC, PID identifiers, Rulebooks, revocation, unlinkability methods and pseudonyms. Load for steps 3 and 6.
- **`references/issuance-and-presentation.md`**: OpenID4VCI issuance checks, embedded disclosure policies, remote and proximity flows, Relying Party authentication, User approval, RP verification and intermediaries. Load for steps 4 and 5.
- **`references/requirements-index.md`**: how Annex 2 is organised, identifier prefixes per topic, and the HLRs to check per role. Load for step 7.

## Related skills

- `openid4vc` for OpenID4VCI, OpenID4VP, DCQL, the Digital Credentials API and HAIP: `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`.
- `sd-jwt` for SD-JWT, SD-JWT VC and key binding: `npx skills add ScaleDockHQ/scaledock-skills --skill sd-jwt`.
- `vc-data-model` for W3C VCDM 2.0 attestations: `npx skills add ScaleDockHQ/scaledock-skills --skill vc-data-model`.
- `did` for W3C Decentralized Identifiers: `npx skills add ScaleDockHQ/scaledock-skills --skill did`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [ARF repository at v3.0.0](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/tree/v3.0.0) (main document chapters 1 to 7, Annex 2, technical specifications index): Released, v3.0.0 (21 July 2026, commit c64f2cb), checked 2026-10-05.
- [ARF High-Level Requirements CSV at v3.0.0](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/v3.0.0/hltr/high-level-requirements.csv): Released, v3.0.0 (725 rows), checked 2026-10-05.
- [ARF releases](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/releases): release index, v1.0.0 to v3.0.0, checked 2026-10-05.
- [ARF changelog](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/CHANGELOG.md): changelog on main, entries 1.0.0 to 3.0.0, checked 2026-10-05.
- [ARF repository at v2.9.0](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/tree/v2.9.0): Released, v2.9.0 (21 May 2026), checked 2026-10-05.
- [ARF repository at v1.10.0](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/tree/v1.10.0): Released, v1.10.0 (2 May 2025), checked 2026-10-05.
- [ARF repository main branch](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/tree/main): development branch, commit f5789a7 (2 October 2026), checked 2026-10-05.
- [ARF published site](https://eu-digital-identity-wallet.github.io/eudi-doc-architecture-and-reference-framework/) (redirects to eudi.dev): published site, shows v3.0.0 (21 July 2026), checked 2026-10-05.
- [Regulation (EU) 2024/1183](https://eur-lex.europa.eu/eli/reg/2024/1183/oj) (amending Regulation (EU) No 910/2014; Articles 5a and 5b cited): Regulation, in force, OJ L 2024/1183 of 30 April 2024, checked 2026-10-05.
