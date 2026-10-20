---
name: vc-data-model
description: >-
  W3C Verifiable Credentials Data Model 2.0: build, secure, verify and
  validate verifiable credentials and presentations. Use when issuing or
  checking a VC or VP, writing @context
  (https://www.w3.org/ns/credentials/v2), type, issuer, credentialSubject,
  validFrom, validUntil, credentialStatus, credentialSchema, relatedResource,
  refreshService, termsOfUse or evidence, wrapping credentials as
  EnvelopedVerifiableCredential, choosing application/vc or application/vp,
  deciding between JSON-LD and plain JSON processing, or reviewing VC privacy
  and security. Covers VC JOSE COSE (vc+jwt, vc+sd-jwt, vc+cose), VC Data
  Integrity 1.0, and Bitstring Status List 1.0 revocation and suspension.
  Upgrades VC Data Model 1.1 (issuanceDate, expirationDate, vc and vp JWT
  claims) and tracks the VC Data Model 2.1, VC Data Integrity 1.1 and
  Bitstring Status List 1.1 drafts. Also Controlled Identifiers v1.0, VC JSON
  Schema, VC Barcodes, VC Rendering Methods, VC Confidence Methods, VC Forgery
  Defense and VCALM.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Verifiable Credentials Data Model

The W3C Verifiable Credentials Data Model v2.0 (VCDM) defines how an issuer expresses claims about subjects as a tamper-evident verifiable credential, how a holder combines credentials into a verifiable presentation, and how a verifier checks them. Companion W3C Recommendations secure the data model (VC JOSE COSE and VC Data Integrity 1.0) and publish revocation and suspension status (Bitstring Status List 1.0). With this skill the agent produces conforming credentials and presentations, secures them, and builds verifiers that verify and then validate them.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Bare section numbers (§ 4.7) refer to VC Data Model 2.0; other specifications are named with the section. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: issuer, holder (wallet), verifier, status list publisher, or the author of a credential type or extension context.
- Target version: VC Data Model 2.0 (current, the default), secured with VC JOSE COSE or VC Data Integrity 1.0, with status from Bitstring Status List 1.0; each is the current line of its own family. VC Data Model 1.1 is legacy: read it and upgrade from it, never author it. VC Data Model 2.1, VC Data Integrity 1.1 and Bitstring Status List 1.1 are previews (posture: track): never emit anything only they define. Controlled Identifiers v1.0 is current. VC JSON Schema is current with posture build. VC Barcodes, VC Rendering Methods, VC Confidence Methods, VC Forgery Defense and VCALM are each current with posture track, because each family's only text is a Working Draft. See [`references/versions.md`](references/versions.md).
- Securing mechanism: enveloping (JWT, SD-JWT or COSE through VC JOSE COSE) or embedded (a Data Integrity cryptosuite). Name the cryptosuite or the `typ`.
- Processing mode: general JSON-LD processing (a JSON-LD library, required by the `-rdfc-` and SD cryptosuites) or type-specific credential processing (plain JSON against a fixed, hashed set of contexts).
- Disclosure needs: full disclosure, selective disclosure (SD-JWT, `ecdsa-sd-2023`, `bbs-2023`) or unlinkable disclosure (`bbs-2023`).
- Status: none, revocation, suspension, or status messages.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the W3C history page of each specification for a newer Recommendation or draft, check the [VC Overview](https://www.w3.org/TR/vc-overview/) for status changes (for example BBS reaching Recommendation), and update the pins.

## Invariants

1. **Base context first.** Every credential and presentation has `@context`, an ordered set whose first item is `https://www.w3.org/ns/credentials/v2`; later items are URLs or objects processable as JSON-LD contexts (§ 4.3).
2. **Types.** Every credential has a `type` that includes `VerifiableCredential`; every presentation includes `VerifiablePresentation`; `credentialStatus`, `credentialSchema`, `refreshService`, `termsOfUse` and `evidence` objects each carry a `type` (§ 4.5, § 4.13).
3. **Issuer and subject.** A credential MUST have `issuer` (a URL, or an object whose `id` is a URL) and `credentialSubject` (one or more objects, never strings) (§ 4.7, § 4.8).
4. **Identifiers and times.** `id` is a single URL (§ 4.4). `validFrom` and `validUntil` are optional `dateTimeStamp` strings, with `validFrom` not later than `validUntil` (§ 4.9); values without an offset are read as UTC (§ 5.8).
5. **Secured or not a VC.** A conforming document is compacted JSON-LD, has media type `application/vc` or `application/vp`, and is secured by at least one securing mechanism; issuers MUST secure what they produce (§ 1.3, § 6.1).
6. **Credentials in presentations are objects.** `verifiableCredential` values are verifiable credentials or `EnvelopedVerifiableCredential` objects whose `id` is a `data:` URL, never bare strings or URLs (§ 4.13).
7. **Verifiers verify before they validate.** Run the § 7.1 algorithm (securing mechanism, then conforming-document check), report `CRYPTOGRAPHIC_SECURITY_ERROR` or `MALFORMED_VALUE_ERROR`, and only then apply validity period, status, schema and issuer-trust checks (§ 7.1, § 7.2, Appendix A).
8. **Understand every context.** Applications MUST understand each JSON-LD context they use (§ 4.3); Data Integrity verifiers MUST run context validation or an equivalent (VC Data Integrity § 2.4.1). The base context is treated as already retrieved with SHA-256 `59955ced6697d61e03f2b2556febe5308ab16842846f5b586d7f1f7adec92734` (§ B.1).
9. **No silent term loss.** JSON-LD expansion errors fail verification (§ B.1); JSON-LD processors MUST error when data is dropped, for example on an undefined term (VC Data Integrity § 2.4.3). Without full term definitions, `https://www.w3.org/ns/credentials/undefined-terms/v2` is the last context (§ 5.2).
10. **Digests are checked.** A verifier that uses a `relatedResource` MUST compute its digest and error on mismatch (§ 5.3).
11. **JOSE payload is the credential.** With VC JOSE COSE the unsecured credential is the JWS payload; `vc` and `vp` claims MUST NOT appear, unsecured JWT claim sets are ignored, and an `iss` MUST match `issuer` or `issuer.id` (VC JOSE COSE § 1.1.2.1, § 3.1.3, § 4.1.2).
12. **Data Integrity proofs are complete.** A `proof` has `type`, `proofPurpose` and `verificationMethod`; `DataIntegrityProof` requires `cryptosuite` and `proofValue`; verifiers check the expected purpose, `domain` and `challenge` (VC Data Integrity § 2.1, § 3.1, § 4.4).
13. **Status does not phone home.** Status schemes MUST NOT let the issuer learn which verifier checks which holder (§ 4.10); Bitstring Status List bitstrings are at least 131,072 entries (Bitstring Status List § 2.2, § 3.2).

## Workflow

1. **Pick the versions.** Target VC Data Model 2.0 with the current securing and status lines. If the input uses `https://www.w3.org/2018/credentials/v1`, plan an upgrade (step 9).
   -> [`references/versions.md`](references/versions.md)
   ✓ The design names the data model, securing mechanism and status lines, and none is legacy or preview.
2. **Model the credential.** Write `@context`, `type`, `issuer`, `credentialSubject` and the optional properties; publish a context and vocabulary for new terms, or add `undefined-terms/v2` while prototyping.
   -> [`references/data-model.md`](references/data-model.md)
   ✓ The unsecured credential meets every MUST in § 4 to § 6, and the examples context is not used outside examples.
3. **Choose the processing mode.** Decide between general JSON-LD processing and type-specific processing, and pin the expected context list with hashes.
   -> [`references/data-model.md`](references/data-model.md)
   ✓ The context list, its order and its hashes are fixed and documented.
4. **Secure it.** Use VC JOSE COSE (`vc+jwt`, `vc+sd-jwt`, `vc+cose`) or a Data Integrity cryptosuite; publish keys the verifier can discover.
   -> [`references/securing.md`](references/securing.md)
   ✓ The verifier can find the key from `kid`, `iss` or `verificationMethod`, and verification returns the original credential.
5. **Add status if needed.** Publish a `BitstringStatusListCredential`, assign random indexes, and add a `BitstringStatusListEntry`.
   -> [`references/status-lists.md`](references/status-lists.md)
   ✓ The list decodes to at least 131,072 entries and the entry's purpose appears in the list.
6. **Present.** Wrap credentials in a presentation (embedded or `EnvelopedVerifiableCredential`), bound to the verifier's challenge and domain or audience.
   -> [`references/data-model.md`](references/data-model.md), [`references/securing.md`](references/securing.md)
   ✓ A replayed presentation with an old challenge is rejected.
7. **Verify, then validate.** Run the verification algorithm, then validity period, status, schema, issuer trust and fitness for purpose; report errors as Problem Details.
   -> [`references/validation.md`](references/validation.md)
   ✓ A tampered credential fails with `CRYPTOGRAPHIC_SECURITY_ERROR`, and an expired or revoked one fails validation.
8. **Review privacy and security.** Go through correlation, data minimization, bearer credentials, status lookups and the security considerations.
   -> [`references/validation.md`](references/validation.md)
   ✓ Every item has a mitigation or a reason it does not apply.
9. **Upgrade** (only when asked). Follow the VC Data Model 1.1 to 2.0 steps.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded credential uses the v2 context, `validFrom` and `validUntil`, a current securing mechanism, and verifies.

## Verify before done

- [ ] `@context[0]` is exactly `https://www.w3.org/ns/credentials/v2` and every other context is pinned by hash or a local copy (§ 4.3, § B.1).
- [ ] `type` includes `VerifiableCredential` or `VerifiablePresentation` plus a narrower type (§ 4.5).
- [ ] `issuer` is a URL or an object with a URL `id`; `credentialSubject` holds objects (§ 4.7, § 4.8).
- [ ] Every time value is a `dateTimeStamp` with `Z` or an offset, and `validFrom` ≤ `validUntil` (§ 4.9, § 5.8).
- [ ] The credential is secured; JOSE payloads have no `vc` or `vp` claim and use `typ` `vc+jwt`, `vc+sd-jwt` or `application/vc+cose`; Data Integrity proofs have `type`, `cryptosuite`, `proofPurpose`, `verificationMethod` and `proofValue` (VC JOSE COSE § 3; VC Data Integrity § 2.1).
- [ ] SD-JWT credentials keep `@context`, `type`, `credentialStatus`, `credentialSchema` and `relatedResource` always disclosed (VC JOSE COSE § 3.2.1).
- [ ] A verifier returns a § 7.1 result and checks validity period, status and schema only after verification succeeds.
- [ ] Status lists are at least 131,072 entries, GZIP-compressed, multibase base64url without padding, with random indexes (Bitstring Status List § 2.1, § 2.2).
- [ ] Nothing from VC Data Model 2.1, VC Data Integrity 1.1 or Bitstring Status List 1.1 (for example `TerseBitstringStatusListEntry`) is emitted.

## Reference index

- **`references/versions.md`**: every version line and family with its status, which to use, what changed, the 1.1 to 2.0 upgrade, and the three previews. Load for steps 1 and 9.
- **`references/data-model.md`**: contexts, types, every credential and presentation property, enveloped forms, related resources, language values, media types, and when JSON-LD processing is required. Load for steps 2, 3 and 6.
- **`references/securing.md`**: VC JOSE COSE (JWT, SD-JWT, COSE, key discovery) and VC Data Integrity (proofs, purposes, context validation, cryptosuites). Load for steps 4 and 6.
- **`references/status-lists.md`**: Bitstring Status List entries, list credentials, generate and validate algorithms, errors and privacy. Load for step 5.
- **`references/validation.md`**: the verification algorithm, Problem Details, validation checks, and the privacy and security considerations. Load for steps 7 and 8.

## Related skills

- `sd-jwt`, for the SD-JWT format behind `vc+sd-jwt`: `npx skills add ScaleDockHQ/scaledock-skills --skill sd-jwt`
- `jwt`, for JWS and JWT validation behind `vc+jwt`: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`
- `did`, for DID identifiers used as issuer, subject and key identifiers: `npx skills add ScaleDockHQ/scaledock-skills --skill did`
- `openid4vc`, for issuing and presenting credentials over OpenID4VCI and OpenID4VP: `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`
- `eudi-wallet`, for the EU Digital Identity Wallet profiles: `npx skills add ScaleDockHQ/scaledock-skills --skill eudi-wallet`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Verifiable Credentials Data Model v2.0](https://www.w3.org/TR/vc-data-model-2.0/): W3C Recommendation, 15 May 2025 (REC-vc-data-model-2.0-20250515), checked 2026-10-05.
- [Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/): W3C Recommendation, 15 May 2025 (REC-vc-jose-cose-20250515), checked 2026-10-05.
- [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/): W3C Recommendation, 15 May 2025 (REC-vc-data-integrity-20250515), checked 2026-10-05.
- [Data Integrity EdDSA Cryptosuites v1.0](https://www.w3.org/TR/vc-di-eddsa/): W3C Recommendation, 15 May 2025 (REC-vc-di-eddsa-20250515), checked 2026-10-05.
- [Data Integrity ECDSA Cryptosuites v1.0](https://www.w3.org/TR/vc-di-ecdsa/): W3C Recommendation, 15 May 2025 (REC-vc-di-ecdsa-20250515), checked 2026-10-05.
- [Data Integrity BBS Cryptosuites v1.0](https://www.w3.org/TR/vc-di-bbs/): W3C Candidate Recommendation Draft, 10 September 2026 (CRD-vc-di-bbs-20260910), checked 2026-10-05.
- [Bitstring Status List v1.0](https://www.w3.org/TR/vc-bitstring-status-list/): W3C Recommendation, 15 May 2025 (REC-vc-bitstring-status-list-20250515), checked 2026-10-05.
- [Verifiable Credentials Data Model v1.1](https://www.w3.org/TR/vc-data-model-1.1/): W3C Recommendation, superseded by v2.0, 3 March 2022 (REC-vc-data-model-20220303), checked 2026-10-05.
- [Verifiable Credentials Overview](https://www.w3.org/TR/vc-overview/): W3C Group Note, 30 July 2026 (NOTE-vc-overview-1.0-20260730), checked 2026-10-05.
- [Verifiable Credentials Data Model v2.1](https://www.w3.org/TR/vc-data-model-2.1/): W3C Working Draft, 30 September 2026 (WD-vc-data-model-2.1-20260930), checked 2026-10-05. Draft posture: track.
- [Verifiable Credential Data Integrity 1.1](https://www.w3.org/TR/vc-data-integrity-1.1/): W3C Working Draft, 30 September 2026 (WD-vc-data-integrity-1.1-20260930), checked 2026-10-05. Draft posture: track.
- [Bitstring Status List v1.1](https://www.w3.org/TR/vc-bitstring-status-list-1.1/): W3C First Public Working Draft, 24 September 2026 (WD-vc-bitstring-status-list-1.1-20260924), checked 2026-10-05. Draft posture: track.
- [Data Integrity EdDSA Cryptosuites v1.1](https://www.w3.org/TR/vc-di-eddsa-1.1/): W3C First Public Working Draft, 16 April 2026 (WD-vc-di-eddsa-1.1-20260416), checked 2026-10-05. Draft posture: track.
- [Data Integrity ECDSA Cryptosuites v1.1](https://www.w3.org/TR/vc-di-ecdsa-1.1/): W3C Working Draft, 16 September 2026 (WD-vc-di-ecdsa-1.1-20260916), checked 2026-10-05. Draft posture: track.
- [Controlled Identifiers v1.0](https://www.w3.org/TR/cid-1.0/): W3C Recommendation, 15 May 2025 (REC-cid-1.0-20250515), checked 2026-10-06.
- [Verifiable Credentials JSON Schema Specification](https://www.w3.org/TR/vc-json-schema/): W3C Candidate Recommendation Draft, 4 February 2025 (CRD-vc-json-schema-20250204), checked 2026-10-06. Posture: build.
- [Verifiable Credential Barcodes v1.0](https://www.w3.org/TR/vc-barcodes/): W3C Working Draft, 22 August 2026 (WD-vc-barcodes-1.0-20260822), checked 2026-10-06. Posture: track.
- [Verifiable Credential Rendering Methods v1.0](https://www.w3.org/TR/vc-render-method/): W3C Working Draft, 29 September 2026 (WD-vc-render-method-20260929), checked 2026-10-06. Posture: track.
- [Verifiable Credential Confidence Methods v1.0](https://www.w3.org/TR/vc-confidence-method/): W3C Working Draft, 10 September 2026 (WD-vc-confidence-method-20260910), checked 2026-10-06. Its abstract defines mechanisms that increase a verifier's confidence that a presenter is appropriately related for the credential's use. Posture: track.
- [VC Forgery Defense](https://www.w3.org/TR/vc-forgery-defense/): W3C Working Draft, 25 August 2026 (WD-vc-forgery-defense-1.0-20260825), checked 2026-10-06. Posture: track.
- [VCALM](https://www.w3.org/TR/vcalm/): W3C Working Draft, 21 August 2026 (WD-vcalm-1.0-20260821), checked 2026-10-06. Posture: track.
