---
name: openid4vc
description: "OpenID4VC: issue and verify verifiable credentials over OAuth. Use when building or reviewing a credential issuer, wallet or verifier with OpenID4VCI 1.0, OpenID4VP 1.0 or HAIP 1.0 (the 1.1 drafts tracked; upgrades from Implementer's Drafts such as VCI draft 13 and VP ID2): credential offers, authorization and pre-authorized code flows, issuer metadata at /.well-known/openid-credential-issuer, nonce and credential endpoints, key proofs, key and wallet attestations, DCQL queries, vp_token responses, client identifier prefixes such as x509_hash, direct_post.jwt and the W3C Digital Credentials API (dc_api). Also use it for SD-JWT VC (dc+sd-jwt), ISO mdoc (mso_mdoc) and W3C VCDM credentials at the protocol level, and OpenID conformance testing. Triggers: OID4VCI, OID4VP, HAIP, verifiable credentials, digital wallet, mDL, SD-JWT VC, DCQL, vp_token, credential offer, Presentation Exchange migration."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.2"
  kind: standard
---

# OpenID4VC

OpenID for Verifiable Credentials is the OpenID Foundation's family of protocols for verifiable credentials. OpenID4VCI issues credentials to a wallet over OAuth 2.0. OpenID4VP lets a wallet present credentials to a verifier. HAIP profiles both for high-assurance deployments. With this skill an agent builds or reviews an issuer, a wallet or a verifier, writes DCQL queries, wires up the browser Digital Credentials API, and prepares for the OpenID conformance tests.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: credential issuer (with its authorization server), wallet, or verifier. A wallet implements both the issuance and presentation sides.
- Flows: issuance with the authorization code flow, the pre-authorized code flow or both; presentation through redirects (same-device or cross-device) or through the Digital Credentials API.
- Formats: `dc+sd-jwt`, `mso_mdoc`, `jwt_vc_json`, `jwt_vc_json-ld` or `ldp_vc` (OpenID4VCI Appendix A, OpenID4VP Appendix B).
- Profile: plain OpenID4VCI and OpenID4VP, or HAIP. HAIP is required for OpenID certification of both.
- Target version, per specification: OpenID4VCI 1.0, OpenID4VP 1.0 and HAIP 1.0 are current (the defaults). OpenID4VCI ID1 (draft 13), OpenID4VCI ID2 (draft 15), OpenID4VP ID2 (draft 18), OpenID4VP ID3 (draft 23) and HAIP ID1 (draft 03) are legacy: read them and upgrade, never author them; OpenID4VP ID2 is still met in ISO 18013-7 Annex B deployments. OpenID4VCI 1.1, OpenID4VP 1.1 and HAIP 1.1 are previews (posture: track): never emit them. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the DCP WG specifications page and each specification's errata URL for a newer revision, and update the pins.

## Invariants

1. **Issuer identity and metadata** (OpenID4VCI §12.2.1, §12.2.2). The credential issuer identifier is an `https` URL without query or fragment. Metadata is fetched over TLS from `/.well-known/openid-credential-issuer` inserted between host and path, and its `credential_issuer` equals the identifier.
2. **Offers are untrusted** (OpenID4VCI §13.5). A wallet validates the issuer in a credential offer exactly as if it had started the flow, and never accepts credentials just because an offer arrived.
3. **Pre-authorized codes are short-lived and single use** (OpenID4VCI §4.1.1, §13.6). A transaction code (`tx_code`) sent over a separate channel mitigates replay. To resist transaction-code phishing, wallets should talk only to trusted issuers, and may show the user which issuer will receive the code.
4. **Key proofs are fresh and audience-bound** (OpenID4VCI §7, §8.2, Appendix F). A `jwt` proof has `typ` `openid4vci-proof+jwt`, an asymmetric `alg`, `aud` set to the issuer identifier and, when a nonce endpoint exists, `nonce` set to a `c_nonce`.
5. **Long-lived access tokens are sender-constrained** (OpenID4VCI §13.10, §13.2). Tokens that live longer than about 5 minutes are not issued as bearer tokens; DPoP is recommended for native wallets.
6. **Presentation requests are fresh and identify the verifier** (OpenID4VP §5.2, §5.9). Each request has a new random `nonce`, a `client_id` with its client identifier prefix, and, when signed, a request object with `typ` `oauth-authz-req+jwt`.
7. **Every presentation is bound to audience and nonce** (OpenID4VP §14.1.2, Appendix A.4). The audience is the full client identifier, or `origin:<origin>` over the Digital Credentials API. The verifier rejects the response if any presentation has the wrong nonce.
8. **DCQL is all or nothing per credential** (OpenID4VP §6.4). A wallet returns no claims from a credential if it cannot satisfy the query, and no credentials if a required credential set cannot be met. `values` matching is best effort and never a security check.
9. **`direct_post` is protected against session fixation** (OpenID4VP §8.2, §14.2, §14.3). The response URI returns a `redirect_uri` with a fresh response code, and the verifier's frontend must present that code to fetch the result.
10. **Encrypted responses use the verifier's request keys** (OpenID4VP §8.3). The wallet encrypts to a key from `client_metadata.jwks`, uses the JWK's `alg`, echoes its `kid`, and picks `enc` from `encrypted_response_enc_values_supported` (default `A128GCM`).
11. **HAIP, when chosen, narrows every choice** (HAIP §4 to §8).
    - Issuance uses the authorization code flow, FAPI 2.0 with DPoP, client authentication at PAR and token endpoints, and key attestations.
    - Presentation uses `vp_token`, DCQL, `x509_hash` for signed requests, `direct_post.jwt` over redirects or `dc_api.jwt` over the DC API, and ECDH-ES on P-256.
    - Every party supports ES256 and SHA-256.

## Workflow

1. **Pick the versions and pin roles, flows, formats and profile.** Use the 1.0 Finals unless a named consumer needs a legacy draft for reading. Record the rest from the inputs.
   -> [`references/versions.md`](references/versions.md)
   ✓ Each family has a recorded target that is not a legacy or preview line, every flow and format is named, and HAIP is in or out.
2. **Build issuance.** Issuer metadata, credential offer, authorization or pre-authorized code, token, nonce, credential, deferred and notification endpoints, and the wallet side of each.
   -> [`references/issuance.md`](references/issuance.md)
   ✓ A wallet obtains a credential from metadata alone, and a replayed proof or offer is rejected.
3. **Build the presentation request and response handling.** Client identifier prefixes, request objects, response modes, encryption, errors and VP token validation.
   -> [`references/presentation.md`](references/presentation.md)
   ✓ The verifier rejects a presentation with a wrong nonce or audience, and `direct_post` uses a response code.
4. **Write the DCQL query.** Credential queries, claims, claim sets, credential sets and trusted authorities.
   -> [`references/dcql.md`](references/dcql.md)
   ✓ Each query asks for the least information that meets the use case, and the wallet's selection rules give the intended result.
5. **Add the Digital Credentials API if the verifier is a website.** Protocol identifiers, signed and unsigned requests, `expected_origins` and the `origin:` audience.
   -> [`references/dc-api.md`](references/dc-api.md)
   ✓ The request uses `openid4vp-v1-*`, and the KB-JWT `aud` is `origin:<origin>`.
6. **Handle credential formats.** Format identifiers, format-specific metadata, query parameters and holder-binding proofs.
   -> [`references/formats.md`](references/formats.md)
   ✓ Each format has its issuer metadata, its DCQL `meta`, and its presentation check.
7. **Apply HAIP if required.** Issuance, presentation, SD-JWT VC, mdoc and crypto requirements.
   -> [`references/haip.md`](references/haip.md)
   ✓ Every HAIP row in the checklist holds for the chosen flows.
8. **Prepare certification.** Choose the HAIP test plans for wallet, verifier or issuer.
   -> [`references/certification.md`](references/certification.md)
   ✓ The plan, credential format, response mode and client identifier prefix are configured.
9. **Upgrade** (only when asked). Follow the upgrade section for each step from the source draft to the 1.0 Final, per family.
   -> [`references/versions.md`](references/versions.md)
   ✓ No Presentation Exchange, `client_id_scheme`, JARM, `proof` or `vc+sd-jwt` remains, and the conformance tests pass against 1.0.

## Verify before done

- [ ] Issuer metadata is served at the well-known path with a matching `credential_issuer`, and every configuration has a `format`.
- [ ] Credential requests use `credential_identifier` or `credential_configuration_id`, never both, and carry fresh `proofs` when proofs are required.
- [ ] The issuer rejects proofs with the wrong `typ`, `aud` or `nonce`, a symmetric `alg`, or a private key in the header.
- [ ] Verifier requests carry a fresh `nonce`, a prefixed `client_id` and either `dcql_query` or a DCQL scope, not both.
- [ ] The verifier checks integrity, holder binding, audience, nonce, query criteria and its own policy for every presentation, then the set as a whole.
- [ ] `direct_post` responses use a response code; encrypted responses use the request's key and an allowed `enc`.
- [ ] Over the DC API, signed requests carry `expected_origins`, and responses are bound to `origin:<origin>`.
- [ ] SD-JWT VC presentations carry a `kb+jwt` KB-JWT with a correct `sd_hash`, verified with the key in `cnf`, and a `status` reference is checked against a `statuslist+jwt` token before the credential is accepted.
- [ ] If HAIP is in scope, the matching conformance test plans finish with no failures.
- [ ] Nothing from a 1.1 editor's draft or an Implementer's Draft is emitted.

## Reference index

- **`references/versions.md`**: the version lines of OpenID4VCI, OpenID4VP and HAIP, which to use, what changed since each Implementer's Draft, upgrade steps and the 1.1 previews. Load for steps 1 and 9.
- **`references/issuance.md`**: OpenID4VCI issuer metadata, offers, grants, token, nonce, credential, deferred and notification endpoints, proofs, attestations and errors.
- **`references/presentation.md`**: OpenID4VP requests, client identifier prefixes, response modes, encryption, errors, validation and security checks, with TypeScript.
- **`references/dcql.md`**: the Digital Credentials Query Language, claims path pointers and selection rules, with examples.
- **`references/dc-api.md`**: OpenID4VP over the W3C Digital Credentials API, with a browser example.
- **`references/formats.md`**: SD-JWT VC, ISO mdoc and W3C VCDM parameters in OpenID4VCI and OpenID4VP, and the SD-JWT, SD-JWT VC and Token Status List base rules.
- **`references/haip.md`**: the HAIP 1.0 requirements as a checklist.
- **`references/certification.md`**: OpenID conformance test plans for OpenID4VP and OpenID4VCI.

## Related skills

- `oauth` for the OAuth 2.0 framework, PAR, PKCE, DPoP and token handling: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`.
- `jwt` for JWS, JWE, JWK and RFC 8725 checks on proofs, request objects and KB-JWTs: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`.
- `fapi` because HAIP builds its issuance profile on the FAPI 2.0 Security Profile: `npx skills add ScaleDockHQ/scaledock-skills --skill fapi`.
- `openid-federation` for the `openid_federation` client identifier prefix and trust chains: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-federation`.
- `openid-connect` for SIOPv2-style `vp_token id_token` responses and OpenID Connect basics: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`.
- `openid` for an overview of OpenID Foundation specifications: `npx skills add ScaleDockHQ/scaledock-skills --skill openid`.
- `sd-jwt` for RFC 9901 SD-JWT, SD-JWT VC and Token Status List in depth: disclosures, Key Binding JWTs, type metadata and status checks behind `dc+sd-jwt`: `npx skills add ScaleDockHQ/scaledock-skills --skill sd-jwt`.
- `vc-data-model` for the W3C Verifiable Credentials Data Model 2.0 behind `jwt_vc_json`, `jwt_vc_json-ld` and `ldp_vc`, with VC JOSE COSE, Data Integrity and Bitstring Status List: `npx skills add ScaleDockHQ/scaledock-skills --skill vc-data-model`.
- `did` for W3C DIDs, DID documents and resolution behind `did:<method>` binding methods and the `decentralized_identifier:` client identifier prefix: `npx skills add ScaleDockHQ/scaledock-skills --skill did`.
- `eudi-wallet` for the EU Digital Identity Wallet ARF, which profiles OpenID4VCI, OpenID4VP and HAIP for PID and attestation issuers, wallets and relying parties: `npx skills add ScaleDockHQ/scaledock-skills --skill eudi-wallet`.
- `digital-credentials`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill digital-credentials`
- `fedcm`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill fedcm`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenID for Verifiable Credential Issuance 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-final.html): Final, published 16 September 2025, checked 2026-10-02.
- [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0-final.html): Final, published 9 July 2025, checked 2026-10-02.
- [OpenID4VC High Assurance Interoperability Profile 1.0](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-final.html): Final, published 24 December 2025, checked 2026-10-02.
- [OpenID for Verifiable Credential Issuance - draft 13 (Implementer's Draft 1)](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-ID1.html): Implementer's Draft, ID1, document draft 13 (8 February 2024), checked 2026-10-05. Legacy line.
- [OpenID for Verifiable Credential Issuance - draft 15 (Implementer's Draft 2)](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-ID2.html): Implementer's Draft, ID2, document draft 15 (19 December 2024), checked 2026-10-05. Legacy line.
- [OpenID for Verifiable Credential Issuance 1.0 - draft 17](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0-17.html): Draft, draft 17 (17 August 2025), checked 2026-10-05. Read for its Document History; superseded by the Final.
- [OpenID for Verifiable Credential Issuance 1.1 - Editor's draft](https://openid.github.io/OpenID4VCI/openid-4-verifiable-credential-issuance-1_1-wg-draft.html): Editor's draft, 1.1 -01 (1 October 2026), checked 2026-10-05. Draft posture: track.
- [OpenID for Verifiable Presentations - draft 18 (Implementer's Draft 2)](https://openid.net/specs/openid-4-verifiable-presentations-1_0-ID2.html): Implementer's Draft, ID2, document draft 18 (21 April 2023), checked 2026-10-05. Legacy line, used by ISO 18013-7 Annex B.
- [OpenID for Verifiable Presentations - draft 23 (Implementer's Draft 3)](https://openid.net/specs/openid-4-verifiable-presentations-1_0-ID3.html): Implementer's Draft, ID3, document draft 23 (2 December 2024), checked 2026-10-05. Legacy line.
- [OpenID for Verifiable Presentations - draft 29](https://openid.net/specs/openid-4-verifiable-presentations-1_0-29.html): Draft, draft 29 (10 June 2025), checked 2026-10-05. Read for its Document History; superseded by the Final.
- [OpenID for Verifiable Presentations 1.1 - Editor's draft](https://openid.github.io/OpenID4VP/openid-4-verifiable-presentations-1_1-wg-draft.html): Editor's draft, 1.1 -01 (1 October 2026), checked 2026-10-05. Draft posture: track.
- [OpenID4VC High Assurance Interoperability Profile - draft 03 (Implementer's Draft 1)](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-ID1.html): Implementer's Draft, ID1, document draft 03 (7 February 2025), checked 2026-10-05. Legacy line.
- [OpenID4VC High Assurance Interoperability Profile 1.0 - draft 06](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0-06.html): Draft, draft 06 (20 November 2025), checked 2026-10-05. Read for its Document History; superseded by the Final.
- [OpenID4VC High Assurance Interoperability Profile 1.1 - Editor's draft](https://openid.github.io/OpenID4VC-HAIP/openid4vc-high-assurance-interoperability-profile-1_1-wg-draft.html): Editor's draft, 1.1 -01 (24 September 2026), checked 2026-10-05. Draft posture: track.
- [Security and Trust in OpenID for Verifiable Credentials Ecosystems](https://openid.github.io/OpenID4VC_SecTrust/draft-oid4vc-security-and-trust.html): WG draft, draft-oid4vc-security-and-trust-latest (14 March 2024), checked 2026-10-02. Draft posture: track, because it is an unfinished, non-normative analysis.
- [Digital Credentials](https://www.w3.org/TR/digital-credentials/): W3C Working Draft, 4 September 2026, checked 2026-10-02. Draft posture: build, because OpenID4VP Appendix A and HAIP §5.2 depend on it.
- [RFC 9901: Selective Disclosure for JSON Web Tokens](https://www.rfc-editor.org/rfc/rfc9901.html): RFC (Proposed Standard), RFC 9901 (November 2025), checked 2026-10-05.
- [SD-JWT-based Verifiable Digital Credentials (SD-JWT VC)](https://datatracker.ietf.org/doc/draft-ietf-oauth-sd-jwt-vc/19/): WG draft (IETF OAuth), draft-ietf-oauth-sd-jwt-vc-19 (31 August 2026), checked 2026-10-05. Draft posture: build; HAIP pins -13.
- [Token Status List (TSL)](https://datatracker.ietf.org/doc/draft-ietf-oauth-status-list/21/): WG draft (IETF OAuth), in the RFC Editor queue, draft-ietf-oauth-status-list-21 (21 June 2026), checked 2026-10-05. Draft posture: build; HAIP pins -14.
- [DCP WG specifications](https://openid.net/wg/digital-credentials-protocols/specifications/): Index, page as read 2026-10-02, checked 2026-10-02.
- [Conformance testing for OpenID for Verifiable Presentations](https://openid.net/certification/conformance-testing-for-openid-for-verifiable-presentations/): Published, page as read 2026-10-02, checked 2026-10-02.
- [Conformance testing for OpenID for Verifiable Credential Issuance](https://openid.net/certification/conformance-testing-for-openid-for-verifiable-credential-issuance/): Published, page as read 2026-10-02, checked 2026-10-02.
