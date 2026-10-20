---
name: ciba
description: >-
  OpenID CIBA Core 1.0: build and review Client-Initiated Backchannel
  Authentication, where the client starts sign-in and the user approves on a
  separate authentication device. Use when implementing or reviewing a CIBA
  OpenID Provider or client: the backchannel authentication endpoint and
  request (login_hint, login_hint_token, id_token_hint, binding_message,
  user_code, requested_expiry, client_notification_token, signed request
  objects), the auth_req_id acknowledgement, poll, ping and push token
  delivery with their client registration and discovery metadata
  (backchannel_token_delivery_mode, backchannel_authentication_endpoint), the
  urn:openid:params:grant-type:ciba token request, authorization_pending,
  slow_down, expired_token and access_denied, push-mode ID Token claims
  (at_hash, urn:openid:params:jwt:claim:auth_req_id, rt_hash), and
  cross-device approval.
  Targets CIBA Core 1.0 (Final), upgrades from the Implementer's Drafts and the
  2017 MODRNA draft, and tracks the CIBA Core 1.0 errata set 1 draft.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# CIBA

OpenID Connect Client-Initiated Backchannel Authentication Flow (CIBA) Core 1.0 is an OpenID Foundation specification from the MODRNA working group. The client posts an authentication request straight to the OpenID Provider (OP), without a browser redirect. The user authenticates and consents on an Authentication Device (AD), often a phone, while using the client on a separate Consumption Device (CD). The client then gets the tokens by poll, ping or push (CIBA §1, §2, §3). With this skill the agent builds or reviews a CIBA OP or client that meets the MUST-level rules of the Final specification.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: OpenID Provider (authorization server) or client (relying party), or both.
- Delivery mode: poll, ping or push. A client registers exactly one (CIBA §4, §10).
- User hint: `login_hint`, `login_hint_token` or `id_token_hint`, and where the client gets it.
- Profile: plain CIBA, or FAPI-CIBA for high-security APIs, which the `fapi` skill covers.
- Target version: CIBA Core 1.0 (current, the default; Final, 1 September 2021). CIBA Core Implementer's Draft 2, CIBA Core Implementer's Draft 1 and MODRNA CIBA 1.0 Implementer's Draft 1 are legacy: read them and upgrade from them, never author them. CIBA Core 1.0 errata set 1 draft is a preview (posture: track): do not build OP behaviour from it yet. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first. Check the MODRNA specifications page and the "Errata Corrections" section of the OpenID specifications list for an approved CIBA errata set, then update the pins.

## Invariants

1. **`openid` scope and exactly one hint.** A CIBA request MUST contain the `openid` scope and exactly one of `login_hint_token`, `id_token_hint` or `login_hint`. The OP MUST answer more than one hint with `invalid_request` (§7.1, §7.2, §13).
2. **Authenticated client over TLS.** The client MUST authenticate to the backchannel authentication endpoint with its registered method, and the endpoint MUST use TLS. With JWT client assertions the client SHOULD use the OP's Issuer Identifier as audience. The OP MUST accept the issuer, the token endpoint URL or the backchannel authentication endpoint URL (§7, §7.1).
3. **Signed requests carry everything in the JWT.** A signed request sends all parameters as claims of an asymmetrically signed JWT. The JWT has `aud` set to the OP issuer, `iss` set to the `client_id`, and `exp`, `iat`, `nbf` and `jti`. It travels in the `request` parameter, and no request parameter may appear outside it. Encrypted requests are not supported (§7.1.1).
4. **`auth_req_id` is unguessable and opaque.** It MUST have at least 128 bits of entropy (160 recommended) and use only `A-Z a-z 0-9 . - _`. The client MUST treat it as opaque. `expires_in` is REQUIRED, and a missing `interval` means 5 seconds (§7.3).
5. **One delivery mode, chosen at registration.** The OP MUST deliver the result only through the registered mode. A push client MUST NOT call the token endpoint with the CIBA grant, and the OP answers `unauthorized_client` (§4, §10, §11).
6. **Poll politely.** The client MUST NOT poll more often than `interval`, MUST NOT send overlapping requests for one `auth_req_id`, and on `slow_down` MUST add at least 5 seconds to the interval for all later requests (§10.1, §11).
7. **Callbacks are authenticated by the client's token.** For ping and push, `client_notification_token` is REQUIRED, at most 1024 characters, RFC 6750 bearer syntax, with at least 128 bits of entropy. The client MUST check it on every callback against the `auth_req_id` (§7.1, §10.2, §10.3.1).
8. **HTTPS callbacks, no redirects.** `backchannel_client_notification_endpoint` MUST be an HTTPS URL. The client MUST NOT answer a callback with 3xx, and the OP MUST NOT follow redirects (§4, §9, §10.2, §10.3.1).
9. **Push binds the tokens in the ID Token.** In push mode the ID Token MUST carry `at_hash` and `urn:openid:params:jwt:claim:auth_req_id`, plus `urn:openid:params:jwt:claim:rt_hash` when a refresh token is sent. The client MUST validate the ID Token and all three bindings (§10.3.1).
10. **`auth_req_id` is single-use and client-bound.** After a successful token response it is no longer valid. An unknown `auth_req_id`, or one issued to another client, gets `invalid_grant` (§10.1, §10.1.1, §11).
11. **User codes are never stored.** The client MUST NOT store the `user_code` and asks the user for it on each flow (§7.1.2).

## Workflow

1. **Pick the version.** Target CIBA Core 1.0. Read older documents as input to an upgrade.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is CIBA Core 1.0, and nothing is built from a legacy draft or the errata draft.
2. **Publish and register the metadata.** OP: advertise `backchannel_authentication_endpoint`, `backchannel_token_delivery_modes_supported` and the CIBA grant type. Client: register `backchannel_token_delivery_mode`, the CIBA grant type for poll or ping, and a notification endpoint for ping or push.
   -> [`references/backchannel-request.md`](references/backchannel-request.md)
   ✓ The registration matches §4 for the chosen mode, including the pairwise identifier rules if `subject_type` is `pairwise`.
3. **Send the authentication request (client).** Authenticate as the client and choose one hint. Add `binding_message`, `user_code`, `requested_expiry` and `client_notification_token` as needed, and sign the request if one was registered.
   -> [`references/backchannel-request.md`](references/backchannel-request.md)
   ✓ The request has `openid`, one hint, and no parameters outside the JWT when signed.
4. **Validate and acknowledge (OP).** Authenticate the client, verify the signed request, check the hint and the user, and return `auth_req_id`, `expires_in` and `interval`, or an authentication error.
   -> [`references/backchannel-request.md`](references/backchannel-request.md)
   ✓ Each §13 error code is reachable, and the acknowledgement passes the §7.3 rules.
5. **Authenticate the user on the authentication device (OP).** Reach the user out of band, honour `acr_values`, show the `binding_message`, and get an authorization decision as in OpenID Connect Core §3.1.2.4 (§8).
   ✓ The user sees the same binding message on both devices.
6. **Deliver the result.** Poll or ping: token request with `urn:openid:params:grant-type:ciba`. Push: POST the tokens to the notification endpoint.
   -> [`references/delivery-modes.md`](references/delivery-modes.md)
   ✓ The client handles every §11 or §12 error code and stops at `expires_in`.
7. **Review security and privacy.** Check unsolicited requests, binding messages, hint validation, notification endpoint ownership, push-mode bindings, and privacy-friendly identifiers. For FAPI, apply FAPI-CIBA through the `fapi` skill.
   -> [`references/security.md`](references/security.md)
   ✓ Each item in the security checklist has a mitigation or a reason it does not apply.
8. **Upgrade** (only when asked). Follow the steps from the source draft to CIBA Core 1.0.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded OP or client passes the Verify list below, and the delivery mode is unchanged.

## Verify before done

- [ ] OP metadata lists `backchannel_authentication_endpoint` and `backchannel_token_delivery_modes_supported`. For poll or ping, `grant_types_supported` includes `urn:openid:params:grant-type:ciba` (§4).
- [ ] A request with two hints, or without `openid`, is rejected with `invalid_request` (§7.1, §7.2, §13).
- [ ] A signed request with a parameter outside the JWT is rejected; the JWT has `aud`, `iss`, `exp`, `iat`, `nbf` and `jti` (§7.1.1).
- [ ] `auth_req_id` values use only the §7.3 character set and are rejected after one successful redemption (§7.3, §10.1.1).
- [ ] A poll faster than `interval` gets `slow_down` or `invalid_request`, and the client then adds 5 seconds or stops (§11).
- [ ] A ping or push callback with a wrong bearer token gets 401 from the client, and no 3xx is ever returned (§10.2, §10.3.1).
- [ ] A push ID Token's `at_hash`, `urn:openid:params:jwt:claim:rt_hash` and `urn:openid:params:jwt:claim:auth_req_id` match the delivered values (§10.3.1).
- [ ] A push-mode client calling the token endpoint gets `unauthorized_client` (§11).
- [ ] Nothing depends on the errata draft's sole-audience rule unless the user opted in (see versions).

## Reference index

- **`references/versions.md`**: every CIBA line, the Implementer's Drafts and the 2017 MODRNA draft, what each changed, the upgrade steps, and the errata set 1 draft. Load for steps 1 and 8.
- **`references/backchannel-request.md`**: discovery and registration metadata, pairwise identifiers, request parameters, signed requests, user codes, OP validation, the acknowledgement and authentication errors. Load for steps 2 to 4.
- **`references/delivery-modes.md`**: poll, ping and push, the CIBA grant token request, long polling, callbacks, push ID Token bindings, sender-constrained push tokens, token and push errors. Load for step 6.
- **`references/security.md`**: CIBA security and privacy considerations, a summary of the FAPI-CIBA constraints, and a review checklist. Load for step 7.

## Related skills

- `openid`, for the OpenID Foundation spec index, MODRNA and maturity terms: `npx skills add ScaleDockHQ/scaledock-skills --skill openid`
- `openid-connect`, for ID Token validation, `at_hash`, client authentication and Discovery: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`
- `oauth`, for OAuth 2.0 token endpoint errors, mTLS and sender-constrained tokens: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`
- `fapi`, for the FAPI-CIBA profile and certification: `npx skills add ScaleDockHQ/scaledock-skills --skill fapi`
- `jwt`, for signing and validating signed authentication requests: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenID Connect Client-Initiated Backchannel Authentication Flow - Core 1.0](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0.html): Final, 1 September 2021, checked 2026-10-05.
- [CIBA Core 1.0 - draft 06 incorporating errata set 1](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0-06.html): Draft (proposed errata), published 23 January 2025, checked 2026-10-05. Draft posture: track.
- [CIBA Core 1.0 draft-04](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0-04.html): Draft, 4 June 2021, the last draft before Final, checked 2026-10-05.
- [CIBA Core 1.0 Implementer's Draft 2](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0-ID2.html): Implementer's Draft, draft-03 (22 January 2020), checked 2026-10-05.
- [CIBA Core 1.0 Implementer's Draft 1](https://openid.net/specs/openid-client-initiated-backchannel-authentication-core-1_0-ID1.html): Implementer's Draft, draft-02 (16 January 2019), checked 2026-10-05.
- [OpenID Connect MODRNA Client initiated Backchannel Authentication Flow 1.0](https://openid.net/specs/openid-connect-modrna-client-initiated-backchannel-authentication-1_0.html): Implementer's Draft 1 (same document as the `-ID1` URL), 6 March 2017, replaced by CIBA Core, checked 2026-10-05.
- [OpenID Specifications](https://openid.net/developers/specs/): index page; lists CIBA Core under MODRNA Final Specifications and has no CIBA entry under Errata Corrections, checked 2026-10-05.
- [MODRNA Working Group](https://openid.net/wg/mobile/): working group page, checked 2026-10-05.
- [MODRNA Working Group Specifications](https://openid.net/wg/modrna/specifications/): index page; lists CIBA Core as Final and draft 06 incorporating errata set 1 under Drafts, checked 2026-10-05.
- [FAPI: Client Initiated Backchannel Authentication Profile](https://openid.net/specs/openid-financial-api-ciba-ID1.html): Implementer's Draft, ID1 (labelled Draft-02, 15 August 2019), checked 2026-10-05.
- [FAPI Client Initiated Backchannel Authentication Profile (working copy)](https://openid.bitbucket.io/fapi/fapi-ciba.html): Draft, published 26 June 2026, checked 2026-10-05.
- [RFC 6749: The OAuth 2.0 Authorization Framework](https://www.rfc-editor.org/rfc/rfc6749): RFC (Proposed Standard), RFC 6749, checked 2026-10-05.
- [RFC 8414: OAuth 2.0 Authorization Server Metadata](https://www.rfc-editor.org/rfc/rfc8414): RFC (Proposed Standard), RFC 8414, checked 2026-10-05.
- [RFC 8628: OAuth 2.0 Device Authorization Grant](https://www.rfc-editor.org/rfc/rfc8628): RFC (Proposed Standard), RFC 8628, checked 2026-10-05.
