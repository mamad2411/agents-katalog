---
name: eu-age-verification
description: >-
  EU Age Verification blueprint: issue and verify privacy-preserving proof-of-age (age_over_18) attestations as ISO mDoc over OpenID4VCI, OpenID4VP and the W3C Digital Credentials API, with zero-knowledge proofs. Covers the European Commission age verification technical specification and Annex A profile at commit 8b97287 (2026-09-02), with v1.0.6 as legacy. Use when building an age verification app, attestation provider or relying party for online services protecting minors. Triggers: EU age verification, mini wallet, proof of age, eu.europa.ec.av.1, age_over_18, DSA Article 28.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# EU Age Verification

The European Commission's age verification solution: the Operational, Security, Product, and Architecture Specifications and Annex A, the Age Verification Profile, published in the `eu-digital-identity-wallet/av-doc-technical-specification` repository. It defines enrolment, batch issuance of Proof of Age attestations, presentation with zero-knowledge proofs or plain ISO mDoc, and the trusted list of Attestation Providers.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Attestation Provider (issuing service), Age Verification App (holder), or Relying Party (verifier).
- Target version: EU Age Verification 2026-09-02 (current, posture: build); EU Age Verification v1.0.6 (legacy). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ A.4.1.** "The document type for Proof of Age attestation SHALL be `eu.europa.ec.av.1`."
2. **§ A.4.2.** "A Proof of Age Attestation SHALL NOT include any other attribute."
3. **§ A.6.** "A plain ISO mDoc presentation SHALL be used as the fallback where, and only where, either (a) the User's device does not support Zero-Knowledge Proof generation, or (b) the OpenID for Verifiable Presentations transport is used."
4. **§ A.7.** "All entities MUST support P-256 (secp256r1) as a key type with ES256 JWT algorithm for signing and signature validation whenever this profile requires to do so."
5. **§ A.8.** "An RP SHALL verify that the Zero-Knowledge Proof was generated using an accepted circuit, by verifying the circuit hash against the set of circuits accepted for the purposes of this profile, before verifying the proof."
6. **§ A.8.** "The RP SHALL be able to verify both a Zero-Knowledge Proof presentation and the plain ISO mDoc fallback presentation."
7. **§ A.9.** "A Relying Party SHALL NOT reject a presentation solely on the ground that it uses the plain ISO mDoc fallback mechanism."
8. **§ 3.2.4.** "To distinguish an authorised AP from an unauthorised one, all APs MUST be registered with the EU and included in a centrally maintained trusted list."
9. **§ 3.4.1.** "Since neither the Attestation Provider nor the Age Verification App Instance can determine, at issuance time, whether the fallback presentation mechanism will be required, the system SHALL support the issuance of attestations in batches so that the User has several attestations available."
10. **§ 4.2.** "Where a Proof of Age attestation is presented as a plain ISO mDoc, the Age Verification App SHALL use a Proof of Age attestation only once and SHALL then remove it from the batch of the issued attestations."

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
- [ ] An issued attestation uses document type `eu.europa.ec.av.1` and carries no attribute outside the Annex A § A.4.2 table.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `eudi-wallet`, `openid4vc`, `digital-credentials`, `eidas`, `eu-dsa`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Age verification: Operational, Security, Product, and Architecture Specifications](https://raw.githubusercontent.com/eu-digital-identity-wallet/av-doc-technical-specification/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/architecture-and-technical-specifications.md): European Commission technical specification, commit 8b97287, 2026-09-02, checked 2026-10-06.
- [Age verification Annex A: Age Verification Profile](https://raw.githubusercontent.com/eu-digital-identity-wallet/av-doc-technical-specification/8b9728752bd8d8eede6077ade4be8900949de2d9/docs/annexes/annex-A/annex-A-av-profile.md): European Commission technical specification, commit 8b97287, 2026-09-02, checked 2026-10-06.
