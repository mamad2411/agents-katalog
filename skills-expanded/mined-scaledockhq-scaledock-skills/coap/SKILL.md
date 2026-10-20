---
name: coap
description: >-
  CoAP (RFC 7252): build REST-style request and response messaging over UDP for constrained devices. Covers RFC 7252 The Constrained Application Protocol (CoAP). Use when speaking the Constrained Application Protocol. Triggers: CoAP, RFC 7252.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# The Constrained Application Protocol (CoAP)

The Constrained Application Protocol (CoAP)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when speaking the Constrained Application Protocol.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 7252 The Constrained Application Protocol (CoAP) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 7252 § 3.** "The presence of a marker followed by a zero-length payload MUST be processed as a message format error."
2. **RFC 7252 § 4.2.** "The Acknowledgement message MUST echo the Message ID of the Confirmable message and MUST carry a response or be Empty (see Sections 5.2.1 and 5.2.2)."
3. **RFC 7252 § 4.4.** "The same Message ID MUST NOT be reused (in communicating with the same endpoint) within the EXCHANGE_LIFETIME (Section 4.8.2)."
4. **RFC 7252 § 4.7.** "In order not to cause congestion, clients (including proxies) MUST strictly limit the number of simultaneous outstanding interactions that they maintain to a given server (including proxies) to NSTART."
5. **RFC 7252 § 5.3.1.** "Every request carries a client-generated token that the server MUST echo (without modification) in any resulting response."
6. **RFC 7252 § 5.3.2.** "In a piggybacked response, the Message ID of the Confirmable request and the Acknowledgement MUST match, and the tokens of the response and original request MUST match."
7. **RFC 7252 § 5.4.1.** "Unrecognized options of class "critical" that occur in a Confirmable request MUST cause the return of a 4.02 (Bad Option) response."
8. **RFC 7252 § 5.7.1.** "A CoAP-to-CoAP proxy MUST forward to the origin server all Safe-to-Forward options that it does not recognize."
9. **RFC 7252 § 8.1.** "To avoid an implosion of error responses, when a server is aware that a request arrived via multicast, it MUST NOT return a Reset message in reply to a Non-confirmable message."
10. **RFC 7252 § 9.1.2.** "This means the response to a DTLS secured request MUST always be DTLS secured using the same security session and epoch."
11. **RFC 7252 § 11.2.** "Unlike the "coap" scheme, responses to "coaps" identified requests are never "public" and thus MUST NOT be reused for shared caching, unless the cache is able to make equivalent access control decisions to the ones that led to the cached entry."

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

- [RFC 7252 The Constrained Application Protocol (CoAP)](https://www.rfc-editor.org/rfc/rfc7252.html): PROPOSED STANDARD, RFC 7252 (PROPOSED STANDARD, June 2014), checked 2026-10-06.
