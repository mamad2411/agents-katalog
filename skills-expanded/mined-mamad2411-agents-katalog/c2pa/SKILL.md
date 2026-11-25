---
name: c2pa
description: >-
  C2PA 2.4 Content Credentials: build, sign and validate C2PA manifests, claims
  and assertions. Use when embedding or reading Content Credentials (a C2PA
  Manifest Store in JUMBF or an application/c2pa sidecar), writing a
  c2pa.claim.v2, recording actions such as c2pa.created and c2pa.edited with an
  IPTC digitalSourceType for AI-generated content, adding ingredients, data,
  box, BMFF or collection hash bindings, thumbnails, soft bindings and
  watermarks, or metadata, signing claims with COSE and X.509 certificates,
  RFC 3161 time-stamps and OCSP, configuring the C2PA Trust List and TSA Trust
  List, or implementing the Well-Formed, Valid and Trusted states and status
  codes. Also covers the Conformance Program's extra requirements and the AI/ML
  guidance. Targets C2PA 2.4; supports C2PA 2.3 and C2PA 2.2, upgrades from
  C2PA 2.1, C2PA 2.0 and C2PA 1.4 (claim v1); no draft is published.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# C2PA (Content Credentials)

The C2PA Technical Specification defines Content Credentials: a signed, tamper-evident record of an asset's provenance, made of manifests that hold assertions (actions, ingredients, content bindings, metadata), a claim listing them, and a COSE claim signature backed by an X.509 certificate. This skill pins C2PA 2.4 and produces a claim generator, a validator, or a review that meets its normative rules.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites; section numbers are from C2PA 2.4 unless another version is named. When a rule and the pinned source disagree, the source wins; when the source has a newer version than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: claim generator (creates and signs manifests), validator (manifest consumer), or both, for example an editor that validates ingredients before signing.
- Target version: C2PA 2.4 (current, the default; the newest version on spec.c2pa.org). C2PA 2.3 and C2PA 2.2 are supported: produce them only for a named consumer that needs them, and for the Conformance Program pick 2.4 or 2.2, the versions it accepts. C2PA 2.1, C2PA 2.0 and C2PA 1.4 (with 1.0 to 1.3) are legacy: validate and upgrade from them, never author them. No draft is published, so there is no preview line. See [`references/versions.md`](references/versions.md).
- Revision: the version history entry of the target (§ 5.3), recorded as `specVersion` in `claim_generator_info`.
- Asset formats: which media types are produced or read (JPEG, PNG, BMFF video, PDF, ZIP, fonts, text, HTML, live video, or a collection of files), and whether the manifest is embedded or external.
- Content origin: captured, edited, composited, or created with generative AI, which decides the `digitalSourceType` and the AI Disclosure assertion.
- Signing: algorithm, certificate source (a CA on the C2PA Trust List or a private PKI), time-stamp authority, and OCSP availability.
- Conformance: whether the product will apply to the C2PA Conformance Program.
- Sources refresh: when refreshing this skill or when a rule looks out of date, open the specifications index for a newer version, read its § 5.3 version history and Appendix C, then re-read every URL in [Sources](#sources). Update the pins and bump the version.

## Invariants

1. **Everything lives in a Manifest Store.** Manifests, assertion stores, claims and signatures are processed only inside a `c2pa` JUMBF superbox, and the last manifest in the store is the active one (§ 11.1.2, § 15.5.1).
2. **Write claim v2.** Generators write `c2pa.claim.v2` in core deterministic CBOR with `instanceID`, `claim_generator_info` (with `name`), `signature` and `created_assertions`; validators reject a claim missing any of them (§ 10.1, § 10.2.2, § 15.6.2).
3. **Every assertion is declared and hashed.** Each assertion in the store is referenced from `created_assertions` or `gathered_assertions` by a hashed URI that resolves inside the same manifest; anything else is `assertion.undeclared`, `assertion.outsideManifest` or `assertion.hashedURI.mismatch` (§ 10.3.2.1, § 15.10.3.1).
4. **One hard binding per standard manifest, none in an update manifest.** Exactly one of `c2pa.hash.data`, `c2pa.hash.boxes`, `c2pa.hash.bmff.v3` or `c2pa.hash.collection.data` per standard manifest (§ 9.1, § 11.2.2, § 15.10.1.2); update manifests carry no hard binding, thumbnail or multi-asset hash (§ 11.2.3).
5. **Actions start the history.** A standard manifest has an actions assertion in `created_assertions` whose first action is `c2pa.created` (with a `digitalSourceType`) or `c2pa.opened` (referencing its `parentOf` ingredient), and only one of either per manifest (§ 18.15.2).
6. **Ingredients are validated and linked.** A `c2pa.ingredient.v3` has a `relationship` of `parentOf`, `componentOf` or `inputTo`; one with a manifest carries `activeManifest`, `claimSignature` and the generator's `validationResults`; at most one `parentOf` (§ 15.2.1, § 15.10.1.2, § 18.16).
7. **Only the allowed algorithms.** Hashes are SHA-256, SHA-384 or SHA-512; signatures are ES256/384/512, PS256/384/512 (RSA keys of at least 2048 bits) or Ed25519; anything else is `algorithm.unsupported` and implementations do not add optional algorithms (§ 13.1, § 13.2.1).
8. **COSE with exactly one X.509 credential.** The claim signature is a detached `COSE_Sign1_Tagged` over the claim box, with `alg` and `x5chain` (label 33, end-entity first, all intermediates) in the protected header; zero or several credentials are rejected (§ 13.2, § 14.2, § 14.5).
9. **Certificates follow the profile.** Signers are end-entity certificates with `digitalSignature`, a non-empty EKU without `anyExtendedKeyUsage`, and a chain to a trust anchor for one of their EKUs, including `c2pa-kp-claimSigning` against the C2PA Trust List (§ 14.4.1, § 14.5.1).
10. **Time-stamp with `sigTst2`.** One RFC 3161 time-stamp per manifest over the signature (v2 payload), with `certReq`; it is required when OCSP responses are stapled in `rVals`; CRLs are not used (§ 10.3.2.5, § 10.3.2.6, § 14.5.2).
11. **States are cumulative.** Well-Formed, then Valid (`claimSignature.validated`, `claimSignature.insideValidity`, not `signingCredential.ocsp.revoked`), then Trusted (`signingCredential.trusted`); an asset is Valid only when its content bindings also match (§ 14.3).
12. **Do not present invalid provenance as fact.** Data from manifests or assets that are not Valid is not shown, or is shown with a warning that it is not valid and not attributable to the signer (§ 15.3).
13. **Never write deprecated constructs.** Generators write nothing marked deprecated in Appendix C for their target version; validators should still read them (§ 5.1, § 6.3, Appendix C).

## Workflow

1. **Pick the version and scope.** Confirm the role, formats and target version from Inputs.
   -> [`references/versions.md`](references/versions.md)
   ✓ The design names C2PA 2.4 (or a supported line with a named reason) and writes that `specVersion` in `claim_generator_info`.
2. **Choose the binding and embedding.** Pick the hard binding for each format, prefer box hashing where the format allows, and decide between an embedded store and an external `application/c2pa` store.
   -> [`references/manifests-and-claims.md`](references/manifests-and-claims.md), [`references/assertions.md`](references/assertions.md)
   ✓ Each format has exactly one hard binding type and a documented store location.
3. **Write the assertions.** Actions (with `digitalSourceType` and `allActionsIncluded`), ingredients with their validation results, thumbnails, metadata, soft bindings, and AI Disclosure for model output; salt every assertion.
   -> [`references/assertions.md`](references/assertions.md)
   ✓ The first action is `c2pa.created` or `c2pa.opened`, and each ingredient matches an action.
4. **Build the claim and the store.** Fill `created_assertions` and `gathered_assertions`, copy ingredient manifests with the label-conflict rules, and use multiple step processing where offsets must be fixed before signing.
   -> [`references/manifests-and-claims.md`](references/manifests-and-claims.md)
   ✓ Every assertion in the store appears in the claim, and every hashed URI resolves.
5. **Sign, time-stamp and staple.** Sign the claim with a profile-conforming certificate, add a `sigTst2` time-stamp, and staple OCSP responses.
   -> [`references/signing-and-trust.md`](references/signing-and-trust.md)
   ✓ The signature verifies against the claim box bytes, and the time-stamp imprint matches the signature.
6. **Configure trust (validator).** Load the C2PA Trust List and TSA Trust List as separate anchor sets per EKU, keep them refreshed, and keep any private credential store user-managed.
   -> [`references/signing-and-trust.md`](references/signing-and-trust.md)
   ✓ A test manifest signed under the C2PA Trust List reports `signingCredential.trusted`; one from an unknown CA reports `signingCredential.untrusted`.
7. **Validate.** Locate the active manifest, then check the claim, algorithms, signature, time-stamp, revocation, assertions, ingredients and content, and return the status codes.
   -> [`references/validation.md`](references/validation.md)
   ✓ A changed byte inside the bound content gives a hash mismatch failure, and an unchanged asset is Valid.
8. **Check conformance (if applying).** Apply the Conformance Program's additional requirements and produce crJSON validation output from a test harness.
   -> [`references/signing-and-trust.md`](references/signing-and-trust.md)
   ✓ Sample manifests carry `specVersion` and `allActionsIncluded`, and the harness accepts an asset, trust lists and a validation time.
9. **Upgrade** (only when asked). Follow the step-by-step checklists from the source version to C2PA 2.4.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded generator passes the Verify list below, and older assets are kept as ingredients rather than rewritten.

## Verify before done

- [ ] The store is a single `c2pa` superbox, the active manifest is last, and the asset has no second embedded store.
- [ ] The claim is `c2pa.claim.v2` with `instanceID`, `claim_generator_info.name`, `signature`, `created_assertions`, and `specVersion` in `claim_generator_info`.
- [ ] Every assertion has a salt and is listed in the claim; none is a deprecated construct.
- [ ] A standard manifest has one hard binding, one actions assertion starting with `c2pa.created` or `c2pa.opened`, and at most one `parentOf` ingredient.
- [ ] AI-generated content uses `c2pa.created` with an IPTC `trainedAlgorithmicMedia` (or matching) `digitalSourceType`.
- [ ] The signature uses an allowed algorithm and key, a single `x5chain` (label 33) in the protected header, and a certificate that passes the profile.
- [ ] There is a `sigTst2` time-stamp, and stapled OCSP responses sit in `rVals`.
- [ ] The validator reports Well-Formed, Valid and Trusted using the standard status codes, and an edited asset fails its content binding.
- [ ] The UI hides or warns about data that is not Valid.

## Reference index

- **`references/versions.md`**: every version line, what each changed, which to produce, the upgrade checklists from 1.x through 2.3, and the preview policy. Load for steps 1 and 9.
- **`references/manifests-and-claims.md`**: JUMBF boxes and UUIDs, manifest types, URNs and hashed URIs, claim v2 fields, signing order, multiple step processing, embedding and external stores, redaction.
- **`references/assertions.md`**: labels, actions and `digitalSourceType`, AI Disclosure and the AI/ML guidance, ingredients, hard and soft bindings, thumbnails, embedded and external data, metadata, time-stamp and certificate status assertions.
- **`references/signing-and-trust.md`**: hash and signature algorithms, COSE, the certificate profile, time-stamps, OCSP, validator trust configuration, the C2PA Trust List, and the Conformance Program.
- **`references/validation.md`**: the validation states, result reporting, the step-by-step algorithm with status codes, ingredient recursion, content checks, and display rules.

## Related skills

- `eu-ai-act`, for transparency duties on AI-generated or manipulated content: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-ai-act`
- `nist-ai-rmf`, for AI risk management that content provenance supports: `npx skills add ScaleDockHQ/scaledock-skills --skill nist-ai-rmf`
- `scitt`, for transparency logs of signed statements next to Content Credentials: `npx skills add ScaleDockHQ/scaledock-skills --skill scitt`
- `jwt`, for JOSE-based signing when a system uses JWTs alongside COSE: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [C2PA Specifications index](https://spec.c2pa.org/specifications/specifications/2.4/index.html): Published, lists 2.4 as the newest version (c2pa.org/specifications redirects here), checked 2026-10-05.
- [C2PA Technical Specification 2.4](https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html): Published, 2.4 (April 2026), checked 2026-10-05.
- [C2PA Technical Specification 2.3](https://spec.c2pa.org/specifications/specifications/2.3/specs/C2PA_Specification.html): Published, 2.3 (December 2025; GitHub release 2026-01-11), checked 2026-10-05.
- [C2PA Technical Specification 2.2](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html): Published, 2.2 (May 2025), checked 2026-10-05.
- [C2PA Technical Specification 2.1](https://spec.c2pa.org/specifications/specifications/2.1/specs/C2PA_Specification.html): Published, 2.1 (September 2024), checked 2026-10-05.
- [C2PA Technical Specification 2.0](https://spec.c2pa.org/specifications/specifications/2.0/specs/C2PA_Specification.html): Published, 2.0 (January 2024), checked 2026-10-05.
- [C2PA Technical Specification 1.4](https://spec.c2pa.org/specifications/specifications/1.4/specs/C2PA_Specification.html): Published, 1.4 (November 2023), checked 2026-10-05.
- [C2PA Guidance for Artificial Intelligence and Machine Learning](https://spec.c2pa.org/specifications/specifications/2.4/ai-ml/ai_ml.html): Informative document, 2.4 site build, checked 2026-10-05.
- [c2pa-org/specifications](https://github.com/c2pa-org/specifications): Source repository, latest release 2.3, no branch for a later version, checked 2026-10-05.
- [C2PA Conformance](https://c2pa.org/conformance/): Program page, Interim Trust List frozen 2026-01-01 and retired, checked 2026-10-05.
- [C2PA Conformance Program](https://github.com/c2pa-org/conformance-public/blob/main/docs/v0.2/C2PA%20Conformance%20Program.md): v0.2, released 2026-07-31 (accepts spec 2.2 and 2.4), checked 2026-10-05.
- [Additional Conformance Requirements Against the Content Credentials Specification](https://github.com/c2pa-org/conformance-public/blob/main/docs/v0.2/Additional%20Conformance%20Requirements%20Against%20the%20Content%20Credentials%20Specification.md): v0.2, 2026-07-31, checked 2026-10-05.
- [C2PA Trust List and TSA Trust List](https://github.com/c2pa-org/conformance-public/tree/main/trust-list): Published lists, issued 2026-08-05, next update 2027-08-05, checked 2026-10-05.
