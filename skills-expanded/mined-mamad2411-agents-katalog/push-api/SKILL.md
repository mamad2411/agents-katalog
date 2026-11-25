---
name: push-api
description: >-
  Push API: The Push API enables sending of a push message to a web application via a push service . Covers Push API (track). Use when subscribing to or delivering a web push message. Triggers: Push API, pushManager, RFC 8030.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Push API

The Push API enables sending of a push message to a web application via a push service . An application server can send a push message at any time, even when a web application or user agent is inactive. The push service ensures reliable and efficient delivery to the user agent . Push messages are delivered to a Service Worker that runs in the origin of the web application, which can use the information in the message to update local state or display a notification to the user. This specification is designed for use with the web push protocol , which describes how an application server or user agent interacts with a push service .

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when subscribing to or delivering a web push message.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Push API (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 3.4.** "A push endpoint MUST uniquely identify the push subscription."
2. **§ 3.4.3.** "When a push subscription is deactivated, both the user agent and the push service MUST delete any stored copies of its details."
3. **§ 4.** "The push endpoint MUST NOT expose information about the user to be derived by actors other than the push service, such as the user's device, identity or location."
4. **§ 7.** "User agents MUST support the aes128gcm content coding defined in [RFC8291], and MAY support content codings defined in previous versions of the draft for compatibility reasons."
5. **§ 7.2.** "If present, the value of applicationServerKey MUST include a point on the P-256 elliptic curve [DSS], encoded in the uncompressed form described in [ANSI-X9-62] Annex A (that is, 65 octets, starting with an 0x04 octet)."
6. **RFC 8030 § 3.** "The push service MUST use HTTP over Transport Layer Security (TLS) [RFC2818] following the recommendations in [RFC7525]."
7. **RFC 8030 § 5.2.** "An application server MUST include the TTL (Time-To-Live) header field in its request for push message delivery."
8. **RFC 8291 § 3.2.** "A user agent MUST generate and provide a hard-to-guess sequence of 16 octets that is used for authentication of push messages."
9. **RFC 8291 § 4.** "An application server MUST encrypt a push message with a single record."
10. **RFC 8292 § 2.** "The signature MUST use ECDSA on the NIST P-256 curve [FIPS186], which is identified as "ES256" [RFC7518]."
11. **RFC 8292 § 3.2.** "An application server MUST select a different private key for the key exchange [RFC8291] and signing the authentication token."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Push API](https://www.w3.org/TR/push-api/): Working Draft, push-api WD-push-api-20261005 (Working Draft, 2026-10-05), checked 2026-10-06.
- [Generic Event Delivery Using HTTP Push](https://www.rfc-editor.org/rfc/rfc8030.html): RFC, RFC 8030, checked 2026-10-06.
- [Message Encryption for Web Push](https://www.rfc-editor.org/rfc/rfc8291.html): RFC, RFC 8291, checked 2026-10-06.
- [Voluntary Application Server Identification (VAPID) for Web Push](https://www.rfc-editor.org/rfc/rfc8292.html): RFC, RFC 8292, checked 2026-10-06.
