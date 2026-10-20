---
name: jmap
description: >-
  JMAP (RFC 8620, RFC 8621): synchronize mail and other data with the JSON Meta Application Protocol. Covers RFC 8620 The JSON Meta Application Protocol (JMAP), RFC 8621 The JSON Meta Application Protocol (JMAP) for Mail. Use when synchronizing mail with JMAP. Triggers: JMAP, RFC 8620.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# The JSON Meta Application Protocol (JMAP)

The JSON Meta Application Protocol (JMAP)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when synchronizing mail with JMAP.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 8620 The JSON Meta Application Protocol (JMAP) (default); RFC 8621 The JSON Meta Application Protocol (JMAP) for Mail (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 8620 § 1.5.** "All data sent from the client to the server or from the server to the client (except binary file upload/download) MUST be valid I-JSON according to the RFC and is therefore case sensitive and encoded in UTF-8 [RFC3629]."
2. **RFC 8620 § 1.7.** "All HTTP requests MUST use the "https://" scheme (HTTP over TLS [RFC2818])."
3. **RFC 8620 § 1.7.** "All HTTP requests MUST be authenticated."
4. **RFC 8620 § 1.8.** "The client MUST opt in to use an extension by passing the appropriate capability identifier in the "using" array of the Request object, as described in Section 3.3."
5. **RFC 8620 § 3.3.** "The method calls MUST be processed sequentially, in order."
6. **RFC 8620 § 3.6.2.** "If a method encounters an error, the appropriate "error" response MUST be inserted at the current point in the "methodResponses" array and, unless otherwise specified, further processing MUST NOT happen within that method call."
7. **RFC 8620 § 3.6.2.** "With the exception of when the "serverPartialFail" error is returned, the externally visible state of the server MUST NOT have changed if an error is returned at the method level."
8. **RFC 8620 § 5.3.** "It is permissible for the server to commit changes to some objects but not others; however, it MUST NOT only commit part of an update to a single record (e.g., update a "name" property but not a "count" property, if both are supplied in the update object)."
9. **RFC 8620 § 8.1.** "To ensure the confidentiality and integrity of data sent and received via JMAP, all requests MUST use TLS 1.2 [RFC5246] [RFC8446] or later, following the recommendations in [RFC7525]."
10. **RFC 8620 § 8.1.** "Clients MUST validate TLS certificate chains to protect against man-in-the-middle attacks [RFC5280]."
11. **RFC 8621 § 7.5.** "The server MUST remove any Bcc header field present on the message during delivery."

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

- [RFC 8620 The JSON Meta Application Protocol (JMAP)](https://www.rfc-editor.org/rfc/rfc8620.html): PROPOSED STANDARD, RFC 8620 (PROPOSED STANDARD, July 2019), checked 2026-10-06.
- [RFC 8621 The JSON Meta Application Protocol (JMAP) for Mail](https://www.rfc-editor.org/rfc/rfc8621.html): PROPOSED STANDARD, RFC 8621 (PROPOSED STANDARD, August 201), checked 2026-10-06.
