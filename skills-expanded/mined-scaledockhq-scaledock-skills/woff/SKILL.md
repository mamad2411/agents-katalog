---
name: woff
description: >-
  WOFF: Based on experience with WOFF 1.0, which is widely deployed, this specification was developed to provide improved compression and thus lower use of network bandwidth, while still allowing fast decompression even on mobile devices. Covers WOFF File Format 2.0. Use when packaging web fonts. Triggers: WOFF, WOFF 2.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WOFF

Based on experience with WOFF 1.0, which is widely deployed, this specification was developed to provide improved compression and thus lower use of network bandwidth, while still allowing fast decompression even on mobile devices. This is achieved by combining a content-aware preprocessing step and improved entropy coding, compared to the Flate compression used in WOFF 1.0.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when packaging web fonts.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WOFF File Format 2.0 (default); WOFF File Format 1.0 (legacy: read and upgrade, never author). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Notational Conventions.** "The all-uppercase key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119 [ RFC2119 ]."
2. **2. General Requirements.** "In particular, such linked fonts are only available to the documents that reference them; they MUST NOT be made available to other applications or documents on the user's system ."
3. **3. Overall file structure and basic data types.** "Except for padding with a maximum of three null bytes in places where 4-byte alignment of a table length or block offset is specified, there MUST NOT be any extraneous data between the data blocks or WOFF2 header and table directory, or beyond the last such block or table ."
4. **3. Overall file structure and basic data types.** "If such extraneous data is present a conforming user agent MUST reject the file as invalid ."
5. **3. Overall file structure and basic data types.** "The file MUST also be rejected as invalid if the offsets and lengths of any data blocks or font tables indicate overlapping byte ranges of the file, or ranges that would extend beyond the end of the file ."
6. **255UInt16 Data Type.** "An encoder may produce any of these, and a decoder MUST accept them all ."
7. **UIntBase128 Data Type.** "A decoder MUST reject the font file if it encounters a UintBase128-encoded value with leading zeros (a value that starts with the byte 0x80), if UintBase128-encoded sequence is longer than 5 bytes, or if a UintBase128-encoded value exceeds 2 32 -1 ."
8. **3.2. WOFF2 Header.** "The signature field in the WOFF2 header MUST contain the value of 0x774F4632 ('wOF2') , which distinguishes it from WOFF 1.0 files."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
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

- [WOFF File Format 2.0](https://www.w3.org/TR/WOFF2/): Recommendation, WOFF2 REC-WOFF2-20240808 (Recommendation, 2024-08-08), checked 2026-10-06.
- [WOFF File Format 1.0](https://www.w3.org/TR/WOFF/): Recommendation, WOFF REC-WOFF-20121213 (Recommendation, 2012-12-13), checked 2026-10-06.
