---
name: did
description: >-
  W3C DID 1.0 Decentralized Identifiers: parse DIDs and DID URLs, build and validate DID documents, resolve and dereference
  them, and evaluate DID methods. Use when working with did:<method>:<id> identifiers, DID URLs with path, query or fragment
  and the service, serviceType, relativeRef, versionId, versionTime or hl parameters, DID documents (id, controller,
  alsoKnownAs, verificationMethod with publicKeyJwk or publicKeyMultibase, Multikey, JsonWebKey, authentication,
  assertionMethod, keyAgreement, capabilityInvocation, capabilityDelegation, service, serviceEndpoint), JSON and JSON-LD
  representations and the application/did, did+json and did+ld+json media types, DID resolvers (resolve, dereference,
  metadata, deactivated, INVALID_DID, NOT_FOUND, the HTTP(S) binding), DID method specifications, the DID Extensions
  notes, the DID Method Rubric, or did:web. Targets DID 1.0
  (Recommendation), previews DID 1.1 (Candidate Recommendation, posture build), and covers DID Resolution 1.0
  (Candidate Recommendation Draft).
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# DID (Decentralized Identifiers)

Decentralized Identifiers are W3C URIs of the form `did:<method>:<method-specific-id>`. Each one resolves, through its DID method, to a DID document holding verification methods and services. With this skill an agent produces conforming DIDs, DID URLs and DID documents, implements resolvers and dereferencers, and reviews DID method specifications.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: {{ROLE}}. One of: DID controller or document producer; consumer or verifier; resolver or dereferencer implementer; resolver client; DID method author; method evaluator.
- Target version: DID 1.0 (default, Recommendation). DID 1.1 is a preview (posture: build): implement it only behind a version switch for named peers, and never make it the default. Resolution follows DID Resolution 1.0, a Candidate Recommendation Draft (posture: build), whose sections 5, 6, 8 and 10 are at risk. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the W3C history pages for `did-1.1` and `did-resolution-1.0` for a newer revision or a Recommendation, and update the pins.
- DID methods: {{METHODS}}. The methods to support, each with a link to its specification.
- Representation: {{REPRESENTATION}}. JSON or JSON-LD, and the media type peers expect.
- Resolver binding: {{BINDING}}. A local library, or a remote HTTP(S) resolver and who runs it.

## Invariants

DID 1.0 is the default; a "DID 1.1" cite applies only on that line. "Resolution" means DID Resolution 1.0; "CID" means Controlled Identifiers v1.0.

1. **DIDs match the ABNF** (DID 1.0 § 3.1, DID 1.1 § 3.1). The form is `did:` plus a method name of `[a-z0-9]+` plus `:` plus a non-empty method-specific id of `ALPHA / DIGIT / . - _ / pct-encoded` characters and colons, not ending in a colon. Do not normalize the method-specific id generically; its case rules belong to the method (DID 1.0 § 8.1).
2. **DID URLs are `did path-abempty [ "?" query ] [ "#" fragment ]`** (DID 1.0 § 3.2). Relative DID URLs resolve with RFC 3986 § 5, using the DID as the base (DID 1.0 § 3.2.2). The semicolon is reserved.
3. **The document `id` is the DID** (DID 1.0 § 5.1.1). The top-level `id` MUST be a DID in the root map, and the resolved document's `id` MUST equal the resolved DID (Resolution § 4). The subject `id` and `controller` values carry no query or fragment (DID 1.1 § 5.1.3).
4. **Verification methods have `id`, `type`, `controller` and one form of key material** (DID 1.0 § 5.2, § 5.2.1). `publicKeyJwk` MUST NOT contain `d` or other private members. A method MUST NOT have two material properties for the same key.
5. **A key is valid only in its relationship** (DID 1.0 § 5.3). Before accepting a proof, check that the verification method is in the relationship the proof claims: `authentication`, `assertionMethod`, `keyAgreement`, `capabilityInvocation` or `capabilityDelegation`. Retrieve the method with the CID § 3.3 checks. A method absent from the latest document is invalid or revoked.
6. **Services have `id`, `type` and `serviceEndpoint`, and ids are unique** (DID 1.0 § 5.4). A producer MUST NOT emit duplicate service `id`s, and a consumer MUST raise an error on them.
7. **The representation matches the line** (DID 1.0 § 6.2, § 6.3; DID 1.1 § 6.2).
   - DID 1.0: `application/did+json`, or `application/did+ld+json` with `@context` first item `https://www.w3.org/ns/did/v1`.
   - DID 1.1: `application/did` with `https://www.w3.org/ns/did/v1.1`.
   - The root MUST be a JSON object.
8. **Producers and consumers conform** (DID 1.0 § 6.1). Producers MUST NOT produce non-conforming DIDs or documents. Consumers MUST choose the representation from the media type and MUST produce errors on non-conforming input.
9. **Resolution results follow the contract** (Resolution § 4, § 4.4).
   - On error: an `error` in the resolution metadata, and an empty document and document metadata.
   - Deactivated DIDs: `deactivated: true` in the document metadata.
   - Errors are RFC 9457 objects with `https://www.w3.org/ns/did#` type URLs (Resolution § 11).
10. **DID parameter values are ASCII strings** (DID 1.0 § 3.2.1, Resolution § 3).
    - `versionTime` is a UTC XML datetime without sub-seconds.
    - `relativeRef` is percent-encoded.
    - `versionId` and `versionTime` are mutually exclusive (Resolution § 13.4).
11. **Metadata is a JSON-serializable map** (DID 1.0 § 7.3, Resolution § 7).
12. **A DID method specification covers syntax, the four operations, security and privacy** (DID 1.0 § 8.1 to § 8.4). The operations are Create, Resolve with authenticity verification, Update and Deactivate, each specified or stated as impossible. Security follows RFC 3552 and privacy follows RFC 6973 § 5.

## Workflow

1. **Pick the version.** Use DID 1.0 unless a named peer needs DID 1.1, and use DID Resolution 1.0 for resolvers.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target DID line and resolution line are recorded, and DID 1.1 is used only behind a switch.
2. **Parse and build DIDs and DID URLs.** Validate against the ABNF, split off path, query and fragment, and percent-encode caller-supplied parameter values.
   -> [`references/syntax-and-urls.md`](references/syntax-and-urls.md)
   ✓ Invalid DIDs are rejected, relative DID URLs expand per RFC 3986 § 5, and duplicate or injected parameters are rejected.
3. **Author or validate the DID document.** Write `id`, `controller` and `alsoKnownAs`, then the verification methods, relationships and services.
   -> [`references/did-documents.md`](references/did-documents.md)
   ✓ The document passes the validation checklist there, with no private key members and unique service ids.
4. **Serialize and consume.** Choose the representation and media type for the line, and pin JSON-LD contexts.
   -> [`references/did-documents.md`](references/did-documents.md)
   ✓ The `@context` and media type match the line, and a non-object root or non-conforming document produces an error.
5. **Resolve and dereference.** Implement or call `resolve()` and `dereference()` with the options, metadata, errors and HTTP binding.
   -> [`references/resolution.md`](references/resolution.md)
   ✓ An invalid DID, an unsupported method, a missing DID and a deactivated DID each give the specified result and HTTP status.
6. **Verify proofs through the relationship.** Resolve the signer's DID, retrieve the verification method with the CID § 3.3 checks, and check its relationship and expiry.
   -> [`references/did-documents.md`](references/did-documents.md), [`references/security-and-privacy.md`](references/security-and-privacy.md)
   ✓ A key that is in `verificationMethod` but not in the required relationship is rejected.
7. **Choose or write a DID method.** Check the method against the DID 1.0 § 8 requirements, evaluate it with the rubric for your use, and follow its read steps, for example `did:web`.
   -> [`references/methods.md`](references/methods.md)
   ✓ Every supported method has a specification with all four operations, and its security and privacy sections have been read.
8. **Review security and privacy.**
   -> [`references/security-and-privacy.md`](references/security-and-privacy.md)
   ✓ The review checklist there passes: no personal data in public documents, a written rotation and revocation path, and trusted or local resolution.
9. **Upgrade** (only when asked). Upgrade DID 1.0 documents to DID 1.1 behind a switch, or a DID 1.0 § 7 resolver to DID Resolution 1.0.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded artifact validates against the target version and behaves the same.

## Verify before done

- [ ] Every DID and DID URL produced matches the DID 1.0 § 3.1 and § 3.2 ABNF.
- [ ] Every DID document has a top-level `id` equal to the DID, and the `@context` and media type of its line.
- [ ] Every verification method has `id`, `type`, `controller` and exactly one form of public key material, with no private members.
- [ ] Every proof is accepted only from a verification method in the required relationship of the resolved document.
- [ ] Service ids are unique, and service endpoints are valid URIs (DID 1.0) or URLs (DID 1.1).
- [ ] Resolver errors use the Resolution § 11 type URLs, with the § 12.1 HTTP statuses when served over HTTP.
- [ ] Nothing DID 1.1-specific (the `v1.1` context, `application/did`) is emitted to peers that have not opted in.
- [ ] No personal data or human-meaningful identifiers appear in public DID documents.

## Reference index

- **`references/versions.md`**: DID 1.0, DID 1.1 and DID Resolution 1.0 with their status, which to use, what changed, upgrade steps and the preview. Load for steps 1 and 9.
- **`references/syntax-and-urls.md`**: the DID and DID URL ABNF, identifier restrictions, relative DID URLs, the DID parameters and query normalization. Load for step 2.
- **`references/did-documents.md`**: core properties, verification methods and material, verification relationships, the CID § 3.3 retrieval checks, services, JSON and JSON-LD, media types and examples. Load for steps 3, 4 and 6.
- **`references/resolution.md`**: `resolve()` and `dereference()`, options, metadata, the algorithm, errors, the HTTP(S) binding, architectures and resolver security. Load for step 5.
- **`references/methods.md`**: method specification requirements, the DID Extensions notes and registration, the DID Method Rubric, and `did:web`. Load for step 7.
- **`references/security-and-privacy.md`**: proving control, expiry, rotation, revocation, recovery, integrity, equivalence and privacy. Load for steps 6 and 8.

## Related skills

Install related spec skills by name:

- `vc-data-model`: Verifiable Credentials, the mechanism DID 1.0 § 9.2 and § 10.1 point to for binding a DID to a real-world identity and carrying personal data. `npx skills add ScaleDockHQ/scaledock-skills --skill vc-data-model`
- `openid4vc`: OpenID for Verifiable Credential Issuance and Verifiable Presentations. `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`
- `eudi-wallet`: the EU Digital Identity Wallet architecture. `npx skills add ScaleDockHQ/scaledock-skills --skill eudi-wallet`
- `jwt`: JSON Web Tokens and JWK, used with `publicKeyJwk`. `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/2022/REC-did-core-20220719/): W3C Recommendation, 19 July 2022 (also served at https://www.w3.org/TR/did-1.0/), checked 2026-10-05.
- [Decentralized Identifiers (DIDs) v1.1](https://www.w3.org/TR/2026/CR-did-1.1-20260305/): W3C Candidate Recommendation Snapshot, 5 March 2026, checked 2026-10-05.
- [Decentralized Identifiers (DIDs) v1.1, editor's draft](https://w3c.github.io/did/): Editor's Draft, commit a2bb463 (27 August 2026), checked 2026-10-05.
- [Decentralized Identifier Resolution (DID Resolution) v1](https://www.w3.org/TR/2026/CRD-did-resolution-1.0-20261001/): W3C Candidate Recommendation Draft, 1 October 2026, checked 2026-10-05.
- [DID Resolution, editor's draft](https://w3c.github.io/did-resolution/): Editor's Draft, commit a5f3d89 (1 October 2026), checked 2026-10-05.
- [Controlled Identifiers v1.0](https://www.w3.org/TR/2025/REC-cid-1.0-20250515/): W3C Recommendation, 15 May 2025, checked 2026-10-05.
- [Decentralized Identifier Extensions](https://www.w3.org/TR/2025/NOTE-did-extensions-20251211/): W3C Group Note, 11 December 2025, checked 2026-10-05.
- [DID Document Property Extensions](https://www.w3.org/TR/2025/NOTE-did-extensions-properties-20251211/): W3C Group Note, 11 December 2025, checked 2026-10-05.
- [DID Method Extensions](https://www.w3.org/TR/2026/NOTE-did-extensions-methods-20261001/): W3C Group Note, 1 October 2026, checked 2026-10-05.
- [DID Resolution Extensions](https://www.w3.org/TR/2024/NOTE-did-extensions-resolution-20241119/): W3C Group Note, 19 November 2024, checked 2026-10-05.
- [DID Method Rubric](https://www.w3.org/TR/2026/NOTE-did-rubric-20260922/): W3C Group Note, 22 September 2026, checked 2026-10-05.
- [did:web Method Specification](https://w3c-ccg.github.io/did-method-web/): W3C Credentials Community Group unofficial draft, commit ea423c1 (8 May 2026), checked 2026-10-05.
- [IANA Media Types registry](https://www.iana.org/assignments/media-types/media-types.txt): IANA registry, last updated 24 September 2026, checked 2026-10-05.
