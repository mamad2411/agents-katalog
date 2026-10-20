---
name: internet-message-format
description: >-
  Internet Message Format (RFC 5322) and MIME: parse and build email headers, bodies and multipart media types. Covers RFC 5322 Internet Message Format, RFC 2045 Multipurpose Internet Mail Extensions (MIME) Part One: Format of Internet Message Bodies, RFC 2046 Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types, RFC 2047 MIME (Multipurpose Internet Mail Extensions) Part Three: Message Header Extensions for Non-ASCII Text, RFC 6838 Media Type Specifications and Registration Procedures, RFC 4289 Multipurpose Internet Mail Extensions (MIME) Part Four: Registration Procedures, RFC 2049 Multipurpose Internet Mail Extensions (MIME) Part Five: Conformance Criteria and Examples. Use when parsing an email message or a MIME body. Triggers: RFC 5322, MIME, RFC 2045.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
  kind: standard
---

# Internet Message Format

Internet Message Format

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when parsing an email message or a MIME body.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 5322 Internet Message Format (default); RFC 2045 Multipurpose Internet Mail Extensions (MIME) Part One: Format of Internet Message Bodies (default); RFC 2046 Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types (default); RFC 2047 MIME (Multipurpose Internet Mail Extensions) Part Three: Message Header Extensions for Non-ASCII Text (default); RFC 2048 Multipurpose Internet Mail Extensions (MIME) Part Four: Registration Procedures (legacy); RFC 4288 Media Type Specifications and Registration Procedures (legacy); RFC 6838 Media Type Specifications and Registration Procedures (default); RFC 4289 Multipurpose Internet Mail Extensions (MIME) Part Four: Registration Procedures (default); RFC 2049 Multipurpose Internet Mail Extensions (MIME) Part Five: Conformance Criteria and Examples (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 5322 § 2.1.1.** "Each line of characters MUST be no more than 998 characters, and SHOULD be no more than 78 characters, excluding the CRLF."
2. **RFC 5322 § 2.2.** "A field body MUST NOT include CR and LF except when used in "folding" and "unfolding", as described in section 2.2.3."
3. **RFC 5322 § 2.3.** "CR and LF MUST only occur together as CRLF; they MUST NOT appear independently in the body."
4. **RFC 5322 § 3.3.** "A date-time specification MUST be semantically valid."
5. **RFC 5322 § 3.6.2.** "If the from field contains more than one mailbox specification in the mailbox-list, then the sender field, containing the field name "Sender" and a single mailbox specification, MUST appear in the message."
6. **RFC 5322 § 3.6.4.** "The message identifier (msg-id) itself MUST be a globally unique identifier for a message."
7. **RFC 5322 § 4.** "Though these syntactic forms MUST NOT be generated according to the grammar in section 3, they MUST be accepted and parsed by a conformant receiver."
8. **RFC 2045 § 6.7.** "Octets with values of 9 and 32 MAY be represented as US-ASCII TAB (HT) and SPACE characters, respectively, but MUST NOT be so represented at the end of an encoded line."
9. **RFC 2046 § 5.1.** "The boundary delimiter MUST NOT appear inside any of the encapsulated parts, on a line by itself or as the prefix of any line."
10. **RFC 2047 § 5.** "An 'encoded-word' MUST NOT appear in any portion of an 'addr-spec'."
11. **RFC 2047 § 6.3.** "However, a mail reader MUST NOT prevent the display or handling of a message because an 'encoded-word' is incorrectly formed."

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

- [RFC 5322 Internet Message Format](https://www.rfc-editor.org/rfc/rfc5322.html): DRAFT STANDARD, RFC 5322 (DRAFT STANDARD, October 20), checked 2026-10-06.
- [RFC 2045 Multipurpose Internet Mail Extensions (MIME) Part One: Format of Internet Message Bodies](https://www.rfc-editor.org/rfc/rfc2045.html): DRAFT STANDARD, RFC 2045 (DRAFT STANDARD, November 1), checked 2026-10-06.
- [RFC 2046 Multipurpose Internet Mail Extensions (MIME) Part Two: Media Types](https://www.rfc-editor.org/rfc/rfc2046.html): DRAFT STANDARD, RFC 2046 (DRAFT STANDARD, November 1), checked 2026-10-06.
- [RFC 2047 MIME (Multipurpose Internet Mail Extensions) Part Three: Message Header Extensions for Non-ASCII Text](https://www.rfc-editor.org/rfc/rfc2047.html): DRAFT STANDARD, RFC 2047 (DRAFT STANDARD, November 1), checked 2026-10-06.
- [RFC 2048 Multipurpose Internet Mail Extensions (MIME) Part Four: Registration Procedures](https://www.rfc-editor.org/rfc/rfc2048.html): BEST CURRENT PRACTICE, RFC 2048 (BEST CURRENT PRACTICE, November 1), checked 2026-10-06.
- [RFC 4288 Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc4288): Best Current Practice, RFC 4288, December 2005, checked 2026-10-06.
- [RFC 4289 Multipurpose Internet Mail Extensions (MIME) Part Four: Registration Procedures](https://www.rfc-editor.org/rfc/rfc4289): Best Current Practice, RFC 4289, December 2005, checked 2026-10-06.
- [RFC 6838 Media Type Specifications and Registration Procedures](https://www.rfc-editor.org/rfc/rfc6838): Best Current Practice, RFC 6838, January 2013, checked 2026-10-06.
- [RFC 2049 Multipurpose Internet Mail Extensions (MIME) Part Five: Conformance Criteria and Examples](https://www.rfc-editor.org/rfc/rfc2049.html): DRAFT STANDARD, RFC 2049 (DRAFT STANDARD, November 1), checked 2026-10-06.
