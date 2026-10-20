---
name: tls
description: >-
  TLS 1.3: prevent eavesdropping, tampering and message forgery. Covers RFC 9846 The Transport Layer Security (TLS) Protocol Version 1.3, RFC 9325 Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS), RFC 8705 OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens, and TLS Encrypted Client Hello. Use when configuring TLS. Triggers: TLS 1.3, RFC 9846.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
  kind: standard
---

# The Transport Layer Security (TLS) Protocol Version 1.3

The Transport Layer Security (TLS) Protocol Version 1.3

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when configuring TLS.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9846 The Transport Layer Security (TLS) Protocol Version 1.3 (default); RFC 8446 The Transport Layer Security (TLS) Protocol Version 1.3 (legacy); RFC 5246 The Transport Layer Security (TLS) Protocol Version 1.2 (legacy); RFC 9325 Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS) (default); RFC 8705 OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens (default); TLS Encrypted Client Hello (preview, posture track: emit only when the user opts in and the posture is build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9846 § 4.2.3.** "TLS 1.3 servers which negotiate TLS 1.2 or below in response to a ClientHello MUST set the last 8 bytes of their Random value specially in their ServerHello."
2. **RFC 9846 § 4.3.8.** "Clients and Servers MUST NOT reuse a key share for multiple connections."
3. **RFC 9846 § 4.5.2.** "The receiver of a CertificateVerify message MUST verify the signature field."
4. **RFC 9846 § 4.5.3.** "Recipients of Finished messages MUST verify that the contents are correct and if incorrect MUST terminate the connection with a "decrypt_error" alert."
5. **RFC 9846 § 6.** "Upon receiving an error alert, the TLS implementation SHOULD indicate an error to the application and MUST NOT allow any further data to be sent or received on the connection."
6. **RFC 9846 § 8.** "The server MUST ensure that any instance of it (be it a machine, a thread, or any other entity within the relevant serving infrastructure) would accept 0-RTT for the same 0-RTT handshake at most once; this limits the number of replays to the number of server instances in the deployment."
7. **RFC 9846 § 9.3.** "A server receiving a ClientHello MUST correctly ignore all unrecognized cipher suites, extensions, and other parameters."
8. **RFC 9325 § 3.1.1.** "Implementations MUST NOT negotiate TLS version 1.1 [RFC4346]."
9. **RFC 9325 § 4.1.** "Implementations MUST support and prefer to negotiate cipher suites offering forward secrecy."
10. **RFC 8705 § 3.** "The protected resource MUST obtain, from its TLS implementation layer, the client certificate used for mutual TLS and MUST verify that the certificate matches the certificate associated with the access token."

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

- [RFC 9846 The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc9846): Proposed Standard, RFC 9846, July 2026, checked 2026-10-06.
- [RFC 8446 The Transport Layer Security (TLS) Protocol Version 1.3](https://www.rfc-editor.org/rfc/rfc8446.html): PROPOSED STANDARD, RFC 8446 (PROPOSED STANDARD, August 201), checked 2026-10-06.
- [RFC 5246 The Transport Layer Security (TLS) Protocol Version 1.2](https://www.rfc-editor.org/rfc/rfc5246.html): PROPOSED STANDARD, RFC 5246 (PROPOSED STANDARD, August 200), checked 2026-10-06.
- [RFC 9325 Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)](https://www.rfc-editor.org/rfc/rfc9325.html): BEST CURRENT PRACTICE, RFC 9325 (BEST CURRENT PRACTICE, November 2), checked 2026-10-06.
- [RFC 8705 OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens](https://www.rfc-editor.org/rfc/rfc8705.html): PROPOSED STANDARD, RFC 8705 (PROPOSED STANDARD, February 2), checked 2026-10-06.
- [TLS Encrypted Client Hello](https://datatracker.ietf.org/doc/html/draft-ietf-tls-esni-25): WG draft, draft-ietf-tls-esni-25 (WG draft, 2026-10-06), checked 2026-10-06.
