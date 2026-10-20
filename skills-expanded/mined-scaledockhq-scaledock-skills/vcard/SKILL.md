---
name: vcard
description: >-
  vCard (RFC 6350): read and write contact data, plus jCard and JSContact. Covers RFC 6350 vCard Format Specification, RFC 7095 jCard: The JSON Format for vCard, RFC 9553 JSContact: A JSON Representation of Contact Data. Use when reading or writing contact data. Triggers: vCard, RFC 6350, JSContact.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# vCard Format Specification

vCard Format Specification

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading or writing contact data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 6350 vCard Format Specification (default); RFC 7095 jCard: The JSON Format for vCard (default); RFC 9553 JSContact: A JSON Representation of Contact Data (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 6350 § 3.2.** "Content lines SHOULD be folded to a maximum width of 75 octets, excluding the line break."
2. **RFC 6350 § 3.3.** "A vCard object MUST include the VERSION and FN properties."
3. **RFC 6350 § 3.4.** "Finally, BACKSLASH characters in values MUST be escaped with a BACKSLASH character."
4. **RFC 6350 § 3.4.** "NEWLINE (U+000A) characters in values MUST be encoded by two characters: a BACKSLASH followed by either an 'n' (U+006E) or an 'N' (U+004E)."
5. **RFC 6350 § 5.** "Applications MUST ignore x-param and iana-param values they don't recognize."
6. **RFC 6350 § 10.1.** ""charset": as defined for text/plain [RFC2046]; encodings other than UTF-8 [RFC3629] MUST NOT be used."
7. **RFC 7095 § 3.2.** "Although [RFC6350] defines BEGIN and END to be properties, they MUST NOT appear as properties of the jCard."
8. **RFC 7095 § 3.4.** "The name of the parameter MUST be in lowercase; the original case of the parameter value MUST be preserved."
9. **RFC 9553 § 1.3.** "All JSContact data MUST be valid according to the constraints given in I-JSON [RFC7493]."
10. **RFC 9553 § 1.4.3.** "Implementations MUST reject a PatchObject in its entirety if any of its patches are invalid."
11. **RFC 9553 § 1.8.1.** "Implementations MUST preserve vendor-specific properties in JSContact data, irrespective if they know their use."

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

- [RFC 6350 vCard Format Specification](https://www.rfc-editor.org/rfc/rfc6350.html): PROPOSED STANDARD, RFC 6350 (PROPOSED STANDARD, August 201), checked 2026-10-06.
- [RFC 7095 jCard: The JSON Format for vCard](https://www.rfc-editor.org/rfc/rfc7095.html): PROPOSED STANDARD, RFC 7095 (PROPOSED STANDARD, January 20), checked 2026-10-06.
- [RFC 9553 JSContact: A JSON Representation of Contact Data](https://www.rfc-editor.org/rfc/rfc9553.html): PROPOSED STANDARD, RFC 9553 (PROPOSED STANDARD, May 2024), checked 2026-10-06.
