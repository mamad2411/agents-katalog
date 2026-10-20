---
name: time-zone-database
description: >-
  IANA Time Zone Database: use tz identifiers and data correctly, as maintained under RFC 6557. Covers RFC 6557 Procedures for Maintaining the Time Zone Database. Use when using the IANA time zone database. Triggers: time zone, RFC 6557, tzdb.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Procedures for Maintaining the Time Zone Database

Procedures for Maintaining the Time Zone Database

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when using the IANA time zone database.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 6557 Procedures for Maintaining the Time Zone Database (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 6557 § 3.** "The TZ Coordinator is empowered to decide, as the designated expert, appropriate changes, but SHOULD take into account views expressed on the mailing list."
2. **RFC 6557 § 3.** "Moving forward, the TZ database, supporting code, and any appropriate supporting information SHOULD be cryptographically signed prior to release using well known public keys, along with any appropriate supporting information and distributed from <http://www.iana.org/time-zones>."
3. **RFC 6557 § 3.** "New TZ names (e.g., locations) are only to be created when the scope of the region a name was envisioned to cover is no longer accurate."
4. **RFC 6557 § 3.** "In order to correct historical inaccuracies, a new TZ name MAY be added when it is necessary to indicate what was the consensus view at a given time and location."
5. **RFC 6557 § 3.** "Changes to existing entries SHALL reflect the consensus on the ground in the region covered by that entry."
6. **RFC 6557 § 3.** "To be clear, the TZ Coordinator SHALL NOT set time zone policy for a region but use judgment and whatever available sources exist to assess what the average person on street would think the time actually is, or in case of historical corrections, was."
7. **RFC 6557 § 6.** "The reference implementation shall be distributed along with an associated cryptographic signature verifiable by a public key."
8. **RFC 6557 § 7.** "The TZ database itself is not an IETF Contribution or an IETF document."
9. **RFC 6557 § 9.** "This memo states that the TZ database SHOULD be distributed with a valid cryptographic signature moving forward."

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

- [RFC 6557 Procedures for Maintaining the Time Zone Database](https://www.rfc-editor.org/rfc/rfc6557.html): BEST CURRENT PRACTICE, RFC 6557 (BEST CURRENT PRACTICE, February 2), checked 2026-10-06.
