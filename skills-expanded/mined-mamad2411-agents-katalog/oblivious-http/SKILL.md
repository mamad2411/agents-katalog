---
name: oblivious-http
description: >-
  Oblivious HTTP: This document describes Oblivious HTTP, a protocol for forwarding encrypted HTTP messages. Covers RFC 9458 Oblivious HTTP. Use when sending a request through an oblivious relay. Triggers: Oblivious HTTP, RFC 9458.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Oblivious HTTP

This document describes Oblivious HTTP, a protocol for forwarding encrypted HTTP messages. Oblivious HTTP allows a client to make multiple requests to an origin server without that server being able to link those requests to the client or to identify the requests as having come from the same client, while placing only limited trust in the nodes used to forward the messages. ¶

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sending a request through an oblivious relay.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 9458 Oblivious HTTP (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 9458 § 3.** "In order to ensure that Clients do not encapsulate messages that other entities can intercept, the key configuration MUST be authenticated and have integrity protection."
2. **RFC 9458 § 5.2.** "A server that receives an invalid message for any reason MUST generate an HTTP response with a 4xx status code."
3. **RFC 9458 § 5.2.** "Errors detected by the Oblivious Gateway Resource after successfully removing encapsulation and errors detected by the Target Resource MUST be sent in an Encapsulated Response."
4. **RFC 9458 § 6.** "Requests from the Client to Oblivious Relay Resource and from Oblivious Relay Resource to Oblivious Gateway Resource MUST use HTTPS in order to provide unlinkability in the presence of a network observer."
5. **RFC 9458 § 6.1.** "Clients MUST generate a new HPKE context for every request, using a good source of entropy [RANDOM] for generating keys."
6. **RFC 9458 § 6.1.** "The request that carries the Encapsulated Request and that is sent to the Oblivious Relay Resource MUST NOT include identifying information unless the Client can trust that this information is removed by the relay."
7. **RFC 9458 § 6.2.** "A relay MUST NOT add information when forwarding requests that might be used to identify Clients, except for information that a Client is aware of; see Section 6.2.1."
8. **RFC 9458 § 6.4.** "A server MUST ensure that the HPKE keys it uses are not valid for any other protocol that uses HPKE with the "message/bhttp request" label."
9. **RFC 9458 § 6.5.** "A Client or Oblivious Relay Resource MUST NOT automatically attempt to retry a failed request unless it receives a positive signal indicating that the request was not processed or forwarded."
10. **RFC 9458 § 6.5.2.** "When retrying a request, the Client MUST create a fresh encryption of the modified request, using a new HPKE context."

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

- [RFC 9458 Oblivious HTTP](https://www.rfc-editor.org/rfc/rfc9458.html): PROPOSED STANDARD, RFC 9458 (PROPOSED STANDARD, January 20), checked 2026-10-06.
