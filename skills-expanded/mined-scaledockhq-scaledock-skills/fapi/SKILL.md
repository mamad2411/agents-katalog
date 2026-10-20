---
name: fapi
description: "FAPI 2.0: high-security OAuth profile for financial-grade APIs. Use when building or reviewing an authorization server, client or resource server that must meet the OpenID FAPI 2.0 Security Profile or FAPI 2.0 Message Signing: PAR, PKCE S256, sender-constrained tokens with DPoP or mTLS, private_key_jwt or mTLS client authentication, PS256, ES256 or Ed25519, the RFC 9207 iss parameter, short code lifetimes and strict redirect URIs. Also use it to migrate from FAPI 1.0 Baseline or Advanced, to apply JARM, FAPI-CIBA or Grant Management, and to prepare for OpenID FAPI certification. Triggers: FAPI, FAPI2, financial-grade API, open banking, open finance, high-security OAuth, PAR, DPoP, MTLS, JARM, signed request object, x-fapi-interaction-id, CIBA, grant_id."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# FAPI

FAPI is the OpenID Foundation's family of high-security OAuth 2.0 profiles. FAPI 2.0 is the current family and FAPI 1.0 is the legacy family. With this skill an agent configures or reviews an authorization server, a client or a resource server so that it meets the FAPI 2.0 Security Profile, adds FAPI 2.0 Message Signing when non-repudiation is needed, and prepares for the OpenID conformance suite.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: authorization server (AS), client, or resource server (RS). Many reviews cover all three.
- Target version: FAPI 2.0 (current, the default). FAPI 1.0 is legacy: read it and migrate from it, and build it only when a named ecosystem still mandates it; the FAPI WG strongly recommends FAPI 2.0 for new ecosystems (FAPI WG specifications page). No preview is listed. See [`references/versions.md`](references/versions.md).
- Profile: FAPI 2.0 Security Profile alone, or with FAPI 2.0 Message Signing.
- Options: sender-constraining with DPoP or mTLS; client authentication with `private_key_jwt` or mTLS; whether OpenID Connect is used; any ecosystem profile on top (it may add rules but shall not remove mandatory behaviour, FAPI 2.0 SP §5.1.2).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the FAPI WG specifications page for a newer revision, and update the pins.

## Invariants

These come from the FAPI 2.0 Security Profile (SP) unless another document is named.

1. **Confidential clients only** (SP §5.1.1, §5.3.2.1). Public clients are out of scope. The AS rejects the resource owner password credentials grant.
2. **Authorization code flow through PAR, with PKCE S256** (SP §5.3.2.2). `response_type=code` only. The AS rejects authorization requests that were not pushed, and pushed requests without client authentication. `redirect_uri` is required in the PAR request.
3. **Sender-constrained access tokens only** (SP §5.3.2.1, §5.3.3.1, §5.3.4). Use mTLS (RFC 8705) or DPoP (RFC 9449). Every party verifies the binding.
4. **Client authentication with mTLS or `private_key_jwt`** (SP §5.3.2.1). The AS accepts only its issuer identifier, as a string, in the `aud` of a client assertion.
5. **Mix-up defence with `iss`** (SP §5.3.2.2, §5.3.3.2). The AS returns `iss` in the authorization response (RFC 9207), and the client checks it.
6. **Short lifetimes and single use** (SP §5.3.2.1, §5.3.2.2). Authorization codes live at most 60 seconds and are rejected on reuse. A PAR `expires_in` is under 600 seconds.
7. **Strict redirects** (SP §5.3.2.1, §5.3.2.2). No `http` redirect URIs except native-app loopback (RFC 8252 §7.3). No open redirectors. Redirect with 303, never 307.
8. **Algorithms and keys** (SP §5.4.1). JWTs follow RFC 8725 and use PS256, ES256 or EdDSA with Ed25519, never `none`. RSA keys are at least 2048 bits and EC keys at least 224 bits. Machine credentials have at least 128 bits of entropy.
9. **Transport** (SP §5.2). TLS 1.2 or later per BCP 195, with certificate checks per RFC 9525. Browser-facing endpoints prevent TLS stripping. The authorization endpoint does not support CORS.
10. **Tokens in headers only** (SP §5.3.3.1, §5.3.4). Clients send access tokens in the `Authorization` header. Resource servers reject tokens in the query string.
11. **Message Signing, when chosen, signs every leg it claims** (Message Signing §5.3 to §5.6). Signed request objects at PAR, JARM responses, signed introspection responses and verified ID tokens are separate conformance options, and each one is implemented in full.

## Workflow

1. **Pick the version, profile and options.** Use FAPI 2.0 unless a named ecosystem mandates FAPI 1.0. Record the profile, sender-constraining method, client authentication method and any ecosystem profile from the inputs.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version and every option are named, and nothing in the ecosystem profile removes a FAPI 2.0 requirement.
2. **Configure the authorization server.** Metadata, PAR, PKCE, the authorization and token endpoints, lifetimes, clock tolerance and refresh tokens.
   -> [`references/authorization-server.md`](references/authorization-server.md)
   ✓ Every AS row in the checklist holds, and a request without PAR is rejected.
3. **Build or review the client.** Discovery, PAR, PKCE, the `iss` check, DPoP or mTLS, and token use.
   -> [`references/client.md`](references/client.md)
   ✓ The client sends only `client_id` and `request_uri` to the authorization endpoint and rejects a response with the wrong `iss`.
4. **Protect the resource server.** Header-only tokens, validation and sender-constraint checks.
   -> [`references/resource-server.md`](references/resource-server.md)
   ✓ A bearer-only token, a query-string token and a token presented with the wrong key are all rejected.
5. **Check cryptography and key distribution.** Algorithms, key sizes, `jwks_uri` and `kid` handling.
   -> [`references/cryptography.md`](references/cryptography.md)
   ✓ Only PS256, ES256 or Ed25519 keys are published or accepted, and `none` is refused.
6. **Add Message Signing if required.** Signed request objects, JARM, signed introspection and ID token verification.
   -> [`references/message-signing.md`](references/message-signing.md)
   ✓ Each chosen option is implemented on both sides.
7. **Upgrade from FAPI 1.0** (only when the deployment is on FAPI 1.0). Follow the 1.0 to 2.0 upgrade steps, which use the migration checklist in `fapi-1.md`.
   -> [`references/versions.md`](references/versions.md), [`references/fapi-1.md`](references/fapi-1.md)
   ✓ Every FAPI 1.0 to 2.0 difference is resolved for the deployment, and the FAPI 2.0 test plans pass.
8. **Apply drafts only when asked.** FAPI-CIBA for decoupled flows and Grant Management for grant lifecycle APIs.
   -> [`references/ciba-and-grant-management.md`](references/ciba-and-grant-management.md)
   ✓ Draft features are labelled with the pinned revision.
9. **Review against the attacker model.** Walk the attackers and the security considerations.
   -> [`references/attacker-model.md`](references/attacker-model.md)
   ✓ Each attacker class has a named mitigation.
10. **Prepare certification.** Configure the conformance suite test plans.
    -> [`references/certification.md`](references/certification.md)
    ✓ The right test plan per option is identified, with two clients and the suite's redirect URIs.

## Verify before done

- [ ] AS metadata advertises PAR, PKCE S256, only FAPI client authentication methods and only FAPI signing algorithms.
- [ ] An authorization request without PAR, a PAR request without client authentication and a request without PKCE S256 are each rejected.
- [ ] The authorization response carries `iss`, and the client rejects a mismatched `iss`.
- [ ] Authorization codes expire within 60 seconds and fail on second use; `request_uri` `expires_in` is under 600.
- [ ] Access tokens are DPoP-bound or certificate-bound, and the RS rejects them without a matching proof.
- [ ] No endpoint accepts `alg: none`, RS256 or keys below the minimum sizes.
- [ ] If Message Signing is in scope, each chosen option passes its own test plan.
- [ ] The conformance suite plan for each configured variant finishes with no failures.

## Reference index

- **`references/versions.md`**: the FAPI 2.0 and FAPI 1.0 lines with their status, which one to use, what changed, the 1.0 to 2.0 upgrade steps, and why no preview is listed.
- **`references/authorization-server.md`**: AS requirements, metadata, PAR, PKCE, lifetimes, clock skew and refresh tokens.
- **`references/client.md`**: client requirements and request examples for PAR, `private_key_jwt` and DPoP.
- **`references/resource-server.md`**: RS validation steps and a framework-neutral TypeScript check.
- **`references/cryptography.md`**: algorithms, key sizes, JWKS rules, duplicate `kid` handling and the Ed25519 identifier.
- **`references/message-signing.md`**: FAPI 2.0 Message Signing and JARM processing rules.
- **`references/fapi-1.md`**: FAPI 1.0 Baseline and Advanced, and the differences from FAPI 2.0.
- **`references/ciba-and-grant-management.md`**: the FAPI-CIBA and Grant Management Implementer's Drafts.
- **`references/attacker-model.md`**: security goals, attacker classes and security considerations.
- **`references/certification.md`**: OpenID conformance suite setup for FAPI servers and clients.

## Related skills

- `oauth` for the underlying OAuth 2.0 framework, PAR, PKCE, DPoP and mTLS: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`.
- `jwt` for JWT, JWS and JWK processing and RFC 8725: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`.
- `openid-connect` for ID tokens and discovery when FAPI is used with OpenID Connect: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`.
- `openid` for an overview of OpenID Foundation specifications: `npx skills add ScaleDockHQ/scaledock-skills --skill openid`.
- `openid4vc` because HAIP builds its issuance profile on FAPI 2.0: `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`.
- `shared-signals` for session and credential revocation events between FAPI parties: `npx skills add ScaleDockHQ/scaledock-skills --skill shared-signals`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [FAPI 2.0 Security Profile](https://openid.net/specs/fapi-security-profile-2_0-final.html): Final, published 22 February 2025, checked 2026-10-05.
- [FAPI 2.0 Message Signing](https://openid.net/specs/fapi-message-signing-2_0-final.html): Final, published 25 September 2025, checked 2026-10-02.
- [FAPI 2.0 Attacker Model](https://openid.net/specs/fapi-attacker-model-2_0-final.html): Final, published 22 February 2025, checked 2026-10-02.
- [FAPI 1.0 Part 1: Baseline](https://openid.net/specs/openid-financial-api-part-1-1_0.html): Final, 12 March 2021, checked 2026-10-02.
- [FAPI 1.0 Part 2: Advanced](https://openid.net/specs/openid-financial-api-part-2-1_0.html): Final, 12 March 2021, checked 2026-10-02.
- [JWT Secured Authorization Response Mode for OAuth 2.0 (JARM)](https://openid.net/specs/oauth-v2-jarm-final.html): Final, published 9 November 2022, checked 2026-10-02.
- [JARM incorporating errata set 1](https://openid.net/specs/oauth-v2-jarm.html): Final with errata set 1, 17 August 2025, checked 2026-10-02.
- [FAPI: Client Initiated Backchannel Authentication Profile](https://openid.net/specs/openid-financial-api-ciba-ID1.html): Implementer's Draft, ID1 (document labelled Draft-02, 15 August 2019), checked 2026-10-02. Draft posture: build, pinned to ID1, because the conformance suite certifies it.
- [Grant Management for OAuth 2.0](https://openid.net/specs/oauth-v2-grant-management-ID1.html): Implementer's Draft, ID1 (document labelled oauth-v2-grant-management-03, 9 May 2023), checked 2026-10-02. Draft posture: track, pinned to ID1.
- [RFC 9864: Fully-Specified Algorithms for JOSE and COSE](https://www.rfc-editor.org/rfc/rfc9864.txt): RFC, October 2025, checked 2026-10-02.
- [RFC 9126: OAuth 2.0 Pushed Authorization Requests](https://www.rfc-editor.org/rfc/rfc9126.txt): RFC, September 2021, checked 2026-10-02.
- [RFC 9207: OAuth 2.0 Authorization Server Issuer Identification](https://www.rfc-editor.org/rfc/rfc9207.txt): RFC, March 2022, checked 2026-10-02.
- [RFC 9449: OAuth 2.0 Demonstrating Proof of Possession (DPoP)](https://www.rfc-editor.org/rfc/rfc9449.txt): RFC, September 2023, checked 2026-10-02.
- [RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705.txt): RFC, February 2020, checked 2026-10-02.
- [RFC 7523: JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants](https://www.rfc-editor.org/rfc/rfc7523.txt): RFC, May 2015, checked 2026-10-02.
- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750.txt): RFC, October 2012, checked 2026-10-02.
- [OpenID Certification](https://openid.net/certification/): Published, page as read 2026-10-02, checked 2026-10-02.
- [FAPI WG specifications](https://openid.net/wg/fapi/specifications/): Index, page as read 2026-10-05, checked 2026-10-05.
- [Conformance Testing for FAPI OPs](https://openid.net/certification/certification-fapi_op_testing/): Published, page as read 2026-10-02, checked 2026-10-02.
- [FAPI RP certification submission](https://openid.net/certification/fapi_rp_submission/): Published, page as read 2026-10-02, checked 2026-10-02.
- [Conformance Testing for FAPI-CIBA OPs](https://openid.net/certification/fapi_ciba_op_testing/): Published, page as read 2026-10-02, checked 2026-10-02.
