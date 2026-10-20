---
name: shared-signals
description: "Shared Signals (SSF, CAEP, RISC): send and receive security events between identity providers, apps and services. Targets the SSF 1.0, CAEP 1.0 and RISC 1.0 Finals, and upgrades peers from the Implementer's Drafts (spec_version 1_0-ID1 to 1_0-ID3); no next-line draft exists. Use when building or reviewing an OpenID Shared Signals Framework transmitter or receiver: /.well-known/ssf-configuration discovery, stream management, subjects, verification events, push delivery (RFC 8935) or poll delivery (RFC 8936), and Security Event Token validation (RFC 8417). Also use it to emit or act on CAEP events such as session-revoked, credential-change, token-claims-change, assurance-level-change, device-compliance-change and risk-level-change, or RISC account events; to apply the CAEP Interoperability Profile or the SSF conformance tests; and to feed Back-Channel Logout into revocation. Triggers: SSF, CAEP, RISC, shared signals, continuous access evaluation, SET, secevent+jwt, sub_id, RFC 9493, logout token."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Shared Signals

The OpenID Shared Signals Framework (SSF) lets a transmitter send signed security events to receivers over managed streams. CAEP defines session and access events; RISC defines account events. With this skill an agent builds or reviews a transmitter or receiver, its event payloads, and its delivery and validation logic.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: transmitter, receiver, or both.
- Delivery: push (`urn:ietf:rfc:8935`), poll (`urn:ietf:rfc:8936`), or both.
- Events: which CAEP, RISC or custom event types the stream carries.
- Target version: SSF 1.0, CAEP 1.0, RISC 1.0 (current, the default; `spec_version` `1_0`). SSF 1.0 Implementer's Draft 3, SSF 1.0 Implementer's Draft 2 and SSE Framework 1.0 Implementer's Draft 1 are legacy: read them and upgrade from them, never author them. No preview is listed. See [`references/versions.md`](references/versions.md).
- Profile: plain SSF 1.0, or the CAEP Interoperability Profile (pinned ID1, with the working-group draft tracked).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the Shared Signals WG specifications page for a newer revision, and update the pins.

## Invariants

These come from SSF 1.0 unless another document is named.

1. **Discovery is bound to the issuer** (SSF §7.2, §7.2.4). Metadata lives at `/.well-known/ssf-configuration`, inserted between host and path. Its `issuer` equals the issuer URL used for discovery and the `iss` of every SET.
2. **Each SET is a typed JWT with one event** (SSF §4.1.1, §4.2.1; RFC 8417 §2.3). The header `typ` is `secevent+jwt`. Each SET carries exactly one event in `events`.
3. **Subjects use `sub_id`, never `sub`** (SSF §3.1, §4.1.2; RFC 9493 §4.1). The top-level `sub_id` holds a subject identifier with a `format`. New event types MUST NOT use the `subject` event member (§3.1.2).
4. **No `exp` on SETs** (SSF §4.1.7). The `iss` matches the stream configuration (§4.1.6), and `aud` names the receiver (§4.1.8).
5. **Receivers validate before acting** (RFC 8935 §2, SSF §4.1, RFC 8417). They check the signature against the transmitter's `jwks_uri` keys, then `iss`, `aud`, `typ` and the event type, and they ignore unknown members (SSF §4.2.3).
6. **Delivery acknowledges correctly** (RFC 8935 §2.2, RFC 8936 §2). A push endpoint returns 202 with an empty body, or 400 with an `err` code. A poll receiver acknowledges every SET by `jti`.
7. **Streams are managed over authenticated HTTP** (SSF §8). Creating a stream returns 201, and the receiver checks the `iss` in the response. Deleting a stream returns 204.
8. **Status changes are announced** (SSF §8.1.5). Before pausing or disabling a stream, and when re-enabling it, the transmitter sends `stream-updated`. A paused stream holds events in order.
9. **Verification proves the path** (SSF §8.1.4). A verification event's `sub_id` is `opaque` with the `stream_id`. The receiver checks that `state` matches, and answers `invalid_state` if it does not.
10. **Subject handling is privacy-safe** (SSF §9.1, §9.3). An add-subject success does not mean the subject exists or that events will follow. Receivers tolerate events for subjects they removed.

## Workflow

1. **Pick the version, and pin role, delivery, events and profile.** Target the 1.0 Finals. For an existing peer, read its `spec_version` to find its line. Record the inputs.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version, event list and delivery method are named for each stream, and no draft-only shape is planned.
2. **Model SETs and subjects.** Build or parse the SET claims and subject identifiers.
   -> [`references/sets-and-subjects.md`](references/sets-and-subjects.md)
   ✓ Every SET has `typ` `secevent+jwt`, one event, a `sub_id`, and no `sub` or `exp`.
3. **Pick the event payloads.** Use the CAEP and RISC event types with their required claims.
   -> [`references/events.md`](references/events.md)
   ✓ Each event carries its required claims, using the spec's values.
4. **Implement the transmitter.** Metadata, stream configuration, status, subjects, verification and delivery.
   -> [`references/transmitter.md`](references/transmitter.md)
   ✓ The well-known document, stream CRUD, status and verify endpoints answer with the status codes in the reference.
5. **Implement the receiver.** Discovery, stream creation, SET validation and push or poll handling.
   -> [`references/receiver.md`](references/receiver.md)
   ✓ A SET with a bad signature, wrong `iss`, wrong `aud` or wrong `typ` is rejected with the RFC 8935 error code.
6. **Apply the CAEP Interoperability Profile if required.** It pins mandatory endpoints, scopes, formats, algorithms and use cases.
   -> [`references/caep-interop.md`](references/caep-interop.md)
   ✓ Every MUST in the profile for the chosen role holds.
7. **Connect Back-Channel Logout if relevant.** Validate logout tokens and map them to session revocation.
   -> [`references/backchannel-logout.md`](references/backchannel-logout.md)
   ✓ Logout tokens are validated per Back-Channel Logout §2.6 and end the matching sessions.
8. **Upgrade from an Implementer's Draft** (only when a peer runs one). Follow each upgrade section from the peer's `spec_version` to `1_0`.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded side publishes `spec_version` `1_0`, uses `ssf-configuration`, `sub_id` and URN delivery methods, and passes the checks above.

## Verify before done

- [ ] `GET /.well-known/ssf-configuration` returns metadata whose `issuer` equals the discovery URL issuer.
- [ ] Every SET header has `typ: secevent+jwt`; every payload has `iss`, `jti`, `iat`, `aud`, `sub_id` and exactly one event, and no `sub` or `exp`.
- [ ] The receiver rejects a SET signed with an unknown key, with a wrong `iss` or `aud`, or with an unknown critical subject member.
- [ ] Push returns 202 with no body on success, and 400 with `err` and `description` on failure.
- [ ] Poll acknowledges each processed `jti` and reports failures in `setErrs`.
- [ ] A verification request returns 204, and the resulting event echoes `state`.
- [ ] Pausing or disabling a stream emits `stream-updated` first.
- [ ] If the CAEP Interoperability Profile applies, the SSF conformance test plan for the role passes.

## Reference index

- **`references/versions.md`**: the 1.0 Finals and the Implementer's Draft lines by `spec_version`, which to use, what changed, and upgrade steps from each draft.
- **`references/sets-and-subjects.md`**: RFC 8417 SET claims, SSF restrictions, RFC 9493 subject formats and complex subjects.
- **`references/events.md`**: CAEP and RISC event types, their claims, and the SSF stream events.
- **`references/transmitter.md`**: metadata, stream management API, status, subjects, verification and delivery.
- **`references/receiver.md`**: discovery checks, stream creation, SET validation, push and poll handling, with TypeScript.
- **`references/caep-interop.md`**: CAEP Interoperability Profile ID1, the working-group draft changes, and SSF conformance testing.
- **`references/backchannel-logout.md`**: OpenID Connect Back-Channel Logout tokens and validation.

## Related skills

- `jwt` for JWS signing and verification of SETs: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`.
- `oauth` for the access tokens that protect the stream management API: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`.
- `openid-connect` for the sessions and logout that CAEP events revoke: `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`.
- `openid` for an overview of OpenID Foundation specifications: `npx skills add ScaleDockHQ/scaledock-skills --skill openid`.
- `fapi` for high-security OAuth deployments that consume these signals: `npx skills add ScaleDockHQ/scaledock-skills --skill fapi`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenID Shared Signals Framework Specification 1.0](https://openid.net/specs/openid-sharedsignals-framework-1_0-final.html): Final, published 29 August 2025, checked 2026-10-05.
- [OpenID Continuous Access Evaluation Profile 1.0](https://openid.net/specs/openid-caep-1_0-final.html): Final, published 29 August 2025, checked 2026-10-05.
- [OpenID RISC Profile Specification 1.0](https://openid.net/specs/openid-risc-1_0-final.html): Final, published 29 August 2025, checked 2026-10-05.
- [Shared Signals Framework 1.0, Implementer's Draft 3](https://openid.net/specs/openid-sharedsignals-framework-1_0-ID3.html): Implementer's Draft, ID3 (draft 03, 25 June 2024), checked 2026-10-05. Legacy line `1.0-id3`.
- [Shared Signals Framework 1.0, Implementer's Draft 2](https://openid.net/specs/openid-sharedsignals-framework-1_0-ID2.html): Implementer's Draft, ID2 (draft 02, 9 October 2023), checked 2026-10-05. Legacy line `1.0-id2`.
- [Shared Signals and Events Framework 1.0, Implementer's Draft 1](https://openid.net/specs/openid-sse-framework-1_0-ID1.html): Implementer's Draft, ID1 (draft 01, 8 June 2021), checked 2026-10-05. Legacy line `1.0-id1`.
- [Continuous Access Evaluation Profile 1.0, Implementer's Draft 2](https://openid.net/specs/openid-caep-1_0-ID2.html): Implementer's Draft, ID2 (draft 03, 19 June 2024), checked 2026-10-05.
- [Continuous Access Evaluation Profile 1.0, Implementer's Draft 1](https://openid.net/specs/openid-caep-specification-1_0-ID1.html): Implementer's Draft, ID1 (draft 02, 9 August 2021), checked 2026-10-05.
- [RISC Profile Specification 1.0, Implementer's Draft 2](https://openid.net/specs/openid-risc-profile-specification-1_0-ID2.html): Implementer's Draft, ID2 (draft 02, 5 April 2022), checked 2026-10-05.
- [RISC Profile of IETF Security Events 1.0, Implementer's Draft 1](https://openid.net/specs/openid-risc-profile-1_0-ID1.html): Implementer's Draft, ID1 (24 April 2018), checked 2026-10-05. Predates the SSE framework.
- [CAEP Interoperability Profile](https://openid.net/specs/openid-caep-interoperability-profile-1_0-ID1.html): Implementer's Draft, ID1 (document labelled draft 00, 25 June 2024), checked 2026-10-02. Draft posture: build, pinned to ID1.
- [CAEP Interoperability Profile, working-group draft](https://openid.github.io/sharedsignals/openid-caep-interoperability-profile-1_0.html): WG draft, draft 01, 1 September 2026, checked 2026-10-02. Draft posture: track, because the SSF conformance tests already follow it.
- [RFC 8417: Security Event Token (SET)](https://www.rfc-editor.org/rfc/rfc8417.txt): RFC, July 2018, checked 2026-10-02.
- [RFC 8935: Push-Based SET Delivery Using HTTP](https://www.rfc-editor.org/rfc/rfc8935.txt): RFC, November 2020, checked 2026-10-02.
- [RFC 8936: Poll-Based SET Delivery Using HTTP](https://www.rfc-editor.org/rfc/rfc8936.txt): RFC, November 2020, checked 2026-10-02.
- [RFC 9493: Subject Identifiers for Security Event Tokens](https://www.rfc-editor.org/rfc/rfc9493.txt): RFC, December 2023, checked 2026-10-02.
- [OpenID Connect Back-Channel Logout 1.0](https://openid.net/specs/openid-connect-backchannel-1_0.html): Final, 1.0 incorporating errata set 1, 15 December 2023, checked 2026-10-02.
- [Shared Signals WG specifications](https://openid.net/wg/sharedsignals/specifications/): Index, page as read 2026-10-05, checked 2026-10-05.
- [OpenID Shared Signals conformance testing](https://openid.net/certification/ssf_testing/): Published (tests in alpha), page as read 2026-10-02, checked 2026-10-02.
