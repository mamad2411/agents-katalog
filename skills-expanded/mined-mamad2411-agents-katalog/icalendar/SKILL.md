---
name: icalendar
description: >-
  iCalendar (RFC 5545): read and write calendar events, to-dos and recurrence rules, plus jCal and JSCalendar. Covers RFC 5545 Internet Calendaring and Scheduling Core Object Specification (iCalendar), RFC 7265 jCal: The JSON Format for iCalendar, RFC 8984 JSCalendar: A JSON Representation of Calendar Data. Use when reading or writing calendar data. Triggers: iCalendar, RFC 5545, JSCalendar.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Internet Calendaring and Scheduling Core Object Specification (iCalendar)

Internet Calendaring and Scheduling Core Object Specification (iCalendar)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when reading or writing calendar data.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 5545 Internet Calendaring and Scheduling Core Object Specification (iCalendar) (default); RFC 7265 jCal: The JSON Format for iCalendar (default); RFC 8984 JSCalendar: A JSON Representation of Calendar Data (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 5545 § 3.1.** "Lines of text SHOULD NOT be longer than 75 octets, excluding the line break."
2. **RFC 5545 § 3.1.** "When parsing a content line, folded lines MUST first be unfolded according to the unfolding procedure described above."
3. **RFC 5545 § 3.2.** "Applications MUST ignore x-param and iana-param values they don't recognize."
4. **RFC 5545 § 3.3.5.** "The "TZID" property parameter MUST NOT be applied to DATE-TIME properties whose time values are specified in UTC."
5. **RFC 5545 § 3.3.10.** "Compliant applications MUST accept rule parts ordered in any sequence, but to ensure backward compatibility with applications that pre-date this revision of iCalendar the FREQ rule part MUST be the first rule part specified in a RECUR value."
6. **RFC 5545 § 3.3.11.** "A BACKSLASH character in a "TEXT" property value MUST be escaped with another BACKSLASH character."
7. **RFC 5545 § 3.6.5.** "An individual "VTIMEZONE" calendar component MUST be specified for each unique "TZID" parameter value specified in the iCalendar object."
8. **RFC 5545 § 3.8.4.7.** "The "UID" itself MUST be a globally unique identifier."
9. **RFC 7265 § 3.1.** "When converting from iCalendar to jCal: First, iCalendar lines MUST be unfolded. Afterwards, any iCalendar escaping MUST be unescaped. Finally, JSON escaping, as described in Section 7 of [RFC7159], MUST be applied."
10. **RFC 8984 § 3.** "A JSCalendar object is a JSON object [RFC8259], which MUST be valid I-JSON (a stricter subset of JSON) [RFC7493]."
11. **RFC 8984 § 1.4.9.** "Implementations MUST reject a PatchObject in its entirety if any of its patches are invalid."

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

- [RFC 5545 Internet Calendaring and Scheduling Core Object Specification (iCalendar)](https://www.rfc-editor.org/rfc/rfc5545.html): PROPOSED STANDARD, RFC 5545 (PROPOSED STANDARD, September ), checked 2026-10-06.
- [RFC 7265 jCal: The JSON Format for iCalendar](https://www.rfc-editor.org/rfc/rfc7265.html): PROPOSED STANDARD, RFC 7265 (PROPOSED STANDARD, May 2014), checked 2026-10-06.
- [RFC 8984 JSCalendar: A JSON Representation of Calendar Data](https://www.rfc-editor.org/rfc/rfc8984.html): PROPOSED STANDARD, RFC 8984 (PROPOSED STANDARD, July 2021), checked 2026-10-06.
