---
name: http-message-signatures
description: >-
  RFC 9421 HTTP Message Signatures: sign and verify HTTP requests and responses with the Signature-Input and Signature fields, and protect content with RFC 9530 Content-Digest and Repr-Digest. Use when adding, reviewing or debugging message signing between clients, servers, proxies or gateways: covered components (@method, @target-uri, @authority, @path, @query, @query-param, @status, field parameters sf, key, bs, req, tr), the signature base and @signature-params, created, expires, nonce, alg, keyid and tag, the algorithms rsa-pss-sha512, rsa-v1_5-sha256, hmac-sha256, ecdsa-p256-sha256, ecdsa-p384-sha384 and ed25519, Accept-Signature, verification and key or algorithm confusion, replay, multiple signatures and TLS-terminating proxies, Want-Content-Digest and Want-Repr-Digest. Targets RFC 9421 and RFC 9530; upgrades from draft-cavage-http-signatures-12 (hs2019, keyId, (request-target), headers=) and RFC 3230 Digest and Want-Digest. Triggers: HTTP signatures, httpsig, signed requests, digest header.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# HTTP Message Signatures

RFC 9421, an IETF Standards Track RFC, defines how to create, attach and verify a detached digital signature or MAC over selected components of an HTTP message, so the signature survives the transformations HTTP allows. It does not cover message content itself; RFC 9530 Digest Fields supplies `Content-Digest` and `Repr-Digest` for that. With this skill the agent produces a signing profile, signer and verifier code, or a review that meets both RFCs.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Bare section numbers are RFC 9421; other documents are named. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: signer, verifier, or both; client, server, or an intermediary (reverse proxy, gateway) that re-signs.
- Message direction: signed requests, signed responses, or responses that also cover parts of the request (`req`).
- Keys: asymmetric (RSA, ECDSA, Ed25519) or shared secret (HMAC), and how the verifier resolves `keyid` to a trusted key.
- Content: whether the message has content that must be covered, which brings in RFC 9530.
- Target version: RFC 9421 (current, the default) for signatures and RFC 9530 (current, the default) for digests. draft-cavage-http-signatures-12 and RFC 3230 are legacy: read them and upgrade from them, never author them. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the RFC Editor entries for RFC 9421 and RFC 9530 for errata or updating RFCs, check the IANA registries for new algorithms, parameters and derived components, and update the pins.

## Invariants

1. **The application profile is defined first.** An application of RFC 9421 MUST specify the required components and parameters, their Structured Field types, key retrieval, allowed algorithms, how algorithm and key fit the context, any request-response binding, and its error responses (§ 1.4). It MUST enforce those requirements and fail verification when they are not met (§ 3.2.1).
2. **Both fields, same labels.** A signature uses both `Signature-Input` and `Signature`, with the same label in each; a label in only one is an error, and labels are unique across all field values of a message (§ 4, § 4.1, § 4.2, § 4.3).
3. **`Signature-Input` is the exact `@signature-params` value.** It MUST contain the same serialization used as the last line of the signature base, with component and parameter order preserved (§ 2.3, § 4.1). Once chosen, the order of covered components MUST NOT change (§ 3.1).
4. **`@signature-params` is always last and never listed.** It is the required final line of the base and MUST NOT appear in the covered components (§ 2.3, § 3.1).
5. **Component identifiers are exact.** Field names are lowercased (§ 2.1); each identifier occurs at most once (§ 2); values never contain newlines (§ 2); a missing field, unknown parameter, absent Dictionary key or absent query parameter MUST produce an error and no base (§ 2.5).
6. **Derived names start with `@` and never come from fields.** A name starting with `@` is always derived, never read from a header (§ 2.2, § 7.5.1). `@status` MUST NOT be used in a request (§ 2.2.9), and `req` MUST NOT be used in a signature that targets a request (§ 2.4).
7. **The base is strict ASCII.** Lines are `"name";params: value` joined by LF with no trailing newline; any error or non-ASCII output fails the algorithm (§ 2.5).
8. **The verifier picks the key and algorithm.** An unknown or untrusted key MUST fail (§ 3.2 step 5); the algorithm must be in the application's allowed set, and if it is stated in more than one place the values MUST match (§ 3.2 step 6). `alg` values come from the IANA registry (§ 3.3); JWS algorithms MUST NOT be `none` or Prohibited and use no `alg` parameter (§ 3.3.7).
9. **Verify with the verification function.** RSA-PSS and ECDSA are non-deterministic; never re-sign and compare (§ 3.3.1, § 3.3.4, § 7.3.5).
10. **Content needs a digest, and the digest must be checked.** Cover `Content-Digest` (or `Repr-Digest`) and validate it against the received content, or the content can be swapped (§ 7.2.8). Deprecated hash algorithms (`md5`, `sha`, `unixsum`, `unixcksum`, `adler`, `crc32c`) MUST NOT be used in an adversarial setting such as signing (RFC 9530 § 5, § 7.2).
11. **Test keys stay in tests.** The RFC 9421 Appendix B.1 keys MUST NOT be used for any other purpose (Appendix B.1).

## Workflow

1. **Pick the version.** Use RFC 9421 and RFC 9530. If the system sends a `Signature` header without `Signature-Input`, or a `Digest` header, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is RFC 9421 with RFC 9530, and no new code emits cavage or RFC 3230 fields.
2. **Write the profile.** Record each item § 1.4 requires: required components and parameters (for example `created` and a `tag`), key resolution, allowed algorithms, maximum age, nonce policy, and the status code and problem body for each failure.
   -> [`references/signing-and-verifying.md`](references/signing-and-verifying.md)
   ✓ Every § 1.4 item has a written answer, and the verifier rejects anything outside it.
3. **Choose covered components.** Cover the control data (`@method`, `@authority`, `@path` or `@target-uri`, `@query` or `@query-param`), the fields the application acts on, and `@status` in responses. Prefer `@authority` over `host` and `created` over `date` (§ 7.2.4); leave out `Via` and `Forwarded` unless tightly coupled (§ 7.2.3).
   -> [`references/components-and-base.md`](references/components-and-base.md)
   ✓ Every message part that changes processing is covered, and every component can be derived the same way by signer and verifier.
4. **Cover the content.** Add `Content-Digest` (content bytes as sent) or `Repr-Digest` (selected representation) with `sha-256` or `sha-512`, cover it and the representation metadata such as `content-type`.
   -> [`references/digest-fields.md`](references/digest-fields.md)
   ✓ The digest uses an Active algorithm, is covered, and the verifier recomputes it.
5. **Sign.** Pick the algorithm and key, set `created` (and `expires`, `nonce`, `keyid`, `tag` as the profile says), build the base, sign it, and attach `Signature-Input` and `Signature` under one label (§ 3.1, § 4).
   -> [`references/components-and-base.md`](references/components-and-base.md), [`references/algorithms-and-keys.md`](references/algorithms-and-keys.md)
   ✓ The RFC 9421 Appendix B.2 test cases reproduce the published bases, and deterministic algorithms (HMAC, Ed25519) reproduce the published signatures.
6. **Verify.** Run the § 3.2 steps in order: select the signature by policy (for example by `tag`), parse with a compliant Structured Fields parser, check parameters and required components, resolve a trusted key and allowed algorithm, rebuild the base from the received message, verify, then validate covered field values and the digest.
   -> [`references/signing-and-verifying.md`](references/signing-and-verifying.md)
   ✓ Tests include invalid, expired, wrong-key, wrong-algorithm, missing-component and tampered-content cases, and each fails (§ 7.1.1).
7. **Review security and topology.** Check replay limits, multiple-signature handling, signer identity, proxies that rewrite `@authority`, `req` bindings, and `Accept-Signature` caching.
   -> [`references/signing-and-verifying.md`](references/signing-and-verifying.md)
   ✓ Each § 7 consideration that applies has a decision in the profile.
8. **Upgrade** (only when asked). Follow the cavage -12 to RFC 9421 and RFC 3230 to RFC 9530 checklists, then re-run steps 3 to 6.
   -> [`references/versions.md`](references/versions.md)
   ✓ Messages carry `Signature-Input`, `Signature` and `Content-Digest` or `Repr-Digest` only, and every old covered header has an RFC 9421 equivalent.

## Verify before done

- [ ] The profile answers every § 1.4 item, and the verifier enforces it (§ 3.2.1).
- [ ] `Signature-Input` and `Signature` carry the same unique labels (§ 4).
- [ ] The base matches § 2.5: quoted lowercased identifiers, LF separators, `@signature-params` last, no trailing newline.
- [ ] The verifier never takes the algorithm from `alg` alone, rejects unknown keys, and rejects HMAC with a public key (§ 3.2, § 7.3.6).
- [ ] `created` is set and checked against a maximum age; `expires` and `nonce` are enforced when the profile requires them (§ 2.3, § 3.2.1, § 7.2.2).
- [ ] Content is covered by `Content-Digest` or `Repr-Digest` with `sha-256` or `sha-512`, and the digest is validated (§ 7.2.8; RFC 9530 § 5).
- [ ] Only signatures from expected signers are accepted when several are present (§ 7.2.6).
- [ ] No `Signature` header in the cavage format and no `Digest` or `Want-Digest` field is emitted.

## Reference index

- **`references/versions.md`**: RFC 9421, draft-cavage-http-signatures-12, RFC 9530 and RFC 3230 with their status, what changed, and the two upgrade checklists. Load for steps 1 and 8.
- **`references/components-and-base.md`**: HTTP field components and the `sf`, `key`, `bs`, `req`, `tr` and `name` parameters, every derived component, the signature parameters, and the signature base algorithm with its error cases. Load for steps 3 and 5.
- **`references/signing-and-verifying.md`**: the profile, creating a signature, the `Signature-Input`, `Signature` and `Accept-Signature` fields, multiple signatures, verification, and the security and privacy considerations. Load for steps 2, 6 and 7.
- **`references/algorithms-and-keys.md`**: the six registered algorithms with their exact encodings, JWS algorithms, the registry statuses, key and algorithm selection, downgrade and symmetric-key risks. Load for step 5.
- **`references/digest-fields.md`**: `Content-Digest`, `Repr-Digest`, `Want-Content-Digest`, `Want-Repr-Digest`, the hash algorithm registry, and using digests under signatures. Load for step 4.

## Related skills

- `web-bot-auth` for the RFC 9421 profile that bots and AI agents use to identify themselves to websites: `npx skills add ScaleDockHQ/scaledock-skills --skill web-bot-auth`.
- `http-semantics` for target URIs, authority normalization, fields, trailers and content codings that the components depend on: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.
- `oauth` for the access tokens and authorization flows that signed requests often travel with: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`.
- `standard-webhooks` for signed webhook deliveries: `npx skills add ScaleDockHQ/scaledock-skills --skill standard-webhooks`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9421: HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421.html): RFC (Proposed Standard), RFC 9421 (February 2024), checked 2026-10-05.
- [RFC 9421 errata](https://www.rfc-editor.org/errata/rfc9421): RFC Editor errata, two verified (8102, 8103), checked 2026-10-05.
- [RFC 9530: Digest Fields](https://www.rfc-editor.org/rfc/rfc9530.html): RFC (Proposed Standard, obsoletes RFC 3230), RFC 9530 (February 2024), checked 2026-10-05.
- [RFC 9530 errata](https://www.rfc-editor.org/errata/rfc9530): RFC Editor errata, two verified (8158, 8273), one reported (8890), checked 2026-10-05.
- [RFC 3230: Instance Digests in HTTP](https://www.rfc-editor.org/rfc/rfc3230.html): RFC (Proposed Standard, obsoleted by RFC 9530), RFC 3230 (January 2002), checked 2026-10-05.
- [draft-cavage-http-signatures-12: Signing HTTP Messages](https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures-12): Internet-Draft (individual, expired 2020-04-23), revision -12 (last), checked 2026-10-05.
- [RFC 9651: Structured Field Values for HTTP](https://www.rfc-editor.org/rfc/rfc9651.html): RFC (Proposed Standard, obsoletes RFC 8941), RFC 9651 (September 2024), checked 2026-10-05.
- [IANA HTTP Message Signature registries](https://www.iana.org/assignments/http-message-signature/): IANA registry group, last updated 2026-07-20, checked 2026-10-05.
- [IANA Hash Algorithms for HTTP Digest Fields](https://www.iana.org/assignments/http-digest-hash-alg/): IANA registry, last updated 2024-05-22, checked 2026-10-05.
- [IANA HTTP Digest Algorithm Values](https://www.iana.org/assignments/http-dig-alg/): IANA registry (deprecated by RFC 9530), last updated 2024-02-16, checked 2026-10-05.
